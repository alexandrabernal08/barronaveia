#!/usr/bin/env python3
"""
Molde de gesso de 1 PEÇA para COPO de barbotina — Barro na Veia
===============================================================

Copo com fundo bem arredondado, paredes que abrem levemente até a boca (a
parte mais larga) e um PÉ EM ANEL no fundo. Como a boca é a parte mais larga,
o copo sai do gesso por cima: molde de uma peça só, sem emenda.

Medidas padrão da peça (crua, como sai do molde):
    altura 14 cm (com o pé)  ·  boca Ø 14 cm  ·  pé em anel Ø 7 cm × 0,5 cm

  stl/copo/
  * matriz_copo.stl   -> o copo de cabeça para baixo sobre uma aba em degraus
                         (reservatório + degrau de corte + encaixe do anel).
                         Por dentro é oca, com um tubo central para o pino.
  * anel_quarto.stl   -> 1/4 da parede de contenção (imprimir 4x).
  * presilha.stl      -> trava os quartos do anel (imprimir 12x: 3 por emenda).
  * pino_desmolde.stl -> tampa o canal de ar durante o despejo (imprimir 2x).

Uso:
    python3 gerar_copo.py --preview
    python3 gerar_copo.py --altura 120 --boca 120
    python3 gerar_copo.py --retracao 12   # molde maior para o copo QUEIMADO ter as medidas
"""

from __future__ import annotations

import argparse
import math
import os
from dataclasses import dataclass, fields

import numpy as np
from manifold3d import CrossSection, Manifold
from shapely.geometry import Polygon, box

from gerar_moldes import Params as ParamsPrato, anel_segmento, para_trimesh, presilha, receita


@dataclass
class ParamsCopo:
    # Peça (mm) — medidas da peça CRUA (como sai do molde), salvo --retracao
    altura: float = 140.0          # do apoio do pé até a boca
    boca: float = 140.0            # diâmetro externo da boca (a parte mais larga)
    saida_parede: float = 3.0      # graus que a parede abre até a boca (para desmoldar)
    altura_curva: float = 45.0     # altura onde termina a curva do fundo
    diametro_pe: float = 70.0      # diâmetro externo do anel do pé
    largura_anel_pe: float = 6.0
    altura_pe: float = 5.0
    aba_fundo: float = 3.0         # faixa plana do fundo em volta do pé, antes da curva
    retracao: float = 0.0          # % — ex. 12 = as medidas acima valem para a peça queimada

    # Reservatório (acima da boca) e degrau de corte
    altura_reservatorio: float = 25.0
    degrau_corte: float = 2.0
    saida_reservatorio: float = 5.0

    # Bloco de gesso
    margem_gesso: float = 25.0     # gesso em volta da boca/reservatório e acima do pé

    # Caixa impressa
    parede: float = 4.0
    aba_presilha: float = 10.0
    folga: float = 0.25
    espessura_base: float = 3.0
    altura_plug: float = 4.0
    segmentos_anel: int = 4
    espessura_casca: float = 3.5   # parede da matriz oca

    # Canal + pino de desmoldagem (tubo central da matriz)
    canal_desmolde: bool = True
    diametro_canal: float = 6.2    # cabe o bico de uma seringa de 60 ml "bico cateter"
    diametro_pino: float = 6.0
    diametro_cabeca_pino: float = 20.0
    espessura_cabeca_pino: float = 3.0
    saliencia_pino: float = 0.2

    segmentos: int = 256


# --------------------------------------------------------------------------
# Perfil do copo, em pé: (r, h) com h = 0 no apoio do pé
# --------------------------------------------------------------------------
def escala(p: ParamsCopo) -> float:
    return 1.0 / (1.0 - p.retracao / 100.0)


def perfil_copo(p: ParamsCopo, n: int = 120) -> list[tuple[float, float]]:
    """Contorno externo do copo em pé, de r=0 no fundo (dentro do pé) até a boca."""
    k = escala(p)
    H, Rb = p.altura * k, p.boca / 2 * k
    hp, Rpo = p.altura_pe * k, p.diametro_pe / 2 * k
    Rpi = Rpo - p.largura_anel_pe * k
    r0 = Rpo + p.aba_fundo * k
    hc = p.altura_curva * k
    rc = Rb - (H - hc) * math.tan(math.radians(p.saida_parede))   # raio no fim da curva
    pts = [(0.0, hp), (Rpi, hp), (Rpi, 0.0), (Rpo, 0.0), (Rpo, hp), (r0, hp)]
    for t in np.linspace(0, np.pi / 2, n)[1:]:                       # fundo arredondado
        pts.append((r0 + (rc - r0) * math.sin(t), hc - (hc - hp) * math.cos(t)))
    pts.append((Rb, H))                                               # parede reta com saída
    return pts


def geometria(p: ParamsCopo) -> dict:
    """Medidas da matriz, com z = 0 na mesa e o copo de cabeça para baixo."""
    k = escala(p)
    H, Rb = p.altura * k, p.boca / 2 * k
    S = p.altura_reservatorio
    z_boca = p.espessura_base + p.altura_plug + S          # boca do copo (linha de corte)
    r_res_topo = Rb + p.degrau_corte                        # reservatório junto ao degrau
    r_res_base = r_res_topo + S * math.tan(math.radians(p.saida_reservatorio))
    R_in = math.ceil(r_res_base + p.margem_gesso)
    z_topo = z_boca + H                                     # apoio do pé
    z_centro = z_topo - p.altura_pe * k                     # centro do fundo (dentro do anel)
    return dict(H=H, Rb=Rb, S=S, z_boca=z_boca, z_plug=p.espessura_base + p.altura_plug,
                r_res_topo=r_res_topo, r_res_base=r_res_base, R_in=R_in,
                z_topo=z_topo, z_centro=z_centro,
                altura_anel=math.ceil(z_topo + p.margem_gesso - p.espessura_base))


def perfil_matriz(p: ParamsCopo) -> np.ndarray:
    """Contorno (r, z) da parte da matriz que fica em contato com o gesso:
    reservatório (de pé na mesa) + copo invertido."""
    g = geometria(p)
    pts = [(0.0, g["z_plug"] - 0.5), (g["r_res_base"], g["z_plug"] - 0.5), (g["r_res_base"], g["z_plug"]),
           (g["r_res_topo"], g["z_boca"]), (g["Rb"], g["z_boca"])]
    copo = perfil_copo(p)[::-1]                    # da boca até o fundo
    for r, h in copo[1:]:
        pts.append((r, g["z_topo"] - h))
    return np.array(pts)


# --------------------------------------------------------------------------
# Sólidos
# --------------------------------------------------------------------------
def revolve(pts: np.ndarray, seg: int) -> Manifold:
    return Manifold.revolve(CrossSection([pts]), seg)


def regiao_matriz(p: ParamsCopo) -> Polygon:
    pf = perfil_matriz(p)
    return Polygon(np.r_[pf, [[0.0, pf[0, 1]]]]).buffer(0)


def regiao_oca(p: ParamsCopo) -> Polygon:
    """Interior oco da matriz, aberto embaixo (atravessa a base)."""
    g = geometria(p)
    t = p.espessura_casca
    dentro = regiao_matriz(p).buffer(-t, join_style=2)
    r_abre = g["r_res_base"] - t - 2
    return dentro.union(box(0, -1, r_abre, g["z_plug"] + t + 1)).intersection(box(0, -1, 1e4, 1e4))


def poligono_rz(poly: Polygon) -> np.ndarray:
    poly = max(getattr(poly, "geoms", [poly]), key=lambda g: g.area)
    xy = np.asarray(poly.exterior.coords)[:-1]
    xy[:, 0] = np.maximum(xy[:, 0], 0.0)
    if Polygon(xy).exterior.is_ccw is False:
        xy = xy[::-1]
    return xy


def matriz_copo(p: ParamsCopo) -> Manifold:
    g = geometria(p)
    base = CrossSection.circle(g["R_in"] + p.parede + 3, p.segmentos).extrude(p.espessura_base)
    plug = CrossSection.circle(g["R_in"] - p.folga, p.segmentos).extrude(p.altura_plug + 0.01).translate(
        (0, 0, p.espessura_base))
    corpo = base + plug + revolve(perfil_matriz(p), p.segmentos)
    oco = revolve(poligono_rz(regiao_oca(p)), p.segmentos)
    m = corpo - oco
    if p.canal_desmolde:
        # tubo central (do chão da impressão até o fundo do copo) + 3 nervuras de travamento
        alto = g["z_centro"] + 1
        tubo = Manifold.cylinder(alto, 6.5, 6.5, 64) + Manifold.cylinder(18, 13, 13, 96)
        nerv = Manifold()
        for a in (90, 210, 330):
            nerv = nerv + Manifold.cube((g["R_in"], 2.0, alto)).translate((0, -1.0, 0)).rotate((0, 0, a))
        m = m + ((tubo + nerv) ^ oco)
        m = m - Manifold.cylinder(g["z_topo"] + 2, p.diametro_canal / 2, p.diametro_canal / 2, 48).translate((0, 0, -1))
        rc = p.diametro_cabeca_pino / 2 + 0.6
        m = m - Manifold.cylinder(p.espessura_cabeca_pino + 2, rc, rc, 64).translate((0, 0, -1))
    return m


def comprimento_pino(p: ParamsCopo) -> float:
    g = geometria(p)
    return g["z_centro"] - (p.espessura_cabeca_pino + 1) + p.saliencia_pino


def pino(p: ParamsCopo) -> Manifold:
    cab = Manifold.cylinder(p.espessura_cabeca_pino, p.diametro_cabeca_pino / 2, p.diametro_cabeca_pino / 2, 96)
    L, r = comprimento_pino(p), p.diametro_pino / 2
    haste = Manifold.cylinder(L - 0.8, r, r, 48) + Manifold.cylinder(0.8, r, r - 0.5, 48).translate((0, 0, L - 0.8))
    return cab + haste.translate((0, 0, p.espessura_cabeca_pino))


def anel_copo(p: ParamsCopo) -> Manifold:
    g = geometria(p)
    return anel_segmento(g["R_in"], p.parede, p.aba_presilha, g["altura_anel"], p.segmentos_anel)


# --------------------------------------------------------------------------
# Desenho em corte
# --------------------------------------------------------------------------
def espelha(poly: Polygon) -> Polygon:
    from shapely.affinity import scale
    return poly.union(scale(poly, -1, 1, origin=(0, 0))).buffer(0)


def corte(p: ParamsCopo, caminho: str, parede_peca: float = 4.0) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    g = geometria(p)
    R, zp = g["R_in"], g["z_plug"]
    zt = p.espessura_base + g["altura_anel"]
    mat = espelha(regiao_matriz(p))
    oco = espelha(regiao_oca(p))

    def pinta(ax, geom, **kw):
        for poly in getattr(geom, "geoms", [geom]):
            if poly.geom_type == "Polygon" and not poly.is_empty:
                x, y = poly.exterior.xy
                ax.fill(x, y, **kw)
                for i in poly.interiors:
                    xi, yi = i.xy
                    ax.fill(xi, yi, color="white", lw=0)
                kw.pop("label", None)

    def estilo(ax, titulo):
        ax.set_aspect("equal"); ax.set_title(titulo, fontsize=9.5)
        ax.set_yticks([]); ax.set_xlabel("mm")
        ax.legend(loc="upper left", fontsize=7, frameon=False)
        for s in ("top", "right", "left"):
            ax.spines[s].set_visible(False)

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(13, 8.2), dpi=120)

    # 1) fazendo o molde
    a1.fill_between([-R - 20, R + 20], -8, 0, color="#cfd6da", label="mesa")
    gesso = box(-R, zp, R, zt).difference(mat)
    pinta(a1, gesso, color="#e8e2d6", ec="#9c9284", lw=1, label="gesso (despejado por cima)")
    casca = mat.union(box(-R - 7 - p.parede, 0, R + 7 + p.parede, p.espessura_base)).union(box(-R, 0, R, zp))
    casca = casca.difference(oco)
    if p.canal_desmolde:
        tubo = box(-6.5, 0, 6.5, g["z_centro"]).union(box(-13, 0, 13, 18)).intersection(oco)
        casca = casca.union(tubo)
        rc = p.diametro_canal / 2
        casca = casca.difference(box(-rc, -1, rc, g["z_topo"] + 1)).difference(
            box(-p.diametro_cabeca_pino / 2 - 0.6, -1, p.diametro_cabeca_pino / 2 + 0.6, p.espessura_cabeca_pino + 1))
    pinta(a1, casca, color="#b9a3e3", ec="#7d66b0", lw=0.8, label="matriz impressa (oca)")
    if p.canal_desmolde:
        hc = p.diametro_cabeca_pino / 2
        pin = box(-hc, 1, hc, 1 + p.espessura_cabeca_pino).union(
            box(-p.diametro_pino / 2, 1 + p.espessura_cabeca_pino, p.diametro_pino / 2, g["z_centro"] + p.saliencia_pino))
        pinta(a1, pin, color="#f2c94c", ec="#a8841d", lw=0.8, label="pino no tubo central")
    for x in (-R - p.parede, R):
        a1.fill_between([x, x + p.parede], p.espessura_base, zt, color="#9b85cf")
    a1.set_xlim(-R - 25, R + 25); a1.set_ylim(-10, zt + 30)
    estilo(a1, "1) Fazendo o molde: matriz na base, anel em volta, gesso por cima")

    # 2) molde pronto (virado: a face da base vira a boca)
    blk = box(-R, 0, R, zt - zp)
    cav = espelha(regiao_matriz(p)).intersection(box(-R, zp, R, zt))
    from shapely.affinity import scale, translate
    cav = translate(scale(cav, 1, -1, origin=(0, 0)), 0, zt)            # vira de cabeça para baixo
    gesso2 = blk.difference(cav)
    pinta(a2, gesso2, color="#e8e2d6", ec="#9c9284", lw=1, label="gesso – molde de 1 peça")
    cascaz = cav.intersection(gesso2.buffer(parede_peca, resolution=16))
    y_corte = zt - zp - g["S"]
    pinta(a2, cascaz.intersection(box(-R, -1, R, y_corte)), color="#b5653f", label=f"parede colada (~{parede_peca:g} mm) = o copo")
    pinta(a2, cascaz.intersection(box(-R, y_corte, R, zt)), color="#e0b49c", label="sobra do reservatório (aparar)")
    a2.plot([-R, R], [y_corte, y_corte], color="#7a2e12", lw=0.8, ls="--")
    a2.text(R - 2, y_corte + 1.5, "linha de corte", ha="right", fontsize=8, color="#7a2e12")
    k = escala(p)
    a2.annotate(f"pé em anel Ø {p.diametro_pe*k:.0f} × {p.altura_pe*k:.0f} mm",
                xy=(p.diametro_pe * k / 2 - 3, zt - zp - g["z_topo"] + zp + 2), xytext=(8, 8), fontsize=8,
                arrowprops=dict(arrowstyle="->", lw=0.7))
    a2.set_xlim(-R - 25, R + 25); a2.set_ylim(-10, zt + 30)
    estilo(a2, f"2) Molde pronto, boca para cima — copo cru: altura {g['H']:.0f}, boca Ø {2*g['Rb']:.0f} mm")

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

    k = escala(p)
    rc = p.boca / 2 - (p.altura - p.altura_curva) * math.tan(math.radians(p.saida_parede))
    assert p.diametro_pe / 2 + p.aba_fundo < rc, "pé grande demais para o fundo"
    assert p.largura_anel_pe < p.diametro_pe / 2 - 8
    assert p.altura_pe < p.altura_curva < p.altura

    g = geometria(p)
    os.makedirs(a.saida, exist_ok=True)
    pp = ParamsPrato(parede=p.parede, aba_presilha=p.aba_presilha)
    pecas = {
        "matriz_copo": matriz_copo(p),
        "anel_quarto" if p.segmentos_anel == 4 else f"anel_1_de_{p.segmentos_anel}": anel_copo(p),
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

    print(f"  Copo cru: altura {g['H']:.1f} mm, boca Ø {2*g['Rb']:.1f}, pé em anel Ø {p.diametro_pe*k:.1f}"
          + (f"  (retração {p.retracao:g}% -> queimado: altura {p.altura:g}, boca {p.boca:g})" if p.retracao else ""))
    zt = p.espessura_base + g["altura_anel"]
    cil = CrossSection.circle(g["R_in"], p.segmentos).extrude(zt - g["z_plug"]).translate((0, 0, g["z_plug"]))
    v = (cil - revolve(perfil_matriz(p), p.segmentos)).volume() / 1000.0
    gr, w = receita(v)
    print(f"  Bloco de gesso: Ø {2*g['R_in']} x {zt - g['z_plug']:.0f} mm")
    print(f"  Gesso: ~{v/1000:.2f} L de mistura -> {gr/1000:.2f} kg de gesso + {w/1000:.2f} L de água")

    if a.preview:
        pasta = os.path.join(raiz, "imagens")
        os.makedirs(pasta, exist_ok=True)
        corte(p, os.path.join(pasta, "corte_copo.png"))
        print("  imagens/corte_copo.png gerado")


if __name__ == "__main__":
    main()
