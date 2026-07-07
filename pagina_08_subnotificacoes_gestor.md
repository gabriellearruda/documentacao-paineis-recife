# Página 8 – Subnotificações

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

**Arquivos utilizados:**
- `dados/dados_modelo_bairro.qs` → modelo de subnotificação agregado por bairro
- `dados/dados_modelo_ubs.qs` → modelo de subnotificação agregado por UBS

---

## Filtros disponíveis

| Filtro | O que faz |
|---|---|
| **Ano** | Seleciona o(s) ano(s) de referência da análise |
| **Bairro** | Filtra por bairro de residência |
| **UBS** | Filtra por unidade de saúde (depende do bairro selecionado) |

---

## Visualizações

### 1. Tabela – Subnotificação provável por bairro de residência
**O que mostra:** Para cada bairro e ano selecionados:

| Coluna | Descrição |
|---|---|
| Bairro de residência | Nome do bairro |
| Ano | Ano de referência |
| Usuárias da atenção básica | Mulheres com registro no e-SUS APS no bairro |
| Notificações no SINAN | Notificações de violência registradas para moradoras do bairro |
| Casos subnotificados | Estimativa de casos não notificados |
| Casos prováveis | Total estimado de casos (notificados + subnotificados) |
| População feminina | População feminina do bairro |
| Taxa casos prováveis (por 10 mil hab.) | Casos prováveis por 10.000 mulheres |

**Download disponível:** sim

---

### 2. Tabela – Subnotificação provável por UBS
**O que mostra:** Para cada unidade de saúde, com as mesmas colunas acima, acrescentando o código CNES e o nome da unidade.

**Download disponível:** sim
