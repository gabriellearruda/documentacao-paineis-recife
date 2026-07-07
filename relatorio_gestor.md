## Sobre este documento

Este relatório descreve cada página do Painel Recife, explicando **o que cada visualização mostra**, **de onde vêm os dados** e **quais filtros estão disponíveis**. O objetivo é permitir que gestores e profissionais de saúde pública utilizem o painel com segurança e interpretem corretamente as informações apresentadas.

O painel integra dados de múltiplos sistemas de saúde:

| Sistema | Sigla | O que registra |
|---|---|---|
| Sistema de Informação de Agravos de Notificação | SINAN | Notificações de violência e intoxicação exógena |
| Sistema de Informações Hospitalares | SIH | Internações hospitalares |
| Sistema de Informação sobre Mortalidade | SIM | Óbitos e causas de morte |
| Sistema de Atenção Básica | e-SUS APS | Atendimentos na atenção primária |
| Cadastro Nacional de Estabelecimentos de Saúde | CNES | Unidades de saúde e sua localização |

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

# Página 1 - Mapa da Violência

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

&nbsp;

---

# Página 2 - SINAN Violência

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
**O que mostra:** Evolução do número de notificações ao longo dos anos, permitindo identificar tendências de aumento ou queda nos registros.

---

### 2. Distribuição por faixa etária
**O que mostra:** Proporção de notificações em cada faixa de idade, revelando quais grupos etários concentram mais registros de violência.  
**Download disponível:** sim

---

### 3. Distribuição por raça/cor
**O que mostra:** Proporção de notificações por raça/cor declarada da vítima.  
**Download disponível:** sim

---

### 4. Tabela de informações do SINAN
**O que mostra:** Tabela detalhada que permite explorar diferentes características das notificações. O usuário escolhe **qual tipo de informação analisar** e **como estratificar**:

**Tipos de informação disponíveis:**

| Opção | O que analisa |
|---|---|
| Encaminhamentos | Para onde a vítima foi encaminhada após o atendimento (rede de saúde, CREAS, casa da mulher, delegacia, conselho tutelar, MPU, vara da infância, etc.) |
| Procedimentos | Procedimentos realizados durante o atendimento |
| Relação com o agressor | Vínculo entre vítima e agressor (cônjuge, familiar, conhecido, desconhecido, etc.) |
| Tipo de violência | Categorias de violência registradas na notificação |
| Meio de agressão | Como a agressão foi praticada (força corporal, arma de fogo, objeto cortante, envenenamento, etc.) |
| Deficiências | Deficiências da vítima registradas na ficha |
| Transtornos | Transtornos mentais ou comportamentais registrados na ficha |

**Formas de estratificar os resultados:**

| Opção | O que faz |
|---|---|
| Raça/cor | Abre os resultados por categoria racial |
| Faixa etária | Abre os resultados por faixa de idade |
| Ano da notificação | Mostra a evolução ao longo dos anos |
| Outras vezes | Separa casos em que houve violência anterior (Sim / Não / Ignorado) |
| Local de ocorrência | Abre por local onde ocorreu a violência (residência, via pública, escola, etc.) |

**Download disponível:** sim

---

### 5. Sexo do agressor por suspeita de uso de álcool
**O que mostra:** Gráfico de barras empilhadas cruzando o sexo do agressor (masculino, feminino, ambos, ignorado) com a suspeita de uso de álcool no momento da agressão. Permite avaliar se o uso de álcool está associado ao perfil do agressor.

---

### 6. Tabela cruzada configurável
**O que mostra:** Tabela de dupla entrada que o usuário monta livremente, cruzando duas variáveis para identificar padrões. Por exemplo: quantas notificações de cada faixa etária ocorreram em cada ano.

**Variáveis disponíveis para cruzamento:**

| Variável | Descrição |
|---|---|
| Faixa etária | Grupo de idade da vítima |
| Raça/cor | Raça/cor da vítima |
| Ano da notificação | Ano em que a notificação foi registrada |
| Outras vezes | Se houve episódios anteriores de violência |
| Local de ocorrência | Onde a violência aconteceu |

**Download disponível:** sim

---

&nbsp;

---

# Página 3 - SINAN Intoxicação Exógena

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
**O que mostra:** Evolução do número de notificações de intoxicação ao longo dos anos, permitindo identificar tendências.

---

### 2. Distribuição por faixa etária
**O que mostra:** Proporção de notificações em cada faixa de idade.  
**Download disponível:** sim

---

### 3. Distribuição por raça/cor
**O que mostra:** Proporção de notificações por raça/cor declarada da vítima.  
**Download disponível:** sim

---

### 4. Proporção por circunstância
**O que mostra:** Distribuição das notificações segundo o motivo da intoxicação (tentativa de suicídio, acidente, abuso, violência, etc.), ordenadas por frequência.  
**Download disponível:** sim

---

### 5. Proporção por agente intoxicante
**O que mostra:** Distribuição das notificações segundo a substância que causou a intoxicação (medicamentos, agrotóxicos, drogas, etc.), ordenadas por frequência.  
**Download disponível:** sim

---

### 6. Tipo de atendimento por hospitalização
**O que mostra:** Gráfico de barras empilhadas que cruza o tipo de atendimento recebido (ambulatorial, domiciliar, hospitalar, nenhum) com se o paciente foi hospitalizado (Sim / Não / Ignorado). Permite avaliar a gravidade dos casos.  
**Download disponível:** sim

---

&nbsp;

---

# Página 4 - Hospitalizações

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

---

### 2. Distribuição por faixa etária
**O que mostra:** Proporção de internações em cada faixa de idade.  
**Download disponível:** sim

---

### 3. Distribuição por raça/cor
**O que mostra:** Proporção de internações por raça/cor declarada do paciente.  
**Download disponível:** sim

---

### 4. Proporção de internações por capítulo da CID-10 (2016–2025)
**O que mostra:** Distribuição das internações pelas categorias de causa dos capítulos XIX e XX da CID-10, como fraturas, queimaduras, intoxicações, acidentes de transporte, agressões, etc. Permite identificar quais tipos de causas externas mais geram internações.

---

&nbsp;

---

# Página 5 - Mortalidade

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

---

### 2. Distribuição por faixa etária
**O que mostra:** Proporção de óbitos em cada faixa de idade.  
**Download disponível:** sim

---

### 3. Distribuição por raça/cor
**O que mostra:** Proporção de óbitos por raça/cor declarada.  
**Download disponível:** sim

---

### 4. Proporção de óbitos por causas externas — CID-10 (2016–2025)
**O que mostra:** Distribuição dos óbitos pelas categorias de causa dos capítulos XIX e XX da CID-10, como homicídios, suicídios, acidentes de transporte, afogamentos, quedas, etc. Permite identificar quais causas externas são responsáveis pela maior parte das mortes.

---

&nbsp;

---

# Página 6 - Análise do Linkage

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

---

### 1. Distribuição por faixa etária das mulheres
**O que mostra:** Comparação da distribuição etária entre mulheres **com** e **sem** notificação de violência.  
**Download disponível:** sim

---

### 2. Distribuição por raça/cor das mulheres
**O que mostra:** Comparação da distribuição por raça/cor entre mulheres **com** e **sem** notificação de violência.  
**Download disponível:** sim

---

### 3. Comparação das causas de óbito (gráfico de bolhas)
**O que mostra:** Gráfico de bolhas comparando as proporções de cada causa de óbito entre três grupos: mulheres com notificação de violência, com notificação de intoxicação exógena, e sem notificação. O tamanho da bolha representa a proporção. Período: 2019–2025.  
**Download disponível:** sim

---

### 4. Comparação das causas de internação (gráfico de bolhas)
**O que mostra:** Mesmo formato do gráfico anterior, mas para internações hospitalares. Permite comparar quais condições levam mais mulheres violentadas ao hospital. Período: 2019–2025.  
**Download disponível:** sim

---

### 5. Mulheres no SINAN Violências vs. SINAN Intoxicação Exógena
**O que mostra:** Gráfico de barras com o número de mulheres que aparecem exclusivamente no SINAN Violências, exclusivamente no SINAN Intoxicação Exógena, ou em ambos os sistemas. Período: 2019–2025.  
**Download disponível:** sim

---

&nbsp;

---

# Página 7 - Linha da Vida

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
| **Banco de dados** | Mostra mulheres que aparecem em determinado sistema; permite visualizar exclusivamente quem está só no SINAN Violências ou só no e-SUS APS |
| **Tipo de violência** | Filtra mulheres com notificação de um tipo específico de violência |
| **Violência autoprovocada** | Filtra se a violência foi autoprovocada |
| **Óbitos** | Filtra se a mulher foi a óbito |
| **Nº de notificações (SINAN Violências)** | Filtra pelo número de vezes que a mulher foi notificada no SINAN |

Os filtros só são aplicados ao clicar no botão **Filtrar**.

---

## Visualizações

### Indicadores de resumo
Exibidos abaixo do gráfico, mostram para o recorte atual:
- Número de mulheres únicas
- Total de registros de violência (SINAN)
- Maior número de notificações de uma mesma mulher
- Média e mediana de notificações por mulher

---

### Gráfico de linha da vida
**O que mostra:** Cada linha horizontal é uma mulher. Os pontos ao longo da linha mostram os eventos registrados para ela, com cores e formas diferentes por sistema. O eixo X representa o tempo (ano do evento).

**Como interagir:**
- Clique em um ponto para ver o detalhamento da mulher no painel lateral
- Clique duas vezes fora do ponto para desfazer a seleção
- Use o botão **Limpar** para redefinir todos os filtros

**Download disponível:** sim (exporta a trajetória textual de cada mulher em `.xlsx`)

---

### Painel de detalhes (lateral)
**O que mostra:** Ao clicar em uma mulher no gráfico, exibe seu perfil demográfico (raça/cor, idade) e um resumo da trajetória nos sistemas de saúde.

---

&nbsp;

---

# Página 8 - Subnotificações

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

### 1. Tabela - Subnotificação provável por bairro de residência

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

### 2. Tabela - Subnotificação provável por UBS

Para cada unidade de saúde, com as mesmas colunas acima, acrescentando o código CNES e o nome da unidade.

**Download disponível:** sim

---

*© Vital Strategies, 2026 · datascience@vitalstrategies.org*
