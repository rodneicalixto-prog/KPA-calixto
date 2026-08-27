# Plano de correção geográfica — Terra Fibra

**Status:** draft, cobertura recebida e campanha pausada; aguardando configuração e revisão no Meta.
**Ação real executada:** pausa manual confirmada por Rodnei às 14:54 de 26/08/2026. Nenhuma alteração geográfica foi executada.

## Evidência que dispara o plano

- 9 conversas recebidas entre 24/08 e 26/08;
- 8 fora da área de cobertura (88,89%);
- 1 sem resposta (11,11%);
- 0 qualificadas;
- 0 vendas ou instalações encaminhadas;
- conjunto observado: `CS | Todas cidades | WhatsApp`.

O nome do conjunto e a qualidade das conversas sustentam a hipótese de segmentação geográfica ampla ou desalinhada com a cobertura real. Isso ainda é uma hipótese operacional; a configuração de localização precisa ser aberta e auditada antes da correção.

## Decisão recomendada

**Pausa temporária aprovada e executada manualmente por Rodnei em 26/08/2026 às 14:54**, para evitar continuar comprando conversas sem possibilidade de instalação.

Se Rodnei decidir manter a campanha ativa durante a auditoria:

1. não aumentar orçamento;
2. acompanhar diariamente cidade/bairro das novas conversas;
3. interromper assim que surgir novo lead fora da área;
4. limitar o período de observação a no máximo 24 horas.

## Cobertura recebida

A operação informou 21 cidades. A lista normalizada e suas limitações estão em `05_WORKSPACE/clientes/terra-fibra/coverage.md`.

- Não foi indicada uma única cidade principal.
- Bairros, CEPs e exclusões internas não foram fornecidos.
- A cobertura é validada automaticamente por geolocalização.
- Estar em uma cidade listada não deve ser interpretado como garantia de cobertura no endereço.

## Alteração proposta no Meta Ads

### Segmentação

1. Duplicar o conjunto atual para preservar rollback e histórico.
2. Nomear a cópia como `CS | Cobertura validada | WhatsApp | v1`.
3. Remover localidades genéricas que não constem na lista oficial.
4. Adicionar inicialmente somente as 21 cidades registradas em `coverage.md`, sem prometer cobertura integral.
5. Adicionar exclusões explícitas para regiões próximas sem cobertura quando a interface permitir.
6. Usar a opção de presença geográfica mais restritiva disponível na conta, evitando pessoas apenas interessadas ou recentemente presentes na região.
7. Revisar se expansão automática, Advantage ou controles equivalentes podem ampliar a entrega além da cobertura escolhida.
8. Salvar como rascunho e revisar estimativa de público antes de publicar.

### Rollback

- conjunto original permanece documentado;
- conjunto corrigido começa como rascunho;
- publicação exige aprovação de Rodnei;
- se a nova segmentação não entregar, revisar cobertura e tamanho do público antes de reativar configuração ampla;
- nunca reabrir `Todas cidades` apenas para recuperar volume sem validar a qualidade.

## Pré-qualificação no anúncio

Texto draft para inserir no criativo ou copy, substituindo os marcadores:

> Internet fibra de 500 Mega em regiões selecionadas das cidades atendidas pela Terra Fibra. Consulte a disponibilidade para seu endereço pelo WhatsApp.

CTA draft:

> Consultar cobertura no WhatsApp

Não afirmar cobertura total da cidade; a disponibilidade final depende da geolocalização do endereço.

## Primeira mensagem no WhatsApp

```text
Olá! Pra eu confirmar se a Terra Fibra atende seu endereço, me envie:

1. Cidade
2. Bairro
3. CEP

Não precisa enviar número da casa neste primeiro contato.
```

### Resposta quando há cobertura

```text
Ótimo, atendemos essa região. Vou continuar seu atendimento e confirmar os detalhes da instalação.
```

### Resposta quando não há cobertura

```text
Obrigado pelas informações. No momento, a Terra Fibra ainda não atende essa região. Posso registrar apenas sua cidade e bairro para avisarmos se a cobertura chegar?
```

O registro para aviso futuro deve ocorrer somente com consentimento e política de retenção definida.

## Medição após a correção

Rodar um teste controlado sem aumento de orçamento e classificar cada conversa:

| Métrica | Critério inicial |
|---|---|
| Conversas com localização informada | 100% das novas conversas |
| Fora da área | tendência de queda imediata; qualquer ocorrência deve ser investigada |
| Qualificadas | deve sair de 0 antes de considerar escala |
| Custo por qualificada | calcular somente após existir qualificada |
| Instalações | confirmar no atendimento, não apenas no Meta |

## Gate de publicação

- [x] lista de 21 cidades recebida do operador;
- [ ] segmentação e exclusões revisadas;
- [x] copy sem marcadores aprovada por Rodnei;
- [x] fluxo de WhatsApp aprovado por Rodnei;
- [ ] conjunto corrigido salvo como rascunho;
- [x] rollback documentado;
- [x] pausa temporária aprovada por Rodnei;
- [x] pausa confirmada no Meta Ads Manager às 14:54 de 26/08/2026;
- [ ] tracking e janela de leitura definidos.
