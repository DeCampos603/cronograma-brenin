# -*- coding: utf-8 -*-
"""
Cronograma de estudos do Brenin — ESA + EAM, ciclo 2026/2027.  Versão 2.
Curso preparatório de segunda a sexta, 08h–12h.
Paleta validada em validate_palette.py / paleta_final.py (codificação por família de prova).
"""
import datetime as _dt
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.worksheet.hyperlink import Hyperlink
from openpyxl.formatting.rule import CellIsRule, FormulaRule, DataBarRule, IconSetRule
from openpyxl.chart import BarChart, Reference

OUT = r"G:\Meu Drive\REPO\Cronograma_Brenin_ESA_EAM.xlsx"
FT = "Segoe UI"          # fonte de sistema do Windows/Office — legível em corpo pequeno

# ══════════════════════════════════════════════════ TOKENS DE DESIGN
CANVAS = "F4F5F7"; CARD = "FFFFFF"; LINE = "E2E5EA"; LINE2 = "CFD5DD"
INK = "11161D"; INK2 = "5A6673"; INK3 = "97A1AD"
NAVY = "0E2038"; NAVY2 = "1C3A5E"; NAVY3 = "35597F"; NAVY_T = "D8DFE8"
GOLD = "C8952A"
OK_BG, OK_FG = "E3F2E8", "1E6B3A"
BAD_BG, BAD_FG = "FBE7E4", "A32A1C"
NEU_BG, NEU_FG = "EEF0F3", "6B7684"
INPUT_BG, INPUT_FG = "FFFBEA", "8A6212"

# família de prova → (âncora, rótulo)
FAM = {
    "AMBAS": ("1A51BD", "Cai nas DUAS provas"),
    "EAM":   ("0C7E65", "Só EAM — Marinha"),
    "ESA":   ("7B5400", "Só ESA — Exército"),
}
# matéria → (família, barra, tinta clara, tinta média, tinta escura p/ texto)
SUB = {
    "Matemática": ("AMBAS", "1A51BD", "E8EEF8", "D1DCF2", "0244BE"),
    "Português":  ("AMBAS", "487CDE", "EDF2FC", "DAE5F8", "1148B3"),
    "Inglês":     ("AMBAS", "719DEF", "F1F5FD", "E3EBFC", "204CA4"),
    "Física":     ("EAM",   "0C7E65", "E7F2F0", "CEE5E0", "01614D"),
    "Química":    ("EAM",   "0DB28F", "E7F7F4", "CFF0E9", "01614D"),
    "História":   ("ESA",   "7B5400", "F2EEE6", "E5DDCC", "6D4B04"),
    "Geografia":  ("ESA",   "9F6E00", "F5F0E6", "ECE2CC", "6D4B04"),
    "Literatura": ("ESA",   "C48800", "F9F3E6", "F3E7CC", "6D4B04"),
    "Redação":    ("ESA",   "E5A424", "FCF6E9", "FAEDD3", "6D4B04"),
}
ORDEM = ["Matemática", "Português", "Inglês", "Física", "Química",
         "História", "Geografia", "Literatura", "Redação"]

# blocos estruturais (neutros — cor só carrega identidade de matéria)
T_CURSO  = (NAVY,   "FFFFFF")
T_SIM    = (NAVY_T, NAVY2)
T_REV    = ("EDF0F4", NAVY2)
T_MEAL   = ("F0F1F4", INK2)
T_REST   = (CANVAS,  INK3)
T_TREINO = ("FBE7E4", "A32A1C")
T_FREE   = ("F7F8FA", INK3)
T_SLEEP  = ("E9EBEF", INK3)

hair = Side(style="thin", color=LINE)
B_ALL = Border(left=hair, right=hair, top=hair, bottom=hair)


def st(c, *, b=False, i=False, sz=9.5, fg=INK, bg=None, ha="left", va="center",
       wrap=False, bd=True, fmt=None, ul=None):
    c.font = Font(name=FT, bold=b, italic=i, size=sz, color=fg, underline=ul)
    if bg:
        c.fill = PatternFill("solid", fgColor=bg)
    c.alignment = Alignment(horizontal=ha, vertical=va, wrap_text=wrap)
    if bd:
        c.border = B_ALL
    if fmt:
        c.number_format = fmt
    return c


def mg(ws, r1, c1, r2, c2):
    if (r1, c1) != (r2, c2):
        ws.merge_cells(start_row=r1, start_column=c1, end_row=r2, end_column=c2)


def band(ws, r, ncols, txt, sub=None, bg=NAVY, h=34):
    """faixa-título com filete dourado embaixo; a última coluna fica livre para o link de índice"""
    mg(ws, r, 1, r, ncols - 1)
    st(ws.cell(r, 1, txt), b=True, sz=15, fg="FFFFFF", bg=bg, ha="left", bd=False)
    st(ws.cell(r, ncols, None), bg=bg, bd=False)
    ws.row_dimensions[r].height = h
    if sub:
        mg(ws, r + 1, 1, r + 1, ncols)
        st(ws.cell(r + 1, 1, sub), sz=9, fg="C7D2DF", bg=bg, ha="left", bd=False)
        ws.row_dimensions[r + 1].height = 17
        r += 1
    for j in range(1, ncols + 1):
        st(ws.cell(r + 1, j, None), bg=GOLD, bd=False)
    ws.row_dimensions[r + 1].height = 3
    return r + 2


def sec(ws, r, ncols, txt, nota=None):
    """cabeçalho de seção"""
    mg(ws, r, 1, r, ncols)
    st(ws.cell(r, 1, txt), b=True, sz=11, fg=NAVY, bg=CANVAS, ha="left", bd=False)
    ws.row_dimensions[r].height = 26
    if nota:
        mg(ws, r + 1, 1, r + 1, ncols)
        st(ws.cell(r + 1, 1, nota), sz=8.5, i=True, fg=INK2, bg=CANVAS, ha="left", bd=False, wrap=True)
        ws.row_dimensions[r + 1].height = 15
        return r + 2
    return r + 1


def thead(ws, r, hs, ws_=None, h=26, bg=NAVY2):
    for j, t in enumerate(hs, 1):
        st(ws.cell(r, j, t), b=True, sz=8.5, fg="FFFFFF", bg=bg, ha="center", wrap=True)
    ws.row_dimensions[r].height = h
    if ws_:
        for j, w in enumerate(ws_, 1):
            ws.column_dimensions[get_column_letter(j)].width = w
    return r + 1


def back(ws, ncols):
    """link de volta ao índice, no canto direito da faixa-título"""
    c = ws.cell(1, ncols)
    c.value = "◀  ÍNDICE"
    c.hyperlink = Hyperlink(ref=c.coordinate, location="'INÍCIO'!A1")
    st(c, b=True, sz=9, fg="9FB4CC", bg=NAVY, ha="right", bd=False)


def finish(ws, ncols, zoom=90):
    """pinta o canvas em tudo que ficou sem preenchimento e ajusta a visualização"""
    mr = max(ws.max_row + 4, 12)
    for rr in range(1, mr + 1):
        for cc in range(1, ncols + 3):
            c = ws.cell(rr, cc)
            if c.fill is None or c.fill.patternType is None:
                c.fill = PatternFill("solid", fgColor=CANVAS)
    ws.sheet_view.showGridLines = False
    ws.sheet_view.zoomScale = zoom
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True


wb = Workbook()

# ═══════════════════════════════════════════════════════ 1 · INÍCIO
ws = wb.active
ws.title = "INÍCIO"
ws.sheet_properties.tabColor = NAVY
NC = 12
for j, w in enumerate([2.5, 20, 17, 15, 15, 15, 3, 20, 17, 15, 15, 15], 1):
    ws.column_dimensions[get_column_letter(j)].width = w

r = band(ws, 1, NC, "  PLANO DE ESTUDOS DO BRENIN   ·   ESA + EAM",
         "  Curso preparatório de segunda a sexta, 08h–12h  ·  estudo próprio à tarde e à noite  ·  domingo de descanso")
back(ws, NC)
r += 1

# ---- índice navegável (cartões) ----
r = sec(ws, r, NC, "  ONDE FICA CADA COISA", "  Clique no cartão para ir direto à aba.")
CARDS = [
    ("PAINEL", "📊", "Contagem regressiva, progresso e desempenho", "Só olhar"),
    ("GRADE SEMANAL", "🗓", "Seu horário fixo, hora a hora, dos 7 dias", "Todo dia"),
    ("PLANO MENSAL", "📅", "Que assunto estudar em cada mês, ago/26 a jul/27", "Início do mês"),
    ("CONTEÚDO E REVISÃO", "✅", "198 tópicos das duas provas + revisão espaçada", "A cada tópico"),
    ("CONTROLE SEMANAL", "📈", "As 52 semanas: horas, questões, acertos", "Sábado à noite"),
    ("SIMULADOS", "📝", "Nota por matéria em cada simulado", "Todo sábado"),
    ("REDAÇÕES", "✍", "Tema, nota e erros. A ESA elimina abaixo de 5,0", "Quarta e sábado"),
    ("TAF", "🏃", "Corrida, natação, barra e abdominais vs. meta", "A cada treino"),
    ("PLANO SEM CURSO", "☀", "Versão de férias/recesso, com a manhã livre", "Quando não há aula"),
]
r0 = r
for i, (aba, ic, desc, freq) in enumerate(CARDS):
    lin_ = r0 + (i // 2) * 3
    col = 2 if i % 2 == 0 else 8
    fam_bg = CARD
    # ícone + título (com hyperlink)
    st(ws.cell(lin_, col, ic), sz=14, ha="center", bg=fam_bg, bd=False)
    mg(ws, lin_, col + 1, lin_, col + 4)
    c = ws.cell(lin_, col + 1, aba)
    c.hyperlink = Hyperlink(ref=c.coordinate, location=f"'{aba}'!A1")
    st(c, b=True, sz=11, fg=NAVY2, bg=fam_bg, ul="single", bd=False)
    ws.row_dimensions[lin_].height = 20
    # descrição
    st(ws.cell(lin_ + 1, col, None), bg=fam_bg, bd=False)
    mg(ws, lin_ + 1, col + 1, lin_ + 1, col + 4)
    st(ws.cell(lin_ + 1, col + 1, desc), sz=8.5, fg=INK2, bg=fam_bg, bd=False, wrap=True)
    ws.row_dimensions[lin_ + 1].height = 15
    # frequência
    st(ws.cell(lin_ + 2, col, None), bg=fam_bg, bd=False)
    mg(ws, lin_ + 2, col + 1, lin_ + 2, col + 4)
    st(ws.cell(lin_ + 2, col + 1, "↻  " + freq), sz=8, i=True, fg=INK3, bg=fam_bg, bd=False)
    ws.row_dimensions[lin_ + 2].height = 14
r = r0 + ((len(CARDS) + 1) // 2) * 3 + 1

# ---- o dia do Brenin ----
r = sec(ws, r, NC, "  O DIA DO BRENIN, EM QUATRO PARTES",
        "  Detalhe hora a hora na aba GRADE SEMANAL.")
DIA = [
    ("🎓", "08h00 – 12h00", "CURSO PREPARATÓRIO", "4 h", "Segunda a sexta. É a sua base — chegar sem sono é metade do resultado.", NAVY, "FFFFFF"),
    ("🔁", "12h00 – 13h00", "REVISÃO DA AULA DO DIA", "1 h", "A hora mais valiosa do dia: reescrever o resumo da aula enquanto está fresco.", "EDF0F4", NAVY2),
    ("📚", "14h15 – 17h00", "ESTUDO PRÓPRIO — TARDE", "2 h 30", "Dois blocos: uma matéria pesada e uma matéria de leitura.", "E8EEF8", "0244BE"),
    ("📖", "19h40 – 22h00", "ESTUDO PRÓPRIO — NOITE", "2 h 05", "Um bloco de 90 min mais 35 min de caderno de erros.", "E8EEF8", "0244BE"),
]
for ic, hor, tit, dur, txt, bg, fg in DIA:
    st(ws.cell(r, 2, ic), sz=13, ha="center", bg=bg, fg=fg)
    st(ws.cell(r, 3, hor), b=True, sz=9.5, ha="center", bg=bg, fg=fg)
    mg(ws, r, 4, r, 5)
    st(ws.cell(r, 4, tit), b=True, sz=9.5, bg=bg, fg=fg)
    st(ws.cell(r, 6, dur), sz=9, ha="center", bg=bg, fg=fg)
    mg(ws, r, 8, r, 12)
    st(ws.cell(r, 8, txt), sz=8.5, fg=INK2, bg=CARD, wrap=True)
    ws.row_dimensions[r].height = 24
    r += 1
mg(ws, r, 2, r, 12)
st(ws.cell(r, 2, "Somando tudo: 20 h de curso + 33 h de estudo próprio = 53 h por semana.  "
                 "Refeições fixas às 13h, 17h e 22h.  Treino físico às 17h40.  Domingo é descanso total."),
   sz=8.5, i=True, fg=INK2, bg=CARD)
ws.row_dimensions[r].height = 20
r += 2

# ---- datas-alvo ----
r = sec(ws, r, NC, "  DATAS-ALVO", "  As células claras são suas — corrija quando os editais oficiais saírem.")
mg(ws, r, 2, r, 4); st(ws.cell(r, 2, "Marco"), b=True, sz=8.5, fg="FFFFFF", bg=NAVY2)
st(ws.cell(r, 5, "Data"), b=True, sz=8.5, fg="FFFFFF", bg=NAVY2, ha="center")
mg(ws, r, 6, r, 8); st(ws.cell(r, 6, "Faltam"), b=True, sz=8.5, fg="FFFFFF", bg=NAVY2, ha="center")
mg(ws, r, 9, r, 12); st(ws.cell(r, 9, "O que fazer"), b=True, sz=8.5, fg="FFFFFF", bg=NAVY2)
ws.row_dimensions[r].height = 20
r += 1
MARCOS = [
    ("Início deste plano", _dt.date(2026, 8, 3), None, "Montar a rotina e não quebrar nas 4 primeiras semanas."),
    ("Edital da EAM 2027 (previsto)", _dt.date(2027, 1, 20), None, "Conferir o conteúdo oficial e ajustar esta planilha."),
    ("Inscrição na EAM (previsto)", _dt.date(2027, 2, 1), None, "Inscrever-se no primeiro dia. Não deixar para depois."),
    ("PROVA DA EAM (previsto)", _dt.date(2027, 4, 25), "EAM", "Último domingo de abril. 50 questões em 4 horas."),
    ("Edital da ESA 2028 (previsto)", _dt.date(2027, 3, 20), None, "Conferir e ajustar."),
    ("Inscrição na ESA (previsto)", _dt.date(2027, 5, 5), None, "Inscrever-se assim que abrir."),
    ("PROVA DA ESA (previsto)", _dt.date(2027, 7, 25), "ESA", "Último domingo de julho. 50 questões + redação eliminatória."),
]
L_EAM = L_ESA = None
for nome, data, tag, acao in MARCOS:
    bg = CARD if not tag else ("E7F2F0" if tag == "EAM" else "F2EEE6")
    fg = INK if not tag else ("01614D" if tag == "EAM" else "6D4B04")
    mg(ws, r, 2, r, 4)
    st(ws.cell(r, 2, nome), b=bool(tag), sz=9, bg=bg, fg=fg)
    st(ws.cell(r, 5, data), b=True, sz=9, ha="center", bg=INPUT_BG, fg=INPUT_FG, fmt="DD/MM/YYYY")
    mg(ws, r, 6, r, 8)
    st(ws.cell(r, 6, f'=IF(E{r}<TODAY(),"—  já passou",TEXT(E{r}-TODAY(),"0")&" dias")'),
       b=bool(tag), sz=9, ha="center", bg=bg, fg=fg)
    mg(ws, r, 9, r, 12)
    st(ws.cell(r, 9, acao), sz=8.5, fg=INK2, bg=CARD, wrap=True)
    ws.row_dimensions[r].height = 19
    if tag == "EAM": L_EAM = r
    if tag == "ESA": L_ESA = r
    r += 1
mg(ws, r, 2, r, 12)
st(ws.cell(r, 2, "As datas de 2027 são projeções pelo padrão histórico dos editais (EAM em abril, ESA no último domingo de julho). "
                 "Confirme no edital oficial — todo o painel se reajusta sozinho quando você corrigir aqui."),
   sz=8, i=True, fg=INK3, bg=CANVAS, bd=False, wrap=True)
ws.row_dimensions[r].height = 22
r += 2

# ---- as duas provas ----
r = sec(ws, r, NC, "  AS DUAS PROVAS, LADO A LADO",
        "  A cor de cada matéria nesta planilha diz para qual prova ela serve.")
mg(ws, r, 2, r, 3); st(ws.cell(r, 2, "Matéria"), b=True, sz=8.5, fg="FFFFFF", bg=NAVY2)
for j, t in zip(range(4, 9), ["EAM\nquestões", "ESA\nquestões", "Peso\nsomado", "Horas/sem.\nde estudo próprio", "Serve para"]):
    st(ws.cell(r, j, t), b=True, sz=8, fg="FFFFFF", bg=NAVY2, ha="center", wrap=True)
mg(ws, r, 9, r, 12); st(ws.cell(r, 9, "Por que esse peso"), b=True, sz=8.5, fg="FFFFFF", bg=NAVY2)
ws.row_dimensions[r].height = 30
r += 1
PROVAS = [
    ("Matemática", 15, 14, 4.5,  "Maior peso somado das duas provas. É a matéria que mais decide."),
    ("Português",  15, 14, 3.0,  "Empatada em peso com Matemática. O curso já cobre parte — aqui você aprofunda."),
    ("Física",      8,  0, 3.0,  "Só EAM. Sai da grade em maio, depois da prova da Marinha."),
    ("Química",     7,  0, 2.5,  "Só EAM. Sai da grade em maio."),
    ("História",    0,  6, 1.0,  "Só ESA. Ganha o dobro de tempo a partir de maio."),
    ("Geografia",   0,  6, 1.0,  "Só ESA. Ganha o dobro de tempo a partir de maio."),
    ("Literatura",  0, "*", 1.0, "Só ESA — parte das 14 questões de Português."),
    ("Redação",     0, "E", 1.5, "Só ESA e ELIMINATÓRIA: nota abaixo de 5,0 reprova, por melhor que seja o resto."),
    ("Inglês",      5, 10, 1.0,  "Não estava na sua lista, mas vale 10 das 50 questões da ESA — 20% da prova."),
]
p0 = r
for m, eam, esa, hs, pq in PROVAS:
    fam, bar, t1, t2, ink = SUB[m]
    mg(ws, r, 2, r, 3)
    st(ws.cell(r, 2, m), b=True, sz=9, fg=ink, bg=t1)
    st(ws.cell(r, 4, eam if eam else "—"), sz=9, ha="center", bg=CARD, fg=INK if eam else INK3)
    st(ws.cell(r, 5, esa if esa else "—"), sz=9, ha="center", bg=CARD, fg=INK if esa else INK3)
    tot = (eam if isinstance(eam, int) else 0) + (esa if isinstance(esa, int) else 0)
    st(ws.cell(r, 6, tot if tot else "—"), b=True, sz=9, ha="center", bg=CARD)
    st(ws.cell(r, 7, hs), sz=9, ha="center", bg=CARD, fmt='0.0" h"')
    st(ws.cell(r, 8, FAM[fam][1]), b=True, sz=7.5, ha="center", bg=t2, fg=ink, wrap=True)
    mg(ws, r, 9, r, 12)
    st(ws.cell(r, 9, pq), sz=8.5, fg=INK2, bg=CARD, wrap=True)
    ws.row_dimensions[r].height = 22
    r += 1
mg(ws, r, 2, r, 3); st(ws.cell(r, 2, "TOTAL"), b=True, sz=9, fg="FFFFFF", bg=NAVY)
st(ws.cell(r, 4, f"=SUM(D{p0}:D{r-1})"), b=True, sz=9, ha="center", bg=NEU_BG)
st(ws.cell(r, 5, f"=SUM(E{p0}:E{r-1})"), b=True, sz=9, ha="center", bg=NEU_BG)
st(ws.cell(r, 6, f"=SUM(F{p0}:F{r-1})"), b=True, sz=9, ha="center", bg=NEU_BG)
st(ws.cell(r, 7, f"=SUM(G{p0}:G{r-1})"), b=True, sz=9, ha="center", bg=NEU_BG, fmt='0.0" h"')
mg(ws, r, 8, r, 12)
st(ws.cell(r, 8, "50 questões em cada prova.  * Literatura está dentro das 14 de Português da ESA.  E = eliminatória."),
   sz=8, i=True, fg=INK2, bg=NEU_BG)
r += 2

# ---- avisos ----
r = sec(ws, r, NC, "  QUATRO COISAS QUE PODEM CUSTAR A VAGA")
AVISOS = [
    ("A redação da ESA elimina sozinha.",
     "Nota abaixo de 5,0 reprova, não importa quanto você acerte nas 50 questões. São 1h30 por semana na grade "
     "(quarta à noite e sábado à tarde) e a aba REDAÇÕES pinta de vermelho qualquer nota abaixo de 5."),
    ("O TAF elimina tanto quanto a prova escrita.",
     "A EAM exige nadar 50 m em até 1min30s e correr 2.400 m em até 14min30s. Treino todo dia às 17h40 e TAF completo "
     "cronometrado aos sábados. Se você não nada, comece esta semana — é o item mais lento de treinar."),
    ("Inglês vale 20% da prova da ESA.",
     "São 10 das 50 questões — mais que História e Geografia juntas em algumas edições. Não estava na sua lista; "
     "reservei 1h por semana (quinta, 16h). Cortar isso é abrir mão de 20% da nota."),
    ("A revisão das 12h vale mais que qualquer bloco da noite.",
     "Reescrever o resumo da aula do curso enquanto ela ainda está fresca é o que transforma 4 horas assistidas em "
     "4 horas aprendidas. É a única hora do dia que não pode ser trocada por nada."),
]
for t, d in AVISOS:
    st(ws.cell(r, 2, "!"), b=True, sz=12, fg=BAD_FG, bg=BAD_BG, ha="center")
    mg(ws, r, 3, r, 12)
    st(ws.cell(r, 3, t), b=True, sz=9.5, fg=BAD_FG, bg=BAD_BG)
    ws.row_dimensions[r].height = 20
    r += 1
    st(ws.cell(r, 2, None), bg=CARD)
    mg(ws, r, 3, r, 12)
    st(ws.cell(r, 3, d), sz=8.5, fg=INK2, bg=CARD, wrap=True, va="top")
    ws.row_dimensions[r].height = 30
    r += 1
r += 1

# ---- legenda ----
r = sec(ws, r, NC, "  LEGENDA DE CORES",
        "  A cor diz para qual prova a matéria serve; o tom, qual matéria é. Verde, vermelho e cinza são reservados a situação — nunca a matéria.")
for i, m in enumerate(ORDEM):
    fam, bar, t1, t2, ink = SUB[m]
    cc = 2 + (i // 3) * 4
    rr = r + (i % 3)
    st(ws.cell(rr, cc, None), bg=bar)
    ws.column_dimensions[get_column_letter(cc)].width = 2.5 if cc != 2 else 20
    mg(ws, rr, cc + 1, rr, cc + 2)
    st(ws.cell(rr, cc + 1, m), b=True, sz=9, fg=ink, bg=t1)
    st(ws.cell(rr, cc + 3, FAM[fam][1]), sz=7.5, fg=INK2, bg=CARD, ha="center", wrap=True)
    ws.row_dimensions[rr].height = 17
r += 4
LEG2 = [("Curso preparatório", NAVY, "FFFFFF"), ("Revisão / simulado", "EDF0F4", NAVY2),
        ("Refeição", "F0F1F4", INK2), ("Intervalo / descanso", CANVAS, INK3),
        ("Treino físico", "FBE7E4", "A32A1C"), ("Sono", "E9EBEF", INK3),
        ("Feito / no prazo", OK_BG, OK_FG), ("Atrasado / crítico", BAD_BG, BAD_FG),
        ("Célula que você preenche", INPUT_BG, INPUT_FG)]
for i, (nome, bg, fg) in enumerate(LEG2):
    cc = 2 + (i // 3) * 4
    rr = r + (i % 3)
    st(ws.cell(rr, cc, None), bg=bg)
    mg(ws, rr, cc + 1, rr, cc + 3)
    st(ws.cell(rr, cc + 1, nome), sz=8.5, fg=fg, bg=bg)
    ws.row_dimensions[rr].height = 16
r += 4
mg(ws, r, 2, r, 12)
st(ws.cell(r, 2, "Paleta verificada por cálculo (separação sob daltonismo protan/deutan, faixa de luminosidade, piso de croma e contraste), "
                 "não escolhida no olho. Todo bloco colorido também traz o nome da matéria escrito — a cor nunca é a única pista."),
   sz=8, i=True, fg=INK3, bg=CANVAS, bd=False, wrap=True)
ws.row_dimensions[r].height = 24

ws.freeze_panes = "A4"
finish(ws, NC, 100)
INICIO_EAM, INICIO_ESA = L_EAM, L_ESA

# ═══════════════════════════════════════════════════════ 2 · PAINEL
wp = wb.create_sheet("PAINEL")
wp.sheet_properties.tabColor = NAVY2
NC = 12
for j, w in enumerate([2.5, 19, 11, 11, 11, 3, 19, 11, 11, 11, 11, 14], 1):
    wp.column_dimensions[get_column_letter(j)].width = w
r = band(wp, 1, NC, "  PAINEL DE CONTROLE",
         "  Tudo aqui se calcula sozinho a partir das outras abas. Não digite nada nesta aba.")
back(wp, NC)
r += 1

r = sec(wp, r, NC, "  QUANTO FALTA")
for i, (nome, ref, cor, tin) in enumerate([
        ("PROVA DA EAM  ·  Marinha", f"INÍCIO!E{INICIO_EAM}", "0C7E65", "E7F2F0"),
        ("PROVA DA ESA  ·  Exército", f"INÍCIO!E{INICIO_ESA}", "7B5400", "F2EEE6")]):
    c0 = 2 + i * 5
    mg(wp, r, c0, r, c0 + 3)
    st(wp.cell(r, c0, nome), b=True, sz=10, fg="FFFFFF", bg=cor, ha="center")
    wp.row_dimensions[r].height = 20
    mg(wp, r + 1, c0, r + 2, c0 + 3)
    st(wp.cell(r + 1, c0, f'=IF({ref}<TODAY(),"REALIZADA",TEXT({ref}-TODAY(),"0"))'),
       b=True, sz=34, fg=cor, bg=tin, ha="center")
    mg(wp, r + 3, c0, r + 3, c0 + 3)
    st(wp.cell(r + 3, c0, f'=IF({ref}<TODAY(),"",  "dias  ·  "&TEXT(ROUND(({ref}-TODAY())/7,0),"0")&" semanas  ·  prova em "&TEXT({ref},"DD/MM/YYYY"))'),
       sz=9, fg=cor, bg=tin, ha="center")
    wp.row_dimensions[r + 3].height = 18
wp.row_dimensions[r + 1].height = 30
wp.row_dimensions[r + 2].height = 22
r += 5

r = sec(wp, r, NC, "  PROGRESSO DO CONTEÚDO",
        "  Fonte: aba CONTEÚDO E REVISÃO. Marque um tópico como Concluído ou Revisado e a barra anda sozinha.")
r = thead(wp, r, ["", "Matéria", "Serve para", "Tópicos", "Feitos", "", "% concluído",
                  "Confiança\nmédia (1–5)", "% acerto\nmédio", "Situação", "", ""], h=30)
CT = "'CONTEÚDO E REVISÃO'"
pg0 = r
for m in ORDEM:
    fam, bar, t1, t2, ink = SUB[m]
    st(wp.cell(r, 1, None), bg=bar)          # trilho de cor
    st(wp.cell(r, 2, m), b=True, sz=9, fg=ink, bg=t1)
    st(wp.cell(r, 3, FAM[fam][1]), sz=7.5, fg=INK2, bg=CARD, ha="center")
    st(wp.cell(r, 4, f'=COUNTIF({CT}!$B$5:$B$310,$B{r})'), sz=9, ha="center", bg=CARD)
    st(wp.cell(r, 5, f'=COUNTIFS({CT}!$B$5:$B$310,$B{r},{CT}!$H$5:$H$310,"Concluído")'
                     f'+COUNTIFS({CT}!$B$5:$B$310,$B{r},{CT}!$H$5:$H$310,"Revisado")'), sz=9, ha="center", bg=CARD)
    st(wp.cell(r, 6, None), bg=CARD)
    st(wp.cell(r, 7, f'=IFERROR(E{r}/D{r},0)'), b=True, sz=10, ha="center", bg=CARD, fmt="0%")
    st(wp.cell(r, 8, f'=IFERROR(AVERAGEIF({CT}!$B$5:$B$310,$B{r},{CT}!$M$5:$M$310),"")'), sz=9, ha="center", bg=CARD, fmt="0.0")
    st(wp.cell(r, 9, f'=IFERROR(AVERAGEIF({CT}!$B$5:$B$310,$B{r},{CT}!$N$5:$N$310),"")'), sz=9, ha="center", bg=CARD, fmt="0%")
    mg(wp, r, 10, r, 12)
    st(wp.cell(r, 10, f'=IF(E{r}=0,"◻  não iniciado",IF(G{r}>=0.9,"●  dominado",IF(G{r}>=0.6,"●  em ritmo",IF(G{r}>=0.3,"◐  atenção","◔  atrasado"))))'),
       b=True, sz=9, ha="center", bg=CARD)
    wp.row_dimensions[r].height = 20
    r += 1
pg1 = r - 1
st(wp.cell(r, 1, None), bg=NAVY)
st(wp.cell(r, 2, "TOTAL"), b=True, sz=9.5, fg="FFFFFF", bg=NAVY)
st(wp.cell(r, 3, None), bg=NEU_BG)
st(wp.cell(r, 4, f"=SUM(D{pg0}:D{pg1})"), b=True, sz=9.5, ha="center", bg=NEU_BG)
st(wp.cell(r, 5, f"=SUM(E{pg0}:E{pg1})"), b=True, sz=9.5, ha="center", bg=NEU_BG)
st(wp.cell(r, 6, None), bg=NEU_BG)
st(wp.cell(r, 7, f"=IFERROR(E{r}/D{r},0)"), b=True, sz=11, ha="center", bg=NEU_BG, fmt="0%")
for cc in (8, 9): st(wp.cell(r, cc, None), bg=NEU_BG)
mg(wp, r, 10, r, 12); st(wp.cell(r, 10, None), bg=NEU_BG)
tot_r = r
# barras de dados reais nas colunas de %
wp.conditional_formatting.add(f"G{pg0}:G{pg1}",
    DataBarRule(start_type="num", start_value=0, end_type="num", end_value=1,
                color="1A51BD", showValue=True))
wp.conditional_formatting.add(f"I{pg0}:I{pg1}",
    DataBarRule(start_type="num", start_value=0, end_type="num", end_value=1,
                color="0C7E65", showValue=True))
wp.conditional_formatting.add(f"H{pg0}:H{pg1}", IconSetRule("5Rating", "num", [1, 2, 3, 4, 5], showValue=True))
wp.conditional_formatting.add(f"J{pg0}:J{pg1}",
    CellIsRule(operator="equal", formula=['"●  dominado"'], fill=PatternFill("solid", fgColor=OK_BG),
               font=Font(name=FT, bold=True, color=OK_FG)))
wp.conditional_formatting.add(f"J{pg0}:J{pg1}",
    CellIsRule(operator="equal", formula=['"◔  atrasado"'], fill=PatternFill("solid", fgColor=BAD_BG),
               font=Font(name=FT, bold=True, color=BAD_FG)))
wp.conditional_formatting.add(f"J{pg0}:J{pg1}",
    CellIsRule(operator="equal", formula=['"◻  não iniciado"'], fill=PatternFill("solid", fgColor=NEU_BG),
               font=Font(name=FT, color=NEU_FG)))
r += 2

r = sec(wp, r, NC, "  EXECUÇÃO E DESEMPENHO")
CS, SM, RD = "'CONTROLE SEMANAL'", "SIMULADOS", "REDAÇÕES"
r = thead(wp, r, ["", "Indicador", "", "Valor", "", "", "Meta / referência", "", "", "", "", ""], h=20)
k0 = r
KPI = [
    ("Semanas com registro",        f'=COUNTIF({CS}!$H$5:$H$60,">0")', "0", "52 semanas até a prova da ESA"),
    ("Horas próprias planejadas",   f'=SUMIF({CS}!$H$5:$H$60,">0",{CS}!$G$5:$G$60)', "0", "33 h por semana (fora o curso)"),
    ("Horas próprias cumpridas",    f'=SUM({CS}!$H$5:$H$60)', "0", ""),
    ("Aderência ao plano",          f'=IFERROR(D{k0+2}/D{k0+1},0)', "0%", "Mínimo aceitável: 85%"),
    ("Aulas do curso assistidas",   f'=SUM({CS}!$O$5:$O$60)', "0", "5 por semana — falta some direto na nota"),
    ("Questões resolvidas",         f'=SUM({CS}!$J$5:$J$60)', "#,##0", "Meta: 250 por semana"),
    ("Taxa de acerto geral",        f'=IFERROR(SUM({CS}!$K$5:$K$60)/SUM({CS}!$J$5:$J$60),0)', "0.0%", "Meta: acima de 75%"),
    ("Simulados feitos",            f'=COUNT({SM}!$B$5:$B$64)', "0", "1 por sábado"),
    ("Média nos simulados",         f'=IFERROR(AVERAGE({SM}!$O$5:$O$64),0)', "0.0", "EAM aprova com 50 — mire acima de 70"),
    ("Redações escritas",           f'=COUNT({RD}!$B$5:$B$64)', "0", "1 a 2 por semana"),
    ("Média das redações",          f'=IFERROR(AVERAGE({RD}!$E$5:$E$64),0)', "0.00", "A ESA elimina abaixo de 5,0"),
    ("Treinos registrados",         f'=COUNT(TAF!$B$9:$B$215)', "0", "5 a 6 por semana"),
]
for nome, f, fmt, meta in KPI:
    mg(wp, r, 2, r, 3)
    st(wp.cell(r, 2, nome), sz=9, bg=CARD, fg=INK2)
    mg(wp, r, 4, r, 6)
    st(wp.cell(r, 4, f), b=True, sz=12, ha="center", bg=CARD, fg=NAVY2, fmt=fmt)
    mg(wp, r, 7, r, 12)
    st(wp.cell(r, 7, meta), sz=8.5, i=True, fg=INK3, bg=CARD)
    wp.row_dimensions[r].height = 21
    r += 1
wp.conditional_formatting.add(f"D{k0+3}",
    CellIsRule(operator="lessThan", formula=["0.85"], fill=PatternFill("solid", fgColor=BAD_BG),
               font=Font(name=FT, bold=True, size=12, color=BAD_FG)))
wp.conditional_formatting.add(f"D{k0+10}",
    CellIsRule(operator="lessThan", formula=["5"], fill=PatternFill("solid", fgColor=BAD_BG),
               font=Font(name=FT, bold=True, size=12, color=BAD_FG)))
r += 1

ch = BarChart(); ch.type = "bar"; ch.style = 2
ch.title = "Conteúdo concluído por matéria"
ch.add_data(Reference(wp, min_col=7, min_row=pg0 - 1, max_row=pg1), titles_from_data=True)
ch.set_categories(Reference(wp, min_col=2, min_row=pg0, max_row=pg1))
ch.height, ch.width, ch.legend = 9.5, 17, None
ch.y_axis.majorGridlines = None
wp.add_chart(ch, f"B{r}")
wp.freeze_panes = "A4"
finish(wp, NC, 100)

# ═════════════════════════════════════════════════ 3 · GRADE SEMANAL
wg = wb.create_sheet("GRADE SEMANAL")
wg.sheet_properties.tabColor = "1A51BD"
DIAS = ["SEGUNDA", "TERÇA", "QUARTA", "QUINTA", "SEXTA", "SÁBADO", "DOMINGO"]
NC = 12
for j, w in enumerate([2.5, 13, 4, 25, 25, 25, 25, 25, 25, 21, 8.5, 2.5], 1):
    wg.column_dimensions[get_column_letter(j)].width = w
r = band(wg, 1, NC, "  GRADE SEMANAL",
         "  Curso 08h–12h de segunda a sexta  ·  refeições às 13h, 17h e 22h  ·  domingo de descanso total")
back(wg, NC)
r += 1
st(wg.cell(r, 2, "HORÁRIO"), b=True, sz=8.5, fg="FFFFFF", bg=NAVY2, ha="center")
st(wg.cell(r, 3, "⏱"), b=True, sz=9, fg="FFFFFF", bg=NAVY2, ha="center")
for j, d in enumerate(DIAS):
    bgd = NAVY2 if j < 6 else "3E5F3E"
    st(wg.cell(r, 4 + j, d), b=True, sz=9, fg="FFFFFF", bg=bgd, ha="center")
wg.row_dimensions[r].height = 24
r += 1

CU = "CURSO PREPARATÓRIO"
GRID = [
 ("06:50–07:20", "30", "rest",  ["☀ Despertar, hidratar, café rápido"]*6 + ["🌙 Sono livre — sem despertador"]),
 ("07:20–07:50", "30", "rev",   ["🧠 Flashcards do dia anterior"]*5 + ["🧠 Flashcards da semana", "— descanso —"]),
 ("07:50–08:00", "10", "rest",  ["🚶 Saída para o curso"]*5 + ["🚶 Preparar o simulado", "— descanso —"]),
 ("08:00–10:00", "2 h", "curso",[CU]*5 + ["📝 SIMULADO — parte 1 (cronometrado)", "— descanso —"]),
 ("10:00–10:15", "15", "rest",  [CU]*5 + ["☕ Intervalo curto", "— descanso —"]),
 ("10:15–12:00", "1h45","curso",[CU]*5 + ["📝 SIMULADO — parte 2 (cronometrado)", "— descanso —"]),
 ("12:00–13:00", "60", "rev",   ["🔁 REVISÃO DA AULA DE HOJE — reescrever o resumo e marcar as dúvidas"]*5 +
                                ["✔ Correção do simulado + caderno de erros", "— descanso —"]),
 ("13:00–14:15", "75", "meal",  ["🍽 ALMOÇO + descanso"]*7),
 ("14:15–15:45", "90", "blk",   ["Matemática — exercícios do assunto do mês",
                                 "Física — teoria + exercícios",
                                 "Matemática — exercícios do assunto do mês",
                                 "Física — questões de provas anteriores",
                                 "Matemática — provas anteriores da ESA e da EAM",
                                 "✍ REDAÇÃO — tema novo, 1 h cronometrada + autocorreção",
                                 "🌿 Lazer, família, sol"]),
 ("15:45–16:00", "15", "rest",  ["☕ Levantar, alongar, longe da tela"]*6 + ["🌿 Lazer"]),
 ("16:00–17:00", "60", "blk",   ["História do Brasil — teoria",
                                 "Geografia do Brasil — teoria e mapas",
                                 "Literatura — escola literária do mês",
                                 "Inglês — grammar point + reading",
                                 "Química — exercícios",
                                 "🔁 Revisão das matérias em atraso",
                                 "🌿 Lazer, família, sol"]),
 ("17:00–17:40", "40", "meal",  ["🍽 LANCHE"]*7),
 ("17:40–18:55", "75", "trn",   ["🏃 Corrida 2.400 m + abdominais",
                                 "🏊 Natação — séries de 50 m",
                                 "🏃 Corrida 2.400 m + barra fixa",
                                 "🏊 Natação — séries de 50 m",
                                 "🏃 Corrida 2.400 m + abdominais",
                                 "🏅 TAF COMPLETO cronometrado",
                                 "🌿 Caminhada leve ou descanso"]),
 ("18:55–19:40", "45", "rest",  ["🚿 Banho e descanso livre"]*6 + ["🌿 Lazer"]),
 ("19:40–21:10", "90", "blk",   ["Português — gramática",
                                 "Química — teoria + exercícios",
                                 "✍ REDAÇÃO — técnica e produção de parágrafo",
                                 "Português — interpretação de texto e sintaxe",
                                 "🔁 REVISÃO GERAL DA SEMANA — refazer todos os erros",
                                 "🌿 LIVRE — lazer, família, descanso",
                                 "🌿 Lazer livre"]),
 ("21:10–21:25", "15", "rest",  ["☕ Descanso"]*5 + ["🌿 Livre", "🌿 Lazer"]),
 ("21:25–22:00", "35", "rev",   ["🎯 Caderno de erros do dia"]*5 +
                                ["📋 Planejar a semana e preencher a planilha", "— descanso —"]),
 ("22:00–22:50", "50", "meal",  ["🍽 JANTAR"]*7),
 ("22:50–23:20", "30", "rev",   ["🧠 Flashcards espaçados + separar o material de amanhã"]*5 +
                                ["🌿 Livre", "📋 Separar o material de segunda (10 min)"]),
 ("23:20–23:50", "30", "free",  ["📵 Desconexão — sem telas, leitura leve"]*7),
 ("23:50–06:50", "7 h", "sleep",["🌙 SONO — 7 horas, inegociável"]*7),
]
TIPO = {"curso": T_CURSO, "rev": T_REV, "meal": T_MEAL, "rest": T_REST,
        "trn": T_TREINO, "free": T_FREE, "sleep": T_SLEEP, "blk": None}
ICON = {"curso": "🎓", "rev": "🔁", "meal": "🍽", "rest": "☕",
        "trn": "🏃", "free": "📵", "sleep": "🌙", "blk": "📚"}


def paint(txt, tipo):
    """devolve (fill, fontcolor, bold) para um texto de célula"""
    for m in ORDEM:
        if txt.startswith(m):
            fam, bar, t1, t2, ink = SUB[m]
            return t1, ink, True
    if "REDAÇÃO" in txt:
        fam, bar, t1, t2, ink = SUB["Redação"]
        return t1, ink, True
    if txt.startswith("📝 SIMULADO") or txt.startswith("✔ Correção"):
        return T_SIM[0], T_SIM[1], True
    if txt.startswith("🔁") or txt.startswith("🎯") or txt.startswith("📋") or txt.startswith("🧠"):
        return T_REV[0], T_REV[1], txt.startswith("🔁 REVISÃO")
    if txt.startswith("🏃") or txt.startswith("🏊") or txt.startswith("🏅"):
        return T_TREINO[0], T_TREINO[1], txt.startswith("🏅")
    if txt.startswith("🌿") or txt.startswith("— descanso") or txt.startswith("☕"):
        return T_REST[0], T_REST[1], False
    if tipo in TIPO and TIPO[tipo]:
        return TIPO[tipo][0], TIPO[tipo][1], tipo == "curso"
    return CARD, INK, False


g0 = r
for horario, dur, tipo, cells in GRID:
    is_blk = tipo == "blk"
    st(wg.cell(r, 2, horario), b=True, sz=8.5, ha="center",
       bg=NAVY if is_blk else "E9ECF0", fg="FFFFFF" if is_blk else INK2)
    st(wg.cell(r, 3, ICON[tipo]), sz=10, ha="center", bg="E9ECF0")
    # escreve e funde blocos iguais consecutivos
    j = 0
    while j < 7:
        k = j
        while k + 1 < 7 and cells[k + 1] == cells[j]:
            k += 1
        bg, fg, bold = paint(cells[j], tipo)
        for x in range(j, k + 1):
            st(wg.cell(r, 4 + x, None), bg=bg)
        c = wg.cell(r, 4 + j, cells[j])
        st(c, b=bold, sz=8.5 if not bold else 9, fg=fg, bg=bg, ha="center", wrap=True)
        mg(wg, r, 4 + j, r, 4 + k)
        j = k + 1
    st(wg.cell(r, 11, dur + (" min" if dur.isdigit() else "")), sz=8, ha="center", bg="E9ECF0", fg=INK3)
    wg.row_dimensions[r].height = 30 if is_blk or tipo == "curso" else 21
    r += 1
r += 1

r = sec(wg, r, NC, "  QUANTAS HORAS CADA MATÉRIA RECEBE",
        "  Só o estudo próprio. O curso das 08h–12h e a revisão das 12h vêm por cima disso.")
r = thead(wg, r, ["", "Matéria", "", "Blocos", "Horas", "Serve para", "Onde aparece na grade", "", "", "", ""], h=20)
CARGA = [("Matemática", 3, 4.5, "Seg 14h15 · Qua 14h15 · Sex 14h15"),
         ("Português", 2, 3.0, "Seg 19h40 · Qui 19h40"),
         ("Física", 2, 3.0, "Ter 14h15 · Qui 14h15"),
         ("Química", 2, 2.5, "Ter 19h40 · Sex 16h00"),
         ("Redação", 2, 1.5, "Qua 19h40 · Sáb 14h15"),
         ("História", 1, 1.0, "Seg 16h00"),
         ("Geografia", 1, 1.0, "Ter 16h00"),
         ("Literatura", 1, 1.0, "Qua 16h00"),
         ("Inglês", 1, 1.0, "Qui 16h00")]
c0 = r
for m, nb, hs, onde in CARGA:
    fam, bar, t1, t2, ink = SUB[m]
    st(wg.cell(r, 1, None), bg=bar)
    mg(wg, r, 2, r, 3)
    st(wg.cell(r, 2, m), b=True, sz=9, fg=ink, bg=t1)
    st(wg.cell(r, 4, nb), sz=9, ha="center", bg=CARD)
    st(wg.cell(r, 5, hs), sz=9, ha="center", bg=CARD, fmt='0.0" h"')
    st(wg.cell(r, 6, FAM[fam][1]), sz=7.5, ha="center", bg=t2, fg=ink)
    mg(wg, r, 7, r, 11)
    st(wg.cell(r, 7, onde), sz=8.5, fg=INK2, bg=CARD)
    wg.row_dimensions[r].height = 19
    r += 1
st(wg.cell(r, 1, None), bg=NAVY)
mg(wg, r, 2, r, 3); st(wg.cell(r, 2, "Blocos de seg a sex"), b=True, sz=9, fg="FFFFFF", bg=NAVY)
st(wg.cell(r, 4, f"=SUM(D{c0}:D{r-1})"), b=True, sz=9, ha="center", bg=NEU_BG)
st(wg.cell(r, 5, f"=SUM(E{c0}:E{r-1})"), b=True, sz=9, ha="center", bg=NEU_BG, fmt='0.0" h"')
st(wg.cell(r, 6, None), bg=NEU_BG)
mg(wg, r, 7, r, 11)
st(wg.cell(r, 7, "+ 5 h de revisão da aula (12h) + 1h30 de revisão geral (sex) + ~5 h de flashcards e caderno de erros "
                 "+ ~7 h de sábado  =  33 h de estudo próprio por semana."), sz=8.5, i=True, fg=INK2, bg=NEU_BG)
r += 2

r = sec(wg, r, NC, "  COMO A GRADE MUDA AO LONGO DO ANO",
        "  Mesmos horários — só as matérias trocam de lugar conforme a prova se aproxima.")
r = thead(wg, r, ["", "Fase", "", "Período", "O que muda", "", "", "", "Por quê", "", ""], h=20)
FASES = [
 ("FASE 1 · BASE", "Ago a Nov/26", "Use a grade exatamente como está.",
  "Cobrir todo o conteúdo uma primeira vez, acompanhando o curso.", NAVY_T, NAVY2),
 ("FASE 2 · APROFUNDAR", "Dez/26 a Jan/27", "Mesma grade — mas todo exercício passa a sair de prova anterior.",
  "Sair da teoria e aprender o estilo das bancas antes da reta final.", NAVY_T, NAVY2),
 ("FASE 3 · RETA EAM", "Fev a Abr/27", "Seg 16h História → Física · Ter 16h Geografia → Química · Qua 16h Literatura → Matemática.",
  "A EAM não cobra História, Geografia nem Literatura. Elas entram em modo manutenção (só flashcards).", "E7F2F0", "01614D"),
 ("FASE 4 · VIRADA ESA", "Mai a Jun/27", "Todos os blocos de Física e Química viram História, Geografia, Literatura, Redação e Inglês.",
  "Física e Química NÃO caem na ESA. Depois da prova da Marinha, cada hora nelas é hora jogada fora.", "F2EEE6", "6D4B04"),
 ("FASE 5 · PICO ESA", "Jul/27", "Dois simulados por semana (quarta e sábado) e duas redações. Teoria vira revisão.",
  "No último mês não se aprende conteúdo novo: consolida-se e treina-se ritmo de prova.", "F2EEE6", "6D4B04"),
]
for nome, per, muda, pq, bg, fg in FASES:
    st(wg.cell(r, 1, None), bg=fg)
    mg(wg, r, 2, r, 3)
    st(wg.cell(r, 2, nome), b=True, sz=8.5, fg=fg, bg=bg, wrap=True)
    st(wg.cell(r, 4, per), sz=8.5, ha="center", bg=bg, fg=fg)
    mg(wg, r, 5, r, 8)
    st(wg.cell(r, 5, muda), sz=8.5, bg=CARD, wrap=True, va="center")
    mg(wg, r, 9, r, 11)
    st(wg.cell(r, 9, pq), sz=8.5, i=True, fg=INK2, bg=CARD, wrap=True, va="center")
    wg.row_dimensions[r].height = 34
    r += 1
r += 1
mg(wg, r, 2, r, 11)
st(wg.cell(r, 2, "Regra dos blocos:  25 min de estudo → 5 min escrevendo o resumo → repetir.  Todo bloco de exercícios termina com o erro "
                 "anotado no caderno de erros.  Nunca comece assunto novo depois das 21h — a última hora do dia é sempre revisão."),
   sz=8.5, i=True, fg=BAD_FG, bg=BAD_BG, wrap=True)
wg.row_dimensions[r].height = 30
wg.freeze_panes = "D5"
finish(wg, NC, 85)
