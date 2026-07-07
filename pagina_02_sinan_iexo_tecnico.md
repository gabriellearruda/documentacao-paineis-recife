# [TÉCNICO] Página 2 – SINAN Intoxicação Exógena

**Tab:** `tela_iexo`  
**Módulos:** `R/iexo_ui.R`, `R/iexo_server.R`  
**Arquivo de dados:** `dados/df_iexo.qs` → objeto `df_iexo`  
**Período:** 2016–2025

---

## Fonte dos dados

| Campo | Valor |
|---|---|
| Sistema | SINAN – Sistema de Informação de Agravos de Notificação |
| Ficha | Intoxicação Exógena |
| Arquivo local | `dados/df_iexo.qs` |
| Objeto R | `df_iexo` |

---

## Pré-processamento

- `faixa_etaria_func()` aplicada sobre `df_iexo` para gerar `faixa_etaria_padrao`

---

## Filtros

| Input ID | Variável filtrada | Tipo |
|---|---|---|
| `filtro_idade` | `faixa_etaria_padrao` | pickerInput múltiplo |
| `filtro_raca` | `ds_raca` | pickerInput múltiplo |
| `filtro_ano` | `ano` | pickerInput múltiplo |
| `filtro_circuns` | `ds_circunstan` | pickerInput múltiplo (valores únicos da coluna) |

---

## Outputs

### `freq_ano_graf` — plotlyOutput
- **Função:** `ano_graf(df)` → `tab_1(ano)` → linha sobre `n`
- **Colunas:** `ano`, `faixa_etaria_padrao`, `ds_raca`, `ds_circunstan`
- **Obs.:** filtro de ano **não** é aplicado neste gráfico (usa apenas idade, raça, circunstância)

### `faixa_etaria_graf` — plotlyOutput
- **Função:** `faixa_etaria_graf(df)` → `tab_1(faixa_etaria_padrao)` → barras verticais sobre `%`
- **Colunas:** `faixa_etaria_padrao`, `ds_raca`, `ds_circunstan`, `ano`
- **Download:** `download_tab_faixa_etaria` → `.xlsx`

### `raca_cor_graf` — plotlyOutput
- **Função:** `raca_cor_graf(df)` → `tab_1(ds_raca)` → barras horizontais sobre `%`
- **Colunas:** `ds_raca`, `faixa_etaria_padrao`, `ds_circunstan`, `ano`
- **Download:** `download_tab_raca_cor` → `.xlsx`

### `circunstancia_graf` — plotlyOutput
- **Lógica:** `tab_1(ds_circunstan)` → reorder por `n` → barras horizontais sobre `%`
- **Coluna:** `ds_circunstan`
- **Download:** `download_tab_circunstancia` → `.xlsx`

### `ag_intox_graf` — plotlyOutput
- **Lógica:** `tab_1(ds_agente_tox)` → reorder por `n` → barras horizontais sobre `%`
- **Coluna:** `ds_agente_tox`
- **Download:** `download_tab_ag_intox` → `.xlsx`

### `atend_hospit_graf` — plotlyOutput
- **Lógica:** `tab_2(ds_tpatend, ds_hospital)` + `tab_2(..., pct_row=TRUE)` → merge → barras empilhadas
- **Colunas:** `ds_tpatend` (tipo de atendimento), `ds_hospital` (hospitalização: Sim/Não/Ignorado)
- **Categorias de `ds_tpatend`:** `Ambulatorial`, `Domiciliar`, `Hospitalar`, `Ignorado`, `Nenhum`
- **Download:** `download_atend_hospit_graf` → `.xlsx`

---

## Resumo de colunas utilizadas

| Coluna | Origem |
|---|---|
| `ano` | SINAN original |
| `ds_raca` | SINAN original |
| `ds_circunstan` | SINAN original |
| `ds_agente_tox` | SINAN original |
| `ds_tpatend` | SINAN original |
| `ds_hospital` | SINAN original |
| `faixa_etaria_padrao` | Derivada via `faixa_etaria_func()` |
