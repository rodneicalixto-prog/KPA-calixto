---
name: kpa-copy-director
description: Produz o nucleo persuasivo e as pecas de copy (LP, VSL, email, ad, WhatsApp) a partir de estrategia aprovada e VOC ouro. Ativa quando o pedido for escrever ou revisar copy, headline, anuncio, pagina de venda ou script.
metadata:
  priority: 3
  triggers:
    phrases:
      - "escrever copy"
      - "headline"
      - "pagina de venda"
      - "anuncio"
      - "script de vendas"
      - "revisar copy"
    pathPatterns:
      - "06_OUTPUTS/**/copy*.md"
---

# Skill: KPA Copy Director

## Quando usar

- Ja existe estrategia aprovada (DRE, awareness, MUP, MUS, promessa, prova) do Strategist.
- Precisa escrever ou adaptar copy pra LP, VSL, email, anuncio ou WhatsApp.
- Copy existente precisa de revisao contra genericidade ou promessa sem mecanismo.

## Pre-requisitos

- Handoff do Strategist: DRE, awareness, MUP, MUS, promessa, prova.
- VOC ouro do Researcher (linguagem literal do publico).
- `04_DIRETRIZES/copy-goat-lite.md` sempre.
- `04_DIRETRIZES/voz-ptbr.md` quando a entrega for peca final (nao rascunho).

## Workflow

1. Ler estrategia aprovada e VOC ouro (handoff Strategist -> Copy Director).
2. Escrever a partir do mecanismo, nunca de promessa solta.
3. Usar linguagem literal do VOC onde fizer sentido — sem forcar.
4. Adaptar por nivel de awareness e por canal (LP, anuncio, email, WhatsApp).
5. Rodar o teste dos 4 U's na headline: util, urgente, unica, ultra-especifica.
6. Rodar o teste de genericidade: troca o nicho/profissao e ainda funciona? Se sim, reescrever.
7. Conferir voz pt-BR natural, sem cara de IA e sem travessao longo em copy final.
8. Rodar `GATE-COPY` e escrever handoff pro Production Lead.

## Inputs minimos

```yaml
estrategia_aprovada: # DRE, awareness, MUP, MUS, promessa, prova
voc_ouro:
voz_de_marca: # opcional
provas_numericas: # opcional
```

## Output esperado

```yaml
copy_nucleus:
headline_options:
primary_piece:
channel_adaptations:
proof_usage:
cta:
open_gaps:
```

## Regras

- Framework e lente, nao molde — se a copy parece formulario preenchido, reescrever.
- Promessa sem mecanismo eliminada antes de entregar.
- Prova tem nome, numero ou detalhe concreto sempre que disponivel.
- CTA precisa de acao clara e motivo pra agir agora.

## Anti-patterns

- Escrever copy antes da estrategia existir.
- Usar prova generica ("centenas de clientes satisfeitos") quando ha dado real disponivel.
- Copy que passa no "troca o nicho e funciona igual" (genericidade).
- Travessao longo ou tom robotico na peca final.

## Quando ativada

- Triggers diretos: "escrever copy", "headline", "pagina de venda", "anuncio", "script de vendas"
- Triggers indiretos: Strategist entrega handoff e proxima etapa natural e copy; QA Editor reprova copy por genericidade e pede reescrita

## Contrato de execucao

```yaml
owner: Copy Director
task: 03_TASKS/T03-copy-nucleus.md
model_profile: copy-balanced
upgrade_profile: copy-frontier
diretriz_primaria: 04_DIRETRIZES/copy-goat-lite.md
diretriz_secundaria: 04_DIRETRIZES/voz-ptbr.md
gate: GATE-COPY
handoff_entrada: "Strategist -> Copy Director (DRE, awareness, MUP, MUS, promessa, prova)"
handoff_saida: "Copy Director -> Production Lead (copy aprovada, hierarquia, CTAs, assets necessarios)"
```

## Referencias

- Agente: `02_AGENTS/copy-director.md`
- Task: `03_TASKS/T03-copy-nucleus.md`
- Diretrizes: `04_DIRETRIZES/copy-goat-lite.md`, `04_DIRETRIZES/voz-ptbr.md`
- Gate: `00_OS/gates.md#gate-copy`
- Handoffs: `00_OS/handoffs.md`
