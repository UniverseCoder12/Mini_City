Um prédio que existe de fato no mapa (instância de um BuildingType).

1) id
- identificador único do prédio
- tipo inteiro, autoincremento

2) type_id
- chave do tipo de construção
- referente ao atributo id da classe BuildingType
- tipo String

3) type (propriedade; NÃO é campo salvo)
- BuildingType obtido do catálogo por `BUILDING_TYPES[type_id]`

4) x
- coluna do tile do canto superior esquerdo do prédio
- tipo inteiro

5) y
- linha do tile do canto superior esquerdo do prédio
- tipo inteiro

6) level
- nível de evolução do prédio
- tipo inteiro, de 1 a MAX_LEVEL, começa em 1
- apenas prédios de zona (residential, commercial, industrial) mudam de nível; os demais ficam em 1
- regras de subida e descida: seção 11 das regras

7) occupants
- quantidade atual de moradores
- tipo inteiro, de 0 até capacity x level
- usado apenas por prédios residential; nos demais vale sempre 0 (empregos são a própria capacity, ver regras, seção 7)

8) built_day
- dia do jogo em que o prédio foi construído
- tipo inteiro, referente a City.day

9) powered
- o prédio está com energia?
- tipo boolean
- derivado: verdadeiro quando não há apagão na cidade (a energia é global)

10) connected
- o prédio tem acesso a estrada?
- tipo boolean
- derivado: verdadeiro se pelo menos um dos tiles que o prédio ocupa tem near_road verdadeiro
- só importa para prédios de zona; prédios especiais não precisam de estrada

11) happiness
- felicidade local do prédio, de 0 a 100
- tipo inteiro
- derivado: fórmula na seção 10 das regras

12) days_happy
- dias seguidos com happiness acima de HAPPY_LEVEL_UP
- tipo inteiro, começa em 0
- usado só por prédios de zona; deve ser salvo

13) days_unhappy
- dias seguidos com happiness abaixo de HAPPY_LEVEL_DOWN
- tipo inteiro, começa em 0
- usado só por prédios de zona; deve ser salvo

14) on_fire
- o prédio está pegando fogo?
- tipo boolean, padrão false
- vira verdadeiro por um GameEvent do tipo "fire" e volta a falso quando o evento termina (ver regras, seção 13)

15) abandoned
- prédio residencial abandonado
- tipo boolean, padrão false
- só para prédios residential; regras na seção 11 das regras
- prédios abandonados continuam ocupando o tile até serem demolidos
