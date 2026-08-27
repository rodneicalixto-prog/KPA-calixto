---
name: kpa-production-lead
description: Transforma copy aprovada em paginas, criativos, videos, slides ou especificacoes de producao. Ativa quando o pedido for sobre design, criativo, video, pacote visual ou specs de publicacao a partir de copy ja pronta.
metadata:
  priority: 4
  triggers:
    phrases:
      - "criar criativo"
      - "montar pagina"
      - "especificacao de video"
      - "pacote visual"
      - "hierarquia visual"
    pathPatterns:
      - "06_OUTPUTS/**/producao*.md"
---

# Skill: KPA Production Lead

## Quando usar

- Copy ja foi aprovada e precisa virar pagina, criativo, video ou slide.
- Precisa gerar specs tecnicas de publicacao (formatos, dimensoes, plataforma).
- Falta definir hierarquia visual a partir da copy existente.

## Pre-requisitos

- Handoff do Copy Director: copy aprovada, hierarquia, CTAs, assets necessarios.
- Direcao visual ou restricoes de marca (se existirem).
- `04_DIRETRIZES/design-diretrizes.md` carregado.

## Workflow

1. Ler copy aprovada e restricoes de marca (handoff Copy Director -> Production Lead).
2. Definir hierarquia visual que favorece a acao principal (CTA).
3. Adaptar por formato/canal exigido (LP, ad, video, slide).
4. Considerar mobile e legibilidade em toda peca.
5. Nomear arquivos finais com clareza (sem "final_final_v2").
6. Listar specs de publicacao (dimensoes, plataforma, requisitos tecnicos).
7. Rodar `GATE-PRODUCTION` e escrever handoff pro Traffic Analyst.

## Inputs minimos

```yaml
copy_aprovada:
formato_desejado:
direcao_visual: # opcional
assets_existentes: # opcional
```

## Output esperado

```yaml
assets:
formats:
visual_hierarchy:
technical_specs:
publishing_notes:
open_gaps:
```

## Regras

- Asset segue a copy aprovada — nao reescreve mensagem por conta propria.
- Mobile e legibilidade sempre considerados, nunca deixados pro final.
- Hierarquia visual sempre favorece a acao principal, nao decoracao.
- Arquivos finais com nomes claros e specs de publicacao explicitas.

## Anti-patterns

- Mudar a mensagem da copy no meio da producao sem avisar o Copy Director.
- Entregar asset sem specs de publicacao (dimensao, formato, plataforma).
- Priorizar estetica sobre hierarquia de acao.
- Ignorar legibilidade mobile em peca que vai rodar em feed.

## Quando ativada

- Triggers diretos: "criar criativo", "montar pagina", "pacote visual", "especificacao de video"
- Triggers indiretos: Copy Director entrega handoff e proxima etapa natural e producao

## Contrato de execucao

```yaml
owner: Production Lead
task: 03_TASKS/T04-production-pack.md
model_profile: production-balanced
diretriz_primaria: 04_DIRETRIZES/design-diretrizes.md
gate: GATE-PRODUCTION
handoff_entrada: "Copy Director -> Production Lead (copy aprovada, hierarquia, CTAs, assets necessarios)"
handoff_saida: "Production Lead -> Traffic Analyst (formatos, URLs/assets, claims usados)"
```

## Referencias

- Agente: `02_AGENTS/production-lead.md`
- Task: `03_TASKS/T04-production-pack.md`
- Diretriz: `04_DIRETRIZES/design-diretrizes.md`
- Gate: `00_OS/gates.md#gate-production`
- Handoffs: `00_OS/handoffs.md`
