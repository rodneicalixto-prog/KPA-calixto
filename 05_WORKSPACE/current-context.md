# Current Context

```yaml
projeto: "KPA Calixto"
objetivo: "Instalar e deixar operavel o Kit Piloto Automatico V30 para funis, campanhas, WhatsApp, automacoes e entregas com IA"
publico: "negocios e operadores que precisam transformar briefing, campanha, WhatsApp, trafego e entrega em processos guiados"
oferta: "Kit Piloto Automatico V30"
mecanismo: "CoS como entry point, tasks pequenas, gates de qualidade, squads adaptativos e MCPs sob demanda"
tom: "pt-BR direto, operacional, pratico e sem enrolacao"
provas_confirmadas: []
restricoes:
  - "Anti-leak: nada com token sai do .env local"
  - "Voz humana pt-BR obrigatoria em qualquer copy entregue"
  - "Encoding UTF-8 obrigatorio em payloads pt-BR"
  - "Acoes reais em WhatsApp, campanhas, CRM, publicacao ou budget exigem confirmacao humana"
status: "onboarded_partial"
proxima_task: "Configurar MCPs escolhidos ou rodar primeira task operacional"
arquivos_relevantes:
  - ".claude/config.md"
  - "00_OS/commands/instalar-kpa30.md"
  - "15_PRODUCT_RELEASE/README.md"
  - "15_PRODUCT_RELEASE/IMPORT_MANIFEST.md"
  - "20_MCP_SETUP/README.md"
  - "06_OUTPUTS/2026-08-21_primeira-tarefa/briefing-kpa-calixto.md"
squad_manifest: "[A DEFINIR apos escolher cliente piloto]"
whatsapp_status: "sera_mapeado"
preflight_status: "partial"
platform: "claude-code"
install_date: "2026-08-21"
```

Este arquivo deve permanecer curto. Se ficar grande, criar resumo e arquivar detalhes no projeto correspondente.

> **Primeiro uso?** Rode `/instalar-kpa30` pra fazer o setup completo do kit (dependencias, .env, MCPs, onboarding do seu negocio e primeira tarefa).
