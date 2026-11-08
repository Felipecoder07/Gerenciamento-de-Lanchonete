# 🍔 Sistema de Gerenciamento de Lanchonete (API REST)

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=for-the-badge&logo=pydantic&logoColor=white)

API RESTful desenvolvida em **Python** com **FastAPI** e **SQLAlchemy** para automação e gerenciamento de pedidos de lanchonete, integrando o atendimento de **Garçom**, **WhatsApp** e o fluxo de produção da **Cozinha**.

---

## ✨ Funcionalidades Principais

- **Gestão de Cardápio (`/produtos`)**:
  - Cadastro, listagem paginada, edição e desativação lógica (*soft delete* via `ativo = False`) de produtos.
  - Bloqueio automático de pedidos contendo produtos inativos ou inexistentes.
- **Central de Pedidos (`/pedidos`)**:
  - Criação de pedidos com múltiplos itens e validação de origem (`GARCOM` ou `WHATSAPP`).
  - Validação de quantidades e integridade relacional entre pedidos e itens (`CASCADE`).
- **Fluxo Operacional da Cozinha (`/cozinha`)**:
  - Fila dedicada com listagem em tempo real dos pedidos `PENDENTE` e `EM_PREPARO`.
  - **Máquina de Estados Estrita** para transição de status, impedindo saltos ou regressões inválidas no preparo:

```mermaid
stateDiagram-v2
    direction LR
    [*] --> PENDENTE
    PENDENTE --> EM_PREPARO
    EM_PREPARO --> PRONTO
    PRONTO --> ENTREGUE
    ENTREGUE --> [*]
```

- **Controle de Usuários e Papéis (`/usuarios`)**:
  - CRUD completo de operadores do sistema com validação de perfil (`GARCOM`, `COZINHA`, `ADMIN`).
- **Performance & Banco de Dados**:
  - Índices compostos e individuais configurados no SQLAlchemy (`idx_pedido_status_criado`, `idx_produto_ativo`, `idx_usuario_papel`) para consultas rápidas na fila da cozinha.

---

## 🏗️ Arquitetura e Estrutura do Projeto

```mermaid
flowchart LR
    Garcom["Garçom"] --> API["API FastAPI + Pydantic"]
    WhatsApp["WhatsApp"] --> API
    Cozinha["Cozinha"] --> API
    Admin["Admin"] --> API
    API --> ORM["SQLAlchemy ORM"]
    ORM --> DB[("PostgreSQL")]
    API --> Docs["Swagger / ReDoc"]
```

```text
Gerenciamento-de-Lanchonete/
└── lanchonete-system/
    ├── app/
    │   ├── core/
    │   │   └── config.py               # Configurações gerais
    │   ├── models/                     # Modelos ORM (SQLAlchemy)
    │   │   ├── usuario.py              # Tabela 'usuarios'
    │   │   ├── produto.py              # Tabela 'produtos'
    │   │   ├── pedido.py               # Tabela 'pedidos'
    │   │   └── item_pedido.py          # Tabela 'itens_pedido'
    │   ├── routers/                    # Rotas da API (FastAPI)
    │   │   ├── usuario.py              # Endpoints /usuarios
    │   │   ├── produto.py              # Endpoints /produtos
    │   │   ├── pedido.py              # Endpoints /pedidos
    │   │   └── cozinha.py              # Endpoints /cozinha
    │   ├── schemas/                    # Schemas Pydantic & Regras de Negócio
    │   │   ├── services/
    │   │   │   └── pedido_service.py   # Máquina de estados do pedido
    │   │   ├── usuario.py
    │   │   ├── produto.py
    │   │   ├── pedido.py
    │   │   └── item_pedido.py
    │   ├── database.py                 # Conexão SQLAlchemy e sessão (get_db)
    │   ├── create_tables.py            # Script de criação das tabelas
    │   └── main.py                     # Ponto de entrada da aplicação FastAPI
    └── requirements.txt                # Dependências do projeto
```

---

## 🚀 Como Executar Localmente

### 1. Pré-requisitos
- **Python 3.10+**
- **PostgreSQL** (ou SQLite para testes locais)

### 2. Clonar o repositório
```bash
git clone https://github.com/Felipecoder07/Gerenciamento-de-Lanchonete.git
cd Gerenciamento-de-Lanchonete/lanchonete-system
```

### 3. Criar e ativar o ambiente virtual
```bash
python -m venv venv

# Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# Linux / macOS
source venv/bin/activate
```

### 4. Instalar as dependências
```bash
pip install -r requirements.txt
```

### 5. Configurar variáveis de ambiente
Crie um arquivo `.env` dentro de `lanchonete-system/` com a string de conexão do seu banco de dados:

```env
# Exemplo com PostgreSQL
DATABASE_URL=postgresql://usuario:senha@localhost:5432/lanchonete_db

# Ou exemplo rápido com SQLite local
# DATABASE_URL=sqlite:///./lanchonete.db
```

### 6. Criar as tabelas no banco
```bash
python create_tables.py
```

### 7. Iniciar o servidor
```bash
uvicorn app.main:app --reload
```

A API estará disponível em `http://127.0.0.1:8000`.

---

## 📖 Documentação Interativa (Swagger / Redoc)

Com o servidor rodando, acesse a documentação automática gerada pelo FastAPI:

- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`

---

## 🔌 Principais Endpoints da API

### 👤 Usuários (`/usuarios`)
| Método | Rota | Descrição |
| :--- | :--- | :--- |
| `POST` | `/usuarios/` | Cria um usuário (`GARCOM`, `COZINHA` ou `ADMIN`) |
| `GET` | `/usuarios/` | Lista usuários cadastrados (`skip`, `limit`) |
| `GET` | `/usuarios/{usuario_id}` | Busca um usuário pelo ID |
| `PUT` | `/usuarios/{usuario_id}` | Atualiza nome ou papel do usuário |
| `DELETE` | `/usuarios/{usuario_id}` | Remove um usuário |

### 🍟 Produtos (`/produtos`)
| Método | Rota | Descrição |
| :--- | :--- | :--- |
| `POST` | `/produtos/` | Cadastra um novo produto no cardápio |
| `GET` | `/produtos/` | Lista todos os produtos ativos (`skip`, `limit`) |
| `GET` | `/produtos/{produto_id}` | Detalha um produto pelo ID |
| `PUT` | `/produtos/{produto_id}` | Atualiza nome, preço ou status do produto |
| `DELETE` | `/produtos/{produto_id}` | Desativa um produto do cardápio (`ativo = False`) |

### 🧾 Pedidos (`/pedidos`)
| Método | Rota | Descrição |
| :--- | :--- | :--- |
| `POST` | `/pedidos/` | Registra um novo pedido (`GARCOM` ou `WHATSAPP`) |
| `GET` | `/pedidos/` | Lista pedidos registrados (`skip`, `limit`) |
| `GET` | `/pedidos/{pedido_id}` | Consulta detalhes e itens de um pedido |

**Exemplo de payload (`POST /pedidos/`):**
```json
{
  "origem": "WHATSAPP",
  "itens": [
    {
      "produto_id": 1,
      "quantidade": 2
    },
    {
      "produto_id": 3,
      "quantidade": 1
    }
  ]
}
```

### 👨‍🍳 Cozinha (`/cozinha`)
| Método | Rota | Descrição |
| :--- | :--- | :--- |
| `GET` | `/cozinha/pedidos` | Lista pedidos ativos na fila (`PENDENTE` e `EM_PREPARO`) |
| `PUT` | `/cozinha/pedido/{pedido_id}/status` | Avança o status do pedido (`EM_PREPARO` → `PRONTO` → `ENTREGUE`) |

---

## 🛠️ Tecnologias Utilizadas

- **[FastAPI](https://fastapi.tiangolo.com/)** — Framework web assíncrono de alta performance
- **[SQLAlchemy](https://www.sqlalchemy.org/)** — ORM e mapeamento objeto-relacional
- **[Pydantic](https://docs.pydantic.dev/)** — Validação e serialização de dados
- **[Uvicorn](https://www.uvicorn.org/)** — Servidor ASGI
- **[PostgreSQL](https://www.postgresql.org/) / `psycopg2-binary`** — Banco de dados relacional
- **`python-dotenv`** — Gerenciamento de variáveis de ambiente

---

## 👨‍💻 Autor

Desenvolvido por **Luiz Felipe** — [GitHub](https://github.com/Felipecoder07)
