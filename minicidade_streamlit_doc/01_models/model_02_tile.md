Cada quadradinho do mapa. O mapa é uma grade de tiles; estradas e zonas são propriedades do tile, e prédios ocupam um ou mais tiles.

1) x
- coluna do tile, começando em 0
- tipo inteiro

2) y
- linha do tile, começando em 0
- tipo inteiro

3) terrain
- tipo de terreno
- valores possíveis: "grass" (grama), "water" (água), "forest" (floresta)
- "water" não aceita nenhuma ação; "forest" vira "grass" quando recebe estrada, zona ou prédio (custo em CLEAR_FOREST_COST)
- geração do terreno: usar City.seed; água ocupa de 10% a 15% do mapa em uma ou duas manchas contínuas; floresta cerca de 15% em manchas; o quadrado central de 8 x 8 é sempre grama

4) road
- indica se existe estrada neste tile
- tipo boolean, padrão false
- um tile com estrada não pode ter zona nem prédio

5) zone
- zona definida pelo jogador
- valores possíveis: "none", "residential", "commercial", "industrial"
- padrão: "none"
- só pode haver zona em tile sem estrada
- prédios de zona nascem automaticamente em tiles zonados vazios

6) building_id
- id do prédio que ocupa este tile
- tipo inteiro; NULL se o tile está vazio
- um prédio maior que 1x1 ocupa vários tiles, todos com o mesmo building_id

7) building (propriedade; NÃO é campo salvo)
- devolve o Building a partir de building_id, via `city.building_at(x, y)`; None se vazio
- não guardar o objeto dentro do Tile, para evitar referência circular ao salvar em JSON

8) near_road
- indica se algum dos 4 tiles vizinhos (cima, baixo, esquerda, direita) possui estrada
- tipo boolean
- derivado, recalculado quando uma estrada é criada ou demolida
- não verifica se a estrada leva a algum lugar
