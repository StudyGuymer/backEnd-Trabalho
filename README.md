_# News API - FastAPI + Supabase

Esta é uma API RESTful simples para gerenciamento de notícias, construída com **Python** e o framework **FastAPI**, utilizando o **Supabase** como backend (banco de dados e autenticação).

## Tecnologias Utilizadas

*   **Backend:** Python 3.11+
*   **Framework:** FastAPI
*   **Servidor:** Uvicorn
*   **Banco de Dados & Autenticação:** Supabase (PostgreSQL + Auth)
*   **Deploy:** Render (sugestão)
*   **Testes:** Postman (coleções inclusas)

## Estrutura do Projeto

O projeto segue uma estrutura modular para organização e limpeza de código:

```
.
├── app/
│   ├── auth.py         # Lógica de autenticação com Supabase
│   ├── config.py       # Carregamento de variáveis de ambiente
│   ├── crud.py         # Funções de CRUD (interação com PostgREST)
│   ├── main.py         # Definição dos endpoints da API
│   └── schemas.py      # Modelos de dados (Pydantic)
├── collection/
│   ├── News.postman_collection.json
│   └── User.postman_collection.json
├── sql/
│   └── news.sql        # Script SQL para criação da tabela e RLS
├── .env                # Variáveis de ambiente (local)
├── .env.example        # Exemplo de variáveis de ambiente
└── requirements.txt    # Dependências do Python
```

## Como Rodar Localmente

### 1. Pré-requisitos

*   Python 3.11+
*   Conta no Supabase com um projeto criado.

### 2. Configuração do Supabase

1.  Acesse o painel do seu projeto Supabase.
2.  Vá para **SQL Editor** e execute o script `sql/news.sql` para criar a tabela `news` e configurar as políticas de Row Level Security (RLS).

### 3. Configuração do Ambiente

1.  Crie um ambiente virtual e instale as dependências:

    ```bash
    pip install -r requirements.txt
    ```

2.  Crie o arquivo `.env` na raiz do projeto e preencha com suas credenciais do Supabase (você pode usar o `.env.example` como base):

    ```ini
    # .env
    SUPABASE_URL="SUA_URL_DO_PROJETO"
    SUPABASE_ANON_KEY="SUA_CHAVE_ANON_PUBLICA"
    TABLE_NEWS="news"
    ```

### 4. Execução da API

Inicie o servidor Uvicorn:

```bash
uvicorn app.main:app --reload --port 8000 
```

A API estará disponível em `http://127.0.0.1:8000`. A documentação interativa (Swagger UI) estará em `http://127.0.0.1:8000/docs`.

## Endpoints da API

Todos os endpoints de CRUD exigem autenticação via token JWT do Supabase no cabeçalho `Authorization: Bearer <token>`.

| Método | Endpoint | Descrição | Autenticação |
| :--- | :--- | :--- | :--- |
| `GET` | `/health` | Verifica o status da API. | Não |
| `GET` | `/news` | Lista todas as notícias do usuário autenticado. | Sim |
| `GET` | `/news/{news_id}` | Busca uma notícia específica por ID. | Sim |
| `POST` | `/news` | Cria uma nova notícia. | Sim |
| `PATCH` | `/news/{news_id}` | Atualiza parcialmente uma notícia. | Sim |
| `DELETE` | `/news/{news_id}` | Exclui uma notícia. | Sim |

### Códigos HTTP e Tratamento de Erros

A API retorna códigos HTTP padrão e mensagens JSON claras:

*   **`200 OK`**: Sucesso (GET, PATCH).
*   **`201 Created`**: Recurso criado (POST).
*   **`204 No Content`**: Recurso excluído (DELETE).
*   **`400 Bad Request`**: Dados de entrada inválidos (validação Pydantic).
*   **`401 Unauthorized`**: Token ausente ou inválido.
*   **`404 Not Found`**: Recurso não encontrado.
*   **`500 Internal Server Error`**: Erro interno do servidor.

## Testes com Postman

As coleções do Postman para testes de **Usuário** (login/signup) e **Notícias** (CRUD) estão disponíveis na pasta `collection/`.

1.  Importe os arquivos `.json` da pasta `collection/` para o seu Postman.
2.  Use a coleção `User` para se registrar e fazer login, obtendo o token JWT.
3.  Defina o token JWT como uma variável de ambiente no Postman para usar na coleção `News`.

## Deploy no Render

Para publicar a API, você pode usar o Render como um serviço de *Web Service*.

1.  Crie um novo **Web Service** no Render.
2.  Conecte ao seu repositório Git (GitHub/GitLab).
3.  **Build Command:** `pip install -r requirements.txt`
4.  **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5.  Adicione as variáveis de ambiente (`SUPABASE_URL`, `SUPABASE_ANON_KEY`, `TABLE_NEWS`) nas configurações do Render.

**Link da API Publicada no Render:**

> **[INSERIR LINK AQUI APÓS O DEPLOY]**
>
