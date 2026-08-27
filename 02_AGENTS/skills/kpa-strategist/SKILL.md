---
name: kpa-strategist
description: Define a tese do funil (publico, awareness, DRE, MUP, MUS, promessa, prova e posicionamento) antes de qualquer copy ser escrita. Ativa quando o pedido for sobre oferta, mecanismo, posicionamento, Big Idea ou "qual a promessa/estrategia" de um produto/campanha.
metadata:
  priority: 2
  triggers:
    phrases:
      - "definir estrategia"
      - "qual a promessa"
      - "mecanismo unico"
      - "big idea"
      - "posicionamento da oferta"
      - "DRE"
      - "MUP e MUS"
    pathPatterns:
      - "05_WORKSPACE/clientes/*/estrategia*.md"
---

# Skill: KPA Strategist

## Quando usar

- O pedido envolve definir ou revisar oferta, mecanismo ou posicionamento.
- Existe VOC/pesquisa pronta (do Researcher) mas falta a tese que amarra tudo.
- Alguem vai escrever copy e ainda nao ha awareness, DRE, MUP/MUS ou promessa definidos.
- Precisa validar se uma promessa existente tem mecanismo ou e generica.

## Pre-requisitos

- Context pack do projeto (`05_WORKSPACE/current-context.md` ou equivalente do cliente).
- Output do Researcher (VOC ouro, dores, desejos, objecoes) — se nao existir, marcar como gap e seguir com hipoteses `[A PREENCHER]`.
- `04_DIRETRIZES/copy-goat-lite.md` carregado.

## Workflow

1. Ler context pack + output de research (handoff Researcher -> Strategist: VOC ouro, objecoes, linguagem literal).
2. Identificar o nivel de awareness do publico.
3. Separar causa raiz do problema (DRE) da solucao proprietaria (mecanismo).
4. Definir MUP (mecanismo unico do problema) e MUS (mecanismo unico da solucao) separadamente.
5. Redigir a Big Idea e testar: especifica, emocional, defensavel, memoravel. Rodar tambem o Logo Test (troca o nicho/marca e ainda funciona? Se sim, e generica).
6. Amarrar a promessa a prova disponivel — promessa sem mecanismo nao passa; mecanismo que concorrente rouba sem mudar nada nao passa.
7. Rodar `GATE-STRATEGY` e escrever handoff curto pro Copy Director.

## Inputs minimos

```yaml
context_pack:
research_output: # VOC ouro, dores, desejos, objecoes, linguagem literal
provas_existentes: # opcional
```

## Output esperado

```yaml
publico:
awareness:
dre:
mup:
mus:
big_idea:
promessa:
provas:
inimigo:
risco_principal:
```

## Regras

- Promessa sem mecanismo nao passa no gate.
- Mecanismo que o concorrente copia sem mudar nada nao passa.
- Awareness, MUP e MUS devem aparecer separados — nunca misturados num paragrafo so.
- Sem VOC real disponivel, marcar hipoteses como `[A PREENCHER]` em vez de inventar dado de publico.

## Anti-patterns

- Pular direto pra copy sem awareness/DRE/mecanismo definidos.
- Copiar promessa de concorrente e so trocar o nome da marca.
- Big Idea generica que passa despercebida no Logo Test.
- Inventar prova que nao existe pra sustentar a promessa.

## Quando ativada

- Triggers diretos: "definir estrategia", "qual a promessa", "mecanismo unico", "big idea", "posicionamento da oferta"
- Triggers indiretos: usuario pede copy/LP/ads mas ainda nao tem tese definida; QA Editor devolve gate GATE-COPY reprovado por "promessa sem mecanismo"

## Contrato de execucao

```yaml
owner: Strategist
task: 03_TASKS/T02-strategy-mechanism.md
model_profile: strategy-frontier
diretriz_primaria: 04_DIRETRIZES/copy-goat-lite.md
gate: GATE-STRATEGY
handoff_entrada: "Researcher -> Strategist (VOC ouro, objecoes, linguagem literal)"
handoff_saida: "Strategist -> Copy Director (DRE, awareness, MUP, MUS, promessa, prova)"
```

## Referencias

- Agente: `02_AGENTS/strategist.md`
- Task: `03_TASKS/T02-strategy-mechanism.md`
- Diretriz: `04_DIRETRIZES/copy-goat-lite.md`
- Gate: `00_OS/gates.md#gate-strategy`
- Handoffs: `00_OS/handoffs.md`
