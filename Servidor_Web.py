from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime, timezone

SENHA_CORRETA = "BOBESPONJA"
TAMANHO_MAXIMO = 1024  # 1 KB

def http_date():
    return datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT")

INSTRUCOES_RAIZ = """

Se você digitar apenas curl https://www.google.com no seu terminal, ele vai baixar o código HTML da página e exibir diretamente na sua tela.

1) Use o metodo GET para acessar este servidor e ler esta mensagem.

2) Em seguida, utilize o metodo POST para enviar:
   - A senha correta: BOBESPONJA
   - Uma string qualquer (mensagem livre)

3) A senha deve ser enviada no header:
   Authorization: Basic BOBESPONJA

4) A string deve ser enviada no corpo da requisicao.

Se a senha estiver correta, o servidor respondera com sucesso.
Caso contrario, o acesso sera negado.
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
