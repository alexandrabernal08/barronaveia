#!/usr/bin/env python3
"""
RASCUNHO da jarra com alça em argola — Barro na Veia
====================================================

Modelo 3D da PEÇA (ainda não do molde), feito a partir de uma única foto
lateral. Serve para aprovar formato e proporções antes de gerar os moldes.

Medidas estimadas pela foto, com altura total de 22 cm (apoio até o topo
da argola). Quando as medidas reais chegarem, basta mudar --altura-total
e as proporções em PERFIL_* abaixo.

    python3 gerar_jarra.py               # gera stl/jarra/jarra_rascunho.stl
    python3 gerar_jarra.py --altura-total 200

Coordenadas: x = da frente (bico, negativo) para trás (alça, positivo),
y = de lado a lado, z = altura (0 no apoio).
"""

from __future__ import annotations

import argparse
import math
import os
from dataclasses import dataclass, fields

import numpy as np
import trimesh
from manifold3d import CrossSection, Manifold, Mesh

from gerar_moldes import para_trimesh

# --------------------------------------------------------------------------
# Medidas tiradas da foto (pixels da imagem original 1500 x 2000)
# --------------------------------------------------------------------------
PX_APOIO = 1800          # y do apoio
PX_TOPO = 345            # y do topo da argola
PX_CENTRO_X = 615        # x de referência (meio do corpo)
# contorno do CORPO visto de lado (sem a alça): (y, x_frente, x_costas)
PERFIL_PX = [
    (1797, 520, 650), (1780, 430, 760), (1750, 370, 850), (1700, 300, 930),
    (1650, 265, 990), (1600, 235, 1020), (1550, 205, 1040), (1500, 185, 1048),
    (1450, 175, 1055), (1400, 170, 1065), (1300, 158, 1085), (1200, 150, 1090),
    (1100, 145, 1060), (1000, 140, 985), (900, 125, 860), (820, 118, 720),
]
BICO_PX = (60, 870)                       # ponta do bico
BORDA_COSTAS_PX = (660, 805)              # borda no fundo da boca, junto da alça
ARGOLA_PX = dict(cx=1072, cy=722, d_ext=800, tubo=125, sx=1.03, sz=0.97)


@dataclass
class ParamsJarra:
    altura_total: float = 220.0     # mm, do apoio até o topo da argola
    largura_relativa: float = 0.80  # largura (lado a lado) / comprimento (frente-trás) do corpo
    parede: float = 5.0             # espessura de parede da peça (só para o rascunho)
    bico: float = 9.0               # quanto o bico avança além da borda (mm)
    expoente: float = 2.3           # 2 = elipse; maior = seção mais "quadrada"
    pontos: int = 180
    camadas: int = 90


def escala(p: ParamsJarra) -> float:
    return p.altura_total / (PX_APOIO - PX_TOPO)


def mm(p: ParamsJarra, x_px: float, y_px: float) -> tuple[float, float]:
    s = escala(p)
    return (x_px - PX_CENTRO_X) * s, (PX_APOIO - y_px) * s


def perfil(p: ParamsJarra):
    """Funções z -> (x_frente, x_costas), suavizadas por spline (traçado à mão da foto)."""
    from scipy.interpolate import UnivariateSpline
    pts = np.array([[*mm(p, xf, y), mm(p, xc, y)[0]] for y, xf, xc in PERFIL_PX])
    z, xf, xc = pts[:, 1], pts[:, 0], pts[:, 2]
    o = np.argsort(z)
    z, xf, xc = z[o], xf[o], xc[o]
    s = escala(p)
    sf = UnivariateSpline(z, xf, s=len(z) * (6 * s) ** 2)
    sc = UnivariateSpline(z, xc, s=len(z) * (6 * s) ** 2)
    return (lambda q: sf(np.asarray(q))), (lambda q: sc(np.asarray(q))), float(z.max())


def plano_borda(p: ParamsJarra):
    """Borda inclinada: mais baixa no bico, mais alta atrás. Devolve (normal, offset) do semiespaço de baixo."""
    xb, zb = mm(p, *BICO_PX)
    xa, za = mm(p, *BORDA_COSTAS_PX)
    incl = (za - zb) / (xa - xb)                           # dz/dx
    n = np.array([-incl, 0.0, 1.0]); n /= np.linalg.norm(n)
    return -n, -float(np.dot(n, [xb, 0, zb])), (xb, zb, incl)


def secao(p: ParamsJarra, xf: float, xc: float, z: float, encolhe: float, bico_amt: float) -> np.ndarray:
    a = (xc - xf) / 2 - encolhe
    b = (xc - xf) / 2 * p.largura_relativa - encolhe
    cx = (xc + xf) / 2
    t = np.linspace(0, 2 * np.pi, p.pontos, endpoint=False)
    e = 2.0 / p.expoente
    x = np.sign(np.cos(t)) * np.abs(np.cos(t)) ** e * a
    y = np.sign(np.sin(t)) * np.abs(np.sin(t)) ** e * b
    # bico: a frente (cos t = -1) se estreita e avança perto da borda
    frente = np.clip(-np.cos(t), 0, 1) ** 6
    x = x - bico_amt * frente
    y = y * (1 - 0.35 * (bico_amt / max(p.bico, 1e-6)) * frente)
    return np.c_[x + cx, y, np.full_like(x, z)]


def loft(secoes: list[np.ndarray]) -> Manifold:
    n, m = len(secoes[0]), len(secoes)
    v = np.vstack(secoes + [[[secoes[0][:, 0].mean(), 0, secoes[0][0, 2]]],
                            [[secoes[-1][:, 0].mean(), 0, secoes[-1][0, 2]]]])
    cb, ct = m * n, m * n + 1
    f = []
    for k in range(m - 1):
        for i in range(n):
            a, b = k * n + i, k * n + (i + 1) % n
            c, d = (k + 1) * n + (i + 1) % n, (k + 1) * n + i
            f += [[a, b, c], [a, c, d]]
    for i in range(n):
        f += [[cb, (i + 1) % n, i], [ct, (m - 1) * n + i, (m - 1) * n + (i + 1) % n]]
    tm = trimesh.Trimesh(v, np.array(f), process=True)
    trimesh.repair.fix_normals(tm)
    assert tm.is_volume
    return Manifold(Mesh(np.asarray(tm.vertices, np.float32), np.asarray(tm.faces, np.uint32)))


def corpo(p: ParamsJarra) -> Manifold:
    ff, fc, ztop = perfil(p)
    n_cima, off, (xb, zb, incl) = plano_borda(p)
    z_extra = ztop + 25                                      # passa da borda; o plano corta depois
    zs = np.r_[np.linspace(0, ztop, p.camadas), ztop + 8, z_extra]
    z_bico0 = zb - 35

    def bico_em(z):
        return p.bico * float(np.clip((z - z_bico0) / (zb - z_bico0), 0, 1)) ** 2

    ext = loft([secao(p, ff(min(z, ztop)) - (z - ztop) * 0.15 * (z > ztop), fc(min(z, ztop)), z, 0, bico_em(z)) for z in zs])
    t = p.parede
    zi = np.r_[np.linspace(t, ztop, p.camadas), ztop + 8, z_extra + 5]
    inn = loft([secao(p, ff(min(z, ztop)) - (z - ztop) * 0.15 * (z > ztop), fc(min(z, ztop)), z, t, bico_em(z)) for z in zi])
    oca = ext - inn
    return oca.trim_by_plane(tuple(n_cima), off)


def argola(p: ParamsJarra) -> Manifold:
    s = escala(p)
    cx, cz = mm(p, ARGOLA_PX["cx"], ARGOLA_PX["cy"])
    R = (ARGOLA_PX["d_ext"] - ARGOLA_PX["tubo"]) / 2 * s
    r = ARGOLA_PX["tubo"] / 2 * s
    tor = Manifold.revolve(CrossSection.circle(r, 48).translate((R, 0)), 160)   # eixo z
    tor = tor.scale((ARGOLA_PX["sx"], ARGOLA_PX["sz"], 1.0))
    return tor.rotate((90, 0, 0)).translate((cx, 0, cz))                         # plano xz


def ponto_argola(p: ParamsJarra, ang: float) -> tuple[float, float]:
    s = escala(p)
    cx, cz = mm(p, ARGOLA_PX["cx"], ARGOLA_PX["cy"])
    R = (ARGOLA_PX["d_ext"] - ARGOLA_PX["tubo"]) / 2 * s
    return cx + R * ARGOLA_PX["sx"] * math.cos(ang), cz + R * ARGOLA_PX["sz"] * math.sin(ang)


def pescoco(p: ParamsJarra) -> Manifold:
    """Junção da argola com as costas: uma "membrana" da espessura do tubo que
    preenche o espaço entre o arco de baixo/esquerda da argola e o corpo."""
    s = escala(p)
    r = ARGOLA_PX["tubo"] / 2 * s
    ff, fc, ztop = perfil(p)
    angs = np.linspace(math.radians(200), math.radians(290), 22)
    pecas = []
    for i, a in enumerate(angs):
        x, z = ponto_argola(p, a)
        # ponto correspondente na parede do corpo, um pouco abaixo e para dentro
        u = i / (len(angs) - 1)
        zc = float(np.clip(z - 10 - 14 * math.sin(u * math.pi), 10, ztop))
        xb = None
        abre = 1.25 + 0.45 * math.sin(u * math.pi)               # alarga suavemente até o corpo
        xb = float(fc(zc)) - r * abre + 1.5                       # a esfera só encosta na parede
        pecas.append((Manifold.sphere(r * 0.98, 40).translate((x, 0, z)),   # mesma grossura do tubo
                      Manifold.sphere(r * abre, 40).translate((xb, 0, zc))))
    web = Manifold()
    for (a1, b1), (a2, b2) in zip(pecas[:-1], pecas[1:]):
        web = web + Manifold.batch_hull([a1, a2, b1, b2])
    return web


def miolo(p: ParamsJarra) -> Manifold:
    """Espaço interno da jarra (para a alça não invadir)."""
    ff, fc, ztop = perfil(p)
    t = p.parede
    zi = np.r_[np.linspace(t, ztop, p.camadas), ztop + 30]
    m = loft([secao(p, ff(min(z, ztop)), fc(min(z, ztop)), z, t, 0) for z in zi])
    n_cima, off, _ = plano_borda(p)
    return m.trim_by_plane(tuple(n_cima), off)      # só até a borda: a argola acima dela fica inteira


def jarra(p: ParamsJarra) -> Manifold:
    alca = (argola(p) + pescoco(p)) - miolo(p)     # a alça não invade o interior
    return corpo(p) + alca


def main() -> None:
    p = ParamsJarra()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    for f in fields(p):
        ap.add_argument("--" + f.name.replace("_", "-"), type=type(getattr(p, f.name)), default=getattr(p, f.name))
    raiz = os.path.dirname(os.path.abspath(__file__))
    ap.add_argument("--saida", default=os.path.join(raiz, "stl", "jarra"))
    a = ap.parse_args()
    p = ParamsJarra(**{f.name: getattr(a, f.name) for f in fields(p)})
    os.makedirs(a.saida, exist_ok=True)
    tm = para_trimesh(jarra(p))
    tm.export(os.path.join(a.saida, "jarra_rascunho.stl"))
    ff, fc, ztop = perfil(p)
    s = escala(p)
    zz = np.linspace(0, ztop, 200)
    comp = (fc(zz) - ff(zz)).max()
    print(f"[jarra – rascunho]  fechado: {tm.is_watertight}")
    print(f"  altura total {tm.extents[2]:.0f} mm · corpo: altura {ztop:.0f}, comprimento {comp:.0f}, "
          f"largura ~{comp*p.largura_relativa:.0f} mm")
    print(f"  argola: Ø externo {ARGOLA_PX['d_ext']*s:.0f} mm, tubo Ø {ARGOLA_PX['tubo']*s:.0f} mm")
    print(f"  volume interno aproximado: {(loft_vol(p))/1e6:.2f} L")


def loft_vol(p: ParamsJarra) -> float:
    ff, fc, ztop = perfil(p)
    zz = np.linspace(p.parede, ztop - 8, 300)
    a = (fc(zz) - ff(zz)) / 2 - p.parede
    b = a * p.largura_relativa
    return float(np.trapezoid(math.pi * a * b * 0.93, zz))


if __name__ == "__main__":
    main()
