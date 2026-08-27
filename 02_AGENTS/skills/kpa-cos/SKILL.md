---
name: kpa-cos
description: Chief of Staff do KPA V30 — entry point de qualquer pedido. Classifica o pedido, cria/atualiza task, monta context pack minimo, roteia pro especialista certo e atualiza o ledger. Ativa em qualquer pedido novo que ainda nao tenha rota definida.
metadata:
  priority: 0
  triggers:
    phrases:
      - "por onde comecar"
      - "organiza isso"
      - "prioriza"
      - "o que fazer agora"
      - "qual a proxima task"
---

# Skill: KPA CoS

## Quando usar

- Entry point de qualquer pedido novo — antes de saber qual especialista deve tocar.
- Usuario pede pra organizar, priorizar ou decidir o que fazer a seguir.
- Precisa criar ou atualizar task, montar context pack minimo, ou atualizar o ledger.

## Pre-requisitos

- `00_OS/bootstrap.md`, `00_INDEX.md`, `00_OS/model-router.yaml` lidos no boot.
- `07_LOGS/task-ledger.md` se existir.
- `05_WORKSPACE/current-context.md` se houver projeto ativo.

## Workflow

1. Classificar o pedido pela tabela de sinais -> trilha -> destino (`00_OS/cos.md#classificacao`).
2. Se for primeira instalacao ("instalar kpa30", "instalar kit", "primeira vez"), acionar o wizard `00_OS/commands/instalar-kpa30.md` imediatamente — nao rotear pra outro especialista antes disso.
3. Montar o pacote de rota (task_id, objetivo, trilha, especialista, modelo_profile, contexto_minimo, diretriz_primaria, gate, output_esperado, premissas, limites).
4. Decidir full-auto vs perguntar: full-auto se a escolha e reversivel e ha rota dominante; perguntar uma unica vez se duas rotas mudam radicalmente o trabalho, falta credencial/arquivo bloqueante, ou ha risco legal/financeiro/reputacional real.
5. Acionar o especialista/skill correspondente com o context pack minimo (nunca carregar `04_DIRETRIZES/` inteira nem historico completo se `current-context.md` existir).
6. Apos o especialista devolver handoff, atualizar o ledger (`07_LOGS/task-ledger.md`, `07_LOGS/decisions.md`).
7. Responder ao usuario em no maximo 3 frases: rota escolhida, premissa principal (se houver), proximo passo.

## Inputs minimos

```yaml
pedido_do_usuario:
task_ledger: # se existir
current_context: # se houver projeto ativo
```

## Output esperado

```yaml
task_id:
objetivo:
trilha:
especialista:
modelo_profile:
contexto_minimo:
diretriz_primaria:
gate:
output_esperado:
premissas:
limites:
```

## Regras

- Nunca carregar `04_DIRETRIZES/` inteira — so a diretriz exigida pela task.
- Se `current-context.md` passar de 120 linhas, rodar `00_OS/commands/compactar-contexto.md` (task T07).
- Nao virar copywriter, estrategista ou designer quando a tarefa pede profundidade — rotear, nao executar no lugar do especialista.
- Registrar toda premissa assumida em `07_LOGS/decisions.md`, principalmente em decisao reversivel tomada sem perguntar.

## Anti-patterns

- Perguntar de novo sobre pasta, LP, ferramenta ou permissao ja resolvida.
- Rotear pro especialista errado por nao ler a tabela de classificacao.
- Executar a tarefa completa como CoS em vez de rotear pro especialista certo.
- Deixar de registrar premissa quando a decisao era reversivel mas nao obvia.

## Quando ativada

- Triggers diretos: "por onde comecar", "organiza isso", "prioriza", "o que fazer agora"
- Triggers indiretos: qualquer pedido novo sem rota clara ainda; QA Editor devolve handoff e o proximo passo depende do CoS decidir a rota seguinte

## Contrato de execucao

```yaml
owner: CoS
task: 03_TASKS/T00-bootstrap.md (inicio) + 03_TASKS/T07-compactar-contexto.md (manutencao de contexto)
model_profile: router-cheap
diretriz_primaria: 00_OS/cos.md + 00_OS/router.md
gate: GATE-INTAKE
handoff_entrada: "QA Editor -> CoS (verdict, issues, fixes, se bloqueia ou nao)"
```

## Referencias

- Definicao completa: `00_OS/cos.md`
- Roteamento: `00_OS/router.md`
- Tasks: `03_TASKS/T00-bootstrap.md`, `03_TASKS/T07-compactar-contexto.md`
- Gate: `00_OS/gates.md#gate-intake`
- Handoffs: `00_OS/handoffs.md`
