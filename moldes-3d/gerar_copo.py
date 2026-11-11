#!/usr/bin/env python3
"""
Molde de gesso de 2 partes para COPO de barbotina — Barro na Veia
=================================================================

Copo arredondado embaixo, com um pezinho em disco no meio do fundo.
Medidas padrão da peça (crua, como sai do molde):

    altura 14 cm (com o pé)  ·  boca Ø 13 cm  ·  largura máxima Ø 14 cm
    pé: disco Ø 7 cm com 0,5 cm de altura

Como a barriga (14 cm) é mais larga que a boca (13 cm), a peça não sai de um
molde inteiriço: o molde é dividido em DUAS METADES na vertical, passando
pelo eixo do copo. Cada metade de gesso é feita numa bandeja impressa:

  stl/copo/
  * bandeja_A.stl  -> meio copo deitado + chaves (bolinhas). Gera a metade A.
  * bandeja_B.stl  -> igual, com covinhas no lugar das bolinhas. Gera a metade B.
  * moldura_U.stl  -> metade da moldura que cerca a bandeja (imprimir 2x).
  * presilha.stl   -> trava as duas metades da moldura (imprimir 4x).
  * pino_desmolde.stl -> tampa o canal de ar durante o despejo (imprimir 2x).

Uso:
    python3 gerar_copo.py --preview
    python3 gerar_copo.py --altura 120 --boca 110 --largura 125
    python3 gerar_copo.py --retracao 12   # aumenta o molde para o copo QUEIMADO ter as medidas
"""

from __future__ import annotations

import argparse
import math
import os
from dataclasses import dataclass, fields

import numpy as np
from manifold3d import CrossSection, Manifold

from gerar_moldes import Params as ParamsPrato, para_trimesh, presilha, receita


@dataclass
class ParamsCopo:
    # Peça (mm). Por padrão, medidas da peça CRUA (como sai do molde).
    altura: float = 140.0          # do apoio do pé até a boca
    boca: float = 130.0            # diâmetro externo da boca
    largura: float = 140.0         # diâmetro externo máximo (barriga)
    altura_barriga: float = 60.0   # altura (a partir do apoio) onde fica a largura máxima
    diametro_pe: float = 70.0
    altura_pe: float = 5.0
    aba_fundo: float = 3.0         # faixa plana do fundo em volta do pé, antes da curva
    retracao: float = 0.0          # % — 0 = medidas da peça crua; ex. 12 = medidas da peça queimada

    # Reservatório (acima da boca)
    altura_reservatorio: float = 25.0
    degrau_corte: float = 2.0
    saida_reservatorio: float = 5.0

    # Bloco de gesso
    margem_gesso: float = 25.0     # gesso mínimo em volta da barriga e embaixo do pé

    # Caixa impressa
    parede: float = 4.0
    aba_presilha: float = 10.0
    folga: float = 0.25
    espessura_base: float = 3.0
    altura_plug: float = 4.0

    # Chaves de registro entre as metades
    raio_chave: float = 5.0
    folga_chave: float = 0.4

    # Canal + pino de desmoldagem
    canal_desmolde: bool = True
    diametro_canal: float = 4.2
    diametro_pino: float = 3.9
    diametro_bolso: float = 34.0
    profundidade_bolso: float = 12.0
    diametro_cabeca_pino: float = 18.0
    espessura_cabeca_pino: float = 3.0
    saliencia_pino: float = 0.2

    segmentos: int = 256


# --------------------------------------------------------------------------
# Perfil do copo (r, z): z = 0 no apoio do pé, eixo em r = 0
# --------------------------------------------------------------------------
def escala(p: ParamsCopo) -> float:
    return 1.0 / (1.0 - p.retracao / 100.0)


def perfil(p: ParamsCopo, n: int = 120) -> np.ndarray:
    """Contorno externo do copo + reservatório, como lista de pontos (r, z)."""
    k = escala(p)
    H, Rb, Rm = p.altura * k, p.boca / 2 * k, p.largura / 2 * k
    zm, Rp, hp = p.altura_barriga * k, p.diametro_pe / 2 * k, p.altura_pe * k
    r0 = Rp + p.aba_fundo * k                  # onde começa a curva do fundo
    pts = [(0.0, 0.0), (Rp, 0.0), (Rp, hp), (r0, hp)]
    # fundo bem arredondado: quarto de elipse do fundo até a barriga
    for t in np.linspace(0, np.pi / 2, n)[1:]:
        pts.append((r0 + (Rm - r0) * math.sin(t), zm - (zm - hp) * math.cos(t)))
    # da barriga até a boca: fecha suavemente (tangente vertical na barriga)
    for u in np.linspace(0, 1, n)[1:]:
        pts.append((Rm - (Rm - Rb) * u * u, zm + (H - zm) * u))
    # degrau de corte + reservatório
    S = p.altura_reservatorio
    rs = Rb + p.degrau_corte
    pts += [(rs, H), (rs + S * math.tan(math.radians(p.saida_reservatorio)), H + S), (0.0, H + S)]
    return np.array(pts)


def dimensoes(p: ParamsCopo) -> dict:
    pf = perfil(p)
    rmax = pf[:, 0].max()
    meia = math.ceil(rmax + p.margem_gesso)          # meia largura do bloco
    return {
        "meia": meia,                                 # bloco: u ∈ [-meia, meia]
        "v0": -p.margem_gesso,                        # embaixo do pé
        "v1": pf[:, 1].max(),                         # topo do reservatório = topo do bloco
        "esp": meia,                                  # espessura de cada metade
        "rmax": rmax,
        "z_barriga": p.altura_barriga * escala(p),
    }


# --------------------------------------------------------------------------
# Sólidos (coordenadas da BANDEJA: u = x, v = y = eixo do copo, w = z = para cima)
# A face de partição fica em w = 0.
# --------------------------------------------------------------------------
def copo_solido(p: ParamsCopo) -> Manifold:
    """Copo + reservatório como sólido de revolução, eixo ao longo de v."""
    cs = CrossSection([perfil(p)])
    sol = Manifold.revolve(cs, p.segmentos)          # eixo em z
    return sol.rotate((-90, 0, 0))                   # eixo z -> eixo y (v)


def meio_copo(p: ParamsCopo) -> Manifold:
    d = dimensoes(p)
    m = copo_solido(p).trim_by_plane((0, 0, 1), -0.5)
    # termina rente à parede da moldura no topo do reservatório
    return m.trim_by_plane((0, -1, 0), -(d["v1"] - p.folga))


def posicoes_chaves(p: ParamsCopo) -> list[tuple[float, float]]:
    d = dimensoes(p)
    uc = d["meia"] - p.margem_gesso / 2 - 0.5
    h = d["v1"]
    return [(s * uc, v) for s in (-1, 1) for v in (h * 0.3, h * 0.88)]


def bandeja(p: ParamsCopo, lado: str) -> Manifold:
    d = dimensoes(p)
    M, v0, v1 = d["meia"], d["v0"], d["v1"]
    aba = CrossSection.square((2 * (M + p.parede + 3), v1 - v0 + 2 * (p.parede + 3))).translate(
        (-(M + p.parede + 3), v0 - p.parede - 3))
    plug = CrossSection.square((2 * (M - p.folga), v1 - v0 - 2 * p.folga)).translate((-(M - p.folga), v0 + p.folga))
    b = (aba.extrude(p.espessura_base).translate((0, 0, -p.altura_plug - p.espessura_base))
         + plug.extrude(p.altura_plug + 0.01).translate((0, 0, -p.altura_plug)))
    b = b + meio_copo(p)
    for u, v in posicoes_chaves(p):
        if lado == "A":
            b = b + Manifold.sphere(p.raio_chave, 64).translate((u, v, 0)).trim_by_plane((0, 0, 1), 0)
        else:
            b = b - Manifold.sphere(p.raio_chave - p.folga_chave, 64).translate((u, v, 0))
    if p.canal_desmolde:
        # canal no ponto mais alto do meio copo (a barriga), saindo num bolso por baixo
        zb = d["z_barriga"]
        base = -p.altura_plug - p.espessura_base
        b = b - Manifold.cylinder(d["rmax"] - base + 2, p.diametro_canal / 2, p.diametro_canal / 2, 48).translate((0, zb, base - 1))
        b = b - Manifold.cylinder(p.profundidade_bolso + 1, p.diametro_bolso / 2, p.diametro_bolso / 2, 128).translate((0, zb, base - 1))
    return b


def comprimento_pino(p: ParamsCopo) -> float:
    d = dimensoes(p)
    return p.espessura_base + p.altura_plug + d["rmax"] - p.profundidade_bolso + p.saliencia_pino


def pino(p: ParamsCopo) -> Manifold:
    cab = Manifold.cylinder(p.espessura_cabeca_pino, p.diametro_cabeca_pino / 2, p.diametro_cabeca_pino / 2, 96)
    L, r = comprimento_pino(p), p.diametro_pino / 2
    haste = Manifold.cylinder(L - 0.6, r, r, 48) + Manifold.cylinder(0.6, r, r - 0.4, 48).translate((0, 0, L - 0.6))
    return cab + haste.translate((0, 0, p.espessura_cabeca_pino))


def moldura_u(p: ParamsCopo) -> Manifold:
    """Metade da moldura retangular (as duas metades são iguais, giradas 180°)."""
    d = dimensoes(p)
    M, v0, v1, t = d["meia"], d["v0"], d["v1"], p.parede
    vm = (v0 + v1) / 2
    ext = CrossSection.square((2 * (M + t), v1 - v0 + 2 * t)).translate((-(M + t), v0 - t))
    inte = CrossSection.square((2 * M, v1 - v0)).translate((-M, v0))
    corte = CrossSection.square((2 * (M + t) + 2, v1 - vm + t + 1)).translate((-(M + t) - 1, vm))
    u = (ext - inte) ^ corte
    for s in (-1, 1):
        x0 = M if s > 0 else -(M + t + p.aba_presilha)
        u = u + CrossSection.square((t + p.aba_presilha, t)).translate((x0, vm))
    return u.extrude(p.altura_plug + d["esp"]).translate((0, -vm, 0))


# --------------------------------------------------------------------------
# Desenho em corte
# --------------------------------------------------------------------------
def corte(p: ParamsCopo, caminho: str, parede_peca: float = 4.0) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from shapely.geometry import Polygon, box

    d = dimensoes(p)
    M, v0, v1 = d["meia"], d["v0"], d["v1"]
    pf = perfil(p)
    cav = Polygon(np.r_[pf, pf[::-1] * [-1, 1]]).buffer(0)
    k = escala(p)
    H = p.altura * k

    fig, ax = plt.subplots(figsize=(8, 8.4), dpi=130)

    def pinta(g, **kw):
        for poly in getattr(g, "geoms", [g]):
            if poly.geom_type == "Polygon" and not poly.is_empty:
                x, y = poly.exterior.xy
                ax.fill(x, y, **kw)
                kw.pop("label", None)

    pinta(box(-M, v0, 0, v1).difference(cav), color="#e8e2d6", ec="#9c9284", lw=1, label="gesso – metade A")
    pinta(box(0, v0, M, v1).difference(cav), color="#dfe6ea", ec="#8a969c", lw=1, label="gesso – metade B")
    casca = cav.intersection(box(-M, v0, M, v1).difference(cav).buffer(parede_peca, resolution=16))
    pinta(casca.intersection(box(-M, v0, M, H)), color="#b5653f", label=f"parede colada (~{parede_peca:g} mm) = o copo")
    pinta(casca.intersection(box(-M, H, M, v1)), color="#e0b49c", label="sobra do reservatório (aparar)")
    ax.plot([0, 0], [v0, v1], color="#555", lw=0.8, ls="--")
    ax.plot([-M, M], [H, H], color="#7a2e12", lw=0.8, ls="--")
    ax.text(M - 2, H + 1.5, "linha de corte", ha="right", fontsize=8, color="#7a2e12")
    ax.text(2, v0 + 4, "divisão das metades", fontsize=8, color="#555")
    ax.annotate(f"pé Ø {p.diametro_pe*k:.0f} × {p.altura_pe*k:.0f} mm", xy=(p.diametro_pe * k / 4, p.altura_pe * k / 2),
                xytext=(M * 0.35, -p.margem_gesso * 0.55), fontsize=8, arrowprops=dict(arrowstyle="->", lw=0.7))
    ax.set_xlim(-M - 5, M + 5); ax.set_ylim(v0 - 5, v1 + 32); ax.set_aspect("equal")
    ax.set_xlabel("mm")
    ax.set_title(f"Molde de copo em 2 partes — copo cru: altura {H:.0f}, boca Ø {p.boca*k:.0f}, "
                 f"largura Ø {p.largura*k:.0f} mm", fontsize=9.5)
    ax.legend(loc="upper left", fontsize=7.5, frameon=False, ncol=2)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    plt.tight_layout()
    plt.savefig(caminho)
    plt.close(fig)


# --------------------------------------------------------------------------
def main() -> None:
    p = ParamsCopo()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    for f in fields(p):
        v = getattr(p, f.name)
        opt = "--" + f.name.replace("_", "-")
        if isinstance(v, bool):
            ap.add_argument(opt, type=lambda s: s.lower() in ("1", "sim", "true", "s"), default=v)
        else:
            ap.add_argument(opt, type=type(v), default=v)
    raiz = os.path.dirname(os.path.abspath(__file__))
    ap.add_argument("--saida", default=os.path.join(raiz, "stl", "copo"))
    ap.add_argument("--preview", action="store_true", help="gera imagens/corte_copo.png")
    a = ap.parse_args()
    p = ParamsCopo(**{f.name: getattr(a, f.name) for f in fields(p)})

    assert p.boca / 2 < p.largura / 2 + 1e-9, "boca maior que a largura: use um molde de 1 peça"
    assert p.diametro_pe / 2 + p.aba_fundo < p.largura / 2, "pé grande demais"
    assert p.altura_pe < p.altura_barriga < p.altura

    d = dimensoes(p)
    os.makedirs(a.saida, exist_ok=True)
    pp = ParamsPrato(parede=p.parede, aba_presilha=p.aba_presilha)
    pecas = {
        "bandeja_A": bandeja(p, "A"),
        "bandeja_B": bandeja(p, "B"),
        "moldura_U": moldura_u(p),
        "presilha": presilha(pp),
    }
    if p.canal_desmolde:
        pecas["pino_desmolde"] = pino(p)
    print("[copo]")
    for nome, m in pecas.items():
        tm = para_trimesh(m)
        assert tm.is_watertight, f"{nome} não está fechado"
        tm.export(os.path.join(a.saida, f"{nome}.stl"))
        dx, dy, dz = tm.extents
        print(f"  {nome:15s} {dx:6.1f} x {dy:6.1f} x {dz:5.1f} mm   {len(tm.faces):7d} triângulos")

    k = escala(p)
    print(f"  Copo cru: altura {p.altura*k:.1f} mm, boca Ø {p.boca*k:.1f}, largura Ø {p.largura*k:.1f}"
          + (f"  (retração {p.retracao:g}% -> queimado: {p.altura:g} / {p.boca:g} / {p.largura:g})" if p.retracao else ""))
    bloco = (Manifold.cube((2 * d["meia"], d["v1"] - d["v0"], d["esp"])).translate((-d["meia"], d["v0"], 0)))
    v = (bloco - copo_solido(p)).volume() / 1000.0
    g, w = receita(v)
    print(f"  Bloco montado: {2*d['esp']:.0f} x {2*d['meia']:.0f} x {d['v1']-d['v0']:.0f} mm")
    print(f"  Gesso POR METADE: ~{v/1000:.2f} L de mistura -> {g/1000:.2f} kg de gesso + {w/1000:.2f} L de água")

    if a.preview:
        pasta = os.path.join(raiz, "imagens")
        os.makedirs(pasta, exist_ok=True)
        corte(p, os.path.join(pasta, "corte_copo.png"))
        print("  imagens/corte_copo.png gerado")


if __name__ == "__main__":
    main()
