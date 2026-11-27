#!/usr/bin/env python3
"""
Molde de gesso de 2 PARTES para o COPINHO BARRIGUDO — Barro na Veia
==================================================================

Peça medida nas fotos com régua (+ vídeo girando a peça):
    altura 7,0 cm · boca Ø 6,3 cm · barriga Ø ~7,2 cm (a ~2,6 cm do apoio)
    pescoço levemente fechado, boca abrindo de leve, fundo bem redondo
    uma COVINHA (marca de dedo) de um lado, na altura da barriga

A barriga é mais larga que a boca, então a peça não sai de um molde inteiriço:
o molde é dividido em DUAS METADES na vertical, pelo eixo do copinho. A covinha
fica no meio da metade A (sai reto, sem prender).

  stl/copinho/
  * bandeja_A.stl         -> meio copinho deitado COM a covinha + 4 bolinhas (chaves).
  * bandeja_B.stl         -> meio copinho deitado sem covinha + 4 covinhas (chaves).
  * moldura_U.stl         -> metade da moldura (lisa).
  * moldura_U_logo.stl    -> a outra metade, com o logo da escola em relevo por dentro
                             (fica gravado na lateral de cada metade de gesso).
  * presilha.stl          -> trava as metades da moldura (imprimir 4x).
  * pino_A.stl / pino_B.stl -> tampam o canal de ar de cada bandeja.

    python3 gerar_copinho.py --preview
    python3 gerar_copinho.py --retracao 12   # molde maior: a peça QUEIMADA fica com as medidas
"""

from __future__ import annotations

import argparse
import math
import os
from dataclasses import dataclass, fields

import numpy as np
from manifold3d import CrossSection, Manifold

from gerar_moldes import Params as ParamsPrato, para_trimesh, presilha, receita
from marca import relevo_local

# Perfil medido (altura cm, raio externo cm), do apoio até a boca
PERFIL_CM = [
    (0.00, 0.90), (0.10, 1.35), (0.40, 2.00), (0.75, 2.40), (1.35, 2.95), (1.95, 3.38),
    (2.60, 3.58), (3.20, 3.55), (3.85, 3.42), (4.45, 3.25), (5.05, 3.08), (5.60, 3.00),
    (6.20, 3.03), (6.70, 3.10), (7.00, 3.15),
]


@dataclass
class ParamsCopinho:
    aumento: float = 20.0          # % que o molde é maior que a peça medida (compensa a retração da barbotina)
    retracao: float = 0.0          # alternativa: % de retração (usado só se aumento = 0)
    # covinha (marca de dedo) — desligada: a covinha é feita à mão depois de desenformar
    covinha: bool = False
    covinha_altura: float = 23.0   # mm do apoio até o centro da covinha
    covinha_largura: float = 30.0  # mm (diâmetro aproximado da marca)
    covinha_alta: float = 32.0     # mm (altura da marca)
    covinha_fundura: float = 6.5   # mm
    # reservatório
    altura_reservatorio: float = 20.0
    degrau_corte: float = 2.0
    saida_reservatorio: float = 5.0
    # bloco de gesso e caixa
    margem_gesso: float = 25.0
    parede: float = 4.0
    aba_presilha: float = 10.0
    folga: float = 0.25
    espessura_base: float = 3.0
    altura_plug: float = 4.0
    raio_chave: float = 4.0
    folga_chave: float = 0.4
    # canal + pino de desmoldagem
    canal_desmolde: bool = True
    diametro_canal: float = 4.2
    diametro_pino: float = 3.9
    diametro_bolso: float = 30.0
    profundidade_bolso: float = 12.0
    diametro_cabeca_pino: float = 16.0
    espessura_cabeca_pino: float = 3.0
    saliencia_pino: float = 0.2
    # marca
    logo: bool = True
    logo_largura: float = 42.0
    logo_profundidade: float = 1.0
    logo_arquivo: str = ""
    segmentos: int = 256


def escala(p: ParamsCopinho) -> float:
    if p.aumento:
        return 1.0 + p.aumento / 100.0
    return 1.0 / (1.0 - p.retracao / 100.0)


def perfil(p: ParamsCopinho) -> np.ndarray:
    """Contorno (r, h) em mm: copinho suavizado por spline + degrau + reservatório."""
    from scipy.interpolate import splev, splprep
    k = escala(p)
    pts = np.array([(r * 10 * k, h * 10 * k) for h, r in PERFIL_CM])
    tck, _ = splprep([pts[:, 0], pts[:, 1]], s=len(pts) * 0.15, k=3)
    r, h = splev(np.linspace(0, 1, 220), tck)
    r[0], h[0] = pts[0]
    h = np.maximum.accumulate(np.maximum(h, 0))          # sempre subindo
    H, Rb = h[-1], r[-1]
    S = p.altura_reservatorio
    rs = Rb + p.degrau_corte
    cont = [(0.0, 0.0)] + list(zip(r, h)) + [(rs, H), (rs + S * math.tan(math.radians(p.saida_reservatorio)), H + S),
                                             (0.0, H + S)]
    return np.array(cont)


def dimensoes(p: ParamsCopinho) -> dict:
    pf = perfil(p)
    rmax = float(pf[:, 0].max())
    meia = math.ceil(rmax + p.margem_gesso)
    return {"meia": meia, "v0": -p.margem_gesso, "v1": float(pf[:, 1].max()), "esp": meia, "rmax": rmax}


def raio_em(p: ParamsCopinho, h: float) -> float:
    pf = perfil(p)
    corpo = pf[1:-3]
    return float(np.interp(h, corpo[:, 1], corpo[:, 0]))


def copinho(p: ParamsCopinho, com_covinha: bool, so_peca: bool = False) -> Manifold:
    """Sólido da peça (+ reservatório) em coordenadas da BANDEJA:
    u = x, v = y = eixo do copinho, w = z = para cima (partição em w = 0)."""
    pf = perfil(p)
    if so_peca:                                                          # sem reservatório, oca (para conferir)
        corpo = pf[:-3]
        H = corpo[-1, 1]
        pf = np.r_[corpo, [[0.0, H]]]
    sol = Manifold.revolve(CrossSection([pf]), p.segmentos)             # eixo z
    if so_peca:
        from shapely.geometry import Polygon as SPoly, box as sbox
        reg = SPoly(np.r_[pf, [[0, 0]]]).buffer(0)
        H = float(pf[:, 1].max())
        r_in = float(pf[-2, 0]) - 3.5
        dentro = reg.buffer(-3.5, join_style=1).union(sbox(0, H - 12, r_in, H + 5)).intersection(sbox(0, -1, 1e3, 1e3))
        dentro = max(getattr(dentro, "geoms", [dentro]), key=lambda g: g.area)
        xy = np.asarray(dentro.exterior.coords)[:-1]
        if not dentro.exterior.is_ccw:
            xy = xy[::-1]
        sol = sol - Manifold.revolve(CrossSection([xy]), p.segmentos)
    if com_covinha and p.covinha:
        k = escala(p)
        h0, d = p.covinha_altura * k, p.covinha_fundura * k
        su, sv = p.covinha_largura * k / 2.0, p.covinha_alta * k / 2.0   # meia largura / meia altura
        sol = sol.refine_to_length(1.2)

        def afunda(v: np.ndarray) -> np.ndarray:
            x, y, z = v[:, 0], v[:, 1], v[:, 2]
            r = np.hypot(x, y)
            ang = np.arctan2(y, x)
            arco = np.angle(np.exp(1j * (ang + math.pi / 2))) * np.maximum(r, 1e-6)   # covinha em -y
            q = (arco / su) ** 2 + ((z - h0) / sv) ** 2
            g = np.exp(-1.8 * q ** 1.15)                   # fundo arredondado, borda suave (marca de dedo)
            g = np.where(r > 5, g, 0.0)
            nr = np.maximum(r - d * g, 0)
            f = np.where(r > 1e-6, nr / np.maximum(r, 1e-6), 1.0)
            return np.c_[x * f, y * f, z]

        sol = sol.warp_batch(afunda)
    if so_peca:
        return sol
    return sol.rotate((-90, 0, 0))          # eixo -> v; o lado -y (covinha) vira +w (topo da metade)


def meio(p: ParamsCopinho, com_covinha: bool) -> Manifold:
    d = dimensoes(p)
    m = copinho(p, com_covinha).trim_by_plane((0, 0, 1), -0.5)
    return m.trim_by_plane((0, -1, 0), -(d["v1"] - p.folga))


def chaves(p: ParamsCopinho) -> list[tuple[float, float]]:
    d = dimensoes(p)
    uc = d["meia"] - p.margem_gesso / 2
    return [(s * uc, v) for s in (-1, 1) for v in (d["v1"] * 0.25, d["v1"] * 0.8)]


def altura_canal(p: ParamsCopinho, lado: str) -> tuple[float, float]:
    """(v, w) do ponto onde o canal de ar sai na superfície da peça
    (no centro da covinha, se houver; senão na parte mais larga da barriga)."""
    k = escala(p)
    if p.covinha:
        h0 = p.covinha_altura * k
        w = raio_em(p, h0) - (p.covinha_fundura * k if lado == "A" else 0.0)
        return h0, w
    pf = perfil(p)[1:-3]
    i = int(np.argmax(pf[:, 0]))
    return float(pf[i, 1]), float(pf[i, 0])


def bandeja(p: ParamsCopinho, lado: str) -> Manifold:
    d = dimensoes(p)
    M, v0, v1 = d["meia"], d["v0"], d["v1"]
    aba = CrossSection.square((2 * (M + p.parede + 3), v1 - v0 + 2 * (p.parede + 3))).translate(
        (-(M + p.parede + 3), v0 - p.parede - 3))
    plug = CrossSection.square((2 * (M - p.folga), v1 - v0 - 2 * p.folga)).translate((-(M - p.folga), v0 + p.folga))
    b = (aba.extrude(p.espessura_base).translate((0, 0, -p.altura_plug - p.espessura_base))
         + plug.extrude(p.altura_plug + 0.01).translate((0, 0, -p.altura_plug)))
    b = b + meio(p, com_covinha=(lado == "A"))
    for u, v in chaves(p):
        if lado == "A":
            b = b + Manifold.sphere(p.raio_chave, 48).translate((u, v, 0)).trim_by_plane((0, 0, 1), 0)
        else:
            b = b - Manifold.sphere(p.raio_chave - p.folga_chave, 48).translate((u, v, 0))
    if p.canal_desmolde:
        vc, wc = altura_canal(p, lado)
        base = -p.altura_plug - p.espessura_base
        rc = p.diametro_canal / 2
        b = b - Manifold.cylinder(wc - base + 2, rc, rc, 48).translate((0, vc, base - 1))
        b = b - Manifold.cylinder(p.profundidade_bolso + 1, p.diametro_bolso / 2, p.diametro_bolso / 2, 96).translate((0, vc, base - 1))
    return b


def pino(p: ParamsCopinho, lado: str) -> Manifold:
    _, wc = altura_canal(p, lado)
    L = p.espessura_base + p.altura_plug + wc - p.profundidade_bolso + p.saliencia_pino
    cab = Manifold.cylinder(p.espessura_cabeca_pino, p.diametro_cabeca_pino / 2, p.diametro_cabeca_pino / 2, 96)
    r = p.diametro_pino / 2
    haste = Manifold.cylinder(L - 0.6, r, r, 48) + Manifold.cylinder(0.6, r, r - 0.4, 48).translate((0, 0, L - 0.6))
    return cab + haste.translate((0, 0, p.espessura_cabeca_pino))


def moldura_u(p: ParamsCopinho, logo: bool = False) -> tuple[Manifold, str]:
    """Metade da moldura (parte de cima da caixa, v > meio). Com logo: relevo na
    parede lateral u = +M, que vira a lateral de cada metade de gesso."""
    d = dimensoes(p)
    M, v0, v1, t = d["meia"], d["v0"], d["v1"], p.parede
    vm = (v0 + v1) / 2
    H = p.altura_plug + d["esp"]
    ext = CrossSection.square((2 * (M + t), v1 - v0 + 2 * t)).translate((-(M + t), v0 - t))
    inte = CrossSection.square((2 * M, v1 - v0)).translate((-M, v0))
    corte = CrossSection.square((2 * (M + t) + 2, v1 - vm + t + 1)).translate((-(M + t) - 1, vm))
    u = (ext - inte) ^ corte
    for s in (-1, 1):
        x0 = M if s > 0 else -(M + t + p.aba_presilha)
        u = u + CrossSection.square((t + p.aba_presilha, t)).translate((x0, vm))
    m = u.extrude(H)
    origem = ""
    if logo:
        rel, alt, origem = relevo_local(p.logo_largura, p.logo_profundidade, virado=False,
                                        arquivo=p.logo_arquivo or None)
        assert alt + 10 < v1 - vm, "logo alto demais: diminua --logo-largura"
        vc = vm + 5 + alt / 2                              # metade de cima da parede lateral
        wc = p.altura_plug + d["esp"] / 2                   # meio da espessura do gesso
        dd = p.logo_profundidade
        # local: x = direita (vista de fora = -w), y = cima (+v), z = para dentro da parede (+u)
        T = np.array([[0, 0, 1, M - dd], [0, 1, 0, vc], [-1, 0, 0, wc]], dtype=np.float64)
        m = m + rel.transform(T)
    return m.translate((0, -vm, 0)), origem


# --------------------------------------------------------------------------
def main() -> None:
    p = ParamsCopinho()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    for f in fields(p):
        v = getattr(p, f.name)
        opt = "--" + f.name.replace("_", "-")
        if isinstance(v, bool):
            ap.add_argument(opt, type=lambda s: s.lower() in ("1", "sim", "true", "s"), default=v)
        else:
            ap.add_argument(opt, type=type(v), default=v)
    raiz = os.path.dirname(os.path.abspath(__file__))
    ap.add_argument("--saida", default=os.path.join(raiz, "stl", "copinho"))
    ap.add_argument("--peca", action="store_true", help="exporta também a peça (copinho) para conferir")
    a = ap.parse_args()
    p = ParamsCopinho(**{f.name: getattr(a, f.name) for f in fields(p)})
    d = dimensoes(p)
    os.makedirs(a.saida, exist_ok=True)

    pecas = {"bandeja_A": bandeja(p, "A"), "bandeja_B": bandeja(p, "B")}
    pecas["moldura_U"], _ = moldura_u(p, logo=False)
    if p.logo:
        pecas["moldura_U_logo"], origem = moldura_u(p, logo=True)
        print(f"  logo: {origem}")
    pecas["presilha"] = presilha(ParamsPrato(parede=p.parede, aba_presilha=p.aba_presilha))
    if p.canal_desmolde:
        if p.covinha:
            pecas["pino_A"], pecas["pino_B"] = pino(p, "A"), pino(p, "B")
        else:
            pecas["pino"] = pino(p, "A")                  # igual para as duas bandejas (imprimir 2x)
    if a.peca:
        pecas["_peca_copinho"] = copinho(p, True, so_peca=True)
    print("[copinho]")
    for nome, m in pecas.items():
        tm = para_trimesh(m)
        assert tm.is_watertight, f"{nome} não está fechado"
        tm.export(os.path.join(a.saida, f"{nome}.stl"))
        dx, dy, dz = tm.extents
        print(f"  {nome:15s} {dx:6.1f} x {dy:6.1f} x {dz:5.1f} mm")
    k = escala(p)
    print(f"  Peça no molde (crua): altura {70*k:.0f} mm, boca Ø {63*k:.0f}, barriga Ø {2*d['rmax']:.0f}"
          f"  (molde {k*100-100:+.0f}% em relação à peça medida)")
    bloco = Manifold.cube((2 * d["meia"], d["v1"] - d["v0"], d["esp"])).translate((-d["meia"], d["v0"], 0))
    v = (bloco - copinho(p, True)).volume() / 1000.0
    g, w = receita(v)
    print(f"  Bloco montado: {2*d['esp']} x {2*d['meia']} x {d['v1']-d['v0']:.0f} mm")
    print(f"  Gesso POR METADE: ~{v/1000:.2f} L -> {g/1000:.2f} kg de gesso + {w/1000:.2f} L de água")


if __name__ == "__main__":
    main()
