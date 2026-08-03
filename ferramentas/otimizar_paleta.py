# -*- coding: utf-8 -*-
"""Busca 9 cores categoricas maximizando a pior separacao (normal + protan + deutan)
dentro da faixa de luminosidade e do piso de croma do skill dataviz."""
import math, itertools, random
from validate_palette import (oklab_from_lin, lin, simulate, deltaE, oklch,
                              contrast, BAND, CHROMA_FLOOR)

random.seed(7)
LO, HI = BAND["light"]
CVD_TARGET, NORMAL_FLOOR = 8.0, 15.0


def lin2s(c):
    c = min(1.0, max(0.0, c))
    return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055


def oklch_to_hex(L, C, Hdeg):
    h = math.radians(Hdeg)
    a, b = C * math.cos(h), C * math.sin(h)
    l_ = L + 0.3963377774 * a + 0.2158037573 * b
    m_ = L - 0.1055613458 * a - 0.0638541728 * b
    s_ = L - 0.0894841775 * a - 1.2914855480 * b
    l, m, s = l_ ** 3, m_ ** 3, s_ ** 3
    r = 4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s
    g = -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s
    bl = -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s
    if min(r, g, bl) < -0.002 or max(r, g, bl) > 1.002:
        return None  # fora do gamut sRGB
    return "".join(f"{round(lin2s(v) * 255):02X}" for v in (r, g, bl))


# grade de candidatos
CANDS = []
L = 0.45
while L <= 0.755:
    C = 0.10
    while C <= 0.221:
        for H in range(0, 360, 5):
            hx = oklch_to_hex(L, C, H)
            if hx is None:
                continue
            Lr, Cr = oklch(hx)
            if not (LO <= Lr <= HI) or Cr < CHROMA_FLOOR:
                continue
            if contrast(hx, "#FFFFFF") < 3.0:
                continue
            CANDS.append((hx, H, L, C))
        C += 0.02
    L += 0.05
# dedup
seen, C2 = set(), []
for c in CANDS:
    if c[0] not in seen:
        seen.add(c[0]); C2.append(c)
CANDS = C2
print("candidatos em gamut/faixa/croma/contraste:", len(CANDS))

CACHE = {}
def score_pair(a, b):
    k = (a, b) if a < b else (b, a)
    if k not in CACHE:
        dn = deltaE(a, b) / NORMAL_FLOOR
        dp = deltaE(a, b, "protan") / CVD_TARGET
        dd = deltaE(a, b, "deutan") / CVD_TARGET
        CACHE[k] = min(dn, dp, dd)
    return CACHE[k]

def obj(sel):
    return min(score_pair(a, b) for a, b in itertools.combinations(sel, 2))

# 1) farthest-point greedy a partir de varias sementes
best = None
for seed_idx in random.sample(range(len(CANDS)), 60):
    sel = [CANDS[seed_idx][0]]
    while len(sel) < 9:
        nxt = max(CANDS, key=lambda c: min(score_pair(c[0], s) for s in sel) if c[0] not in sel else -1)
        sel.append(nxt[0])
    v = obj(sel)
    if best is None or v > best[0]:
        best = (v, list(sel))
print(f"apos greedy: pior par normalizado = {best[0]:.3f}")

# 2) melhoria local por troca
sel = best[1]
cur = best[0]
improved = True
rounds = 0
while improved and rounds < 40:
    improved = False
    rounds += 1
    for i in range(9):
        base = sel[:i] + sel[i+1:]
        cand_best, cand_val = None, cur
        for c, _, _, _ in CANDS:
            if c in base:
                continue
            v = min(min(score_pair(c, s) for s in base),
                    min(score_pair(a, b) for a, b in itertools.combinations(base, 2)))
            if v > cand_val + 1e-9:
                cand_val, cand_best = v, c
        if cand_best:
            sel[i] = cand_best
            cur = cand_val
            improved = True
print(f"apos busca local: pior par normalizado = {cur:.3f}")

# 3) ordenar por matiz e mostrar
info = []
for hx in sel:
    Lr, Cr = oklch(hx)
    a, b = oklab_from_lin(lin(hx))[1:]
    H = (math.degrees(math.atan2(b, a)) + 360) % 360
    info.append((H, hx, Lr, Cr))
info.sort()
print("\ncor      matiz     L      C     contraste/branco")
for H, hx, Lr, Cr in info:
    print(f"  {hx}   {H:6.1f}  {Lr:.3f}  {Cr:.3f}   {contrast(hx,'#FFFFFF'):.2f}")
print("\nlista:", ",".join(h for _, h, _, _ in info))
