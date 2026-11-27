# Guia do copinho barrigudo: molde de gesso de 2 partes para barbotina

*Escola de cerâmica Barro na Veia*

Copinho com **fundo bem redondo**, barriga, pescoço levemente fechado e boca abrindo de leve. A **covinha** de dedo **não está no molde**: ela é feita à mão, apertando com o dedo, depois de desenformar.

## Medidas

O molde é **20% maior** que a peça de referência, para compensar a retração da barbotina na secagem e na queima. Assim a cópia queimada fica do tamanho da original.

| | Peça de referência (queimada) | Peça que sai do molde (crua) |
|---|---|---|
| Altura | 7,0 cm | **8,4 cm** |
| Boca (diâmetro externo) | 6,3 cm | **7,6 cm** |
| Barriga (parte mais larga) | ~7,1 cm | **8,5 cm** |

Medidas tiradas das fotos com régua e do vídeo da peça girando.

![O copinho como sai do molde](imagens/copinho_peca.png)

## Por que 2 partes?

A **barriga é mais larga que a boca**. Num molde inteiriço a peça ficaria presa. Por isso o molde é dividido em **duas metades na vertical**, passando pelo eixo do copinho:
- as metades encaixam por **4 chaves de registro**: bolinhas numa metade, covinhas na outra;
- cada metade sai com o **logo Barro na Veia** gravado na lateral.

Montado, o molde é um bloco de **13,6 × 13,6 × 12,9 cm**.

## Peças (pasta `stl/copinho/`)

![Bandejas A e B e os pinos](imagens/copinho_bandejas.png)

| Arquivo | Imprimir | O que é | Tamanho (mm) |
|---|---|---|---|
| `bandeja_A.stl` | 1x | Meio copinho deitado, com reservatório, 4 **bolinhas** de encaixe e canal de ar. Gera a **metade A**. | 150 × 143 × 50 |
| `bandeja_B.stl` | 1x | Igual, com 4 **covinhas** de encaixe. Gera a **metade B**. | 150 × 143 × 50 |
| `moldura_U.stl` | 1x | Metade da moldura que cerca a bandeja. | 164 × 69 × 72 |
| `moldura_U_logo.stl` | 1x | A outra metade da moldura, com o **logo** em relevo por dentro. | 164 × 69 × 72 |
| `presilha.stl` | 4x | Trava as duas metades da moldura, 2 por emenda. | 14 × 13 × 20 |
| `pino.stl` | 2x | Tampa o canal de ar das bandejas (o mesmo pino serve para as duas). | Ø 16 × 41 |

`peca_copinho_conferencia.stl` é só a peça, para conferir o formato. Não precisa imprimir.

Tudo cabe numa impressora com mesa de 22 × 22 cm, como a Ender 3 V3 KE.

**Impressão:**

- As bandejas vão com a placa na mesa e o meio copinho para cima, sem suportes. Use camada de 0,12–0,16 mm e **lixe bem** o meio copinho: a barbotina copia tudo.
- A moldura vai em pé. Use as configurações do Creality Print da pasta `impressao/creality_print/`.
- Os pinos vão em pé, com a cabeça na mesa e 100% de preenchimento. Passe uma broca de 4 mm nos canais das bandejas.

## Fazendo as duas metades de gesso

Faça uma metade de cada vez: primeiro com a `bandeja_A`, depois com a `bandeja_B`. A moldura é a mesma.

1. **Pino:** encaixe o pino por baixo da bandeja, até a ponta ficar rente à superfície do meio copinho.
2. **Moldura:** encaixe as duas metades da moldura em volta do degrau da placa. Prenda com 2 presilhas em cada emenda.
3. **Vedação:** vede as emendas por fora com argila. Vede também a junção do meio copinho com a parede da moldura, do lado do reservatório.
4. **Desmoldante:** passe em tudo, inclusive dentro das letras do logo.
5. **Gesso:** consistência 70 (70 de água para 100 de gesso). **Por metade:** ~1 kg de gesso e ~0,7 L de água.
    1. Despeje pela lateral até a borda da moldura.
    2. Bata na mesa para subir as bolhas.
    3. Espere esquentar e esfriar (30–60 min).
6. **Desmolde:**
    1. Tire as presilhas e a moldura.
    2. Vire o conjunto e puxe o pino.
    3. Injete ar ou água com a seringa no canal: a bandeja se solta.
7. Chanfre as quinas e deixe as duas metades secarem **7 dias**.

![Metade de gesso com o logo gravado na lateral](imagens/copinho_gesso_logo.png)

## Colando o copinho

1. **Monte o molde:** junte as metades, encaixando as chaves. Prenda com elásticos largos. A boca do reservatório fica para cima.
2. **Encha:** barbotina de colagem (1,75–1,80 g/ml) até o topo do reservatório. Vá completando enquanto o nível baixa.
3. **Espere a parede formar:** 8–15 min para 3–4 mm. Para conferir, raspe com a unha a barbotina na parede do reservatório.
4. **Escorra:** vire de boca para baixo por 10 min.
5. **Corte:** quando o brilho sumir, corte a sobra seguindo o degrau.
6. **Abra:** quando a peça começar a se soltar, tire os elásticos e abra as metades **de lado**.
7. **Covinha:** com a peça ainda macia, logo depois de desenformar, aperte a covinha com o dedo, de fora para dentro, na altura da barriga.
8. **Acabamento:** passe esponja úmida na linha de emenda (dos dois lados e no fundo) e na borda.

## Outros tamanhos

```bash
python3 gerar_copinho.py --aumento 15            # molde 15% maior que a peça medida
python3 gerar_copinho.py --aumento 0             # molde do tamanho exato da peça medida
python3 gerar_copinho.py --covinha sim           # covinha já no molde (metade A)
python3 gerar_copinho.py --help
```
