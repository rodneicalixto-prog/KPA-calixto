# Command - automatizar-processo

## Objetivo

Transformar um processo do cliente em automacao documentada, testavel e segura — sempre em modo `draft` ate confirmacao humana.

## Passos

1. Ler `18_AUTOMATION_STACK/README.md` e `18_AUTOMATION_STACK/tasks/build-process-automation.md`.
2. Preencher `18_AUTOMATION_STACK/templates/process-intake.md` com o processo, trigger, ferramentas, dados e limites do que pode rodar automatico.
3. Gerar blueprint (`18_AUTOMATION_STACK/templates/automation-blueprint.yaml`) e SOP (`18_AUTOMATION_STACK/templates/sop-template.md`).
4. Rodar `GATE-AUTOMATION` — sem handoff humano, teste e rollback, fica `draft`.
5. Nenhum envio, API write, CRM update, budget ou publicacao roda sem confirmacao humana explicita.

## Saida

```yaml
blueprint_path:
sop_path:
gate_result:
activation_status: draft
```
