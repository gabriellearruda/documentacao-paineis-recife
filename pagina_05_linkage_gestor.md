# Página 5 – Análise do Linkage

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

**Arquivos utilizados:**
- `dados/linkage_compilado_sem_banco.RData` → dados agregados para os cards e gráficos de perfil
- `dados/base_linkage_feminino.RData` → dados individuais para os gráficos comparativos de causas

**Dicionário de causas:** `dados/icd_map_ufmg.Rdata` — mapeamento de códigos CID-10 para descrições resumidas (elaborado pela UFMG)

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

---

### 1. Distribuição por faixa etária das mulheres
**O que mostra:** Comparação da distribuição etária entre mulheres **com** e **sem** notificação de violência. Permite identificar se há concentração em determinadas faixas de idade entre as vítimas.  
**Download disponível:** sim

---

### 2. Distribuição por raça/cor das mulheres
**O que mostra:** Comparação da distribuição por raça/cor entre mulheres **com** e **sem** notificação de violência.  
**Download disponível:** sim

---

### 3. Comparação das causas de óbito (gráfico de bolhas)
**O que mostra:** Gráfico de bolhas comparando as proporções de cada causa de óbito entre três grupos: mulheres com notificação de violência, mulheres com notificação de intoxicação exógena, e mulheres sem notificação. O tamanho da bolha representa a proporção. Período: 2019–2025.  
**Download disponível:** sim

---

### 4. Comparação das causas de internação (gráfico de bolhas)
**O que mostra:** Mesmo formato do gráfico anterior, mas para internações hospitalares em vez de óbitos. Permite comparar quais condições levam mais mulheres violentadas ao hospital. Período: 2019–2025.  
**Download disponível:** sim

---

### 5. Mulheres no SINAN Violências vs. SINAN Intoxicação Exógena
**O que mostra:** Gráfico de barras com o número de mulheres que aparecem exclusivamente no SINAN Violências, exclusivamente no SINAN Intoxicação Exógena, ou em ambos os sistemas. Período: 2019–2025.  
**Download disponível:** sim
