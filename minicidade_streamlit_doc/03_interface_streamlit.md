# Interface Streamlit

## 1. Visão geral
Site com três páginas, navegação lateral e uma cidade por sessão.
Aparência: layout largo (`layout="wide"`), título "MiniCidade", ícone 🏙️.

## 2. Regras do Streamlit que o projeto deve respeitar
1. **Estado só em `st.session_state`.** Nunca guardar cidade, rng ou mensagens em variáveis globais de módulo: elas seriam compartilhadas entre todos os usuários.
2. **Inicialização única.** `init_state()` (em `ui/state.py`) cria as chaves que ainda não existem; é chamado no começo de `app.py`, antes da navegação.
3. **`st.set_page_config` deve ser o primeiro comando Streamlit de `app.py`.**
4. **Navegação por `st.navigation` e `st.Page`.** As páginas ficam na pasta `views/` (não usar a pasta `pages/`, para não misturar com a descoberta automática de páginas do Streamlit).
5. **Widgets com `key` são descartados quando a página deixa de renderizá-los.** Ao sair da página Jogar e voltar, velocidade e ferramenta voltam ao valor inicial (`paused` e `inspect`). Isso é comportamento padrão do Streamlit e é aceito: o jogo "pausa" ao sair da página.
6. **Nunca escrever em `st.session_state[chave_de_widget]` depois de o widget ter sido criado na mesma execução** (o Streamlit levanta exceção). Alterações dessas chaves só em callbacks (`on_change`, `on_click`) ou antes de o widget ser criado.
7. **Fragmentos.** A área do jogo é uma função decorada com `st.fragment(run_every=...)`. Duas consequências:
   - o fragmento é reexecutado tanto pelo temporizador quanto por qualquer clique dentro dele; por isso o avanço do tempo usa `last_tick_time` (seção 4.3)
   - widgets fora do fragmento (a barra lateral) só atualizam quando o app inteiro é reexecutado; quando algo do fragmento precisa mudar a barra lateral, chamar `st.rerun()` (escopo app)
8. **`run_every` dinâmico.** O intervalo depende da velocidade: `REFRESH_SECONDS` se `speed` != "paused", senão `None`. Como a velocidade é um widget da barra lateral (fora do fragmento), trocar a velocidade reexecuta o app inteiro e o fragmento é redefinido com o novo intervalo:
```python
run_every = REFRESH_SECONDS if st.session_state.get("speed", "paused") != "paused" else None
st.fragment(run_every=run_every)(game_view)()
```
9. **Cliques repetidos.** O componente de clique devolve o último clique a cada execução do script. Cada clique só pode ser tratado uma vez: comparar `unix_time` com `last_click_unix` (seção 4.4).
10. **Imagem como fonte de cliques.** O componente devolve a posição do clique em pixels relativa à imagem exibida. Conferir, na versão instalada do componente, quais campos ele devolve (`x`, `y`, `unix_time` e, em versões recentes, `width` e `height` da imagem exibida) e como fixar a largura exibida igual à largura real da imagem (parâmetro `width`).

## 3. Páginas
| Arquivo | Título na navegação | Conteúdo |
|---|---|---|
| `views/jogar.py` | 🏙️ Jogar | Barra lateral de ferramentas e a área do jogo (fragmento) |
| `views/como_jogar.py` | 📖 Como jogar | Texto de ajuda estático, com a tabela de prédios gerada a partir do catálogo |
| `views/salvar_carregar.py` | 💾 Salvar / Carregar | Novo jogo, baixar save, carregar save |

## 4. Página Jogar

### 4.1 Barra lateral (fora do fragmento)
| Widget | key | Detalhes |
|---|---|---|
| `st.radio` Velocidade | `speed` | opções `paused`, `normal`, `fast` com rótulos "⏸ Pausado", "▶ Normal", "⏩ Rápido"; desabilitado se `city.game_over` |
| `st.radio` Ferramenta | `tool` | opções do `model_07_ui_state.md`, com rótulos em português; `on_change` limpa `pending` |
| `st.selectbox` Prédio | `build_type_id` | só aparece quando `tool` = `build`; lista os tipos de categoria power, service e park com `unlock_population` <= população; cada opção mostra nome e custo |
| `st.slider` Imposto (%) | `tax_slider` | de TAX_MIN a TAX_MAX, `value=city.tax_rate`; `on_change` copia o valor para `city.tax_rate` |
| `st.button` Cancelar seleção | `cancel_pending` | só aparece se `pending` não for None; limpa `pending` |

### 4.2 Área do jogo (dentro do fragmento `game_view`)
Disposição: uma linha de métricas no topo e, abaixo, duas colunas (mapa à esquerda, painéis à direita, proporção 3 para 1).
- **Métricas (`st.metric`):** dinheiro, data (dia e mês), população, felicidade, energia (produzida / consumida), saldo do último mês
- **Mapa:** imagem desenhada por `render_map` dentro do componente de clique
- **Painéis (direita):**
  - Demanda: três linhas "Residencial", "Comercial", "Industrial", cada uma com `st.progress` (valor = (demanda + 100) / 200) e o número com sinal ao lado
  - Inspeção: dados do tile em `selected_tile`; se houver prédio, mostra tipo, nível, ocupantes, felicidade, energia, estrada, estado (em chamas, abandonado)
  - Mensagens: as 5 últimas de `messages`; o restante em um `st.expander`
- **Fim de jogo:** se `city.game_over`, em vez do mapa interativo mostra `st.error` com dias jogados e população máxima e orienta a usar "Novo jogo" na página Salvar / Carregar

### 4.3 Ordem de execução do fragmento
1. **Tick do relógio.** Se `speed` != "paused", `city.game_over` é falso e `time.monotonic() - last_tick_time` >= REFRESH_SECONDS x 0,9: atualizar `last_tick_time` e executar `TICKS_NORMAL` ou `TICKS_FAST` vezes `tick(city, rng)`. Sem essa guarda, cada clique no mapa adiantaria o relógio. Adicionar as mensagens do relatório (`TickReport`) a `messages` e mostrar cada uma com `st.toast`
2. **Reação ao relatório.** Se o relatório indicar `game_over` ou `new_unlocks` não vazio, chamar `st.rerun()` (escopo app) para atualizar a barra lateral
3. **Métricas** (seção 4.2)
4. **Mapa e clique** (seção 4.4)
5. **Painéis** (seção 4.2)

### 4.4 Tratamento de cliques
```python
img = render_map(city, pending=ui.pending, selected=ui.selected_tile)
click = streamlit_image_coordinates(img, key="map")   # ver regra 10 da seção 2
if click and click["unix_time"] != ui.last_click_unix:
    ui.last_click_unix = click["unix_time"]
    tile = pixel_to_tile(click, img.size, city)       # None se fora do mapa
    if tile is not None and handle_click(tile):       # True se algo mudou
        st.rerun(scope="fragment")                    # redesenha o mapa já com o resultado
```
`handle_click(tile)` (em `ui/actions_ui.py`) aplica a ferramenta atual:

| Ferramenta | Cliques | Comportamento |
|---|---|---|
| inspect | 1 | `selected_tile` = tile clicado |
| road | 2 | 1º clique: `pending` = tile. 2º clique: `paint_road(city, pending, tile)` e `pending` = None |
| zone_residential, zone_commercial, zone_industrial | 2 | 1º clique: `pending` = tile. 2º clique: `paint_zone(city, zona, pending, tile)` e `pending` = None |
| build | 1 | `place_building(city, build_type_id, x, y)` com o tile clicado como canto superior esquerdo |
| demolish | 1 | `demolish(city, x, y)` |

- Toda ação devolve `ActionResult`; se `ok` for falso, a mensagem vai para `messages` e para `st.toast` e nada muda
- Com `pending` definido, o mapa mostra o primeiro canto destacado e abaixo do mapa aparece a legenda "Primeiro canto em (x, y): clique no segundo canto"
- Mudar de ferramenta ou clicar em "Cancelar seleção" zera `pending`
- Depois de qualquer ação que alterou a cidade, chamar `recompute_derived(city)` antes de redesenhar

## 5. Página Como jogar
Texto estático em Markdown com: objetivo do jogo, como começar em 4 passos (1. faça uma estrada, 2. construa uma usina a carvão perto, 3. pinte zonas ao lado da estrada, 4. aperte Normal e acompanhe a demanda), significado das barras R / C / I, legenda de cores do mapa e tabela dos prédios.
A tabela de prédios (nome, custo, manutenção, efeito) é gerada em código a partir do catálogo `BUILDING_TYPES`, para nunca ficar diferente do jogo.

## 6. Página Salvar / Carregar
Três blocos:
1. **Novo jogo:** `st.text_input` (nome da cidade) e `st.number_input` (seed; 0 significa "sortear"), botão "Criar". Ao criar: `reset_game(name, seed)`, velocidade fica pausada
2. **Baixar save:** `st.download_button` com `city_to_json(city)`; nome do arquivo `<nome>_dia<day>.json`; `mime="application/json"`
3. **Carregar save:** `st.file_uploader` (tipo json) e um botão "Carregar" separado. O arquivo só é aplicado ao clicar no botão (o uploader mantém o arquivo entre execuções e, sem o botão, recarregaria a cada execução). Ao carregar: `city_from_json(texto)`; em caso de `SaveError`, mostrar `st.error` com o motivo e manter a cidade atual; em caso de sucesso, substituir a cidade, recriar o `rng`, limpar `pending`, `selected_tile` e `messages` e mostrar `st.success`

Aviso permanente no topo da página: "Recarregar a página apaga o jogo em andamento. Baixe o save antes."

## 7. Aparência do mapa
Tile de TILE_PX pixels; cores em hexadecimal (sugestão):

| Elemento | Cor |
|---|---|
| grama | `#9ccc65` |
| água | `#4fc3f7` |
| floresta | `#2e7d32` |
| estrada | `#424242` |
| zona residencial vazia | `#c8e6c9` |
| zona comercial vazia | `#bbdefb` |
| zona industrial vazia | `#fff9c4` |
| prédio residencial | `#66bb6a` |
| prédio comercial | `#1e88e5` |
| prédio industrial | `#fdd835` |
| usina | `#ef6c00` |
| serviço | `#8e24aa` |
| parque | `#00c853` |

- Prédios de zona mostram pontos brancos no canto indicando o nível (1 a 3)
- Prédio em chamas: contorno vermelho `#e53935`; prédio abandonado: cor escurecida
- Prédios especiais mostram uma letra no centro (U usina, P polícia, B bombeiros, E escola, H hospital, A parque), usando a fonte padrão do Pillow (sem arquivos de fonte)
- Primeiro canto pendente: contorno amarelo `#ffeb3b`; tile em inspeção: contorno branco
- Linhas de grade finas (`#00000020`) entre os tiles
- Tema do Streamlit em `.streamlit/config.toml` (cor primária e fundo claro)

## 8. Desempenho
- Mapa de 32 x 32 tiles a 20 px = imagem de 640 x 640 px: desenhar em poucos milissegundos
- Felicidade: iterar apenas sobre os prédios que têm `effect_radius` > 0 (usinas a carvão, fábricas, serviços, parques), não sobre todos os pares de prédios
- No modo `fast` são feitos 5 ticks por execução, mas o mapa é desenhado uma vez só
- Não usar `st.cache_data` na cidade (ela muda); cache só para dados imutáveis, como a tabela do catálogo

## 9. Limitações conhecidas desta interface
- Dois cliques para estrada e zona em vez de arrastar; tiles inválidos no meio do caminho são ignorados
- Não há desfazer: erros custam dinheiro
- Recarregar a página perde o jogo não salvo
- O tempo só corre enquanto a aba está aberta e a página Jogar visível
- Sem versão otimizada para celular
