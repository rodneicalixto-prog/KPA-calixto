# Config do mentorado

```yaml
business:
  name: "Calixto Soluções"
  offer: "Agência full-service digital (tráfego pago, criativos, copy, WhatsApp/automação para múltiplos clientes)"
  segment: "Agência de marketing digital multi-nicho"
  target_audience: "PMEs locais/regionais com verba de tráfego (ex: provedores de internet, clínicas, consorciadoras) que já vendem mas precisam estruturar aquisição via tráfego pago e WhatsApp"
  main_channel: "todos (WhatsApp, Instagram, indicação)"
  current_bottleneck: "Padronização de processo entre clientes"
  family: "agencia-servico-digital"
preset_used: null
tom_de_voz: "pt-BR coloquial profissional, direto e orientado a resultado"
mcps_ativos: ["filesystem", "rube (pendente autenticação)"]
recommended_templates: ["10_TEMPLATES_OPERACIONAIS/cliente-template", "10_TEMPLATES_OPERACIONAIS/projeto-template", "10_TEMPLATES_OPERACIONAIS/output-template"]
recommended_whatsapp_flows: ["12_WHATSAPP_STACK"]
recommended_automation: "18_AUTOMATION_STACK — padronizar processo de onboarding/entrega entre clientes"
first_task: "Briefing organizado de cliente novo"
created_at: "2026-08-27"
```

## Arquivos do kit adaptados

- Família operacional: `exemplos/familias/agencia-servico-digital.md`
- Preset (se houver): N/A
- Squad inicial: `13_ADAPTIVE_SQUADS/`

## Pendências da instalação

- Meta Ads CLI (`meta-ads`) instalado (Python 3.12.11 + uv + meta-ads-cli 0.2.0), mas falta preencher `META_ACCESS_TOKEN`, `META_ACT_ID`, `META_PIXEL_ID` no `.env` local.
- MCP `rube` registrado (`claude mcp add --transport http rube https://rube.app/mcp`), mas precisa de autenticação OAuth (rodar quando usar pela primeira vez).
- Vault Obsidian preparado (`.obsidian/app.json` + `OBSIDIAN.md`), mas a instalação do app em si é responsabilidade do usuário, feita localmente.
