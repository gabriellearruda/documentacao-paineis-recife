# [TÉCNICO] Página 7 – Mapa da Violência

**Tab:** `mapa_viol`  
**Módulo:** `R/mapa_ui.R` (contém UI e server)  
**Arquivos de dados:**
- `dados/pontos_viol_real.qs` → objeto `pontos_viol` (carregado no `global.R`)
- `dados/bairros.geojson` → objeto `mapa` (lido via `st_read` no módulo)
- `dados/cnes.RData` → objeto `cnes`
- `dados/cnes_join.RData` → objeto `cnes_join`

---

## Fonte dos dados

| Objeto | Arquivo | Conteúdo |
|---|---|---|
| `pontos_viol` | `dados/pontos_viol_real.qs` | Coordenadas (Latitude, Longitude) + dados demográficos + trajetória das mulheres |
| `mapa` | `dados/bairros.geojson` | Polígonos dos bairros de Recife (sf object) |
| `cnes` | `dados/cnes.RData` | Unidades de saúde: `cd_cnes_unid_not`, `NO_FANTASIA`, `latitude_cnes`, `longitude_cnes` |
| `cnes_join` | `dados/cnes_join.RData` | Tabela de join para enriquecer `df_linha_vida` com `id_unico` |

---

## Pré-processamento em `mapa_ui.R`

```r
# Garante tipos corretos em pontos_viol
pontos_viol <- pontos_viol |>
  mutate(Latitude = as.numeric(Latitude),
         Longitude = as.numeric(Longitude),
         ano_geo = as.integer(ano_geo))

# Enriquece pontos com dados da linha da vida
df_linha_vida2 <- df_linha_vida |> left_join(cnes_join, by = "id_unico")
pontos_viol    <- pontos_viol  |> left_join(df_linha_vida2, by = "id_unico")

# Lê shapefile dos bairros
mapa <- st_read("dados/bairros.geojson")
```

---

## Filtros

| Input ID | Variável filtrada | Tipo |
|---|---|---|
| `filtro_id_pessoa` | `id_pessoa` (highlight, não exclusão) | numericInput |
| `filtro_idade` | `nu_idade_anos` (range) | sliderInput |
| `filtro_raca` | `ds_raca` | selectInput (uma opção + "Todas") |
| `filtro_ano` | `ano_geo` (range) | sliderInput (2016–2025) |

**Reactive:** `filtered_pontos()` — aplica os filtros sobre `pontos_viol`; adiciona coluna `highlight` (TRUE se `id_pessoa == filtro_id_pessoa`)

**Filtro por CNES:** ao clicar em marcador de unidade, `selected_cnes()` armazena o `cd_cnes_unid_not` e filtra `filtered_pontos()` e `cnes_data` para aquela unidade. Duplo clique no mapa (`mapa_click`, delta < 0.5s) limpa a seleção.

---

## Output

### `mapa` — leafletOutput
- **Tiles:** `CartoDB.Positron` (padrão) ou `addTiles()` conforme `map_style`
- **Polígonos:** `addPolygons(mapa)` com cor/opacidade configuráveis
- **Marcadores CNES:** `addMarkers(cnes_data)` com ícone `www/img/hospital.png`
  - popup: `NO_FANTASIA`
  - layerId: `cd_cnes_unid_not`
- **Pontos das mulheres (modo normal):** `addCircleMarkers(filtered_pontos())`
  - cor: `highlight_color` se `highlight==TRUE`, senão `default_color`
  - radius: 5 se highlight, senão 1
  - popup: `nu_idade_anos`, `ds_raca_padronizada`, `texto_final`
- **Heatmap (modo ativo):** `addWebGLHeatmap` / `addHeatmap` sobre `filtered_pontos()`
- **Atualização incremental:** `leafletProxy` via `observe()` limpa e redesenha apenas os grupos `markers`, `heatmap`, `cnes`

---

## Colunas utilizadas

| Coluna | Objeto | Origem |
|---|---|---|
| `Latitude`, `Longitude` | `pontos_viol` | Coordenadas geográficas |
| `id_pessoa` | `pontos_viol` | Identificador da mulher |
| `nu_idade_anos` | `pontos_viol` | Idade em anos |
| `ds_raca` | `pontos_viol` | Raça/cor |
| `ds_raca_padronizada` | `pontos_viol` (via join) | Raça/cor padronizada |
| `ano_geo` | `pontos_viol` | Ano do evento georreferenciado |
| `cd_cnes_unid_not` | `pontos_viol` | CNES da unidade notificadora |
| `texto_final` | `pontos_viol` (via join com `df_linha_vida2`) | Resumo textual da trajetória |
| `NO_FANTASIA` | `cnes` | Nome fantasia da unidade de saúde |
| `latitude_cnes`, `longitude_cnes` | `cnes` | Coordenadas da unidade |
| `geometry` | `mapa` (sf) | Polígonos dos bairros de Recife |
