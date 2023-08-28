# Atividade Programação Ponderada 2

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

1. Abra um terminal na pasta raiz do seu projeto e execute o seguinte comando para construir o contêiner (deve estar com o Docker Desktop aberto):

   docker build -t atividade .

2. Rode o Contêiner:

   Após o build ser concluído, execute o seguinte comando para rodar o contêiner:

   docker run -p 8000:8000 atividade

3. Acesse a Aplicação:

   Abra o seu navegador e acesse http://localhost:8000 para visualizar a aplicação.
