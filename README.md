# 🧪 Servidor HTTP em Python para Laboratório com curl

Este projeto apresenta um servidor HTTP simples em Python, desenvolvido com fins educacionais, para uso em laboratórios de redes, sistemas operacionais e infraestrutura. O servidor foi projetado para interagir diretamente com a ferramenta curl, permitindo que estudantes compreendam, de forma prática, o funcionamento do protocolo HTTP, métodos GET e POST, cabeçalhos e códigos de resposta.

---
## 🎯 Objetivos Educacionais
* Ao utilizar este servidor, o aluno será capaz de:
* Compreender o funcionamento do protocolo HTTP
* Diferenciar os métodos GET e POST
* Enviar e interpretar cabeçalhos HTTP
* Utilizar autenticação simples via Authorization (Basic)
* Analisar códigos de status HTTP
* Entender boas práticas mínimas de segurança em servidores
* Testar requisições usando curl em uma rede local
---
## 🖥️ Funcionamento do Servidor
### 🔹 Requisição GET
 ### - O método GET retorna:
- A descrição da atividade
- Instruções sobre como interagir com o servidor
- Informações sobre o que deve ser enviado no POST
- Esse endpoint é usado como página informativa da atividade.
---
## 🔹 Requisição POST
 ### - O método POST espera:
 - Um cabeçalho Authorization com o valor correto
 - Uma mensagem de texto enviada no corpo da requisição
### - 📌 Regras do POST
 - A senha esperada é:
   ***BOBESPONJA***
 - O tamanho máximo permitido do corpo da requisição é:
    ***1024 bytes***
 - Caso o tamanho seja excedido, o servidor responde com:
    ***HTTP 413 – Payload Too Large***
---
## 🔐 Controle de Segurança Implementado
Este servidor inclui controles básicos, adequados ao ambiente de laboratório:
 - ✔️ Limite de tamanho do corpo do POST (proteção contra payload excessivo)
 - ✔️ Validação explícita do cabeçalho Authorization
 - ✔️ Respostas HTTP padronizadas (RFC 7231 / RFC 9110)
- ✔️ Registro do IP do cliente que realizou a requisição POST (exibido no terminal)
  
***⚠️ Aviso:***
Este servidor não deve ser usado em produção. Ele foi projetado exclusivamente para fins educacionais e ambientes controlados.

---
### 🌐 Execução em Rede Local
O servidor pode ser executado em uma rede local (LAN) para testes com múltiplas máquinas.
Recomenda-se:
Executar em uma rede isolada ou de laboratório
Utilizar firewall ativo
Encerrar o servidor após a atividade

---
### 🧰 Tecnologias Utilizadas
Python 3
Biblioteca padrão http.server
Biblioteca padrão socketserver
Cliente HTTP: curl
Nenhuma dependência externa é necessária.

---
### 🧪 Exemplos de Testes com curl
Durante o laboratório, os alunos devem utilizar o curl para:
- Realizar requisições GET
- Enviar cabeçalhos personalizados
- Testar POST com autenticação
- Observar códigos de erro HTTP
- Validar limites de tamanho de requisição
- Esses testes permitem visualizar na prática o comportamento de um servidor HTTP real.
