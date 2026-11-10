# Regras da simulação e constantes de balanceamento

Todos os números são valores iniciais sugeridos e podem ser ajustados, mas devem ficar definidos como constantes nomeadas em um único lugar do código.
Convenção: `clamp(v, a, b)` limita v ao intervalo [a, b]; `round` arredonda para o inteiro mais próximo.

## 1. Tempo
- 1 tick = 1 dia do jogo
- 1 mês = 30 dias; o fechamento do mês ocorre ao final do tick em que `day` é múltiplo de 30
- Velocidades (estado da interface, não da cidade): `paused` (nenhum tick), `normal` (TICKS_NORMAL tick por execução do fragmento), `fast` (TICKS_FAST ticks por execução do fragmento)
- O fragmento do jogo executa a cada REFRESH_SECONDS segundos; por isso `normal` = 1 dia/s e `fast` = 5 dias/s, com o mapa desenhado uma única vez por execução
- Ao criar ou carregar um jogo, a velocidade começa em `paused`

## 2. Constantes
| Nome | Valor | Significado |
|---|---|---|
| MAP_SIZE | 32 | largura e altura padrão do mapa |
| START_MONEY | 20000 | dinheiro inicial |
| TAX_DEFAULT / TAX_MIN / TAX_MAX | 9 / 0 / 20 | imposto em % |
| ROAD_COST / ROAD_UPKEEP | 10 / 1 | custo por tile / manutenção mensal por tile |
| ZONE_COST | 5 | custo por tile ao pintar zona |
| CLEAR_FOREST_COST | 50 | custo por tile de floresta limpo |
| WORKING_AGE_RATIO | 0,6 | fração da população em idade de trabalhar |
| INCOME_FACTOR | 0,1 | usado na receita mensal |
| SPAWN_BASE_CHANCE | 0,10 | chance diária por tile candidato quando a demanda é 100 |
| SPAWN_MAX_PER_ZONE_TICK | 3 | máximo de prédios novos por tipo de zona por dia |
| OCCUPANCY_GROW / OCCUPANCY_SHRINK | 0,05 / 0,10 | fração da capacidade que entra/sai por dia |
| BASE_HAPPINESS | 50 | felicidade de partida de um prédio |
| HAPPY_POSITIVE_CAP / HAPPY_NEGATIVE_CAP | +30 / -30 | limite da soma dos efeitos de prédios próximos |
| TAX_NEUTRAL / TAX_HAPPY_FACTOR | 9 / 2 | efeito do imposto na felicidade |
| UNEMPLOYMENT_FREE / UNEMPLOYMENT_FACTOR | 10 / 0,5 | desemprego tolerado (%) / peso da penalidade |
| BLACKOUT_PENALTY | 15 | penalidade de felicidade durante apagão |
| HAPPY_MIN_GROWTH | 40 | felicidade mínima para ocupantes entrarem |
| HAPPY_LEVEL_UP / HAPPY_LEVEL_DOWN | 70 / 30 | limiares para subir/descer de nível |
| LEVEL_DAYS | 30 | dias seguidos para mudar de nível |
| MAX_NEGATIVE_MONTHS | 3 | meses seguidos negativos até o game over |
| EVENT_CHANCE | 0,02 | chance diária de um evento |
| MAX_LEVEL | 3 | nível máximo dos prédios de zona |
| TILE_PX | 20 | tamanho de um tile no mapa desenhado, em pixels |
| REFRESH_SECONDS | 1,0 | intervalo de execução do fragmento do jogo |
| TICKS_NORMAL / TICKS_FAST | 1 / 5 | ticks por execução do fragmento |
| MESSAGE_LOG_MAX | 50 | máximo de mensagens guardadas no painel |

## 3. Catálogo inicial de BuildingType
Tamanho em tiles (largura x altura). Consumo de energia dos prédios de zona é multiplicado pelo nível; capacidade também.

| id | category | tamanho | build_cost | upkeep/mês | capacity | power_consumption | power_production | service_type | effect_radius | happiness_effect | unlock_population |
|---|---|---|---|---|---|---|---|---|---|---|---|
| house | residential | 1x1 | 0 | 0 | 6 | 1 | 0 | – | 0 | 0 | 0 |
| shop | commercial | 1x1 | 0 | 0 | 8 | 2 | 0 | – | 0 | 0 | 0 |
| factory | industrial | 1x1 | 0 | 0 | 20 | 5 | 0 | – | 4 | -6 | 0 |
| coal_plant | power | 2x2 | 3000 | 100 | 0 | 0 | 100 | – | 6 | -10 | 0 |
| solar_plant | power | 2x2 | 5000 | 60 | 0 | 0 | 40 | – | 0 | 0 | 500 |
| police | service | 1x1 | 500 | 50 | 0 | 3 | 0 | police | 6 | +5 | 0 |
| fire_station | service | 1x1 | 500 | 50 | 0 | 3 | 0 | fire | 6 | +3 | 0 |
| school | service | 1x1 | 800 | 80 | 0 | 4 | 0 | education | 6 | +8 | 0 |
| hospital | service | 2x2 | 1000 | 120 | 0 | 6 | 0 | health | 8 | +6 | 300 |
| park | park | 1x1 | 100 | 10 | 0 | 0 | 0 | – | 4 | +5 | 0 |

Observações:
- Prédios de zona usam sempre os tipos `house`, `shop` e `factory`; a evolução é feita pelo atributo `level`, não por tipos diferentes
- Prédios de zona são sempre 1x1
- Para os serviços, só `fire_station` tem função própria além da felicidade (apaga incêndios, seção 13)

## 4. Ordem de execução de um tick
0. Todo sorteio usa o gerador `rng` (`random.Random`) recebido por `tick(city, rng)`; isso torna a simulação reproduzível em testes
1. Atualizar `near_road` dos tiles e `connected` dos prédios
2. Calcular energia (seção 6) e `blackout`
3. Calcular empregos e demanda (seção 7)
4. Nascer novos prédios de zona (seção 8)
5. Atualizar ocupantes dos prédios residenciais (seção 9)
6. Calcular felicidade, níveis e abandono (seções 10 e 11)
7. Avançar eventos ativos e sortear novo evento (seção 13)
8. Incrementar `day`; se for múltiplo de 30, fazer o fechamento do mês (seção 12)
9. Recalcular `CityStats` finais para exibição

## 5. Regras de edição do mapa (ferramentas)
- Toda ação paga só é permitida se `money` >= custo total; senão é recusada com mensagem e nada é alterado. Ações do jogador nunca deixam o dinheiro negativo
- Estrada e zona são aplicadas por **dois cliques** (primeiro e segundo canto; ver `03_interface_streamlit.md`). Estrada: caminho em "L" (primeiro horizontal, depois vertical). Zona: retângulo entre os dois cantos
- Em ações de vários tiles (estrada, zona), tiles inválidos (água, ocupados, etc.) são ignorados e não cobrados; o custo é calculado sobre os tiles válidos; se `money` for menor que esse custo, nada é aplicado. O resultado informa quantos tiles foram alterados e quantos ignorados
- Tile de água: nenhuma ação é permitida
- Tile de floresta: ao receber estrada, zona ou prédio, vira grama e cobra CLEAR_FOREST_COST adicional por tile
- **Estrada:** só em tile sem prédio. Se o tile tem zona (sem prédio), a zona é removida
- **Zona:** só em tile sem estrada e sem prédio. Pintar outro tipo de zona sobre uma zona sem prédio troca o tipo (cobra ZONE_COST); pintar o mesmo tipo não cobra
- **Construir (prédio especial):** todos os tiles da área devem ser grama (ou floresta, com limpeza), sem estrada e sem prédio; zonas vazias nesses tiles são removidas. Prédios especiais não precisam de estrada para funcionar
- **Demolir:** gratuito e sem reembolso. Ao clicar num tile: se há prédio, remove o prédio inteiro (todos os tiles dele) e mantém a zona; senão, se há estrada, remove a estrada; senão, se há zona, remove a zona
- Prédios com `unlock_population` maior que a população atual ficam indisponíveis na lista de construção
- A estrada é considerada "ligada" se qualquer um dos 4 tiles vizinhos do prédio tem estrada. Não há verificação de que a estrada leva a algum lugar (simplificação consciente)

## 6. Energia
- `power_produced` = soma de `power_production` de todas as usinas; multiplicada por 0,5 se houver evento `power_failure` ativo
- `power_consumed` = soma de `power_consumption` x `level` de todos os prédios (inclusive os vazios)
- `blackout` = `power_produced` < `power_consumed`
- Se há apagão: nenhum prédio novo nasce, ocupantes não aumentam e a felicidade sofre BLACKOUT_PENALTY
- `Building.powered` = não há apagão (a energia é global, sem fios)

## 7. Empregos e demanda
Definições (calculadas a cada tick):
- `working_age` = floor(`population` x WORKING_AGE_RATIO)
- `jobs_commercial` = soma de `capacity` x `level` dos prédios comerciais que estão `connected` e não estão `on_fire`
- `jobs_industrial` = idem para os industriais
- `jobs` = `jobs_commercial` + `jobs_industrial`
- `workers` = min(`working_age`, `jobs`)
- `unemployment` = 0 se `working_age` = 0; senão (`working_age` - `workers`) / `working_age` x 100
- `residential_capacity` = soma de `capacity` x `level` dos prédios residenciais não abandonados

Demanda (todas de -100 a +100):
- `target_c` = max(`working_age` x 0,6; 5)
- `target_i` = max(`working_age` x 0,6; 10)
- `demand_commercial` = clamp(round((`target_c` - `jobs_commercial`) / `target_c` x 100), -100, 100)
- `demand_industrial` = clamp(round((`target_i` - `jobs_industrial`) / `target_i` x 100), -100, 100)
- `demand_residential` = clamp(round((`jobs` - `working_age`) / max(`jobs`, `working_age`, 10) x 100), -100, 100)
  - se `population` < 20: `demand_residential` = max(`demand_residential`, 30) (impulso inicial; evita que a cidade nunca comece)
  - se `residential_capacity` > 0 e `population` / `residential_capacity` < 0,7: `demand_residential` = min(`demand_residential`, 0) (só constrói mais casas quando as existentes estão 70% cheias)
- Evento `boom` ativo: soma 30 a `demand_residential` e `demand_commercial` antes do clamp
- Se a felicidade média da cidade for menor que HAPPY_MIN_GROWTH, as três demandas ficam limitadas a no máximo 0

## 8. Nascimento de prédios de zona
Para cada tipo de zona (residential → `house`, commercial → `shop`, industrial → `factory`) com demanda > 0:
- Candidatos: tiles com essa zona, sem prédio, `near_road` verdadeiro
- Para cada candidato, nasce um prédio com probabilidade `SPAWN_BASE_CHANCE` x demanda / 100, até SPAWN_MAX_PER_ZONE_TICK por dia
- Só nasce se sobrar energia: (`power_produced` - `power_consumed`) >= consumo do prédio novo; o consumo é somado ao `power_consumed` após cada nascimento
- O prédio novo nasce com `level` 1 e `occupants` 0
- Na fase 3 de desenvolvimento (antes da demanda existir) usa-se chance fixa de 5%

## 9. Ocupantes (apenas prédios residenciais)
Por dia, para cada prédio residencial:
- Se `connected`, sem apagão e `happiness` >= HAPPY_MIN_GROWTH: `occupants` aumenta max(1, round(`capacity` x `level` x OCCUPANCY_GROW)), limitado à capacidade
- Se `happiness` < HAPPY_LEVEL_DOWN: `occupants` diminui max(1, round(`capacity` x `level` x OCCUPANCY_SHRINK)), mínimo 0
- Caso contrário, não muda
- `population` = soma de `occupants` de todos os prédios residenciais
- Prédios comerciais e industriais não têm ocupantes simulados: os empregos são a própria capacidade (seção 7)

## 10. Felicidade
Felicidade de um prédio (`Building.happiness`), recalculada a cada tick:
```
H = BASE_HAPPINESS
  + min(soma dos happiness_effect positivos de prédios próximos, +30)
  + max(soma dos happiness_effect negativos de prédios próximos, -30)
  - (imposto - 9) x 2
  - round(max(0, desemprego - 10) x 0,5)
  - 15 se houver apagão
  + 10 se houver evento festival ativo
H = clamp(round(H), 0, 100)
```
- "Prédio próximo" é todo prédio cuja distância euclidiana entre os centros é menor ou igual ao seu `effect_radius`. O centro de um prédio de largura w e altura h na posição (x, y) é (x + (w-1)/2, y + (h-1)/2)
- Cada prédio próximo conta uma vez; o próprio prédio não conta para si
- Felicidade da cidade (`CityStats.happiness`) = média arredondada de `Building.happiness` dos prédios residenciais com `occupants` > 0; se não há nenhum, vale 50
- Exemplo: imposto 9, sem desemprego, com escola + hospital + delegacia + parque por perto: 50 + (8+6+5+5 = 24) = 74

## 11. Níveis e abandono (prédios de zona)
Por dia, para cada prédio de zona:
- Se `happiness` > HAPPY_LEVEL_UP: `days_happy` += 1 e `days_unhappy` = 0
- Senão, se `happiness` < HAPPY_LEVEL_DOWN: `days_unhappy` += 1 e `days_happy` = 0
- Senão: os dois contadores voltam a 0
- Se `days_happy` >= LEVEL_DAYS e `level` < MAX_LEVEL: sobe um nível e zera os contadores
- Se `days_unhappy` >= LEVEL_DAYS e `level` > 1: desce um nível, zera os contadores e `occupants` é limitado à nova capacidade
- Abandono (só residencial): `abandoned` vira verdadeiro quando `occupants` = 0 e `happiness` < HAPPY_LEVEL_DOWN; volta a falso quando `happiness` >= HAPPY_MIN_GROWTH

## 12. Economia (fechamento do mês)
- `income` = round((`population` + `workers`) x `tax_rate` x INCOME_FACTOR)
- `expenses` = soma de `upkeep` de todos os prédios + (`road_tiles` x ROAD_UPKEEP)
- `balance` = `income` - `expenses`; `money` += `balance`
- Se `money` < 0: `negative_months` += 1; senão `negative_months` = 0
- Se `negative_months` >= MAX_NEGATIVE_MONTHS: `game_over` = verdadeiro

## 13. Eventos aleatórios
Por dia, com chance EVENT_CHANCE, sorteia-se um tipo entre os elegíveis (uniforme). Nunca há dois eventos ativos do mesmo tipo.

| Tipo | Elegível quando | Duração (dias) | Efeito |
|---|---|---|---|
| fire | existe ao menos 1 prédio que não esteja em chamas | 5 | Um prédio aleatório fica `on_fire`. Ao final: se há `fire_station` com distância menor ou igual ao seu `effect_radius` até o prédio, o fogo apaga e o prédio sobrevive; senão o prédio é destruído (tiles liberados, zona permanece) |
| power_failure | existe ao menos 1 usina | 10 | `power_produced` x 0,5 |
| festival | `population` >= 100 | 15 | +10 de felicidade em todos os prédios |
| boom | `population` >= 100 | 20 | +30 em `demand_residential` e `demand_commercial` |

- Um prédio `on_fire` não conta para `jobs` e não recebe novos ocupantes
- O fogo não se espalha
- Eventos ativos nunca são descartados do histórico (ver `City.events`)

## 14. Fim de jogo
- Condição: seção 12 (3 fechamentos de mês seguidos com dinheiro negativo)
- Ao ocorrer: `tick` deixa de avançar, a interface mostra aviso de falência com dias jogados (`City.day`), população máxima (`City.peak_population`) e botão "Novo jogo"
- Não há condição de vitória
