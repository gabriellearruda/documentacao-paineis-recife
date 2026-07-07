# [TÉCNICO] Página 5 – Análise do Linkage

**Tab:** `analise_linkage`  
**Módulo:** `R/linkage.R`  
**Arquivos de dados:**
- `dados/linkage_compilado_sem_banco.RData` → objeto `linkage_compilado`
- `dados/base_linkage_feminino.RData` → objeto `base_linkage`
- `dados/icd_map_ufmg.Rdata` → objeto `icd_map`

**Período:** KPIs e perfil: 2016–2025 / Gráficos comparativos: 2019–2025

---

## Fontes dos dados

| Objeto | Origem | Conteúdo |
|---|---|---|
| `linkage_compilado` | `dados/linkage_compilado_sem_banco.RData` | Dados agregados por combinação de flags (violência, esus, raça, faixa etária) |
| `base_linkage` | `dados/base_linkage_feminino.RData` | Registros individuais com banco de origem + flags de linkage |
| `icd_map` | `dados/icd_map_ufmg.Rdata` | Mapeamento `icd_code_4 → CIDBR_RESUMIDO_EXTERNAS` (UFMG) |

---

## Pré-processamento em `linkage.R`

```r
# Seleção dos campos de KPI
linkage_kpi <- linkage_compilado |>
  select(rotulo_viol_interpessoal, fl_esus, raca_cor,
         faixa_etaria_padrao, fl_ob_not_externas, registros, n_pessoas)

# Separação por banco de dados
df_obitos    <- base_linkage |> filter(banco == "SIM")
df_internacoes <- base_linkage |> filter(banco == "SIH")

# Join com dicionário CID (renomeia icd_code_4 → cd_causabas, CIDBR_RESUMIDO_EXTERNAS → causa_resumida)
df_obitos    <- df_obitos    |> left_join(icd_map, by = "cd_causabas")
df_internacoes <- df_internacoes |> left_join(icd_map, by = "cd_causabas")

# Pré-computação do gráfico SINAN Viol vs IEXO
viol_iexo <- base_linkage |> filter(banco %in% c("SINAN_VIOL", "SINAN_IEXO"))
```

---

## Filtros (aplicados sobre `linkage_kpi`)

| Input ID | Variável filtrada | Tipo |
|---|---|---|
| `filtro_idade` | `faixa_etaria_padrao` | pickerInput múltiplo |
| `filtro_raca` | `raca_cor` | pickerInput múltiplo |
| `filtro_esus` | `fl_esus` (0/1) | pickerInput múltiplo |

**Reactive base:** `kpi_filtrada()` — aplica os três filtros sobre `linkage_kpi`

---

## Outputs

### `num_registros` — uiOutput (KPI card)
- **Lógica:** `sum(registros)` sobre `kpi_filtrada()`
- **Coluna:** `registros`

### `num_mulheres` — uiOutput (KPI card)
- **Lógica:** `sum(n_pessoas)` sobre `kpi_filtrada()`
- **Coluna:** `n_pessoas`

### `mulheres_notificadas` — uiOutput (KPI card)
- **Lógica:** `sum(n_pessoas)` onde `rotulo_viol_interpessoal == 1`
- **Colunas:** `n_pessoas`, `rotulo_viol_interpessoal`

### `obitos_agressao_notif` — uiOutput (KPI card)
- **Lógica:** `sum(n_pessoas)` onde `fl_ob_not_externas == 1`
- **Colunas:** `n_pessoas`, `fl_ob_not_externas`

### `faixa_etaria_graf` — plotlyOutput
- **Função:** `faixa_etaria_graf_npessoas(kpi_filtrada())`
- **Lógica:** agrupa por `(faixa_etaria_padrao, rotulo_viol_interpessoal)`, soma `n_pessoas`, calcula `pct` dentro de cada grupo
- **Colunas:** `faixa_etaria_padrao`, `rotulo_viol_interpessoal`, `n_pessoas`
- **Download:** `download_tab_faixa_etaria` → `.xlsx`

### `raca_cor_graf` — plotlyOutput
- **Função:** `raca_cor_graf_npessoas(kpi_filtrada())`
- **Lógica:** agrupa por `(raca_cor, rotulo_viol_interpessoal)`, soma `n_pessoas`, calcula `pct` dentro de cada grupo
- **Colunas:** `raca_cor`, `rotulo_viol_interpessoal`, `n_pessoas`
- **Download:** `download_tab_raca_cor` → `.xlsx`

### `causas_obito_linkage` — plotlyOutput
- **Base:** `df_obitos` (de `base_linkage` filtrado por `banco == "SIM"`)
- **Lógica:** 3 grupos via `FL_SINAN_VIOL` e `FL_SINAN_IEXO` → `tab_1(causa_resumida)` em cada → bind_rows → bubble chart
- **Grupos:** `Com notificação de violência` (FL_SINAN_VIOL==1), `Com notificação de intoxicação exógena` (FL_SINAN_IEXO==1), `Sem notificação` (ambos != 1)
- **Colunas:** `banco`, `FL_SINAN_VIOL`, `FL_SINAN_IEXO`, `causa_resumida` (via join com `icd_map`)
- **Download:** `download_bolha` → `.xlsx`

### `causas_internacao_linkage` — plotlyOutput
- **Base:** `df_internacoes` (de `base_linkage` filtrado por `banco == "SIH"`)
- **Lógica:** idêntica ao `causas_obito_linkage`
- **Colunas:** mesmas, sobre internações
- **Download:** `download_bolha_internacao` → `.xlsx`

### `graf_viol_iexo` — plotlyOutput
- **Base:** pré-computado (`df` com `so_viol`, `so_iexo`, `ambos`)
- **Lógica:** conta mulheres únicas (`id_pessoa`) por combinação de `FL_SINAN_VIOL` e `FL_SINAN_IEXO`
- **Não reage aos filtros da página**
- **Download:** `download_viol_iexo` → `.xlsx`

---

## Resumo de colunas utilizadas

| Coluna | Objeto | Origem |
|---|---|---|
| `rotulo_viol_interpessoal` | `linkage_compilado` | Flag: mulher tem notificação de violência |
| `fl_esus` | `linkage_compilado` | Flag: mulher tem registro no e-SUS APS |
| `fl_ob_not_externas` | `linkage_compilado` | Flag: mulher com notificação de violência foi a óbito por causas externas |
| `raca_cor` | `linkage_compilado` | Raça/cor |
| `faixa_etaria_padrao` | `linkage_compilado` | Faixa etária |
| `registros` | `linkage_compilado` | Contagem de registros no linkage |
| `n_pessoas` | `linkage_compilado` | Número de mulheres únicas |
| `banco` | `base_linkage` | Sistema de origem do registro |
| `FL_SINAN_VIOL` | `base_linkage` | Flag: registro linkado ao SINAN Violências |
| `FL_SINAN_IEXO` | `base_linkage` | Flag: registro linkado ao SINAN IEXO |
| `cd_causabas` | `base_linkage` | Código CID-10 da causa |
| `causa_resumida` | `icd_map` (join) | Descrição resumida da causa (UFMG) |
| `id_pessoa` | `base_linkage` | Identificador único da mulher |
