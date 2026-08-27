---
name: kpa-qa-editor
description: Valida qualquer output relevante contra o gate correspondente antes de considera-lo pronto — prioriza bugs, riscos, genericidade, falta de prova e desalinhamento com estrategia. Ativa antes de qualquer entrega final ou quando outro especialista pede revisao.
metadata:
  priority: 9
  triggers:
    phrases:
      - "revisar antes de entregar"
      - "rodar o gate"
      - "isso esta pronto?"
      - "validar qualidade"
      - "stress test"
---

# Skill: KPA QA Editor

## Quando usar

- Qualquer entrega relevante antes de ser considerada final (regra geral do kit).
- Um especialista termina o trabalho e precisa de validacao independente.
- Ha duvida se um output vai gerar retrabalho caro mais adiante.

## Pre-requisitos

- Output a revisar.
- Gate aplicavel (`00_OS/gates.md`) — cada camada tem o seu (GATE-RESEARCH, GATE-STRATEGY, GATE-COPY, GATE-PRODUCTION, GATE-TRAFFIC, GATE-WHATSAPP, GATE-AUTOMATION, GATE-PRODUCT, GATE-NICHE-KIT, GATE-DELIVERY).
- Context pack do projeto.
- Diretriz da area especifica, so se precisar diagnosticar a falha em profundidade.

## Workflow

1. Identificar qual gate se aplica ao output (pela area: pesquisa, estrategia, copy, producao, trafego, whatsapp, automacao, produto).
2. Ler o output contra os criterios exatos daquele gate em `00_OS/gates.md`.
3. Listar problemas especificos — nunca comentario abstrato tipo "melhorar a copy".
4. Pra cada problema, escrever a correcao concreta.
5. Calcular severidade (S0-S4) e score (0-10) usando `00_OS/gate-matrix.md`.
6. Definir verdict: pass, concerns, rework ou fail.
7. Escrever handoff curto pro CoS com o veredito e o proximo passo.

## Inputs minimos

```yaml
output_a_revisar:
gate_aplicavel:
context_pack:
diretriz_da_area: # opcional
```

## Output esperado

```yaml
verdict:
score:
specific_issues:
concrete_fixes:
must_rework:
can_ship_with_notes:
```

## Regras

- Sem comentario abstrato: toda critica aponta o problema exato e a correcao concreta.
- Score 9-10 = pass; 7-8 = concerns (avanca se nao houver S3); 5-6 = rework; 0-4 = fail.
- S3 bloqueia e volta pro especialista; S4 escala pro CoS pedir decisao humana.
- Falha repetida 3 vezes no mesmo gate e bloqueio automatico — nao insistir num quarto ciclo sem mudar de abordagem.

## Anti-patterns

- Aprovar output "porque ja demorou muito" ignorando bloqueio S3/S4.
- Dar feedback vago sem apontar a correcao.
- Rodar o gate errado pro tipo de output (ex: aplicar GATE-COPY numa entrega de trafego).
- Revisar sem ler os criterios do gate, so por intuicao.

## Quando ativada

- Triggers diretos: "revisar antes de entregar", "rodar o gate", "validar qualidade", "stress test"
- Triggers indiretos: qualquer especialista (Researcher, Strategist, Copy Director, Production Lead, Traffic Analyst, Product Auditor) termina e a proxima etapa e handoff pro CoS

## Contrato de execucao

```yaml
owner: QA Editor
task: sem task dedicada — usa o gate correspondente ao output revisado (00_OS/gates.md)
model_profile: reviewer-frontier (quando bloqueante)
diretriz_primaria: 00_OS/gates.md + 00_OS/gate-matrix.md
gate: "gate correspondente ao output (dinamico)"
handoff_entrada: "Traffic Analyst -> QA Editor (hipotese, KPI, evento, plano de leitura) — e qualquer outro especialista final de fase"
handoff_saida: "QA Editor -> CoS (verdict, issues, fixes, se bloqueia ou nao)"
```

## Referencias

- Agente: `02_AGENTS/qa-editor.md`
- Gates: `00_OS/gates.md`
- Matriz de severidade/verdict/escalada: `00_OS/gate-matrix.md`
- Handoffs: `00_OS/handoffs.md`
