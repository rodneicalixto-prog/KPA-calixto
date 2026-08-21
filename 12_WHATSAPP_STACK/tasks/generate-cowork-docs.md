# Task: Generate Cowork Docs

```yaml
owner: cowork-automation-architect
model_profile: automation-balanced
objective: Gerar documentos operacionais para rodar os bots de WhatsApp no Cowork.
inputs:
  required:
    - fluxos aprovados
    - estados
    - handoff humano
  optional:
    - schema de ferramenta
    - exemplos de conversa
output_contract:
  - cowork-agent-spec.yaml
  - conversation-map.md
  - variables-and-tags.md
  - handoff-schema.md
  - test-cases.md
acceptance_gate: GATE-WHATSAPP
budget: medio
```

## Checklist

- [ ] Cada estado tem entrada, resposta, proxima transicao e stop condition.
- [ ] Cada variavel tem origem, tipo e uso.
- [ ] Cada tag tem quando aplicar e quando remover.
- [ ] Toda acao externa esta marcada como leitura, escrita ou destrutiva.
- [ ] Handoff humano inclui resumo e prioridade.
- [ ] Nao ha segredo, token ou credencial no documento.

