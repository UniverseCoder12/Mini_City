# MiniCidade

Sistema web para gestão de uma cidade de jogo, desenvolvido com Streamlit e SQLAlchemy. O projeto usa SQLite para desenvolvimento local e permite a conexão com MySQL em produção por meio de variáveis de ambiente.

## Objetivo

O app oferece uma interface para administrar os principais elementos do sistema MiniCidade, incluindo cidades, tiles, tipos de construção, prédios, estatísticas e eventos. A estrutura foi organizada em uma pasta `src/`, como solicitado na instrução do projeto.

## Tecnologias

- Python 3.11+
- Streamlit
- SQLAlchemy
- PyMySQL
- Pandas
- uv

## Requisitos

1. Instale o `uv`:

```bash
pip install uv
```

2. Instale as dependências do projeto:

```bash
uv sync
```

3. Crie um arquivo `.env` a partir do exemplo:

```bash
cp .env.example .env
```

4. Ajuste as variáveis de conexão do MySQL quando necessário:

```env
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=mini_city
MYSQL_PASSWORD=mini_city
MYSQL_DATABASE=mini_city
```

Se `MYSQL_HOST` não estiver definido, a aplicação usa o banco SQLite local (`mini_city.db`).

## Como executar

```bash
uv run streamlit run src/app.py
```

A aplicação estará disponível em `http://localhost:8501`.

## Estrutura do projeto

```text
Mini_City/
├── .env.example
├── .gitignore
├── .streamlit/
│   └── config.toml
├── README.md
├── pyproject.toml
├── src/
│   ├── __init__.py
│   ├── app.py
│   ├── database.py
│   ├── models.py
│   ├── seed_data.py
│   └── pages/
│       ├── __init__.py
│       ├── dashboard.py
│       ├── cities.py
│       ├── tiles.py
│       ├── building_types.py
│       ├── buildings.py
│       ├── city_stats.py
│       └── game_events.py
└── mini_city.db
```

## Observações

- O SQLite é usado para testes locais e desenvolvimento.
- O MySQL foi configurado para uso em produção, com variáveis de ambiente para host, porta, usuário, senha e banco.
- O sistema pode ser publicado no Streamlit Cloud com as variáveis de ambiente configuradas no painel do deployment.
