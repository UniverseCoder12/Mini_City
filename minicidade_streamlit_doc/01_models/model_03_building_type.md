Catálogo dos tipos de construção disponíveis no jogo. É uma lista fixa definida no código (não é criada pelo jogador). Cada Building aponta para um BuildingType.
Os valores concretos de cada tipo estão na tabela da seção 3 de `../02_regras_e_constantes.md`.

1) id
- identificador textual único do tipo
- tipo String
- valores existentes: "house", "shop", "factory", "coal_plant", "solar_plant", "police", "fire_station", "school", "hospital", "park"

2) name
- nome exibido ao jogador
- tipo String
- exemplos de valores: "Casa", "Loja", "Fábrica", "Usina a carvão", "Delegacia"

3) category
- categoria do prédio
- valores possíveis: "residential", "commercial", "industrial", "power", "service", "park"
- residential, commercial e industrial nascem sozinhos em zonas (um único tipo para cada: house, shop, factory; a evolução visual é feita pelo level do Building)
- power, service e park são colocados manualmente pelo jogador

4) icon
- emoji usado na lista de construção e na página Como jogar
- tipo String
- exemplos de valores: "🏠", "🏭", "🚓"
- o mapa NÃO usa o emoji (a fonte padrão do Pillow não desenha emojis): usa cor e letra por categoria, definidas em `03_interface_streamlit.md`, seção 7

5) width
- largura em tiles
- tipo inteiro, padrão 1

6) height
- altura em tiles
- tipo inteiro, padrão 1
- prédios de zona são sempre 1x1

7) build_cost
- custo para construir manualmente
- tipo inteiro
- 0 para os tipos de zona (house, shop, factory), pois nascem sozinhos

8) upkeep
- custo de manutenção por mês
- tipo inteiro
- 0 para os tipos de zona

9) capacity
- para residential: quantidade máxima de moradores no nível 1
- para commercial e industrial: quantidade de empregos no nível 1
- para os demais: 0
- tipo inteiro
- a capacidade efetiva é capacity x level do Building

10) power_consumption
- energia consumida por dia, no nível 1
- tipo inteiro; 0 para parques e usinas
- para prédios de zona, o consumo efetivo é power_consumption x level

11) power_production
- energia produzida por dia
- tipo inteiro; 0 para quem não é usina

12) service_type
- tipo de serviço prestado, se category = "service"
- valores possíveis: "police", "fire", "health", "education", ou NULL
- apenas "fire" tem efeito próprio (apagar incêndios); os demais só afetam felicidade

13) effect_radius
- raio de alcance, em tiles, do efeito sobre a felicidade dos prédios ao redor (e do alcance dos bombeiros)
- tipo inteiro; 0 se não tem efeito
- a distância é medida entre os centros dos prédios (ver regras, seção 10)

14) happiness_effect
- quanto soma (ou subtrai) na felicidade dos prédios dentro do raio
- tipo inteiro (pode ser negativo)

15) unlock_population
- população mínima da cidade para o tipo ficar disponível
- tipo inteiro, padrão 0
