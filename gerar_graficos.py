"""
Gera gráficos ilustrativos para cada página do Painel Recife – Violência.
Usa dados simulados realistas (sem acesso ao banco).
Salva PNGs em docs/imagens/
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as mticker
from matplotlib.gridspec import GridSpec

np.random.seed(42)

OUT = "C:/Users/gabri/painel-shiny-recife/docs/imagens"
os.makedirs(OUT, exist_ok=True)

AZUL      = "#121E87"
VERMELHO  = "#FF5054"
CINZA     = "#6b7280"
CINZA_CLR = "#f3f4f6"
VERDE     = "#10b981"
LARANJA   = "#f59e0b"

ANOS = list(range(2016, 2025))

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "axes.grid.axis": "y",
    "grid.alpha": 0.3,
    "figure.dpi": 150,
})


def salvar(fig, nome):
    path = f"{OUT}/{nome}.png"
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  {nome}.png")


# ══════════════════════════════════════════════════════════════════════════════
# PÁGINA 2 – SINAN Violência
# ══════════════════════════════════════════════════════════════════════════════
print("Página 2 – SINAN Violência")

# 1. Notificações por ano
notif = [620, 710, 780, 830, 890, 760, 1020, 1150, 1080]
fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.bar(ANOS, notif, color=AZUL, alpha=0.85, width=0.6)
ax.bar_label(bars, fmt="%d", fontsize=9, color=CINZA, padding=3)
ax.set_title("Notificações de Violência por Ano – Recife", fontsize=13, fontweight="bold")
ax.set_xlabel("Ano")
ax.set_ylabel("Notificações")
ax.set_ylim(0, 1300)
salvar(fig, "p2_notificacoes_por_ano")

# 2. Tipo de violência
tipos = ["Física", "Psicológica", "Sexual", "Tortura", "Tráfico", "Financeira", "Negligência"]
pcts  = [62, 48, 29, 18, 4, 9, 11]
fig, ax = plt.subplots(figsize=(9, 5))
cores = [AZUL, AZUL, VERMELHO, CINZA, CINZA, CINZA, CINZA]
barras = ax.barh(tipos[::-1], pcts[::-1], color=cores[::-1], alpha=0.85)
ax.bar_label(barras, fmt="%.0f%%", fontsize=9, padding=3)
ax.set_title("Tipo de Violência (% das notificações)", fontsize=13, fontweight="bold")
ax.set_xlabel("% das notificações")
ax.set_xlim(0, 80)
salvar(fig, "p2_tipo_violencia")

# 3. Faixa etária
faixas = ["< 10", "10–19", "20–29", "30–39", "40–49", "50–59", "60+"]
vals   = [5, 18, 30, 25, 12, 6, 4]
fig, ax = plt.subplots(figsize=(9, 5))
ax.bar(faixas, vals, color=AZUL, alpha=0.85, width=0.6)
ax.set_title("Distribuição por Faixa Etária – SINAN Violência", fontsize=13, fontweight="bold")
ax.set_xlabel("Faixa etária")
ax.set_ylabel("% das notificações")
salvar(fig, "p2_faixa_etaria")

# 4. Raça/cor
racas = ["Parda", "Preta", "Branca", "Amarela", "Indígena", "Ignorado"]
vals  = [54, 22, 18, 1, 0.5, 4.5]
fig, ax = plt.subplots(figsize=(8, 4))
cores2 = [AZUL, AZUL, CINZA, CINZA, CINZA, CINZA]
b = ax.barh(racas[::-1], vals[::-1], color=cores2[::-1], alpha=0.85)
ax.bar_label(b, fmt="%.1f%%", fontsize=9, padding=3)
ax.set_title("Raça/Cor – SINAN Violência", fontsize=13, fontweight="bold")
ax.set_xlim(0, 70)
salvar(fig, "p2_raca_cor")


# ══════════════════════════════════════════════════════════════════════════════
# PÁGINA 3 – SINAN Intoxicação Exógena
# ══════════════════════════════════════════════════════════════════════════════
print("Página 3 – SINAN Intoxicação Exógena")

# 5. Casos por ano
iexo = [310, 350, 420, 390, 460, 510, 580, 620, 590]
fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(ANOS, iexo, marker="o", color=LARANJA, linewidth=2.5, markersize=7)
ax.fill_between(ANOS, iexo, alpha=0.15, color=LARANJA)
ax.set_title("Notificações de Intoxicação Exógena por Ano – Recife", fontsize=13, fontweight="bold")
ax.set_xlabel("Ano")
ax.set_ylabel("Notificações")
ax.set_ylim(0, 750)
salvar(fig, "p3_iexo_por_ano")

# 6. Agente tóxico
agentes = ["Medicamentos", "Agrotóxico", "Álcool", "Droga", "Produto químico", "Outros"]
vals    = [38, 22, 14, 12, 8, 6]
fig, ax = plt.subplots(figsize=(9, 5))
b = ax.barh(agentes[::-1], vals[::-1], color=LARANJA, alpha=0.85)
ax.bar_label(b, fmt="%.0f%%", fontsize=9, padding=3)
ax.set_title("Agente Tóxico (% das notificações)", fontsize=13, fontweight="bold")
ax.set_xlim(0, 50)
salvar(fig, "p3_agente_toxico")

# 7. Circunstância
circs = ["Tentativa suicídio", "Acidental", "Uso habitual", "Automedicação", "Violência", "Outros"]
vals  = [34, 28, 17, 11, 5, 5]
fig, ax = plt.subplots(figsize=(9, 5))
cores3 = [VERMELHO] + [LARANJA] * 5
b = ax.bar(circs, vals, color=cores3, alpha=0.85, width=0.6)
ax.bar_label(b, fmt="%.0f%%", fontsize=9, padding=3)
ax.set_title("Circunstância da Intoxicação", fontsize=13, fontweight="bold")
ax.set_ylabel("% das notificações")
plt.xticks(rotation=20, ha="right")
salvar(fig, "p3_circunstancia")


# ══════════════════════════════════════════════════════════════════════════════
# PÁGINA 4 – Hospitalizações (SIH)
# ══════════════════════════════════════════════════════════════════════════════
print("Página 4 – Hospitalizações")

# 8. Internações por ano
intern = [1800, 1950, 2100, 1900, 2200, 2050, 2400, 2600, 2450]
fig, ax = plt.subplots(figsize=(9, 5))
ax.bar(ANOS, intern, color=VERDE, alpha=0.85, width=0.6)
ax.set_title("Internações Hospitalares por Ano – Recife (mulheres)", fontsize=13, fontweight="bold")
ax.set_xlabel("Ano")
ax.set_ylabel("Internações")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
salvar(fig, "p4_internacoes_por_ano")

# 9. Capítulos CID-10
cids = ["S/T (lesões)", "Z (fatores)", "O (gravidez)", "N (geniturin.)", "F (mental)", "Outros"]
vals = [41, 18, 14, 10, 8, 9]
fig, ax = plt.subplots(figsize=(9, 5))
cores4 = [VERDE, VERDE, CINZA, CINZA, CINZA, CINZA]
b = ax.barh(cids[::-1], vals[::-1], color=cores4[::-1], alpha=0.85)
ax.bar_label(b, fmt="%.0f%%", fontsize=9, padding=3)
ax.set_title("Capítulos CID-10 mais frequentes – SIH", fontsize=13, fontweight="bold")
ax.set_xlim(0, 55)
salvar(fig, "p4_cid10")


# ══════════════════════════════════════════════════════════════════════════════
# PÁGINA 5 – Mortalidade (SIM)
# ══════════════════════════════════════════════════════════════════════════════
print("Página 5 – Mortalidade")

# 10. Óbitos por ano
obitos = [280, 295, 310, 290, 330, 315, 360, 390, 370]
fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(ANOS, obitos, marker="o", color=VERMELHO, linewidth=2.5, markersize=7)
ax.fill_between(ANOS, obitos, alpha=0.12, color=VERMELHO)
ax.set_title("Óbitos Registrados por Ano – Recife (mulheres)", fontsize=13, fontweight="bold")
ax.set_xlabel("Ano")
ax.set_ylabel("Óbitos")
ax.set_ylim(0, 450)
salvar(fig, "p5_obitos_por_ano")

# 11. Causa base
causas = ["Causas externas\n(V/W/X/Y)", "Neoplasias", "Doenças circulat.", "Gravidez/parto", "Outros"]
vals   = [28, 22, 20, 8, 22]
fig, ax = plt.subplots(figsize=(8, 5))
wedges, texts, autotexts = ax.pie(
    vals, labels=causas, autopct="%1.1f%%",
    colors=[VERMELHO, AZUL, VERDE, LARANJA, CINZA],
    startangle=140, pctdistance=0.75,
)
for t in autotexts:
    t.set_fontsize(9)
ax.set_title("Causa Básica de Óbito – SIM", fontsize=13, fontweight="bold")
salvar(fig, "p5_causa_obito")


# ══════════════════════════════════════════════════════════════════════════════
# PÁGINA 6 – Análise do Linkage
# ══════════════════════════════════════════════════════════════════════════════
print("Página 6 – Linkage")

# 12. Mulheres por nº de sistemas
sistemas = ["1 sistema", "2 sistemas", "3 sistemas", "4 sistemas", "5 sistemas"]
counts   = [4800, 2900, 1500, 600, 180]
fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.bar(sistemas, counts, color=AZUL, alpha=0.85, width=0.55)
ax.bar_label(bars, fmt="%d", fontsize=9, color=CINZA, padding=3)
ax.set_title("Mulheres Identificadas por Número de Sistemas – Linkage", fontsize=13, fontweight="bold")
ax.set_ylabel("Nº de mulheres")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
salvar(fig, "p6_mulheres_por_sistema")

# 13. Sobreposição entre sistemas (venn simplificado como barras)
sistemas2 = ["SINAN Viol.", "e-SUS APS", "SIH", "SIM", "SINAN Iexo"]
totais    = [9800, 8500, 4200, 3100, 2100]
linkados  = [6200, 5900, 2800, 1900, 1100]
x = np.arange(len(sistemas2))
w = 0.38
fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(x - w/2, totais, w, label="Total no sistema", color=CINZA, alpha=0.7)
ax.bar(x + w/2, linkados, w, label="Com linkage confirmado", color=AZUL, alpha=0.85)
ax.set_xticks(x)
ax.set_xticklabels(sistemas2)
ax.set_title("Total vs. Linkage Confirmado por Sistema", fontsize=13, fontweight="bold")
ax.set_ylabel("Nº de registros")
ax.legend()
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
salvar(fig, "p6_linkage_por_sistema")


# ══════════════════════════════════════════════════════════════════════════════
# PÁGINA 7 – Linha da Vida
# ══════════════════════════════════════════════════════════════════════════════
print("Página 7 – Linha da Vida")

# 14. Eventos por tipo ao longo do tempo (linha)
fig, ax = plt.subplots(figsize=(11, 5))
cores_lv = {"SINAN Viol.": VERMELHO, "e-SUS APS": AZUL, "SIH": VERDE, "SIM": CINZA}
base = {"SINAN Viol.": [80,95,110,105,120,100,140,160,145],
        "e-SUS APS":   [900,1050,1200,1100,1300,1250,1500,1700,1600],
        "SIH":         [200,215,230,210,250,235,280,310,295],
        "SIM":         [30,32,34,30,36,34,40,44,42]}
for nome, vals in base.items():
    ax.plot(ANOS, vals, marker="o", label=nome, linewidth=2, markersize=5, color=cores_lv[nome])
ax.set_title("Eventos Registrados por Sistema e Ano – Linha da Vida", fontsize=13, fontweight="bold")
ax.set_xlabel("Ano")
ax.set_ylabel("Nº de eventos")
ax.legend(loc="upper left")
salvar(fig, "p7_linha_vida_por_sistema")


# ══════════════════════════════════════════════════════════════════════════════
# PÁGINA 8 – Subnotificações
# ══════════════════════════════════════════════════════════════════════════════
print("Página 8 – Subnotificações")

# 15. Subnotificação por bairro (top 10)
bairros = ["Boa Viagem", "Afogados", "Imbiribeira", "Vasco da Gama",
           "Ibura", "Areias", "Pina", "Caçote", "Cohab", "Ipsep"]
notificados   = [120, 98, 87, 75, 68, 62, 58, 54, 50, 45]
subnotificados = [210, 170, 145, 130, 125, 108, 100, 92, 88, 78]
x = np.arange(len(bairros))
w = 0.38
fig, ax = plt.subplots(figsize=(12, 6))
ax.bar(x - w/2, notificados, w, label="Notificados (SINAN)", color=AZUL, alpha=0.85)
ax.bar(x + w/2, subnotificados, w, label="Estimativa subnotificados", color=VERMELHO, alpha=0.75)
ax.set_xticks(x)
ax.set_xticklabels(bairros, rotation=25, ha="right")
ax.set_title("Casos Notificados vs. Estimativa de Subnotificação – Top 10 Bairros", fontsize=13, fontweight="bold")
ax.set_ylabel("Casos")
ax.legend()
salvar(fig, "p8_subnotificacao_bairro")

# 16. Taxa de subnotificação ao longo do tempo
taxa = [2.8, 2.6, 2.4, 2.5, 2.3, 2.2, 2.0, 1.9, 2.0]
fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(ANOS, taxa, marker="o", color=VERMELHO, linewidth=2.5, markersize=7)
ax.axhline(y=2.0, color=CINZA, linestyle="--", linewidth=1, label="Meta estimada")
ax.fill_between(ANOS, taxa, 2.0, where=[t > 2.0 for t in taxa], alpha=0.15, color=VERMELHO)
ax.set_title("Taxa de Subnotificação Estimada por Ano (casos prováveis / notificados)", fontsize=13, fontweight="bold")
ax.set_xlabel("Ano")
ax.set_ylabel("Razão subnotificação")
ax.legend()
ax.set_ylim(1.5, 3.5)
salvar(fig, "p8_taxa_subnotificacao")


print(f"\nPronto! {len(os.listdir(OUT))} imagens salvas em {OUT}")
