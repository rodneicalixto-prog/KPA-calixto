# Diagnóstico preliminar — Terra Fibra — Meta Ads

**Fonte:** capturas do Meta Ads Manager fornecidas pelo operador em 26/08/2026.  
**Janela exibida:** 27/07/2026 a 25/08/2026.  
**Status:** preliminar; aguardando CSV para validação das definições e totais.

## Resumo executivo

A campanha está ativa e gerou 4 conversas por mensagem com R$ 25,92 de investimento, resultando em R$ 6,48 por conversa. O volume ainda é pequeno para declarar tendência ou recomendar escala, pausa ou mudança de orçamento. A próxima decisão deve esperar o CSV e a confirmação de que `Conversas por mensagem` representa conversas realmente iniciadas e úteis para o comercial.

## Estrutura observada

| Nível | Nome/status |
|---|---|
| Campanha | `TERRA FIBRA | 500MEGA | TRAFEGO WHATS | ...` — ativa, nome truncado |
| Conjunto | `CS | Todas cidades | WhatsApp` — ativo |
| Anúncio | `Novo anúncio de Tráfego` — ativo |
| Destino | WhatsApp |
| Resultado | Conversas por mensagem |

## Métricas observadas

| Métrica | Valor |
|---|---:|
| Orçamento diário exibido | R$ 21,54 |
| Valor gasto | R$ 25,92 |
| Resultados | 4 conversas por mensagem |
| Custo por resultado | R$ 6,48 |
| Alcance | 219 |
| Impressões | 246 |
| Frequência | 1,12 |
| CPM | R$ 105,37 |
| Cliques no link | 7 |
| CPC do link | R$ 3,70 |
| CTR do link | 2,85% |
| Cliques (todos) | 6 |
| CPC (todos) | R$ 4,32 |
| CTR (todos) | 2,44% |

## Validações aritméticas

- CPA: R$ 25,92 / 4 = R$ 6,48.
- CPC do link: R$ 25,92 / 7 = R$ 3,70, arredondado.
- CTR do link: 7 / 246 = 2,85%, arredondado.
- CPC (todos): R$ 25,92 / 6 = R$ 4,32.
- CTR (todos): 6 / 246 = 2,44%, arredondado.
- Frequência: 246 / 219 = 1,12, arredondado.

## Fatos

- A campanha, o conjunto e o anúncio aparecem ativos.
- O destino observado é WhatsApp.
- O evento de resultado exibido é `Conversas por mensagem`.
- As métricas derivadas conferem aritmeticamente com gasto, impressões, cliques e resultados mostrados.

## Pontos que ainda não permitem conclusão

1. A interface mostra 7 cliques no link e 6 cliques (todos). Como isso é contraintuitivo, as definições e o CSV precisam ser conferidos antes de interpretar taxa de clique.
2. Não há informação sobre quantas das 4 conversas eram qualificadas, quantas receberam resposta e quantas viraram instalação/venda.
3. O nome completo da campanha está truncado.
4. A captura não mostra breakdown por idade, gênero, posicionamento, cidade ou horário.
5. Não há baseline histórico aprovado nem meta comercial de custo por conversa/venda.
6. A classificação enviada posteriormente soma pelo menos 7 conversas (6 fora de área e 1 sem resposta), mas o Meta mostra 4 resultados na janela. Os denominadores ou períodos ainda não estão conciliados.
7. Rodnei confirmou que a campanha estava rodando havia 3 dias e que as conversas vieram somente desta campanha, sem origem orgânica ou outra campanha. Isso reduz uma hipótese de mistura de origem, mas não resolve a diferença de atribuição 7+ versus 4.

## Decisão operacional

**Não alterar orçamento, público, criativo ou status com base somente nessas capturas.** Manter a campanha sob observação enquanto o primeiro export é conciliado e o atendimento das quatro conversas é qualificado.

## Próximas ações

### Agora

1. Exportar CSV da mesma janela com as colunas exibidas.
2. Copiar o nome completo da campanha.
3. Classificar as 4 conversas no WhatsApp como: qualificada, fora de área, sem resposta, problema técnico, venda/instalação ou outro.

Classificação parcial recebida: 6 fora de área, 1 sem resposta, 0 suporte e 0 venda/instalação. Faltam as quantidades de qualificadas e outro. Como o subtotal 7 excede os 4 resultados do Meta, nenhum percentual ou custo por qualidade deve ser calculado até confirmar origem e período.

Confirmação posterior: a campanha estava rodando havia 3 dias; as conversas vieram somente dela; não havia conversas orgânicas ou de outras campanhas. Permanecem pendentes as datas exatas, a quantidade de qualificadas e a quantidade de `Outro`.

Nova atualização: Rodnei informou 24/08/2026 a 25/08/2026, 0 qualificadas e 8 registros em `Outro` descritos como fora da área de cobertura. Os 8 devem ser recategorizados como `Fora de área`, mas ainda falta confirmar se substituem os 6 anteriores ou se são adicionais. As datas fornecidas cobrem 2 datas de calendário, não 3, e também precisam de confirmação.

Consolidação final da classificação: a janela do WhatsApp inclui 26/08/2026; as 8 fora da cobertura substituem as 6 anteriores; `Outro` é 0. O total classificado é 9 conversas, sendo 8 fora da área e 1 sem resposta, sem qualificadas ou vendas. Como o Meta foi capturado com data final 25/08, ainda não é válido dividir o gasto da captura pelas 9 conversas.

Reconciliação diária recebida: 1 conversa em 24/08, 5 em 25/08 e 3 em 26/08. Assim, até o fim de 25/08 havia 6 conversas no WhatsApp contra 4 atribuídas pelo Meta. A cobertura preliminar de atribuição é 66,67%, com gap de 2 conversas (33,33%). Usando somente a janela até 25/08, o custo operacional preliminar é R$ 25,92 / 6 = R$ 4,32 por conversa recebida.

## Recomendação revisada

Com 0 qualificadas e 8 de 9 conversas fora da cobertura, o principal problema observado é geográfico/comercial, não falta de clique. Recomenda-se auditar imediatamente a segmentação de localização e a lista real de cidades atendidas. Considerar pausa temporária até corrigir a cobertura, mas qualquer pausa depende de aprovação explícita de Rodnei.

Plano draft criado em `06_OUTPUTS/terra-fibra/traffic/plano-correcao-geografica-draft.md`. Nenhuma alteração ou pausa foi executada.

### Depois do CSV

1. Conciliar gasto, impressões, cliques e resultados.
2. Calcular custo por conversa qualificada e custo por venda, se houver.
3. Definir baseline inicial e meta econômica com Rodnei.
4. Só então decidir manutenção, teste criativo ou ajuste de segmentação.

## Privacidade

As capturas originais também exibem números de telefone e conversas particulares do WhatsApp. Esses dados não foram copiados para este relatório. Próximas evidências devem conter apenas a área do Meta Ads Manager ou ter dados pessoais ocultados.
