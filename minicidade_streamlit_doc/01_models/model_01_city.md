Representa o estado completo de uma partida. Existe uma única City por sessão de jogo e ela é guardada em `st.session_state["city"]`.

1) version
- versão do formato de salvamento
- int, valor atual: 1
- ao carregar um arquivo com versão diferente, o jogo mostra o erro e não carrega

2) name
- nome da cidade, escolhido pelo jogador
- str
- exemplos de valores: "Vila Nova", "Cidade Teste"

3) seed
- número usado para gerar o terreno do mapa
- int
- a mesma seed gera sempre o mesmo mapa: usar `random.Random(seed)` na geração (`mapgen.generate_map`)
- os sorteios da simulação (nascimento de prédios, eventos) usam o `rng` passado a `tick(city, rng)`; esse `rng` não é salvo

4) width
- largura do mapa, em tiles
- int, valor padrão MAP_SIZE

5) height
- altura do mapa, em tiles
- int, valor padrão MAP_SIZE

6) money
- dinheiro atual da cidade
- int (sem centavos)
- valor inicial START_MONEY
- só pode ficar negativo no fechamento do mês (ver regras, seção 12)

7) day
- número de dias passados desde o início do jogo
- int, começa em 1

8) tax_rate
- imposto, em porcentagem
- int entre TAX_MIN e TAX_MAX, valor padrão TAX_DEFAULT

9) negative_months
- quantidade de meses seguidos com dinheiro negativo no fechamento
- int, começa em 0

10) game_over
- indica se o jogo terminou
- bool, padrão False

11) peak_population
- maior população já atingida
- int, começa em 0
- atualizado ao final de cada tick; mostrado na tela de fim de jogo

12) next_building_id
- próximo id a ser usado por um novo Building
- int, começa em 1; deve ser salvo

13) next_event_id
- próximo id a ser usado por um novo GameEvent
- int, começa em 1; deve ser salvo

14) tiles
- lista de todos os tiles do mapa (width x height)
- list[Tile]
- acesso por coordenada: `tiles[y * width + x]`; a classe City oferece `tile_at(x, y)`

15) buildings
- lista de prédios existentes na cidade
- list[Building]
- a classe City oferece `building_at(x, y)` e `get_building(building_id)`

16) stats
- objeto CityStats com os números calculados
- derivado, exceto os três campos mensais (income, expenses, balance), que devem ser salvos

17) events
- lista de eventos do jogo
- list[GameEvent]
- eventos com active = True nunca são removidos
- dos eventos encerrados, guardar no máximo os 20 mais recentes

Observação: a velocidade da simulação NÃO faz parte da City; é estado da interface (ver `model_07_ui_state.md`).
