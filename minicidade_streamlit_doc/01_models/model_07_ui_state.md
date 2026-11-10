Estado da interface Streamlit, guardado em `st.session_state` (um por sessão do navegador). É separado da City: nada aqui é salvo no arquivo de save, e a simulação (`minicidade/`) nunca lê esses valores.
As regras do Streamlit que afetam este estado estão em `../03_interface_streamlit.md`, seção 2.

1) city
- a cidade da sessão
- City
- criada por `init_state()` na primeira execução (novo jogo com nome "Minha Cidade" e seed aleatória)

2) rng
- gerador de números aleatórios usado pela simulação
- random.Random
- criado junto com a cidade; não é salvo

3) speed
- velocidade da simulação
- valores possíveis: "paused", "normal", "fast"
- é a chave de um widget (`key="speed"`); começa "paused"
- regra: nunca escrever nesta chave depois de o widget ser criado na mesma execução

4) tool
- ferramenta selecionada
- valores possíveis: "inspect", "road", "zone_residential", "zone_commercial", "zone_industrial", "build", "demolish"
- é a chave de um widget (`key="tool"`); padrão "inspect"

5) build_type_id
- tipo de prédio especial selecionado quando tool = "build"
- str; id de um BuildingType de categoria power, service ou park
- é a chave de um widget (`key="build_type_id"`)

6) pending
- primeiro canto já clicado nas ferramentas de dois cliques (estrada e zonas)
- tupla (x, y) em tiles; None se não há seleção em andamento
- volta a None quando: o segundo clique é processado, a ferramenta muda, ou o jogador clica em "Cancelar seleção"

7) selected_tile
- tile em inspeção
- tupla (x, y); None se nenhum

8) last_click_unix
- valor `unix_time` do último clique já tratado no mapa
- float; None no início
- usado para não tratar o mesmo clique duas vezes (o componente devolve o último clique a cada execução)

9) last_tick_time
- instante (`time.monotonic()`) do último tick executado pelo temporizador
- float; usado para que cliques e outros eventos não adiantem o relógio do jogo

10) messages
- mensagens para o jogador (eventos, avisos, erros de ação)
- list[str], no máximo MESSAGE_LOG_MAX; as mais novas por último
- não é salvo
