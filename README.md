# Kanban Board (Streamlit + Supabase)

Aplicacao Kanban para gerenciamento visual de tarefas, com filtros por texto, categoria e prioridade.

## Funcionalidades

- Quadro Kanban com 3 colunas: `A Fazer`, `Em Andamento` e `Concluido`
- Criacao, edicao, exclusao e movimentacao de tarefas entre colunas
- Filtro por busca (titulo/descricao), categorias e prioridades
- Categorias e subcategorias para organizacao
- Prazo com indicador visual de vencimento
- Interface construida com Streamlit e CSS customizado

## Stack

- Python
- Streamlit
- Supabase (PostgreSQL + API)

## Estrutura do projeto

```text
app.py
database/
  connection.py
  schema.sql
services/
  category_service.py
  task_service.py
styles/
  kanban.css
ui/
  board.py
  card.py
  dialogs.py
  sidebar.py
```

## Requisitos

- Python 3.10+
- Conta/projeto no Supabase

## Instalacao

1. Clone o repositorio e entre na pasta do projeto.
2. Crie e ative um ambiente virtual.
3. Instale as dependencias.

### Windows (PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Linux/macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuracao do Supabase

1. No Supabase, abra o SQL Editor.
2. Execute o arquivo `database/schema.sql` para criar tabelas, indices e policies.
3. Crie o arquivo `.streamlit/secrets.toml` com suas credenciais:

```toml
[supabase]
url = "https://SEU-PROJETO.supabase.co"
key = "SUA_ANON_KEY"
```

Tambem sao aceitas chaves planas (util no Streamlit Cloud):

```toml
SUPABASE_URL = "https://SEU-PROJETO.supabase.co"
SUPABASE_KEY = "SUA_ANON_KEY"
```

Observacao: `.streamlit/secrets.toml` esta no `.gitignore` e nao deve ser versionado.

## Deploy no Streamlit Cloud

1. Abra sua app no Streamlit Cloud.
2. Va em `Settings > Secrets`.
3. Cole um dos formatos de secrets mostrados acima.
4. Salve e faça `Reboot app` se necessario.

## Como executar

Com o ambiente virtual ativo:

```bash
streamlit run app.py
```

A aplicacao sera aberta no navegador em `http://localhost:8501`.

## Fluxo basico de uso

1. Clique em `Nova Tarefa` para criar cards.
2. Edite o status no seletor de cada card para mover entre colunas.
3. Use os filtros no topo para buscar e segmentar tarefas.
4. Na aba `Subcategorias`, crie e remova subcategorias por categoria.

## Observacao sobre seguranca

O arquivo `database/schema.sql` cria policies permissivas para uso pessoal (sem autenticacao). Para ambiente de producao, ajuste RLS e policies conforme sua estrategia de acesso.
