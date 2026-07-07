# Página 7 – Mapa da Violência

## O que é essa página?

Apresenta um **mapa interativo de Recife** com a localização geográfica das mulheres identificadas nos bancos de dados, sobreposta aos bairros da cidade e às unidades de saúde (CNES). Permite visualizar a distribuição espacial dos casos de violência e identificar concentrações por região.

---

## De onde vêm os dados?

| Dado | O que contém |
|---|---|
| **Pontos das mulheres** | Coordenadas geográficas das mulheres, com informações demográficas e trajetória nos sistemas de saúde. Originados do processo de linkage (`dados/pontos_viol_real.qs`), enriquecidos com dados da linha da vida |
| **Bairros de Recife** | Polígonos (shapefile) dos bairros da cidade (`dados/bairros.geojson`) |
| **Unidades de saúde** | Localização e nome das unidades do CNES (`dados/cnes.RData`) |

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

Um segundo painel (**Mapa**) permite personalizar a exibição:

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
