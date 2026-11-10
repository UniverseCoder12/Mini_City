# Estrutura de código

## 1. Pastas e arquivos
```
minicidade/                     (raiz do repositório)
├── app.py                      ponto de entrada: set_page_config, init_state, navegação
├── requirements.txt
├── .streamlit/
│   └── config.toml             tema
├── views/                      páginas do Streamlit
│   ├── jogar.py
│   ├── como_jogar.py
│   └── salvar_carregar.py
├── ui/                         interface (usa streamlit)
│   ├── state.py                init_state, reset_game
│   ├── components.py           métricas, barras de demanda, painel de inspeção, mensagens
│   └── actions_ui.py           handle_click (ferramenta atual -> função do jogo)
├── minicidade/                 o jogo (NÃO importa streamlit)
│   ├── __init__.py
│   ├── constants.py            todas as constantes nomeadas da seção 2 das regras
│   ├── models.py               dataclasses: City, Tile, Building, CityStats, GameEvent
│   ├── catalog.py              BUILDING_TYPES (tabela da seção 3 das regras)
│   ├── mapgen.py               geração do terreno
│   ├── actions.py              ações do jogador (estrada, zona, construir, demolir)
│   ├── simulation.py           tick e subfunções
│   ├── persistence.py          salvar/carregar JSON
│   └── render.py               desenho do mapa com Pillow
└── tests/
    ├── test_mapgen.py
    ├── test_actions.py
    ├── test_simulation.py
    ├── test_persistence.py
    └── test_architecture.py
```

## 2. Convenções
- Anotações de tipo em todas as funções públicas
- Constantes só em `constants.py`, com os nomes exatos da seção 2 das regras; nenhum número de balanceamento solto no código
- O pacote `minicidade/` não pode importar `streamlit` (verificado por teste)
- Nenhuma função de `minicidade/` guarda estado em variável global; tudo recebe e devolve `City`
- Funções de `minicidade/` que sorteiam recebem o `rng` por parâmetro
- Mensagens para o jogador em português

## 3. Dependências (`requirements.txt`)
```
streamlit>=1.37
streamlit-image-coordinates
Pillow
pytest
```
Depois da primeira instalação que funcionar, fixar as versões exatas (`pip freeze`) para evitar que uma atualização do componente de clique quebre o jogo.
Executar: `streamlit run app.py`. Testes: `pytest`.

## 4. Especificação dos módulos

### 4.1 `minicidade/models.py`
- Dataclasses `Tile`, `Building`, `CityStats`, `GameEvent`, `City`, com os campos dos arquivos de `01_models/`
- `City.tile_at(x, y) -> Tile`, `City.building_at(x, y) -> Building | None` (usa `building_id` do tile), `City.get_building(building_id) -> Building | None`
- `new_city(name: str, seed: int) -> City`: cria cidade com mapa de `mapgen.generate_map`, `money` = START_MONEY e demais valores padrão
- `to_dict()` e `from_dict()` em `City` (e nos tipos aninhados); campos derivados (`near_road`, `powered`, `connected`, `happiness`) não são salvos e são recalculados por `recompute_derived`

### 4.2 `minicidade/catalog.py`
- `BUILDING_TYPES: dict[str, BuildingType]` com os 10 tipos da tabela da seção 3 das regras
- `BuildingType` é uma dataclass imutável (`frozen=True`)
- `ZONE_BUILDING = {"residential": "house", "commercial": "shop", "industrial": "factory"}`

### 4.3 `minicidade/mapgen.py`
- `generate_map(seed: int, width: int = MAP_SIZE, height: int = MAP_SIZE) -> list[Tile]`
- Usa `random.Random(seed)`; deve ser determinística
- Critérios: água entre 10% e 15% dos tiles, em uma ou duas manchas contínuas; floresta cerca de 15%, em manchas; quadrado central 8 x 8 sempre grama

### 4.4 `minicidade/actions.py`
```python
@dataclass
class ActionResult:
    ok: bool
    message: str
    cost: int = 0
    changed: int = 0
    skipped: int = 0

def paint_road(city, start: tuple[int, int], end: tuple[int, int]) -> ActionResult
def paint_zone(city, zone: str, start: tuple[int, int], end: tuple[int, int]) -> ActionResult
def place_building(city, type_id: str, x: int, y: int) -> ActionResult
def demolish(city, x: int, y: int) -> ActionResult
def recompute_derived(city) -> None   # near_road, connected, powered, stats
```
- Regras de cada ação: seção 5 das regras (custos, tiles inválidos ignorados, tudo ou nada pelo dinheiro)
- `place_building` também recusa se a população for menor que `unlock_population`
- Estas funções nunca levantam exceção por entrada do jogador; devolvem `ok=False` com mensagem

### 4.5 `minicidade/simulation.py`
```python
@dataclass
class TickReport:
    messages: list[str]
    month_closed: bool
    new_unlocks: list[str]     # ids de tipos que acabaram de ficar disponíveis
    game_over: bool

def tick(city, rng: random.Random) -> TickReport
```
- Executa a ordem da seção 4 das regras (passos 0 a 9)
- Funções internas, uma por seção das regras, para testar separadamente: `compute_power`, `compute_jobs_and_demand`, `spawn_buildings`, `update_occupants`, `compute_happiness`, `update_levels_and_abandonment`, `process_events`, `close_month`, `compute_stats`
- Se `city.game_over` já for verdadeiro, `tick` não altera nada e devolve um relatório vazio
- Atualiza `city.peak_population` ao final

### 4.6 `minicidade/persistence.py`
```python
class SaveError(Exception): ...
def city_to_json(city) -> str
def city_from_json(text: str) -> City   # levanta SaveError com mensagem em português
```
- Valida: JSON válido, `version` igual a 1, campos obrigatórios presentes, tipos corretos, dimensões do mapa coerentes com `width` x `height`, valores dentro dos limites (ex.: `tax_rate` entre TAX_MIN e TAX_MAX)
- Ao carregar, chamar `recompute_derived`

### 4.7 `minicidade/render.py`
```python
def render_map(city, tile_px: int = TILE_PX, pending=None, selected=None) -> PIL.Image.Image
def pixel_to_tile(click: dict, image_size: tuple[int, int], city) -> tuple[int, int] | None
```
- `pixel_to_tile` converte a posição clicada para tile levando em conta a largura realmente exibida (se o clique trouxer `width`, usar a proporção entre `width` e a largura real da imagem); devolve None se fora do mapa
- Aparência: seção 7 de `03_interface_streamlit.md`

### 4.8 `ui/state.py`
- `init_state() -> None`: cria as chaves que faltam (`city`, `rng`, `pending`, `selected_tile`, `last_click_unix`, `last_tick_time`, `messages`)
- `reset_game(name: str, seed: int) -> None`: nova cidade, novo `rng`, limpa `pending`, `selected_tile`, `messages`; `seed` 0 significa sortear
- `add_message(text: str) -> None`: acrescenta respeitando MESSAGE_LOG_MAX

## 5. Testes (`tests/`)
| Arquivo | Verifica |
|---|---|
| `test_mapgen.py` | mesma seed gera o mesmo mapa; seeds diferentes geram mapas diferentes; centro 8 x 8 é grama; proporção de água e floresta |
| `test_actions.py` | estrada em "L"; tiles inválidos ignorados e não cobrados; recusa por falta de dinheiro não altera nada; zona sobre estrada recusada; demolir na ordem prédio, estrada, zona; prédio 2 x 2 ocupa 4 tiles |
| `test_simulation.py` | com `rng` fixo o resultado é reproduzível; **a cidade cresce a partir do zero** (cenário do critério da fase 6: usina, ruas em grade, zonas R/C/I) até mais de 100 habitantes e estabiliza quando a energia acaba; apagão impede prédios novos; fechamento do mês; 3 meses negativos geram `game_over`; incêndio sem bombeiros destrói o prédio |
| `test_persistence.py` | salvar e carregar devolve cidade igual; arquivo inválido, versão errada e valores fora do limite levantam `SaveError` |
| `test_architecture.py` | nenhum arquivo de `minicidade/` contém `import streamlit` |

## 6. Validação de balanceamento
Criar o script `tools/simular.py` (fora do jogo) que roda `tick` por pelo menos 10 anos de jogo (3600 dias) em alguns cenários e imprime população, dinheiro e saldo mensal a cada 6 meses. Usar o resultado para decidir os pontos em aberto da seção 7 da visão geral (principalmente o equilíbrio da economia, pois na versão original o saldo ficou perto de zero com ruas em grade).

## 7. Publicação
- Local: `streamlit run app.py`
- Streamlit Community Cloud (ou similar): repositório com `requirements.txt` e `app.py` na raiz
- O sistema de arquivos do servidor não deve ser usado para guardar jogos (é descartado e é compartilhado entre sessões); todo salvamento é pelo arquivo JSON do jogador
