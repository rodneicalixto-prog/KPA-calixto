---
name: kpa-orchestrator
description: Coordena o pipeline completo do KPA V30 (research -> estrategia -> copy -> producao -> trafego -> QA) quando o pedido exige tres ou mais especialistas em sequencia — funil completo, lancamento, produto novo. Ativa quando o CoS identifica que a task nao e um pedido pontual, e sim um pacote de fases dependentes.
metadata:
  priority: 1
  triggers:
    phrases:
      - "funil completo"
      - "lancamento"
      - "produto novo"
      - "pacote de entregas"
      - "rodar o pipeline inteiro"
---

# Skill: KPA Orchestrator

## Quando usar

- O pedido e um funil completo, lancamento ou produto novo.
- Ha 3 ou mais especialistas envolvidos em sequencia (ex: Research -> Strategy -> Copy -> Producao -> Trafego).
- O CoS roteou o pedido aqui porque exige acompanhar dependencias de producao entre fases, nao so uma unica task.

## Pre-requisitos

- Task contract e context pack ja montados pelo CoS.
- Pipeline de referencia: `01_PIPELINE/kpa-v30-pipeline.yaml`.
- Gates aplicaveis de cada fase (`00_OS/gates.md`).

## Workflow

1. Ler o pipeline mestre (`01_PIPELINE/kpa-v30-pipeline.yaml`) e identificar em qual fase (P0-P7) o pedido comeca.
2. Montar o plano sequencial: qual especialista/skill entra em cada fase, na ordem certa.
3. Identificar paralelismo permitido (ex: Producao pode comecar em paralelo apos `GATE-COPY` passar).
4. Definir os handoffs exigidos entre fases, usando `00_OS/handoffs.md` como contrato.
5. Acionar cada especialista/skill na ordem (`kpa-researcher` -> `kpa-strategist` -> `kpa-copy-director` -> `kpa-production-lead` -> `kpa-traffic-analyst` -> `kpa-qa-editor`), sem pular gate pra acelerar.
6. Reportar status consolidado pro CoS a cada fase concluida.

## Inputs minimos

```yaml
task_contract:
context_pack:
pipeline_escolhido: # ex: 01_PIPELINE/kpa-v30-pipeline.yaml
gates_aplicaveis:
```

## Output esperado

```yaml
plano_sequencial:
ordem_de_execucao:
paralelismo_permitido:
handoffs_exigidos:
status_para_cos:
```

## Regras

- Nunca ignora gate pra acelerar entrega.
- Nao escreve copy final, nao faz pesquisa profunda — coordena, nao executa no lugar do especialista.
- Paralelismo so depois que o gate da fase anterior que o bloqueia passar (ex: Producao so em paralelo apos GATE-COPY pass).

## Anti-patterns

- Acionar Copy Director antes do Strategist entregar handoff completo.
- Pular GATE-STRATEGY ou GATE-COPY achando que "da pra ajustar depois".
- Assumir o papel de um especialista (ex: escrever a copy) em vez de rotear pra `kpa-copy-director`.
- Rodar fases em paralelo sem checar se o gate que as separa ja passou.

## Quando ativada

- Triggers diretos: "funil completo", "lancamento", "produto novo", "pacote de entregas"
- Triggers indiretos: CoS identifica 3+ especialistas necessarios pro mesmo pedido

## Contrato de execucao

```yaml
owner: KPA Orchestrator
pipeline: 01_PIPELINE/kpa-v30-pipeline.yaml
gates: "GATE-INTAKE -> GATE-RESEARCH -> GATE-STRATEGY -> GATE-COPY -> GATE-PRODUCTION -> GATE-TRAFFIC -> GATE-DELIVERY"
```

## Referencias

- Agente: `02_AGENTS/kpa-orchestrator.md`
- Pipeline: `01_PIPELINE/kpa-v30-pipeline.yaml`, `01_PIPELINE/operacao-ciclica.md`, `01_PIPELINE/deliverables.md`
- Gates: `00_OS/gates.md`
- Handoffs: `00_OS/handoffs.md`
