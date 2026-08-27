# Variables and Tags

> Gerado por `@cowork-automation-architect`. Define a memoria (campos que o bot le/escreve durante a conversa) e as tags (segmentacao/etiquetas) do fluxo de WhatsApp. Nunca inclui segredo, token ou credencial.

```yaml
flow_name: "[A PREENCHER]"
owner_bot: "[A PREENCHER]"
```

## Variaveis de memoria

| Variavel | Tipo | Preenchida por | Obrigatoria | Descricao |
|---|---|---|---|---|
| lead_nome | string | usuario | sim | Nome do lead informado na conversa |
| lead_telefone | string | sistema | sim | Numero de origem da conversa |
| intencao | enum | bot | sim | Classificacao da intencao (ex: interesse, duvida, reclamacao, opt-out) |
| fit | enum | bot | nao | alto \| medio \| baixo \| desconhecido |
| [A PREENCHER] | [A PREENCHER] | [A PREENCHER] | [A PREENCHER] | [A PREENCHER] |

## Tags/segmentos

| Tag | Quando aplicar | Usada por |
|---|---|---|
| lead-quente | Fit alto + intencao de compra explicita | SDR, follow-up |
| lead-frio | Sem resposta apos sequencia de follow-up completa | Reativacao |
| opt-out | Usuario pediu pra parar | Todos os bots — bloqueia novo disparo |
| handoff-humano | Encaminhado pra atendimento humano | CS, SDR |
| [A PREENCHER] | [A PREENCHER] | [A PREENCHER] |

## Regras

- Nenhuma variavel guarda senha, token, dado de pagamento ou documento pessoal completo.
- Toda variavel usada em condicao de transicao (`conversation-map.md`) precisa estar listada aqui.
- Tag nova so entra no fluxo depois de aparecer pelo menos 2 vezes numa conversa real (evita explosão de tags soltas).
- `opt-out` sempre existe e sempre bloqueia qualquer novo disparo automatico pro contato.

## Referencias

- Agente: `12_WHATSAPP_STACK/agents/cowork-automation-architect.md`
- Usado junto com: `conversation-map.md`, `handoff-schema.md`, `test-cases.md`
- Gate: `00_OS/gates.md#gate-whatsapp`
