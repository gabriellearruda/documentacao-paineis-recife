"""
Gera os PDFs relatorio_gestor.pdf e relatorio_tecnico.pdf a partir dos .md.
Usa fpdf2 (puro Python, sem dependências nativas).
"""

import re
from fpdf import FPDF, XPos, YPos

DOCS   = "C:/Users/gabri/painel-shiny-recife/docs"
IMAGENS = "C:/Users/gabri/painel-shiny-recife/docs/imagens"

# Mapeamento: palavra-chave no título H1 → arquivo de fluxograma
FLUXO_MAP = {
    "mapa":           f"{IMAGENS}/fluxo_p1_mapa.png",
    "sinan viol":     f"{IMAGENS}/fluxo_p2_sinan_viol.png",
    "intoxica":       f"{IMAGENS}/fluxo_p3_iexo.png",
    "hospitaliza":    f"{IMAGENS}/fluxo_p4_sih.png",
    "mortalidade":    f"{IMAGENS}/fluxo_p5_sim.png",
    "linkage":        f"{IMAGENS}/fluxo_p6_linkage.png",
    "linha da vida":  f"{IMAGENS}/fluxo_p7_linha_vida.png",
    "subnotifica":    f"{IMAGENS}/fluxo_p8_subnotificacoes.png",
}

# ── Cores ──────────────────────────────────────────────────────────────────
AZUL      = (18,  30, 135)   # #121E87
VERMELHO  = (255, 80,  84)   # #FF5054
CINZA_ESC = (31,  41,  55)   # #1f2937
CINZA_MED = (107, 114, 128)  # #6b7280
CINZA_CLR = (243, 244, 246)  # #f3f4f6
BRANCO    = (255, 255, 255)
PRETO     = (0,   0,   0)


# ── PDF base ───────────────────────────────────────────────────────────────
FONT_DIR = "C:/Windows/Fonts"

# Substitui simbolos Unicode que Arial nao suporta por equivalentes ASCII/latin
def sanitize(text: str) -> str:
    replacements = {
        "–": "-", "—": "-", "―": "-",
        "‘": "'", "’": "'", "“": '"', "”": '"',
        "•": "*", "‣": ">", "●": "*", "○": "o",
        "◆": "<>", "■": "[x]", "▲": "/\\",
        "✕": "[x]", "✓": "[ok]", "✔": "[ok]",
        "×": "x", "é": "e", "ê": "e", "ã": "a",
        "ç": "c", "á": "a", "í": "i", "ó": "o",
        "ú": "u", "à": "a", "õ": "o", "ü": "u",
        "ä": "a", "ö": "o", "â": "a", "ô": "o",
        "î": "i", "ù": "u", "û": "u", "è": "e",
        "ë": "e", "ï": "i", "ò": "o", "É": "E",
        "Ã": "A", "Ç": "C", "Á": "A", "Ó": "O",
        "Ú": "U", "Â": "A", "Ê": "E", "Ô": "O",
        "À": "A", "È": "E",
        "·": "*", "…": "...", " ": " ",
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    # remove qualquer outro char fora do latin-1
    return text.encode("latin-1", errors="replace").decode("latin-1")

class RelatorioPDF(FPDF):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_font("Arial", "",  f"{FONT_DIR}/arial.ttf")
        self.add_font("Arial", "B", f"{FONT_DIR}/arialbd.ttf")
        self.add_font("Arial", "I", f"{FONT_DIR}/ariali.ttf")
        self.add_font("CourierNew", "", f"{FONT_DIR}/cour.ttf")
        self.set_font("Arial", "", 10)

    def header(self):
        # barra fina no topo (exceto capa)
        if self.page_no() > 1:
            self.set_fill_color(*AZUL)
            self.rect(0, 0, 210, 3, "F")

    def footer(self):
        if self.page_no() > 1:
            self.set_y(-15)
            self.set_font("Arial", "I", 8)
            self.set_text_color(*CINZA_MED)
            self.cell(0, 10,
                      f"© Vital Strategies  ·  {self.page_no() - 1}",
                      align="C")

    # ── CAPA ────────────────────────────────────────────────────────────────
    def capa(self, titulo, subtitulo):
        self.add_page()
        # fundo azul escuro
        self.set_fill_color(*AZUL)
        self.rect(0, 0, 210, 297, "F")

        # barra vermelha decorativa
        self.set_fill_color(*VERMELHO)
        self.rect(0, 130, 210, 6, "F")

        # título
        self.set_y(85)
        self.set_font("Arial", "B", 28)
        self.set_text_color(*BRANCO)
        self.multi_cell(0, 12, sanitize(titulo), align="C")

        # subtitulo
        self.ln(14)
        self.set_font("Arial", "", 13)
        self.set_text_color(180, 190, 220)
        self.multi_cell(0, 7, sanitize(subtitulo), align="C")

    # ── Linha horizontal ────────────────────────────────────────────────────
    def hr(self, cor=None, espessura=0.3):
        cor = cor or (229, 231, 235)
        self.set_draw_color(*cor)
        self.set_line_width(espessura)
        self.ln(3)
        self.line(self.l_margin, self.get_y(),
                  self.w - self.r_margin, self.get_y())
        self.ln(4)
        self.set_line_width(0.2)

    # ── Título H1 ───────────────────────────────────────────────────────────
    def h1(self, texto):
        self.add_page()
        self.set_fill_color(*AZUL)
        self.rect(self.l_margin, self.get_y(), 4, 10, "F")
        self.set_x(self.l_margin + 7)
        self.set_font("Arial", "B", 16)
        self.set_text_color(*AZUL)
        self.multi_cell(0, 8, sanitize(texto), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_draw_color(*VERMELHO)
        self.set_line_width(0.6)
        self.line(self.l_margin, self.get_y(),
                  self.w - self.r_margin, self.get_y())
        self.set_line_width(0.2)
        self.ln(5)

    # ── Imagem de fluxograma ─────────────────────────────────────────────────
    def imagem_fluxo(self, img_path):
        import os
        if not os.path.exists(img_path):
            return
        # Largura disponível
        w = self.w - self.l_margin - self.r_margin
        # Quebra de página se não couber (~60mm de altura estimada)
        if self.get_y() + 62 > self.h - self.b_margin:
            self.add_page()
        self.ln(3)
        self.set_font("Arial", "I", 8)
        self.set_text_color(*CINZA_MED)
        self.cell(0, 5, "Fluxo de dados desta pagina:", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.image(img_path, x=self.l_margin, w=w)
        self.ln(5)
        self.set_text_color(*CINZA_ESC)

    # ── Título H2 ───────────────────────────────────────────────────────────
    def h2(self, texto):
        self.ln(4)
        self.set_fill_color(*AZUL)
        self.rect(self.l_margin, self.get_y(), 3, 7, "F")
        self.set_x(self.l_margin + 6)
        self.set_font("Arial", "B", 12)
        self.set_text_color(*CINZA_ESC)
        self.multi_cell(0, 6, sanitize(texto), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(2)

    # ── Título H3 ───────────────────────────────────────────────────────────
    def h3(self, texto):
        self.ln(3)
        self.set_font("Arial", "B", 10)
        self.set_text_color(*CINZA_ESC)
        self.multi_cell(0, 6, sanitize(texto), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(1)

    # ── Parágrafo normal ────────────────────────────────────────────────────
    def paragrafo(self, texto, bold=False):
        self.set_font("Arial", "B" if bold else "", 10)
        self.set_text_color(*CINZA_ESC)
        self.multi_cell(0, 5.5, sanitize(texto), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(1)

    # ── Item de lista ───────────────────────────────────────────────────────
    def item_lista(self, texto):
        self.set_font("Arial", "", 10)
        self.set_text_color(*CINZA_ESC)
        x0 = self.l_margin
        self.set_x(x0 + 4)
        self.cell(5, 5.5, "-")
        self.set_x(x0 + 9)
        self.multi_cell(self.w - self.r_margin - x0 - 9, 5.5,
                        sanitize(texto), new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # ── Bloco de código ─────────────────────────────────────────────────────
    def bloco_codigo(self, linhas):
        self.ln(2)
        h_linha = 4.5
        total_h = len(linhas) * h_linha + 6
        self.set_fill_color(30, 30, 46)
        self.rect(self.l_margin, self.get_y(),
                  self.w - self.l_margin - self.r_margin, total_h, "F")
        self.set_y(self.get_y() + 3)
        for linha in linhas:
            self.set_x(self.l_margin + 4)
            self.set_font("CourierNew", "", 8)
            self.set_text_color(205, 214, 244)
            self.cell(0, h_linha, sanitize(linha[:110]),
                      new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(3)
        self.set_text_color(*CINZA_ESC)

    # ── Tabela markdown ─────────────────────────────────────────────────────
    def tabela_md(self, linhas_tabela):
        linhas = [l for l in linhas_tabela
                  if l.strip() and not re.match(r"^\|[-| :]+\|$", l.strip())]
        if not linhas:
            return

        rows = []
        for l in linhas:
            cells = [c.strip() for c in l.strip().strip("|").split("|")]
            rows.append(cells)

        if not rows:
            return

        ncols = max(len(r) for r in rows)
        col_w = (self.w - self.l_margin - self.r_margin) / ncols

        for i, row in enumerate(rows):
            # quebra de página preventiva
            if self.get_y() > self.h - self.b_margin - 12:
                self.add_page()

            is_header = (i == 0)
            if is_header:
                self.set_fill_color(*AZUL)
                self.set_text_color(*BRANCO)
                self.set_font("Arial", "B", 8.5)
            else:
                bg = (249, 250, 251) if i % 2 == 0 else BRANCO
                self.set_fill_color(*bg)
                self.set_text_color(*CINZA_ESC)
                self.set_font("Arial", "", 8.5)

            row_h = 6
            for j in range(ncols):
                txt = row[j] if j < len(row) else ""
                # strip bold/italic markers
                txt = re.sub(r"\*{1,2}(.+?)\*{1,2}", r"\1", txt)
                txt = re.sub(r"`(.+?)`", r"\1", txt)
                txt = sanitize(txt)
                self.cell(col_w, row_h, txt[:60], border=0,
                          fill=True, new_x=XPos.RIGHT, new_y=YPos.TOP)
            self.ln(row_h)

        self.ln(4)


# ── Resolve imagem de fluxo para um título H1 ────────────────────────────────
def fluxo_para_titulo(titulo: str):
    t = titulo.lower()
    for chave, caminho in FLUXO_MAP.items():
        if chave in t:
            return caminho
    return None


# ── Parser de Markdown simples ─────────────────────────────────────────────
def render_md(pdf: RelatorioPDF, md_text: str, inserir_fluxo: bool = False):
    lines = md_text.splitlines()
    i = 0
    in_code = False
    code_buf = []
    table_buf = []
    secao_atual = None   # título da seção H1 em curso

    def flush_table():
        if table_buf:
            pdf.tabela_md(table_buf)
            table_buf.clear()

    def flush_fluxo():
        """Insere fluxograma ao fim da seção anterior."""
        if inserir_fluxo and secao_atual:
            img = fluxo_para_titulo(secao_atual)
            if img:
                pdf.imagem_fluxo(img)

    while i < len(lines):
        raw = lines[i]
        stripped = raw.strip()

        # bloco de código
        if stripped.startswith("```"):
            flush_table()
            if not in_code:
                in_code = True
                code_buf = []
            else:
                in_code = False
                pdf.bloco_codigo(code_buf)
                code_buf = []
            i += 1
            continue

        if in_code:
            code_buf.append(raw)
            i += 1
            continue

        # linha de tabela
        if stripped.startswith("|"):
            flush_table()
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_buf.append(lines[i])
                i += 1
            pdf.tabela_md(table_buf)
            table_buf.clear()
            continue

        # divisória
        if re.match(r"^---+$", stripped):
            flush_table()
            pdf.hr()
            i += 1
            continue

        # h1 — fecha seção anterior, abre nova
        if stripped.startswith("# "):
            flush_table()
            flush_fluxo()
            titulo_h1 = stripped[2:].strip()
            secao_atual = titulo_h1
            pdf.h1(titulo_h1)
            i += 1
            continue

        # h2
        if stripped.startswith("## "):
            flush_table()
            pdf.h2(stripped[3:].strip())
            i += 1
            continue

        # h3
        if stripped.startswith("### "):
            flush_table()
            pdf.h3(stripped[4:].strip())
            i += 1
            continue

        # h4
        if stripped.startswith("#### "):
            flush_table()
            pdf.h3(stripped[5:].strip())
            i += 1
            continue

        # lista
        if re.match(r"^[-*] ", stripped):
            flush_table()
            txt = re.sub(r"^[-*] ", "", stripped)
            txt = re.sub(r"\*{1,2}(.+?)\*{1,2}", r"\1", txt)
            txt = re.sub(r"`(.+?)`", r"\1", txt)
            pdf.item_lista(txt)
            i += 1
            continue

        # linha em branco
        if stripped == "" or stripped == "&nbsp;":
            flush_table()
            pdf.ln(2)
            i += 1
            continue

        # parágrafo normal
        flush_table()
        txt = re.sub(r"\*{1,2}(.+?)\*{1,2}", r"\1", stripped)
        txt = re.sub(r"`(.+?)`", r"\1", txt)
        if txt:
            pdf.paragrafo(txt)
        i += 1

    flush_table()
    flush_fluxo()   # insere fluxo da última seção


# ── Geração ────────────────────────────────────────────────────────────────
def gerar(md_path, pdf_path, titulo_capa, subtitulo_capa):
    with open(md_path, encoding="utf-8") as f:
        md = f.read()

    # Separa intro ("Sobre este documento" etc.) das secoes de pagina (H1)
    partes = re.split(r"(?m)^(?=# )", md, maxsplit=1)
    intro = partes[0].strip()
    secoes = partes[1] if len(partes) > 1 else ""

    pdf = RelatorioPDF(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.set_margins(20, 15, 20)

    pdf.capa(titulo_capa, subtitulo_capa)

    # Pagina branca para o intro (evita conflito com fundo azul da capa)
    if intro:
        pdf.add_page()
        render_md(pdf, intro)

    if secoes:
        render_md(pdf, secoes, inserir_fluxo=True)

    pdf.output(pdf_path)
    print(f"OK: {pdf_path}")


# ── MAIN ───────────────────────────────────────────────────────────────────
gerar(
    f"{DOCS}/relatorio_gestor.md",
    f"{DOCS}/relatorio_gestor.pdf",
    "Painéis Vigilância - Recife",
    "Guia de origem dos dados e visualizações\npara gestores e tomadores de decisão"
)

gerar(
    f"{DOCS}/relatorio_tecnico.md",
    f"{DOCS}/relatorio_tecnico.pdf",
    "Painéis Vigilância - Recife",
    "Documentação técnica de dados e variáveis\npor página do painel"
)
