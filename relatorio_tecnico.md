## Sobre este documento

Este relatório documenta a origem dos dados, as variáveis utilizadas, os pré-processamentos aplicados e a lógica de cada visualização em cada página do Painel Recife. Destina-se a desenvolvedores, analistas de dados e profissionais responsáveis pela manutenção e evolução do painel.

O painel integra dados de múltiplos sistemas de saúde:

| Sistema | Sigla | O que registra |
|---|---|---|
| Sistema de Informação de Agravos de Notificação | SINAN | Notificações de violência e intoxicação exógena |
| Sistema de Informações Hospitalares | SIH | Internações hospitalares |
| Sistema de Informação sobre Mortalidade | SIM | Óbitos e causas de morte |
| Sistema de Atenção Básica | e-SUS APS | Atendimentos na atenção primária |
| Cadastro Nacional de Estabelecimentos de Saúde | CNES | Unidades de saúde e sua localização |

---

## Arquitetura de dados

Os dados epidemiológicos são carregados como arquivos locais na pasta `dados/` (formatos `.qs` e `.RData`). O banco PostgreSQL é utilizado **exclusivamente para autenticação** (schema `auth`), não armazenando dados do painel.

### Arquivos de dados

| Arquivo | Objeto R | Usado em |
|---|---|---|
| `dados/sinan_viol.qs` | `df_sinan` | Páginas 2, 7, 8 |
| `dados/df_iexo.qs` | `df_iexo` | Página 3 |
| `dados/df_sih.qs` | `df_sih` | Página 4 |
| `dados/df_sim.qs` | `df_sim` | Página 5 |
| `dados/cid_10.csv` | lido em runtime | Páginas 4, 5 |
| `dados/linkage_compilado_sem_banco.RData` | `linkage_compilado` | Página 6 |
| `dados/base_linkage_feminino.RData` | `base_linkage` | Páginas 6, 7 |
| `dados/icd_map_ufmg.Rdata` | `icd_map` | Página 6 |
| `dados/linha_vida_esus4.qs` | `df_linha_vida` | Páginas 7, 1 |
| `dados/pontos_viol_real.qs` | `pontos_viol` | Página 1 |
| `dados/bairros.geojson` | `mapa` (sf) | Página 1 |
| `dados/cnes.RData` | `cnes` | Página 1 |
| `dados/cnes_join.RData` | `cnes_join` | Página 1 |
| `dados/dados_modelo_bairro.qs` | `modelo_bairro` | Página 8 |
| `dados/dados_modelo_ubs.qs` | `modelo_ubs` | Página 8 |

### Funções compartilhadas

| Função | Arquivo | O que faz |
|---|---|---|
| `faixa_etaria_func()` | `R/funcoes/faixa_etaria_func.R` | Deriva `faixa_etaria_padrao` a partir de `nu_idade_anos` |
| `ano_graf()` | `R/graficos/ano_graf.R` | Gráfico de linha por `ano` usando `tab_1()` |
| `faixa_etaria_graf()` | `R/graficos/faixa_etaria_graf.R` | Barras verticais de `%` por `faixa_etaria_padrao` |
| `raca_cor_graf()` | `R/graficos/raca_cor_graf.R` | Barras horizontais de `%` por `ds_raca` |
| `vitaltable::tab_1()` | pacote externo | Frequência + proporção de uma variável |
| `vitaltable::tab_2()` | pacote externo | Tabela cruzada entre duas variáveis |
| `vitaltable::tab_cat_sinan()` | pacote externo | Tabela de categorias SINAN estratificada |

---

## Índice

1. Mapa da Violência
2. SINAN Violência
3. SINAN Intoxicação Exógena
4. Hospitalizações
5. Mortalidade
6. Análise do Linkage
7. Linha da Vida
8. Subnotificações

---

&nbsp;

---

# [TÉCNICO] Página 1 - Mapa da Violência

## O que é essa página?

Apresenta um **mapa interativo de Recife** com a localização geográfica das mulheres identificadas nos bancos de dados, sobreposta aos bairros da cidade e às unidades de saúde (CNES). Permite visualizar a distribuição espacial dos casos de violência e identificar concentrações por região.

---

## De onde vêm os dados?

| Dado | O que contém |
|---|---|
| **Pontos das mulheres** | Coordenadas geográficas das mulheres, com informações demográficas e trajetória nos sistemas de saúde. Originados do processo de linkage, enriquecidos com dados da linha da vida |
| **Bairros de Recife** | Polígonos (shapefile) dos bairros da cidade |
| **Unidades de saúde** | Localização e nome das unidades do CNES |

---

## Filtros disponíveis

Os filtros ficam ocultos por padrão e podem ser abertos pelo botão **Filtros** no canto superior direito.

| Filtro | O que faz |
|---|---|
| **ID Pessoa** | Destaca no mapa uma mulher específica pelo seu identificador |
| **Idade** | Restringe os pontos a um intervalo de idade (slider) |
| **Raça/cor** | Mostra apenas pontos de uma determinada raça/cor |
| **Ano** | Restringe os pontos ao intervalo de anos selecionado (2016–2025) |

---

## Opções de visualização

| Opção | O que faz |
|---|---|
| **Estilo do mapa** | Altera o fundo cartográfico (Padrão ou Carto Positron) |
| **Intensidade do preenchimento** | Opacidade do preenchimento dos bairros |
| **Intensidade da borda** | Opacidade das bordas dos bairros |
| **Cor do shapefile** | Cor dos polígonos dos bairros |
| **Cor padrão dos pontos** | Cor dos marcadores das mulheres |
| **Cor do destaque** | Cor usada para destacar uma mulher específica pelo ID |
| **Ativar/Desativar Heatmap** | Alterna entre pontos individuais e mapa de calor (concentração) |

---

## Interatividade

- **Clicar em um marcador de unidade de saúde:** exibe o nome da unidade (CNES)
- **Clicar em um ponto de mulher:** exibe idade, raça/cor e resumo da trajetória nos sistemas de saúde
- **Clicar em uma unidade de saúde:** filtra e mostra apenas os pontos das mulheres atendidas naquela unidade; duplo clique no mapa desfaz a seleção

---

## Detalhamento técnico

**Tab:** `mapa_viol`  
**Módulo:** `R/mapa_ui.R`  
**Arquivos:**
- `dados/pontos_viol_real.qs` → `pontos_viol`
- `dados/bairros.geojson` → `mapa` (sf, lido em módulo)
- `dados/cnes.RData` → `cnes`
- `dados/cnes_join.RData` → `cnes_join`

---

## Fontes dos dados

| Objeto | Arquivo | Conteúdo |
|---|---|---|
| `pontos_viol` | `dados/pontos_viol_real.qs` | Mulheres identificadas via **linkage probabilístico** (SINAN Violência + SIH + SIM + e-SUS APS). Contém coordenadas geográficas, dados demográficos e trajetória nos sistemas de saúde. As mulheres são incluídas porque possuem ao menos uma notificação de violência no SINAN; a coordenada geográfica é obtida pelo endereço mais recente registrado em qualquer sistema. |
| `mapa` | `dados/bairros.geojson` | Polígonos dos bairros (sf object) |
| `cnes` | `dados/cnes.RData` | `cd_cnes_unid_not`, `NO_FANTASIA`, `latitude_cnes`, `longitude_cnes` — localização das unidades de saúde |
| `cnes_join` | `dados/cnes_join.RData` | Join `id_unico` para enriquecer `df_linha_vida` |

---

## Pré-processamento

```r
pontos_viol <- pontos_viol |>
  mutate(Latitude = as.numeric(Latitude), Longitude = as.numeric(Longitude),
         ano_geo = as.integer(ano_geo))

df_linha_vida2 <- df_linha_vida |> left_join(cnes_join, by = "id_unico")
pontos_viol    <- pontos_viol  |> left_join(df_linha_vida2, by = "id_unico")

mapa <- st_read("dados/bairros.geojson")
```

---

## Filtros

| Input ID | Variável | Tipo |
|---|---|---|
| `filtro_id_pessoa` | `id_pessoa` (highlight) | numericInput |
| `filtro_idade` | `nu_idade_anos` (range) | sliderInput |
| `filtro_raca` | `ds_raca` | selectInput |
| `filtro_ano` | `ano_geo` (range 2016–2025) | sliderInput |

**Reactive:** `filtered_pontos()` — filtra e adiciona coluna `highlight`  
**Filtro por CNES:** `selected_cnes()` via clique em marcador; duplo clique no mapa limpa

---

## Output: `mapa` — leafletOutput

| Camada | Dados | Detalhes |
|---|---|---|
| Tiles | — | `CartoDB.Positron` ou `addTiles()` |
| Polígonos | `mapa` (sf) | Cor/opacidade configuráveis |
| Marcadores CNES | `cnes_data` | Ícone `www/img/hospital.png`; popup: `NO_FANTASIA`; layerId: `cd_cnes_unid_not` |
| Pontos (modo normal) | `filtered_pontos()` | `addCircleMarkers`; cor por `highlight`; popup: idade, raça, `texto_final` |
| Heatmap (modo ativo) | `filtered_pontos()` | `addWebGLHeatmap` / `addHeatmap` |

Atualização incremental via `leafletProxy` (limpa/redesenha grupos `markers`, `heatmap`, `cnes`).

---

## Colunas utilizadas

| Coluna | Objeto | Origem |
|---|---|---|
| `Latitude`, `Longitude` | `pontos_viol` | Coordenadas do endereço mais recente no linkage |
| `id_pessoa`, `nu_idade_anos`, `ds_raca` | `pontos_viol` | Dados da mulher |
| `ds_raca_padronizada`, `texto_final` | `pontos_viol` (via join com `df_linha_vida2`) | Dados do linkage |
| `ano_geo` | `pontos_viol` | Ano do evento georreferenciado |
| `cd_cnes_unid_not` | `pontos_viol` | CNES da unidade notificadora |
| `NO_FANTASIA`, `latitude_cnes`, `longitude_cnes` | `cnes` | Dados da unidade de saúde (CNES) |
| `geometry` | `mapa` (sf) | Polígonos dos bairros |

---

&nbsp;

---

# [TÉCNICO] Página 2 - SINAN Violência

## O que é essa página?

Apresenta análises sobre as **notificações de violência doméstica, sexual e outras violências interpessoais** registradas em Recife. Os dados cobrem o período de **2016 a 2025**.

---

## De onde vêm os dados?

**Sistema de origem:** SINAN - Sistema de Informação de Agravos de Notificação  
**Ficha utilizada:** Violência Doméstica, Sexual e/ou Outras Violências Interpessoais

O SINAN é o sistema nacional onde profissionais de saúde registram obrigatoriamente casos de violência atendidos nas unidades de saúde. Cada linha do dado representa uma notificação individual.

---

## Filtros disponíveis

| Filtro | O que faz |
|---|---|
| **Faixa etária** | Restringe os dados a uma ou mais faixas de idade da vítima |
| **Raça/cor** | Restringe os dados pela raça/cor declarada da vítima |
| **Ano** | Seleciona um ou mais anos de notificação (2016 a 2025) |
| **Tipo de violência** | Filtra por tipo específico (física, psicológica, sexual, tortura, negligência, financeira, trabalho infantil, intervenção legal, tráfico de humanos, outras) |
| **Lesão autoprovocada** | Indica se a violência foi autoprovocada (Sim / Não / Ignorado) |

---

## Visualizações

### 1. Frequência de notificação por ano
**O que mostra:** Evolução do número de notificações ao longo dos anos.

### 2. Distribuição por faixa etária
**O que mostra:** Proporção de notificações em cada faixa de idade.

### 3. Distribuição por raça/cor
**O que mostra:** Proporção de notificações por raça/cor declarada da vítima.

### 4. Tabela de informações do SINAN
**O que mostra:** Tabela configurável que cruza tipos de informação (encaminhamentos, procedimentos, relação com agressor, tipo de violência, meio de agressão, deficiências, transtornos) com estratificações (raça/cor, faixa etária, ano, etc.).

### 5. Sexo do agressor por suspeita de uso de álcool
**O que mostra:** Barras empilhadas cruzando sexo do agressor com suspeita de uso de álcool.

### 6. Tabela cruzada configurável
**O que mostra:** Tabela de dupla entrada que o usuário monta livremente cruzando duas variáveis.

---

## Detalhamento técnico

**Tab:** `tela_sinan`  
**Módulos:** `R/viol_ui.R`, `R/viol_server.R`  
**Arquivo de dados:** `dados/sinan_viol.qs` → objeto `df_sinan`  
**Período:** 2016–2025

---

## Fonte dos dados

| Campo | Valor |
|---|---|
| Sistema | SINAN - Sistema de Informação de Agravos de Notificação |
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

## Resumo de colunas

| Coluna | Origem |
|---|---|
| `ano`, `ds_raca`, `autor_alco` | SINAN original |
| `viol_fisic` … `viol_outr` | SINAN original (flags 0/1) |
| `ag_forca` … `ag_outros` | SINAN original (flags 0/1) |
| `def_trans` … `def_espec` | SINAN original (flags 0/1) |
| `tran_ment`, `tran_comp` | SINAN original (flags 0/1) |
| `faixa_etaria_padrao` | Derivada via `faixa_etaria_func()` |
| `les_autop`, `local_ocor`, `out_vezes`, `ds_autor_sexo` | Derivadas (decode de código) |
| `rede_enc_sau` … `infan_enc_juv` | Derivadas (OR de flags de encaminhamento) |

---

&nbsp;

---

# [TÉCNICO] Página 3 - SINAN Intoxicação Exógena

## O que é essa página?

Apresenta análises sobre as **notificações de intoxicação exógena** registradas em Recife — casos em que uma pessoa foi exposta a substâncias tóxicas como medicamentos, agrotóxicos, drogas ou produtos químicos. Os dados cobrem o período de **2016 a 2025**.

---

## De onde vêm os dados?

**Sistema de origem:** SINAN - Sistema de Informação de Agravos de Notificação  
**Ficha utilizada:** Intoxicação Exógena

O SINAN é o sistema nacional onde profissionais de saúde registram obrigatoriamente casos de intoxicação atendidos nas unidades de saúde. Cada linha do dado representa uma notificação individual.

---

## Filtros disponíveis

| Filtro | O que faz |
|---|---|
| **Faixa etária** | Restringe os dados a uma ou mais faixas de idade da vítima |
| **Raça/cor** | Restringe os dados pela raça/cor declarada da vítima |
| **Ano** | Seleciona um ou mais anos de notificação (2016 a 2025) |
| **Circunstância** | Filtra pelo motivo da intoxicação (tentativa de suicídio, acidente, uso habitual, violência, etc.) |

---

## Visualizações

### 1. Frequência de notificação por ano
**O que mostra:** Evolução do número de notificações de intoxicação ao longo dos anos.

### 2. Distribuição por faixa etária
**O que mostra:** Proporção de notificações em cada faixa de idade.

### 3. Distribuição por raça/cor
**O que mostra:** Proporção de notificações por raça/cor declarada da vítima.

### 4. Proporção por circunstância
**O que mostra:** Distribuição das notificações segundo o motivo da intoxicação.

### 5. Proporção por agente intoxicante
**O que mostra:** Distribuição segundo a substância que causou a intoxicação.

### 6. Tipo de atendimento por hospitalização
**O que mostra:** Barras empilhadas cruzando tipo de atendimento com se o paciente foi hospitalizado.

---

## Detalhamento técnico

**Tab:** `tela_iexo`  
**Módulos:** `R/iexo_ui.R`, `R/iexo_server.R`  
**Arquivo de dados:** `dados/df_iexo.qs` → objeto `df_iexo`  
**Período:** 2016–2025

---

## Fonte dos dados

| Campo | Valor |
|---|---|
| Sistema | SINAN - Sistema de Informação de Agravos de Notificação |
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
- **Função:** `ano_graf(df)` → linha sobre `n`
- **Obs.:** filtro de `ano` **não** é aplicado neste gráfico

### `faixa_etaria_graf` — plotlyOutput
- **Função:** `faixa_etaria_graf(df)` — Download: `download_tab_faixa_etaria` → `.xlsx`

### `raca_cor_graf` — plotlyOutput
- **Função:** `raca_cor_graf(df)` — Download: `download_tab_raca_cor` → `.xlsx`

### `circunstancia_graf` — plotlyOutput
- **Lógica:** `tab_1(ds_circunstan)` → reorder por `n` → barras horizontais sobre `%`
- **Coluna:** `ds_circunstan` — Download: `download_tab_circunstancia` → `.xlsx`

### `ag_intox_graf` — plotlyOutput
- **Lógica:** `tab_1(ds_agente_tox)` → reorder por `n` → barras horizontais sobre `%`
- **Coluna:** `ds_agente_tox` — Download: `download_tab_ag_intox` → `.xlsx`

### `atend_hospit_graf` — plotlyOutput
- **Lógica:** `tab_2(ds_tpatend, ds_hospital)` + `tab_2(..., pct_row=TRUE)` → merge → barras empilhadas
- **Colunas:** `ds_tpatend`, `ds_hospital` (Sim/Não/Ignorado)
- **Categorias de `ds_tpatend`:** `Ambulatorial`, `Domiciliar`, `Hospitalar`, `Ignorado`, `Nenhum`
- **Download:** `download_atend_hospit_graf` → `.xlsx`

---

## Resumo de colunas

| Coluna | Origem |
|---|---|
| `ano`, `ds_raca`, `ds_circunstan`, `ds_agente_tox`, `ds_tpatend`, `ds_hospital` | SINAN original |
| `faixa_etaria_padrao` | Derivada via `faixa_etaria_func()` |

---

&nbsp;

---

# [TÉCNICO] Página 4 - Hospitalizações

## O que é essa página?

Apresenta análises sobre as **internações hospitalares por causas externas** registradas em Recife, com foco nos capítulos XIX e XX da CID-10 (lesões, envenenamentos e causas externas de morbidade). Os dados cobrem o período de **2016 a 2025**.

---

## De onde vêm os dados?

**Sistema de origem:** SIH - Sistema de Informações Hospitalares do SUS  
**Tabela auxiliar:** CID-10 — usada para traduzir os códigos de diagnóstico em descrições legíveis

O SIH registra todas as internações financiadas pelo SUS. Cada linha do dado representa uma autorização de internação hospitalar (AIH).

---

## Filtros disponíveis

| Filtro | O que faz |
|---|---|
| **Faixa etária** | Restringe os dados a uma ou mais faixas de idade do paciente |
| **Raça/cor** | Restringe os dados pela raça/cor declarada |
| **Ano** | Seleciona um ou mais anos de internação (2016 a 2025) |

---

## Visualizações

### 1. Frequência de internações por ano
**O que mostra:** Evolução do número de internações por causas externas ao longo dos anos.

### 2. Distribuição por faixa etária
**O que mostra:** Proporção de internações em cada faixa de idade.

### 3. Distribuição por raça/cor
**O que mostra:** Proporção de internações por raça/cor declarada do paciente.

### 4. Proporção de internações por capítulo da CID-10
**O que mostra:** Distribuição das internações pelas categorias de causa (fraturas, queimaduras, intoxicações, acidentes de transporte, agressões, etc.).

---

## Detalhamento técnico

**Tab:** `tela_sih`  
**Módulos:** `R/sih_ui.R`, `R/sih_server.R`  
**Arquivo de dados:** `dados/df_sih.qs` → objeto `df_sih`  
**Tabela auxiliar:** `dados/cid_10.csv` (lida em runtime no `graf_obito`)  
**Período:** 2016–2025

---

## Fonte dos dados

| Campo | Valor |
|---|---|
| Sistema | SIH - Sistema de Informações Hospitalares do SUS |
| Arquivo local | `dados/df_sih.qs` |
| Objeto R | `df_sih` |
| Tabela auxiliar | `dados/cid_10.csv` (colunas: `SUBCAT`, `CAPITULO`, `DESCRICAO_CAT`) |

---

## Pré-processamento

- `faixa_etaria_func()` aplicada sobre `df_sih`

---

## Filtros

| Input ID | Variável filtrada |
|---|---|
| `filtro_idade` | `faixa_etaria_padrao` |
| `filtro_raca` | `ds_raca` |
| `filtro_ano` | `ano` |

---

## Outputs

### `freq_ano_graf` — plotlyOutput
- `ano_graf(df)` sobre `ano`, `faixa_etaria_padrao`, `ds_raca`

### `faixa_etaria_graf` — plotlyOutput
- `faixa_etaria_graf(df)` — Download: `.xlsx`

### `raca_cor_graf` — plotlyOutput
- `raca_cor_graf(df)` — Download: `.xlsx`

### `graf_obito` — plotlyOutput
- **Lógica:** `read.csv2('dados/cid_10.csv')` → `left_join(df_sih, cid_10, by = c("cd_diag_pri" = "SUBCAT"))` → filtra capítulos XIX e XX → `tab_1(DESCRICAO_CAT)` → barras horizontais
- **Filtro aplicado:** somente `filtro_ano`
- **Colunas:** `cd_diag_pri`, `ano` + `CAPITULO`, `DESCRICAO_CAT` (via join)

---

## Resumo de colunas

| Coluna | Origem |
|---|---|
| `ano`, `ds_raca`, `cd_diag_pri` | SIH original |
| `faixa_etaria_padrao` | Derivada via `faixa_etaria_func()` |
| `CAPITULO`, `DESCRICAO_CAT` | Join com `dados/cid_10.csv` via `cd_diag_pri = SUBCAT` |

---

&nbsp;

---

# [TÉCNICO] Página 5 - Mortalidade

## O que é essa página?

Apresenta análises sobre os **óbitos por causas externas** registrados em Recife, com foco nos capítulos XIX e XX da CID-10 (lesões, envenenamentos, agressões, acidentes e outras causas externas de morte). Os dados cobrem o período de **2016 a 2025**.

---

## De onde vêm os dados?

**Sistema de origem:** SIM - Sistema de Informação sobre Mortalidade  
**Tabela auxiliar:** CID-10 — usada para traduzir os códigos de causa do óbito em descrições legíveis

O SIM registra todos os óbitos ocorridos no Brasil com base nas Declarações de Óbito. Cada linha do dado representa um óbito individual.

---

## Filtros disponíveis

| Filtro | O que faz |
|---|---|
| **Faixa etária** | Restringe os dados a uma ou mais faixas de idade do falecido |
| **Raça/cor** | Restringe os dados pela raça/cor declarada |
| **Ano** | Seleciona um ou mais anos de óbito (2016 a 2025) |

---

## Visualizações

### 1. Frequência de óbitos por ano
**O que mostra:** Evolução do número de óbitos por causas externas ao longo dos anos.

### 2. Distribuição por faixa etária
**O que mostra:** Proporção de óbitos em cada faixa de idade.

### 3. Distribuição por raça/cor
**O que mostra:** Proporção de óbitos por raça/cor declarada.

### 4. Proporção de óbitos por causas externas — CID-10
**O que mostra:** Distribuição dos óbitos pelas categorias de causa (homicídios, suicídios, acidentes de transporte, afogamentos, quedas, etc.).

---

## Detalhamento técnico

**Tab:** `tela_sim`  
**Módulos:** `R/sim_ui.R`, `R/sim_server.R`  
**Arquivo de dados:** `dados/df_sim.qs` → objeto `df_sim`  
**Tabela auxiliar:** `dados/cid_10.csv` (lida em runtime)  
**Período:** 2016–2025

---

## Fonte dos dados

| Campo | Valor |
|---|---|
| Sistema | SIM - Sistema de Informação sobre Mortalidade |
| Arquivo local | `dados/df_sim.qs` |
| Objeto R | `df_sim` |
| Tabela auxiliar | `dados/cid_10.csv` (colunas: `SUBCAT`, `CAPITULO`, `DESCRICAO_CAT`) |

---

## Pré-processamento

- `faixa_etaria_func()` aplicada sobre `df_sim`

---

## Filtros

| Input ID | Variável filtrada |
|---|---|
| `filtro_idade` | `faixa_etaria_padrao` |
| `filtro_raca` | `ds_raca` |
| `filtro_ano` | `ano` |

---

## Outputs

### `freq_ano_graf` — plotlyOutput
- `ano_graf(df)` — filtro de `ano` **não** aplicado neste gráfico

### `faixa_etaria_graf` — plotlyOutput
- `faixa_etaria_graf(df)` — Download: `.xlsx`

### `raca_cor_graf` — plotlyOutput
- `raca_cor_graf(df)` — Download: `.xlsx`

### `graf_obito` — plotlyOutput
- **Lógica:** `read.csv2('dados/cid_10.csv')` → `left_join(df_sim, cid_10, by = c("cd_causabas" = "SUBCAT"))` → filtra capítulos XIX e XX → `tab_1(DESCRICAO_CAT)` → barras horizontais
- **Filtro aplicado:** somente `filtro_ano`
- **Colunas:** `cd_causabas`, `ano` + `CAPITULO`, `DESCRICAO_CAT` (via join)

---

## Resumo de colunas

| Coluna | Origem |
|---|---|
| `ano`, `ds_raca`, `cd_causabas` | SIM original |
| `faixa_etaria_padrao` | Derivada via `faixa_etaria_func()` |
| `CAPITULO`, `DESCRICAO_CAT` | Join com `dados/cid_10.csv` via `cd_causabas = SUBCAT` |

---

&nbsp;

---

# [TÉCNICO] Página 6 - Análise do Linkage

## O que é essa página?

Apresenta resultados do **linkage probabilístico** — um processo que cruza os registros de diferentes sistemas de saúde para identificar as mesmas mulheres em múltiplas bases de dados. Isso permite comparar o perfil e os desfechos (óbitos, internações) de mulheres que tiveram notificação de violência com aquelas que não tiveram.

Os dados cobrem o período de **2019 a 2025** para os gráficos comparativos, e **2016–2025** para os indicadores gerais.

---

## De onde vêm os dados?

Esta página integra informações de **quatro sistemas** cruzados via linkage:

| Sistema | O que contém |
|---|---|
| **SINAN Violências** | Notificações de violência doméstica, sexual e interpessoal |
| **SINAN Intoxicação Exógena** | Notificações de intoxicação |
| **SIM** (Mortalidade) | Óbitos e causas de morte |
| **SIH** (Hospitalizações) | Internações hospitalares e causas |

**Dicionário de causas:** mapeamento de códigos CID-10 para descrições resumidas, elaborado pela UFMG.

---

## Filtros disponíveis

| Filtro | O que faz |
|---|---|
| **Faixa etária** | Restringe os dados a uma ou mais faixas de idade |
| **Raça/cor** | Restringe os dados pela raça/cor declarada |
| **Registro no ESUS APS** | Filtra se a mulher tem ou não registro na atenção básica (e-SUS) |

---

## Visualizações

### Indicadores (cards)

| Indicador | O que mostra |
|---|---|
| **Total de registros processados** | Número total de registros cruzados no linkage (2016–2025) |
| **Total de mulheres no período** | Número de mulheres únicas identificadas no cruzamento |
| **Mulheres com notificação de violência** | Quantas tiveram ao menos um registro de violência no SINAN |
| **Óbitos por agressão de mulheres notificadas** | Quantas mulheres com notificação de violência foram a óbito por causas externas |

### 1. Distribuição por faixa etária — plotlyOutput
**O que mostra:** Comparação da distribuição etária entre mulheres com e sem notificação de violência.

### 2. Distribuição por raça/cor — plotlyOutput
**O que mostra:** Comparação da distribuição por raça/cor entre mulheres com e sem notificação de violência.

### 3. Comparação das causas de óbito (gráfico de bolhas)
**O que mostra:** Proporções de cada causa de óbito entre três grupos. Período: 2019–2025.

### 4. Comparação das causas de internação (gráfico de bolhas)
**O que mostra:** Mesmo formato, mas para internações hospitalares. Período: 2019–2025.

### 5. Mulheres no SINAN Violências vs. SINAN Intoxicação Exógena
**O que mostra:** Barras com o número de mulheres que aparecem exclusivamente em cada sistema ou em ambos.

---

## Detalhamento técnico

**Tab:** `analise_linkage`  
**Módulo:** `R/linkage.R`  
**Arquivos:**
- `dados/linkage_compilado_sem_banco.RData` → `linkage_compilado`
- `dados/base_linkage_feminino.RData` → `base_linkage`
- `dados/icd_map_ufmg.Rdata` → `icd_map`

**Período:** KPIs/perfil: 2016–2025 · Gráficos comparativos: 2019–2025

---

## Fontes dos dados

| Objeto | Arquivo | Conteúdo |
|---|---|---|
| `linkage_compilado` | `dados/linkage_compilado_sem_banco.RData` | Dados agregados por combinação de flags |
| `base_linkage` | `dados/base_linkage_feminino.RData` | Registros individuais com banco + flags de linkage |
| `icd_map` | `dados/icd_map_ufmg.Rdata` | `icd_code_4 → CIDBR_RESUMIDO_EXTERNAS` (UFMG) |

---

## Pré-processamento

```r
linkage_kpi <- linkage_compilado |>
  select(rotulo_viol_interpessoal, fl_esus, raca_cor,
         faixa_etaria_padrao, fl_ob_not_externas, registros, n_pessoas)

df_obitos      <- base_linkage |> filter(banco == "SIM")
df_internacoes <- base_linkage |> filter(banco == "SIH")

# Renomeia icd_code_4 → cd_causabas, CIDBR_RESUMIDO_EXTERNAS → causa_resumida
df_obitos      <- df_obitos      |> left_join(icd_map, by = "cd_causabas")
df_internacoes <- df_internacoes |> left_join(icd_map, by = "cd_causabas")
```

---

## Filtros (sobre `linkage_kpi` via `kpi_filtrada()`)

| Input ID | Variável |
|---|---|
| `filtro_idade` | `faixa_etaria_padrao` |
| `filtro_raca` | `raca_cor` |
| `filtro_esus` | `fl_esus` (0/1) |

---

## Outputs

### KPI cards (`num_registros`, `num_mulheres`, `mulheres_notificadas`, `obitos_agressao_notif`)
- `sum(registros)`, `sum(n_pessoas)`, filtros por `rotulo_viol_interpessoal == 1` e `fl_ob_not_externas == 1`

### `faixa_etaria_graf` / `raca_cor_graf` — plotlyOutput
- `faixa_etaria_graf_npessoas()` / `raca_cor_graf_npessoas()` — agrupam por `(faixa_etaria_padrao / raca_cor, rotulo_viol_interpessoal)`, somam `n_pessoas`, calculam `pct` dentro de cada grupo
- Downloads: `.xlsx`

### `causas_obito_linkage` — plotlyOutput
- **Base:** `df_obitos` (banco == "SIM")
- **3 grupos:** `FL_SINAN_VIOL==1`, `FL_SINAN_IEXO==1`, ambos != 1
- **Lógica:** `tab_1(causa_resumida)` em cada grupo → bind_rows → bubble chart (size = `%`)
- Download: `download_bolha` → `.xlsx`

### `causas_internacao_linkage` — plotlyOutput
- **Base:** `df_internacoes` (banco == "SIH") — mesma lógica
- Download: `download_bolha_internacao` → `.xlsx`

### `graf_viol_iexo` — plotlyOutput
- **Base:** pré-computada (`so_viol`, `so_iexo`, `ambos` — contagem de `id_pessoa` únicos)
- **Não reage aos filtros da página**
- Download: `download_viol_iexo` → `.xlsx`

---

## Resumo de colunas

| Coluna | Objeto | Descrição |
|---|---|---|
| `rotulo_viol_interpessoal` | `linkage_compilado` | Flag: tem notificação de violência |
| `fl_esus`, `fl_ob_not_externas` | `linkage_compilado` | Flags de e-SUS e óbito por causas externas |
| `raca_cor`, `faixa_etaria_padrao` | `linkage_compilado` | Dados demográficos agregados |
| `registros`, `n_pessoas` | `linkage_compilado` | Contagens de registros e mulheres únicas |
| `banco`, `FL_SINAN_VIOL`, `FL_SINAN_IEXO` | `base_linkage` | Sistema de origem e flags de linkage |
| `cd_causabas` | `base_linkage` | Código CID-10 da causa |
| `causa_resumida` | `icd_map` (join) | Descrição resumida UFMG |
| `id_pessoa` | `base_linkage` | Identificador único da mulher |

---

&nbsp;

---

# [TÉCNICO] Página 7 - Linha da Vida

## O que é essa página?

Permite visualizar a **trajetória individual de cada mulher** ao longo do tempo, mostrando em que sistemas de saúde ela apareceu e quando. Cada linha no gráfico representa uma mulher; cada ponto representa um evento registrado (uma notificação de violência, uma internação, um óbito, um atendimento na atenção básica, etc.).

A página resulta do processo de **linkage** — cruzamento de múltiplos bancos de dados para identificar a mesma pessoa em sistemas diferentes.

---

## De onde vêm os dados?

Esta página integra registros de **cinco sistemas** cruzados via linkage:

| Sistema | Símbolo no gráfico | O que representa |
|---|---|---|
| **SINAN Violências** | ✕ vermelho | Notificação de violência doméstica ou interpessoal |
| **SIH** (Hospitalizações) | ▲ amarelo | Internação hospitalar |
| **SIM** (Mortalidade) | ■ azul escuro | Óbito |
| **SINAN Intox. Exógena** | ◆ azul claro | Notificação de intoxicação |
| **e-SUS APS** | ● roxo | Atendimento na atenção básica |

A data usada no eixo do tempo é: a data do óbito (para o SIM) ou a data do registro do evento (para os demais sistemas).

---

## Filtros disponíveis

| Filtro | O que faz |
|---|---|
| **Último bairro de residência** | Mostra apenas mulheres cujo último endereço registrado é no(s) bairro(s) selecionado(s) |
| **Raça/cor** | Restringe por raça/cor declarada |
| **Faixa etária** | Restringe por faixa de idade |
| **Banco de dados** | Mostra mulheres que aparecem em determinado sistema |
| **Tipo de violência** | Filtra mulheres com notificação de um tipo específico de violência |
| **Violência autoprovocada** | Filtra se a violência foi autoprovocada |
| **Óbitos** | Filtra se a mulher foi a óbito |
| **Nº de notificações (SINAN Violências)** | Filtra pelo número de vezes que a mulher foi notificada no SINAN |

Os filtros só são aplicados ao clicar no botão **Filtrar**.

---

## Visualizações

### Indicadores de resumo
- Número de mulheres únicas
- Total de registros de violência (SINAN)
- Maior número de notificações de uma mesma mulher
- Média e mediana de notificações por mulher

### Gráfico de linha da vida
Cada linha horizontal é uma mulher. Os pontos representam eventos registrados, com cores e formas diferentes por sistema. O eixo X é o tempo (ano do evento). Clique em um ponto para ver detalhes no painel lateral.

### Painel de detalhes (lateral)
Exibe perfil demográfico e resumo da trajetória da mulher selecionada.

---

## Detalhamento técnico

**Tab:** `linhavida`  
**Módulo:** `R/linha_vida.R`  
**Arquivo de dados:** `dados/linha_vida_esus4.qs` → objeto `df_linha_vida`

---

## Fonte dos dados

| Campo | Valor |
|---|---|
| Arquivo local | `dados/linha_vida_esus4.qs` |
| Objeto R | `df_linha_vida` |
| Sistemas integrados | SINAN_VIOL, SIM, SIH, SINAN_IEXO, ESUS_APS |

---

## Pré-processamento

```r
# dt_registro → Date
# nome_ultimo_bairro NA → "Sem informação"
# Por mulher (group_by id_pessoa):
#   fl_esus_aps: any(fl_esus_aps == 1)
#   so_sinan:    all(banco == "SINAN_VIOL")
#   so_esus_aps: all(banco == "ESUS_APS")
#   idade_minima: min(nu_idade_anos)
# faixa_etaria_func() sobre idade_minima
# dt_comum = coalesce(dt_registro, dt_evento_inicio, dt_evento_fim)
```

---

## Filtros (aplicados via `btn_filtrar` → `filtros_aplicados`)

| Input ID | Variável / lógica |
|---|---|
| `filtro_bairro` | `nome_ultimo_bairro` |
| `filtro_raca` | `ds_raca_padronizada` |
| `filtro_idade` | `faixa_etaria_padrao` |
| `filtro_banco` | flags `fl_*` via `filtrar_bancos()`; `EXCLUSIVO_SINAN_VIOL` → `so_sinan==1`; `EXCLUSIVO_ESUS_APS` → `so_esus_aps==1` |
| `filtro_violencias2` | colunas binárias `fl_viol_*` (filter_at/any_vars) |
| `filtro_autoprovocada` | `fl_les_autop` (0/1) |
| `filtro_obitos` | `fl_sim` (0/1) |
| `filtro_n_notif` | contagem de `SINAN_VIOL` por `id_pessoa` |

---

## Outputs

### `linha_vida_geral_` — plotlyOutput
- Eixo X: `dt_comum`; Eixo Y: `par_reduzido_1 = as.numeric(factor(id_pareamento)) * 20`
- Cor/forma por `banco`; registra `plotly_click` e `plotly_doubleclick` (source `"A"`)

### `selected_point_info` — uiOutput
- Exibe `ds_raca_padronizada`, `nu_idade_anos`, `texto_final` da mulher selecionada

### `resumo_linhavida` — uiOutput
- `n_distinct(id_pessoa)`, `nrow(SINAN_VIOL)`, `max/mean/median(n_notif por mulher)`

### Download `btn_download`
- `distinct(id_pessoa, texto_final)` → `.xlsx` via `openxlsx`

---

## Colunas principais

| Coluna | Origem |
|---|---|
| `id_pessoa`, `id_pareamento` | Linkage |
| `banco` | Sistema de origem |
| `dt_registro`, `dt_evento_inicio`, `dt_evento_fim` | Datas originais por sistema |
| `dt_comum` | Derivada: `coalesce(...)` |
| `ds_raca_padronizada`, `nu_idade_anos`, `faixa_etaria_padrao` | Demográficos |
| `nome_ultimo_bairro` | Endereço (NA → "Sem informação") |
| `fl_sinan_viol`, `fl_sim`, `fl_sih`, `fl_sinan_iexo`, `fl_esus_aps` | Flags de presença |
| `so_sinan`, `so_esus_aps` | Flags de exclusividade (derivadas) |
| `fl_les_autop`, `fl_viol_*` | Flags de tipo de violência |
| `texto_final` | Resumo textual da trajetória (HTML) |

---

&nbsp;

---

# [TÉCNICO] Página 8 - Subnotificações

## O que é essa página?

Apresenta uma estimativa dos **casos de violência prováveis que não foram notificados** no SINAN. A análise parte do princípio de que mulheres que frequentam unidades de atenção básica (UBS) e constam no e-SUS APS, mas não possuem notificação de violência no SINAN, podem representar casos subnotificados.

A página exibe dois níveis de análise: por **bairro de residência** e por **unidade de saúde (UBS)**.

---

## De onde vêm os dados?

Esta página integra informações de dois sistemas:

| Sistema | O que contribui |
|---|---|
| **e-SUS APS** | Número de mulheres usuárias da atenção básica por bairro/UBS |
| **SINAN Violências** | Número de notificações de violência registradas por bairro/UBS |

A diferença entre o esperado (com base no volume de usuárias do e-SUS) e o observado (notificações no SINAN) gera a estimativa de subnotificação.

---

## Filtros disponíveis

| Filtro | O que faz |
|---|---|
| **Ano** | Seleciona o(s) ano(s) de referência da análise |
| **Bairro** | Filtra por bairro de residência |
| **UBS** | Filtra por unidade de saúde (depende do bairro selecionado) |

---

## Visualizações

### 1. Tabela — Subnotificação provável por bairro de residência
Colunas: Bairro, Ano, Usuárias da atenção básica, Notificações no SINAN, Casos subnotificados, Casos prováveis, População feminina, Taxa casos prováveis (por 10 mil hab.).

### 2. Tabela — Subnotificação provável por UBS
Mesmas colunas, acrescentando código CNES e nome da unidade.

---

## Detalhamento técnico

**Tab:** `tab_subnotificadas`  
**Módulo:** `R/subnotificacoes.R`  
**Arquivos:**
- `dados/dados_modelo_bairro.qs` → `modelo_bairro`
- `dados/dados_modelo_ubs.qs` → `modelo_ubs`

---

## Fontes dos dados

| Objeto | Arquivo | Conteúdo |
|---|---|---|
| `modelo_bairro` | `dados/dados_modelo_bairro.qs` | Estimativas de subnotificação por bairro e ano |
| `modelo_ubs` | `dados/dados_modelo_ubs.qs` | Estimativas de subnotificação por UBS e ano |

Ambos integram **e-SUS APS** (usuárias da atenção básica) e **SINAN Violências** (notificações).

---

## Filtros

| Input ID | Variável | Obs. |
|---|---|---|
| `year` | `year` | Valores únicos das duas bases |
| `neighborhood` | `neighborhood` | Label via `pretty_name` quando disponível |
| `unit_name` | `unit_name` | Atualizado dinamicamente por `observeEvent(input$neighborhood)` |

---

## Outputs

### `tab_bairro` — DT::DTOutput
- **Reactive:** `bairro_filtrado()` → filtra `modelo_bairro` por `year` e `neighborhood`

| Nome exibido | Coluna |
|---|---|
| Bairro de residência | `pretty_name` |
| Ano | `year` |
| Usuárias da atenção básica | `resident_esus_users` |
| Notificações no SINAN | `resident_sinan_notifications` |
| Casos subnotificados | `resident_underreported_cases` |
| Casos prováveis | `resident_suspected_cases` |
| População feminina | `population` |
| Taxa casos prováveis (10k) | `subnotification_rate * 10000` |

Download: `download_bairro_filtrado` → `.xlsx`

### `tab_ubs` — DT::DTOutput
- **Reactive:** `ubs_filtrado()` → filtra `modelo_ubs` + join com `map_pretty()` para `pretty_name`

| Nome exibido | Coluna |
|---|---|
| Bairro | `pretty_name` (via join) |
| Ano | `year` |
| CNES | `cnes` |
| Unidade | `unit_name` |
| Usuárias da atenção básica | `esus_users` |
| Notificações no SINAN | `sinan_notifications` |
| Casos subnotificados | `underreported_cases` |
| Casos prováveis | `suspected_cases` |
| Taxa casos prováveis (10k) | `subnotification_rate * 10000` |

Download: `download_ubs_filtrado` → `.xlsx`

---

## Resumo de colunas

### `modelo_bairro`

| Coluna | Descrição |
|---|---|
| `neighborhood`, `pretty_name` | Identificador e nome legível do bairro |
| `year` | Ano de referência |
| `resident_esus_users` | Usuárias e-SUS APS residentes |
| `resident_sinan_notifications` | Notificações SINAN de residentes |
| `resident_underreported_cases` | Estimativa de casos subnotificados |
| `resident_suspected_cases` | Total de casos prováveis |
| `population` | População feminina |
| `subnotification_rate` | Taxa de subnotificação |

### `modelo_ubs`

| Coluna | Descrição |
|---|---|
| `neighborhood`, `year`, `cnes`, `unit_name` | Identificadores |
| `esus_users` | Usuárias e-SUS APS na unidade |
| `sinan_notifications` | Notificações SINAN na unidade |
| `underreported_cases`, `suspected_cases` | Estimativas de subnotificação |
| `subnotification_rate` | Taxa de subnotificação |

---

*© Vital Strategies, 2026*
