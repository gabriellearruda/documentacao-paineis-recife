# [TÉCNICO] Página 4 – Mortalidade

**Tab:** `tela_sim`  
**Módulos:** `R/sim_ui.R`, `R/sim_server.R`  
**Arquivo de dados:** `dados/df_sim.qs` → objeto `df_sim`  
**Tabela auxiliar:** `dados/cid_10.csv` → lida em runtime no `graf_obito`  
**Período:** 2016–2025

---

## Fonte dos dados

| Campo | Valor |
|---|---|
| Sistema | SIM – Sistema de Informação sobre Mortalidade |
| Arquivo local | `dados/df_sim.qs` |
| Objeto R | `df_sim` |
| Tabela auxiliar | `dados/cid_10.csv` (colunas: `SUBCAT`, `CAPITULO`, `DESCRICAO_CAT`) |

---

## Pré-processamento

- `faixa_etaria_func()` aplicada sobre `df_sim` para gerar `faixa_etaria_padrao`

---

## Filtros

| Input ID | Variável filtrada | Tipo |
|---|---|---|
| `filtro_idade` | `faixa_etaria_padrao` | pickerInput múltiplo |
| `filtro_raca` | `ds_raca` | pickerInput múltiplo |
| `filtro_ano` | `ano` | pickerInput múltiplo |

---

## Outputs

### `freq_ano_graf` — plotlyOutput
- **Função:** `ano_graf(df)` → `tab_1(ano)` → linha sobre `n`
- **Colunas:** `ano`, `faixa_etaria_padrao`, `ds_raca`
- **Obs.:** filtro de `ano` **não** é aplicado neste gráfico

### `faixa_etaria_graf` — plotlyOutput
- **Função:** `faixa_etaria_graf(df)` → `tab_1(faixa_etaria_padrao)` → barras verticais sobre `%`
- **Colunas:** `faixa_etaria_padrao`, `ds_raca`, `ano`
- **Download:** `download_tab_faixa_etaria` → `.xlsx`

### `raca_cor_graf` — plotlyOutput
- **Função:** `raca_cor_graf(df)` → `tab_1(ds_raca)` → barras horizontais sobre `%`
- **Colunas:** `ds_raca`, `faixa_etaria_padrao`, `ano`
- **Download:** `download_tab_raca_cor` → `.xlsx`

### `graf_obito` — plotlyOutput
- **Lógica:**
  1. Lê `dados/cid_10.csv` em runtime
  2. `left_join(df_sim, cid_10, by = c("cd_causabas" = "SUBCAT"))`
  3. Filtra `CAPITULO` para capítulos XIX e XX da CID-10
  4. `tab_1(DESCRICAO_CAT)` → barras horizontais sobre `%`, ordenadas por `n`
- **Colunas:** `cd_causabas` (causa básica do óbito), `ano`; join para `CAPITULO`, `DESCRICAO_CAT`
- **Filtro aplicado:** somente `filtro_ano`

---

## Resumo de colunas utilizadas

| Coluna | Origem |
|---|---|
| `ano` | SIM original |
| `ds_raca` | SIM original |
| `cd_causabas` | SIM original (código CID-10 da causa básica do óbito) |
| `faixa_etaria_padrao` | Derivada via `faixa_etaria_func()` |
| `CAPITULO`, `DESCRICAO_CAT` | Join com `dados/cid_10.csv` via `cd_causabas = SUBCAT` |
