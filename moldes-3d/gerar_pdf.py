#!/usr/bin/env python3
"""Converte um guia .md desta pasta em PDF A4, com as imagens.

    python3 gerar_pdf.py GUIA_COPO.md PROMPT_NOVO_MOLDE.md

Precisa de: pip install markdown  ·  Node.js com o pacote playwright (Chromium).
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
import tempfile

import markdown

CSS = """
body{font-family:'DejaVu Sans',Arial,sans-serif;font-size:10.5pt;color:#2b2622;line-height:1.45}
h1{color:#556B2F;font-size:19pt;margin:0 0 4px}
h2{color:#556B2F;border-bottom:2px solid #c8d5b0;padding-bottom:3px;margin-top:20px;page-break-after:avoid}
h3{color:#6B8E23}
img{max-width:100%;display:block;margin:8px auto;page-break-inside:avoid}
table{border-collapse:collapse;width:100%;margin:8px 0;page-break-inside:avoid}
th,td{border:1px solid #d8d0c4;padding:4px 6px;vertical-align:top} th{background:#eef2e6}
td img{max-height:230px}
code{background:#f3efe8;padding:1px 3px;border-radius:3px;font-size:9pt}
pre{background:#f7f4ee;border:1px solid #e3dccf;border-left:4px solid #6B8E23;padding:10px;border-radius:4px;
    font-size:8.3pt;line-height:1.35;white-space:pre-wrap;word-break:break-word}
pre code{background:none;padding:0;font-size:inherit}
a{color:#556B2F} li{margin:2px 0} hr{border:0;border-top:1px solid #d8d0c4;margin:14px 0}
blockquote{border-left:4px solid #c8d5b0;margin:8px 0;padding:2px 10px;color:#555}
"""

NODE = r"""
const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage();
await p.goto('file://'+process.argv[1]);await p.waitForLoadState('networkidle');
await p.pdf({path:process.argv[2],format:'A4',printBackground:true,
  margin:{top:'14mm',bottom:'14mm',left:'12mm',right:'12mm'}});await b.close();})();
"""


def preparar(md: str) -> str:
    # listas logo depois de uma linha em negrito precisam de linha em branco
    md = re.sub(r"(\*\*[^\n]*:\*\*)\n(- |\d+\. )", r"\1\n\n\2", md)
    # sublistas com 3 espaços -> 4 (padrão do Python-Markdown)
    return re.sub(r"(?m)^   (\d+\.|-) ", r"    \1 ", md)


def gerar(md_path: str) -> str:
    md_path = os.path.abspath(md_path)
    pasta = os.path.dirname(md_path)
    titulo = os.path.splitext(os.path.basename(md_path))[0].replace("_", " ").title()
    corpo = markdown.markdown(preparar(open(md_path, encoding="utf-8").read()),
                              extensions=["tables", "fenced_code", "sane_lists"])
    html = (f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>{titulo}</title>'
            f"<style>{CSS}</style></head><body>{corpo}</body></html>")
    with tempfile.NamedTemporaryFile("w", suffix=".html", dir=pasta, delete=False, encoding="utf-8") as f:
        f.write(html)
        tmp = f.name
    pdf = os.path.splitext(md_path)[0] + ".pdf"
    try:
        subprocess.run(["node", "-e", NODE, tmp, pdf], check=True)
    finally:
        os.remove(tmp)
    return pdf


if __name__ == "__main__":
    for arq in sys.argv[1:] or ["GUIA_COPO.md", "PROMPT_NOVO_MOLDE.md"]:
        print("PDF:", gerar(arq))
