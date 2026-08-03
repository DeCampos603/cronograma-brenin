# -*- coding: utf-8 -*-
"""Exporta os dados do gerador da planilha para JSON — fonte única para o site."""
import os, io, json, datetime

_b = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gerar_v2c.py")
exec(compile(io.open(_b, encoding="utf-8").read(), _b, "exec"), globals())

DEST = r"G:\Meu Drive\REPO\Cronograma-Brenin\docs\dados\plano.json"
os.makedirs(os.path.dirname(DEST), exist_ok=True)


def grade(G):
    out = []
    for horario, dur, tipo, cells in G:
        out.append({"h": horario, "dur": dur, "tipo": tipo, "dias": list(cells)})
    return out


def cor_de(txt, tipo):
    bg, fg, bold = paint(txt, tipo)
    mat = None
    for m in ORDEM:
        if txt.startswith(m):
            mat = m
            break
    if mat is None and "REDAÇÃO" in txt:
        mat = "Redação"
    return {"bg": bg, "fg": fg, "bold": bold, "materia": mat}


dados = {
    "gerado_em": datetime.date(2026, 8, 3).isoformat(),
    "aluno": "Brenin",
    "familias": {k: {"cor": v[0], "rotulo": v[1]} for k, v in FAM.items()},
    "materias": {m: {"familia": SUB[m][0], "barra": SUB[m][1], "tinta": SUB[m][2],
                     "tinta2": SUB[m][3], "texto": SUB[m][4]} for m in ORDEM},
    "ordem": ORDEM,
    "dias": DIAS,
    "marcos": [{"nome": n, "data": d.isoformat(), "tag": t, "acao": a} for n, d, t, a in MARCOS],
    "provas": [{"materia": m, "eam": e, "esa": s, "horas": h, "porque": p} for m, e, s, h, p in PROVAS],
    "carga": [{"materia": m, "blocos": b, "horas": h, "onde": o} for m, b, h, o in CARGA],
    "fases": [{"nome": n, "periodo": p, "muda": mu, "porque": pq} for n, p, mu, pq, _, _ in FASES],
    "grade": grade(GRID),
    "grade_sem_curso": grade(GRID2),
    "meses": [{"mes": mes, "fase": fase, "marco": marco,
               "itens": [{"materia": m, "conteudo": c, "meta": mt} for m, c, mt in itens]}
              for mes, fase, marco, itens in MESES],
    "topicos": [{"id": i, "materia": m, "unidade": u, "topico": t, "prova": p,
                 "prioridade": pr, "mes": ms}
                for i, (m, u, t, p, pr, ms) in enumerate(TOP, 1)],
    "taf": {"corrida_min": 14.5, "natacao_seg": 90},
}

# paleta de cada célula da grade, pré-calculada (o site não recalcula regra de cor)
for chave, G in (("grade", GRID), ("grade_sem_curso", GRID2)):
    for linha, (horario, dur, tipo, cells) in zip(dados[chave], G):
        linha["cores"] = [cor_de(c, tipo) for c in cells]

io.open(DEST, "w", encoding="utf-8").write(json.dumps(dados, ensure_ascii=False, indent=1))
print("JSON ->", DEST)
print("  topicos:", len(dados["topicos"]), "| meses:", len(dados["meses"]),
      "| linhas de grade:", len(dados["grade"]), "| marcos:", len(dados["marcos"]))
