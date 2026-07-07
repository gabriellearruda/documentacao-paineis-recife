# [TÉCNICO] Página 3 – Hospitalizações

**Tab:** `tela_sih`  
**Módulos:** `R/sih_ui.R`, `R/sih_server.R`  
**Arquivo de dados:** `dados/df_sih.qs` → objeto `df_sih`  
**Tabela auxiliar:** `dados/cid_10.csv` → lida em runtime no `graf_obito`  
**Período:** 2016–2025

---

## Fonte dos dados

| Campo | Valor |
|---|---|
| Sistema | SIH – Sistema de Informações Hospitalares do SUS |
| Arquivo local | `dados/df_sih.qs` |
| Objeto R | `df_sih` |
| Tabela auxiliar | `dados/cid_10.csv` (colunas: `SUBCAT`, `CAPITULO`, `DESCRICAO_CAT`) |

---

## Pré-processamento

- `faixa_etaria_func()` aplicada sobre `df_sih` para gerar `faixa_etaria_padrao`

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
  2. `left_join(df_sih, cid_10, by = c("cd_diag_pri" = "SUBCAT"))`
  3. Filtra `CAPITULO` para capítulos XIX e XX da CID-10
  4. `tab_1(DESCRICAO_CAT)` → barras horizontais sobre `%`, ordenadas por `n`
- **Colunas:** `cd_diag_pri` (diagnóstico principal), `ano`; join para `CAPITULO`, `DESCRICAO_CAT`
- **Filtro aplicado:** somente `filtro_ano`

---

## Resumo de colunas utilizadas

| Coluna | Origem |
|---|---|
| `ano` | SIH original |
| `ds_raca` | SIH original |
| `cd_diag_pri` | SIH original (código CID-10 do diagnóstico principal) |
| `faixa_etaria_padrao` | Derivada via `faixa_etaria_func()` |
| `CAPITULO`, `DESCRICAO_CAT` | Join com `dados/cid_10.csv` via `cd_diag_pri = SUBCAT` |
