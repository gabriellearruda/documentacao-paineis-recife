# [TÉCNICO] Página 6 – Linha da Vida

**Tab:** `linhavida`  
**Módulo:** `R/linha_vida.R`  
**Arquivo de dados:** `dados/linha_vida_esus4.qs` → objeto `df_linha_vida` (carregado no `global.R`)  
**Período:** determinado pelos dados (registros com `dt_registro` / `dt_evento_inicio`)

---

## Fonte dos dados

| Campo | Valor |
|---|---|
| Arquivo local | `dados/linha_vida_esus4.qs` |
| Objeto R | `df_linha_vida` |
| Sistemas integrados | SINAN_VIOL, SIM, SIH, SINAN_IEXO, ESUS_APS |

---

## Pré-processamento em `linha_vida.R`

```r
# Converte dt_registro para Date
# Preenche nome_ultimo_bairro NA com "Sem informação"
# Deriva flags de exclusividade por mulher:
#   fl_esus_aps: se a mulher tem qualquer registro no ESUS_APS
#   so_sinan:    se TODOS os registros da mulher são SINAN_VIOL
#   so_esus_aps: se TODOS os registros da mulher são ESUS_APS
# Calcula idade_minima por mulher → faixa_etaria_func()
# Calcula max_notif_global para montar o filtro de nº de notificações
```

---

## Filtros

| Input ID | Variável filtrada | Tipo |
|---|---|---|
| `filtro_bairro` | `nome_ultimo_bairro` | pickerInput múltiplo (live-search) |
| `filtro_raca` | `ds_raca_padronizada` | pickerInput múltiplo |
| `filtro_idade` | `faixa_etaria_padrao` | pickerInput múltiplo |
| `filtro_banco` | flags `fl_sinan_viol`, `fl_sim`, `fl_sih`, `fl_sinan_iexo`, `fl_esus_aps`, `so_sinan`, `so_esus_aps` | pickerInput múltiplo |
| `filtro_violencias2` | colunas binárias `fl_viol_*` (filter_at/any_vars) | pickerInput múltiplo |
| `filtro_autoprovocada` | `fl_les_autop` | pickerInput múltiplo (0/1) |
| `filtro_obitos` | `fl_sim` | pickerInput múltiplo (0/1) |
| `filtro_n_notif` | contagem de registros `SINAN_VIOL` por `id_pessoa` | pickerInput múltiplo |

**Aplicação:** os filtros são acumulados em `filtros_aplicados` (reactiveValues) e só enviados ao `df_filtrado()` ao clicar em `btn_filtrar`.

**Filtragem de banco** (`filtrar_bancos()`): lógica de OR entre flags; `EXCLUSIVO_SINAN_VIOL` filtra `so_sinan == 1`; `EXCLUSIVO_ESUS_APS` filtra `so_esus_aps == 1`.

---

## Outputs

### `linha_vida_geral_` — plotlyOutput
- **Base:** `df_filtrado()` após `filtrar_bancos()`
- **Eixo X:** `dt_comum` = `coalesce(dt_registro, dt_evento_inicio, dt_evento_fim)` convertido para Date
- **Eixo Y:** `par_reduzido_1 = as.numeric(factor(id_pareamento)) * 20` (posição por mulher)
- **Cor/forma:** `banco` → `colors_banco` / `shapes_banco`
- **Interatividade:** registra `plotly_click` e `plotly_doubleclick` (source `"A"`)

### `selected_point_info` — uiOutput
- **Trigger:** clique em ponto (`selected_point()`)
- **Colunas exibidas:** `ds_raca_padronizada`, `nu_idade_anos`, `texto_final`

### `resumo_linhavida` — uiOutput
- **Lógica:** sobre `df_filtrado()` após `filtrar_bancos()`:
  - `n_distinct(id_pessoa)` → nº de mulheres
  - `nrow(filter(banco == "SINAN_VIOL"))` → nº registros de violência
  - `count(id_pessoa)` → `max`, `mean`, `median` de notificações por mulher

### Download `btn_download`
- **Lógica:** `df_filtrado() |> filtrar_bancos() |> distinct(id_pessoa, texto_final)`
- **Formato:** `.xlsx` via `openxlsx::write.xlsx`

---

## Colunas principais utilizadas

| Coluna | Origem |
|---|---|
| `id_pessoa` | Identificador único da mulher no linkage |
| `id_pareamento` | Identificador de grupo de linkage |
| `banco` | Sistema de origem do registro (`SINAN_VIOL`, `SIM`, `SIH`, `SINAN_IEXO`, `ESUS_APS`) |
| `dt_registro` | Data de registro do evento |
| `dt_evento_inicio`, `dt_evento_fim` | Datas alternativas do evento |
| `dt_comum` | Derivada: `coalesce(dt_registro, dt_evento_inicio, dt_evento_fim)` |
| `ds_raca_padronizada` | Raça/cor padronizada |
| `nu_idade_anos` | Idade em anos |
| `faixa_etaria_padrao` | Derivada via `faixa_etaria_func()` sobre `idade_minima` |
| `nome_ultimo_bairro` | Último bairro de residência (NA → "Sem informação") |
| `fl_sinan_viol`, `fl_sim`, `fl_sih`, `fl_sinan_iexo`, `fl_esus_aps` | Flags de presença em cada sistema |
| `so_sinan`, `so_esus_aps` | Flags de exclusividade (derivadas) |
| `fl_les_autop` | Flag de lesão autoprovocada |
| `fl_viol_fisic` … `fl_viol_outr` | Flags de tipo de violência |
| `texto_final` | Texto descritivo da trajetória (HTML) |
