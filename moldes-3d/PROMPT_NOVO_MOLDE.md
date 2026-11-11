# Prompt para criar um novo molde de gesso

Copie o bloco abaixo, preencha a parte **"A PEÇA"** e cole numa nova conversa com o Claude, de preferência no repositório `barronaveia`. Anexe as fotos de referência junto.

---

```text
Você vai criar um novo MOLDE DE GESSO PARA CERÂMICA a partir de uma matriz
impressa em 3D, seguindo o processo padrão da escola Barro na Veia, que já
está no repositório em moldes-3d/ (leia moldes-3d/README.md,
moldes-3d/gerar_copo.py e moldes-3d/gerar_moldes.py antes de começar e
reaproveite as funções que já existem).

==================== A PEÇA (preencher) ====================
Nome da peça (curto, sem acento, para pastas/arquivos): ____________
Tipo de molde: [ ] barbotina (colagem)  [ ] prensagem (placa)  [ ] não sei, decida
Medidas (cm): altura ___  boca ___  largura máxima ___  (outras: ___)
Essas medidas são da peça: [ ] crua, saindo do molde  [ ] queimada (aplicar retração de ___ %)
Formato / detalhes: (fundo reto ou arredondado, parede reta/aberta/barriguda,
  borda, pé em anel ou disco, altura do pé, alças, relevos, textura...)
Fotos anexadas: (diga o que observar em cada uma)
Impressora: mesa ___ x ___ mm, altura útil ___ mm   (padrão: 220 x 220 x 250)
=============================================================

REGRAS DO PROCESSO (siga todas):

1. ANÁLISE ANTES DE MODELAR
   - Descreva o que entendeu da peça e das fotos (perfil, pé, borda, detalhes).
   - Teste de contrassaída: a peça só sai de um molde de 1 PEÇA se ficar cada
     vez mais estreita da boca para o fundo (boca = parte mais larga) e todas as
     paredes tiverem saída de pelo menos 2–3°. Se não ficar, diga isso
     claramente e proponha as opções: (a) ajustar o formato para 1 peça ou
     (b) molde de 2+ partes com divisão vertical e chaves de registro.
   - Se algo for ambíguo e mudar o resultado (1 ou 2 partes, pé em anel ou em
     disco, medida crua ou queimada, diâmetro do pé...), PERGUNTE antes de
     modelar, com opções claras. Não invente medidas importantes sem avisar.

2. PADRÃO DA MATRIZ (barbotina, 1 peça — modelo "chapéu")
   - Peça de cabeça para baixo sobre uma ABA EM DEGRAUS, que:
     encaixa e centraliza o anel de contenção (plug com folga 0,25 mm),
     forma o RESERVATÓRIO (20–25 mm acima da boca, parede com 5° de saída) e
     forma o DEGRAU DE CORTE (2 mm) exatamente na altura da borda.
   - Matriz OCA (casca de ~3,5 mm), aberta por baixo, com TUBO CENTRAL e
     3 nervuras até o fundo da peça.
   - CANAL + PINO DE DESMOLDAGEM: furo no ponto mais alto da matriz (centro do
     fundo da peça) com Ø 6,2 mm e pino de Ø 6,0 mm. Em matriz maciça, use
     Ø 4,2 mm e pino de Ø 3,9 mm com um bolso por baixo. A ponta do pino passa
     0,2 mm da superfície. Ofereça como alternativa uma cavilha/vareta ou um
     prego do mesmo diâmetro.
   - Gesso: mínimo de 25 mm em volta da parte mais larga e acima do fundo
     (30–40 mm em peças grandes ou que vão ser coladas muitas vezes).

3. PADRÃO DA CONTENÇÃO
   - Anel em N segmentos (padrão 4) com parede de 4 mm, abas de 10 mm nas
     pontas e PRESILHAS em "C" (folga de 0,3 mm), de 2 a 3 por emenda,
     conforme a altura.
   - Molde de 2 partes: bandejas com chaves de registro hemisféricas de
     raio 5 mm (bolinha numa metade, covinha com folga de 0,4 mm na outra),
     moldura em U com presilhas e canal + pino em cada bandeja.
   - Prensagem: base fêmea (positivo) e base macho (rebaixo já descontada a
     espessura da argila, por erosão 3D), mesmo anel e chaves.
   - Todas as peças devem caber na impressora informada. Se não couberem,
     divida em mais segmentos ou avise e sugira o ajuste.

4. CÓDIGO
   - Crie moldes-3d/gerar_<nome>.py PARAMÉTRICO (dataclass de parâmetros +
     argparse automático, como gerar_copo.py), em milímetros, com o parâmetro
     --retracao (%) e --preview.
   - Use manifold3d (revolve/extrude/booleanos), shapely e trimesh. Reaproveite
     de gerar_moldes.py: presilha, anel_segmento, para_trimesh e receita.
   - Exporte os STL para moldes-3d/stl/<nome>/ e confira que TODOS saem
     fechados (watertight). Imprima no terminal as dimensões de cada peça e
     o gesso necessário (consistência 70, +10% de sobra).
   - Inclua asserts para os parâmetros impossíveis (pé maior que o fundo,
     sem saída, sem espaço para as chaves etc.).

5. VERIFICAÇÃO (obrigatória antes de entregar)
   - Desenho EM CORTE (matplotlib) em moldes-3d/imagens/corte_<nome>.png:
     (1) fazendo o molde: mesa, matriz, pino, anel e gesso;
     (2) molde pronto com a parede colada (~4 mm), a sobra do reservatório
     e a linha de corte.
   - Renderizações 3D (three.js + Playwright): todas as peças, a matriz vista
     por baixo e a PEÇA PRONTA (em pé e de cabeça para baixo).
   - Olhe as imagens você mesmo e corrija o que estiver errado: contrassaída,
     saída insuficiente, pé errado, peça que não cabe na impressora, artefato
     visual.
   - Teste pelo menos duas variações de parâmetros (ex.: --retracao 12 e uma
     peça menor).

6. DOCUMENTAÇÃO (em português, para alunas)
   - Nova seção no moldes-3d/README.md e um guia separado
     moldes-3d/GUIA_<NOME>.md + GUIA_<NOME>.pdf (com as imagens), contendo:
     tabela de medidas (deixando claro se é crua ou queimada) · imagem da peça
     pronta · corte · tabela de peças (arquivo, quantas imprimir, o que é,
     tamanho) · links de download · lista de material · impressão (camada,
     orientação, lixar/primer/verniz, broca no canal, pino) · como fazer o
     molde de gesso (pino, montagem, vedação, desmoldante, quantidade de
     gesso, desmolde com seringa, secagem de 7 dias) · como colar ou prensar
     (densidade da barbotina 1,75–1,80, tempo, escorrer, cortar no degrau,
     desenformar) · retração e como gerar outras medidas.

7. ENTREGA
   - Commit e push no branch de trabalho, com mensagem descritiva.
   - Envie na conversa: imagens (peça pronta, corte, peças), os STL e o
     guia em PDF.
   - Resposta final curta: o que foi feito, decisões tomadas, medidas finais,
     quantas peças imprimir, gesso necessário, avisos (impressora, retração)
     e links individuais de cada STL no GitHub.
```

---

## Exemplo preenchido

```text
==================== A PEÇA ====================
Nome da peça: tigela_ondulada
Tipo de molde: barbotina (colagem)
Medidas (cm): altura 7  boca 16  largura máxima 16
Essas medidas são da peça: queimada (aplicar retração de 12 %)
Formato / detalhes: tigela baixa, parede aberta, borda ondulada com 8 ondas,
  pé em anel Ø 8 cm com 0,4 cm de altura.
Fotos anexadas: foto 1 = referência do formato; foto 2 = detalhe do pé.
Impressora: mesa 256 x 256 mm, altura útil 256 mm
================================================
```
