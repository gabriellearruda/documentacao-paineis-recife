# [TÉCNICO] Página 1 – SINAN Violência

**Tab:** `tela_sinan`  
**Módulos:** `R/viol_ui.R`, `R/viol_server.R`  
**Arquivo de dados:** `dados/sinan_viol.qs` → objeto `df_sinan`  
**Período:** 2016–2025

---

## Fonte dos dados

| Campo | Valor |
|---|---|
| Sistema | SINAN – Sistema de Informação de Agravos de Notificação |
| Ficha | Violência Doméstica, Sexual e/ou Outras Violências Interpessoais |
| Arquivo local | `dados/sinan_viol.qs` |
| Objeto R | `df_sinan` |

---

## Variáveis derivadas via `mutate()` em `viol_ui.R`

| Coluna derivada | Lógica | Colunas de origem |
|---|---|---|
| `rede_enc_sau` | `rede_sau == "1" \| enc_saude == "1"` | `rede_sau`, `enc_saude` |
| `assit_soc_creas` | `assist_soc == "1" \| enc_creas == "1"` | `assist_soc`, `enc_creas` |
| `atend_enc_mulh` | `atend_mulh == "1" \| enc_mulher == "1"` | `atend_mulh`, `enc_mulher` |
| `cons_enc_tutela` | `cons_tutel == "1" \| enc_tutela == "1"` | `cons_tutel`, `enc_tutela` |
| `mpu_enc_mpu` | `mpu == "1" \| enc_mpu == "1"` | `mpu`, `enc_mpu` |
| `deleg_enc_cria` | `deleg_cria == "1" \| enc_dpca == "1"` | `deleg_cria`, `enc_dpca` |
| `deleg_enc_mulh` | `deleg_mulh == "1" \| enc_deam == "1"` | `deleg_mulh`, `enc_deam` |
| `deleg_enc_deleg` | `deleg == "1" \| enc_deleg == "1"` | `deleg`, `enc_deleg` |
| `infan_enc_juv` | `infan_juv == "1" \| enc_vara == "1"` | `infan_juv`, `enc_vara` |
| `ds_autor_sexo` | decode: `"1"→Masculino`, `"2"→Feminino`, `"3"→Ambos`, else `Ignorado` | `autor_sexo` |
| `les_autop` | decode: `"1"→Sim`, `"2"→Não`, `"9"/NA→Ignorado` | `les_autop` (original) |
| `local_ocor` | decode código 2 dígitos para texto | `local_ocor` (original) |
| `out_vezes` | decode: `"1"→Sim`, `"2"→Não`, `"9"→Ignorado` | `out_vezes` (original) |
| `faixa_etaria_padrao` | `faixa_etaria_func()` sobre `nu_idade_anos` | `nu_idade_anos` |

---

## Filtros

| Input ID | Variável filtrada | Tipo |
|---|---|---|
| `filtro_idade` | `faixa_etaria_padrao` | pickerInput múltiplo |
| `filtro_raca` | `ds_raca` | pickerInput múltiplo |
| `filtro_ano` | `ano` | pickerInput múltiplo |
| `filtro_violencias` | colunas binárias `viol_*` (filter_at/any_vars) | pickerInput múltiplo |
| `les_autop_fil` | `les_autop` | pickerInput múltiplo |

---

## Outputs

### `freq_ano_graf` — plotlyOutput
- **Função:** `ano_graf(df)` → `tab_1(ano)` → linha sobre `n` por `ano`
- **Colunas:** `ano`, `faixa_etaria_padrao`, `ds_raca`, `les_autop`, colunas `viol_*`
- **Filtros aplicados:** todos exceto `filtro_ano`

### `faixa_etaria_graf` — plotlyOutput
- **Função:** `faixa_etaria_graf(df)` → `tab_1(faixa_etaria_padrao)` → barras verticais sobre `%`
- **Colunas:** `faixa_etaria_padrao`, `ds_raca`, `les_autop`, `ano`, colunas `viol_*`
- **Download:** `download_tab_faixa_etaria` → `.xlsx`

### `raca_cor_graf` — plotlyOutput
- **Função:** `raca_cor_graf(df)` → `tab_1(ds_raca)` → barras horizontais sobre `%`
- **Colunas:** `ds_raca`, `faixa_etaria_padrao`, `les_autop`, `ano`, colunas `viol_*`
- **Download:** `download_tab_raca_cor` → `.xlsx`

### `sinan` — dataTableOutput
- **Função:** `vitaltable::tab_cat_sinan(filtered_df, extrato, valor)`
- **Variável de categoria** (`evolution_filter`):

| Opção | Objeto R | Colunas |
|---|---|---|
| `enc` | objeto `enc` do pacote `vitaltable` | `rede_enc_sau`, `assit_soc_creas`, `atend_enc_mulh`, `cons_enc_tutela`, `mpu_enc_mpu`, `deleg_enc_cria`, `deleg_enc_mulh`, `deleg_enc_deleg`, `infan_enc_juv` |
| `proc` | objeto `proc` | colunas de procedimentos |
| `rel` | objeto `rel` | colunas de relacionamento com agressor |
| `viol` | objeto `viol` | `viol_fisic`, `viol_psico`, `viol_sexu`, `viol_tort`, `viol_negli`, `viol_finan`, `viol_infan`, `viol_legal`, `viol_traf`, `viol_outr` |
| `agc` | objeto `agc` | `ag_forca`, `ag_enfor`, `ag_objeto`, `ag_corte`, `ag_quente`, `ag_enven`, `ag_fogo`, `ag_ameaca`, `ag_outros` |
| `defic` | objeto `defic` | `def_trans`, `def_fisica`, `def_mental`, `def_visual`, `def_auditi`, `def_out`, `def_espec` |
| `transt` | objeto `transt` | `tran_ment`, `tran_comp` |

- **Variável de estratificação** (`extrato_sinan_filter`): `ds_raca`, `faixa_etaria_padrao`, `ano`, `out_vezes`, `local_ocor`
- **Download:** `download_tab_sinan` → `.xlsx`

### `sexo_alcool_graf` — plotlyOutput
- **Lógica:** `tab_2(ds_autor_sexo, autor_alco)` + `tab_2(..., pct_row=TRUE)` → merge → barras empilhadas
- **Colunas:** `ds_autor_sexo` (derivada de `autor_sexo`), `autor_alco`

### `tabela_cruzada` — dataTableOutput
- **Função local:** `tabela_2(df, var_row, var_col)` → pivot_wider + adorn_totals
- **Variáveis de linha** (`var1`): `faixa_etaria_padrao`, `ds_raca`, `ano`, `out_vezes`, `local_ocor`
- **Variáveis de coluna** (`var2`): `ds_raca`, `ano`, `out_vezes`
- **Download:** `download_tab2_sinan` → `.xlsx`

---

## Resumo de colunas utilizadas

| Coluna | Origem |
|---|---|
| `ano` | SINAN original |
| `ds_raca` | SINAN original |
| `autor_alco` | SINAN original |
| `viol_fisic` … `viol_outr` | SINAN original (flags 0/1) |
| `ag_forca` … `ag_outros` | SINAN original (flags 0/1) |
| `def_trans` … `def_espec` | SINAN original (flags 0/1) |
| `tran_ment`, `tran_comp` | SINAN original (flags 0/1) |
| `faixa_etaria_padrao` | Derivada via `faixa_etaria_func()` |
| `les_autop` | Derivada (decode de código) |
| `local_ocor` | Derivada (decode de código) |
| `out_vezes` | Derivada (decode de código) |
| `ds_autor_sexo` | Derivada de `autor_sexo` |
| `rede_enc_sau` … `infan_enc_juv` | Derivadas (OR de flags de encaminhamento) |
