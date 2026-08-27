# Task: Investigar Queda de Performance (Root Cause Analysis)

> Task usada por `@traffic-diagnostician` e `@traffic-orchestrator` quando o usuario reporta queda de performance ("caiu", "ROAS despencou", "CPA disparou"). Implementa a arvore de diagnostico de 6 camadas do agente, cruzando dados reais do CLI `meta` com os frameworks das especialidades da stack.

## Quando esta task e executada

- `*queda [janela]` em `@traffic-orchestrator`
- `*investigar`, `*queda-cpa`, `*queda-roas`, `*saturacao`, `*post-mortem`, `*checklist` em `@traffic-diagnostician`

## Pre-requisitos (validar antes de executar)

1. **Cliente carregado** — `05_WORKSPACE/clientes/<cliente>/CLAUDE.md` lido.
2. **`act_id` resolvido**.
3. **CLI `meta` funcionando**.
4. **Sintoma reportado** — o que o usuario descreveu como "queda" (metrica especifica: ROAS, CPA, spend, conversoes).
5. **Baseline do cliente** — `05_WORKSPACE/clientes/<cliente>/baseline-kpis.md` lido, pra comparar contra o normal do cliente, nao benchmark generico.

Se algum falhar, ABORTAR com mensagem clara. Nao chutar causa sem dado.

## Pipeline de execucao — arvore de 6 camadas (ordem obrigatoria, nao pular)

Regra do agente: investigar sempre em ordem — pular camada = perder evidencia.

### Camada 1 — Tracking (delegar pra `@attribution-auditor`)

1. Rodar a auditoria de tracking (ver `04_DIRETRIZES/traffic-diretrizes.md` e o agente `attribution-auditor.md`): pixel/CAPI saude, match quality, dedup, Standard vs Incremental ROAS.
2. Sintomas que apontam pra essa camada: conversoes reportadas cairam sem queda de trafego real; ROAS subiu mas vendas de backend cairam (falsa euforia); janela de atribuicao mudou no periodo.
3. Se tracking quebrado: essa e a causa-raiz. Parar aqui, reportar, corrigir tracking antes de qualquer outra acao.
4. Se tracking OK: seguir pra Camada 2.

### Camada 2 — Criativo

Puxar insights por ad (mesmo pipeline de `analisar-criativos.md`, Etapas 1-2) e checar:

| Sintoma | Diagnostico | Acao |
|---|---|---|
| Hook rate caiu 30%+ semana-a-semana | Saturacao criativa | Lateralizar vencedor (5-10 variacoes) |
| Frequencia >5 + CTR caindo + sem vendas novas | Audience exhaustion + criativo cansado | Trocar 50% dos criativos ou expandir audience |
| CTR em plateau por 2+ semanas | Criativos no piloto automatico | Refresh com novos conceitos, nao so lateralizacoes |
| Retention caiu mas hook ok | Body perdeu forca | Refazer body mantendo hook |

### Camada 3 — Audience

Puxar insights por adset (`--level adset`) e checar overlap, CPM subindo, LAL pequeno saturado, exclusion lists desatualizadas (compradores aparecendo em campanhas cold).

### Camada 4 — Oferta

Sem dado de CLI direto — perguntar ao cliente/checar `05_WORKSPACE/clientes/<cliente>/CLAUDE.md`: preco mudou? bonus removido? garantia mudou? Se `conversion rate` caiu sem mudanca interna, considerar concorrencia — delegar pra `@competitor-spy`.

### Camada 5 — Funil pos-clique (delegar pra `@funnel-analyst`)

Aplicar o framework "Onde Quebrou?" do `@funnel-analyst`: CTR ok mas conversao caiu, time on page mudou, bounce rate disparou. Ver `04_DIRETRIZES/traffic-diretrizes.md`.

### Camada 6 — Externo

Checar sazonalidade (comparar mesmo periodo do ano anterior), mudanca de politica/algoritmo Meta (Meta Business Help + comunidades), evento social/economico, aumento de competicao (CPM subiu sem aumentar audience — delegar pra `@competitor-spy`).

### Consolidacao — ranquear hipoteses

1. Listar toda evidencia coletada por camada (tabela: camada | status ✅/⚠️/❌ | evidencia).
2. Ranquear hipoteses por probabilidade, cada uma com evidencia especifica — nunca concluir com 1 hipotese so.
3. Causa-raiz precisa ser **acionavel**: "o algoritmo mudou" sozinho nao e resposta valida, tem que vir com uma acao concreta.

### Output — formato do relatorio

```markdown
## Diagnostico Forensic — {Cliente} {Data}

### Sintoma reportado
{o que o usuario descreveu}

### Investigacao realizada (camadas)
| Camada | Status | Evidencia |
| 1. Tracking | ... | ... |
| 2. Criativo | ... | ... |
| 3. Audience | ... | ... |
| 4. Oferta | ... | ... |
| 5. Funil | ... | ... |
| 6. Externo | ... | ... |

### Causa-raiz mais provavel
Hipotese principal: {hipotese} (probabilidade XX%) — evidencia: {dado}

### Causas secundarias
1. {hipotese 2} (XX%)
2. {hipotese 3} (XX%)

### Acao imediata (24h)
- {acao} — quem: {agente}

### Acao media (7d)
- {acao}

### Metricas pra acompanhar
- {KPI} — alvo {valor} em {dias}
```

Salvar em `05_WORKSPACE/clientes/<cliente>/_relatorios/<YYYY-MM-DD>-post-mortem.md`.

## `*checklist` — atalho sem investigacao completa

Quando o usuario pede so o checklist de sintomas -> causas (sem rodar toda a arvore), devolver a tabela consolidada das camadas 2-4 acima como referencia rapida, deixando claro que e heuristica, nao substitui a investigacao completa se a decisao for cara (pausar campanha, cortar budget).

## Tratamento de erros

| Erro | Causa provavel | Acao |
|---|---|---|
| `@attribution-auditor` nao consegue validar tracking | Falta de permissao ou pixel nao configurado | Reportar como bloqueio na Camada 1; nao seguir pras demais camadas sem resolver |
| Dados insuficientes numa camada | Conta nova, pouco spend, janela curta | Marcar camada como `sem_dado_suficiente`, nao inventar conclusao |

## Handoff

- `@traffic-diagnostician` -> `@attribution-auditor` (camada 1)
- `@traffic-diagnostician` -> `@creative-analyst` (camada 2)
- `@traffic-diagnostician` -> `@funnel-analyst` (camada 5)
- `@traffic-diagnostician` -> `@competitor-spy` (camada 6)
- `@traffic-diagnostician` -> `CoS`/`QA Editor`: causa-raiz + acao imediata, pra registrar no ledger do cliente

## Referencias

- Agente: `11_TRAFFIC_STACK/agents/traffic-diagnostician.md`
- Diretriz: `04_DIRETRIZES/traffic-diretrizes.md`
- Gate: `00_OS/gates.md#gate-traffic`
