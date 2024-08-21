import rpyc
import os
import time
import logging
from threading import Thread

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class MyService(rpyc.Service):
    client_counter = 0  # Contador global de clientes

    def __init__(self):
        self.base_dir = os.path.join(os.getcwd(), "arquivos")
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)
        self.arquivos = set(os.listdir(self.base_dir))
        self.interesses = {}
        self.clients = {}

        # Iniciar a thread de monitoramento de novos arquivos
        monitor_thread = Thread(target=self.monitor_new_files)
        monitor_thread.daemon = True  # Para garantir que a thread termine junto com o programa
        monitor_thread.start()

    def on_connect(self, conn):
        # Adiciona o cliente à lista quando ele se conecta
        MyService.client_counter += 1
        self.clients[MyService.client_counter] = conn
        logging.info(f"Cliente {MyService.client_counter} conectado.")

    def on_disconnect(self, conn):
        # Remove o cliente da lista quando ele se desconecta
        client_refs = [ref for ref, c in self.clients.items() if c == conn]
        for client_ref in client_refs:
            logging.info(f"Cliente {client_ref} desconectado.")
            del self.clients[client_ref]

    def exposed_get_client_id(self):
        return MyService.client_counter

    def exposed_upload_file(self, file, data):
        file_path = os.path.join(self.base_dir, file)
        try:
            with open(file_path, "wb") as f:
                f.write(data)
            self.arquivos.add(file)  # Adicionar o arquivo à lista de arquivos monitorados
            return f"Arquivo {file} carregado com sucesso."
        except Exception as e:
            logging.error(f"Erro ao carregar o arquivo {file}: {e}")
            return f"Erro ao carregar o arquivo {file}: {e}"

    def monitor_new_files(self):
        while True:
            time.sleep(5)  # Verificar novos arquivos a cada 5 segundos
            current_files = set(os.listdir(self.base_dir))
            new_files = current_files - self.arquivos  # Identificar arquivos novos
            if new_files:
                self.arquivos.update(new_files)  # Atualizar a lista de arquivos monitorados
                for new_file in new_files:
                    self.notify_interested_clients(new_file)

    def notify_interested_clients(self, file):
        self.clean_expired_interests()  # Limpa interesses expirados antes de notificar
        if file in self.interesses:
            for client_ref, _ in self.interesses[file]:
                if client_ref in self.clients:
                    try:
                        client_conn = self.clients[client_ref]
                        # Verificar se o método 'exposed_notify_event' existe
                        if hasattr(client_conn.root, 'exposed_notify_event'):
                            client_conn.root.exposed_notify_event(file)  # Notifica o cliente
                            logging.info(f"Notificacao enviada para o cliente {client_ref} sobre o arquivo {file}.")
                        else:
                            logging.warning(f"Cliente {client_ref} nao tem o metodo 'exposed_notify_event'.")
                    except Exception as e:
                        logging.error(f"Erro ao notificar cliente {client_ref} sobre o arquivo {file}: {e}")

    def exposed_register_interest(self, file, client_ref, duration):
        if file not in self.interesses:
            self.interesses[file] = []
        expiry_time = time.time() + duration
        self.interesses[file].append((client_ref, expiry_time))
        logging.info(f"Interesse registrado em {file} por {duration} segundos para o cliente {client_ref}.")
        return f"Interesse registrado em {file} por {duration} segundos."

    def exposed_cancel_interest(self, file, client_ref):
        if file in self.interesses:
            self.interesses[file] = [i for i in self.interesses[file] if i[0] != client_ref]
            if not self.interesses[file]:
                del self.interesses[file]
        logging.info(f"Interesse cancelado para o arquivo {file} pelo cliente {client_ref}.")
        return f"Interesse cancelado para o arquivo {file}."

    def exposed_list_files(self):
        return [f for f in os.listdir(self.base_dir) if os.path.isfile(os.path.join(self.base_dir, f))]

    def exposed_download_file(self, file):
        file_path = os.path.join(self.base_dir, file)
        if os.path.exists(file_path):
            try:
                with open(file_path, "rb") as f:
                    return f.read()
            except Exception as e:
                logging.error(f"Erro ao ler o arquivo {file}: {e}")
                return f"Erro ao ler o arquivo {file}: {e}"
        else:
            return f"{file} nao encontrado"

    def exposed_list_files_with_interest(self):
        self.clean_expired_interests()  # Limpa interesses expirados antes de listar
        files_with_interest = [
            file for file, interests in self.interesses.items()
            if any(expiry_time > time.time() for _, expiry_time in interests)
        ]
        return files_with_interest

    def clean_expired_interests(self):
        current_time = time.time()
        expired_files = []
        for file in list(self.interesses.keys()):
            self.interesses[file] = [
                (client_ref, expiry_time)
                for client_ref, expiry_time in self.interesses[file]
                if expiry_time > current_time
            ]
            if not self.interesses[file]:
                expired_files.append(file)
        for file in expired_files:
            del self.interesses[file]
        if expired_files:
            logging.info(f"Interesses expirados removidos: {', '.join(expired_files)}")

if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer
    server = ThreadedServer(MyService, port=4001)
    server.start()
