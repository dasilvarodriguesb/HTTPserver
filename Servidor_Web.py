from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

SENHA_CORRETA = "BOBESPONJA"
TAMANHO_MAXIMO = 1024  # 1 KB
PORTA = 8000
TIMEOUT_CONEXAO = 10  # segundos


INSTRUCOES_RAIZ = """
Esta atividade tem como objetivo capacitar o aluno a compreender, na prática, o funcionamento do protocolo HTTP e o modelo cliente-servidor por meio do uso da ferramenta de linha de comando curl e análise de pacotes usando o software Wireshark. Durante o laboratório, os alunos irão enviar requisições HTTP manualmente e analisar as respostas do servidor, observando como métodos, cabeçalhos e códigos de status são utilizados na comunicação Web.

Ao final deste laboratório, o aluno deverá ser capaz de:

• Compreender o funcionamento básico do protocolo HTTP no modelo cliente-servidor
• Enviar requisições HTTP utilizando diferentes métodos (GET e POST) com a ferramenta curl.
• Interpretar códigos de status HTTP (como 200, 401 e 413) retornados por um servidor
• Analisar cabeçalhos HTTP presentes nas requisições e respostas usando o Wireshark.


Sobre a Atividade:

* Use o metodo GET (padrão do cURL) para acessar este servidor e ler esta mensagem.

* Na atividade para autenticar, a senha deve ser enviada no header:
   Authorization: Basic BOBESPONJA

* O teste de cookie deve ser feito passando o modo=debug
   Cookie: modo=debug

Observação:
Nesta atividade, o header Authorization é utilizado de forma simplificada.
O valor "BOBESPONJA" não utiliza a codificação Base64 normalmente empregada
pelo HTTP Basic Authentication.


O cURL pode ser usado para realizar solicitações utilizando diversos protocolos,
como HTTP, HTTPS, FTP e outros.

Se você digitar apenas:

curl https://www.google.com

no seu terminal, ele vai baixar o código HTML da página e exibir diretamente na sua tela.

Para maiores informações sobre essa atividade:

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

Opção    Nome Longo     Descrição
-X       --request      Especifica o método HTTP (GET, POST, PUT, DELETE).
-I       --head         Traz apenas o cabeçalho da resposta. Ótimo para debug.
-d       --data         Envia dados em uma requisição POST (como preencher um formulário).
-H       --header       Adiciona um cabeçalho extra (ex: autenticação ou tipo de conteúdo).
-o       --output       Salva a resposta em um arquivo em vez de exibir no terminal.
-L       --location     Segue redirecionamentos (se a página mudou de endereço).
-v       --verbose      Modo "fofoqueiro": mostra tudo o que está acontecendo na conexão.



Exemplos Práticos:

Fazendo a requisição de um site:
    curl https://example.com

Fazendo a requisição de um site e analisando o cabeçalho de resposta:
    curl -i https://example.com

Adicionando um cabeçalho à requisição:
    curl https://example.com -H "User-Agent: curl/8.7.1"

Salvando a resposta em um arquivo:
    curl -o instalador.zip https://exemplo.com/

Alterando o método da solicitação:
    curl -X POST https://example.com

Verificando toda a comunicação HTTP:
    curl -v https://example.com
"""


INSTRUCOES_ERRO = """Objeto solicitado não encontrado

Opções válidas:

URL
 ├─ /
 ├─ /curl
 └─ /REF

Lembrando que a URL pode ser no formato:

http://IP:PORTA
"""


INSTRUCOES_REF = """Para entender mais sobre a atividade consulte:

Documentação para módulo http.server:
https://docs.python.org/3/library/http.server.html

RFC 2616 - Hypertext Transfer Protocol -- HTTP/1.1:
https://datatracker.ietf.org/doc/html/rfc2616

Documentação sobre Curl:
https://curl.se
"""


class ServidorLab(BaseHTTPRequestHandler):

    def setup(self):
        """
        Configura a conexão e aplica um timeout.
        Evita que uma conexão abandonada fique bloqueando
        indefinidamente o atendimento.
        """
        super().setup()
        self.connection.settimeout(TIMEOUT_CONEXAO)

    def enviar_resposta(self, status, corpo, enviar_corpo=True):
        """
        Envia uma resposta HTTP padronizada.
        """
        if isinstance(corpo, str):
            corpo = corpo.encode("utf-8")

        self.send_response(status)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(corpo)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("Connection", "close")
        self.end_headers()

        if enviar_corpo:
            self.wfile.write(corpo)

    def do_GET(self):

        cookie = self.headers.get("Cookie", "")

        # Ativa modo debug quando o cookie contém modo=debug
        if "modo=debug" in cookie:
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
            self.enviar_resposta(200, resposta)
            return

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
            resposta = INSTRUCOES_ERRO
            status = 404

        self.enviar_resposta(status, resposta)

    def do_HEAD(self):
        """
        HEAD deve enviar os mesmos cabeçalhos que GET,
        mas não deve enviar o corpo da resposta.
        """

        if self.path == "/":
            corpo = INSTRUCOES_RAIZ
            status = 200

        elif self.path == "/curl":
            corpo = INSTRUCOES_CURL
            status = 200

        elif self.path == "/REF":
            corpo = INSTRUCOES_REF
            status = 200

        else:
            corpo = INSTRUCOES_ERRO
            status = 404

        self.enviar_resposta(status, corpo, enviar_corpo=False)

    def do_POST(self):

        auth = self.headers.get("Authorization")

        # Obtém Content-Length
        content_length = self.headers.get("Content-Length")

        if content_length is None:
            corpo = "Requisição POST sem Content-Length.\n"
            self.enviar_resposta(400, corpo)
            return

        try:
            tamanho = int(content_length)
        except ValueError:
            corpo = "Content-Length inválido.\n"
            self.enviar_resposta(400, corpo)
            return

        # Impede valores negativos
        if tamanho < 0:
            corpo = "Content-Length inválido.\n"
            self.enviar_resposta(400, corpo)
            return

        # Verifica tamanho máximo antes de ler o corpo
        if tamanho > TAMANHO_MAXIMO:

            corpo = "Payload muito grande (limite: 1024 bytes)\n"

            self.send_response(413)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(corpo.encode("utf-8"))))
            self.send_header("Connection", "close")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()

            self.wfile.write(corpo.encode("utf-8"))
            return

        # Lê exatamente a quantidade de bytes informada
        dados = self.rfile.read(tamanho)

        # Trata problemas de codificação
        try:
            mensagem = dados.decode("utf-8").strip()
        except UnicodeDecodeError:
            corpo = "Conteúdo recebido não está em UTF-8.\n"
            self.enviar_resposta(400, corpo)
            return

        # Verifica autenticação
        if auth != f"Basic {SENHA_CORRETA}":

            corpo = "Senha incorreta ou ausente.\n"

            self.send_response(401)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(corpo.encode("utf-8"))))
            self.send_header("Connection", "close")
            self.send_header("Cache-Control", "no-store")
            self.send_header("WWW-Authenticate", "Basic")
            self.end_headers()

            self.wfile.write(corpo.encode("utf-8"))
            return

        # Autenticação correta
        resposta = f"""POST RECEBIDO COM SUCESSO

Senha correta.
Mensagem enviada pelo aluno:
"{mensagem}"
"""

        self.enviar_resposta(200, resposta)

        print(
            "Mensagem recebida:",
            mensagem,
            "no endereço:",
            self.client_address
        )

    def log_message(self, format, *args):
        """
        Desativa o log padrão do http.server
        para não poluir o terminal durante a aula.
        """
        return


print(f"Servidor de laboratorio ativo na porta {PORTA}")
print("Aguardando usuários se conectarem......")
print(f"Timeout das conexões: {TIMEOUT_CONEXAO} segundos")

servidor = ThreadingHTTPServer(("", PORTA), ServidorLab)

try:
    servidor.serve_forever()
except KeyboardInterrupt:
    print("\nServidor encerrado pelo usuário.")
finally:
    servidor.server_close()
