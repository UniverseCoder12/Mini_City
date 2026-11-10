Acontecimentos aleatórios que dão imprevisibilidade ao jogo. Chance, elegibilidade, duração e efeitos estão na seção 13 de `../02_regras_e_constantes.md`.

1) id
- identificador único do evento
- tipo inteiro, autoincremento

2) type
- tipo de evento
- valores possíveis: "fire", "power_failure", "festival", "boom"
- atenção: "power_failure" (evento) é diferente de CityStats.blackout (estado de falta de energia); o evento só reduz a produção das usinas

3) day
- dia do jogo em que o evento começou
- tipo inteiro, referente a City.day

4) duration
- duração em dias
- tipo inteiro, sempre maior que 0 (fire: 5, power_failure: 10, festival: 15, boom: 20)

5) active
- o evento ainda está em andamento?
- tipo boolean
- vira falso quando City.day >= day + duration

6) building_id
- prédio afetado, apenas para eventos do tipo "fire"
- tipo inteiro; NULL nos demais
- referente ao atributo id da classe Building

7) message
- texto mostrado ao jogador quando o evento começa
- tipo String
- exemplos de valores:
  - "Um incêndio começou em um prédio!"
  - "Falha nas usinas: a produção de energia caiu pela metade."
  - "Festival na cidade! A população está mais feliz."
