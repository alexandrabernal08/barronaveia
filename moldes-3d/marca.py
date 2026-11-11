#!/usr/bin/env python3
"""
Marca "Escola de Cerâmica BARRO NA VEIA" gravada no gesso.

O logo vai em RELEVO na parede de dentro de um segmento do anel de contenção.
O gesso copia esse relevo, e o logo fica GRAVADO (baixo-relevo) na parede
externa do molde. Gravado é mais resistente que letra saltada: não lasca.

Ordem de preferência da fonte do logo:
  1. marca/logo.png (ou o arquivo passado em --logo-arquivo): o logo original,
     vetorizado automaticamente (tudo que não é branco vira relevo);
  2. sem o arquivo: o logo é montado com a fonte Barrio (a mesma do logo),
     no mesmo layout: "ESCOLA DE CERÂMICA" / "BARRO" / "NA VEIA".

Detalhes que este módulo resolve:
  * o logo é aplicado lido de FORA do anel, então no gesso ele fica legível;
  * em molde que é VIRADO para usar (boca para cima), o logo é girado 180°
    para ficar de pé com o molde em uso;
  * o relevo é curvado acompanhando a parede cilíndrica.
"""

from __future__ import annotations

import math
import os

import numpy as np
from manifold3d import CrossSection, FillRule, Manifold
from shapely.affinity import scale as sh_scale, translate as sh_translate
from shapely.geometry import MultiPolygon, Polygon
from shapely.ops import unary_union

PASTA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "marca")
FONTE = os.path.join(PASTA, "Barrio-Regular.ttf")
LOGO_PADRAO = os.path.join(PASTA, "logo.png")

# Layout do logo original (proporções medidas na arte): altura de cada linha
LINHAS = [("ESCOLA DE CERÂMICA", 0.105), ("BARRO", 0.40), ("NA VEIA", 0.385)]
ESPACO_LINHAS = 0.035


def _xor_aneis(aneis: list[np.ndarray]) -> MultiPolygon:
    """Monta polígonos com furos pela regra par-ímpar (contornos de fonte/imagem)."""
    geo = Polygon()
    for a in sorted(aneis, key=lambda r: -abs(Polygon(r).area)):
        if len(a) >= 3:
            geo = geo.symmetric_difference(Polygon(a).buffer(0))
    return geo


def _linha_texto(texto: str, aperto: float = 0.06) -> MultiPolygon:
    """Uma linha de texto na fonte Barrio, com as letras mais juntas (como no logo)."""
    from matplotlib.font_manager import FontProperties
    from matplotlib.textpath import TextPath

    fp = FontProperties(fname=FONTE)
    x, partes = 0.0, []
    for ch in texto:
        if ch == " ":
            x += 18
            continue
        tp = TextPath((0, 0), ch, size=100, prop=fp)
        aneis = [np.asarray(p) for p in tp.to_polygons()]
        g = _xor_aneis(aneis)
        if g.is_empty:
            continue
        minx, _, maxx, _ = g.bounds
        partes.append(sh_translate(g, x - minx, 0))
        x += (maxx - minx) + 100 * aperto
    return unary_union(partes)


def _encaixa(g, x0, y0, w, h):
    minx, miny, maxx, maxy = g.bounds
    g = sh_translate(g, -minx, -miny)
    g = sh_scale(g, w / (maxx - minx), h / (maxy - miny), origin=(0, 0))
    return sh_translate(g, x0, y0)


def logo_fonte() -> MultiPolygon:
    """Logo montado com a fonte Barrio, largura 1, linhas esticadas na largura toda."""
    total = sum(h for _, h in LINHAS) + ESPACO_LINHAS * (len(LINHAS) - 1)
    y, partes = total, []
    for texto, h in LINHAS:
        y -= h
        partes.append(_encaixa(_linha_texto(texto), 0, y, 1.0, h))
        y -= ESPACO_LINHAS
    return unary_union(partes)


def logo_imagem(caminho: str, limiar: int = 200) -> MultiPolygon:
    """Vetoriza um PNG/JPG: tudo que não for (quase) branco vira relevo."""
    import contourpy
    from PIL import Image

    img = Image.open(caminho).convert("RGBA")
    fundo = Image.new("RGBA", img.size, (255, 255, 255, 255))
    img = Image.alpha_composite(fundo, img).convert("L")
    a = np.asarray(img, dtype=float)
    mask = (a < limiar).astype(float)
    mask = np.pad(mask, 2)[::-1]                     # y para cima
    gen = contourpy.contour_generator(z=mask, name="serial")
    aneis = [np.asarray(l) for l in gen.lines(0.5) if len(l) > 8]
    g = _xor_aneis(aneis).simplify(0.6)
    g = g.buffer(0)
    minx, miny, maxx, maxy = g.bounds
    return _encaixa(g, 0, 0, 1.0, (maxy - miny) / (maxx - minx))


def carrega_logo(arquivo: str | None = None) -> tuple[MultiPolygon, str]:
    arq = arquivo or (LOGO_PADRAO if os.path.exists(LOGO_PADRAO) else None)
    if arq:
        return logo_imagem(arq), f"imagem {os.path.basename(arq)}"
    return logo_fonte(), "fonte Barrio"


def proporcao(g) -> float:
    minx, miny, maxx, maxy = g.bounds
    return (maxy - miny) / (maxx - minx)


def _cross_section(g, traco_min: float) -> CrossSection:
    if traco_min > 0:                                 # engrossa traços muito finos
        g = g.buffer(traco_min / 2, join_style=1).buffer(-traco_min / 2 + traco_min * 0.15, join_style=1)
    polys = list(getattr(g, "geoms", [g]))
    aneis = []
    for p in polys:
        if p.area < 0.05:
            continue
        aneis.append(np.asarray(p.exterior.coords)[:-1])
        aneis += [np.asarray(i.coords)[:-1] for i in p.interiors]
    return CrossSection(aneis, FillRule.EvenOdd)


def relevo_no_anel(raio: float, angulo_centro: float, z_centro: float, largura: float,
                   profundidade: float = 1.2, virado: bool = True,
                   arquivo: str | None = None) -> tuple[Manifold, float, str]:
    """Relevo do logo para unir à parede INTERNA de um anel de raio `raio`.

    angulo_centro em graus; z_centro = altura do centro do logo na peça do anel.
    virado=True quando o molde é usado de cabeça para baixo em relação a como
    foi feito (copo e prato de barbotina): o logo gira 180° para ficar de pé.
    Devolve (sólido, altura do logo em mm, origem do logo)."""
    g, origem = carrega_logo(arquivo)
    altura = largura * proporcao(g)
    g = _encaixa(g, -largura / 2, -altura / 2, largura, altura)
    if virado:
        g = sh_scale(g, -1, -1, origin=(0, 0))
    g = g.buffer(0.35, join_style=1).buffer(-0.35, join_style=1)   # traço mínimo para o gesso
    base = g.buffer(0.6, join_style=1).buffer(-0.6, join_style=1)   # suaviza cantos
    d = profundidade
    # relevo em degraus com laterais inclinadas (~30°): o anel solta do gesso
    # sem arrancar as bordas das letras, mesmo sendo puxado um pouco de lado
    passos = 4
    m = Manifold()
    for k in range(passos):
        alto = d * (k + 1) / passos                   # altura deste degrau (a partir da ponta)
        folga = 0.6 * k / (passos - 1)                # mais largo perto da parede
        cs = _cross_section(base.buffer(folga, join_style=1), traco_min=0)
        espessura = d - alto + d / passos + 0.6       # vai da ponta do degrau até dentro da parede
        m = m + cs.extrude(espessura).translate((0, 0, alto - d / passos))
    m = m.refine_to_length(2.0)
    a0 = math.radians(angulo_centro)

    def dobra(v: np.ndarray) -> np.ndarray:
        x, y, z = v[:, 0], v[:, 1], v[:, 2]
        r = raio - d + z                              # z=0 é a ponta do relevo; z>d fica dentro da parede
        ang = a0 + x / raio                           # visto de FORA, x cresce da esquerda para a direita
        return np.c_[r * np.cos(ang), r * np.sin(ang), z_centro + y]

    return m.warp_batch(dobra), altura, origem
