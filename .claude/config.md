# Config do mentorado

```yaml
business:
  name: "KPA Calixto"
  offer: "Kit Piloto Automatico V30 para operar funis, campanhas, WhatsApp, automacoes e entregas com IA"
  segment: "operacao com IA, marketing, automacoes, funis e atendimento comercial"
  target_audience: "negocios e operadores que precisam transformar briefing, campanha, WhatsApp, trafego e entrega em processos guiados"
  main_channel: "WhatsApp, Instagram, GitHub e projetos com automacao"
  current_bottleneck: "instalar e organizar o kit completo para operar sem depender de anexos grandes e sem perder contexto"
  family: "agencia-servico-digital"
preset_used: "kpa-calixto"
tom_de_voz: "pt-BR direto, operacional, pratico e sem enrolacao"
mcps_ativos: []
mcps_pendentes:
  - "Composio Rube"
  - "WhatsApp MCP"
  - "Filesystem MCP"
  - "Playwright MCP"
recommended_templates:
  - "10_TEMPLATES_OPERACIONAIS/projeto-template/current-context.md"
  - "10_TEMPLATES_OPERACIONAIS/task-template.md"
recommended_whatsapp_flows:
  - "12_WHATSAPP_STACK/templates/conversation-map.md"
  - "12_WHATSAPP_STACK/templates/handoff-schema.md"
recommended_automation: "Criar blueprint de onboarding de cliente novo"
first_task: "Briefing organizado de cliente novo para operacao KPA"
created_at: "2026-08-21"
install_status: "partial"
```

## Arquivos do kit adaptados

- Familia operacional: `exemplos/familias/agencia-servico-digital.md`
- Contexto ativo: `05_WORKSPACE/current-context.md`
- Release publica: `15_PRODUCT_RELEASE/`
- Primeira entrega: `06_OUTPUTS/2026-08-21_primeira-tarefa/briefing-kpa-calixto.md`

## Pendencias de ambiente

- Claude CLI nao foi detectado neste workspace, entao os comandos `claude mcp add` nao foram executados.
- MCPs dependem de login/OAuth ou instalacao local do operador.
