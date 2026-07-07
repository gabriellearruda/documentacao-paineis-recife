# Página 6 – Linha da Vida

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

**Arquivo de dados:** `dados/linha_vida_esus4.qs`

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
