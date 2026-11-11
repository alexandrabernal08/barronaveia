#!/usr/bin/env python3
"""
RASCUNHO da jarra-passarinho com alça em argola — Barro na Veia
===============================================================

A jarra é um PASSARINHO: o bico da jarra é o bico do pássaro, o corpo bojudo
é a barriga e a argola é o rabo enrolado, que sai de um "pescoço" que desce
fundo pelas costas.

Modelo 3D da PEÇA (ainda não do molde), feito a partir de uma única foto
lateral. Serve para aprovar formato e proporções antes de gerar os moldes.

As proporções vêm da foto. O tamanho é calculado para a jarra caber pelo
menos --capacidade-min litros (padrão 2 L) até a altura do bico. Quando as
medidas reais chegarem, use --altura-total (e --capacidade-min 0).

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
    (1100, 145, 1060), (1000, 135, 985), (930, 127, 900), (845, 125, 690),
]
PX_BORDA = 845                            # borda reta e horizontal
BICO_PX = (60, 878)                       # ponta do bico (um pouco abaixo da borda)
PX_BICO_BAIXO = 905                       # onde a parte de baixo do bico encontra a parede
PX_PESCOCO_FUNDO = 1200                   # até onde o pescoço da alça desce pelas costas
ARGOLA_PX = dict(cx=1072, cy=722, d_ext=800, tubo=125, sx=1.03, sz=0.97)


@dataclass
class ParamsJarra:
    altura_total: float = 220.0     # mm, do apoio até o topo da argola (ajustado pela capacidade)
    capacidade_min: float = 2.0     # litros até a altura do bico; 0 = usa a altura_total como está
    largura_relativa: float = 0.80  # largura (lado a lado) / comprimento (frente-trás) do corpo
    parede: float = 5.0             # espessura de parede da peça (só para o rascunho)
    bico: float = 10.0              # quanto o bico avança além da parede (mm, na escala de 22 cm)
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


def z_borda(p: ParamsJarra) -> float:
    return mm(p, 0, PX_BORDA)[1]


def secao(p: ParamsJarra, xf: float, xc: float, z: float, encolhe: float, bico_amt: float) -> np.ndarray:
    a = (xc - xf) / 2 - encolhe
    b = (xc - xf) / 2 * p.largura_relativa - encolhe
    cx = (xc + xf) / 2
    t = np.linspace(0, 2 * np.pi, p.pontos, endpoint=False)
    e = 2.0 / p.expoente
    x = np.sign(np.cos(t)) * np.abs(np.cos(t)) ** e * a
    y = np.sign(np.sin(t)) * np.abs(np.sin(t)) ** e * b
    # bico de passarinho: a frente (cos t = -1) se estreita bastante e avança
    frente = np.clip(-np.cos(t), 0, 1) ** 10
    k = bico_amt / max(p.bico * escala(p) / (220.0 / (PX_APOIO - PX_TOPO)), 1e-6)
    x = x - bico_amt * frente
    y = y * (1 - 0.55 * k * np.clip(-np.cos(t), 0, 1) ** 4)
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


def bico_mm(p: ParamsJarra) -> float:
    return p.bico * escala(p) / (220.0 / (PX_APOIO - PX_TOPO))


def bico_em(p: ParamsJarra, z: float) -> float:
    """Quanto o bico avança em cada altura: nasce na parede e chega ao máximo
    na altura da ponta (parte de baixo do bico inclinada, como no passarinho)."""
    z0 = mm(p, 0, PX_BICO_BAIXO)[1]
    z1 = mm(p, 0, BICO_PX[1])[1]
    u = float(np.clip((z - z0) / (z1 - z0), 0, 1))
    return bico_mm(p) * (3 * u * u - 2 * u * u * u)


def corpo(p: ParamsJarra) -> Manifold:
    ff, fc, ztop = perfil(p)
    zr = z_borda(p)
    zs = np.r_[np.linspace(0, ztop, p.camadas), ztop + 10]
    ext = loft([secao(p, ff(min(z, ztop)), fc(min(z, ztop)), z, 0, bico_em(p, z)) for z in zs])
    t = p.parede
    zi = np.r_[np.linspace(t, ztop, p.camadas), ztop + 15]
    inn = loft([secao(p, ff(min(z, ztop)), fc(min(z, ztop)), z, t, max(bico_em(p, z) - 1, 0)) for z in zi])
    c = (ext - inn).trim_by_plane((0, 0, -1), -zr)               # borda reta e horizontal
    # ponta do bico arredondada e um pouco abaixo da borda (cabecinha do passarinho)
    xw = float(ff(zr)) + 2
    xt, zt = mm(p, *BICO_PX)
    xt -= 0.0
    cunha = CrossSection([np.array([[xt - 30, zt + 1.5], [xw, zr], [xw, zr + 30], [xt - 30, zr + 30]])])
    cunha = cunha.extrude(200).translate((0, 0, -100)).rotate((90, 0, 0))   # plano xz, espessura em y
    return c - cunha


def capacidade_l(p: ParamsJarra) -> float:
    """Volume interno até a altura da ponta do bico (litros)."""
    zt = mm(p, *BICO_PX)[1]
    return miolo(p).trim_by_plane((0, 0, -1), -zt).volume() / 1e6


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
    """Pescoço/rabo: liga o arco de baixo da argola às costas do corpo e desce
    FUNDO pelas costas (como na foto), deixando a argola inteira em destaque."""
    s = escala(p)
    r = ARGOLA_PX["tubo"] / 2 * s
    ff, fc, ztop = perfil(p)
    z_fundo = mm(p, 0, PX_PESCOCO_FUNDO)[1]
    angs = np.linspace(math.radians(205), math.radians(300), 26)
    pecas = []
    for i, a in enumerate(angs):
        x, z = ponto_argola(p, a)
        u = i / (len(angs) - 1)
        zc = (1 - u ** 0.8) * (z - 6) + u ** 0.8 * z_fundo          # desce até o fundo do pescoço
        zc = float(np.clip(zc, 10, ztop))
        abre = 1.15 + 0.5 * math.sin(u * math.pi)                   # alarga no meio, afina nas pontas
        xb = float(fc(zc)) - r * abre + 1.0                         # só encosta na parede
        pecas.append((Manifold.sphere(r * 0.98, 40).translate((x, 0, z)),
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
    m = loft([secao(p, ff(min(z, ztop)), fc(min(z, ztop)), z, t, max(bico_em(p, z) - 1, 0)) for z in zi])
    return m.trim_by_plane((0, 0, -1), -z_borda(p))  # só até a borda: a argola acima dela fica inteira


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
    if p.capacidade_min > 0:                       # escala a jarra inteira até caber a capacidade
        for _ in range(3):
            v = capacidade_l(p)
            p.altura_total *= (p.capacidade_min * 1.02 / v) ** (1 / 3)
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
    print(f"  capacidade até o bico: {capacidade_l(p):.2f} L")


def loft_vol(p: ParamsJarra) -> float:
    ff, fc, ztop = perfil(p)
    zz = np.linspace(p.parede, ztop - 8, 300)
    a = (fc(zz) - ff(zz)) / 2 - p.parede
    b = a * p.largura_relativa
    return float(np.trapezoid(math.pi * a * b * 0.93, zz))


if __name__ == "__main__":
    main()
