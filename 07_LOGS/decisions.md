# Decisions

Registre decisoes que afetam o rumo do projeto.

| Data | Decisao | Premissa | Impacto | Reversivel |
|---|---|---|---|---|
| 2026-08-27 | Criadas 10 Skills (`02_AGENTS/skills/kpa-*`) empacotando os agentes core do V30 (CoS, Orchestrator, Researcher, Strategist, Copy Director, Production Lead, Traffic Analyst, Product Auditor, QA Editor, Memory Curator) com triggers ativaveis | Nenhum desses agentes tinha SKILL.md; convertidos seguindo `21_BUILDER_KIT/scaffolds/skill-scaffold.md`, cada um validado contra sua task (`03_TASKS/`), diretriz (`04_DIRETRIZES/`), gate (`00_OS/gates.md`) e handoff (`00_OS/handoffs.md`) | Agentes core agora ativaveis por frase-gatilho como as outras stacks (Trafego/WhatsApp/Automacao) | Sim — sao arquivos novos, remover nao afeta os agentes originais em `02_AGENTS/*.md` |
| 2026-08-27 | Nao foi criada skill `kpa-automation-architect` | Pre-flight (regra do Forge) encontrou skill equivalente ja existente: `18_AUTOMATION_STACK/skills/process-automation-design/SKILL.md` cobre a mesma task (T09), mesmo gate (GATE-AUTOMATION) e mesmos outputs (blueprint/SOP/matriz/teste/rollback) | Evita skill duplicada | Sim — pode ser criada depois se o conteudo divergir |
| 2026-08-27 | Adicionada definicao de `GATE-MEMORY` em `00_OS/gates.md` | `02_AGENTS/kpa-memory-curator.md` ja citava `GATE-MEMORY` mas o gate nunca tinha sido definido em `00_OS/gates.md` nem `00_OS/gate-matrix.md` — usados os criterios ja descritos no proprio agente | Fecha lacuna de gate ausente; QA Editor agora tem criterio pra validar output do Memory Curator | Sim — e so documentacao, pode ser editado |
| 2026-08-27 | Registrada divergencia de `owner` em `03_TASKS/T08-product-hardening-lp-audit.md` (diz `CoS`, mas quem executa e o Product Auditor) | Nao corrigido automaticamente por ser mudanca em contrato de task existente; documentado como nota dentro de `02_AGENTS/skills/kpa-product-auditor/SKILL.md` | Nenhum imediato; fica registrado pra correcao humana decidir se e erro de digitacao | Sim — trocar o campo `owner` no task file quando confirmado |

> Quando uma decisao for tomada com impacto no produto/projeto, anote aqui. Inclua premissa (por que decidiu assim), impacto (o que muda) e reversibilidade (consegue desfazer? como?).
