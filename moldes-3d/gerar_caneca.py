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

from gerar_moldes import Params as ParamsPrato, loft, para_trimesh, presilha, raio_polar, receita
from marca import relevo_local


@dataclass
class ParamsCaneca:
    # Peça QUEIMADA (como fica pronta)
    altura: float = 80.0           # mm (medida da foto)
    largura_total: float = 77.0    # mm, corpo + alça (medida da foto)
    capacidade: float = 180.0      # ml até a borda (medida da foto)
    parede_peca: float = 4.0       # parede da peça queimada (só para calcular a capacidade)
    afina_boca: float = 1.0        # raio da boca / raio do corpo
    raio_fundo: float = 18.0       # arredondado do fundo (formato de "U")
    # Alça em bloco (peça queimada). Ela quase não sai do corpo: a largura total já a inclui.
    alca_espessura: float = 15.0   # grossura da alça (mais estreita, como nas fotos)
    alca_espessura_base: float = 15.0  # (mesmo valor: a alça nasce do próprio corpo)
    alca_concordancia: float = 7.0 # raio da curva que une a alça ao corpo (vista de cima)
    alca_barra: float = 8.0        # barra de fora (onde se segura), arredondada
    alca_base: float = 0.05        # a alça desce até perto do fundo, acompanhando o "U"
    alca_topo_folga: float = 0.0   # 0 = topo da alça rente à borda (topo reto, como na foto)
    furo_altura: float = 38.0      # altura do furo em "D"
    furo_centro: float = 0.54      # altura do centro do furo (fração da altura)
    furo_largura_mm: float = 18.0  # largura do furo no meio (do fundo da curva até a barra)
    furo_canto: float = 6.0        # raio das curvas onde o furo encontra a alça (sem quina)
    rampa_fundura: float = 0.0     # (desligado)
    rampa_largura: float = 5.0
    meia_lua_abre: float = 6.0     # quanto o túnel do furo abre ao sair na lateral (meia-lua arredondada)
    concha_fundura: float = 12.0   # quanto a barriga invertida entra no meio (cintura)
    concha_inicio: float = 0.08    # onde a curva começa embaixo (fração da altura)
    concha_fim: float = 1.04       # onde ela termina em cima (passa um pouco da borda)
    maciez_interna: float = 7.0    # barriga interna bem lisa (sem degrau)
    concha_maciez: float = 3.0     # quanto mais, mais macia a borda do sulco
    arredonda: float = 3.5         # arredondado das quinas da alça
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


def saliencia(p: ParamsCaneca, R: float | None = None) -> float:
    """Quanto a alça sai além do corpo (vem da largura total da foto)."""
    return p.largura_total - 2 * (raio_corpo(p) if R is None else R)


def furo_d(p: ParamsCaneca, R: float) -> tuple[float, float, float, float]:
    """Furo em "D": (x do lado reto = face de dentro da barra, z do centro,
    largura no meio, meia altura). O lado curvo é meia elipse, entrando no corpo."""
    x_bin = R + saliencia(p, R) - p.alca_barra
    return x_bin, p.furo_centro * p.altura, p.furo_largura_mm, p.furo_altura / 2


def furo_largura(p: ParamsCaneca, R: float | None = None) -> float:
    """Largura visível do furo: do fundo da concha até a barra de fora."""
    return saliencia(p, R) - p.alca_barra + p.concha_fundura


def furo_d_antigo(p: ParamsCaneca, R: float) -> tuple[float, float, float, float]:
    """Furo em "D": (x do lado reto, z do centro, meia largura a, meia altura b).
    O lado curvo é meia elipse; a ponta encosta no fundo da concha."""
    a = furo_largura(p, R)
    x_out = R - p.concha_fundura + a
    return x_out, p.furo_centro * p.altura, a, p.furo_altura / 2


# ---- concha: o corpo afunda em volta do furo (curva e macia, como na foto) ----
def x_concha(p: ParamsCaneca, R: float, z: np.ndarray, recuo: float = 0.0) -> np.ndarray:
    """Lado curvo do furo em "D" (até onde a parede vai, na direção da alça).
    Fora da altura do furo devolve um valor alto (não mexe na parede)."""
    x_bin, zc, a, b = furo_d(p, R)
    u = np.clip(1 - ((z - zc) / b) ** 2, 0, 1)
    return x_bin - a * np.sqrt(u) + 40 * (u <= 0) - recuo


def amassa(p: ParamsCaneca, m: Manifold, R: float, recuo: float = 0.0, k: float | None = None) -> Manifold:
    """Empurra a parede do lado da alça para dentro até a concha, com transição suave
    (mínimo suave). Para cada altura, a parede só RECUA conforme se afasta do meio
    (y = 0), então o molde dividido nesse plano solta sem prender."""
    k = p.concha_maciez if k is None else k
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


def escareia(p: ParamsCaneca, m: Manifold, R: float) -> Manifold:
    """Rampa em meia-lua em volta do lado curvo do furo, nas DUAS faces (a que se vê de
    frente nas fotos): a superfície desce suavemente até a boca do furo.
    Cada rampa abre para o lado em que a sua metade do molde sai, então não prende."""
    x_out, zc, a, b = furo_d(p, R)
    d0, faixa = p.rampa_fundura, p.rampa_largura
    meia = p.alca_espessura / 2
    m = m.refine_to_length(0.9)

    def f(v: np.ndarray) -> np.ndarray:
        x, y, z = v[:, 0], v[:, 1], v[:, 2]
        rho = np.sqrt(((np.minimum(x, x_out) - x_out) / a) ** 2 + ((z - zc) / b) ** 2)
        dist = np.maximum(rho - 1, 0) * min(a, b)                 # distância aproximada da borda curva
        prof = d0 * np.clip(1 - dist / faixa, 0, 1) ** 1.6
        t = np.clip((x_out - 1.0 - x) / 7.0, 0, 1)
        prof = prof * t * t * (3 - 2 * t)                          # some suave na barra de fora (fica lisa)
        fi = np.minimum(np.abs(y) / meia, 1.0)                     # 0 no meio da alça, 1 nas faces
        return np.c_[x, y - np.sign(y) * prof * fi, z]

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
        box(-1, t, 8, p.altura + 5))                           # vai até o eixo (sem "pino" no meio)
    dentro = dentro.intersection(box(0, 0, 1e3, p.altura))
    dentro = max(getattr(dentro, "geoms", [dentro]), key=lambda g: g.area)
    xy = np.asarray(dentro.exterior.coords)[:-1]
    xy[:, 0] = np.maximum(xy[:, 0], 0)
    if not dentro.exterior.is_ccw:
        xy = xy[::-1]
    return amassa(p, Manifold.revolve(CrossSection([xy]), seg), R, recuo=t, k=p.maciez_interna)


def capacidade_ml(p: ParamsCaneca, R: float, seg: int = 96) -> float:
    return interno(p, R, seg).volume() / 1000.0


def raio_corpo(p: ParamsCaneca) -> float:
    chave = tuple(sorted(vars(p).items()))
    if chave in _cache_raio:
        return _cache_raio[chave]
    lo, hi = 18.0, 70.0
    for _ in range(18):
        mid = (lo + hi) / 2
        if capacidade_ml(p, mid, 64) < p.capacidade:
            lo = mid
        else:
            hi = mid
    _cache_raio[chave] = (lo + hi) / 2
    return _cache_raio[chave]


def forma_alca_2d(p: ParamsCaneca, R: float):
    """Alça vista de lado (plano xz) e o furo. O furo fica entre a barra de fora e a
    própria barriga invertida do corpo: o lado de dentro do furo É a parede da caneca."""
    H = p.altura
    z0 = p.alca_base * H
    xo = R + saliencia(p, R)
    x_bin = xo - p.alca_barra
    z1 = H + p.arredonda + 2                                   # passa da borda; é aparado depois
    bloco = box(R - 30, z0, xo, z1)
    r = 18.0
    bloco = bloco.buffer(-r, join_style=1).buffer(r, join_style=1).union(box(R - 30, z0 + r, R - 12, z1 - r))
    zc, hb = p.furo_centro * H, p.furo_altura / 2
    zz = np.linspace(zc - hb, zc + hb, 160)
    xin = x_concha(p, R, zz) - 6.0                              # entra no corpo (só corta a alça)
    furo = Polygon(np.r_[np.c_[np.full_like(zz, x_bin), zz][::-1], np.c_[xin, zz]])
    c = p.furo_canto
    furo = furo.buffer(-c, join_style=1).buffer(c, join_style=1)
    from shapely.geometry.polygon import orient
    return orient(bloco, 1.0), orient(furo, 1.0)


def funil_furo(p: ParamsCaneca, R: float, furo: Polygon) -> Manifold:
    """Túnel em "D" atravessando de lado a lado. Na grossura da alça ele é exato; daí para
    fora vai ABRINDO suave (como um escareado), até sair na lateral do corpo. O encontro
    do túnel com a lateral redonda forma a meia-lua das fotos, com a borda arredondada."""
    import trimesh
    from manifold3d import Mesh
    x_bin, zc, a, b = furo_d(p, R)
    W = p.alca_espessura / 2
    cx, cz = x_bin - a * 0.45, zc
    N = 256
    th = np.linspace(-np.pi, np.pi, N, endpoint=False)

    def polar(poly):
        from shapely.affinity import translate
        return raio_polar(translate(poly, -cx, -cz).segmentize(0.4), th)   # lado reto continua reto

    y_fim = R + 3
    ys = np.r_[np.linspace(0, W - 1.5, 3), W - 1.5 + (y_fim - W + 1.5) * np.linspace(0, 1, 14)[1:]]
    camadas = {}
    for y in ys:
        t = np.clip((y - (W - 1.5)) / (y_fim - (W - 1.5)), 0, 1)
        e = p.meia_lua_abre * (t ** 1.6)
        r = polar(furo.buffer(e, join_style=1, resolution=32)) if e > 1e-3 else polar(furo)
        camadas[y] = np.c_[cx + r * np.cos(th), np.full(N, y), cz + r * np.sin(th)]
    ordem = [-y for y in ys[::-1] if y > 0] + list(ys)
    secs = [camadas[abs(y)] * [1, np.sign(y) if y != 0 else 1, 1] for y in ordem]
    m_ = len(secs)
    v = np.vstack(secs + [[secs[0].mean(axis=0)], [secs[-1].mean(axis=0)]])
    f = []
    for k in range(m_ - 1):
        for i in range(N):
            a0, b0 = k * N + i, k * N + (i + 1) % N
            c0, d0 = (k + 1) * N + (i + 1) % N, (k + 1) * N + i
            f += [[a0, b0, c0], [a0, c0, d0]]
    cb, ct = m_ * N, m_ * N + 1
    for i in range(N):
        f += [[cb, (i + 1) % N, i], [ct, (m_ - 1) * N + i, (m_ - 1) * N + (i + 1) % N]]
    tm = trimesh.Trimesh(v, np.array(f), process=True)
    trimesh.repair.fix_normals(tm)
    assert tm.is_volume
    return Manifold(Mesh(np.asarray(tm.vertices, np.float32), np.asarray(tm.faces, np.uint32)))


def prisma_furo(p: ParamsCaneca, R: float, furo: Polygon | None = None, comprimento: float | None = None) -> Manifold:
    if furo is None:
        furo = forma_alca_2d(p, R)[1]
    fxy = np.asarray(furo.simplify(0.05).exterior.coords)[:-1]
    if Polygon(fxy).exterior.is_ccw is False:
        fxy = fxy[::-1]
    L = comprimento if comprimento is not None else p.alca_espessura_base
    return CrossSection([fxy], FillRule.EvenOdd).extrude(2 * L).translate((0, 0, -L)).rotate((90, 0, 0))


def planta(p: ParamsCaneca, R: float) -> Polygon:
    """Vista de cima: o círculo do corpo e a alça saindo dele, unidos por uma curva
    (concordância). A alça é o próprio corpo esticado, não um bloco grudado."""
    W = p.alca_espessura / 2
    xo = R + saliencia(p, R)
    lobo = box(R - 15, -W, xo - W, W).union(Point(xo - W, 0).buffer(W, resolution=48))
    base = Point(0, 0).buffer(R, resolution=180).union(lobo)
    f = p.alca_concordancia
    return base.buffer(f, join_style=1, resolution=32).buffer(-f, join_style=1, resolution=32)


def casca_externa(p: ParamsCaneca, R: float) -> Manifold:
    """Sólido de fora: em cada altura, a planta encolhida junto com o fundo em "U".
    Assim a alça acompanha o fundo arredondado e a borda reta, como uma peça só."""
    pts = contorno_corpo(p, R)
    zs_c = np.array([q[1] for q in pts[1:]])
    rs_c = np.array([q[0] for q in pts[1:]])
    base = planta(p, R)
    th = np.linspace(-np.pi, np.pi, 360, endpoint=False)
    zs = np.r_[np.linspace(0, p.raio_fundo + 2, 30), np.linspace(p.raio_fundo + 3, p.altura, 30)]
    raios = []
    for z in zs:
        enc = R - float(np.interp(z, zs_c, rs_c))
        g = base.buffer(-enc, join_style=1, resolution=24) if enc > 1e-3 else base
        raios.append(raio_polar(g, th))
    return loft(list(zs), raios, th)


def peca(p: ParamsCaneca, com_reservatorio: bool = False, oca: bool = False) -> Manifold:
    R = raio_corpo(p)
    H = p.altura
    m = casca_externa(p, R)
    if com_reservatorio:
        pts = contorno_corpo(p, R)
        S = p.altura_reservatorio / escala(p)
        rb = pts[-1][0]
        rs = rb + p.degrau_corte / escala(p)
        res = [(0.0, H - 1), (rb, H - 1), (rb, H), (rs, H), (rs + S * math.tan(math.radians(p.saida_reservatorio)), H + S),
               (0.0, H + S)]
        m = m + revolve_contorno(p, res, p.segmentos)
    # furo em "D" atravessando de lado a lado: abre o furo na alça e, nas laterais do corpo,
    # forma a meia-lua rebaixada em volta do lado curvo (como nas fotos)
    x_bin, zc, a, b = furo_d(p, R)
    zz = np.linspace(zc - b, zc + b, 200)
    xd = x_bin - a * np.sqrt(np.clip(1 - ((zz - zc) / b) ** 2, 0, 1))       # lado curvo do "D"
    furo = Polygon(np.r_[np.c_[xd, zz], [[x_bin, zc + b], [x_bin, zc - b]]]).buffer(0)
    c = 4.0
    furo = furo.buffer(-c, join_style=1).buffer(c, join_style=1)
    m = m - funil_furo(p, R, furo)
    assert m.volume() > 0
    if oca:
        m = m - interno(p, R, p.segmentos)
    return escareia(p, m, R) if p.rampa_fundura > 0 else m


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
