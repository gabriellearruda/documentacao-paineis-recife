# [TÉCNICO] Página 8 – Subnotificações

**Tab:** `tab_subnotificadas`  
**Módulo:** `R/subnotificacoes.R`  
**Arquivos de dados:**
- `dados/dados_modelo_bairro.qs` → objeto `modelo_bairro`
- `dados/dados_modelo_ubs.qs` → objeto `modelo_ubs`

---

## Fonte dos dados

| Objeto | Arquivo | Conteúdo |
|---|---|---|
| `modelo_bairro` | `dados/dados_modelo_bairro.qs` | Estimativas de subnotificação por bairro e ano |
| `modelo_ubs` | `dados/dados_modelo_ubs.qs` | Estimativas de subnotificação por UBS (unidade de saúde) e ano |

Ambos os objetos integram dados do **e-SUS APS** (usuárias da atenção básica) e do **SINAN Violências** (notificações).

---

## Filtros

| Input ID | Variável filtrada | Tipo |
|---|---|---|
| `year` | `year` | pickerInput múltiplo (valores únicos de ambas as bases) |
| `neighborhood` | `neighborhood` | pickerInput múltiplo (com label via `pretty_name`) |
| `unit_name` | `unit_name` | pickerInput múltiplo (dependente do bairro selecionado) |

**Obs.:** ao mudar o bairro, o filtro de UBS é atualizado dinamicamente (`observeEvent(input$neighborhood)`).

---

## Outputs

### `tab_bairro` — DT::DTOutput

- **Reactive:** `bairro_filtrado()` → filtra `modelo_bairro` por `year` e `neighborhood`
- **Colunas exibidas:**

| Nome exibido | Coluna no dado |
|---|---|
| Bairro de residência | `pretty_name` |
| Ano | `year` |
| Usuárias da atenção básica | `resident_esus_users` |
| Notificações no SINAN | `resident_sinan_notifications` |
| Casos subnotificados | `resident_underreported_cases` |
| Casos prováveis | `resident_suspected_cases` |
| População feminina | `population` |
| Taxa casos prováveis (10k) | `subnotification_rate * 10000` |

- **Download:** `download_bairro_filtrado` → `.xlsx`

### `tab_ubs` — DT::DTOutput

- **Reactive:** `ubs_filtrado()` → filtra `modelo_ubs` por `year`, `neighborhood` e `unit_name`
- **Join:** com `map_pretty()` (tabela `neighborhood → pretty_name` de `modelo_bairro`) para obter nome legível do bairro
- **Colunas exibidas:**

| Nome exibido | Coluna no dado |
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

- **Download:** `download_ubs_filtrado` → `.xlsx`

---

## Resumo de colunas utilizadas

### `modelo_bairro`

| Coluna | Descrição |
|---|---|
| `neighborhood` | Código/nome interno do bairro |
| `pretty_name` | Nome legível do bairro |
| `year` | Ano de referência |
| `resident_esus_users` | Mulheres usuárias do e-SUS APS residentes no bairro |
| `resident_sinan_notifications` | Notificações SINAN para residentes do bairro |
| `resident_underreported_cases` | Estimativa de casos subnotificados |
| `resident_suspected_cases` | Total de casos prováveis |
| `population` | População feminina do bairro |
| `subnotification_rate` | Taxa de subnotificação (proporção, multiplicada por 10k na exibição) |

### `modelo_ubs`

| Coluna | Descrição |
|---|---|
| `neighborhood` | Código/nome interno do bairro |
| `year` | Ano de referência |
| `cnes` | Código CNES da unidade |
| `unit_name` | Nome da unidade de saúde |
| `esus_users` | Usuárias do e-SUS APS atendidas na unidade |
| `sinan_notifications` | Notificações SINAN vinculadas à unidade |
| `underreported_cases` | Estimativa de casos subnotificados |
| `suspected_cases` | Total de casos prováveis |
| `subnotification_rate` | Taxa de subnotificação |
