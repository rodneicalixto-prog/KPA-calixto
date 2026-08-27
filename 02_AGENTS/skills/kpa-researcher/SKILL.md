---
name: kpa-researcher
description: Transforma mercado confuso em sinais utilizaveis (VOC, objecoes, linguagem literal, concorrentes, provas e gaps) antes de qualquer estrategia ou copy. Ativa quando faltar VOC, pesquisa de publico ou mapeamento de concorrentes claro.
metadata:
  priority: 1
  triggers:
    phrases:
      - "pesquisa de publico"
      - "VOC"
      - "voz do cliente"
      - "quem e o cliente ideal"
      - "mapear concorrentes"
      - "o que o publico fala"
    pathPatterns:
      - "05_WORKSPACE/clientes/*/pesquisa*.md"
---

# Skill: KPA Researcher

## Quando usar

- Nao existe VOC literal suficiente para a task (copy, LP, ads, estrategia).
- Precisa separar fato de hipotese sobre o publico.
- Falta mapear objecoes, linguagem literal, dores e desejos antes de escrever qualquer promessa.
- Precisa levantar concorrentes e provas disponiveis no mercado.

## Pre-requisitos

- Publico ou nicho identificado (mesmo que amplo).
- Oferta ou hipotese de oferta.
- `04_DIRETRIZES/pesquisa-voc.md` carregado.
- `05_WORKSPACE/current-context.md` do projeto/cliente.

## Workflow

1. Ler `03_TASKS/task-contract.md` ou a task especifica que pediu a pesquisa.
2. Coletar sinais reais (reviews, comentarios, transcricoes, grupos, suporte) — nunca inventar frase de cliente.
3. Separar fatos de hipoteses explicitamente.
4. Classificar cada sinal por dor, desejo, objecao, identidade, linguagem e inimigo.
5. Priorizar frases literais do publico (nao parafrasear em linguagem generica de marketing).
6. Selecionar no minimo 3 "quotes ouro" com origem rastreavel, prontas pra copy.
7. Rodar `GATE-RESEARCH` e entregar resumo curto pro Strategist e pro Copy Director.

## Inputs minimos

```yaml
publico_ou_nicho:
oferta_ou_hipotese:
concorrentes: # opcional
fontes_preferidas: # opcional
```

## Output esperado

```yaml
voc_ouro:
dores:
desejos:
objecoes:
linguagem_literal:
concorrentes:
hipoteses:
provas_encontradas:
gaps:
```

## Regras

- Toda quote precisa ter origem (de onde veio) — sem origem nao e "ouro", e hipotese.
- Minimo de 3 quotes ouro pra passar em `GATE-RESEARCH`.
- Fato e hipotese ficam em campos separados, nunca misturados.
- Se a fonte de VOC nao existir, marcar gap explicitamente em vez de simular quote.

## Anti-patterns

- Inventar depoimento ou frase de cliente que ninguem disse.
- Parafrasear a fala do publico em linguagem de marketing genérica, perdendo o literal.
- Entregar pesquisa sem separar dor de objeção de desejo.
- Pular pesquisa "porque o nicho e obvio" quando a task pede VOC.

## Quando ativada

- Triggers diretos: "pesquisa de publico", "VOC", "voz do cliente", "mapear concorrentes"
- Triggers indiretos: Strategist ou Copy Director recebem task sem VOC suficiente e devolvem pedido de pesquisa

## Contrato de execucao

```yaml
owner: Researcher
task: 03_TASKS/T01-research-voc.md
model_profile: research-balanced
diretriz_primaria: 04_DIRETRIZES/pesquisa-voc.md
gate: GATE-RESEARCH
handoff_saida: "Researcher -> Strategist (VOC ouro, objecoes, linguagem literal)"
```

## Referencias

- Agente: `02_AGENTS/researcher.md`
- Task: `03_TASKS/T01-research-voc.md`
- Diretriz: `04_DIRETRIZES/pesquisa-voc.md`
- Gate: `00_OS/gates.md#gate-research`
- Handoffs: `00_OS/handoffs.md`
