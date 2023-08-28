#Atividade programação ponderada 2

##Estrutura de Pastas:

├── static/
│   └── style.css
│   └── app.js
│   └── ...
├── templates/
│   ├── index.html
│   ├── notes.html
├── auth.py
├── database.py
├── Dockerfile
├── docker-compose.yml
├── main.py
├── README.md
├── requirements.txt
└── test.db

##Descrição das Pastas:

- auth.py: Contém funções para autenticação e geração de tokens de acesso.
- databases.py: Configuração e operações de banco de dados.
- README.md: Este arquivo, com informações sobre a estrutura do projeto.
- requirements.txt: Lista de dependências Python necessárias para rodar o projeto.
- test.db: Banco de dados SQLite para desenvolvimento.

##Como Rodar o Projeto:

1 - Abra um terminal na pasta raiz do seu projeto e execute o seguinte comando para construir o contêiner (deve estar com o docker desktop aberto):
```bash
docker build -t atividade .
```

2 - Rode o Contêiner

Após o build ser concluído, execute o seguinte comando para rodar o contêiner:

```bash
docker run -p 8000:8000 atividade
```

3 - Acesse a Aplicação

Abra o seu navegador e acesse `http://localhost:8000` para visualizar a aplicação.
