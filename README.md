<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gerenciador de Arquivos com RPyC e Tkinter</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 20px;
            color: #333;
        }
        h1, h2, h3 {
            color: #007BFF;
        }
        pre {
            background: #f4f4f4;
            border: 1px solid #ddd;
            padding: 10px;
            overflow-x: auto;
        }
        code {
            background: #f4f4f4;
            border: 1px solid #ddd;
            padding: 2px 4px;
            border-radius: 3px;
        }
        a {
            color: #007BFF;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <h1>Gerenciador de Arquivos com RPyC e Tkinter</h1>

    <p>Este projeto consiste em um sistema de gerenciamento de arquivos que utiliza a biblioteca RPyC para comunicação entre cliente e servidor, e a biblioteca Tkinter para a interface gráfica do usuário (GUI). O sistema permite o upload, download e gerenciamento de arquivos com suporte a notificações de interesse.</p>

    <h2>Estrutura do Projeto</h2>
    <p>O projeto é dividido em duas partes principais:</p>
    <ul>
        <li><strong>Cliente (GUI)</strong>: Uma aplicação Tkinter que se conecta ao servidor RPyC e fornece uma interface para o usuário interagir com o sistema de arquivos.</li>
        <li><strong>Servidor</strong>: Um serviço RPyC que gerencia arquivos, interesses de clientes e notifica clientes sobre novos arquivos.</li>
    </ul>

    <h2>Funcionalidades</h2>
    <h3>Cliente</h3>
    <ul>
        <li><strong>Escolher Arquivo</strong>: Permite selecionar um arquivo para upload.</li>
        <li><strong>Upload</strong>: Envia o arquivo selecionado para o servidor.</li>
        <li><strong>Mostrar Arquivos</strong>: Lista todos os arquivos disponíveis no servidor.</li>
        <li><strong>Registrar Interesse</strong>: Registra interesse em um arquivo específico com uma duração em segundos.</li>
        <li><strong>Cancelar Interesse</strong>: Cancela o interesse registrado em um arquivo.</li>
        <li><strong>Download Arquivo</strong>: Baixa um arquivo do servidor.</li>
        <li><strong>Mostrar Arquivos com Interesse</strong>: Lista arquivos que têm interesse registrado.</li>
        <li><strong>Notificação</strong>: Recebe notificações quando um arquivo de interesse se torna disponível.</li>
    </ul>

    <h3>Servidor</h3>
    <ul>
        <li><strong>Upload de Arquivo</strong>: Recebe arquivos do cliente e os salva no diretório especificado.</li>
        <li><strong>Listar Arquivos</strong>: Retorna uma lista de arquivos disponíveis no diretório.</li>
        <li><strong>Registrar Interesse</strong>: Adiciona um cliente à lista de interessados em um arquivo com uma duração específica.</li>
        <li><strong>Cancelar Interesse</strong>: Remove o interesse de um cliente por um arquivo.</li>
        <li><strong>Listar Arquivos com Interesse</strong>: Retorna uma lista de arquivos que têm interesse registrado.</li>
        <li><strong>Download de Arquivo</strong>: Envia um arquivo para o cliente.</li>
        <li><strong>Notificação</strong>: Notifica os clientes interessados quando novos arquivos são adicionados ao diretório monitorado.</li>
    </ul>

    <h2>Dependências</h2>
    <ul>
        <li><code>rpyc</code></li>
        <li><code>tkinter</code></li>
        <li><code>customtkinter</code></li>
        <li><code>Pillow</code> (para manipulação de imagens)</li>
        <li><code>shutil</code> (para operações de arquivos e diretórios)</li>
    </ul>

    <h2>Como Executar</h2>
    <h3>Configuração do Servidor</h3>
    <ol>
        <li>Navegue até o diretório que contém o arquivo <code>server.py</code>.</li>
        <li>Execute o servidor com o comando:</li>
        <pre><code>python server.py</code></pre>
    </ol>

    <h3>Configuração do Cliente</h3>
    <ol>
        <li>Navegue até o diretório que contém o arquivo <code>client.py</code>.</li>
        <li>Execute o cliente com o comando:</li>
        <pre><code>python client.py</code></pre>
    </ol>

    <h2>Detalhes da Implementação</h2>
    <h3>Cliente (<code>client.py</code>)</h3>
    <p>A interface é construída usando <code>customtkinter</code>, que é uma extensão personalizada do Tkinter. O cliente se conecta ao servidor RPyC na porta 4001 e fornece várias funcionalidades para upload, download e gerenciamento de arquivos. Notificações são gerenciadas por meio do método <code>exposed_notify_event</code>, que é chamado pelo servidor quando novos arquivos são detectados.</p>

    <h3>Servidor (<code>server.py</code>)</h3>
    <p>O servidor é implementado como um serviço RPyC que gerencia arquivos e interesses dos clientes. Usa uma thread separada para monitorar novos arquivos no diretório de armazenamento. Notifica clientes interessados sobre a disponibilidade de novos arquivos e limpa interesses expirados periodicamente.</p>

    <h2>Exemplo de Uso</h2>
    <ol>
        <li>Inicie o servidor (<code>server.py</code>).</li>
        <li>Inicie o cliente (<code>client.py</code>).</li>
        <li>Use a interface gráfica do cliente para selecionar, fazer upload e baixar arquivos. Registre e cancele interesse conforme necessário.</li>
    </ol>

    <h2>Contribuições</h2>
    <p>Se você deseja contribuir para o projeto, por favor, faça um fork do repositório e envie um pull request com suas alterações.</p>

    <h2>Licença</h2>
    <p>Este projeto está licenciado sob a Licença MIT - veja o arquivo <code>LICENSE</code> para detalhes.</p>
</body>
</html>
