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
mcps_ativos: ["filesystem", "Composio (via connector nativo do claude.ai — rube.app foi descontinuado)"]
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

- `.env` local recriado em 2026-08-31 (não existia neste container — provavelmente perdido entre sessões, já que está no `.gitignore` por segurança). `OPERATOR_NAME` e `OPERATOR_BRAND` preenchidos automaticamente (dados não sensíveis).
- Meta Ads CLI (`meta-ads`) instalado (Python 3.12.11 + uv + meta-ads-cli 0.2.0), mas falta preencher `META_ACCESS_TOKEN`, `META_ACT_ID`, `META_PIXEL_ID` no `.env` local — isso é feito pelo próprio usuário via `/meta-cli-install` (fluxo OAuth), nunca colado no chat.
- `rube.app` foi descontinuado pela Composio (confirmado em 2026-08-27, `rube.app` sem DNS + redirect da própria Composio pra `composio.dev` com UTM de shutdown). O caminho atual é ativar o connector nativo **Composio** em claude.ai/Claude Desktop → Settings → Connectors (sem comando de terminal). Ver `20_MCP_SETUP/connectors/composio-rube.md`.
- **Correção 2026-08-31:** o usuário já tem um vault Obsidian real e em uso
  na própria máquina (`obsidian-template`, com `02_Projects`, `06_Decisions`,
  `07_Executions`, `08_Lessons`, `99_Inbox`, `Agentes/`, etc.) — **não é** o
  repositório `KPA-calixto`. `OBSIDIAN.md` foi corrigido pra deixar isso
  claro. `KPA_OBSIDIAN_VAULT` no `.env` está vazio de propósito: falta o
  usuário informar o caminho local exato do vault real pra qualquer
  leitura/escrita de memória de longo prazo funcionar (`scripts/obsidian_memory_adapter.py`).
