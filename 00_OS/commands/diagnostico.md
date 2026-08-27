# Command - diagnostico

## Objetivo

Diagnosticar uma operacao (trafego pago, funil, atendimento, operacao geral) e apontar o proximo passo priorizado.

## Passos

1. Identificar o dominio do diagnostico: trafego pago, funil, WhatsApp/atendimento, ou operacao geral do cliente.
2. Trafego: rodar `11_TRAFFIC_STACK/tasks/diagnosticar-campanha-meta-cli.md` (performance geral) ou `11_TRAFFIC_STACK/tasks/investigar-queda.md` (queda especifica).
3. Operacao geral/ledger: usar `02_AGENTS/skills/kpa-qa-editor/SKILL.md` pra revisar entregas recentes contra o gate, ou o CoS pra revisar `07_LOGS/task-ledger.md` e `05_WORKSPACE/current-context.md`.
4. Sempre citar dado real (CLI, metricas, ledger) — nunca estimativa disfarcada de fato.
5. Entregar no maximo 3 acoes priorizadas, com dono e prazo.

## Saida

```yaml
dominio:
achados:
top_3_acoes:
gate_result:
```
