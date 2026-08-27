# Agentes V30

O V30 reduz o time para poucos papeis fortes. A meta e evitar carregar 30 agentes quando 7 contratos resolvem a operacao.

## Time

| Agente | Funcao |
|---|---|
| CoS | task manager, router e contexto |
| KPA Orchestrator | coordena pipeline completo quando necessario |
| Researcher | VOC, mercado, concorrentes |
| Strategist | oferta, posicionamento, mecanismo |
| Copy Director | copy e adaptacao multicanal |
| Production Lead | pagina, design, criativos, video |
| Traffic Analyst | campanhas, metricas, diagnostico |
| Product Auditor | promessa da LP vs entrega real e robustez do produto |
| Automation Architect | automacoes de processo, SOPs, blueprints e ativacao segura |
| QA Editor | gates, revisao, stress test |

## Skills instaladas

Cada agente do time acima (exceto Automation Architect, ja coberto por
`18_AUTOMATION_STACK/skills/process-automation-design/SKILL.md`) tem uma
Skill ativavel por trigger de frase, validada contra sua task, diretriz,
gate e handoff correspondentes:

| Skill | Agente | Task | Gate |
|---|---|---|---|
| `skills/kpa-cos/SKILL.md` | CoS | T00, T07 | GATE-INTAKE |
| `skills/kpa-orchestrator/SKILL.md` | KPA Orchestrator | pipeline (01_PIPELINE) | GATE-INTAKE..GATE-DELIVERY |
| `skills/kpa-researcher/SKILL.md` | Researcher | T01 | GATE-RESEARCH |
| `skills/kpa-strategist/SKILL.md` | Strategist | T02 | GATE-STRATEGY |
| `skills/kpa-copy-director/SKILL.md` | Copy Director | T03 | GATE-COPY |
| `skills/kpa-production-lead/SKILL.md` | Production Lead | T04 | GATE-PRODUCTION |
| `skills/kpa-traffic-analyst/SKILL.md` | Traffic Analyst | T05, T06 | GATE-TRAFFIC |
| `skills/kpa-product-auditor/SKILL.md` | Product Auditor | T08 | GATE-PRODUCT |
| `skills/kpa-qa-editor/SKILL.md` | QA Editor | gate dinamico | conforme output |
| `skills/kpa-memory-curator/SKILL.md` | KPA Memory Curator | — | GATE-MEMORY |

## Camadas especializadas

| Camada | Quando usar |
|---|---|
| `11_TRAFFIC_STACK/` | operacao de campanhas vivas e diagnostico Meta Ads |
| `12_WHATSAPP_STACK/` | WhatsApp, SDR, sucesso, follow-up e Cowork |
| `13_ADAPTIVE_SQUADS/` | squad-manifest e comandos especificos por cliente |
| `14_NICHE_KITS/` | produto futuro de kits por nicho |
| `18_AUTOMATION_STACK/` | automacoes genericas de processos e ferramentas |

## Regra

Agente e papel operacional, nao personalidade. Ele deve ler contrato, produzir output e devolver handoff curto.
