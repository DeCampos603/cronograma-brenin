# -*- coding: utf-8 -*-
"""Porte Python do validate_palette.js do skill dataviz (mesmos limiares e modelo Machado 2009)."""
import sys, math, itertools

BAND = {"light": (0.43, 0.77), "dark": (0.48, 0.67)}
CHROMA_FLOOR = 0.10
CVD_TARGET, CVD_FLOOR = 8.0, 6.0
NORMAL_FLOOR = 15.0
CONTRAST_MIN = 3.0

MACHADO = {
 "protan": [[0.152286, 1.052583, -0.204868],
            [0.114503, 0.786281, 0.099216],
            [-0.003882, -0.048116, 1.051998]],
 "deutan": [[0.367322, 0.860646, -0.227968],
            [0.280085, 0.672501, 0.047413],
            [-0.011820, 0.042940, 0.968881]],
 "tritan": [[1.255528, -0.076749, -0.178779],
            [-0.078411, 0.930809, 0.147602],
            [0.004733, 0.691367, 0.303900]],
}

def hex2srgb(h):
    h = h.strip().lstrip("#")
    return [int(h[i:i+2], 16) / 255 for i in (0, 2, 4)]

def s2lin(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

def lin(h):
    return [s2lin(c) for c in hex2srgb(h)]

def rel_lum(h):
    r, g, b = lin(h)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def contrast(a, b):
    hi, lo = sorted([rel_lum(a), rel_lum(b)], reverse=True)
    return (hi + 0.05) / (lo + 0.05)

def oklab_from_lin(rgb):
    r, g, b = rgb
    l = (0.4122214708*r + 0.5363325363*g + 0.0514459929*b) ** (1/3)
    m = (0.2119034982*r + 0.6806995451*g + 0.1073969566*b) ** (1/3)
    s = (0.0883024619*r + 0.2817188376*g + 0.6299787005*b) ** (1/3)
    return [0.2104542553*l + 0.7936177850*m - 0.0040720468*s,
            1.9779984951*l - 2.4285922050*m + 0.4505937099*s,
            0.0259040371*l + 0.7827717662*m - 0.8086757660*s]

def oklch(h):
    L, a, b = oklab_from_lin(lin(h))
    return L, math.hypot(a, b)

def simulate(h, kind):
    r, g, b = lin(h); M = MACHADO[kind]
    return [min(1, max(0, M[i][0]*r + M[i][1]*g + M[i][2]*b)) for i in range(3)]

def deltaE(h1, h2, kind=None):
    a = oklab_from_lin(simulate(h1, kind) if kind else lin(h1))
    b = oklab_from_lin(simulate(h2, kind) if kind else lin(h2))
    return 100 * math.dist(a, b)

def validate(palette, mode="light", surface="#FFFFFF", pairs="adjacent", names=None):
    lo, hi = BAND[mode]
    names = names or palette
    ok = True
    print(f"\nPaleta ({mode}, superficie {surface}, pares {pairs}): {len(palette)} cores")

    off = [(n, c, round(oklch(c)[0], 3)) for n, c in zip(names, palette)
           if not (lo <= oklch(c)[0] <= hi)]
    if off: ok = False
    print(f"  [{'PASS' if not off else 'FAIL'}] Faixa de luminosidade   " +
          (f"fora da faixa: {off}" if off else f"todas dentro de L {lo}-{hi}"))

    lowc = [(n, c, round(oklch(c)[1], 3)) for n, c in zip(names, palette) if oklch(c)[1] < CHROMA_FLOOR]
    if lowc: ok = False
    print(f"  [{'PASS' if not lowc else 'FAIL'}] Piso de croma           " +
          (f"abaixo do piso (le como cinza): {lowc}" if lowc else f"todas >= {CHROMA_FLOOR}"))

    n = len(palette)
    if pairs == "all":
        pl = list(itertools.combinations(range(n), 2))
    else:
        pl = [(i, i+1) for i in range(n-1)]

    worst = None
    for kind in ("protan", "deutan"):
        for i, j in pl:
            d = deltaE(palette[i], palette[j], kind)
            if worst is None or d < worst[0]:
                worst = (d, kind, names[i], names[j])
    tri = min(deltaE(palette[i], palette[j], "tritan") for i, j in pl)
    state = "PASS" if worst[0] >= CVD_TARGET else ("WARN" if worst[0] >= CVD_FLOOR else "FAIL")
    if state == "FAIL": ok = False
    print(f"  [{state}] Separacao CVD           pior par {worst[2]} <-> {worst[3]}  dE {worst[0]:.1f} ({worst[1]}) · tritan {tri:.1f}")

    nworst = min(((deltaE(palette[i], palette[j]), names[i], names[j]) for i, j in pl), key=lambda t: t[0])
    nstate = "PASS" if nworst[0] >= NORMAL_FLOOR else "FAIL"
    if nstate == "FAIL": ok = False
    print(f"  [{nstate}] Piso de visao normal    pior par {nworst[1]} <-> {nworst[2]}  dE {nworst[0]:.1f}")

    low = [(n_, c, round(contrast(c, surface), 2)) for n_, c in zip(names, palette)
           if contrast(c, surface) < CONTRAST_MIN]
    print(f"  [{'PASS' if not low else 'WARN'}] Contraste vs superficie " +
          (f"abaixo de {CONTRAST_MIN}:1 (exige rotulo visivel): {low}" if low else f"todas >= {CONTRAST_MIN}:1"))

    print(f"\n  -> {'TODAS AS CHECAGENS PASSAM' if ok else 'FALHOU — corrigir as marcadas'}")
    return ok

if __name__ == "__main__":
    raw = sys.argv[1]
    mode = "light"
    surface = "#FFFFFF"
    pairs = "adjacent"
    names = None
    for i, a in enumerate(sys.argv[2:], start=2):
        if a.startswith("--mode="): mode = a.split("=")[1]
        elif a.startswith("--surface="): surface = a.split("=")[1]
        elif a.startswith("--pairs="): pairs = a.split("=")[1]
        elif a.startswith("--names="): names = a.split("=", 1)[1].split(",")
    pal = [c.strip() for c in raw.split(",") if c.strip()]
    sys.exit(0 if validate(pal, mode, surface, pairs, names) else 1)
