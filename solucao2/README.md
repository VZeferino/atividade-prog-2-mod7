# MAIOR AVANÇO NO JWT

# Atividade Programação Ponderada 2

## Descrição

Neste projeto, foi desenvolvida uma aplicação web utilizando o framework FastAPI, o Uvicorn para o servidor, e Docker para facilitar o gerenciamento de notas pessoais em que seria possível criar notas, visualiza-las, edita-las e por fim deleta-las. A estrutura de pastas foi organizada de forma clara, com um foco especial na autenticação de usuários. O sistema permite o login com seu usuário e senha para depois levar a uma página onde poderá fazer adição de notas associadas a cada usuário.

## Arquitetura da Solução
Este projeto foi desenvolvido seguindo uma arquitetura simples e eficiente, buscando atender aos requisitos da atividade. A arquitetura da solução segue o padrão de desenvolvimento web com a separação de responsabilidades em camadas, incluindo o frontend, o backend e o db. A estrutura de pastas e a separação de arquivos foram planejadas para facilitar a organização e o entendimento do projeto.

A escolha dessa arquitetura foi motivada pela necessidade de separar as preocupações do frontend e do backend, tornando o código mais organizado.. A utilização de templates HTML permite a criação de páginas enquanto o backend controla as operações de autenticação, acesso ao banco de dados e manipulação das notas.

A utilização de contêineres Docker simplifica o processo de implantação e reduz problemas de dependências.

Além disso, a separação das operações de autenticação e geração de tokens no arquivo auth.py facilita a manutenção e expansão das funcionalidades de segurança da aplicação.

## Estrutura de Pastas:

- static/
  - style.css
  - app.js
  - ...

- templates/
  - index.html
  - notes.html

- auth.py
- database.py
- Dockerfile
- docker-compose.yml
- main.py
- README.md
- requirements.txt
- test.db

## Descrição dos arquivos:

- auth.py: Contém funções para autenticação e geração de tokens de acesso.
- database.py: Configuração e operações de banco de dados.
- README.md: Este arquivo, com informações sobre a estrutura do projeto.
- requirements.txt: Lista de dependências Python necessárias para rodar o projeto.
- test.db: Banco de dados SQLite para desenvolvimento.

## Como Rodar o Projeto:

[DockerHub](https://hub.docker.com/layers/vzeferino/ponderada2/latest/images/sha256-1e461a287bd8b989c991f6b902d7727ebe3b1d293488b8c225c6138e967cb3ac?context=repo)


Para executar o projeto, siga os passos abaixo:

Abra um terminal na pasta raiz do seu projeto.

Construa a imagem do contêiner utilizando o Docker Compose. Certifique-se de que o Docker Desktop esteja aberto. Execute o seguinte comando:

bash
Copy code
docker-compose build
Inicie o contêiner:

Após a construção da imagem, execute o contêiner utilizando o Docker Compose:

bash
Copy code
docker-compose up

O projeto será iniciado e estará acessível no endereço http://localhost:8000.

Acesse a Aplicação:

Abra o seu navegador e acesse http://localhost:8000 para visualizar a aplicação.
