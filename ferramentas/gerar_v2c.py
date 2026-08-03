# -*- coding: utf-8 -*-
"""Parte 3 do gerador: abas de registro, plano de recesso e gravação."""
import os, io
_b = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gerar_v2b.py")
exec(compile(io.open(_b, encoding="utf-8").read(), _b, "exec"), globals())

# ═══════════════════════════════════════════ 6 · CONTROLE SEMANAL
wk = wb.create_sheet("CONTROLE SEMANAL")
wk.sheet_properties.tabColor = "35597F"
NC = 18
for j, w in enumerate([5.5, 10, 10, 9, 17, 34, 9, 9, 9, 10, 10, 9, 9, 8, 8, 9, 9, 32], 1):
    wk.column_dimensions[get_column_letter(j)].width = w
r = band(wk, 1, NC, "  CONTROLE SEMANAL  ·  52 SEMANAS",
         "  Preencha as colunas claras todo sábado, às 21h25. O resto se calcula e alimenta o PAINEL.")
back(wk, NC)
r = thead(wk, r, ["SEM.", "Início", "Fim", "Mês", "Fase", "Meta principal da semana",
                  "Horas\nplan.", "Horas\nfeitas", "Aderên-\ncia", "Questões\nfeitas", "Questões\ncertas",
                  "%\nacerto", "Reda-\nções", "Trei-\nnos", "Aulas\ndo curso", "Simu-\nlado", "Nota\nsimul.",
                  "O que travou e o que ajustar"], h=34)

FASE_MES = {"Ago/26": ("FASE 1 · BASE", NAVY_T, NAVY2), "Set/26": ("FASE 1 · BASE", NAVY_T, NAVY2),
            "Out/26": ("FASE 1 · BASE", NAVY_T, NAVY2), "Nov/26": ("FASE 1 · BASE", NAVY_T, NAVY2),
            "Dez/26": ("FASE 2 · APROFUNDAR", "E9EEF6", NAVY2), "Jan/27": ("FASE 2 · APROFUNDAR", "E9EEF6", NAVY2),
            "Fev/27": ("FASE 3 · RETA EAM", "E7F2F0", "01614D"), "Mar/27": ("FASE 3 · RETA EAM", "E7F2F0", "01614D"),
            "Abr/27": ("FASE 3 · PICO EAM", "CEE5E0", "01614D"),
            "Mai/27": ("FASE 4 · VIRADA ESA", "F2EEE6", "6D4B04"), "Jun/27": ("FASE 4 · VIRADA ESA", "F2EEE6", "6D4B04"),
            "Jul/27": ("FASE 5 · PICO ESA", "E5DDCC", "6D4B04")}
MES_ABR = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
ini = _dt.date(2026, 8, 3)
ck0 = r
for w_ in range(1, 53):
    d0 = ini + _dt.timedelta(days=7 * (w_ - 1))
    d1 = d0 + _dt.timedelta(days=6)
    mes = f"{MES_ABR[d0.month-1]}/{str(d0.year)[2:]}"
    fase, fbg, ffg = FASE_MES.get(mes, ("—", NEU_BG, INK2))
    zeb = CARD if w_ % 2 else "FBFCFD"
    st(wk.cell(r, 1, w_), b=True, sz=8.5, ha="center", bg=NAVY, fg="FFFFFF")
    st(wk.cell(r, 2, d0), sz=8.5, ha="center", bg=zeb, fmt="DD/MM/YY", fg=INK2)
    st(wk.cell(r, 3, d1), sz=8.5, ha="center", bg=zeb, fmt="DD/MM/YY", fg=INK2)
    st(wk.cell(r, 4, mes), sz=8.5, ha="center", bg=zeb, fg=INK3)
    st(wk.cell(r, 5, fase), b=True, sz=7.5, ha="center", bg=fbg, fg=ffg)
    st(wk.cell(r, 6, None), sz=8.5, bg=INPUT_BG, fg=INPUT_FG, wrap=True)
    st(wk.cell(r, 7, 33), sz=8.5, ha="center", bg=zeb, fg=INK3, fmt="0")
    st(wk.cell(r, 8, None), sz=8.5, ha="center", bg=INPUT_BG, fg=INPUT_FG, fmt="0.0")
    st(wk.cell(r, 9, f'=IF(H{r}="","",IFERROR(H{r}/G{r},0))'), b=True, sz=8.5, ha="center", bg=zeb, fmt="0%")
    st(wk.cell(r, 10, None), sz=8.5, ha="center", bg=INPUT_BG, fg=INPUT_FG, fmt="#,##0")
    st(wk.cell(r, 11, None), sz=8.5, ha="center", bg=INPUT_BG, fg=INPUT_FG, fmt="#,##0")
    st(wk.cell(r, 12, f'=IF(J{r}="","",IFERROR(K{r}/J{r},0))'), b=True, sz=8.5, ha="center", bg=zeb, fmt="0%")
    for c_ in (13, 14, 15):
        st(wk.cell(r, c_, None), sz=8.5, ha="center", bg=INPUT_BG, fg=INPUT_FG, fmt="0")
    st(wk.cell(r, 16, None), sz=8.5, ha="center", bg=INPUT_BG, fg=INPUT_FG)
    st(wk.cell(r, 17, None), sz=8.5, ha="center", bg=INPUT_BG, fg=INPUT_FG, fmt="0.0")
    st(wk.cell(r, 18, None), sz=8.5, bg=INPUT_BG, fg=INPUT_FG, wrap=True)
    wk.row_dimensions[r].height = 19
    r += 1
ck1 = r - 1
st(wk.cell(r, 1, None), bg=NAVY)
mg(wk, r, 2, r, 6); st(wk.cell(r, 2, "TOTAIS  →"), b=True, sz=9, fg="FFFFFF", bg=NAVY, ha="right")
for c_, f, fmt in [(7, f"=SUM(G{ck0}:G{ck1})", "0"), (8, f"=SUM(H{ck0}:H{ck1})", "0.0"),
                   (9, f"=IFERROR(H{r}/G{r},0)", "0%"), (10, f"=SUM(J{ck0}:J{ck1})", "#,##0"),
                   (11, f"=SUM(K{ck0}:K{ck1})", "#,##0"), (12, f"=IFERROR(K{r}/J{r},0)", "0%"),
                   (13, f"=SUM(M{ck0}:M{ck1})", "0"), (14, f"=SUM(N{ck0}:N{ck1})", "0"),
                   (15, f"=SUM(O{ck0}:O{ck1})", "0"), (17, f"=IFERROR(AVERAGE(Q{ck0}:Q{ck1}),0)", "0.0")]:
    st(wk.cell(r, c_, f), b=True, sz=8.5, ha="center", bg=NEU_BG, fmt=fmt)
st(wk.cell(r, 16, None), bg=NEU_BG); st(wk.cell(r, 18, None), bg=NEU_BG)
dv4 = DataValidation(type="list", formula1='"Sim,Não"', allow_blank=True)
wk.add_data_validation(dv4); dv4.add(f"P{ck0}:P{ck1}")
wk.conditional_formatting.add(f"I{ck0}:I{ck1}", CellIsRule(operator="greaterThanOrEqual", formula=["0.85"],
    fill=PatternFill("solid", fgColor=OK_BG), font=Font(name=FT, bold=True, size=8.5, color=OK_FG)))
wk.conditional_formatting.add(f"I{ck0}:I{ck1}", CellIsRule(operator="lessThan", formula=["0.7"],
    fill=PatternFill("solid", fgColor=BAD_BG), font=Font(name=FT, bold=True, size=8.5, color=BAD_FG)))
wk.conditional_formatting.add(f"L{ck0}:L{ck1}", CellIsRule(operator="greaterThanOrEqual", formula=["0.75"],
    fill=PatternFill("solid", fgColor=OK_BG), font=Font(name=FT, bold=True, size=8.5, color=OK_FG)))
wk.conditional_formatting.add(f"L{ck0}:L{ck1}", CellIsRule(operator="lessThan", formula=["0.6"],
    fill=PatternFill("solid", fgColor=BAD_BG), font=Font(name=FT, bold=True, size=8.5, color=BAD_FG)))
wk.conditional_formatting.add(f"O{ck0}:O{ck1}", CellIsRule(operator="lessThan", formula=["5"],
    fill=PatternFill("solid", fgColor=BAD_BG), font=Font(name=FT, bold=True, size=8.5, color=BAD_FG)))
wk.freeze_panes = "G5"
wk.auto_filter.ref = f"A4:R{ck1}"
finish(wk, NC, 85)

# ═══════════════════════════════════════════════════ 7 · SIMULADOS
wsm = wb.create_sheet("SIMULADOS")
wsm.sheet_properties.tabColor = "487CDE"
NC = 17
for j, w in enumerate([5.5, 10, 24, 8, 7.5, 7.5, 7.5, 7.5, 7.5, 7.5, 7.5, 9, 9, 9, 10, 24, 32], 1):
    wsm.column_dimensions[get_column_letter(j)].width = w
r = band(wsm, 1, NC, "  SIMULADOS",
         "  Um por sábado, das 08h às 12h, cronometrado como a prova real. Digite os ACERTOS por matéria — o resto se calcula.")
back(wsm, NC)
r = thead(wsm, r, ["Nº", "Data", "Origem / banca", "Alvo", "Port.", "Mat.", "Fís.", "Quím.",
                   "Hist.", "Geo.", "Ingl.", "Acertos", "Questões", "% acerto", "Nota\n(0–100)",
                   "Matérias mais fracas", "O que fazer nesta semana"], h=32)
SUB_COL = {5: "Português", 6: "Matemática", 7: "Física", 8: "Química",
           9: "História", 10: "Geografia", 11: "Inglês"}
for c_, m in SUB_COL.items():
    fam, bar, t1, t2, ink = SUB[m]
    cell = wsm.cell(r - 1, c_)
    cell.fill = PatternFill("solid", fgColor=bar)
sm0 = r
for i in range(1, 61):
    zeb = CARD if i % 2 else "FBFCFD"
    st(wsm.cell(r, 1, i), b=True, sz=8.5, ha="center", bg=NAVY, fg="FFFFFF")
    st(wsm.cell(r, 2, None), sz=8.5, ha="center", bg=INPUT_BG, fg=INPUT_FG, fmt="DD/MM/YYYY")
    st(wsm.cell(r, 3, None), sz=8.5, bg=INPUT_BG, fg=INPUT_FG)
    st(wsm.cell(r, 4, None), sz=8.5, ha="center", bg=INPUT_BG, fg=INPUT_FG)
    for c_ in range(5, 12):
        fam, bar, t1, t2, ink = SUB[SUB_COL[c_]]
        st(wsm.cell(r, c_, None), sz=8.5, ha="center", bg=INPUT_BG, fg=ink)
    st(wsm.cell(r, 12, f'=IF(COUNT(E{r}:K{r})=0,"",SUM(E{r}:K{r}))'), b=True, sz=8.5, ha="center", bg=zeb)
    st(wsm.cell(r, 13, None), sz=8.5, ha="center", bg=INPUT_BG, fg=INPUT_FG)
    st(wsm.cell(r, 14, f'=IF(OR(L{r}="",M{r}=""),"",IFERROR(L{r}/M{r},0))'), b=True, sz=8.5, ha="center", bg=zeb, fmt="0.0%")
    st(wsm.cell(r, 15, f'=IF(N{r}="","",N{r}*100)'), b=True, sz=9, ha="center", bg=zeb, fmt="0.0")
    st(wsm.cell(r, 16, None), sz=8.5, bg=INPUT_BG, fg=INPUT_FG)
    st(wsm.cell(r, 17, None), sz=8.5, bg=INPUT_BG, fg=INPUT_FG, wrap=True)
    wsm.row_dimensions[r].height = 18
    r += 1
sm1 = r - 1
dv5 = DataValidation(type="list", formula1='"ESA,EAM"', allow_blank=True)
wsm.add_data_validation(dv5); dv5.add(f"D{sm0}:D{sm1}")
wsm.conditional_formatting.add(f"O{sm0}:O{sm1}", CellIsRule(operator="greaterThanOrEqual", formula=["70"],
    fill=PatternFill("solid", fgColor=OK_BG), font=Font(name=FT, bold=True, size=9, color=OK_FG)))
wsm.conditional_formatting.add(f"O{sm0}:O{sm1}", CellIsRule(operator="lessThan", formula=["50"],
    fill=PatternFill("solid", fgColor=BAD_BG), font=Font(name=FT, bold=True, size=9, color=BAD_FG)))
wsm.conditional_formatting.add(f"N{sm0}:N{sm1}",
    DataBarRule(start_type="num", start_value=0, end_type="num", end_value=1, color="487CDE", showValue=True))
r += 1
mg(wsm, r, 2, r, 17)
st(wsm.cell(r, 2, "Corte da EAM: aprova com 50 pontos, exigindo mais de 10 pontos em Português, Matemática e Ciências, sem zerar Inglês. "
                  "Para classificar de verdade — não só passar — mire acima de 70."),
   sz=8.5, i=True, fg=BAD_FG, bg=BAD_BG, wrap=True)
wsm.row_dimensions[r].height = 26
wsm.freeze_panes = "E5"
finish(wsm, NC, 90)

# ═══════════════════════════════════════════════════ 8 · REDAÇÕES
wr = wb.create_sheet("REDAÇÕES")
wr.sheet_properties.tabColor = "E5A424"
NC = 13
for j, w in enumerate([5.5, 10, 42, 9, 11, 10, 11, 9, 10, 10, 11, 30, 32], 1):
    wr.column_dimensions[get_column_letter(j)].width = w
r = band(wr, 1, NC, "  REDAÇÕES  ·  ESA  ·  ELIMINATÓRIA",
         "  Nota abaixo de 5,0 reprova, por melhor que seja o resto da prova. Uma na quarta às 19h40 e outra no sábado às 14h15.")
back(wr, NC)
r = thead(wr, r, ["Nº", "Data", "Tema", "Tempo\n(min)", "NOTA FINAL\n(0–10)", "Estrutura\n(0–2)",
                  "Argumen-\ntação (0–3)", "Coesão\n(0–2)", "Gramática\n(0–2)", "Proposta\n(0–1)",
                  "Soma dos\ncritérios", "Erros principais", "O que fazer diferente na próxima"], h=34)
rd0 = r
for i in range(1, 61):
    zeb = CARD if i % 2 else "FBFCFD"
    st(wr.cell(r, 1, i), b=True, sz=8.5, ha="center", bg=NAVY, fg="FFFFFF")
    st(wr.cell(r, 2, None), sz=8.5, ha="center", bg=INPUT_BG, fg=INPUT_FG, fmt="DD/MM/YYYY")
    st(wr.cell(r, 3, None), sz=8.5, bg=INPUT_BG, fg=INPUT_FG)
    st(wr.cell(r, 4, None), sz=8.5, ha="center", bg=INPUT_BG, fg=INPUT_FG)
    st(wr.cell(r, 5, None), b=True, sz=10, ha="center", bg=INPUT_BG, fg=INPUT_FG, fmt="0.0")
    for c_ in range(6, 11):
        st(wr.cell(r, c_, None), sz=8.5, ha="center", bg=INPUT_BG, fg=INPUT_FG, fmt="0.0")
    st(wr.cell(r, 11, f'=IF(COUNT(F{r}:J{r})=0,"",SUM(F{r}:J{r}))'), b=True, sz=8.5, ha="center", bg=zeb, fmt="0.0")
    st(wr.cell(r, 12, None), sz=8.5, bg=INPUT_BG, fg=INPUT_FG, wrap=True)
    st(wr.cell(r, 13, None), sz=8.5, bg=INPUT_BG, fg=INPUT_FG, wrap=True)
    wr.row_dimensions[r].height = 18
    r += 1
rd1 = r - 1
wr.conditional_formatting.add(f"E{rd0}:E{rd1}", CellIsRule(operator="lessThan", formula=["5"],
    fill=PatternFill("solid", fgColor="F8CFC9"), font=Font(name=FT, bold=True, size=10, color=BAD_FG)))
wr.conditional_formatting.add(f"E{rd0}:E{rd1}", CellIsRule(operator="between", formula=["5", "6.99"],
    fill=PatternFill("solid", fgColor="FCF6E9"), font=Font(name=FT, bold=True, size=10, color="6D4B04")))
wr.conditional_formatting.add(f"E{rd0}:E{rd1}", CellIsRule(operator="greaterThanOrEqual", formula=["7"],
    fill=PatternFill("solid", fgColor=OK_BG), font=Font(name=FT, bold=True, size=10, color=OK_FG)))
r += 1
mg(wr, r, 2, r, 4)
st(wr.cell(r, 2, "MÉDIA ATUAL  →"), b=True, sz=10, ha="right", bg=NAVY, fg="FFFFFF")
st(wr.cell(r, 5, f'=IFERROR(AVERAGE(E{rd0}:E{rd1}),0)'), b=True, sz=14, ha="center", bg=NEU_BG, fmt="0.00")
mg(wr, r, 6, r, 13)
st(wr.cell(r, 6, f'=IF(COUNT(E{rd0}:E{rd1})=0,"Nenhuma redação registrada ainda.",'
                 f'IF(E{r}>=7,"Zona segura — mantenha o ritmo.",'
                 f'IF(E{r}>=5,"Passa, mas sem margem. Uma redação ruim no dia elimina.",'
                 f'"RISCO DE ELIMINAÇÃO — priorize redação sobre qualquer outra matéria.")))'),
   b=True, sz=10, bg=NEU_BG, fg=BAD_FG)
wr.row_dimensions[r].height = 24
wr.freeze_panes = "D5"
finish(wr, NC, 90)

# ══════════════════════════════════════════════════════════ 9 · TAF
wt = wb.create_sheet("TAF")
wt.sheet_properties.tabColor = "A32A1C"
NC = 11
for j, w in enumerate([2.5, 11, 17, 16, 12, 15, 11, 10, 12, 12, 34], 1):
    wt.column_dimensions[get_column_letter(j)].width = w
r = band(wt, 1, NC, "  TESTE DE APTIDÃO FÍSICA  ·  TAF",
         "  O TAF elimina tanto quanto a prova escrita. Tempos em número decimal:  14,5 = 14 min 30 s.")
back(wt, NC)
r = sec(wt, r, NC, "  SUAS METAS", "  Índices mínimos da EAM. Confirme os da ESA no edital e ajuste aqui.")
st(wt.cell(r, 2, "META  →"), b=True, sz=9, ha="right", bg=NAVY, fg="FFFFFF")
st(wt.cell(r, 3, 14.5), b=True, sz=12, ha="center", bg=INPUT_BG, fg=INPUT_FG, fmt='0.00" min"')
st(wt.cell(r, 4, 90), b=True, sz=12, ha="center", bg=INPUT_BG, fg=INPUT_FG, fmt='0" s"')
mg(wt, r, 5, r, 11)
st(wt.cell(r, 5, "Correr 2.400 m em até 14 min 30 s   ·   Nadar 50 m em até 1 min 30 s (90 s)."),
   sz=9, i=True, fg=BAD_FG, bg=BAD_BG)
wt.row_dimensions[r].height = 24
META = r
r += 2
r = thead(wt, r, ["", "Data", "Corrida 2.400 m\n(min — ex.: 13,75)", "Natação 50 m\n(segundos)",
                  "Barra fixa\n(repetições)", "Abdominais\n(em 1 minuto)", "Flexões", "Peso\n(kg)",
                  "Corrida\nno índice?", "Natação\nno índice?", "Observações do treino"], h=34)
tf0 = r
for i in range(1, 204):
    zeb = CARD if i % 2 else "FBFCFD"
    st(wt.cell(r, 1, None), bg="A32A1C" if i % 7 == 1 else CANVAS, bd=False)
    st(wt.cell(r, 2, None), sz=8.5, ha="center", bg=INPUT_BG, fg=INPUT_FG, fmt="DD/MM/YY")
    for c_, fmt in ((3, "0.00"), (4, "0"), (5, "0"), (6, "0"), (7, "0"), (8, "0.0")):
        st(wt.cell(r, c_, None), sz=8.5, ha="center", bg=INPUT_BG, fg=INPUT_FG, fmt=fmt)
    st(wt.cell(r, 9, f'=IF(C{r}="","",IF(C{r}<=$C${META},"✔  sim","✘  ainda não"))'),
       b=True, sz=8.5, ha="center", bg=zeb)
    st(wt.cell(r, 10, f'=IF(D{r}="","",IF(D{r}<=$D${META},"✔  sim","✘  ainda não"))'),
       b=True, sz=8.5, ha="center", bg=zeb)
    st(wt.cell(r, 11, None), sz=8.5, bg=INPUT_BG, fg=INPUT_FG, wrap=True)
    wt.row_dimensions[r].height = 17
    r += 1
tf1 = r - 1
for col in ("I", "J"):
    wt.conditional_formatting.add(f"{col}{tf0}:{col}{tf1}", CellIsRule(operator="equal", formula=['"✔  sim"'],
        fill=PatternFill("solid", fgColor=OK_BG), font=Font(name=FT, bold=True, size=8.5, color=OK_FG)))
    wt.conditional_formatting.add(f"{col}{tf0}:{col}{tf1}", CellIsRule(operator="equal", formula=['"✘  ainda não"'],
        fill=PatternFill("solid", fgColor=BAD_BG), font=Font(name=FT, bold=True, size=8.5, color=BAD_FG)))
wt.conditional_formatting.add(f"C{tf0}:C{tf1}",
    DataBarRule(start_type="num", start_value=10, end_type="num", end_value=20, color="A32A1C", showValue=True))
r += 1
mg(wt, r, 2, r, 4); st(wt.cell(r, 2, "MELHOR CORRIDA  →"), b=True, sz=9, ha="right", bg=NAVY, fg="FFFFFF")
st(wt.cell(r, 5, f'=IFERROR(MIN(C{tf0}:C{tf1}),"")'), b=True, sz=11, ha="center", bg=NEU_BG, fmt='0.00" min"')
mg(wt, r, 6, r, 7); st(wt.cell(r, 6, "MELHOR NATAÇÃO  →"), b=True, sz=9, ha="right", bg=NAVY, fg="FFFFFF")
st(wt.cell(r, 8, f'=IFERROR(MIN(D{tf0}:D{tf1}),"")'), b=True, sz=11, ha="center", bg=NEU_BG, fmt='0" s"')
mg(wt, r, 9, r, 11)
st(wt.cell(r, 9, f'=IF(COUNT(C{tf0}:C{tf1})=0,"Nenhum treino registrado ainda.",'
                 f'IF(AND(E{r}<=$C${META},H{r}<=$D${META}),"Os dois índices já batidos. Agora é manter.",'
                 f'"Ainda falta bater pelo menos um dos índices."))'), b=True, sz=9, ha="center", bg=NEU_BG)
wt.row_dimensions[r].height = 24
wt.freeze_panes = "C8"
finish(wt, NC, 90)

# ══════════════════════════════════════════ 10 · PLANO SEM CURSO
wv = wb.create_sheet("PLANO SEM CURSO")
wv.sheet_properties.tabColor = "0DB28F"
NC = 12
for j, w in enumerate([2.5, 13, 4, 25, 25, 25, 25, 25, 25, 21, 8.5, 2.5], 1):
    wv.column_dimensions[get_column_letter(j)].width = w
r = band(wv, 1, NC, "  PLANO SEM CURSO  ·  RECESSO E FÉRIAS",
         "  Para quando o curso para (dezembro, janeiro e julho) — a manhã volta a ser sua. ~9h30 de estudo por dia.")
back(wv, NC)
r += 1
st(wv.cell(r, 2, "HORÁRIO"), b=True, sz=8.5, fg="FFFFFF", bg=NAVY2, ha="center")
st(wv.cell(r, 3, "⏱"), b=True, sz=9, fg="FFFFFF", bg=NAVY2, ha="center")
for j, d in enumerate(DIAS):
    st(wv.cell(r, 4 + j, d), b=True, sz=9, fg="FFFFFF",
       bg=NAVY2 if j < 6 else "3E5F3E", ha="center")
wv.row_dimensions[r].height = 24
r += 1
GRID2 = [
 ("06:50–07:20", "30", "rest",  ["☀ Despertar, hidratar, café rápido"]*6 + ["🌙 Sono livre"]),
 ("07:20–07:50", "30", "rev",   ["🧠 Flashcards do dia anterior"]*5 + ["🧠 Flashcards da semana", "— descanso —"]),
 ("07:50–09:20", "90", "blk",   ["Matemática — teoria do assunto do mês",
                                 "Física — teoria do assunto do mês",
                                 "Matemática — teoria do assunto do mês",
                                 "Física — teoria do assunto do mês",
                                 "Matemática — teoria do assunto do mês",
                                 "📝 SIMULADO — parte 1 (cronometrado)", "— descanso —"]),
 ("09:20–09:35", "15", "rest",  ["☕ Levantar, alongar, longe da tela"]*6 + ["— descanso —"]),
 ("09:35–11:05", "90", "blk",   ["Matemática — exercícios (30 questões)",
                                 "Química — teoria + exercícios",
                                 "Português — gramática",
                                 "Física — exercícios (25 questões)",
                                 "Química — exercícios",
                                 "📝 SIMULADO — parte 2 (cronometrado)", "— descanso —"]),
 ("11:05–11:20", "15", "rest",  ["☕ Descanso"]*6 + ["— descanso —"]),
 ("11:20–13:00", "100", "blk",  ["História do Brasil — teoria",
                                 "Geografia do Brasil — teoria e mapas",
                                 "Literatura — escola literária do mês",
                                 "História do Brasil — exercícios",
                                 "Geografia do Brasil — exercícios",
                                 "✔ Correção do simulado + caderno de erros", "— descanso —"]),
 ("13:00–14:15", "75", "meal",  ["🍽 ALMOÇO + descanso"]*7),
 ("14:15–15:45", "90", "blk",   ["Português — interpretação de texto",
                                 "Matemática — exercícios (30 questões)",
                                 "Física — teoria + exercícios",
                                 "Português — sintaxe",
                                 "Matemática — provas anteriores",
                                 "✍ REDAÇÃO — tema novo, cronometrada", "🌿 Lazer, família, sol"]),
 ("15:45–16:00", "15", "rest",  ["☕ Descanso"]*6 + ["🌿 Lazer"]),
 ("16:00–17:00", "60", "blk",   ["Inglês — grammar + reading",
                                 "Literatura — leitura e questões",
                                 "Inglês — vocabulary + questões",
                                 "Química — exercícios",
                                 "🔁 Revisão das matérias em atraso",
                                 "🔁 Revisão das matérias em atraso", "🌿 Lazer, família, sol"]),
 ("17:00–17:40", "40", "meal",  ["🍽 LANCHE"]*7),
 ("17:40–18:55", "75", "trn",   ["🏃 Corrida 2.400 m + abdominais", "🏊 Natação — séries de 50 m",
                                 "🏃 Corrida 2.400 m + barra fixa", "🏊 Natação — séries de 50 m",
                                 "🏃 Corrida 2.400 m + abdominais", "🏅 TAF COMPLETO cronometrado",
                                 "🌿 Caminhada leve ou descanso"]),
 ("18:55–19:40", "45", "rest",  ["🚿 Banho e descanso livre"]*6 + ["🌿 Lazer"]),
 ("19:40–21:10", "90", "blk",   ["✍ REDAÇÃO — técnica e produção",
                                 "Português — gramática",
                                 "Química — teoria + exercícios",
                                 "Matemática — questões mistas",
                                 "🔁 REVISÃO GERAL DA SEMANA — refazer todos os erros",
                                 "🌿 LIVRE — lazer, família, descanso", "🌿 Lazer livre"]),
 ("21:10–21:25", "15", "rest",  ["☕ Descanso"]*5 + ["🌿 Livre", "🌿 Lazer"]),
 ("21:25–22:00", "35", "rev",   ["🎯 Caderno de erros do dia"]*5 +
                                ["📋 Planejar a semana e preencher a planilha", "— descanso —"]),
 ("22:00–22:50", "50", "meal",  ["🍽 JANTAR"]*7),
 ("22:50–23:20", "30", "rev",   ["🧠 Flashcards espaçados + separar o material de amanhã"]*5 +
                                ["🌿 Livre", "📋 Separar o material de segunda"]),
 ("23:20–23:50", "30", "free",  ["📵 Desconexão — sem telas, leitura leve"]*7),
 ("23:50–06:50", "7 h", "sleep",["🌙 SONO — 7 horas, inegociável"]*7),
]
for horario, dur, tipo, cells in GRID2:
    is_blk = tipo == "blk"
    st(wv.cell(r, 2, horario), b=True, sz=8.5, ha="center",
       bg=NAVY if is_blk else "E9ECF0", fg="FFFFFF" if is_blk else INK2)
    st(wv.cell(r, 3, ICON[tipo]), sz=10, ha="center", bg="E9ECF0")
    j = 0
    while j < 7:
        k = j
        while k + 1 < 7 and cells[k + 1] == cells[j]:
            k += 1
        bg, fg, bold = paint(cells[j], tipo)
        for x in range(j, k + 1):
            st(wv.cell(r, 4 + x, None), bg=bg)
        st(wv.cell(r, 4 + j, cells[j]), b=bold, sz=8.5 if not bold else 9, fg=fg, bg=bg, ha="center", wrap=True)
        mg(wv, r, 4 + j, r, 4 + k)
        j = k + 1
    st(wv.cell(r, 11, dur + (" min" if dur.isdigit() else "")), sz=8, ha="center", bg="E9ECF0", fg=INK3)
    wv.row_dimensions[r].height = 30 if is_blk else 21
    r += 1
r += 1
mg(wv, r, 2, r, 12)
st(wv.cell(r, 2, "Quando usar:  recesso de dezembro e janeiro, férias de julho e as duas semanas anteriores a cada prova. "
                 "São 6 blocos por dia contra 3 do plano normal — é aqui que se recupera atraso e se ganha vantagem."),
   sz=8.5, i=True, fg=INK2, bg=NEU_BG, wrap=True)
wv.row_dimensions[r].height = 28
wv.freeze_panes = "D5"
finish(wv, NC, 85)

wb.save(OUT)
print("OK ->", OUT)
print("abas:", [s.title for s in wb.worksheets])
