# MiniCidade Leaderboard

Aplicação Streamlit somente de leitura que exibe as cidades do jogo em uma tabela de classificação. O ranking usa população atual; pico populacional, dia de jogo e nome são critérios de desempate.

## Executar localmente

Requer Python 3.11+ e `uv`.

```powershell
uv sync
uv run streamlit run src/app.py
```

Sem configurações MySQL, o app usa `mini_city.db` em SQLite e cria as tabelas necessárias. A aplicação abre em `http://localhost:8501`.

Para MySQL local/remoto, crie `.streamlit/secrets.toml` com base em `.streamlit/secrets.toml.example` e preencha as credenciais privadas:

```toml
[mysql]
host = "seu-host-mysql"
port = 3306
username = "seu-usuario"
password = "sua-senha"
database = "mini_city"
```

O arquivo real `secrets.toml` é ignorado pelo Git. Também são aceitas as variáveis `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_USER`, `MYSQL_PASSWORD` e `MYSQL_DATABASE` para ambientes locais. Quando `MYSQL_HOST` não estiver configurado, o app usa SQLite.

## Publicar no Streamlit Community Cloud

1. Publique o repositório sem credenciais e crie o app apontando para `src/app.py`.
2. No painel do app, abra **Settings > Secrets** e adicione o conteúdo TOML acima com os dados do provedor MySQL.
3. Configure no provedor de banco o acesso de rede necessário para o app hospedado e crie um usuário com permissões mínimas para as tabelas usadas pelo jogo e pelo site.

O repositório não contém nem pode descobrir as credenciais de um servidor MySQL. Para conectar em produção, é necessário fornecer um host e credenciais válidas nos Secrets do deployment. A inicialização cria tabelas SQLAlchemy que ainda não existirem; não substitui migrações para alterações futuras de esquema.

## Integração com o jogo

O jogo deve salvar cada cidade em `cities` e as estatísticas atuais em `city_stats`. A relação é `city_stats.city_id` para `cities.id` e há no máximo uma linha de estatísticas por cidade. A tabela do site atualiza a população, felicidade e saldo ao recarregar a página. O fluxo recomendado e o exemplo de persistência estão em [instrucoes_integracao_jogo_leaderboard.txt](instrucoes_integracao_jogo_leaderboard.txt).
