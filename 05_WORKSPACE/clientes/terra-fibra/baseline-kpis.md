# Baseline de KPIs

> Informar fonte, janela e data de atualização. Não preencher com benchmark inventado.

| KPI | Baseline | Meta | Fonte | Janela | Atualizado em |
|---|---:|---:|---|---|---|
| Investimento | [DADO AUSENTE] | [A PREENCHER] | [A PREENCHER] | [A PREENCHER] | [A PREENCHER] |
| CPA | [DADO AUSENTE] | [A PREENCHER] | [A PREENCHER] | [A PREENCHER] | [A PREENCHER] |
| ROAS | [DADO AUSENTE] | [A PREENCHER] | [A PREENCHER] | [A PREENCHER] | [A PREENCHER] |
| CTR | [DADO AUSENTE] | [A PREENCHER] | [A PREENCHER] | [A PREENCHER] | [A PREENCHER] |

## Observação inicial — captura do operador em 2026-08-26

> Janela exibida: últimos 30 dias, de 27/07/2026 a 25/08/2026. Valores abaixo são leitura visual da interface e ainda precisam ser confirmados por export.

| KPI | Valor observado | Fonte | Status |
|---|---:|---|---|
| Campanhas selecionadas | 1 | captura Meta Ads Manager | preliminar |
| Status | Ativo | captura Meta Ads Manager | preliminar |
| Conversas por mensagem | 4 | captura Meta Ads Manager | preliminar |
| Custo por conversa | R$ 6,48 | captura Meta Ads Manager | preliminar |
| Valor gasto | R$ 25,92 | captura Meta Ads Manager | preliminar |
| Orçamento diário exibido | R$ 21,54 | captura Meta Ads Manager | preliminar |
| Alcance | 219 | captura Meta Ads Manager | preliminar |
| Impressões | 246 | captura Meta Ads Manager | preliminar |
| Frequência | 1,12 | captura Meta Ads Manager | preliminar |
| CPM | R$ 105,37 | captura Meta Ads Manager | preliminar |
| Cliques no link | 7 | captura Meta Ads Manager | preliminar |
| CPC do link | R$ 3,70 | captura Meta Ads Manager | preliminar |
| CTR do link | 2,85% | captura Meta Ads Manager | preliminar |
| Cliques (todos) | 6 | captura Meta Ads Manager | revisar definição no export |
| CPC (todos) | R$ 4,32 | captura Meta Ads Manager | preliminar |
| CTR (todos) | 2,44% | captura Meta Ads Manager | preliminar |

## Identificadores visíveis

- Conjunto de anúncios: `CS | Todas cidades | WhatsApp`.
- Anúncio: `Novo anúncio de Tráfego`.
- Configuração de atribuição exibida: clique de 7 dias; texto complementar aparece truncado e deve ser confirmado no export/configuração.

## Checagem aritmética da captura

- R$ 25,92 / 4 conversas = R$ 6,48 por conversa.
- R$ 25,92 / 7 cliques no link = aproximadamente R$ 3,70 por clique no link.
- 7 / 246 = aproximadamente 2,85% de CTR do link.
- R$ 25,92 / 6 cliques (todos) = R$ 4,32 por clique (todos).
- 6 / 246 = aproximadamente 2,44% de CTR (todos).
- 246 / 219 = aproximadamente 1,12 de frequência.

A interface mostra 7 cliques no link e 6 cliques (todos), combinação contraintuitiva que precisa ser preservada como observação e conferida no CSV, sem correção automática.

Não usar esta observação como baseline aprovado antes de conciliar o CSV para a mesma janela.

## Qualidade comercial pendente

Rodnei informou 6 conversas fora de área, 1 sem resposta, 0 de suporte e 0 encaminhadas para venda/instalação. Qualificadas e `Outro` não tiveram quantidade informada. O subtotal de 7 é maior que os 4 resultados atribuídos pelo Meta na captura, portanto a classificação não pode ser aplicada ao CPA até reconciliar janela e origem.

Rodnei confirmou que a campanha estava rodando havia 3 dias, que as conversas classificadas vieram somente dela e que não havia conversas orgânicas ou de outras campanhas. Ainda faltam as datas exatas e as quantidades de `Qualificadas` e `Outro`. A diferença entre pelo menos 7 conversas no atendimento e 4 atribuídas pelo Meta permanece aberta.

Atualização: foram informadas as datas 24/08/2026 a 25/08/2026 e 0 qualificadas. No campo `Outro`, foram registradas 8 conversas descritas como fora da área de cobertura. Antes de consolidar, é necessário confirmar se essas 8 substituem as 6 anteriormente classificadas como fora de área; a descrição anterior de 3 dias também não coincide com as 2 datas de calendário fornecidas.

Consolidação posterior: a classificação inclui 26/08/2026; as 8 fora da cobertura substituem as 6 anteriores; `Outro` é 0. O atendimento soma 9 conversas: 8 fora da área e 1 sem resposta, com 0 qualificadas e 0 vendas/instalações. A captura do Meta termina em 25/08, portanto gasto/atribuição e classificação comercial ainda têm janelas diferentes.

Reconciliação por dia: 1 conversa em 24/08, 5 em 25/08 e 3 em 26/08. Até 25/08, o WhatsApp soma 6 conversas contra 4 atribuídas pelo Meta. Isso implica cobertura preliminar de atribuição de 66,67%, gap de 33,33% e custo operacional preliminar de R$ 4,32 por conversa recebida, sujeito à confirmação de que as definições dos eventos são equivalentes.
