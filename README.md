# Gerenciador de Arquivos com RPyC e Tkinter

Este projeto consiste em um sistema de gerenciamento de arquivos que utiliza a biblioteca RPyC para comunicação entre cliente e servidor, e a biblioteca Tkinter para a interface gráfica do usuário (GUI). O sistema permite o upload, download e gerenciamento de arquivos com suporte a notificações de interesse.

## Estrutura do Projeto

O projeto é dividido em duas partes principais:

- **Cliente (GUI)**: Uma aplicação Tkinter que se conecta ao servidor RPyC e fornece uma interface para o usuário interagir com o sistema de arquivos.
- **Servidor**: Um serviço RPyC que gerencia arquivos, interesses de clientes e notifica clientes sobre novos arquivos.

## Funcionalidades

### Cliente

- **Escolher Arquivo**: Permite selecionar um arquivo para upload.
- **Upload**: Envia o arquivo selecionado para o servidor.
- **Mostrar Arquivos**: Lista todos os arquivos disponíveis no servidor.
- **Registrar Interesse**: Registra interesse em um arquivo específico com uma duração em segundos.
- **Cancelar Interesse**: Cancela o interesse registrado em um arquivo.
- **Download Arquivo**: Baixa um arquivo do servidor.
- **Mostrar Arquivos com Interesse**: Lista arquivos que têm interesse registrado.
- **Notificação**: Recebe notificações quando um arquivo de interesse se torna disponível.

### Servidor

- **Upload de Arquivo**: Recebe arquivos do cliente e os salva no diretório especificado.
- **Listar Arquivos**: Retorna uma lista de arquivos disponíveis no diretório.
- **Registrar Interesse**: Adiciona um cliente à lista de interessados em um arquivo com uma duração específica.
- **Cancelar Interesse**: Remove o interesse de um cliente por um arquivo.
- **Listar Arquivos com Interesse**: Retorna uma lista de arquivos que têm interesse registrado.
- **Download de Arquivo**: Envia um arquivo para o cliente.
- **Notificação**: Notifica os clientes interessados quando novos arquivos são adicionados ao diretório monitorado.

## Dependências

- `rpyc`
- `tkinter`
- `customtkinter`
- `Pillow` (para manipulação de imagens)
- `shutil` (para operações de arquivos e diretórios)

## Como Executar

### Configuração do Servidor

1. Navegue até o diretório que contém o arquivo `server.py`.
2. Execute o servidor com o comando:

    ```bash
    python server.py
    ```

### Configuração do Cliente

1. Navegue até o diretório que contém o arquivo `client.py`.
2. Execute o cliente com o comando:

    ```bash
    python client.py
    ```

## Detalhes da Implementação

### Cliente (`client.py`)

A interface é construída usando `customtkinter`, que é uma extensão personalizada do Tkinter. O cliente se conecta ao servidor RPyC na porta 4001 e fornece várias funcionalidades para upload, download e gerenciamento de arquivos. Notificações são gerenciadas por meio do método `exposed_notify_event`, que é chamado pelo servidor quando novos arquivos são detectados.

### Servidor (`server.py`)

O servidor é implementado como um serviço RPyC que gerencia arquivos e interesses dos clientes. Usa uma thread separada para monitorar novos arquivos no diretório de armazenamento. Notifica clientes interessados sobre a disponibilidade de novos arquivos e limpa interesses expirados periodicamente.

## Exemplo de Uso

1. Inicie o servidor (`server.py`).
2. Inicie o cliente (`client.py`).
3. Use a interface gráfica do cliente para selecionar, fazer upload e baixar arquivos. Registre e cancele interesse conforme necessário.

## Contribuições

Se você deseja contribuir para o projeto, por favor, faça um fork do repositório e envie um pull request com suas alterações.

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo `LICENSE` para detalhes.
