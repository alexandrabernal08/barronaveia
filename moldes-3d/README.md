# Moldes 3D para gesso: prato flor

Matrizes impressas em 3D para fazer moldes de gesso de um prato em forma de flor. São dois tipos de molde, os dois gerados a partir do mesmo prato:

| | **Molde de colagem (barbotina)** | **Molde de prensagem (placa)** |
|---|---|---|
| Como se usa | despeja-se barbotina, espera formar a parede e escorre-se o excesso | aperta-se uma placa de argila entre duas peças |
| Peças de gesso | 1 | 2 (fêmea + macho) |
| Pasta | `stl/barbotina/` | `stl/prensagem/` |

---

# Molde de colagem (barbotina)

![Molde de colagem](imagens/barbotina.png)

## Peças (pasta `stl/barbotina/`)

| Arquivo | Imprimir | O que é | Tamanho (mm) |
|---|---|---|---|
| `matriz_barbotina.stl` | 1x | O **prato de cabeça para baixo**. Em cima fica o corpo do prato; embaixo, o **reservatório** de 20 mm com o **degrau de corte** de 2 mm na altura da borda. | 163 × 160 × 46 |
| `anel_quarto.stl` | **4x** | 1/4 da parede de contenção (Ø interno 240 mm, 80 mm de altura). | 134 × 134 × 80 |
| `presilha.stl` | **8x** | Presilha em "C". Vão 2 por emenda, uma embaixo e uma em cima. | 14 × 13 × 20 |
| `pino_desmolde.stl` | 1x (faça 2, por garantia) | **Pino de desmoldagem.** Tampa o canal de ar enquanto o gesso está líquido. | Ø 18 × 36 |

Todas as peças cabem numa mesa de impressão de 220 × 220 mm.

| Matriz (lado do prato) | Matriz por baixo: bolso, canal e pino |
|---|---|
| ![Matriz](imagens/matriz_barbotina.png) | ![Pino](imagens/matriz_pino.png) |

### O pino de desmoldagem

O plástico liso da matriz gruda no gesso por **efeito ventosa**: na hora de tirar a matriz, forma-se vácuo entre os dois e ela não sai. Puxar com força pode lascar o molde.

Por isso a matriz tem um **canal de ar** de Ø 4 mm no centro. Ele vai do fundo do prato até um **bolso** na face de baixo.

- **Enquanto o gesso está líquido**, o pino fica encaixado no canal, com a ponta rente à superfície, para o gesso não entrar no furo.
- **Depois que o gesso endurece**, o bloco é virado, o pino sai e injeta-se **ar ou água com uma seringa** pelo canal. A pressão entra entre a matriz e o gesso, quebra o vácuo e empurra a matriz para fora.

### Em corte: fazendo o molde e o molde pronto

![Corte do molde de colagem](imagens/corte_barbotina.png)

O molde é **um bloco de gesso só**, com a "boca" para cima.

- **Reservatório:** a barbotina fica nele acima da borda do prato. Assim o nível não baixa da borda enquanto o gesso absorve a água.
- **Degrau de corte:** marca exatamente onde aparar. Tudo o que colar acima dele é sobra.
- **Espessura do gesso:** ~35 mm nas laterais e embaixo, o que dá absorção suficiente para várias colagens seguidas.

## 1. Impressão da matriz

- PLA ou PETG, com camada de **0,12 mm**. A matriz sai na posição certa: o lado mais largo (o reservatório) fica na mesa, sem suportes.
- **Acabamento é essencial.** Na colagem, a barbotina copia até as linhas de camada.
  1. Lixe com grão 220 → 400 → 600, com água.
  2. Passe primer.
  3. Lixe de novo.
  4. Passe 2 demãos de verniz ou resina de acabamento (tipo XTC-3D).
- O anel e as presilhas podem ser impressos com 0,2–0,28 mm.
- **Pino:** imprima **em pé**, com a cabeça na mesa e 100% de preenchimento.
- **Canal:** depois de impresso, passe uma **broca de 4 mm** à mão pelo canal, de baixo para cima. Furos impressos costumam sair um pouco menores, e a broca deixa o encaixe certo.
- **Teste o pino.** Ele deve entrar justo e com a ponta rente ao fundo do prato. Se sobrar mais de 0,5 mm para fora, lixe a ponta. Se ficar para dentro, imprima outro com `--saliencia-pino` maior. Um pino curto demais deixa o gesso entrar e entupir o canal.

## 2. Montagem para despejar o gesso

1. Use uma **superfície lisa e plana**, como vidro, fórmica ou acrílico, de pelo menos 30 × 30 cm.
2. Passe um pouco de vaselina no pino e **encaixe-o no canal**, por baixo, até a cabeça encostar no fundo do bolso.
3. Apoie a matriz com o **lado largo (reservatório) para baixo**, no centro. O pino fica escondido dentro do bolso, sem encostar na mesa.
4. Vede a junção da matriz com a mesa com um cordão fino de argila ou massinha, para o gesso não entrar por baixo. Alise o cordão rente para não criar um degrau.
5. Monte os 4 quartos do anel em volta e prenda com **2 presilhas por emenda**.
6. **Centralize:** a distância do anel até a ponta de cada pétala deve ser parecida (~36 mm).
7. Vede por fora, com argila, as emendas do anel e a junção do anel com a mesa.
8. Passe **desmoldante** na matriz, no anel e na mesa. Pode ser vaselina líquida diluída, sabão de potássio ou desmoldante próprio para gesso. Tire o excesso com pincel.

## 3. Despejando o gesso

Use **gesso cerâmico** na consistência **70**: 70 partes de água para 100 de gesso, em peso.

| Mistura | Gesso | Água |
|---|---|---|
| ~2,9 L | **~2,9 kg** | **~2,05 L** |

Essa quantidade enche o anel até a borda e já inclui 10% de sobra.

1. Coloque a água no balde e polvilhe o gesso por cima, sem mexer. Deixe hidratar por 1–2 minutos.
2. Misture por 2–3 minutos, sem fazer bolhas, até ficar como um creme de leite grosso.
3. Despeje **pela lateral**, num fio contínuo, até a borda do anel. Isso deixa ~34 mm de gesso por cima da matriz.
4. Dê batidinhas na mesa por 1 minuto para subir as bolhas.
5. Espere o gesso esquentar e esfriar (30–60 min).
6. Tire as presilhas e o anel e **vire o bloco**, com a matriz ainda dentro. O lado que estava na mesa é a boca do molde, e o bolso com o pino fica para cima.
7. **Desmolde com o pino:**
   1. Puxe o pino. Se ele estiver preso, use um alicate.
   2. Encaixe o bico de uma seringa de 20–60 ml no canal e injete ar ou água devagar.
   3. A matriz se solta, e às vezes até "pula". Levante-a.
   4. Se ainda resistir, repita com água: ela não comprime e empurra mais forte.
8. Chanfre as quinas externas do bloco e a borda da boca.
9. **Secagem:** deixe secar por **7 dias** em local ventilado antes da primeira colagem. Se for usar estufa, não passe de 50 °C.

## 4. Colando o prato

1. Use **barbotina de colagem** (defloculada), com densidade de **1,75–1,80 g/ml**. Peneire e mexa bem antes de usar.
2. Com o molde **seco**, despeje a barbotina num fio contínuo até **encher o reservatório**.
3. Enquanto o gesso absorve, o nível baixa. **Complete** para manter o reservatório sempre cheio.
4. Espere a parede formar, normalmente entre **10 e 25 minutos** para 4–5 mm. Para conferir, raspe com a unha a barbotina na parede do reservatório e veja a espessura.
5. **Escorra:** vire o molde de boca para baixo sobre um balde e deixe pingar por 10–15 minutos, apoiado em duas ripas.
6. Desvire o molde. Quando o brilho sumir e a peça começar a descolar do reservatório (30–60 min), **corte com um estilete seguindo o degrau** e retire o anel de sobra.
7. Espere a peça se soltar sozinha (ela retrai e "descola"). Vire o molde sobre uma espuma ou tábua para desenformar.
8. Acabamento: passe uma esponja úmida na borda cortada.
9. Entre uma colagem e outra, deixe o molde secar. Um molde rende umas 2–3 colagens por dia.

> O lado de **fora** do prato (o fundo, com o anel do pé) copia o molde. O lado de **dentro** fica liso, formado pela própria barbotina.

O prato sai cru com **Ø 160 mm**. Com a retração da barbotina (12–15%), deve ficar com uns 14 cm depois da queima.

---

# Molde de prensagem (placa de argila)

![Peças](imagens/pecas.png)

## Peças (pasta `stl/prensagem/`)

| Arquivo | Imprimir | O que é | Tamanho (mm) |
|---|---|---|---|
| `base_femea.stl` | 1x | Base com o **positivo** do prato em relevo e 3 bolinhas de registro. Gera o molde **fêmea** (côncavo). | 214 × 214 × 33 |
| `base_macho.stl` | 1x | Base com o **rebaixo** do prato (já descontados 6 mm de argila) e 3 covinhas de registro. Gera o molde **macho** (convexo). | 214 × 214 × 25 |
| `anel_metade.stl` | **2x** | Metade da parede da caixa (Ø interno 200 mm, 65 mm de altura). Serve para as duas bases. | 228 × 104 × 65 |
| `presilha.stl` | **4x** | Presilha em "C" que trava as abas do anel. | 14 × 13 × 20 |

| Base fêmea | Base macho |
|---|---|
| ![fêmea](imagens/base_femea.png) | ![macho](imagens/base_macho.png) |

![Corte do molde de prensagem](imagens/corte_prensagem.png)

A fêmea fica embaixo e o macho desce dentro dela. Entre os dois sobra um vão de **6 mm**, que é a espessura do prato. As chaves de registro só deixam encaixar numa posição.

## Passo a passo

1. **Impressão:** use as mesmas regras da matriz de colagem. As bases saem deitadas e o anel em pé. A metade do anel tem 228 mm, então numa mesa de 220 × 220 mm imprima na diagonal.
2. **Montagem:** encaixe as duas metades do anel no degrau da base e prenda com 2 presilhas por emenda. Vede as emendas com argila e passe desmoldante.
3. **Gesso:** use consistência 70. Para cada molde, encha até a borda do anel com ~1,6 kg de gesso e ~1,1 L de água.
4. **Molde fêmea:** despeje sobre `base_femea`.
5. **Molde macho:** despeje sobre `base_macho`, usando o mesmo anel.
6. **Secagem:** deixe os moldes secarem por 5–7 dias.
7. **Uso:**
   1. Abra uma placa de argila de 7–8 mm.
   2. Assente a placa na fêmea, com a cavidade para cima.
   3. Encaixe o macho com as bolinhas nas covinhas e pressione.
   4. Corte o excesso de argila rente à borda.
   5. Desenforme quando a peça chegar ao ponto de couro.

---

# Mudando tamanho e formato

Todos os arquivos, dos dois moldes, saem do script `gerar_moldes.py`:

```bash
pip install numpy shapely trimesh manifold3d matplotlib scipy networkx
python3 gerar_moldes.py --preview          # gera stl/ e os desenhos em corte em imagens/
python3 gerar_moldes.py --help             # lista todos os parâmetros
```

Exemplos:

```bash
# Flor de 6 pétalas e mais funda
python3 gerar_moldes.py --petalas 6 --profundidade 30

# Prato menor, com contenção menor também
python3 gerar_moldes.py --raio-petala 65 --raio-vale 55 --largura-aba 18 \
    --raio-anel 85 --raio-anel-barbotina 105

# Reservatório mais alto, para peças com parede mais grossa
python3 gerar_moldes.py --altura-reservatorio 30 --altura-anel-barbotina 90

# Sem o anel em relevo que marca o pé
python3 gerar_moldes.py --marca-pe nao

# Presilhas mais frouxas (aumente) ou mais justas (diminua)
python3 gerar_moldes.py --folga-presilha 0.4
```

| Parâmetro | Padrão | Para que serve |
|---|---|---|
| `--petalas` | 5 | número de pétalas |
| `--raio-petala` / `--raio-vale` | 80 / 68 | raio na ponta e no encontro das pétalas |
| `--profundidade` | 25 | profundidade do prato |
| `--largura-aba` | 22 | largura da borda inclinada até o fundo plano |
| `--marca-pe` | sim | anel em relevo marcando o pé no fundo |
| **Colagem** | | |
| `--altura-reservatorio` | 20 | altura da sobra acima da borda |
| `--degrau-corte` | 2 | largura do degrau que marca o corte |
| `--saida-reservatorio` | 5° | inclinação da parede do reservatório (ajuda a desmoldar) |
| `--raio-anel-barbotina` | 120 | raio interno da contenção. O script avisa se sobrar menos de 30 mm de gesso ao lado das pétalas. |
| `--altura-anel-barbotina` | 80 | altura da contenção, que é a altura do bloco de gesso |
| `--segmentos-anel-barbotina` | 4 | em quantas partes imprimir o anel |
| `--canal-desmolde` | sim | canal de ar + pino de desmoldagem (`nao` para tirar) |
| `--diametro-canal` / `--diametro-pino` | 4,2 / 3,9 | furo do canal e haste do pino |
| `--saliencia-pino` | 0,2 | quanto a ponta do pino passa da superfície do prato |
| **Prensagem** | | |
| `--espessura-argila` | 6 | vão entre macho e fêmea |
| `--raio-anel` | 100 | raio interno da caixa de prensagem |
| `--altura-anel` | 65 | altura da caixa |
| `--folga` | 0,25 | folga entre o anel e a base |
| `--folga-presilha` | 0,3 | folga das presilhas nas abas do anel |

O script confere se todas as peças saem fechadas (*watertight*) e informa as medidas de cada uma e a quantidade de gesso para cada molde.
