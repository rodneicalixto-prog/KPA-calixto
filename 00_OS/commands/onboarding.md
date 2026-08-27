# Command - onboarding

## Objetivo

Onboardar um cliente novo depois do fechamento (kickoff): criar workspace, squad inicial e primeira task.

## Passos

1. Confirmar que o briefing existe (`/briefing` se ainda nao rodou).
2. Criar o workspace do cliente em `05_WORKSPACE/clientes/<cliente>/` a partir de `10_TEMPLATES_OPERACIONAIS/cliente-template/`.
3. Definir o squad inicial usando `13_ADAPTIVE_SQUADS/squad-manifest-template.yaml`.
4. Se o cliente roda trafego pago: inicializar com `11_TRAFFIC_STACK/tools/init_traffic_client.py` (nunca com credencial no comando).
5. Se o cliente usa WhatsApp: mapear em `12_WHATSAPP_STACK/templates/whatsapp-context.md`.
6. Registrar a primeira task em `07_LOGS/task-ledger.md`.

## Saida

```yaml
workspace_path:
squad_manifest:
primeira_task:
```
