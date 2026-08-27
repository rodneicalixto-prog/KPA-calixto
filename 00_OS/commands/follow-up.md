# Command - follow-up

## Objetivo

Gerar mensagem ou sequencia de follow-up pra um lead ou proposta parada, com motivo contextual — nunca "so passando aqui".

## Passos

1. Identificar o estagio: lead frio, proposta sem resposta, pos-venda.
2. Canal WhatsApp: carregar `04_DIRETRIZES/whatsapp-diretrizes.md` e usar `12_WHATSAPP_STACK/agents/sales-followup-bot.md` como referencia de tom/estrutura. Canal email: usar `04_DIRETRIZES/copy-goat-lite.md`.
3. Escrever mensagem curta com motivo contextual especifico (referenciar a ultima interacao real, nao generico).
4. Se for WhatsApp, rodar `GATE-WHATSAPP` (stop rules, opt-out, sem prova/prazo inventado).
5. Nunca disparar de verdade sem confirmacao humana explicita.

## Saida

```yaml
canal:
mensagem:
gate_result:
```
