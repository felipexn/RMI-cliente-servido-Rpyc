import rpyc
import os
from tkinter import *
from tkinter import filedialog
import customtkinter
from tkinter import messagebox
import shutil
from PIL import Image, ImageTk
import subprocess
import sys

class FileManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciador de Arquivos")
        self.root.geometry("650x400")
        self.root.config(background="#2F3136")

        # Conecta ao servidor
        self.conn = rpyc.connect("localhost", 4001, config={"allow_all_attrs": True})
        self.remote_service = self.conn.root

        # Obtem o ID do cliente
        self.client_id = self.remote_service.exposed_get_client_id()
        if self.client_id is None:
            raise Exception("Nao foi possivel obter o ID do cliente do servidor.")

        self.filename = ""
        self.setup_ui()

    def setup_ui(self):
        self.frame = customtkinter.CTkLabel(self.root, text="")
        self.frame.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky='n')

        self.button_upload = customtkinter.CTkButton(master=self.root, text="Escolher Arquivo", command=self.select_file)
        self.button_upload.grid(row=1, column=0, padx=10, pady=10)

        self.path_entry = customtkinter.CTkEntry(master=self.root, width=200)
        self.path_entry.grid(row=1, column=1, padx=10, pady=10)

        self.save_btn = customtkinter.CTkButton(master=self.root, text="Upload", width=50, command=self.upload_file)
        self.save_btn.grid(row=1, column=2, padx=10, pady=10)

        self.button_query_file = customtkinter.CTkButton(master=self.root, text="Mostrar Arquivos", command=self.show_files)
        self.button_query_file.grid(row=2, column=0, padx=10, pady=10)

        self.button_register_interest = customtkinter.CTkButton(master=self.root, text="Registrar Interesse", command=self.register_interest)
        self.button_register_interest.grid(row=2, column=1, padx=10, pady=10)

        self.button_cancel_interest = customtkinter.CTkButton(master=self.root, text="Cancelar Interesse", command=self.cancel_interest)
        self.button_cancel_interest.grid(row=2, column=2, padx=10, pady=10)

        self.button_download_file = customtkinter.CTkButton(master=self.root, text="Download Arquivo", command=self.download_file)
        self.button_download_file.grid(row=3, column=0, padx=10, pady=10)

        self.button_show_file_interest = customtkinter.CTkButton(master=self.root, text="Mostrar Arquivos com Interesse", command=self.show_files_with_interest)
        self.button_show_file_interest.grid(row=3, column=1, padx=10, pady=10)

    def select_file(self):
        self.filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Selecionar Arquivo")
        self.path_entry.delete(0, END)
        self.path_entry.insert(0, self.filename)
        

    def upload_file(self):
        if not self.filename:
            messagebox.showerror("Erro", "Nenhum arquivo selecionado.")
            return

        target_dir = os.path.join(os.getcwd(), "arquivos")
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        target_path = os.path.join(target_dir, os.path.basename(self.filename))
        shutil.copy(self.filename, target_path)

        try:
            with open(target_path, "rb") as f:
                data = f.read()
        except Exception as e:
            messagebox.showerror("Erro", f"Nao foi possivel ler o arquivo: {e}")
            return

        file_name = os.path.basename(target_path)
        try:
            response = self.remote_service.exposed_upload_file(file_name, data)
            messagebox.showinfo("Sucesso", response)
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao fazer o upload do arquivo: {e}")
    
        self.path_entry.delete(0, END)
        self.open_file(target_path)

    def show_files(self):
        try:
            files = self.remote_service.exposed_list_files()
            if files:
                messagebox.showinfo("Arquivos Disponiveis", "\n".join(files))
            else:
                messagebox.showinfo("Arquivos Disponiveis", "Nenhum arquivo disponivel no servidor.")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao listar arquivos: {e}")

    def register_interest(self):
        textDialog = customtkinter.CTkInputDialog(text="Digite o Nome do Arquivo de Interesse", title="Marcar Interesse")
        file = textDialog.get_input()
        if file:
            try:
                durationDialog = customtkinter.CTkInputDialog(text="Digite a Duracao do Interesse (em segundos)", title="Duracao do Interesse")
                duration = int(durationDialog.get_input())
                if duration <= 0:
                    raise ValueError("A duracao deve ser um numero positivo.")
                response = self.remote_service.exposed_register_interest(file, self.client_id, duration)
                messagebox.showinfo("Sucesso", response)
            except ValueError as ve:
                messagebox.showerror("Erro", f"Valor invalido: {ve}")
            except Exception as e:
                messagebox.showerror("Erro", f"Ocorreu um erro ao marcar interesse: {e}")

    def cancel_interest(self):
        textDialog = customtkinter.CTkInputDialog(text="Digite o Nome do Arquivo para Cancelar Interesse", title="Cancelar Interesse")
        file = textDialog.get_input()
        if file:
            try:
                response = self.remote_service.exposed_cancel_interest(file, self.client_id)
                messagebox.showinfo("Sucesso", response)
            except Exception as e:
                messagebox.showerror("Erro", f"Ocorreu um erro ao cancelar interesse: {e}")

    def show_files_with_interest(self):
        try:
            files_with_interest = self.remote_service.exposed_list_files_with_interest()
            if files_with_interest:
                messagebox.showinfo("Arquivos com Interesse", "\n".join(files_with_interest))
            else:
                messagebox.showinfo("Arquivos com Interesse", "Nenhum arquivo com interesse registrado.")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao obter arquivos com interesse: {e}")

    def download_file(self):
        textDialog = customtkinter.CTkInputDialog(text="Digite o Nome do Arquivo para Download", title="Download Arquivo")
        file = textDialog.get_input()
        if file:
            try:
                data = self.remote_service.exposed_download_file(file)
                if isinstance(data, bytes):
                    with open(os.path.join(os.getcwd(), file), "wb") as f:
                        f.write(data)
                    messagebox.showinfo("Sucesso", f"Arquivo {file} baixado com sucesso.")
                else:
                    messagebox.showinfo("Erro", data)
            except Exception as e:
                messagebox.showerror("Erro", f"Ocorreu um erro ao baixar o arquivo: {e}")
     # Metodo que sera chamado pelo servidor para notificar o cliente
    def exposed_notify_event(self, file):
        self.root.after(0, lambda: messagebox.showinfo("Notificacao", f"O arquivo {file} esta disponivel para download."))
"""
    def open_file(self, file_path):
        if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            self.open_image(file_path)
        elif file_path.lower().endswith('.txt'):
            self.open_text_file(file_path)
        else:
            self.open_with_default_application(file_path)

    def open_image(self, image_path):
        img = Image.open(image_path)
        img = img.resize((250, 250), Image.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)
     

    def open_text_file(self, text_file_path):
        try:
            with open(text_file_path, "r", encoding="utf-8") as f:
                content = f.read()
            messagebox.showinfo("Conteudo do Arquivo", content)
        except Exception as e:
            messagebox.showerror("Erro", f"Nao foi possivel ler o arquivo de texto: {e}")

    def open_with_default_application(self, file_path):

        try:
            if os.name == 'nt':
                os.startfile(file_path)
            elif os.name == 'posix':
                subprocess.call(('open', file_path) if sys.platform == 'darwin' else ('xdg-open', file_path))
        except Exception as e:
            messagebox.showerror("Erro", f"Nao foi possivel abrir o arquivo: {e}")

"""

   

if __name__ == "__main__":
    root = customtkinter.CTk()
    app = FileManagerApp(root)
    root.mainloop()
