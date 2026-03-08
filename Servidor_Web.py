from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime, timezone

SENHA_CORRETA = "BOBESPONJA"
TAMANHO_MAXIMO = 1024  # 1 KB

def http_date():
    return datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT")

INSTRUCOES_RAIZ = """
Esta atividade tem como objetivo capacitar o aluno a compreender, na prática, o funcionamento do protocolo HTTP e o modelo cliente-servidor por meio do uso da ferramenta de linha de comando curl e análise de pacotes usando o software Wireshark. Durante o laboratório, os alunos irão enviar requisições HTTP manualmente e analisar as respostas do servidor, observando como métodos, cabeçalhos e códigos de status são utilizados na comunicação Web.
Ao final deste laboratório, o aluno deverá ser capaz de:

•	Compreender o funcionamento básico do protocolo HTTP no modelo cliente-servidor
•	Enviar requisições HTTP utilizando diferentes métodos (GET e POST) com a ferramenta curl.
•	Interpretar códigos de status HTTP (como 200, 401 e 413) retornados por um servidor
•	Analisar cabeçalhos HTTP presentes nas requisições e respostas usando o Wireshark.


Sobre a Atividade:

* Use o metodo GET (padrão do cURL) para acessar este servidor e ler esta mensagem.

* Na atividade para autenticar, a senha deve ser enviada no header:
   Authorization: Basic BOBESPONJA

* O teste de cookie deve ser feito passando o modo=debug
    cookie: modo=debug


O cURL pode ser usado para realizar solicitações em qualquer site, assim como solicitar outros serviços (FTP, SMTP, MQTT, etc). Se você digitar apenas curl https://www.google.com no seu terminal, ele vai baixar o código HTML da página e exibir diretamente na sua tela.

Para maiores informações sobre essa atividade

http://IP:8000/help
http://IP:8000/curl
http://IP:8000/REF
"""

INSTRUCOES_CURL = """ATIVIDADE DE LABORATORIO - HTTP COM CURL


O que é o cURL?

O nome significa "Client for URLs". Basicamente, é uma ferramenta de linha de comando usada para transferir dados de ou para um servidor. Ele suporta quase todos os protocolos que você possa imaginar (HTTP, HTTPS, FTP, SMTP, etc.).

Pense no cURL como um navegador web sem interface gráfica. Enquanto o Chrome ou Firefox renderizam imagens e botões, o cURL foca puramente nos dados e na comunicação.



Estrutura e Sintaxe

A sintaxe básica do cURL é extremamente direta:

curl [opções] [URL]


Principais Opções

Para ser eficiente, você precisa conhecer estas "flags" (opções):

Opção	Nome Longo	Descrição
-X	--request	Especifica o método HTTP (GET, POST, PUT, DELETE).
-I	--head	        Traz apenas o cabeçalho (header) da resposta. Ótimo para debug.
-d	--data	        Envia dados em uma requisição POST (como preencher um formulário).
-H	--header	Adiciona um cabeçalho extra (ex: autenticação ou tipo de conteúdo).
-o	--output	Salva a resposta em um arquivo em vez de exibir no terminal.
-L	--location	Segue redirecionamentos (se a página mudou de endereço).
-v	--verbose	Modo "fofoqueiro": mostra tudo o que está acontecendo na conexão.



Exemplos Práticos:

Fazendo a requisiça de um site:
     curl https://example.com

Fazendo a requisiça de um site e analisando o Cabeçalho de resposta:
     curl -i https://example.com

Adicionando linha de cabeçalho a requisição
    curl https://example.com
    -H "User-Agent: curl/8.7.1"
    
Salvando a resposta em um arquivo
    curl -o instalador.zip https://exemplo.com/

Alterando o Metodo da solicitação
    curl -X POST https://example.com

Verificando toda comunicação HTTP
    curl -v https://example.com

"""

INSTRUCOES_ERRO = """Objeto solicitado não encontrado

opções validas

URL
 ├─ /
 ├─ /curl
 └─ /REF

 lembrando que a URL pode ser no formato http//IP:PORTA
 """ 


INSTRUCOES_REF = """Para entender mais sobre a atividade consulte

Documentação para modulo http.server: https://docs.python.org/3/library/http.server.html

RFC 2616 - Hypertext Transfer Protocol -- HTTP/1.1:  https://datatracker.ietf.org/doc/html/rfc2616

Documentação sobre Curl: https://curl.se

 """


class ServidorLab(BaseHTTPRequestHandler):

    def do_GET(self):
        
        cookie = self.headers.get("Cookie")
                # ativa modo debug
        if cookie == "modo=debug":
            status = 200
            resposta = f"""
-----------------------
MODO DEBUG ATIVADO

Metodo HTTP: {self.command}
URI solicitada: {self.path}
Endereco do cliente: {self.client_address}

Headers recebidos:
User-Agent: {self.headers.get('User-Agent')}
Accept: {self.headers.get('Accept')}
Cookie: {cookie}
"""
        #Se não for acessado o modo debug, o Curl sergue a solicitaçao normal.    
        else: 
            if self.path == "/":
                resposta = INSTRUCOES_RAIZ
                status = 200
            elif self.path == "/curl":
                resposta = INSTRUCOES_CURL
                status = 200
            elif self.path == "/REF":
                resposta = INSTRUCOES_REF
                status = 200
            else:
                if cookie != "modo=debug":
                    resposta = INSTRUCOES_ERRO
                    status = 404


        corpo = resposta.encode("utf-8")

        self.send_response(status)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(corpo)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("Connection", "close")
        self.end_headers()

        self.wfile.write(corpo)
        
 
            

    def do_HEAD(self):
        if self.path == "/":
            corpo = INSTRUCOES_RAIZ.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(corpo)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("Connection", "close")
            self.end_headers()
            
            self.wfile.write(corpo)
        elif self.path == "/curl":
            corpo = INSTRUCOES_CURL.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(corpo)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("Connection", "close")
            self.end_headers()
            self.wfile.write(corpo)
        elif self.path == "/REF":
            corpo = INSTRUCOES_REF.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(corpo)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("Connection", "close")
            self.end_headers()
            self.wfile.write(corpo)
        
        else:
            corpo = INSTRUCOES_ERRO.encode("utf-8")
            self.send_response(404)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(corpo)))
            self.end_headers()
            self.wfile.write(corpo)
            
    def do_POST(self):
        auth = self.headers.get("Authorization")

        try:
            tamanho = int(self.headers.get("Content-Length", 0))
        except ValueError:
            self.send_response(400)
            self.end_headers()
            return
        
        if tamanho > TAMANHO_MAXIMO:
            corpo = "Payload muito grande (limite: 1024 bytes)\n".encode("utf-8")

            self.send_response(413)  # Payload Too Large
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(corpo)))
            self.send_header("Connection", "close")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()

            self.wfile.write(corpo)
            return

        
        mensagem = self.rfile.read(tamanho).decode("utf-8").strip()

        if auth != f"Basic {SENHA_CORRETA}":
            corpo = "Senha incorreta ou ausente.\n".encode("utf-8")
            self.send_response(401)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(corpo)))
            self.send_header("Date", http_date())
            self.send_header("Server", "Python http.server")
            self.send_header("Connection", "close")
            self.send_header("Cache-Control", "no-store")
            self.send_header("WWW-Authenticate", "Basic")
            self.end_headers()

            self.wfile.write(corpo)
            return
        else:
            resposta = f"""POST RECEBIDO COM SUCESSO

Senha correta.
Mensagem enviada pelo aluno:
"{mensagem}"
"""
            corpo = resposta.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(corpo)))
            self.send_header("Date", http_date())
            self.send_header("Server", "Python http.server")
            self.send_header("Connection", "close")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(corpo)
        
        print("Mensagem recebida:", mensagem, "no endereço:", self.client_address)


    def log_message(self, format, *args):
        return  # silencia log para uso em aula

PORTA = 8000
print(f"Servidor de laboratorio ativo na porta {PORTA}")
print("Aguardando usuários se conectarem......")
HTTPServer(("", PORTA), ServidorLab).serve_forever()
