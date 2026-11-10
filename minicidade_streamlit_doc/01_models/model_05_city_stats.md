Números calculados a cada tick a partir do estado da cidade. Nada aqui é digitado pelo jogador; tudo aparece no painel do jogo.
Exceção: `income`, `expenses` e `balance` só são atualizados no fechamento do mês e devem ser salvos no jogo.
As fórmulas completas estão em `../02_regras_e_constantes.md` (seções 6, 7, 10 e 12).

1) population
- total de moradores da cidade
- tipo inteiro
- soma de occupants de todos os prédios residential

2) working_age
- população em idade de trabalhar
- tipo inteiro
- floor(population x WORKING_AGE_RATIO)

3) residential_capacity
- capacidade total dos prédios residenciais não abandonados
- tipo inteiro

4) jobs_commercial
- empregos nos prédios comerciais conectados e que não estão em chamas
- tipo inteiro

5) jobs_industrial
- empregos nos prédios industriais conectados e que não estão em chamas
- tipo inteiro

6) jobs
- total de empregos
- tipo inteiro
- jobs_commercial + jobs_industrial

7) workers
- empregos efetivamente ocupados
- tipo inteiro
- min(working_age, jobs)

8) unemployment
- taxa de desemprego, de 0 a 100 (%)
- tipo número
- 0 se working_age for 0; senão (working_age - workers) / working_age x 100

9) demand_residential
- demanda por moradias, de -100 a +100
- tipo inteiro
- inclui o impulso inicial e o limite por vacância descritos na seção 7 das regras

10) demand_commercial
- demanda por comércio, de -100 a +100
- tipo inteiro

11) demand_industrial
- demanda por indústria, de -100 a +100
- tipo inteiro

12) happiness
- felicidade média da cidade, de 0 a 100
- tipo inteiro
- média de happiness dos prédios residenciais com moradores; vale 50 se não houver nenhum

13) power_produced
- energia produzida (já considerando evento power_failure)
- tipo inteiro

14) power_consumed
- energia consumida por todos os prédios
- tipo inteiro

15) blackout
- indica se há apagão
- tipo boolean
- verdadeiro quando power_produced < power_consumed

16) road_tiles
- quantidade de tiles com estrada
- tipo inteiro

17) income
- receita do último mês fechado
- tipo inteiro
- salvo no jogo; 0 antes do primeiro fechamento

18) expenses
- despesa do último mês fechado
- tipo inteiro
- salvo no jogo; 0 antes do primeiro fechamento

19) balance
- income - expenses do último mês fechado
- tipo inteiro, pode ser negativo
- salvo no jogo
