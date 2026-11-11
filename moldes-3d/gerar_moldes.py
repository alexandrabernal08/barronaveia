#!/usr/bin/env python3
"""
Gerador de matrizes 3D para moldes de gesso — Barro na Veia
============================================================

Gera os arquivos STL para fazer, em gesso, moldes de um prato em forma de flor.

stl/barbotina/  -> MOLDE DE COLAGEM (barbotina), 1 peça
  * matriz_barbotina.stl -> positivo do prato + reservatório + degrau de corte.
                            Vai colado numa mesa lisa (vidro/fórmica).
  * anel_quarto.stl      -> 1/4 da parede de contenção (imprimir 3x).
  * anel_quarto_logo.stl -> o 4º quarto, com o logo da escola em relevo por dentro.
  * presilha.stl         -> presilha em "C" (imprimir 8x).
  * pino_desmolde.stl    -> pino que tampa o canal de ar durante o despejo.

stl/prensagem/  -> MOLDE DE PRENSAGEM (placa de argila), 2 peças
  * base_femea.stl   -> base com o positivo do prato em relevo -> molde FÊMEA.
  * base_macho.stl   -> base com o rebaixo do prato (descontada a espessura
                        da argila) -> molde MACHO.
  * anel_metade.stl  -> metade da parede circular (imprimir 1x).
  * anel_metade_logo.stl -> a outra metade, com o logo da escola em relevo por dentro.
  * presilha.stl     -> presilha em "C" (imprimir 4x).

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

    # Molde de colagem (barbotina)
    altura_reservatorio: float = 20.0   # sobra acima da borda do prato (mm)
    degrau_corte: float = 2.0           # ressalto que marca onde aparar a borda (mm)
    saida_reservatorio: float = 5.0     # inclinação da parede do reservatório (graus)
    raio_anel_barbotina: float = 120.0  # raio INTERNO da contenção (mm)
    altura_anel_barbotina: float = 80.0
    segmentos_anel_barbotina: int = 4   # em quantas partes o anel é impresso

    # Canal + pino de desmoldagem (matriz de barbotina)
    canal_desmolde: bool = True
    diametro_canal: float = 4.2         # cabe o bico de uma seringa comum
    diametro_pino: float = 3.9
    diametro_bolso: float = 34.0        # rebaixo embaixo da matriz, para a cabeça do pino
    profundidade_bolso: float = 12.0
    diametro_cabeca_pino: float = 18.0
    espessura_cabeca_pino: float = 3.0
    saliencia_pino: float = 0.2         # o pino passa um tiquinho da superfície

    # Marca da escola gravada na parede externa do gesso
    logo: bool = True
    logo_arquivo: str = ""               # vazio = marca/logo.png se existir, senão fonte Barrio
    logo_profundidade: float = 1.2
    logo_largura_barbotina: float = 55.0
    logo_largura_prensagem: float = 38.0

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


def matriz_barbotina(p: Params, flor: Polygon, canal: bool | None = None) -> Manifold:
    """Positivo para molde de colagem de 1 peça, de cabeça para baixo como vai
    na mesa: embaixo o reservatório (mais largo na mesa, para desmoldar), depois
    o degrau de corte na altura da borda do prato e, em cima, o corpo do prato.

    Canal de desmoldagem: um furo atravessa a matriz no centro, do fundo do
    prato até um rebaixo (bolso) na face de baixo. Durante o despejo do gesso o
    furo fica tampado pelo pino. Depois de o gesso endurecer e o bloco ser
    virado, tira-se o pino e injeta-se ar ou água com uma seringa: isso quebra
    o vácuo (efeito ventosa) entre o plástico e o gesso e empurra a matriz."""
    th = np.linspace(-np.pi, np.pi, p.resolucao_angular, endpoint=False)
    S, D = p.altura_reservatorio, p.profundidade
    alarga = S * math.tan(math.radians(p.saida_reservatorio))
    zs = [0.0, S]
    raios = [raio_polar(flor.buffer(p.degrau_corte + alarga, resolution=32), th),
             raio_polar(flor.buffer(p.degrau_corte, resolution=32), th)]
    us = np.sin(np.linspace(0, np.pi / 2, p.camadas))
    for u in us:
        zs.append(S + u * D)
        raios.append(raio_polar(secao_femea(p, flor, u * D), th))
    corpo = loft(zs, raios, th)
    if p.marca_pe:
        anel = (CrossSection.circle(p.raio_marca_pe + 0.8, 128)
                - CrossSection.circle(p.raio_marca_pe - 0.8, 128))
        corpo = corpo + anel.extrude(1.4).translate((0, 0, S + D - 0.6))
    if p.canal_desmolde if canal is None else canal:
        corpo = corpo - Manifold.cylinder(S + D + 2, p.diametro_canal / 2, p.diametro_canal / 2, 48).translate((0, 0, -1))
        corpo = corpo - Manifold.cylinder(p.profundidade_bolso + 1, p.diametro_bolso / 2, p.diametro_bolso / 2, 128).translate((0, 0, -1))
    return corpo


def comprimento_pino(p: Params) -> float:
    """Haste do pino: do teto do bolso até a superfície do fundo do prato."""
    return p.altura_reservatorio + p.profundidade - p.profundidade_bolso + p.saliencia_pino


def pino_desmolde(p: Params) -> Manifold:
    """Pino que tampa o canal enquanto o gesso é despejado (imprimir em pé,
    com a cabeça na mesa)."""
    cab = Manifold.cylinder(p.espessura_cabeca_pino, p.diametro_cabeca_pino / 2, p.diametro_cabeca_pino / 2, 96)
    L = comprimento_pino(p)
    r = p.diametro_pino / 2
    haste = Manifold.cylinder(L - 0.6, r, r, 48) + Manifold.cylinder(0.6, r, r - 0.4, 48).translate((0, 0, L - 0.6))
    return cab + haste.translate((0, 0, p.espessura_cabeca_pino))


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


def anel_segmento(ri: float, parede: float, aba: float, altura: float, n: int) -> Manifold:
    """1/n de um anel de contenção, com abas para presilha nas duas pontas."""
    ro = ri + parede
    ang = 2 * math.pi / n
    arco = np.linspace(0, ang, 256)
    cunha = CrossSection([np.r_[[[0.0, 0.0]], np.c_[2 * ro * np.cos(arco), 2 * ro * np.sin(arco)]]])
    anel = (CrossSection.circle(ro, 512) - CrossSection.circle(ri, 512)) ^ cunha
    aba0 = CrossSection.square((ro - ri + aba, parede)).translate((ri, 0))
    aba1 = CrossSection.square((ro - ri + aba, parede)).translate((ri, -parede)).rotate(math.degrees(ang))
    return (anel + aba0 + aba1).extrude(altura)


def anel_metade(p: Params) -> Manifold:
    return anel_segmento(p.raio_anel, p.parede, p.aba_presilha, p.altura_anel, 2)


def anel_barbotina(p: Params) -> Manifold:
    return anel_segmento(p.raio_anel_barbotina, p.parede, p.aba_presilha,
                         p.altura_anel_barbotina, p.segmentos_anel_barbotina)


def com_logo(p: Params, anel: Manifold, raio: float, ang: float, z_c: float, largura: float) -> Manifold:
    """Une o logo em relevo à parede interna de um segmento de anel."""
    from marca import relevo_no_anel
    rel, h, _ = relevo_no_anel(raio, ang, z_c, largura, p.logo_profundidade, virado=True,
                               arquivo=p.logo_arquivo or None)
    return anel + rel


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
    # process=False: mantém a topologia exata do manifold (não funde vértices quase iguais)
    tm = trimesh.Trimesh(np.asarray(mesh.vert_properties)[:, :3], np.asarray(mesh.tri_verts), process=False)
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


def _plt():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    return plt


def corte_barbotina(p: Params, matriz: trimesh.Trimesh, caminho: str, parede_peca: float = 4.0) -> None:
    """Dois cortes: (1) o gesso sendo despejado sobre a matriz com o pino;
    (2) o molde de colagem pronto, virado, com a barbotina colada."""
    from shapely.geometry import box
    plt = _plt()
    R, H, S, D = p.raio_anel_barbotina, p.altura_anel_barbotina, p.altura_reservatorio, p.profundidade
    rs = np.linspace(-R + 0.5, R - 0.5, 2401)
    t = np.maximum(_topo(matriz, 90, rs), 0)   # altura da matriz sobre a mesa (sem o canal)

    def pinta(ax, g, **kw):
        for poly in getattr(g, "geoms", [g]):
            if poly.geom_type == "Polygon" and not poly.is_empty:
                x, y = poly.exterior.xy
                ax.fill(x, y, **kw)
                for interior in poly.interiors:
                    xi, yi = interior.xy
                    ax.fill(xi, yi, color="white", lw=0)
                kw.pop("label", None)

    def estilo(ax, titulo, y0, y1):
        ax.set_xlim(-R - 12, R + 12); ax.set_ylim(y0, y1); ax.set_aspect("equal")
        ax.set_yticks([]); ax.set_title(titulo, fontsize=10)
        ax.legend(loc="upper left", fontsize=7.5, frameon=False, ncol=3)
        for s_ in ("top", "right", "left"):
            ax.spines[s_].set_visible(False)

    fig, (a1, a2) = plt.subplots(2, 1, figsize=(11, 9), dpi=130)

    # ---- 1) moldagem: matriz na mesa, pino no lugar, gesso por cima
    matriz2d = Polygon(np.r_[np.c_[rs, t], [[rs[-1], 0], [rs[0], 0]]]).buffer(0)
    gesso = box(-R, 0, R, H).difference(matriz2d)
    rc, rb = p.diametro_canal / 2, p.diametro_bolso / 2
    furos = box(-rc, 0, rc, S + D).union(box(-rb, 0, rb, p.profundidade_bolso))
    hc, ec = p.diametro_cabeca_pino / 2, p.espessura_cabeca_pino
    pino = box(-hc, p.profundidade_bolso - ec, hc, p.profundidade_bolso).union(
        box(-p.diametro_pino / 2, p.profundidade_bolso, p.diametro_pino / 2, S + D))
    a1.fill_between([-R - 12, R + 12], -8, 0, color="#cfd6da", label="mesa lisa (vidro/fórmica)")
    pinta(a1, gesso, color="#e8e2d6", ec="#9c9284", lw=1, label="gesso (despejado por cima)")
    pinta(a1, matriz2d.difference(furos), color="#e9a7b8", ec="#b0707f", lw=0.8, label="matriz impressa")
    pinta(a1, pino, color="#f2c94c", ec="#a8841d", lw=0.8, label="pino tampando o canal")
    for x in (-R - 4, R):
        a1.fill_between([x, x + 4], 0, H, color="#c98ea0")
    a1.annotate("canal de ar", xy=(0, S + D * 0.6), xytext=(28, S + D + 18), fontsize=8,
                arrowprops=dict(arrowstyle="->", lw=0.7))
    a1.annotate("bolso com a cabeça do pino", xy=(rb * 0.7, p.profundidade_bolso / 2), xytext=(45, 6), fontsize=8,
                arrowprops=dict(arrowstyle="->", lw=0.7))
    estilo(a1, "1) Fazendo o molde: o pino tampa o canal enquanto o gesso está líquido", -10, H + 25)

    # ---- 2) molde pronto (virado)
    sup = -t
    gesso2 = Polygon(np.r_[np.c_[rs, sup], [[rs[-1], -H], [rs[0], -H]]]).buffer(0)
    cavidade = box(rs[0], -H, rs[-1], 0).difference(gesso2)
    casca = cavidade.intersection(gesso2.buffer(parede_peca, resolution=16))
    pinta(a2, gesso2, color="#e8e2d6", ec="#9c9284", lw=1, label="gesso – molde de colagem (1 peça)")
    pinta(a2, casca.intersection(box(-R, -H, R, -S)), color="#b5653f", label=f"parede colada (~{parede_peca:g} mm) = o prato")
    pinta(a2, casca.intersection(box(-R, -S, R, 0)), color="#e0b49c", label="sobra do reservatório (aparar)")
    a2.plot([-R, R], [-S, -S], color="#7a2e12", lw=0.8, ls="--")
    a2.text(R * 0.99, -S + 1.2, "linha de corte (degrau)", ha="right", fontsize=8, color="#7a2e12")
    a2.text(0, -S / 2, "reservatório: manter cheio de barbotina", ha="center", va="center", fontsize=8, color="#555")
    estilo(a2, "2) Molde pronto (virado, boca para cima) com a barbotina colada", -H - 5, 25)
    a2.set_xlabel("mm")

    plt.tight_layout()
    plt.savefig(caminho)
    plt.close(fig)


def corte_prensagem(p: Params, pecas: dict[str, trimesh.Trimesh], caminho: str) -> None:
    """Desenho em corte do molde pronto: fêmea embaixo, argila, macho em cima."""
    plt = _plt()

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
    ap.add_argument("--preview", action="store_true", help="gera os desenhos em corte em imagens/")
    args = ap.parse_args()
    p = Params(**{k: getattr(args, k) for k in vars(p)})

    assert p.raio_vale < p.raio_petala
    assert p.largura_aba < p.raio_vale, "largura_aba grande demais para a flor"
    assert raio_chaves(p) + p.raio_chave < p.raio_anel - 3, "sem espaço para as chaves: aumente --raio-anel"
    if p.canal_desmolde:
        assert p.profundidade_bolso + 6 < p.altura_reservatorio + p.profundidade, "bolso fundo demais"
        assert p.diametro_bolso / 2 + 3 < p.raio_vale - p.largura_aba, "bolso largo demais para o fundo do prato"
        assert p.diametro_pino < p.diametro_canal and p.diametro_canal < p.diametro_cabeca_pino < p.diametro_bolso - 8
    folga_lateral = p.raio_anel_barbotina - (p.raio_petala + p.degrau_corte
                                             + p.altura_reservatorio * math.tan(math.radians(p.saida_reservatorio)))
    if folga_lateral < 30:
        print(f"AVISO: só {folga_lateral:.0f} mm de gesso ao lado das pétalas no molde de barbotina; "
              "o ideal é 30–40 mm (aumente --raio-anel-barbotina).")

    flor = contorno_flor(p)

    def exporta(pasta: str, pecas: dict[str, Manifold]) -> dict[str, trimesh.Trimesh]:
        os.makedirs(pasta, exist_ok=True)
        print(f"\n[{os.path.basename(pasta)}]")
        malhas = {}
        for nome, m in pecas.items():
            tm = para_trimesh(m)
            assert tm.is_watertight, f"{nome} não está fechado"
            tm.export(os.path.join(pasta, f"{nome}.stl"))
            malhas[nome] = tm
            dx, dy, dz = tm.extents
            print(f"  {nome:17s} {dx:6.1f} x {dy:6.1f} x {dz:5.1f} mm   {len(tm.faces):7d} triângulos")
        return malhas

    def mostra_gesso(nome: str, v_ml: float) -> None:
        g, a = receita(v_ml)
        print(f"  Gesso para o molde {nome}: ~{v_ml/1000:.2f} L de mistura -> "
              f"{g/1000:.2f} kg de gesso + {a/1000:.2f} L de água")

    # ---- molde de colagem (barbotina)
    mb = matriz_barbotina(p, flor)
    nome_anel_b = "anel_quarto" if p.segmentos_anel_barbotina == 4 else f"anel_1_de_{p.segmentos_anel_barbotina}"
    barb = exporta(os.path.join(args.saida, "barbotina"), {
        "matriz_barbotina": mb,
        nome_anel_b: anel_barbotina(p),
        **({nome_anel_b + "_logo": com_logo(p, anel_barbotina(p), p.raio_anel_barbotina,
                                             180.0 / p.segmentos_anel_barbotina,
                                             p.altura_anel_barbotina / 2, p.logo_largura_barbotina)}
           if p.logo else {}),
        "presilha": presilha(p),
        **({"pino_desmolde": pino_desmolde(p)} if p.canal_desmolde else {}),
    })
    cil = CrossSection.circle(p.raio_anel_barbotina, 256).extrude(p.altura_anel_barbotina)
    mostra_gesso("de colagem", (cil - matriz_barbotina(p, flor, canal=False)).volume() / 1000.0)

    # ---- molde de prensagem
    fem = base_femea(p, flor)
    mac = base_macho(p, flor)
    pren = exporta(os.path.join(args.saida, "prensagem"), {
        "base_femea": fem,
        "base_macho": mac,
        "anel_metade": anel_metade(p),
        **({"anel_metade_logo": com_logo(p, anel_metade(p), p.raio_anel, 90.0,
                                         (p.altura_plug_femea + p.profundidade - p.espessura_argila + 3 + p.altura_anel) / 2,
                                         p.logo_largura_prensagem)} if p.logo else {}),
        "presilha": presilha(p),
    })
    zmax_macho = p.profundidade - p.espessura_argila
    for nome, base, plug in (("fêmea", fem, p.altura_plug_femea), ("macho", mac, zmax_macho + 3)):
        mostra_gesso(nome, volume_gesso_ml(p, base, plug))

    if args.preview:
        pasta = os.path.join(os.path.dirname(args.saida), "imagens")
        os.makedirs(pasta, exist_ok=True)
        corte_barbotina(p, para_trimesh(matriz_barbotina(p, flor, canal=False)), os.path.join(pasta, "corte_barbotina.png"))
        corte_prensagem(p, pren, os.path.join(pasta, "corte_prensagem.png"))
        print("\nimagens/corte_barbotina.png e imagens/corte_prensagem.png gerados")


if __name__ == "__main__":
    main()
