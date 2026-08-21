# Config do mentorado

```yaml
business:
  name: "Calixto Soluções"
  offer: "Agência de marketing digital / estrategista digital"
  segment: "gestor de tráfego, marketing em geral"
  target_audience: "Empresas e microempresários com dificuldade em gerenciar estratégia de mkt digital, captar clientes, construir sites e implementar automações"
  main_channel: "WhatsApp / Instagram / Google / Indicação / Site (todos)"
  current_bottleneck: "Não tenho tempo de criar conteúdo e automações"
  family: "agencia-servico-digital"
preset_used: null
tom_de_voz: "profissional, direto, consultivo (estrategista digital)"
mcps_ativos: ["rube (pendente - não persiste em container remoto)", "whatsapp (pendente)", "filesystem (pendente)", "playwright (pendente)"]
recommended_templates: []
recommended_whatsapp_flows: []
recommended_automation: "Automação de criação de conteúdo e fluxos recorrentes (maior gargalo relatado)"
first_task: "Automação de criação de conteúdo recorrente (draft) - 05_WORKSPACE/clientes/calixto-solucoes/automacoes/automacao-criacao-conteudo.yaml"
created_at: "2026-08-21T16:18:49Z"
```

## Arquivos do kit adaptados

- Familia operacional: `exemplos/familias/agencia-servico-digital.md`
- Preset (se houver): `nichos/<nicho>/`
- Squad inicial: `13_ADAPTIVE_SQUADS/`

## Pendências desta instalação

- `.env`: repositório não tem `.env.example`; criar manualmente na máquina local com as variáveis necessárias.
- MCPs (Rube, WhatsApp, Filesystem, Playwright): instalar na máquina local do operador — ambiente remoto é efêmero, comandos não persistem.
- Meta Ads CLI: requer instalação nativa + login OAuth via browser — rodar `/meta-cli-install` na máquina local.
