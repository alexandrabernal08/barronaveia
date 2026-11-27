#!/usr/bin/env python3
"""
Molde de gesso de 2 PARTES para a CANECA com alça de furo (alça em bloco) — Barro na Veia
========================================================================================

Caneca de corpo quase reto, fundo arredondado e uma ALÇA EM BLOCO grudada na lateral,
com um furo em "D" para o dedo. Referência: fotos de produto (8 cm / 180 ml);
medidas pedidas para a peça QUEIMADA: altura 10 cm e 300 ml.

Um molde só, com corpo e alça juntos, dividido em DUAS METADES pelo meio da alça.
Cada metade da alça forma metade do furo, e as duas se encontram na divisão.

  stl/caneca/
  * bandeja_A.stl / bandeja_B.stl -> meia caneca deitada (com meia alça) + chaves
  * moldura_U.stl / moldura_U_logo.stl -> moldura (1 lisa + 1 com o logo)
  * presilha.stl (4x) · pino.stl (2x)

    python3 gerar_caneca.py --peca         # também exporta a peça queimada, para conferir
    python3 gerar_caneca.py --capacidade 250 --altura 95
"""

from __future__ import annotations

import argparse
import math
import os
from dataclasses import dataclass, fields

import numpy as np
from manifold3d import CrossSection, FillRule, Manifold
from shapely.geometry import Point, Polygon, box

from gerar_moldes import Params as ParamsPrato, para_trimesh, presilha, receita
from marca import relevo_local


@dataclass
class ParamsCaneca:
    # Peça QUEIMADA (como fica pronta)
    altura: float = 100.0          # mm
    capacidade: float = 300.0      # ml até a borda
    parede_peca: float = 4.5       # parede da peça queimada (só para calcular a capacidade)
    afina_boca: float = 1.0        # raio da boca / raio do corpo
    raio_fundo: float = 24.0       # arredondado do fundo (formato de "U")
    # Alça em bloco (peça queimada)
    alca_espessura: float = 22.0   # grossura da alça (igual à da foto)
    alca_espessura_base: float = 22.0  # grossura onde a alça nasce do corpo
    alca_barra: float = 12.0       # largura da barra de fora da alça (onde se segura)
    alca_base: float = 0.14        # início da alça (fração da altura)
    alca_topo_folga: float = 0.0   # 0 = topo da alça rente à borda
    furo_largura: float = 20.0     # largura do furo em "D"
    furo_altura: float = 46.0
    concha_fundura: float = 10.0   # quanto a parede afunda em volta do furo (a "concha" da foto)
    concha_altura: float = 66.0    # altura da concha (maior que o furo)
    concha_maciez: float = 4.0     # quanto mais, mais macia a borda da concha
    furo_centro: float = 0.55      # altura do centro do furo (fração da altura)
    arredonda: float = 5.0         # arredondado das quinas da alça
    # Molde
    aumento: float = 20.0          # % — molde maior que a peça queimada (retração da barbotina)
    altura_reservatorio: float = 20.0
    degrau_corte: float = 2.0
    saida_reservatorio: float = 5.0
    margem_gesso: float = 25.0
    parede: float = 4.0
    aba_presilha: float = 10.0
    folga: float = 0.25
    espessura_base: float = 3.0
    altura_plug: float = 4.0
    raio_chave: float = 4.5
    folga_chave: float = 0.4
    canal_desmolde: bool = True
    diametro_canal: float = 4.2
    diametro_pino: float = 3.9
    diametro_bolso: float = 30.0
    profundidade_bolso: float = 12.0
    diametro_cabeca_pino: float = 16.0
    espessura_cabeca_pino: float = 3.0
    saliencia_pino: float = 0.2
    logo: bool = True
    logo_largura: float = 46.0
    logo_profundidade: float = 1.0
    logo_arquivo: str = ""
    segmentos: int = 256


# --------------------------------------------------------------------------
# Corpo (peça queimada) e cálculo do raio pela capacidade
# --------------------------------------------------------------------------
def contorno_corpo(p: ParamsCaneca, R: float, n: int = 40) -> list[tuple[float, float]]:
    H, rc = p.altura, p.raio_fundo
    pts = [(0.0, 0.0), (R - rc, 0.0)]
    for t in np.linspace(-math.pi / 2, 0, n)[1:]:
        pts.append((R - rc + rc * math.cos(t), rc + rc * math.sin(t)))
    pts += [(R, 0.5 * H)]
    for u in np.linspace(0, 1, n)[1:]:
        pts.append((R * (1 - (1 - p.afina_boca) * u * u), 0.5 * H + 0.5 * H * u))
    return pts


def volume_interno_ml(p: ParamsCaneca, R: float) -> float:
    pts = contorno_corpo(p, R)
    reg = Polygon(pts + [(0, p.altura)]).buffer(0)
    dentro = reg.buffer(-p.parede_peca, join_style=1).union(
        box(0, p.altura - 10, pts[-1][0] - p.parede_peca, p.altura + 5)).intersection(box(0, 0, 1e3, p.altura))
    xy = np.asarray(dentro.exterior.coords)[:-1]
    xy[:, 0] = np.maximum(xy[:, 0], 0)
    if not dentro.exterior.is_ccw:
        xy = xy[::-1]
    return Manifold.revolve(CrossSection([xy]), 128).volume() / 1000.0


_cache_raio: dict = {}


def escala(p: ParamsCaneca) -> float:
    return 1.0 + p.aumento / 100.0


def saliencia(p: ParamsCaneca) -> float:
    """Quanto a alça sai além do corpo."""
    return p.furo_largura - p.concha_fundura + p.alca_barra


# ---- concha: o corpo afunda em volta do furo (curva e macia, como na foto) ----
def x_concha(p: ParamsCaneca, R: float, z: np.ndarray, recuo: float = 0.0) -> np.ndarray:
    """Até onde a parede vai, na direção da alça, em cada altura (a 'concha').
    Fora da concha devolve um valor alto (não corta nada)."""
    zc = p.furo_centro * p.altura
    hz = p.concha_altura / 2
    u = np.clip(1 - ((z - zc) / hz) ** 2, 0, 1)
    f = u ** 1.3                                        # 1 no centro, 0 nas pontas, sem quina
    return R - recuo - p.concha_fundura * f + 60 * (1 - f) ** 3


def amassa(p: ParamsCaneca, m: Manifold, R: float, recuo: float = 0.0) -> Manifold:
    """Empurra a parede do lado da alça para dentro até a concha, com transição suave
    (mínimo suave). Para cada altura, a parede só RECUA conforme se afasta do meio
    (y = 0), então o molde dividido nesse plano solta sem prender."""
    k = p.concha_maciez
    m = m.refine_to_length(1.5)

    def f(v: np.ndarray) -> np.ndarray:
        x, y, z = v[:, 0], v[:, 1], v[:, 2]
        xs = x_concha(p, R, z, recuo)
        a, b = x / k, xs / k
        mn = np.minimum(a, b)
        smin = k * (mn - np.log(np.exp(-(a - mn)) + np.exp(-(b - mn))))
        nx = np.where(x > 0, np.minimum(x, smin), x)
        return np.c_[nx, y, z]

    return m.warp_batch(f)


def revolve_contorno(p: ParamsCaneca, pts: list, seg: int) -> Manifold:
    return Manifold.revolve(CrossSection([np.array(pts)]), seg)


def interno(p: ParamsCaneca, R: float, seg: int = 96) -> Manifold:
    """Espaço interno da caneca pronta (a parede acompanha a concha: 'barriga interna')."""
    pts = contorno_corpo(p, R)
    reg = Polygon(pts + [(0, p.altura)]).buffer(0)
    t = p.parede_peca
    dentro = reg.buffer(-t, join_style=1).union(
        box(0, p.altura - 10, pts[-1][0] - t, p.altura + 5)).union(
        box(-1, t + 2, 8, p.altura + 5))                           # vai até o eixo (sem "pino" no meio)
    dentro = dentro.intersection(box(0, 0, 1e3, p.altura))
    dentro = max(getattr(dentro, "geoms", [dentro]), key=lambda g: g.area)
    xy = np.asarray(dentro.exterior.coords)[:-1]
    xy[:, 0] = np.maximum(xy[:, 0], 0)
    if not dentro.exterior.is_ccw:
        xy = xy[::-1]
    return amassa(p, Manifold.revolve(CrossSection([xy]), seg), R, recuo=t)


def capacidade_ml(p: ParamsCaneca, R: float, seg: int = 96) -> float:
    return interno(p, R, seg).volume() / 1000.0


def raio_corpo(p: ParamsCaneca) -> float:
    chave = tuple(sorted(vars(p).items()))
    if chave in _cache_raio:
        return _cache_raio[chave]
    lo, hi = 25.0, 70.0
    for _ in range(18):
        mid = (lo + hi) / 2
        if capacidade_ml(p, mid, 64) < p.capacidade:
            lo = mid
        else:
            hi = mid
    _cache_raio[chave] = (lo + hi) / 2
    return _cache_raio[chave]


def forma_alca_2d(p: ParamsCaneca, R: float):
    """Contorno da alça visto de lado (plano xz) e o furo. O furo vai fundo: o lado
    curvo dele é a própria concha do corpo (como na foto)."""
    H = p.altura
    z0, z1 = p.alca_base * H, H - p.alca_topo_folga
    x_out = R - p.concha_fundura + p.furo_largura              # lado reto do furo (de fora)
    xo = x_out + p.alca_barra
    z1 = z1 + p.arredonda + 2                                  # passa da borda; é aparado depois
    bloco = box(R - 30, z0, xo, z1)                             # a parte de dentro some no corpo
    r = 16.0
    bloco = bloco.buffer(-r, join_style=1).buffer(r, join_style=1).union(box(R - 30, z0 + r, R - 12, z1 - r))
    zc = p.furo_centro * H
    from shapely.affinity import scale, translate
    elipse = translate(scale(Point(0, 0).buffer(1, resolution=96), p.furo_largura + 16, p.furo_altura / 2,
                             origin=(0, 0)), x_out, zc)
    furo = elipse.intersection(box(R - 40, zc - p.furo_altura, x_out, zc + p.furo_altura))
    furo = furo.buffer(-3, join_style=1).buffer(3, join_style=1)
    from shapely.geometry.polygon import orient
    return orient(bloco, 1.0), orient(furo, 1.0)


def prisma_furo(p: ParamsCaneca, R: float, furo: Polygon | None = None) -> Manifold:
    if furo is None:
        furo = forma_alca_2d(p, R)[1]
    fxy = np.asarray(furo.simplify(0.05).exterior.coords)[:-1]
    L = p.alca_espessura_base
    return CrossSection([fxy], FillRule.EvenOdd).extrude(2 * L).translate((0, 0, -L)).rotate((90, 0, 0))


def peca(p: ParamsCaneca, com_reservatorio: bool = False, oca: bool = False) -> Manifold:
    R = raio_corpo(p)
    pts = contorno_corpo(p, R)
    H = p.altura
    if com_reservatorio:
        S = p.altura_reservatorio / escala(p)
        rb = pts[-1][0]
        rs = rb + p.degrau_corte / escala(p)
        pts = pts + [(rs, H), (rs + S * math.tan(math.radians(p.saida_reservatorio)), H + S), (0.0, H + S)]
    else:
        pts = pts + [(0.0, H)]
    corpo = amassa(p, revolve_contorno(p, pts, p.segmentos), R)
    # alça em bloco (arredondada), com o furo
    bloco, furo = forma_alca_2d(p, R)
    f = p.arredonda
    nucleo = bloco.buffer(-f, join_style=1)
    cs = CrossSection([np.asarray(nucleo.exterior.coords)[:-1]], FillRule.EvenOdd)
    lam = cs.extrude(p.alca_espessura_base - 2 * f).translate((0, 0, -(p.alca_espessura_base - 2 * f) / 2))
    lam = lam.rotate((90, 0, 0))                                   # plano xz, espessura em y
    xo = R + saliencia(p)
    hb = max(p.alca_espessura_base / 2 - f, 0.5)
    ho = max(p.alca_espessura / 2 - f, 0.5)
    cunha = CrossSection([np.array([[R - 32, -hb], [xo + 1, -ho], [xo + 1, ho], [R - 32, hb]])])
    lam = lam ^ cunha.extrude(H + 40).translate((0, 0, -10))
    # furo com bordas arredondadas: tira o furo "engordado" antes de arredondar
    lam = lam - prisma_furo(p, R, furo.buffer(f, join_style=1))
    alca = lam.minkowski_sum(Manifold.sphere(f, 32)).trim_by_plane((0, 0, -1), -H)   # topo rente à borda
    alca = alca - prisma_furo(p, R, furo)                          # garante o furo aberto até a concha
    m = corpo + alca
    if oca:
        m = m - interno(p, R, p.segmentos)
    return m


# --------------------------------------------------------------------------
def dados(p: ParamsCaneca) -> dict:
    k = escala(p)
    R = raio_corpo(p)
    c = saliencia(p) / 2 * k                                  # centraliza corpo+alça
    meia = math.ceil((R + saliencia(p) / 2) * k + p.margem_gesso)
    v1 = (p.altura + p.altura_reservatorio / k) * k
    return {"R": R, "k": k, "c": c, "meia": meia, "v0": -p.margem_gesso, "v1": v1, "esp": math.ceil(R * k + p.margem_gesso)}


def peca_bandeja(p: ParamsCaneca) -> Manifold:
    d = dados(p)
    m = peca(p, com_reservatorio=True).scale((d["k"],) * 3).translate((-d["c"], 0, 0))
    return m.rotate((-90, 0, 0))                                   # (x,y,z) -> (x, z, -y)


def meio(p: ParamsCaneca) -> Manifold:
    d = dados(p)
    return peca_bandeja(p).trim_by_plane((0, 0, 1), -0.5).trim_by_plane((0, -1, 0), -(d["v1"] - p.folga))


def chaves(p: ParamsCaneca) -> list[tuple[float, float]]:
    d = dados(p)
    uc = d["meia"] - p.margem_gesso / 2
    return [(s * uc, v) for s in (-1, 1) for v in (d["v1"] * 0.2, d["v1"] * 0.85)]


def ponto_canal(p: ParamsCaneca) -> tuple[float, float, float]:
    d = dados(p)
    pts = contorno_corpo(p, d["R"])
    h = 0.4 * p.altura
    r = float(np.interp(h, [q[1] for q in pts[1:]], [q[0] for q in pts[1:]]))
    return -d["c"], h * d["k"], r * d["k"]


def bandeja(p: ParamsCaneca, lado: str) -> Manifold:
    d = dados(p)
    M, v0, v1, E = d["meia"], d["v0"], d["v1"], d["esp"]
    aba = CrossSection.square((2 * (M + p.parede + 3), v1 - v0 + 2 * (p.parede + 3))).translate(
        (-(M + p.parede + 3), v0 - p.parede - 3))
    plug = CrossSection.square((2 * (M - p.folga), v1 - v0 - 2 * p.folga)).translate((-(M - p.folga), v0 + p.folga))
    b = (aba.extrude(p.espessura_base).translate((0, 0, -p.altura_plug - p.espessura_base))
         + plug.extrude(p.altura_plug + 0.01).translate((0, 0, -p.altura_plug)))
    b = b + meio(p)
    for u, v in chaves(p):
        if lado == "A":
            b = b + Manifold.sphere(p.raio_chave, 48).translate((u, v, 0)).trim_by_plane((0, 0, 1), 0)
        else:
            b = b - Manifold.sphere(p.raio_chave - p.folga_chave, 48).translate((u, v, 0))
    if p.canal_desmolde:
        uc, vc, wc = ponto_canal(p)
        base = -p.altura_plug - p.espessura_base
        rc = p.diametro_canal / 2
        b = b - Manifold.cylinder(wc - base + 2, rc, rc, 48).translate((uc, vc, base - 1))
        b = b - Manifold.cylinder(p.profundidade_bolso + 1, p.diametro_bolso / 2, p.diametro_bolso / 2, 96).translate((uc, vc, base - 1))
    return b


def pino(p: ParamsCaneca) -> Manifold:
    _, _, wc = ponto_canal(p)
    L = p.espessura_base + p.altura_plug + wc - p.profundidade_bolso + p.saliencia_pino
    cab = Manifold.cylinder(p.espessura_cabeca_pino, p.diametro_cabeca_pino / 2, p.diametro_cabeca_pino / 2, 96)
    r = p.diametro_pino / 2
    haste = Manifold.cylinder(L - 0.6, r, r, 48) + Manifold.cylinder(0.6, r, r - 0.4, 48).translate((0, 0, L - 0.6))
    return cab + haste.translate((0, 0, p.espessura_cabeca_pino))


def moldura_u(p: ParamsCaneca, logo: bool = False) -> tuple[Manifold, str]:
    d = dados(p)
    M, v0, v1, t, E = d["meia"], d["v0"], d["v1"], p.parede, d["esp"]
    vm = (v0 + v1) / 2
    ext = CrossSection.square((2 * (M + t), v1 - v0 + 2 * t)).translate((-(M + t), v0 - t))
    inte = CrossSection.square((2 * M, v1 - v0)).translate((-M, v0))
    corte = CrossSection.square((2 * (M + t) + 2, v1 - vm + t + 1)).translate((-(M + t) - 1, vm))
    u = (ext - inte) ^ corte
    for s in (-1, 1):
        x0 = M if s > 0 else -(M + t + p.aba_presilha)
        u = u + CrossSection.square((t + p.aba_presilha, t)).translate((x0, vm))
    m = u.extrude(p.altura_plug + E)
    origem = ""
    if logo:
        rel, alt, origem = relevo_local(p.logo_largura, p.logo_profundidade, virado=False,
                                        arquivo=p.logo_arquivo or None)
        assert alt + 10 < v1 - vm and p.logo_largura + 10 < E, "logo grande demais: diminua --logo-largura"
        vc = vm + 5 + alt / 2
        wc = p.altura_plug + E / 2
        dd = p.logo_profundidade
        # lado SEM alça (u = -M): visto de fora, x = direita = +w ; y = cima = +v ; z = para dentro (-u)
        T = np.array([[0, 0, -1, -M + dd], [0, 1, 0, vc], [1, 0, 0, wc]], dtype=np.float64)
        m = m + rel.transform(T)
    return m.translate((0, -vm, 0)), origem


# --------------------------------------------------------------------------
def main() -> None:
    p = ParamsCaneca()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    for f in fields(p):
        v = getattr(p, f.name)
        opt = "--" + f.name.replace("_", "-")
        if isinstance(v, bool):
            ap.add_argument(opt, type=lambda s: s.lower() in ("1", "sim", "true", "s"), default=v)
        else:
            ap.add_argument(opt, type=type(v), default=v)
    raiz = os.path.dirname(os.path.abspath(__file__))
    ap.add_argument("--saida", default=os.path.join(raiz, "stl", "caneca"))
    ap.add_argument("--peca", action="store_true", help="exporta também a peça queimada, para conferir")
    a = ap.parse_args()
    p = ParamsCaneca(**{f.name: getattr(a, f.name) for f in fields(p)})
    d = dados(p)
    os.makedirs(a.saida, exist_ok=True)

    pecas = {"bandeja_A": bandeja(p, "A"), "bandeja_B": bandeja(p, "B")}
    pecas["moldura_U"], _ = moldura_u(p, False)
    if p.logo:
        pecas["moldura_U_logo"], origem = moldura_u(p, True)
        print(f"  logo: {origem}")
    pecas["presilha"] = presilha(ParamsPrato(parede=p.parede, aba_presilha=p.aba_presilha))
    if p.canal_desmolde:
        pecas["pino"] = pino(p)
    if a.peca:
        pecas["peca_caneca_conferencia"] = peca(p, oca=True)
    print("[caneca]")
    for nome, m in pecas.items():
        tm = para_trimesh(m)
        assert tm.is_watertight, f"{nome} não está fechado"
        tm.export(os.path.join(a.saida, f"{nome}.stl"))
        dx, dy, dz = tm.extents
        print(f"  {nome:24s} {dx:6.1f} x {dy:6.1f} x {dz:5.1f} mm")
    R, k = d["R"], d["k"]
    print(f"  Peça queimada: altura {p.altura:.0f} mm, corpo Ø {2*R:.1f} mm, com a alça {2*R + saliencia(p):.0f} mm,"
          f" capacidade {capacidade_ml(p, R):.0f} ml")
    print(f"  Peça crua (no molde, +{p.aumento:.0f}%): altura {p.altura*k:.0f} mm, corpo Ø {2*R*k:.0f} mm")
    bloco = Manifold.cube((2 * d["meia"], d["v1"] - d["v0"], d["esp"])).translate((-d["meia"], d["v0"], 0))
    v = (bloco - peca_bandeja(p)).volume() / 1000.0
    g, w = receita(v)
    print(f"  Bloco montado: {2*d['esp']} x {2*d['meia']} x {d['v1']-d['v0']:.0f} mm")
    print(f"  Gesso POR METADE: ~{v/1000:.2f} L -> {g/1000:.2f} kg de gesso + {w/1000:.2f} L de água")


if __name__ == "__main__":
    main()
