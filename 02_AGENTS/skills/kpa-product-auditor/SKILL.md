---
name: kpa-product-auditor
description: Audita se a promessa publica (LP, onboarding, automacoes, WhatsApp, suporte) e de fato sustentada pela entrega real do produto. Ativa quando a LP promete algo forte, o usuario leigo trava no setup, ou ha duvida se o kit/produto entrega o que vende.
metadata:
  priority: 6
  triggers:
    phrases:
      - "auditar landing page"
      - "promessa vs entrega"
      - "produto robusto"
      - "gap de produto"
      - "a LP promete mas"
---

# Skill: KPA Product Auditor

## Quando usar

- LP promete automacao, facilidade, rapidez ou resultado forte.
- Produto precisa ficar mais robusto antes de vender mais.
- Ha duvida se o kit entrega o que promete.
- Usuario final nao tecnico esta travando no setup.
- WhatsApp/Cowork ainda nao tem fluxo suficiente pra sustentar a promessa.

## Pre-requisitos

- URL ou arquivo da LP.
- Lista de entregaveis atuais, onboarding atual, fluxos WhatsApp/atendimento atuais.
- `04_DIRETRIZES/product-hardening.md` carregado.
- Se a LP nao estiver disponivel (nem pasta nem URL), a auditoria fica `blocked` — pode-se gerar so o framework/checklist.

## Workflow

1. Extrair todos os claims da LP (funcional, resultado, suporte, automacao, velocidade, facilidade, garantia).
2. Mapear onde cada claim e de fato entregue no produto.
3. Marcar cada claim como `entregue`, `parcial`, `nao entregue` ou `sem evidencia` — nunca suavizar.
4. Listar falhas especificas de usuario leigo (onde ele trava sozinho).
5. Priorizar gaps que quebram confianca, ativacao, venda ou retencao.
6. Montar roadmap em fases: bloquear risco -> robustecer core -> automatizar -> nichar.
7. Rodar `GATE-PRODUCT`.

## Inputs minimos

```yaml
url_ou_arquivo_lp:
entregaveis_atuais:
onboarding_atual:
fluxos_whatsapp_atuais:
provas: # opcional
feedback_usuarios: # opcional
```

## Output esperado

```yaml
promise_inventory:
delivery_coverage:
gaps_by_severity:
user_leigo_failures:
automation_gaps:
whatsapp_gaps:
roadmap:
blocked_by:
```

## Regras

- Se a LP promete e o produto nao entrega, isso e gap de produto — nunca vira "ajuste de copy" pra esconder o problema.
- Claim forte sem prova precisa de marcador `[A PREENCHER]`, nunca de invencao.
- Gap de severidade alta que quebra confianca/ativacao vem antes de qualquer polimento cosmetico.

## Anti-patterns

- Suavizar gap real como "pequeno ajuste de expectativa".
- Auditar so a copy da LP e ignorar onboarding/suporte/automacao real.
- Marcar como `entregue` sem checar evidencia concreta.

## Quando ativada

- Triggers diretos: "auditar landing page", "promessa vs entrega", "produto robusto", "gap de produto"
- Triggers indiretos: usuario leigo trava no setup repetidamente; CoS identifica reclamacao recorrente sobre expectativa vs entrega

## Contrato de execucao

```yaml
owner: Product Auditor
task: 03_TASKS/T08-product-hardening-lp-audit.md
model_profile: reviewer-frontier
diretriz_primaria: 04_DIRETRIZES/product-hardening.md
gate: GATE-PRODUCT
```

## Nota de validacao (premissa registrada)

O arquivo `03_TASKS/T08-product-hardening-lp-audit.md` declara `owner: CoS` no seu YAML de contrato, mas o agente que de fato executa essa auditoria (`02_AGENTS/product-auditor.md`) e o Product Auditor. Assumimos que o CoS e o owner do *processo* (abrir/fechar a task) e o Product Auditor e quem *executa* a auditoria — mesmo padrao usado em outras tasks onde o CoS abre e delega. Divergencia registrada em `07_LOGS/decisions.md`; se for erro de digitacao no task file, corrigir o `owner` para `Product Auditor` numa proxima revisao.

## Referencias

- Agente: `02_AGENTS/product-auditor.md`
- Task: `03_TASKS/T08-product-hardening-lp-audit.md`
- Diretriz: `04_DIRETRIZES/product-hardening.md`
- Gate: `00_OS/gates.md#gate-product`
- Checklist relacionado: `08_CHECKLISTS/product-promise-audit.md`
