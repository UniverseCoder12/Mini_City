# MiniCidade — versão Streamlit

## 1. Objetivo
Site de um jogo 2D de construção de cidade, no estilo SimCity, feito 100% em Python com Streamlit.
O jogador abre o site, constrói estradas, pinta zonas e coloca serviços clicando no mapa; a cidade cresce sozinha conforme a "demanda" e o jogador equilibra dinheiro, energia e felicidade dos moradores.
As regras do jogo são as mesmas da versão original (arquivo `02_regras_e_constantes.md`); o que muda aqui é a forma de jogar no navegador e a arquitetura, adaptadas ao funcionamento do Streamlit.
Não há objetivo de vitória: é uma "caixa de areia" que só termina por falência.

## 2. Como ler esta documentação
| Arquivo | Conteúdo |
|---|---|
| `00_visao_geral.md` | O que é o site, tecnologia, limitações do Streamlit, fases de desenvolvimento |
| `01_models/` | Estrutura dos dados em Python (dataclasses), incluindo o estado da interface |
| `02_regras_e_constantes.md` | TODAS as fórmulas, regras e números de balanceamento do jogo |
| `03_interface_streamlit.md` | Páginas, widgets, fluxo de cliques, tempo real com fragmentos |
| `04_estrutura_de_codigo.md` | Pastas, módulos, assinaturas de funções, dependências, testes |

**Regra de precedência:** números e fórmulas existem em um único lugar, `02_regras_e_constantes.md`. Se algum arquivo divergir dele, vale o `02`.

## 3. Tecnologia
- Python 3.10 ou superior
- Streamlit 1.37 ou superior (a partir dessa versão `st.fragment` é estável e aceita `run_every`; `st.navigation` e `st.Page` também são necessários)
- `streamlit-image-coordinates`: componente de terceiros que mostra uma imagem e devolve onde o usuário clicou (o Streamlit não tem clique em imagem nativo)
- Pillow: desenha o mapa como imagem (quadrados coloridos, sem arquivos de imagem externos)
- pytest: testes da simulação
- Sem banco de dados e sem back-end próprio: o estado fica na sessão e o save é um arquivo JSON baixado/enviado pelo jogador

## 4. Arquitetura em camadas
```
Páginas Streamlit (views/)        -> só montam a tela e chamam funções
Interface (ui/)                    -> estado da sessão, painéis, textos
Jogo (minicidade/)                 -> modelos, regras, simulação, desenho do mapa, save/load
                                      NÃO importa streamlit; testável sem navegador
```
Regra central: tudo o que é regra do jogo fica em `minicidade/` e funciona sem Streamlit. As páginas apenas chamam essas funções e mostram o resultado.

## 5. Limitações do Streamlit que moldam o projeto
| Limitação | Consequência no projeto |
|---|---|
| Cada interação reexecuta o script (o estado fica só em `st.session_state`) | Toda a cidade vive em `st.session_state["city"]`; nenhuma variável global de módulo guarda estado de jogo |
| Não existe laço de jogo contínuo | O tempo avança por um fragmento com `run_every`, que executa a cada 1 segundo enquanto a velocidade não for "pausado" |
| Não há clique em imagem nativo | Mapa desenhado como imagem + componente `streamlit-image-coordinates` |
| Não há arrastar para pintar | Estradas e zonas usam dois cliques (primeiro e segundo canto) |
| Recarregar a página (F5) cria uma sessão nova e perde o jogo | Salvar/Carregar por arquivo JSON; a interface avisa o jogador |
| O tempo só corre com a aba aberta e a sessão ativa | Comportamento aceito; o jogo não avança "offline" |
| Cada sessão guarda a cidade na memória do servidor | Cidade pequena (32 x 32); sem persistência no servidor |

## 6. Fora do escopo (por enquanto)
Contas de usuário, ranking, multiplayer, salvamento no servidor, salvamento automático no navegador, sons, desfazer (undo), tutorial guiado, condição de vitória, arrastar para pintar, celular (a interface é pensada para telas largas).

## 7. Pontos em aberto herdados
As decisões CR1 (equilíbrio da economia), CR2 (objetivo do jogo) e CR3 (serviços equivalentes) da revisão da versão original continuam em aberto. Esta versão adota os valores da v2 sem mudanças; o balanceamento deve ser validado por simulação (ver `04_estrutura_de_codigo.md`, seção 6).

## 8. Fases de desenvolvimento (com critério de aceite)
Pedir à IA uma fase por vez; só avançar quando o critério de aceite for atendido.

1. **Esqueleto e mapa.** `app.py` com navegação para as 3 páginas, "Novo jogo" com nome e seed, geração do terreno e mapa desenhado na página Jogar.
   Aceite: `streamlit run app.py` abre o site; a mesma seed gera sempre o mesmo mapa; seeds diferentes geram mapas diferentes; o quadrado central 8 x 8 é sempre grama.
2. **Cliques, dinheiro, estrada e demolir.** Componente de clique, ferramentas Estrada (dois cliques) e Demolir, painel de dinheiro.
   Aceite: clicar uma vez só marca o primeiro canto; o segundo clique desenha o caminho em "L"; sem dinheiro, a ação é recusada com mensagem e nada muda; o mesmo clique nunca é tratado duas vezes.
3. **Tempo e zonas.** Fragmento com `run_every`, botões de velocidade, contador de dias, ferramentas de zona; prédios nascem em zonas com estrada adjacente com chance fixa de 5% por tile por dia (regra provisória, substituída na fase 6).
   Aceite: pausado, `day` não muda; clicar no mapa com o jogo rodando não adianta o relógio; zona sem estrada adjacente não gera prédio.
4. **Fechamento mensal e fim de jogo.** Imposto e manutenção a cada 30 dias; falência.
   Aceite: o painel mostra receita, despesa e saldo do último mês; 3 fechamentos seguidos com dinheiro negativo mostram a tela de falência e param o tempo.
5. **Energia.** Usinas, consumo, apagão.
   Aceite: sem energia sobrando nenhum prédio novo nasce e aparece o aviso de apagão.
6. **Demanda e população.** Fórmulas de demanda, ocupantes, empregos, barras R / C / I.
   Aceite: com 1 usina a carvão, ruas em grade (uma rua a cada 3 linhas) e zonas R/C/I pintadas entre elas, a cidade cresce sozinha até mais de 100 habitantes e para quando `power_consumed` atinge `power_produced`. Este critério deve existir também como teste automatizado.
7. **Serviços, felicidade e inspeção.** Serviços, parques, poluição, níveis, abandono, ferramenta Inspecionar.
   Aceite: um prédio residencial cercado por escola, hospital, delegacia e parque chega ao nível 2 em 30 dias; um ao lado de usina a carvão e sem serviços não sobe de nível.
8. **Eventos, Salvar/Carregar e página Como jogar.**
   Aceite: baixar o save, abrir o site em outra aba, carregar o arquivo e obter exatamente o mesmo estado (dinheiro, dia, mapa, prédios, eventos ativos); arquivo inválido mostra erro sem derrubar o site.
