# Command - whatsapp-system

## Objetivo

Criar ou revisar o sistema de WhatsApp de um cliente: prospeccao, SDR, sucesso, follow-up e docs Cowork.

## Passos

1. Rodar ou consultar `00_OS/access-preflight.md`.
2. Ler `12_WHATSAPP_STACK/README.md`.
3. Ler `12_WHATSAPP_STACK/tasks/build-whatsapp-system.md`.
4. Carregar context pack do cliente.
5. Carregar `04_DIRETRIZES/whatsapp-diretrizes.md`.
6. Produzir fluxos por bot.
7. Gerar docs Cowork se solicitado.
8. Rodar `GATE-WHATSAPP`.

## Saida

```yaml
files:
gate_result:
open_gaps:
activation_status: draft | ready_for_review | blocked
next_step:
```

