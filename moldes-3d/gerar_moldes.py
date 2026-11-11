#!/usr/bin/env python3
"""
Gerador de matrizes 3D para moldes de gesso — Barro na Veia
============================================================

Gera os arquivos STL de um sistema de "caixa de contenção" impressa em 3D
para fazer um MOLDE DE PRENSAGEM DE 2 PARTES em gesso para um prato em forma
de flor:

  * base_femea.stl   -> base com o positivo (o "corpo" do prato) em relevo.
                        Gesso derramado aqui vira o molde FÊMEA (côncavo).
  * base_macho.stl   -> base com o rebaixo do prato (já descontada a
                        espessura da argila). Gesso derramado aqui vira o
                        molde MACHO (convexo).
  * anel_metade.stl  -> metade da parede circular (imprimir 2x).
  * presilha.stl     -> presilha em "C" que trava as duas metades (imprimir 4x).

As duas bases usam o MESMO anel. As chaves de registro (bolinhas na fêmea,
covinhas no macho) fazem as duas peças de gesso encaixarem sempre na mesma
posição.

Todas as medidas estão em milímetros e podem ser alteradas pela linha de
comando. Exemplo para um prato maior (precisa de mesa de impressão maior):

    python3 gerar_moldes.py --raio-petala 95 --raio-anel 120

Dependências: numpy, shapely, trimesh, manifold3d (+ matplotlib, scipy e networkx para --preview)
    pip install numpy shapely trimesh manifold3d matplotlib scipy networkx
"""

from __future__ import annotations

import argparse
import math
import os
from dataclasses import dataclass

import numpy as np
import trimesh
from manifold3d import CrossSection, Manifold, Mesh
from shapely.geometry import Point, Polygon


# --------------------------------------------------------------------------
# Parâmetros
# --------------------------------------------------------------------------
@dataclass
class Params:
    # Prato (medidas da peça CRUA, antes da retração da argila)
    petalas: int = 5            # número de pétalas
    raio_petala: float = 80.0   # raio na ponta das pétalas (mm)
    raio_vale: float = 68.0     # raio no encontro entre pétalas (mm)
    profundidade: float = 25.0  # profundidade do prato (mm)
    largura_aba: float = 22.0   # quanto a borda "entra" até o fundo plano (mm)
    espessura_argila: float = 6.0  # espessura da placa de argila (mm)
    marca_pe: bool = True       # anel em relevo marcando o pé no fundo
    raio_marca_pe: float = 40.0

    # Caixa de contenção
    raio_anel: float = 100.0    # raio INTERNO do anel (mm)
    parede: float = 4.0         # espessura da parede do anel (mm)
    altura_anel: float = 65.0   # altura do anel (mm)
    aba_presilha: float = 10.0  # comprimento das abas onde entram as presilhas
    folga: float = 0.25         # folga de encaixe para impressão (mm)
    altura_presilha: float = 20.0
    folga_presilha: float = 0.3  # maior = presilha mais frouxa

    # Base
    espessura_base: float = 3.0
    altura_plug_femea: float = 4.0

    # Chaves de registro
    raio_chave: float = 5.0
    folga_chave: float = 0.4

    # Malha
    resolucao_angular: int = 360
    camadas: int = 48


# --------------------------------------------------------------------------
# Geometria 2D da flor
# --------------------------------------------------------------------------
def contorno_flor(p: Params, n: int = 1440) -> Polygon:
    """Contorno da flor na borda do prato (pétalas arredondadas, vales suaves).
    Uma pétala fica sempre apontando para +Y, o que deixa a flor simétrica
    em relação ao eixo Y (importante para o macho casar com a fêmea depois de
    virado)."""
    th = np.linspace(0, 2 * np.pi, n, endpoint=False)
    onda = 0.5 + 0.5 * np.cos(p.petalas * (th - np.pi / 2))
    r = p.raio_vale + (p.raio_petala - p.raio_vale) * onda ** 0.6
    return Polygon(np.c_[r * np.cos(th), r * np.sin(th)])


def recuo_parede(p: Params, u: np.ndarray | float) -> np.ndarray | float:
    """Recuo horizontal da parede do prato em função da altura relativa u∈[0,1].
    Começa com ~17° de saída (para desmoldar) e termina tangente ao fundo plano."""
    u = np.clip(u, 0.0, 1.0)
    return p.largura_aba * (0.35 * u + 0.65 * (1.0 - np.sqrt(1.0 - u ** 2)))


def secao_femea(p: Params, flor: Polygon, h: float) -> Polygon:
    """Seção horizontal do positivo do prato na altura h (0 = borda)."""
    return flor.buffer(-float(recuo_parede(p, h / p.profundidade)), resolution=32)


def secao_macho(p: Params, flor: Polygon, z: float) -> Polygon:
    """Seção do macho: erosão 3D do positivo por uma esfera com raio igual à
    espessura da argila (aproximada por fatias). Resultado: superfície que fica
    exatamente 'espessura_argila' afastada da fêmea em toda a peça."""
    t = p.espessura_argila
    reg = None
    for dz in np.linspace(-t, t, 25):
        h = z + dz
        if h < 0:
            continue  # abaixo do plano de partição: tudo é gesso, sem restrição
        if h > p.profundidade + 1e-9:
            return Polygon()
        rho = math.sqrt(max(t * t - dz * dz, 0.0))
        s = secao_femea(p, flor, h).buffer(-rho, resolution=32)
        reg = s if reg is None else reg.intersection(s)
        if reg.is_empty:
            return Polygon()
    return reg


def raio_polar(poly: Polygon, th: np.ndarray) -> np.ndarray:
    """Amostra o contorno (estrelado em relação à origem) em coordenadas polares."""
    if poly.geom_type == "MultiPolygon":
        poly = max(poly.geoms, key=lambda g: g.area)
    xy = np.asarray(poly.exterior.coords)[:-1]
    ang = np.arctan2(xy[:, 1], xy[:, 0])
    rad = np.hypot(xy[:, 0], xy[:, 1])
    ordem = np.argsort(ang)
    ang, rad = ang[ordem], rad[ordem]
    return np.interp(th, ang, rad, period=2 * np.pi)


# --------------------------------------------------------------------------
# Malhas
# --------------------------------------------------------------------------
def loft(zs: list[float], raios: list[np.ndarray], th: np.ndarray) -> Manifold:
    """Sólido fechado ligando camadas polares (z crescente)."""
    n, m = len(th), len(zs)
    verts = []
    for z, r in zip(zs, raios):
        verts.append(np.c_[r * np.cos(th), r * np.sin(th), np.full(n, z)])
    verts = np.vstack(verts + [[[0, 0, zs[0]]], [[0, 0, zs[-1]]]])
    cb, ct = m * n, m * n + 1
    tris = []
    for k in range(m - 1):
        for i in range(n):
            a = k * n + i
            b = k * n + (i + 1) % n
            c = (k + 1) * n + (i + 1) % n
            d = (k + 1) * n + i
            tris += [[a, b, c], [a, c, d]]
    for i in range(n):
        tris.append([cb, (i + 1) % n, i])
        tris.append([ct, (m - 1) * n + i, (m - 1) * n + (i + 1) % n])
    tm = trimesh.Trimesh(verts, np.array(tris), process=True)
    trimesh.repair.fix_normals(tm)
    assert tm.is_volume, "loft não ficou fechado"
    return Manifold(Mesh(np.asarray(tm.vertices, np.float32),
                         np.asarray(tm.faces, np.uint32)))


def positivo_prato(p: Params, flor: Polygon) -> Manifold:
    th = np.linspace(-np.pi, np.pi, p.resolucao_angular, endpoint=False)
    # distribui mais camadas perto do topo, onde a curva é mais fechada
    us = np.sin(np.linspace(0, np.pi / 2, p.camadas))
    zs = [-0.6] + list(us * p.profundidade)
    raios = [raio_polar(flor, th)] + [raio_polar(secao_femea(p, flor, z), th) for z in zs[1:]]
    corpo = loft(zs, raios, th)
    if p.marca_pe:
        anel = (CrossSection.circle(p.raio_marca_pe + 0.8, 128)
                - CrossSection.circle(p.raio_marca_pe - 0.8, 128))
        corpo = corpo + anel.extrude(1.4).translate((0, 0, p.profundidade - 0.6))
    return corpo


def negativo_macho(p: Params, flor: Polygon) -> tuple[Manifold, float]:
    th = np.linspace(-np.pi, np.pi, p.resolucao_angular, endpoint=False)
    zmax = p.profundidade - p.espessura_argila
    us = np.sin(np.linspace(0, np.pi / 2, p.camadas))
    zs = list(us * zmax)
    zs[-1] = zmax - 0.05
    raios = [raio_polar(secao_macho(p, flor, z), th) for z in zs]
    zs = [-1.0] + zs
    raios = [raios[0]] + raios
    # sobe a partir do plano de partição; espelha para virar um rebaixo
    return loft(zs, raios, th).mirror((0, 0, 1)), zmax


def angulos_chaves(p: Params) -> list[float]:
    # nos vales entre pétalas; conjunto simétrico em Y e sem simetria de giro,
    # então as peças só encaixam numa posição
    passo = 360.0 / p.petalas
    vales = [90 + passo / 2 + k * passo for k in range(p.petalas)]
    return [math.radians(a) for a in (vales[0], vales[-1], 270.0)]


def raio_chaves(p: Params) -> float:
    # chaves ficam nos vales, onde sobra mais espaço entre a flor e o anel
    return (p.raio_vale + p.raio_anel) / 2 + 2


def base_comum(p: Params, altura_plug: float) -> Manifold:
    """Disco + 'plug' sobre o qual o anel encaixa. Plano de partição em z=0."""
    aba = CrossSection.circle(p.raio_anel + p.parede + 3, 256).extrude(p.espessura_base)
    aba = aba.translate((0, 0, -altura_plug - p.espessura_base))
    plug = CrossSection.circle(p.raio_anel - p.folga, 256).extrude(altura_plug + 0.01)
    plug = plug.translate((0, 0, -altura_plug))
    return aba + plug


def base_femea(p: Params, flor: Polygon) -> Manifold:
    b = base_comum(p, p.altura_plug_femea) + positivo_prato(p, flor)
    rk = raio_chaves(p)
    for a in angulos_chaves(p):
        esf = Manifold.sphere(p.raio_chave, 64).translate((rk * math.cos(a), rk * math.sin(a), 0))
        b = b + esf.trim_by_plane((0, 0, 1), 0)
    return b


def base_macho(p: Params, flor: Polygon) -> Manifold:
    neg, zmax = negativo_macho(p, flor)
    plug = zmax + 3.0
    b = base_comum(p, plug) - neg
    rk = raio_chaves(p)
    for a in angulos_chaves(p):
        b = b - Manifold.sphere(p.raio_chave - p.folga_chave, 64).translate(
            (rk * math.cos(a), rk * math.sin(a), 0))
    return b


def anel_metade(p: Params) -> Manifold:
    ri, ro = p.raio_anel, p.raio_anel + p.parede
    anel = CrossSection.circle(ro, 512) - CrossSection.circle(ri, 512)
    metade = anel ^ CrossSection.square((ro + 1, 2 * ro + 2)).translate((0, -ro - 1))
    abas = (CrossSection.square((p.parede, ro - ri + p.aba_presilha)).translate((0, ri))
            + CrossSection.square((p.parede, ro - ri + p.aba_presilha)).translate((0, -ro - p.aba_presilha)))
    return (metade + abas).extrude(p.altura_anel)


def presilha(p: Params) -> Manifold:
    vao = 2 * p.parede + p.folga_presilha   # justo: trava por atrito
    prof = p.aba_presilha + 0.4
    w = 3.0
    ext = CrossSection.square((vao + 2 * w, prof + w))
    furo = CrossSection.square((vao, prof + 1)).translate((w, w))
    return (ext - furo).extrude(p.altura_presilha)


# --------------------------------------------------------------------------
# Saída
# --------------------------------------------------------------------------
def para_trimesh(m: Manifold) -> trimesh.Trimesh:
    mesh = m.to_mesh()
    tm = trimesh.Trimesh(np.asarray(mesh.vert_properties)[:, :3], np.asarray(mesh.tri_verts))
    tm.apply_translation((0, 0, -tm.bounds[0][2]))  # apoia na mesa (z=0)
    return tm


def volume_gesso_ml(p: Params, base: Manifold, altura_plug: float) -> float:
    """Volume de gesso dentro do anel acima da base (ml)."""
    # o anel apoia na aba da base e sobe 'altura_anel' a partir dali
    cil = CrossSection.circle(p.raio_anel, 256).extrude(p.altura_anel).translate((0, 0, -altura_plug))
    return (cil - base).volume() / 1000.0


def receita(vol_ml: float, consistencia: float = 70.0) -> tuple[float, float]:
    """Gesso (g) e água (ml) para um volume de mistura, consistência 70
    (70 partes de água para 100 de gesso). Inclui 10% de sobra."""
    vol_por_100g = 100 / 2.65 + consistencia  # cm³ de mistura por 100 g de gesso
    gesso = vol_ml * 1.10 / vol_por_100g * 100
    return gesso, gesso * consistencia / 100


def _topo(tm: trimesh.Trimesh, ang: float, rs: np.ndarray) -> np.ndarray:
    """Altura máxima da peça ao longo de uma linha radial (corte vertical)."""
    a = math.radians(ang)
    sec = tm.section(plane_origin=[0, 0, 0], plane_normal=[-math.sin(a), math.cos(a), 0])
    z = np.full_like(rs, -np.inf)
    for pts in sec.discrete:
        r = pts[:, 0] * math.cos(a) + pts[:, 1] * math.sin(a)
        for (r0, z0), (r1, z1) in zip(zip(r[:-1], pts[:-1, 2]), zip(r[1:], pts[1:, 2])):
            lo, hi = min(r0, r1), max(r0, r1)
            m = (rs >= lo) & (rs <= hi)
            if hi - lo < 1e-9:
                z[m] = np.maximum(z[m], max(z0, z1))
            else:
                z[m] = np.maximum(z[m], z0 + (rs[m] - r0) / (r1 - r0) * (z1 - z0))
    return z


def preview(p: Params, pecas: dict[str, trimesh.Trimesh], caminho: str) -> None:
    """Desenho em corte do molde pronto: fêmea embaixo, argila, macho em cima."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    R = p.raio_anel
    rs = np.linspace(-R + 0.5, R - 0.5, 1601)
    plug_m = p.profundidade - p.espessura_argila + 3
    # corte passando por uma pétala (+y) e por uma chave (-y)
    fem = _topo(pecas["base_femea"], 90, rs) - (p.espessura_base + p.altura_plug_femea)
    mac = _topo(pecas["base_macho"], 90, rs) - (p.espessura_base + plug_m)
    sup_f = -np.maximum(fem, 0)          # fêmea virada: cavidade para cima
    sup_m = np.minimum(mac, 0)           # macho usado na posição em que foi moldado
    H = 45.0

    fig, ax = plt.subplots(figsize=(11, 4.6), dpi=130)
    ax.fill_between(rs, -H, sup_f, color="#e8e2d6", ec="#9c9284", lw=1, label="gesso – molde FÊMEA")
    ax.fill_between(rs, sup_m, H, color="#dfe6ea", ec="#8a969c", lw=1, label="gesso – molde MACHO")
    argila = (sup_m > sup_f + 0.05) & (np.abs(rs) < raio_chaves(p) - p.raio_chave - 1)
    ax.fill_between(rs, sup_f, sup_m, where=argila, color="#b5653f", label=f"argila ({p.espessura_argila:g} mm)")
    ax.axhline(0, color="#555", lw=0.6, ls="--")
    ax.text(R * 0.99, 1.5, "plano de partição", ha="right", fontsize=8, color="#555")
    ax.set_xlim(-R - 5, R + 5); ax.set_ylim(-H - 5, H + 5); ax.set_aspect("equal")
    ax.set_xlabel("mm"); ax.set_yticks([])
    ax.set_title("Corte do molde de prensagem pronto (passando por uma pétala e por uma chave de registro)", fontsize=10)
    ax.legend(loc="upper left", fontsize=8, frameon=False)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    plt.tight_layout()
    plt.savefig(caminho)
    plt.close(fig)


def main() -> None:
    p = Params()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    for campo, valor in vars(p).items():
        opt = "--" + campo.replace("_", "-")
        if isinstance(valor, bool):
            ap.add_argument(opt, type=lambda s: s.lower() in ("1", "sim", "true", "s"), default=valor)
        else:
            ap.add_argument(opt, type=type(valor), default=valor)
    ap.add_argument("--saida", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "stl"))
    ap.add_argument("--preview", action="store_true", help="gera imagens/corte.png (desenho em corte)")
    args = ap.parse_args()
    p = Params(**{k: getattr(args, k) for k in vars(p)})

    assert p.raio_vale < p.raio_petala
    assert p.largura_aba < p.raio_vale, "largura_aba grande demais para a flor"
    assert raio_chaves(p) + p.raio_chave < p.raio_anel - 3, "sem espaço para as chaves: aumente --raio-anel"

    flor = contorno_flor(p)
    os.makedirs(args.saida, exist_ok=True)

    fem = base_femea(p, flor)
    mac = base_macho(p, flor)
    pecas = {
        "base_femea": fem,
        "base_macho": mac,
        "anel_metade": anel_metade(p),
        "presilha": presilha(p),
    }
    malhas = {}
    for nome, m in pecas.items():
        tm = para_trimesh(m)
        assert tm.is_watertight, f"{nome} não está fechado"
        tm.export(os.path.join(args.saida, f"{nome}.stl"))
        malhas[nome] = tm
        dx, dy, dz = tm.extents
        print(f"{nome:12s} {dx:6.1f} x {dy:6.1f} x {dz:5.1f} mm   {len(tm.faces):7d} triângulos")

    zmax_macho = p.profundidade - p.espessura_argila
    for nome, base, plug in (("fêmea", fem, p.altura_plug_femea), ("macho", mac, zmax_macho + 3)):
        v = volume_gesso_ml(p, base, plug)
        g, a = receita(v)
        print(f"Gesso para o molde {nome}: ~{v/1000:.2f} L de mistura -> {g/1000:.2f} kg de gesso + {a/1000:.2f} L de água")

    if args.preview:
        destino = os.path.join(os.path.dirname(args.saida), "imagens", "corte.png")
        os.makedirs(os.path.dirname(destino), exist_ok=True)
        preview(p, malhas, destino)
        print("imagens/corte.png gerado")


if __name__ == "__main__":
    main()
