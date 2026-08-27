---
name: kpa-traffic-analyst
description: Planeja, valida e diagnostica campanhas com hipoteses claras e leitura de dados — do launch review inicial ao ciclo semanal de otimizacao. Ativa quando o pedido for sobre subir campanha, ler metricas ou decidir proximo passo de trafego.
metadata:
  priority: 5
  triggers:
    phrases:
      - "subir campanha"
      - "ler metricas"
      - "diagnostico de campanha"
      - "operacao semanal de trafego"
      - "plano de leitura"
    pathPatterns:
      - "05_WORKSPACE/clientes/*/traffic-state.json"
---

# Skill: KPA Traffic Analyst

## Quando usar

- Campanha esta pronta (oferta, copy, assets, destino) e precisa de validacao antes de ir ao ar.
- Ja existe campanha viva e chegou a hora do ciclo semanal de leitura/decisao.
- Precisa diagnosticar queda de performance ou decidir proxima hipotese de teste.

## Pre-requisitos

- Oferta e copy aprovadas, assets disponiveis, destino definido (pra launch review).
- Metricas da semana e outputs ativos (pra operacao semanal).
- `04_DIRETRIZES/traffic-diretrizes.md` carregado.
- Meta Ads CLI configurado (`.env` com `META_ACCESS_TOKEN`) quando for puxar dados reais — ver `11_TRAFFIC_STACK/skills/meta-cli-install/SKILL.md`.

## Workflow

### Launch review (antes de subir)

1. Ler handoff Production Lead -> Traffic Analyst (formatos, assets, claims usados).
2. Definir objetivo de campanha mensuravel e evento de conversao.
3. Escrever hipoteses de criativo testaveis.
4. Definir plano de leitura de dados antes de subir (quando olhar, o que decide).
5. Listar riscos (tracking, publico, budget, claim).
6. Rodar `GATE-TRAFFIC`.

### Operacao semanal (campanha viva)

1. Ler metricas da semana e outputs ativos.
2. Separar problema por causa: oferta, copy, criativo, pagina, publico ou tracking.
3. Decidir por hipotese (nao por achismo).
4. Atualizar ledger e criar no maximo 3 proximas tasks.
5. Rodar `GATE-TRAFFIC` de novo e escrever handoff pro QA Editor.

## Inputs minimos

```yaml
oferta:
copy:
assets:
destino:
historico_de_metricas: # opcional, obrigatorio na operacao semanal
```

## Output esperado

```yaml
campaign_objective:
tracking_event:
audiences:
creative_tests:
budget_logic:
kpis:
reading_plan:
risks:
```

## Regras

- Campanha paga sem evento de conversao definido nao passa no gate (bloqueio automatico).
- Toda decisao de otimizacao precisa citar a hipotese testada, nao intuicao solta.
- No maximo 3 proximas tasks por ciclo semanal — evita fila infinita.
- Nao inventar numero de metrica: se o dado nao existir, marcar como gap.

## Anti-patterns

- Subir campanha sem plano de leitura definido.
- Misturar problema de oferta com problema de tracking no mesmo diagnostico sem separar.
- Recomendar "testar mais criativos" sem hipotese especifica.
- Ignorar risco de budget/publico levantado antes do launch.

## Quando ativada

- Triggers diretos: "subir campanha", "ler metricas", "diagnostico de campanha", "operacao semanal de trafego"
- Triggers indiretos: Production Lead entrega handoff e proxima etapa e ir ao ar; fim de semana de veiculacao pede leitura

## Contrato de execucao

```yaml
owner: Traffic Analyst
task: 03_TASKS/T05-launch-review.md
task_ciclica: 03_TASKS/T06-operacao-semanal.md
model_profile: analytics-balanced
diretriz_primaria: 04_DIRETRIZES/traffic-diretrizes.md
gate: GATE-TRAFFIC
handoff_entrada: "Production Lead -> Traffic Analyst (formatos, URLs/assets, claims usados)"
handoff_saida: "Traffic Analyst -> QA Editor (hipotese, KPI, evento, plano de leitura)"
```

## Referencias

- Agente: `02_AGENTS/traffic-analyst.md`
- Tasks: `03_TASKS/T05-launch-review.md`, `03_TASKS/T06-operacao-semanal.md`
- Diretriz: `04_DIRETRIZES/traffic-diretrizes.md`
- Gate: `00_OS/gates.md#gate-traffic`
- Handoffs: `00_OS/handoffs.md`
- Camada expandida (operacao continua sobre campanhas vivas): `11_TRAFFIC_STACK/README.md`
