# Documentação técnica — Painel Recife: Violência

---

## Página 1 - Mapa da Violência

### O que é?

Mapa interativo de Recife com a localização geográfica das mulheres identificadas nos bancos de dados, sobreposta aos bairros da cidade e às unidades de saúde (CNES). Permite visualizar a distribuição espacial dos casos e identificar concentrações por região.

### De onde vêm os dados?

| Dado | O que contém |
|---|---|
| Pontos das mulheres | Coordenadas geográficas + trajetória nos sistemas via linkage |
| Bairros de Recife | Polígonos dos bairros |
| Unidades de saúde | Localização e nome (CNES) |

### 1 · SQL / ETL

Arquivos .qs e .RData pré-processados — carregados em `global.R` e `mapa_ui.R`.

| Coluna | Tabela de origem | Descrição |
|---|---|---|
| pontos_viol_real.qs | dados/pontos_viol_real.qs | Mulheres com ≥1 notificação SINAN; coordenada do endereço mais recente via linkage probabilístico (SINAN Viol + SIH + SIM + e-SUS APS) |
| cnes.RData | dados/cnes.RData | Cadastro de unidades de saúde: cd_cnes_unid_not, NO_FANTASIA, latitude_cnes, longitude_cnes |
| cnes_join.RData | dados/cnes_join.RData | Join CNES ↔ id_unico: cd_cnes_unid_not, texto_final |
| bairros.geojson | dados/bairros.geojson | Polígonos dos bairros do Recife (objeto sf) |
| linha_vida_esus4.qs | dados/linha_vida_esus4.qs | Trajetória nos sistemas (df_linha_vida): texto_final e datas de atendimento |

### 2 · Preparação

Executado uma vez no carregamento do módulo.

| Transformação | Descrição |
|---|---|
| mutate(Latitude, Longitude, ano_geo) | Converte para numeric/integer |
| left_join(cnes_join, by='id_unico') | Enriquece df_linha_vida com cd_cnes_unid_not e texto_final |
| left_join(df_linha_vida2, by='id_unico') | Adiciona trajetória e texto_final a pontos_viol |
| mutate(cd_cnes_unid_not = as.numeric(...)) | Garante tipo numérico para match com selected_cnes |
| st_read('dados/bairros.geojson') | Carrega polígonos como objeto sf (mapa) |

### 3 · Filtros

`filtro_id_pessoa` não filtra linhas — apenas define `highlight=TRUE` na linha correspondente.

| Filtro | O que faz | Input | Variável |
|---|---|---|---|
| Raça/cor | Mantém só mulheres da raça selecionada | filtro_raca | ds_raca |
| Idade | Mantém mulheres dentro da faixa de idade | filtro_idade | nu_idade_anos |
| Ano | Mantém registros do período selecionado | filtro_ano | ano_geo |
| ID Pessoa | Destaca a mulher no mapa (highlight=TRUE, não remove linhas) | filtro_id_pessoa | id_pessoa |
| CNES | Mantém só mulheres atendidas naquela unidade | selected_cnes (clique no mapa) | cd_cnes_unid_not |

### 4 · Visualizações

| Gráfico | O que mostra | Colunas usadas | Pré-processamento | Filtros |
|---|---|---|---|---|
| Polígonos dos bairros | Contornos dos bairros de Recife — identifica visualmente a qual bairro pertencem os pontos. | mapa (sf) | — | Nenhum |
| Marcadores CNES | Localização das unidades de saúde cadastradas no CNES. | cnes | — | selected_cnes |
| Circle markers (pontos) | Cada ponto representa uma mulher com ≥1 notificação de violência, posicionada pela coordenada do endereço mais recente. | pontos_viol | — | Todos; cor de destaque se highlight=TRUE |
| Heatmap (WebGL) | Concentração espacial dos casos — mostra áreas de maior densidade sem exibir pontos individuais. | pontos_viol | — | Todos; ativado por toggle_heatmap |

### Opções de visualização

| Opção | O que faz |
|---|---|
| Estilo do mapa | Altera o fundo cartográfico |
| Intensidade preenchimento | Opacidade dos bairros |
| Cor dos pontos | Cor dos marcadores das mulheres |
| Ativar Heatmap | Alterna pontos ↔ mapa de calor |

### Interatividade

- Clicar em marcador CNES: exibe nome da unidade
- Clicar em ponto de mulher: exibe idade, raça/cor e resumo da trajetória
- Clicar em unidade de saúde: filtra pontos daquela unidade; duplo clique no mapa limpa a seleção

---

## Página 2 - SINAN Violência

### O que é?

Análises sobre as notificações de violência doméstica, sexual e outras violências interpessoais registradas em Recife (2016–2025).

### De onde vêm os dados?

Sistema: SINAN — Ficha de Violência Doméstica, Sexual e/ou Outras Violências Interpessoais. Cada linha = uma notificação individual.

### 1 · SQL / ETL

Query na view `tratado_sinan_viol_publica` (PostgreSQL). Resultado salvo como `sinan_viol.qs` → objeto `df_sinan`. Filtro na query: `sg_sexo = 'F'`.

| Coluna | Tabela de origem | Descrição |
|---|---|---|
| id_pessoa | tratado_sinan_viol_publica | Identificador único da mulher (chave de linkage) |
| nu_idade_anos | tratado_sinan_viol_publica | Idade em anos |
| ds_raca | tratado_sinan_viol_publica | Raça/cor declarada |
| ano | tratado_sinan_viol_publica | Ano da notificação |
| ds_bairro_res | tratado_sinan_viol_publica | Bairro de residência |
| autor_sexo | tratado_sinan_viol_publica | Sexo do agressor (código — decodificado em viol_ui.R) |
| autor_alco | tratado_sinan_viol_publica | Suspeita de uso de álcool pelo agressor |
| les_autop | tratado_sinan_viol_publica | Lesão autoprovocada (código — decodificado em viol_ui.R) |
| local_ocor | tratado_sinan_viol_publica | Local de ocorrência (código 2 dígitos — decodificado em viol_ui.R) |
| out_vezes | tratado_sinan_viol_publica | Ocorrência repetida (código — decodificado em viol_ui.R) |
| viol_fisic, viol_psico, viol_sexu, viol_tort, viol_negli, viol_finan, viol_infan, viol_legal, viol_traf, viol_outr | tratado_sinan_viol_publica | Flags de tipo de violência (0/1) |
| ag_forca, ag_enfor, ag_objeto, ag_corte, ag_quente, ag_enven, ag_fogo, ag_ameaca, ag_outros | tratado_sinan_viol_publica | Flags de meio de agressão (0/1) |
| def_trans, def_fisica, def_mental, def_visual, def_auditi, def_out, def_espec | tratado_sinan_viol_publica | Flags de deficiência da vítima (0/1) |
| tran_ment, tran_comp | tratado_sinan_viol_publica | Flags de transtorno mental/comportamental (0/1) |
| rede_sau, enc_saude, assist_soc, enc_creas, atend_mulh, enc_mulher, cons_tutel, enc_tutela, mpu, enc_mpu, deleg_cria, enc_dpca, deleg_mulh, enc_deam, deleg, enc_deleg, infan_juv, enc_vara | tratado_sinan_viol_publica | Flags de encaminhamento para serviços (0/1) — combinados em pares em viol_ui.R |

### 2 · Preparação

Derivações em `global.R` e `viol_ui.R`. Flags `filtro_viol_*` criadas para cada tipo de violência.

| Coluna derivada | Lógica |
|---|---|
| faixa_etaria_padrao | faixa_etaria_func(nu_idade_anos) |
| filtro_viol_fisica … filtro_viol_autoprovocada | Flag binária por tipo de violência (usada nos filtros) |
| ds_tipo_violencia | Descrição concatenada dos tipos de violência presentes |
| ds_autor_sexo | Decode: '1'→Masculino, '2'→Feminino, '3'→Ambos, else Ignorado |
| les_autop (decodificado) | Decode: '1'→Sim, '2'→Não, '9'/NA→Ignorado |
| local_ocor (decodificado) | Decode código 2 dígitos para texto legível |
| out_vezes (decodificado) | Decode: '1'→Sim, '2'→Não, '9'→Ignorado |
| rede_enc_sau … infan_enc_juv | OR dos dois flags de encaminhamento correspondentes |

### 3 · Filtros

`filtro_violencias` usa `filter_at` — retém linhas onde qualquer flag selecionada = 1.

| Filtro | O que faz | Input | Variável |
|---|---|---|---|
| Raça/cor | Mantém só mulheres da raça selecionada | filtro_raca | ds_raca |
| Faixa etária | Mantém mulheres dentro da faixa de idade | filtro_faixa_etaria | faixa_etaria_padrao |
| Tipo de violência | Mantém notificações com o tipo marcado | filtro_violencias | filtro_viol_* (flags) |
| Ano | Mantém registros do período — não aplicado em freq_ano_graf | filtro_ano | ano |
| Circunstância | Mantém só a circunstância selecionada | filtro_circuns | ds_circunstancia |

### 4 · Visualizações

| Gráfico | O que mostra | Colunas usadas | Pré-processamento | Filtros |
|---|---|---|---|---|
| freq_ano_graf | Evolução do número de notificações ao longo dos anos — identifica tendências de aumento ou queda. | df_sinan (sem filtro_ano) | — | Série histórica completa |
| kpi_notificacoes, kpi_pessoas | Total de notificações e número de pessoas únicas no recorte selecionado. | df_filtrado() | — | Todos os filtros |
| graf_tipos | Distribuição dos tipos de violência registrados (física, sexual, psicológica, tortura, etc.). | df_filtrado() | — | Todos os filtros |
| graf_local | Distribuição das notificações por local de ocorrência (residência, via pública, escola, etc.). | df_filtrado() | — | Todos os filtros |
| tabela_cruzada | Tabela de dupla entrada que o usuário monta livremente, cruzando duas variáveis para identificar padrões. | df_sinan direto | — | Ignora filtro_violencias |
| mapa_violencia | Distribuição geográfica das notificações por bairro de residência da vítima. | df_filtrado() | — | Todos os filtros |

---

## Página 3 - SINAN Intoxicação Exógena

### O que é?

Análises sobre notificações de intoxicação exógena — exposição a substâncias tóxicas (medicamentos, agrotóxicos, drogas). Dados de 2016–2025.

### De onde vêm os dados?

Sistema: SINAN — Ficha de Intoxicação Exógena. Cada linha = uma notificação individual.

### 1 · SQL / ETL

Query na view `tratado_sinan_iexo_publica`. Resultado salvo como `df_iexo.qs` → objeto `df_iexo`. Filtro: `sg_sexo = 'F'`.

| Coluna | Tabela de origem | Descrição |
|---|---|---|
| id_pessoa | tratado_sinan_iexo_publica | Identificador único da mulher (chave de linkage) |
| nu_idade_anos | tratado_sinan_iexo_publica | Idade em anos |
| ds_raca | tratado_sinan_iexo_publica | Raça/cor declarada |
| ano | tratado_sinan_iexo_publica | Ano da notificação |
| ds_circunstan | tratado_sinan_iexo_publica | Circunstância da intoxicação (tentativa de suicídio, acidente, etc.) |
| ds_agente_tox | tratado_sinan_iexo_publica | Substância causadora da intoxicação |
| ds_tpatend | tratado_sinan_iexo_publica | Tipo de atendimento (ambulatorial, hospitalar, domiciliar, etc.) |
| ds_hospital | tratado_sinan_iexo_publica | Hospitalização (Sim / Não / Ignorado) |

### 2 · Preparação

Apenas `faixa_etaria_padrao` derivada via `faixa_etaria_func()`.

### 3 · Filtros

`freq_ano_graf` usa `df_iexo` sem `filtro_ano` (série histórica completa).

| Filtro | O que faz | Input | Variável |
|---|---|---|---|
| Raça/cor | Mantém só mulheres da raça selecionada | filtro_raca | ds_raca |
| Faixa etária | Mantém mulheres dentro da faixa de idade | filtro_faixa_etaria | faixa_etaria_padrao |
| Circunstância | Mantém só a circunstância selecionada | filtro_circuns | ds_circunstan |
| Ano | Mantém registros do período — não aplicado em freq_ano_graf | filtro_ano | ano |

### 4 · Visualizações

| Gráfico | O que mostra | Colunas usadas | Pré-processamento | Filtros |
|---|---|---|---|---|
| freq_ano_graf | Evolução das notificações de intoxicação ao longo dos anos. | df_iexo (sem filtro_ano) | — | Série histórica |
| kpi_notificacoes, kpi_pessoas | Total de notificações e número de pessoas únicas no recorte. | df_iexo_filtrado() | — | Todos os filtros |
| graf_circuns | Distribuição por motivo da intoxicação (tentativa de suicídio, acidente, abuso, violência…). | df_iexo_filtrado() | — | Todos os filtros |
| graf_agente | Distribuição por substância causadora (medicamentos, agrotóxicos, drogas…). | df_iexo_filtrado() | — | Todos os filtros |
| graf_faixa_etaria | Proporção de notificações em cada faixa de idade. | df_iexo_filtrado() | — | Todos os filtros |
| tabela_detalhe | Tipo de atendimento × hospitalização — avalia a gravidade dos casos. | df_iexo_filtrado() | — | Todos os filtros |

---

## Página 4 - Hospitalizações

### O que é?

Análises sobre internações hospitalares por causas externas (capítulos XIX e XX da CID-10) registradas em Recife (2016–2025).

### De onde vêm os dados?

Sistema: SIH — Sistema de Informações Hospitalares do SUS. Tabela auxiliar: CID-10.

### 1 · SQL / ETL

Query na view `tratado_sih_publica`. Filtros na query: `sg_sexo = 'F'` · `ds_bairro_res IS NOT NULL` · `cd_diag_pri LIKE S/T/V/W/X/Y/Z%` (caps XIX, XX + Z). Resultado salvo como `df_sih.qs`.

| Coluna | Tabela de origem | Descrição |
|---|---|---|
| id_pessoa | tratado_sih_publica | Identificador único da mulher (chave de linkage) |
| id_pareamento | tratado_sih_publica | Chave de linkage do registro |
| dt_internacao, dt_saida | tratado_sih_publica | Datas de entrada e saída da internação |
| dt_nascimento, ano | tratado_sih_publica | Data de nascimento e ano da internação |
| dias_internacao | Calculada na query | dt_saida − dt_internacao |
| nu_idade_anos | tratado_sih_publica | Idade em anos |
| sg_sexo | tratado_sih_publica | Sexo (sempre 'F') |
| ds_raca | tratado_sih_publica | Raça/cor declarada |
| ds_bairro_res | tratado_sih_publica | Bairro de residência |
| cd_diag_pri | tratado_sih_publica | Diagnóstico principal (CID-10) |
| cd_diag_sec | tratado_sih_publica | Diagnósticos secundários |
| cd_proc_rea | tratado_sih_publica | Procedimento realizado |
| motiv_saida | tratado_sih_publica | Motivo da saída |
| carater_int | tratado_sih_publica | Caráter da internação |
| mod_intern | tratado_sih_publica | Modalidade (eletiva, urgência…) |
| cd_cnes_unid_not | tratado_sih_publica | Unidade de saúde |

### 2 · Preparação

`faixa_etaria_padrao` derivada via `faixa_etaria_func()`. `dias_internacao` calculada na query SQL.

### 3 · Filtros

`freq_ano_graf` usa `df_sih` sem `filtro_ano` (série histórica completa).

| Filtro | O que faz | Input | Variável |
|---|---|---|---|
| Raça/cor | Mantém só mulheres da raça selecionada | filtro_raca | ds_raca |
| Faixa etária | Mantém mulheres dentro da faixa de idade | filtro_faixa_etaria | faixa_etaria_padrao |
| Ano | Mantém registros do período — não aplicado em freq_ano_graf | filtro_ano | ano |

### 4 · Visualizações

| Gráfico | O que mostra | Colunas usadas | Pré-processamento | Filtros |
|---|---|---|---|---|
| freq_ano_graf | Evolução do número de internações por causas externas ao longo dos anos. | df_sih (sem filtro_ano) | — | Série histórica |
| kpi_internacoes, kpi_pessoas | Total de internações e número de pessoas únicas hospitalizadas no recorte. | df_sih_filtrado() | — | Todos os filtros |
| graf_diag | Distribuição das internações pelos capítulos XIX e XX da CID-10 — identifica as causas mais frequentes de hospitalização. | df_sih_filtrado() + join cid_10.csv | join feito por demanda dentro do renderPlotly | Todos os filtros |
| graf_tempo | Distribuição do tempo de internação (dias) por grupo diagnóstico — avalia a gravidade relativa dos casos. | df_sih_filtrado() | — | Todos os filtros |

---

## Página 5 - Mortalidade

### O que é?

Análises sobre óbitos por causas externas (capítulos XIX e XX da CID-10) registrados em Recife (2016–2025).

### De onde vêm os dados?

Sistema: SIM — Sistema de Informações sobre Mortalidade. Tabela auxiliar: CID-10.

### 1 · SQL / ETL

Query na view `tratado_sim_publica`. Filtros: `sg_sexo = 'F'` · causas externas (CID cap. XX). Resultado salvo como `df_sim.qs`.

| Coluna | Tabela de origem | Descrição |
|---|---|---|
| id_pessoa | tratado_sim_publica | Identificador único da mulher (chave de linkage) |
| cd_causabas | tratado_sim_publica | Causa básica do óbito (CID-10) |
| dt_obito | tratado_sim_publica | Data do óbito |
| ano | tratado_sim_publica | Ano do óbito |
| nu_idade_anos | tratado_sim_publica | Idade em anos |
| sg_sexo | tratado_sim_publica | Sexo (sempre 'F') |
| ds_raca | tratado_sim_publica | Raça/cor declarada |
| ds_bairro_res | tratado_sim_publica | Bairro de residência |

### 2 · Preparação

`faixa_etaria_padrao` derivada via `faixa_etaria_func()`.

### 3 · Filtros

`freq_ano_graf` usa `df_sim` sem `filtro_ano` (série histórica completa).

| Filtro | O que faz | Input | Variável |
|---|---|---|---|
| Raça/cor | Mantém só mulheres da raça selecionada | filtro_raca | ds_raca |
| Faixa etária | Mantém mulheres dentro da faixa de idade | filtro_faixa_etaria | faixa_etaria_padrao |
| Ano | Mantém registros do período — não aplicado em freq_ano_graf | filtro_ano | ano |

### 4 · Visualizações

| Gráfico | O que mostra | Colunas usadas | Pré-processamento | Filtros |
|---|---|---|---|---|
| freq_ano_graf | Evolução do número de óbitos por causas externas ao longo dos anos. | df_sim (sem filtro_ano) | — | Série histórica |
| kpi_obitos, kpi_pessoas | Total de óbitos e número de pessoas únicas no recorte. | df_sim_filtrado() | — | Todos os filtros |
| graf_obito | Distribuição dos óbitos pelos capítulos XIX e XX da CID-10 — identifica as causas mais frequentes de morte. | df_sim_filtrado() | join cid_10.csv feito por demanda dentro do renderPlotly | Apenas filtro_ano; join CID por demanda |
| mapa_mortalidade | Distribuição geográfica dos óbitos por bairro de residência. | df_sim_filtrado() | — | Todos os filtros |

---

## Página 6 - Análise do Linkage

### O que é?

Resultados do linkage probabilístico — cruzamento de SINAN Violência, SIH, SIM e e-SUS APS para identificar mulheres presentes em múltiplos sistemas (2019–2025).

### De onde vêm os dados?

Linkage probabilístico entre SINAN Violência, SIH, SIM e e-SUS APS. Objetos: `base_linkage_feminino` + `linkage_compilado` + `icd_map`.

### 1 · SQL / ETL

`base_linkage_feminino` construída via query que cruza `pessoa_publica` com `registro_linkage`, agregando flags de presença por sistema. `linkage_compilado` é uma agregação pré-computada.

| Coluna | Tabela de origem | Descrição |
|---|---|---|
| id_pessoa | pessoa_publica INNER JOIN registro_linkage | Identificador único da mulher |
| in_sinan_viol | base_linkage_feminino | Flag: presente no SINAN Violências |
| in_sim | base_linkage_feminino | Flag: presente no SIM (óbitos) |
| in_sih | base_linkage_feminino | Flag: presente no SIH (internações) |
| in_esus | base_linkage_feminino | Flag: presente no e-SUS APS |
| banco | base_linkage | Sistema de origem do registro |
| cd_causabas | base_linkage | Código CID-10 da causa (óbito ou internação) |
| FL_SINAN_VIOL, FL_SINAN_IEXO | base_linkage | Flags de presença por tipo de SINAN |
| rotulo_viol_interpessoal | linkage_compilado | Flag: tem notificação de violência interpessoal |
| fl_esus, fl_ob_not_externas | linkage_compilado | Flags de e-SUS e óbito por causas externas |
| raca_cor, faixa_etaria_padrao | linkage_compilado | Dados demográficos agregados |
| registros, n_pessoas | linkage_compilado | Contagens de registros e mulheres únicas |
| cd_causabas → causa_resumida | icd_map_ufmg.Rdata | Dicionário CID-10 → descrição resumida UFMG |

### 2 · Preparação

`df_obitos` e `df_internacoes` recebem join com `icd_map` para obter `causa_resumida`.

| Objeto | Lógica |
|---|---|
| linkage_kpi | select() de linkage_compilado: rotulo_viol_interpessoal, fl_esus, raca_cor, faixa_etaria_padrao, fl_ob_not_externas, registros, n_pessoas |
| df_obitos | base_linkage \|> filter(banco=='SIM') \|> left_join(icd_map, by='cd_causabas') |
| df_internacoes | base_linkage \|> filter(banco=='SIH') \|> left_join(icd_map, by='cd_causabas') |

### 3 · Filtros

Filtros reativos se aplicam **apenas** aos KPIs e gráficos demográficos. Bolhas e comparativo SINAN usam dados estáticos.

| Filtro | O que faz | Input | Variável |
|---|---|---|---|
| Faixa etária | Restringe KPIs e gráficos demográficos pela faixa de idade | filtro_idade | faixa_etaria_padrao |
| Raça/cor | Restringe KPIs e gráficos demográficos pela raça | filtro_raca | raca_cor |
| Presença e-SUS | Inclui ou exclui mulheres com atendimento no e-SUS APS | filtro_esus | fl_esus |

### 4 · Visualizações

| Gráfico | O que mostra | Colunas usadas | Pré-processamento | Filtros |
|---|---|---|---|---|
| KPI boxes | Número de mulheres, total de notificações e proporção presente em cada sistema (SINAN, SIH, SIM, e-SUS). | kpi_filtrada() | — | filtro_idade, raça, e-SUS |
| graf_raca | Comparação da distribuição por raça/cor entre mulheres com e sem notificação de violência. | kpi_filtrada() | — | filtro_idade, raça, e-SUS |
| graf_faixa_etaria | Comparação da distribuição etária entre mulheres com e sem notificação de violência. | kpi_filtrada() | — | filtro_idade, raça, e-SUS |
| Bolhas causas óbito | Proporções de cada causa de óbito entre 3 grupos de mulheres (violência, intoxicação, sem notificação). Período: 2019–2025. | df_obitos | estático | Nenhum |
| Bolhas causas internação | Mesmo formato para internações. Período: 2019–2025. | df_internacoes | estático | Nenhum |
| Comparativo SINAN | Mulheres exclusivamente no SINAN Violências vs. Intoxicação vs. em ambos. | linkage_compilado | estático | Nenhum |

---

## Página 7 - Linha da Vida

### O que é?

Trajetória individual de cada mulher ao longo do tempo, mostrando eventos registrados em múltiplos sistemas. Resultado do linkage entre SINAN, SIH, SIM e e-SUS APS.

### De onde vêm os dados?

| Sistema | Símbolo | O que representa |
|---|---|---|
| SINAN Violências | ✕ vermelho | Notificação de violência |
| SIH | ▲ amarelo | Internação hospitalar |
| SIM | ■ azul escuro | Óbito |
| SINAN Intox. Exógena | ◆ azul claro | Notificação de intoxicação |
| e-SUS APS | ● roxo | Atendimento na atenção básica |

### 1 · SQL / ETL

Query `linha_vida_esus4`: cruza `registro_linkage` com `pessoa_publica` e filtra somente mulheres com ≥1 notificação de violência (`viol_ids` subquery sobre `tratado_sinan_viol_publica` com `sg_sexo='F'`).

| Coluna | Tabela de origem | Descrição |
|---|---|---|
| id_pessoa, id_pareamento | registro_linkage INNER JOIN pessoa_publica | Identificadores únicos da mulher e do registro |
| banco | registro_linkage | Sistema de origem do evento |
| dt_evento_inicio, dt_evento_fim | registro_linkage | Datas de início e fim do evento |
| dt_comum | Derivada (coalesce) | Data principal do evento — coalesce das datas disponíveis |
| ds_raca_padronizada | pessoa_publica | Raça/cor padronizada |
| nu_idade_anos | pessoa_publica | Idade em anos |
| nome_ultimo_bairro | pessoa_publica | Bairro do último endereço (NA → 'Sem informação') |
| fl_sinan_viol, fl_sim, fl_sih, fl_sinan_iexo, fl_esus_aps | Derivadas em linha_vida.R | Flags de presença por sistema (group_by id_pessoa) |
| so_sinan, so_esus_aps | Derivadas em linha_vida.R | Flags de exclusividade: só SINAN / só e-SUS |
| fl_les_autop, fl_viol_* | registro_linkage | Flags de lesão autoprovocada e tipo de violência |
| texto_final | Derivado (HTML) | Resumo textual da trajetória da mulher |

### 2 · Preparação

| Coluna derivada | Lógica |
|---|---|
| fl_esus_aps | group_by(id_pessoa) \|> mutate(any(banco == 'e-SUS APS')) |
| so_sinan | group_by \|> mutate(all(banco == 'SINAN_VIOL')) |
| so_esus_aps | group_by \|> mutate(all(banco == 'e-SUS APS')) |
| faixa_etaria_padrao | faixa_etaria_func(idade_minima) — menor idade registrada por pessoa |
| texto_banco / cor_banco | Labels e cores por sistema de origem |

### 3 · Filtros

Filtros aplicados via botão Filtrar → `filtros_aplicados()`. `filtro_banco` suporta seleção exclusiva via flags `so_sinan`/`so_esus_aps`.

| Filtro | O que faz | Input | Variável |
|---|---|---|---|
| Raça/cor | Mantém só mulheres da raça selecionada | filtro_raca | ds_raca_padronizada |
| Faixa etária | Mantém mulheres dentro da faixa de idade mínima | filtro_faixa_etaria | faixa_etaria_padrao |
| Sistema de origem | Exibe mulheres somente no SINAN, somente no e-SUS ou em ambos | filtro_banco | so_sinan / so_esus_aps / fl_esus_aps |
| N° notificações | Mantém mulheres com número de notificações no intervalo | filtro_n_notif (slider) | contagem SINAN_VIOL por id_pessoa |
| Período | Mantém eventos dentro do intervalo de datas | filtro_periodo (dateRange) | dt_evento_inicio |
| Bairro | Mantém mulheres do bairro selecionado | filtro_bairro | nome_ultimo_bairro |
| Unidade notificadora | Mantém mulheres atendidas na unidade selecionada | filtro_unidade | cd_cnes_unid_not |
| ID Pessoa | Filtra diretamente pelo ID da mulher | filtro_id_pessoa | id_pessoa |

### 4 · Visualizações

| Gráfico | O que mostra | Colunas usadas | Pré-processamento | Filtros |
|---|---|---|---|---|
| Gráfico Linha da Vida | Cada linha horizontal é uma mulher. Os pontos mostram eventos nos diferentes sistemas ao longo do tempo, com cor e forma por sistema. | df_linha_filtrado() | — | Todos os filtros |
| KPI pessoas selecionadas | Número de mulheres únicas no recorte atual dos filtros. | df_linha_filtrado() | — | Todos os filtros |
| Tabela resumo por pessoa | Perfil demográfico (raça/cor, faixa etária) e contagem de eventos por sistema para cada mulher no recorte. | df_linha_filtrado() | — | Todos os filtros |
| Download dados filtrados | Exporta a trajetória textual de cada mulher no recorte em formato .xlsx. | df_linha_filtrado() | — | Todos os filtros |

### Interatividade

- Clicar em um ponto do gráfico: exibe perfil demográfico e resumo de eventos no painel lateral
- Clicar duas vezes fora do ponto: desfaz a seleção

---

## Página 8 - Subnotificações

### O que é?

Estimativa dos casos de violência prováveis que não foram notificados no SINAN. Dois níveis de análise: por bairro de residência e por UBS de referência.

### De onde vêm os dados?

| Sistema | O que contribui |
|---|---|
| e-SUS APS | Número de mulheres usuárias da atenção básica por bairro/UBS |
| SINAN Violências | Número de notificações de violência registradas por bairro/UBS |

### 1 · SQL / ETL

Dois queries pré-computados combinando dados e-SUS APS, SINAN Violência e o output do modelo estatístico.

| Coluna | Tabela de origem | Descrição |
|---|---|---|
| neighborhood, pretty_name | dados_modelo_bairro | Identificador e nome legível do bairro |
| year | dados_modelo_bairro | Ano de referência |
| resident_esus_users | dados_modelo_bairro | Mulheres usuárias do e-SUS APS residentes no bairro |
| resident_sinan_notifications | dados_modelo_bairro | Notificações SINAN de violência de residentes |
| resident_underreported_cases | dados_modelo_bairro | Estimativa de casos subnotificados (modelo) |
| resident_suspected_cases | dados_modelo_bairro | Total de casos prováveis (notificados + subnotificados) |
| population | dados_modelo_bairro | População feminina do bairro |
| subnotification_rate | dados_modelo_bairro | Taxa de subnotificação (x10.000 para exibição) |
| cnes, unit_name | dados_modelo_ubs | Código CNES e nome da unidade de saúde |
| esus_users | dados_modelo_ubs | Mulheres usuárias do e-SUS APS na unidade |
| sinan_notifications | dados_modelo_ubs | Notificações SINAN na unidade |
| underreported_cases, suspected_cases | dados_modelo_ubs | Estimativas de subnotificação por UBS |
| subnotification_rate | dados_modelo_ubs | Taxa de subnotificação por UBS (x10.000) |

### 2 · Preparação

Nenhuma derivação adicional no R além do join com `pretty_name` para exibição legível do bairro.

### 3 · Filtros

O filtro de UBS (`unit_name`) depende do bairro selecionado: `observeEvent(neighborhood)` atualiza os choices de `unit_name` dinamicamente.

| Filtro | O que faz | Input | Variável |
|---|---|---|---|
| Ano | Mantém somente o(s) ano(s) selecionado(s) | year (pickerInput) | year |
| Bairro | Mantém somente o(s) bairro(s) selecionado(s) | neighborhood (pickerInput) | neighborhood |
| UBS | Mantém somente a(s) unidade(s) selecionada(s) — choices atualizados por bairro | unit_name (pickerInput) | unit_name |

### 4 · Visualizações

| Gráfico | O que mostra | Colunas usadas | Pré-processamento | Filtros |
|---|---|---|---|---|
| tab_bairro (DT) | Estimativa de subnotificação por bairro — compara casos notificados com esperados pelo modelo. | modelo_bairro | pré-computado | year, neighborhood |
| tab_ubs (DT) | Estimativa de subnotificação por UBS — identifica unidades com maior gap entre notificações e casos esperados. | modelo_ubs | pré-computado | year, neighborhood, unit_name |
