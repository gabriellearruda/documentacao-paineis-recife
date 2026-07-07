"""
Gera fluxogramas de dados para cada página do Painel Recife.
Salva PNGs em docs/imagens/
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

OUT = "C:/Users/gabri/painel-shiny-recife/docs/imagens"
os.makedirs(OUT, exist_ok=True)

AZUL      = "#121E87"
VERMELHO  = "#FF5054"
CINZA     = "#6b7280"
VERDE     = "#10b981"
LARANJA   = "#f59e0b"
ROXO      = "#7c3aed"
BRANCO    = "#ffffff"
CINZA_CLR = "#f1f5f9"

def box(ax, x, y, w, h, label, cor_fundo=AZUL, cor_texto=BRANCO,
        fontsize=8.5, style="round,pad=0.1", cor_borda=None):
    cb = cor_borda or cor_fundo
    b = FancyBboxPatch((x - w/2, y - h/2), w, h,
                       boxstyle=style,
                       facecolor=cor_fundo, edgecolor=cb, linewidth=1.2)
    ax.add_patch(b)
    ax.text(x, y, label, ha="center", va="center",
            fontsize=fontsize, color=cor_texto,
            fontweight="bold", wrap=True,
            multialignment="center")

def db(ax, x, y, w, h, label, cor=AZUL):
    """Cilindro simulado com elipses."""
    from matplotlib.patches import Ellipse, Rectangle
    ax.add_patch(Rectangle((x - w/2, y - h/2), w, h,
                            facecolor=cor, edgecolor=cor, alpha=0.85))
    ax.add_patch(Ellipse((x, y + h/2), w, h * 0.25,
                          facecolor=cor, edgecolor=cor, alpha=0.85))
    ax.add_patch(Ellipse((x, y - h/2), w, h * 0.25,
                          facecolor="#0a1260", edgecolor=cor, alpha=0.9))
    ax.text(x, y, label, ha="center", va="center",
            fontsize=8, color=BRANCO, fontweight="bold", multialignment="center")

def arrow(ax, x0, y0, x1, y1, cor="#444"):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", color=cor,
                                lw=1.5, mutation_scale=14))

def titulo(ax, txt):
    ax.set_title(txt, fontsize=13, fontweight="bold", color=AZUL, pad=14)

def salvar(fig, nome):
    path = f"{OUT}/{nome}.png"
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  {nome}.png")


# ══════════════════════════════════════════════════════
# Página 1 – Mapa da Violência
# ══════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(12, 5))
ax.set_xlim(0, 12); ax.set_ylim(0, 5); ax.axis("off")
titulo(ax, "Fluxo de Dados – Página 1: Mapa da Violência")

# Fontes
db(ax, 1.2, 3.8, 1.8, 0.7, "pontos_viol\n_real.qs", AZUL)
db(ax, 1.2, 2.5, 1.8, 0.7, "bairros\n.geojson", VERDE)
db(ax, 1.2, 1.2, 1.8, 0.7, "cnes\n.RData", ROXO)

# Filtros
box(ax, 4.2, 2.5, 2.2, 0.75, "Filtros\nIdade · Raça · Ano · ID",
    CINZA_CLR, CINZA, cor_borda=CINZA)

# Mapa
box(ax, 7.2, 2.5, 2.2, 0.75, "Mapa Interativo\n(Leaflet)", AZUL)

# Outputs
box(ax, 10.3, 3.5, 2.0, 0.65, "Heatmap", VERMELHO)
box(ax, 10.3, 2.5, 2.0, 0.65, "Pontos\nIndividuais", AZUL)
box(ax, 10.3, 1.5, 2.0, 0.65, "Destaque\npor ID", LARANJA)

arrow(ax, 2.1, 3.8, 3.1, 2.8)
arrow(ax, 2.1, 2.5, 3.1, 2.5)
arrow(ax, 2.1, 1.2, 3.1, 2.2)
arrow(ax, 5.3, 2.5, 6.1, 2.5)
arrow(ax, 8.3, 2.7, 9.3, 3.5)
arrow(ax, 8.3, 2.5, 9.3, 2.5)
arrow(ax, 8.3, 2.3, 9.3, 1.5)

ax.text(0.3, 4.7, "FONTES", fontsize=9, color=CINZA, fontstyle="italic")
ax.text(3.2, 4.7, "FILTROS", fontsize=9, color=CINZA, fontstyle="italic")
ax.text(6.2, 4.7, "VISUALIZAÇÃO", fontsize=9, color=CINZA, fontstyle="italic")
ax.text(9.3, 4.7, "OUTPUTS", fontsize=9, color=CINZA, fontstyle="italic")
salvar(fig, "fluxo_p1_mapa")


# ══════════════════════════════════════════════════════
# Página 2 – SINAN Violência
# ══════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(13, 5))
ax.set_xlim(0, 13); ax.set_ylim(0, 5); ax.axis("off")
titulo(ax, "Fluxo de Dados – Página 2: SINAN Violência")

db(ax, 1.2, 2.5, 2.0, 0.7, "SINAN\nViolências\n(Ministério Saúde)", AZUL)
box(ax, 4.0, 3.2, 2.2, 0.65, "tratado_sinan\n_viol_publica", CINZA_CLR, CINZA, cor_borda=CINZA)
box(ax, 4.0, 1.8, 2.2, 0.65, "Filtros\nSexo F · Recife · Ano", CINZA_CLR, CINZA, cor_borda=CINZA)
db(ax, 7.0, 2.5, 2.0, 0.7, "sinan_viol\n.qs", AZUL)

outputs = ["Notificações\npor Ano", "Tipo de\nViolência", "Faixa\nEtária",
           "Raça/Cor", "Tabela\nDetalhada"]
ys = [4.3, 3.4, 2.5, 1.6, 0.7]
for label, y in zip(outputs, ys):
    box(ax, 10.8, y, 2.0, 0.65, label, AZUL)
    arrow(ax, 8.0, 2.5, 9.8, y)

arrow(ax, 2.2, 2.5, 2.9, 3.2)
arrow(ax, 2.2, 2.5, 2.9, 1.8)
arrow(ax, 5.1, 3.2, 5.9, 2.7)
arrow(ax, 5.1, 1.8, 5.9, 2.3)

ax.text(0.2, 4.7, "FONTE", fontsize=9, color=CINZA, fontstyle="italic")
ax.text(2.9, 4.7, "BANCO / FILTROS", fontsize=9, color=CINZA, fontstyle="italic")
ax.text(6.2, 4.7, "ARQUIVO", fontsize=9, color=CINZA, fontstyle="italic")
ax.text(9.8, 4.7, "VISUALIZAÇÕES", fontsize=9, color=CINZA, fontstyle="italic")
salvar(fig, "fluxo_p2_sinan_viol")


# ══════════════════════════════════════════════════════
# Página 3 – SINAN Intoxicação Exógena
# ══════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(13, 5))
ax.set_xlim(0, 13); ax.set_ylim(0, 5); ax.axis("off")
titulo(ax, "Fluxo de Dados – Página 3: SINAN Intoxicação Exógena")

db(ax, 1.2, 2.5, 2.0, 0.7, "SINAN\nIntoxicação\n(Ministério Saúde)", LARANJA)
box(ax, 4.0, 3.2, 2.2, 0.65, "tratado_sinan\n_iexo_publica", CINZA_CLR, CINZA, cor_borda=CINZA)
box(ax, 4.0, 1.8, 2.2, 0.65, "Filtros\nSexo F · Recife · Ano", CINZA_CLR, CINZA, cor_borda=CINZA)
db(ax, 7.0, 2.5, 2.0, 0.7, "df_iexo\n.qs", LARANJA)

outputs = ["Casos por Ano", "Agente Tóxico", "Circunstância", "Evolução/Óbito"]
ys = [3.8, 2.9, 2.0, 1.1]
for label, y in zip(outputs, ys):
    box(ax, 10.8, y, 2.0, 0.65, label, LARANJA)
    arrow(ax, 8.0, 2.5, 9.8, y)

arrow(ax, 2.2, 2.5, 2.9, 3.2)
arrow(ax, 2.2, 2.5, 2.9, 1.8)
arrow(ax, 5.1, 3.2, 5.9, 2.7)
arrow(ax, 5.1, 1.8, 5.9, 2.3)

ax.text(0.2, 4.7, "FONTE", fontsize=9, color=CINZA, fontstyle="italic")
ax.text(2.9, 4.7, "BANCO / FILTROS", fontsize=9, color=CINZA, fontstyle="italic")
ax.text(6.2, 4.7, "ARQUIVO", fontsize=9, color=CINZA, fontstyle="italic")
ax.text(9.8, 4.7, "VISUALIZAÇÕES", fontsize=9, color=CINZA, fontstyle="italic")
salvar(fig, "fluxo_p3_iexo")


# ══════════════════════════════════════════════════════
# Página 4 – Hospitalizações
# ══════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(13, 5))
ax.set_xlim(0, 13); ax.set_ylim(0, 5); ax.axis("off")
titulo(ax, "Fluxo de Dados – Página 4: Hospitalizações (SIH)")

db(ax, 1.0, 3.0, 1.8, 0.7, "SIH\n(Ministério Saúde)", VERDE)
db(ax, 1.0, 1.8, 1.8, 0.7, "cid_10\n.csv", CINZA)
box(ax, 4.0, 3.0, 2.2, 0.65, "tratado_sih\n_publica", CINZA_CLR, CINZA, cor_borda=CINZA)
box(ax, 4.0, 1.8, 2.2, 0.65, "Filtros\nSexo F · CID S/T/V-Y", CINZA_CLR, CINZA, cor_borda=CINZA)
db(ax, 7.0, 2.4, 2.0, 0.7, "df_sih\n.qs", VERDE)

outputs = ["Internações\npor Ano", "Diagnóstico\nCID-10", "Tempo de\nInternação", "Motivo\nde Saída"]
ys = [3.8, 2.9, 2.0, 1.1]
for label, y in zip(outputs, ys):
    box(ax, 10.8, y, 2.0, 0.65, label, VERDE)
    arrow(ax, 8.0, 2.4, 9.8, y)

arrow(ax, 1.9, 3.0, 2.9, 3.0)
arrow(ax, 1.9, 1.8, 2.9, 2.6)
arrow(ax, 5.1, 3.0, 5.9, 2.6)
arrow(ax, 5.1, 1.8, 5.9, 2.2)

ax.text(0.2, 4.7, "FONTES", fontsize=9, color=CINZA, fontstyle="italic")
ax.text(2.9, 4.7, "BANCO / FILTROS", fontsize=9, color=CINZA, fontstyle="italic")
ax.text(6.2, 4.7, "ARQUIVO", fontsize=9, color=CINZA, fontstyle="italic")
ax.text(9.8, 4.7, "VISUALIZAÇÕES", fontsize=9, color=CINZA, fontstyle="italic")
salvar(fig, "fluxo_p4_sih")


# ══════════════════════════════════════════════════════
# Página 5 – Mortalidade
# ══════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(13, 5))
ax.set_xlim(0, 13); ax.set_ylim(0, 5); ax.axis("off")
titulo(ax, "Fluxo de Dados – Página 5: Mortalidade (SIM)")

db(ax, 1.0, 3.0, 1.8, 0.7, "SIM\n(Ministério Saúde)", VERMELHO)
db(ax, 1.0, 1.8, 1.8, 0.7, "cid_10\n.csv", CINZA)
box(ax, 4.0, 3.0, 2.2, 0.65, "tratado_sim\n_publica", CINZA_CLR, CINZA, cor_borda=CINZA)
box(ax, 4.0, 1.8, 2.2, 0.65, "Filtros\nSexo F · Recife · Ano", CINZA_CLR, CINZA, cor_borda=CINZA)
db(ax, 7.0, 2.4, 2.0, 0.7, "df_sim\n.qs", VERMELHO)

outputs = ["Óbitos\npor Ano", "Causa Básica\nCID-10", "Óbito em\nGravidez", "Local\ndo Óbito"]
ys = [3.8, 2.9, 2.0, 1.1]
for label, y in zip(outputs, ys):
    box(ax, 10.8, y, 2.0, 0.65, label, VERMELHO)
    arrow(ax, 8.0, 2.4, 9.8, y)

arrow(ax, 1.9, 3.0, 2.9, 3.0)
arrow(ax, 1.9, 1.8, 2.9, 2.6)
arrow(ax, 5.1, 3.0, 5.9, 2.6)
arrow(ax, 5.1, 1.8, 5.9, 2.2)

ax.text(0.2, 4.7, "FONTES", fontsize=9, color=CINZA, fontstyle="italic")
ax.text(2.9, 4.7, "BANCO / FILTROS", fontsize=9, color=CINZA, fontstyle="italic")
ax.text(6.2, 4.7, "ARQUIVO", fontsize=9, color=CINZA, fontstyle="italic")
ax.text(9.8, 4.7, "VISUALIZAÇÕES", fontsize=9, color=CINZA, fontstyle="italic")
salvar(fig, "fluxo_p5_sim")


# ══════════════════════════════════════════════════════
# Página 6 – Linkage
# ══════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(13, 6))
ax.set_xlim(0, 13); ax.set_ylim(0, 6); ax.axis("off")
titulo(ax, "Fluxo de Dados – Página 6: Análise do Linkage")

sistemas = [("SINAN\nViolência", 5.0, AZUL),
            ("SINAN\nIntoxicação", 4.1, LARANJA),
            ("SIH", 3.2, VERDE),
            ("SIM", 2.3, VERMELHO),
            ("e-SUS APS", 1.4, ROXO)]
for label, y, cor in sistemas:
    db(ax, 1.2, y, 1.8, 0.6, label, cor)
    arrow(ax, 2.1, y, 3.8, 3.2)

box(ax, 4.8, 3.2, 2.2, 0.8, "Linkage\nProbabilístico", AZUL)

db(ax, 7.8, 4.0, 2.2, 0.7, "linkage\n_compilado\n.RData", AZUL)
db(ax, 7.8, 2.4, 2.2, 0.7, "base_linkage\n_feminino\n.RData", AZUL)

arrow(ax, 5.9, 3.5, 6.7, 4.0)
arrow(ax, 5.9, 2.9, 6.7, 2.4)

outputs_a = ["Sobreposição\nentre Sistemas", "Pares\nConfirmados"]
outputs_b = ["Mulheres por\nNº de Sistemas", "Distribuição\npor Bairro"]
for i, label in enumerate(outputs_a):
    box(ax, 11.2, 4.5 - i*0.8, 2.2, 0.6, label, AZUL)
    arrow(ax, 8.9, 4.0, 10.1, 4.5 - i*0.8)
for i, label in enumerate(outputs_b):
    box(ax, 11.2, 2.8 - i*0.8, 2.2, 0.6, label, AZUL)
    arrow(ax, 8.9, 2.4, 10.1, 2.8 - i*0.8)

ax.text(0.2, 5.7, "FONTES (5 sistemas)", fontsize=9, color=CINZA, fontstyle="italic")
ax.text(3.7, 5.7, "PROCESSO", fontsize=9, color=CINZA, fontstyle="italic")
ax.text(6.8, 5.7, "ARQUIVOS", fontsize=9, color=CINZA, fontstyle="italic")
ax.text(10.1, 5.7, "VISUALIZAÇÕES", fontsize=9, color=CINZA, fontstyle="italic")
salvar(fig, "fluxo_p6_linkage")


# ══════════════════════════════════════════════════════
# Página 7 – Linha da Vida
# ══════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(13, 6))
ax.set_xlim(0, 13); ax.set_ylim(0, 6); ax.axis("off")
titulo(ax, "Fluxo de Dados – Página 7: Linha da Vida")

sistemas = [("sinan_viol.qs", 5.0, AZUL),
            ("df_sih.qs", 4.1, VERDE),
            ("df_sim.qs", 3.2, VERMELHO),
            ("e-SUS APS", 2.3, ROXO)]
for label, y, cor in sistemas:
    db(ax, 1.3, y, 1.8, 0.6, label, cor)
    arrow(ax, 2.2, y, 3.8, 3.6)

box(ax, 4.9, 3.6, 2.2, 0.75, "registro_linkage\n(todos os eventos\npor pessoa)", AZUL)
arrow(ax, 6.0, 3.6, 7.0, 3.6)
db(ax, 8.0, 3.6, 2.2, 0.7, "linha_vida\n_esus4.qs", AZUL)
arrow(ax, 9.1, 3.6, 10.0, 3.6)
box(ax, 10.9, 4.2, 2.2, 0.65, "Filtro\npor ID Pessoa", CINZA_CLR, CINZA, cor_borda=CINZA)
arrow(ax, 10.9, 3.85, 10.9, 3.3)
box(ax, 10.9, 2.9, 2.2, 0.65, "Timeline de\nEventos", AZUL)

ax.text(0.2, 5.7, "ARQUIVOS", fontsize=9, color=CINZA, fontstyle="italic")
ax.text(3.8, 5.7, "LINKAGE", fontsize=9, color=CINZA, fontstyle="italic")
ax.text(7.0, 5.7, "ARQUIVO", fontsize=9, color=CINZA, fontstyle="italic")
ax.text(10.0, 5.7, "VISUALIZAÇÃO", fontsize=9, color=CINZA, fontstyle="italic")
salvar(fig, "fluxo_p7_linha_vida")


# ══════════════════════════════════════════════════════
# Página 8 – Subnotificações
# ══════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(13, 5))
ax.set_xlim(0, 13); ax.set_ylim(0, 5); ax.axis("off")
titulo(ax, "Fluxo de Dados – Página 8: Subnotificações")

db(ax, 1.2, 3.5, 2.0, 0.7, "e-SUS APS\ntratado_esus_aps", ROXO)
db(ax, 1.2, 1.8, 2.0, 0.7, "sinan_viol.qs\n(notificações)", AZUL)

box(ax, 4.2, 3.5, 2.2, 0.65, "Usuárias por\nBairro e UBS", CINZA_CLR, CINZA, cor_borda=CINZA)
box(ax, 4.2, 1.8, 2.2, 0.65, "Notificações por\nBairro e UBS", CINZA_CLR, CINZA, cor_borda=CINZA)

box(ax, 7.0, 2.65, 2.2, 0.75, "Modelo de\nSubnotificação", AZUL)

db(ax, 10.0, 3.5, 2.2, 0.7, "dados_modelo\n_bairro.qs", ROXO)
db(ax, 10.0, 1.8, 2.2, 0.7, "dados_modelo\n_ubs.qs", AZUL)

box(ax, 12.3, 3.5, 1.6, 0.65, "Tabela\npor Bairro", ROXO)
box(ax, 12.3, 1.8, 1.6, 0.65, "Tabela\npor UBS", AZUL)

arrow(ax, 2.2, 3.5, 3.1, 3.5)
arrow(ax, 2.2, 1.8, 3.1, 1.8)
arrow(ax, 5.3, 3.5, 5.9, 3.0)
arrow(ax, 5.3, 1.8, 5.9, 2.3)
arrow(ax, 8.1, 3.0, 8.9, 3.5)
arrow(ax, 8.1, 2.3, 8.9, 1.8)
arrow(ax, 11.1, 3.5, 11.5, 3.5)
arrow(ax, 11.1, 1.8, 11.5, 1.8)

ax.text(0.2, 4.7, "FONTES", fontsize=9, color=CINZA, fontstyle="italic")
ax.text(3.1, 4.7, "AGREGAÇÃO", fontsize=9, color=CINZA, fontstyle="italic")
ax.text(6.1, 4.7, "MODELO", fontsize=9, color=CINZA, fontstyle="italic")
ax.text(9.0, 4.7, "ARQUIVOS", fontsize=9, color=CINZA, fontstyle="italic")
ax.text(11.5, 4.7, "SAÍDA", fontsize=9, color=CINZA, fontstyle="italic")
salvar(fig, "fluxo_p8_subnotificacoes")


print(f"\nPronto! Fluxogramas salvos em {OUT}")
