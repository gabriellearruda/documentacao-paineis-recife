-- ============================================================
-- Painel Recife - Violência
-- Queries to recreate each .qs / .RData dataset used by the panel
--
-- Database: PostgreSQL
-- Convention: all queries are plain SELECT statements ready to run.
--   To materialise as a table, uncomment the CREATE TABLE header
--   and the trailing semicolon, then wrap the SELECT inside it.
--
-- Municipality filter: Recife = cd_mun_res LIKE '261160%'
-- Female filter:       sg_sexo = 'F'  (tratado_*)
--                      sexo = 'F'     (pessoa_publica)
--                      ds_sexo = 'F'  (tratado_esus_aps_publica)
-- ============================================================


-- ============================================================
-- FILE: pontos_viol_real.qs
-- PAGE: Página 1 – Mapa
-- PURPOSE: Individual women who have at least one SINAN Violence
--   notification, with geocoordinates and cross-system trajectory
--   counts. Used to plot points on the map and populate the
--   side-panel demographic summary.
-- SOURCES:
--   registro_linkage_geo_pessoa  (coordinates)
--   registro_linkage             (events per system)
--   pessoa_publica               (demographics)
--   tratado_sinan_viol_publica   (to restrict to violence cases)
-- ============================================================

-- CREATE TABLE pontos_viol_real AS
SELECT
    pp.id_pessoa,

    -- Demographics from master person table
    pp.dt_nascimento,
    pp.sexo,
    pp.raca_cor,
    pp.orientacao_sexual,
    pp.identidade_genero,

    -- Most recent geocoordinate linked to any record for this person
    geo.geometria,
    geo.base_origem                                   AS geo_base_origem,

    -- Trajectory counts: how many records per system
    COUNT(DISTINCT CASE WHEN rl.banco = 'sinan_viol' THEN rl.id_registro_linkage END)
        AS n_sinan_viol,
    COUNT(DISTINCT CASE WHEN rl.banco = 'sinan_iexo' THEN rl.id_registro_linkage END)
        AS n_sinan_iexo,
    COUNT(DISTINCT CASE WHEN rl.banco = 'sih'        THEN rl.id_registro_linkage END)
        AS n_sih,
    COUNT(DISTINCT CASE WHEN rl.banco = 'sim'        THEN rl.id_registro_linkage END)
        AS n_sim,
    COUNT(DISTINCT CASE WHEN rl.banco = 'esus_aps'   THEN rl.id_registro_linkage END)
        AS n_esus_aps,

    -- Date range of recorded events
    MIN(rl.dt_evento_inicio)   AS dt_primeiro_evento,
    MAX(rl.dt_evento_inicio)   AS dt_ultimo_evento,

    -- Neighbourhood from the linkage registry (most common / most recent)
    rl.id_bairro_pessoa

FROM pessoa_publica AS pp

-- Keep only women
INNER JOIN (
    SELECT DISTINCT id_unico
    FROM tratado_sinan_viol_publica
    WHERE sg_sexo = 'F'
) AS viol_ids
    ON pp.id_unico = viol_ids.id_unico

-- All linkage records for this person (any system)
INNER JOIN registro_linkage AS rl
    ON rl.id_unico = pp.id_unico

-- Geocoordinates: take one representative geometry per person
--   (the most recent geocoded record)
LEFT JOIN LATERAL (
    SELECT
        rlg.geometria,
        rlg.base_origem
    FROM registro_linkage_geo_pessoa AS rlg
    INNER JOIN registro_linkage AS rl2
        ON rl2.id_registro_linkage = rlg.id_registro_linkage
        AND rl2.id_unico = pp.id_unico
    ORDER BY rl2.dt_evento_inicio DESC NULLS LAST
    LIMIT 1
) AS geo ON TRUE

WHERE pp.sexo = 'F'

GROUP BY
    pp.id_pessoa,
    pp.dt_nascimento,
    pp.sexo,
    pp.raca_cor,
    pp.orientacao_sexual,
    pp.identidade_genero,
    geo.geometria,
    geo.base_origem,
    rl.id_bairro_pessoa
;


-- ============================================================
-- FILE: sinan_viol.qs
-- PAGES: Página 2 (Violência – visão geral), Página 7 (Linha
--        da Vida), Página 8 (Subnotificações)
-- PURPOSE: Full SINAN Violence notification dataset restricted
--   to Recife and female patients. Used for charts on violence
--   type, aggressor relationship, race, age, neighbourhood, etc.
-- SOURCE: tratado_sinan_viol_publica
-- ============================================================

-- CREATE TABLE sinan_viol AS
SELECT
    sv.id_sinan_viol,
    sv.id_registro_linkage,
    sv.id_unico,

    -- Dates
    sv.dt_notific,
    sv.dt_nasc,
    sv.dt_ocor,
    sv.ano,

    -- Demographics
    sv.nu_idade_anos,
    sv.sg_sexo,
    sv.ds_raca,
    sv.cd_raca,
    sv.orient_sex,
    sv.ident_gen,

    -- Geography
    sv.ds_bairro_res,
    sv.id_bairro,

    -- Violence type flags
    sv.viol_fisic,
    sv.viol_psico,
    sv.viol_tort,
    sv.viol_sexu,
    sv.viol_traf,
    sv.viol_finan,
    sv.viol_negli,
    sv.viol_infan,
    sv.viol_legal,
    sv.viol_outr,

    -- Aggressor relationship
    sv.rel_conj,
    sv.rel_excon,
    sv.rel_namo,
    sv.rel_exnam,

    -- Occurrence setting and outcome
    sv.local_ocor,
    sv.classi_fin,
    sv.evolucao,

    -- Notification unit
    sv.cd_cnes_unid_not,
    sv.banco

FROM tratado_sinan_viol_publica AS sv
WHERE sv.sg_sexo = 'F'
  AND sv.id_bairro IS NOT NULL   -- proxy for Recife residence
;


-- ============================================================
-- FILE: df_iexo.qs
-- PAGE: Página 3 – Intoxicações Exógenas
-- PURPOSE: SINAN Exogenous Intoxication notifications for Recife
--   women. Used for charts on toxic agent, circumstances,
--   hospitalisation, and outcome.
-- SOURCE: tratado_sinan_iexo_publica
-- ============================================================

-- CREATE TABLE df_iexo AS
SELECT
    si.id_sinan_iexo,
    si.id_registro_linkage,
    si.id_unico,

    -- Dates
    si.dt_notific,
    si.dt_nasc,
    si.ano,

    -- Demographics
    si.nu_idade_anos,
    si.sg_sexo,
    si.ds_raca,

    -- Geography
    si.ds_bairro_res,

    -- Intoxication details
    si.cd_agente_tox,
    si.ds_agente_tox,
    si.cd_circunstan,
    si.ds_circunstan,
    si.cd_tpexp,
    si.ds_tpexp,

    -- Hospitalisation and outcome
    si.ds_hospital,
    si.cd_hospitalizacao,
    si.cd_evolucao,
    si.ds_evolucao

FROM tratado_sinan_iexo_publica AS si
WHERE si.sg_sexo = 'F'
  AND si.ds_bairro_res IS NOT NULL  -- restrict to records with a known neighbourhood
;


-- ============================================================
-- FILE: df_sih.qs
-- PAGE: Página 4 – Internações Hospitalares
-- PURPOSE: Hospital admissions for Recife women with diagnoses
--   relevant to violence and injury (CID-10 chapter XIX/XX and
--   related codes). Used for trend charts, diagnosis distribution,
--   and length-of-stay analysis.
-- SOURCE: tratado_sih_publica
-- NOTE: Adjust the CID-10 prefix list below to match the exact
--   codes used in the panel's filtering logic.
-- ============================================================

-- CREATE TABLE df_sih AS
SELECT
    sh.id_sih,
    sh.id_registro_linkage,
    sh.id_unico,

    -- Dates
    sh.dt_internacao,
    sh.dt_saida,
    sh.dt_nasc,
    sh.ano,

    -- Length of stay (days)
    (sh.dt_saida - sh.dt_internacao) AS dias_internacao,

    -- Demographics
    sh.nu_idade_anos,
    sh.sg_sexo,
    sh.ds_raca,

    -- Geography
    sh.ds_bairro_res,

    -- Diagnoses
    sh.cd_diag_pri,
    sh.cd_diag_sec_1,
    sh.cd_diag_sec_2,
    sh.cd_diag_sec_3,
    sh.cd_diag_sec_4,
    sh.cd_diag_sec_5,
    sh.cd_diag_sec_6,
    sh.cd_diag_sec_7,
    sh.cd_diag_sec_8,

    -- Admission details
    sh.cd_procedimento,
    sh.cd_mot_saida,
    sh.cd_car_internacao,
    sh.cd_modalidade_internacao,
    sh.cd_cnes

FROM tratado_sih_publica AS sh
WHERE sh.sg_sexo = 'F'
  AND sh.ds_bairro_res IS NOT NULL
  AND (
      -- CID-10 chapter XIX: injuries, poisonings (S00–T98)
      sh.cd_diag_pri LIKE 'S%'
   OR sh.cd_diag_pri LIKE 'T%'
      -- CID-10 chapter XX: external causes of morbidity (V01–Y98)
   OR sh.cd_diag_pri LIKE 'V%'
   OR sh.cd_diag_pri LIKE 'W%'
   OR sh.cd_diag_pri LIKE 'X%'
   OR sh.cd_diag_pri LIKE 'Y%'
      -- CID-10 Z codes used in violence / abuse contexts
   OR sh.cd_diag_pri LIKE 'Z%'
  )
;


-- ============================================================
-- FILE: df_sim.qs
-- PAGE: Página 5 – Mortalidade
-- PURPOSE: Death records for Recife women. Used for mortality
--   trend charts, cause-of-death distribution, and analysis of
--   pregnancy-related deaths.
-- SOURCE: tratado_sim_publica
-- ============================================================

-- CREATE TABLE df_sim AS
SELECT
    sm.id_sim,
    sm.id_registro_linkage,
    sm.id_unico,

    -- Dates
    sm.dt_obito,
    sm.dt_nasc,
    sm.ano,

    -- Demographics
    sm.nu_idade_anos,
    sm.sg_sexo,
    sm.ds_raca,

    -- Geography
    sm.ds_bairro_res,
    sm.cd_mun_res,

    -- Cause of death (death certificate)
    sm.cd_causabas,
    sm.cd_linhaa,
    sm.cd_linhab,
    sm.cd_linhac,
    sm.cd_linhad,
    sm.cd_linhaii,

    -- Pregnancy / puerperium fields
    sm.cd_gravidez,
    sm.cd_gestacao,
    sm.cd_obitograv,
    sm.cd_obitopuerp,

    -- Certifier type
    sm.cd_atestante

FROM tratado_sim_publica AS sm
WHERE sm.sg_sexo = 'F'
  AND (
      sm.cd_mun_res LIKE '261160%'
   OR sm.ds_bairro_res IS NOT NULL
  )
;


-- ============================================================
-- FILE: linkage_compilado_sem_banco.RData  /  base_linkage_feminino.RData
-- PAGE: Página 6 – Linkage
-- PURPOSE: Person-level view linking all health systems. Each row
--   is one woman identified by the linkage engine, with counts and
--   flags for each system she appears in.
-- SOURCES: pessoa_publica + registro_linkage + all treated tables
-- ============================================================

-- CREATE TABLE base_linkage_feminino AS
SELECT
    pp.id_pessoa,
    pp.dt_nascimento,
    pp.sexo,
    pp.raca_cor,
    pp.orientacao_sexual,
    pp.identidade_genero,

    -- System presence flags
    CASE WHEN COUNT(DISTINCT CASE WHEN rl.banco = 'sinan_viol' THEN rl.id_registro_linkage END) > 0
         THEN 1 ELSE 0 END                             AS tem_sinan_viol,
    CASE WHEN COUNT(DISTINCT CASE WHEN rl.banco = 'sinan_iexo' THEN rl.id_registro_linkage END) > 0
         THEN 1 ELSE 0 END                             AS tem_sinan_iexo,
    CASE WHEN COUNT(DISTINCT CASE WHEN rl.banco = 'sih'        THEN rl.id_registro_linkage END) > 0
         THEN 1 ELSE 0 END                             AS tem_sih,
    CASE WHEN COUNT(DISTINCT CASE WHEN rl.banco = 'sim'        THEN rl.id_registro_linkage END) > 0
         THEN 1 ELSE 0 END                             AS tem_sim,
    CASE WHEN COUNT(DISTINCT CASE WHEN rl.banco = 'esus_aps'   THEN rl.id_registro_linkage END) > 0
         THEN 1 ELSE 0 END                             AS tem_esus_aps,

    -- Record counts per system
    COUNT(DISTINCT CASE WHEN rl.banco = 'sinan_viol' THEN rl.id_registro_linkage END)
        AS n_registros_sinan_viol,
    COUNT(DISTINCT CASE WHEN rl.banco = 'sinan_iexo' THEN rl.id_registro_linkage END)
        AS n_registros_sinan_iexo,
    COUNT(DISTINCT CASE WHEN rl.banco = 'sih'        THEN rl.id_registro_linkage END)
        AS n_registros_sih,
    COUNT(DISTINCT CASE WHEN rl.banco = 'sim'        THEN rl.id_registro_linkage END)
        AS n_registros_sim,
    COUNT(DISTINCT CASE WHEN rl.banco = 'esus_aps'   THEN rl.id_registro_linkage END)
        AS n_registros_esus_aps,

    -- Number of distinct systems (linkage breadth)
    (
        CASE WHEN COUNT(DISTINCT CASE WHEN rl.banco = 'sinan_viol' THEN rl.id_registro_linkage END) > 0 THEN 1 ELSE 0 END
      + CASE WHEN COUNT(DISTINCT CASE WHEN rl.banco = 'sinan_iexo' THEN rl.id_registro_linkage END) > 0 THEN 1 ELSE 0 END
      + CASE WHEN COUNT(DISTINCT CASE WHEN rl.banco = 'sih'        THEN rl.id_registro_linkage END) > 0 THEN 1 ELSE 0 END
      + CASE WHEN COUNT(DISTINCT CASE WHEN rl.banco = 'sim'        THEN rl.id_registro_linkage END) > 0 THEN 1 ELSE 0 END
      + CASE WHEN COUNT(DISTINCT CASE WHEN rl.banco = 'esus_aps'   THEN rl.id_registro_linkage END) > 0 THEN 1 ELSE 0 END
    )                                                   AS n_sistemas,

    -- Date range across all records
    MIN(rl.dt_evento_inicio)                            AS dt_primeiro_registro,
    MAX(rl.dt_evento_inicio)                            AS dt_ultimo_registro,

    -- Neighbourhood (most frequent; approximated as the mode via subquery below)
    bairro_agg.id_bairro_pessoa

FROM pessoa_publica AS pp

INNER JOIN registro_linkage AS rl
    ON rl.id_unico = pp.id_unico

-- Mode neighbourhood per person
LEFT JOIN LATERAL (
    SELECT id_bairro_pessoa
    FROM registro_linkage AS rl_b
    WHERE rl_b.id_unico = pp.id_unico
      AND rl_b.id_bairro_pessoa IS NOT NULL
    GROUP BY id_bairro_pessoa
    ORDER BY COUNT(*) DESC
    LIMIT 1
) AS bairro_agg ON TRUE

WHERE pp.sexo = 'F'

GROUP BY
    pp.id_pessoa,
    pp.dt_nascimento,
    pp.sexo,
    pp.raca_cor,
    pp.orientacao_sexual,
    pp.identidade_genero,
    bairro_agg.id_bairro_pessoa

-- Restrict to women who appear in at least one relevant system
HAVING COUNT(DISTINCT rl.id_registro_linkage) > 0
;


-- ============================================================
-- FILE: linha_vida_esus4.qs
-- PAGE: Página 7 – Linha da Vida
-- PURPOSE: Chronological timeline of all health-system events for
--   each woman who has at least one SINAN Violence notification.
--   One row per record per woman, ordered by event date.
-- SOURCES: registro_linkage + pessoa_publica + filtered by
--   sinan_viol universe.
-- ============================================================

-- CREATE TABLE linha_vida_esus4 AS
SELECT
    rl.id_registro_linkage,
    rl.id_unico,
    rl.id_pessoa,
    rl.banco,

    -- Event timing
    rl.dt_evento_inicio,
    rl.dt_evento_fim,
    rl.dt_registro,

    -- Clinical coding
    rl.cid10_1,

    -- Geography
    rl.id_bairro_pessoa,
    rl.id_estabelecimento_saude,

    -- Age at event
    rl.idade_pessoa_evento,

    -- Analysis flags (pelvic pain / cancer screening pathways)
    rl.analise_dor_pelvica_inicio,
    rl.analise_dor_pelvica_fim,
    rl.analise_cancer_inicio,
    rl.analise_cancer_fim,

    -- Newborn flag
    rl.recem_nasc,

    -- Person-level demographics (denormalised for convenience)
    pp.dt_nascimento,
    pp.sexo,
    pp.raca_cor,
    pp.orientacao_sexual,
    pp.identidade_genero

FROM registro_linkage AS rl

INNER JOIN pessoa_publica AS pp
    ON pp.id_unico = rl.id_unico

-- Restrict universe to women with at least one SINAN Violence record
INNER JOIN (
    SELECT DISTINCT id_unico
    FROM tratado_sinan_viol_publica
    WHERE sg_sexo = 'F'
) AS viol_ids
    ON viol_ids.id_unico = rl.id_unico

WHERE pp.sexo = 'F'

ORDER BY
    rl.id_unico,
    rl.dt_evento_inicio NULLS LAST
;


-- ============================================================
-- FILE: dados_modelo_bairro.qs
-- PAGE: Página 8 – Subnotificações (neighbourhood model)
-- PURPOSE: Aggregated counts per neighbourhood × year comparing
--   e-SUS APS users (demand proxy) vs SINAN Violence notifications
--   (supply proxy). Feeds the underreporting estimation model.
-- SOURCES: tratado_esus_aps_publica  (e-SUS users)
--          tratado_sinan_viol_publica (notifications)
-- ============================================================

-- CREATE TABLE dados_modelo_bairro AS
WITH esus_bairro AS (
    -- Unique female e-SUS users per neighbourhood per year
    SELECT
        ea.ds_bairro_res,
        EXTRACT(YEAR FROM ea.dt_inicio_ap)::integer   AS ano,
        COUNT(DISTINCT ea.id_unico)                   AS n_usuarios_esus
    FROM tratado_esus_aps_publica AS ea
    WHERE ea.ds_sexo = 'F'
      AND ea.ds_bairro_res IS NOT NULL
      AND ea.dt_inicio_ap IS NOT NULL
    GROUP BY
        ea.ds_bairro_res,
        EXTRACT(YEAR FROM ea.dt_inicio_ap)
),
sinan_bairro AS (
    -- SINAN Violence notifications per neighbourhood per year
    SELECT
        sv.ds_bairro_res,
        sv.ano::integer                               AS ano,
        COUNT(*)                                      AS n_notificacoes_sinan,
        COUNT(DISTINCT sv.id_unico)                   AS n_mulheres_notificadas
    FROM tratado_sinan_viol_publica AS sv
    WHERE sv.sg_sexo = 'F'
      AND sv.ds_bairro_res IS NOT NULL
    GROUP BY
        sv.ds_bairro_res,
        sv.ano
)
SELECT
    COALESCE(e.ds_bairro_res, s.ds_bairro_res)        AS ds_bairro_res,
    COALESCE(e.ano,           s.ano)                  AS ano,
    COALESCE(e.n_usuarios_esus, 0)                    AS n_usuarios_esus,
    COALESCE(s.n_notificacoes_sinan, 0)               AS n_notificacoes_sinan,
    COALESCE(s.n_mulheres_notificadas, 0)             AS n_mulheres_notificadas,

    -- Notification rate (notifications per 1 000 e-SUS users)
    CASE
        WHEN COALESCE(e.n_usuarios_esus, 0) > 0
        THEN ROUND(
                 COALESCE(s.n_notificacoes_sinan, 0)::numeric
                 / e.n_usuarios_esus * 1000,
             2)
        ELSE NULL
    END                                               AS taxa_notificacao_por_mil

FROM esus_bairro AS e
FULL OUTER JOIN sinan_bairro AS s
    ON s.ds_bairro_res = e.ds_bairro_res
   AND s.ano           = e.ano

ORDER BY
    COALESCE(e.ds_bairro_res, s.ds_bairro_res),
    COALESCE(e.ano, s.ano)
;


-- ============================================================
-- FILE: dados_modelo_ubs.qs
-- PAGE: Página 8 – Subnotificações (UBS / CNES unit model)
-- PURPOSE: Aggregated counts per CNES health unit × year
--   comparing e-SUS APS users vs SINAN Violence notifications
--   from that unit. Feeds the UBS-level underreporting model.
-- SOURCES: tratado_esus_aps_publica  (e-SUS users, via nu_cnes)
--          tratado_sinan_viol_publica (notifications, via cd_cnes_unid_not)
--          estabelecimento_saude      (unit metadata)
-- ============================================================

-- CREATE TABLE dados_modelo_ubs AS
WITH esus_ubs AS (
    -- Unique female e-SUS users per CNES unit per year
    SELECT
        ea.nu_cnes::integer                           AS cd_cnes,
        EXTRACT(YEAR FROM ea.dt_inicio_ap)::integer   AS ano,
        COUNT(DISTINCT ea.id_unico)                   AS n_usuarios_esus
    FROM tratado_esus_aps_publica AS ea
    WHERE ea.ds_sexo = 'F'
      AND ea.nu_cnes IS NOT NULL
      AND ea.dt_inicio_ap IS NOT NULL
    GROUP BY
        ea.nu_cnes,
        EXTRACT(YEAR FROM ea.dt_inicio_ap)
),
sinan_ubs AS (
    -- SINAN Violence notifications per CNES unit per year
    SELECT
        sv.cd_cnes_unid_not                           AS cd_cnes,
        sv.ano::integer                               AS ano,
        COUNT(*)                                      AS n_notificacoes_sinan,
        COUNT(DISTINCT sv.id_unico)                   AS n_mulheres_notificadas
    FROM tratado_sinan_viol_publica AS sv
    WHERE sv.sg_sexo = 'F'
      AND sv.cd_cnes_unid_not IS NOT NULL
    GROUP BY
        sv.cd_cnes_unid_not,
        sv.ano
)
SELECT
    COALESCE(e.cd_cnes, s.cd_cnes)                    AS cd_cnes,
    COALESCE(e.ano,     s.ano)                        AS ano,
    COALESCE(e.n_usuarios_esus, 0)                    AS n_usuarios_esus,
    COALESCE(s.n_notificacoes_sinan, 0)               AS n_notificacoes_sinan,
    COALESCE(s.n_mulheres_notificadas, 0)             AS n_mulheres_notificadas,

    -- Notification rate (notifications per 1 000 e-SUS users)
    CASE
        WHEN COALESCE(e.n_usuarios_esus, 0) > 0
        THEN ROUND(
                 COALESCE(s.n_notificacoes_sinan, 0)::numeric
                 / e.n_usuarios_esus * 1000,
             2)
        ELSE NULL
    END                                               AS taxa_notificacao_por_mil,

    -- Unit metadata from CNES master
    es.razao_social,
    es.nome_fantasia,
    es.nome_bairro,
    es.id_bairro,
    es.id_tipo_unidade,
    es.id_tipo_estabelecimento

FROM esus_ubs AS e
FULL OUTER JOIN sinan_ubs AS s
    ON s.cd_cnes = e.cd_cnes
   AND s.ano     = e.ano

LEFT JOIN estabelecimento_saude AS es
    ON es.codigo_cnes = COALESCE(e.cd_cnes, s.cd_cnes)

ORDER BY
    COALESCE(e.cd_cnes, s.cd_cnes),
    COALESCE(e.ano, s.ano)
;
