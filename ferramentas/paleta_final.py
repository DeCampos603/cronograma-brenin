# -*- coding: utf-8 -*-
"""Paleta por FAMILIA DE PROVA (codificacao composta):
   matiz = para qual prova a materia serve; luminosidade = a materia dentro da familia.
   Status (verde/vermelho/cinza) fica reservado e nunca reutilizado como identidade."""
import math, itertools
from validate_palette import (lin, oklab_from_lin, deltaE, oklch, contrast, BAND, CHROMA_FLOOR)
from otimizar_paleta import oklch_to_hex

LO, HI = BAND["light"]

def mix_white(hexc, w):
    """mistura hexc com branco (w = fracao de branco) no espaco sRGB."""
    h = hexc.lstrip("#")
    rgb = [int(h[i:i+2], 16) for i in (0, 2, 4)]
    return "".join(f"{round(c + (255 - c) * w):02X}" for c in rgb)


def mk(H, L, Cmax):
    """maior croma <= Cmax que fica no gamut sRGB para (H, L)."""
    C = Cmax
    while C >= 0.02:
        hx = oklch_to_hex(L, C, H)
        if hx:
            return hx
        C -= 0.005
    return None

# ---- familias -------------------------------------------------------------
H_AMBAS, H_EAM, H_ESA = 262, 172, 78   # azul / verde-mar(Marinha) / ocre-caqui(Exercito)

SUBJ = [
    # nome,        familia,  matiz,   L_barra, C
    ("Matemática", "AMBAS",  H_AMBAS, 0.470, 0.180),
    ("Português",  "AMBAS",  H_AMBAS, 0.600, 0.160),
    ("Inglês",     "AMBAS",  H_AMBAS, 0.700, 0.130),
    ("Física",     "EAM",    H_EAM,   0.530, 0.140),
    ("Química",    "EAM",    H_EAM,   0.680, 0.150),
    ("História",   "ESA",    H_ESA,   0.475, 0.120),
    ("Geografia",  "ESA",    H_ESA,   0.575, 0.130),
    ("Literatura", "ESA",    H_ESA,   0.670, 0.140),
    ("Redação",    "ESA",    H_ESA,   0.762, 0.150),
]

bars, inks, tints, tints2, nomes = [], [], [], [], []
print("materia       familia   barra    L      C     texto    contraste   fundo")
for nome, fam, H, L, C in SUBJ:
    bar = mk(H, L, C)
    ink = mk(H, min(L, 0.44), C + 0.02)          # texto escuro legivel
    tint = mix_white(bar, 0.90)                   # fundo bem claro
    tint2 = mix_white(bar, 0.80)                  # fundo medio
    Lr, Cr = oklch(bar)
    bars.append(bar); inks.append(ink); tints.append(tint); tints2.append(tint2); nomes.append(nome)
    print(f"  {nome:12s} {fam:7s}  {bar}  {Lr:.3f}  {Cr:.3f}  {ink}   {contrast(ink,'#FFFFFF'):5.2f}    {tint}")

# ---- 1. familias como paleta categorica (checagem dura) -------------------
print("\n== 1. ANCORAS DE FAMILIA como paleta categorica (todos os pares) ==")
anc = [bars[0], bars[3], bars[5]]
anc_n = ["AMBAS", "EAM", "ESA"]
ok = True
for (i, j) in itertools.combinations(range(3), 2):
    dn = deltaE(anc[i], anc[j])
    dp = deltaE(anc[i], anc[j], "protan")
    dd = deltaE(anc[i], anc[j], "deutan")
    st = "PASS" if (dn >= 15 and min(dp, dd) >= 8) else "FAIL"
    if st == "FAIL": ok = False
    print(f"  [{st}] {anc_n[i]} <-> {anc_n[j]}: normal {dn:.1f} (piso 15) · protan {dp:.1f} · deutan {dd:.1f} (piso 8)")

# ---- 2. cada familia como rampa ordinal ------------------------------------
print("\n== 2. Cada familia como RAMPA ORDINAL (L monotona, gap >= 0.06, ponta clara >= 2:1) ==")
for fam in ("AMBAS", "EAM", "ESA"):
    idx = [k for k, s in enumerate(SUBJ) if s[1] == fam]
    ramp = [bars[k] for k in idx]
    Ls = [oklch(c)[0] for c in ramp]
    mono = all(Ls[i] < Ls[i+1] for i in range(len(Ls)-1))
    gaps = [round(Ls[i+1]-Ls[i], 3) for i in range(len(Ls)-1)]
    gap_ok = all(g >= 0.06 for g in gaps)
    light = ramp[-1]
    cr = contrast(light, "#FFFFFF")
    cr_ok = cr >= 2.0
    if not (mono and gap_ok and cr_ok): ok = False
    print(f"  {fam:6s} L={[round(l,3) for l in Ls]}  gaps={gaps}")
    print(f"         [{'PASS' if mono else 'FAIL'}] monotona   [{'PASS' if gap_ok else 'FAIL'}] gaps>=0.06   "
          f"[{'PASS' if cr_ok else 'FAIL'}] ponta clara {cr:.2f}:1")

# ---- 3. piso de croma e faixa de luminosidade ------------------------------
print("\n== 3. Faixa de luminosidade e piso de croma (as 9 barras) ==")
off = [(n, c, round(oklch(c)[0],3)) for n, c in zip(nomes, bars) if not (LO <= oklch(c)[0] <= HI)]
lowc = [(n, c, round(oklch(c)[1],3)) for n, c in zip(nomes, bars) if oklch(c)[1] < CHROMA_FLOOR]
print(f"  [{'PASS' if not off else 'INFO'}] faixa L: " + (str(off) if off else "todas dentro"))
print(f"  [{'PASS' if not lowc else 'INFO'}] croma:   " + (str(lowc) if lowc else "todas >= 0.10"))

# ---- 4. transparencia: as 9 entre si ---------------------------------------
print("\n== 4. Transparencia — as 9 entre si (identidade tambem vem do NOME em cada celula) ==")
pares = sorted(((deltaE(bars[i], bars[j]), min(deltaE(bars[i],bars[j],'protan'), deltaE(bars[i],bars[j],'deutan')),
                 nomes[i], nomes[j]) for i, j in itertools.combinations(range(9), 2)), key=lambda t: t[0])
print("  5 pares mais proximos (normal / cvd):")
for dn, dc, a, b in pares[:5]:
    dentro = "mesma familia (rampa ordinal, esperado)" if \
        [s[1] for s in SUBJ if s[0]==a][0] == [s[1] for s in SUBJ if s[0]==b][0] else "FAMILIAS DIFERENTES"
    print(f"    {a:12s} <-> {b:12s}  normal {dn:5.1f}  cvd {dc:5.1f}   {dentro}")
entre = [p for p in pares if [s[1] for s in SUBJ if s[0]==p[2]][0] != [s[1] for s in SUBJ if s[0]==p[3]][0]]
print(f"\n  pior par ENTRE familias: {entre[0][2]} <-> {entre[0][3]}  normal {entre[0][0]:.1f}  cvd {entre[0][1]:.1f}")

# ---- status reservado ------------------------------------------------------
print("\n== 5. Status reservado vs identidade das materias ==")
STATUS = {"sucesso": mk(145, 0.55, 0.14), "perigo": mk(25, 0.55, 0.16), "neutro": "9AA4B2"}
for sn, sc in STATUS.items():
    pior = min((deltaE(sc, b), n) for b, n in zip(bars, nomes))
    print(f"  {sn:8s} {sc}  materia mais proxima: {pior[1]} (dE {pior[0]:.1f})")

print("\nBARS   =", bars)
print("INKS   =", inks)
print("TINTS  =", tints)
print("TINTS2 =", tints2)
print("\nRESULTADO:", "TODAS AS CHECAGENS DURAS PASSAM" if ok else "FALHOU")
