# Configurações do Creality Print para os moldes (Ender 3 V3 KE + PLA)

Dois arquivos de configuração para importar no Creality Print (versões 5 e 6):

| Arquivo | O que configura |
|---|---|
| `processo_molde_ender3v3ke.json` | camada 0,2 mm (primeira 0,25 mm), 3 paredes, 15% de preenchimento, **velocidade 80–100 mm/s**, **aceleração 2000–2500 mm/s²**, primeira camada a 20 mm/s, **brim de 8 mm**, sem suporte |
| `filamento_pla_molde_ender3v3ke.json` | PLA, bico 210 °C (primeira camada 215 °C), **mesa 65 °C**, ventoinha desligada nas 3 primeiras camadas |

## Como importar

1. Abra o Creality Print com a **Ender-3 V3 KE** selecionada como impressora.
2. Menu **Arquivo → Importar → Importar configurações** (*File → Import → Import Configs*).
3. Escolha os dois arquivos `.json` desta pasta.
4. No painel da direita, selecione:
   - **Filamento:** "Barro na Veia - PLA molde (Ender 3 V3 KE)"
   - **Processo:** "Barro na Veia - Molde (Ender 3 V3 KE)"
5. Abra o STL, fatie e confira os valores na tabela acima antes de imprimir.

Se a importação der erro (o formato muda um pouco entre versões), faça os ajustes à mão, logo abaixo.

## Ajuste à mão (2 minutos)

**Processo** (painel da direita, abas do processo):

| Onde | Ajuste | Valor |
|---|---|---|
| Qualidade | Altura da camada inicial | 0,25 mm |
| Velocidade | Camada inicial | 20 mm/s |
| Velocidade | Parede externa / interna / preenchimento | 80 / 100 / 100 mm/s |
| Velocidade → Aceleração | Normal / parede externa | 2500 / 2000 mm/s² |
| Outros → Adesão à mesa | Tipo de borda (brim) / largura | Somente externa / 8 mm |

**Filamento** (lápis ao lado do filamento):

| Ajuste | Valor |
|---|---|
| Bico (camada inicial / demais) | 215 / 210 °C |
| Mesa (camada inicial / demais) | 65 / 65 °C |
| Ventoinha: desligar nas primeiras camadas | 3 |

## Antes de imprimir

1. Lave a chapa PEI com detergente e passe álcool isopropílico.
2. Rode o nivelamento automático da impressora.
3. Ajuste o Z-offset até a primeira camada sair achatada como uma fita.
