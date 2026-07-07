-- ============================================================
-- vw_mapa_violencia
-- Página 1 – Mapa da Violência
-- Uma linha por mulher com coordenada geográfica, dados
-- demográficos e presença em cada sistema de saúde.
-- Fonte: registro_linkage_geo_pessoa + registro_linkage + pessoa_publica
-- ============================================================

CREATE OR REPLACE VIEW vw_mapa_violencia AS

WITH

-- 1. Mulheres com ao menos uma notificação de violência no SINAN
mulheres_violencia AS (
    SELECT DISTINCT id_pessoa
    FROM registro_linkage
    WHERE banco = 'SINAN_VIOL'
),

-- 2. Pega a coordenada geográfica mais recente de cada pessoa
geo AS (
    SELECT DISTINCT ON (rl.id_pessoa)
        rl.id_pessoa,
        g.geometria,
        g.base_origem,
        ST_X(g.geometria::geometry) AS longitude,
        ST_Y(g.geometria::geometry) AS latitude
    FROM registro_linkage_geo_pessoa g
    JOIN registro_linkage rl USING (id_registro_linkage)
    WHERE rl.id_pessoa IN (SELECT id_pessoa FROM mulheres_violencia)
    ORDER BY rl.id_pessoa, rl.dt_evento_inicio DESC
),

-- 3. Dados demográficos e sistemas em que a pessoa aparece
perfil AS (
    SELECT
        rl.id_pessoa,
        p.dt_nascimento,
        p.raca_cor,
        EXTRACT(YEAR FROM age(CURRENT_DATE, p.dt_nascimento))::int AS idade,
        -- ano do primeiro evento de violência
        MIN(CASE WHEN rl.banco = 'SINAN_VIOL' THEN EXTRACT(YEAR FROM rl.dt_evento_inicio) END) AS ano_primeira_notificacao,
        MAX(CASE WHEN rl.banco = 'SINAN_VIOL' THEN EXTRACT(YEAR FROM rl.dt_evento_inicio) END) AS ano_ultima_notificacao,
        -- presença em cada sistema (flags)
        MAX(CASE WHEN rl.banco = 'SINAN_VIOL'  THEN 1 ELSE 0 END) AS in_sinan_viol,
        MAX(CASE WHEN rl.banco = 'SINAN_IEXO'  THEN 1 ELSE 0 END) AS in_sinan_iexo,
        MAX(CASE WHEN rl.banco = 'SIH'         THEN 1 ELSE 0 END) AS in_sih,
        MAX(CASE WHEN rl.banco = 'SIM'         THEN 1 ELSE 0 END) AS in_sim,
        MAX(CASE WHEN rl.banco = 'ESUS_APS'    THEN 1 ELSE 0 END) AS in_esus,
        -- contagem de notificações de violência
        COUNT(CASE WHEN rl.banco = 'SINAN_VIOL' THEN 1 END) AS qtd_notificacoes_viol
    FROM registro_linkage rl
    JOIN pessoa_publica p USING (id_pessoa)
    WHERE rl.id_pessoa IN (SELECT id_pessoa FROM mulheres_violencia)
    GROUP BY rl.id_pessoa, p.dt_nascimento, p.raca_cor
)

SELECT
    pf.id_pessoa,
    geo.latitude,
    geo.longitude,
    geo.base_origem,
    pf.dt_nascimento,
    pf.idade,
    pf.raca_cor,
    pf.ano_primeira_notificacao,
    pf.ano_ultima_notificacao,
    pf.qtd_notificacoes_viol,
    pf.in_sinan_viol,
    pf.in_sinan_iexo,
    pf.in_sih,
    pf.in_sim,
    pf.in_esus,
    -- número de sistemas em que a mulher aparece
    (pf.in_sinan_viol + pf.in_sinan_iexo + pf.in_sih + pf.in_sim + pf.in_esus) AS qtd_sistemas

FROM perfil pf
JOIN geo USING (id_pessoa)

-- só inclui quem tem coordenada válida
WHERE geo.latitude IS NOT NULL
  AND geo.longitude IS NOT NULL;
