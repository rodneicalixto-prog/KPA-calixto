# Task: Build WhatsApp System

```yaml
owner: whatsapp-orchestrator
model_profile: conversation-balanced
objective: Criar sistema de WhatsApp por funcao, com fluxos e documentos para runtime.
inputs:
  required:
    - cliente ou projeto
    - oferta
    - publico
    - objetivo do WhatsApp
  optional:
    - VOC
    - provas
    - historico de conversas
    - ferramenta de runtime
output_contract:
  - whatsapp-context.md
  - conversation-map.md
  - fluxos por bot
  - cowork-agent-spec.yaml
  - qa-whatsapp.md
acceptance_gate: GATE-WHATSAPP
budget: medio-alto
```

## Pipeline

1. Criar ou atualizar `whatsapp-context.md`.
2. Definir papeis: prospeccao, SDR, sucesso, follow-up.
3. Mapear estados e transicoes.
4. Produzir mensagens por estado.
5. Definir tags, variaveis e criterios de handoff.
6. Gerar docs Cowork.
7. Rodar `conversation-qa`.

## Regras

- Se faltar contexto, marcar `[A PREENCHER]`.
- Se houver uso real de disparo, credencial ou integracao, bloquear ate confirmacao.
- Se LP/oferta prometem algo que o fluxo nao sustenta, abrir task de hardening.

