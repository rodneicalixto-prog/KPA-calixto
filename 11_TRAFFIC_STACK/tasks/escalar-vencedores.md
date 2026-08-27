# Task: Escalar Campanhas Vencedoras

> Task usada por `@scaling-strategist` e `@traffic-orchestrator` quando o cliente ja tem vencedor validado e quer escalar. Implementa a decision tree e os 5 metodos de escala do agente sobre dados reais do CLI `meta`.

## Quando esta task e executada

- `*escalar [janela]` em `@traffic-orchestrator`
- `*plano-escala`, `*lateralizar`, `*horizontal`, `*multi-account`, `*teto-escala` em `@scaling-strategist`

## Pre-requisitos (validar antes de executar)

1. **Cliente carregado** + **vencedor identificado** — se nao houver vencedor validado, ABORTAR e redirecionar pra `meta-dr-specialist` (ou `analisar-criativos.md`) validar primeiro. Nunca escalar sem vencedor.
2. **Tempo de validacao conhecido** — quantos dias o vencedor ja roda com CPA estavel.
3. **Baseline do cliente** — `05_WORKSPACE/clientes/<cliente>/baseline-kpis.md` (ROAS alvo, CPA alvo, teto de budget se ja definido).

## Pipeline de execucao

### Etapa 1 — Coletar estado atual

```powershell
meta ads insights get `
  --ad-account-id act_<ID> `
  --date-preset last_<N>d `
  --level campaign `
  --fields spend,purchase_roas,cost_per_action_type,frequency `
  -o json
```

Extrair: spend atual/dia, ROAS (Standard e, se disponivel via `@attribution-auditor`, Incremental), CPA, frequencia, tempo de validacao do vencedor.

### Etapa 2 — Decision tree (framework do agente)

```text
Tem vencedor identificado? Nao -> parar, redirecionar pra validacao.
Sim -> quanto tempo de validacao?
  <3 dias -> ABO duplicate (cauteloso, +R$100-200)
  3-7 dias -> CBO ramp (+20%/dia ate teto saudavel)
  >7 dias -> decidir por sintoma:
    - Frequencia alta + CTR caindo -> LATERALIZACAO OXIGENIO
    - Frequencia ok + ROAS estavel -> CBO ramp continuar
    - Ja lateralizou + saturando -> HORIZONTAL
    - Esgotou tudo + ainda quer mais -> MULTI-ACCOUNT
```

### Etapa 3 — `*plano-escala`: montar o plano completo

1. Rodar a decision tree (Etapa 2) e escolher o metodo.
2. Se **ABO duplicate**: instruir duplicar o adset vencedor mantendo o budget original (ex: +R$100/dia em adset novo); alertar sobre auction overlap (gerenciar via exclusion lists).
3. Se **CBO ramp**: gerar cronograma de +20-30%/dia (nunca dobrar), com regra de segurança — CPA subiu >20% em ramp: `HOLD` por 2 dias, nao pausar; CPA subiu >40%: voltar 1 step e investigar (acionar `investigar-queda.md`); em fim de semana/feriado, pausar o ramp.
4. Se **Lateralizacao Oxigenio**: delegar geracao de 5-10 briefings de variacao genuina pra `@creative-analyst` (Etapa 5 de `analisar-criativos.md`) antes de aumentar budget.
5. Se **Horizontal**: propor novas frentes (formatos, publicos LAL diferentes, novo idioma) — so depois de esgotar Oxigenio.
6. Se **Multi-account**: so recomendar apos esgotar Oxigenio + Horizontal; alertar sobre risco de politica Meta (nunca duplicar conta no mesmo BM sem seguir processo oficial).

### Etapa 4 — `*teto-escala`: identificar teto saudavel

Sinais de teto (framework do agente): CPA cresce mesmo aumentando criativos; frequencia alta em todas as audiences; CPM disparou no leilao; ROAS Incremental cai mais que Standard.

Estimativas de referencia por nicho (ajustar sempre pelo baseline real do cliente, nunca usar isso como teto fixo):

| Nicho | Teto estimado |
|---|---|
| Infoproduto baixo ticket | R$3k-10k/dia |
| Infoproduto alto ticket | R$10k-30k/dia |
| E-commerce geral | R$10k-50k/dia |
| E-commerce premium | R$5k-20k/dia |
| Mentoria alto ticket | R$2k-10k/dia |

Apos teto: multi-account, expansao geografica ou novos produtos.

### Etapa 5 — Output — Plano de Escala

```markdown
## Plano de Escala — {Cliente} {Data}

### Estado atual
- Spend atual: R$X/dia
- ROAS: Y x (Standard) / Z x (Incremental)
- CPA: R$W (alvo: R$V)
- Vencedor identificado: {criativo + metricas}
- Tempo de validacao: {N dias}

### Metodo recomendado
{ABO/CBO/Oxigenio/Horizontal/Multi-account}
Justificativa: {por que}

### Cronograma
| Dia | Acao | Budget | KPI alvo |
|---|---|---|---|
| 1 | Validar | R$X | ROAS Yx |
| 2 | +20% | R$1.2X | ROAS Yx +-10% |

### Metricas de abandonar plano
- CPA subir >40% por 2 dias consecutivos -> HOLD + investigar
- ROAS cair <50% do alvo -> reverter pro budget anterior
- Frequencia >7 sem novas vendas -> lateralizar antes de continuar

### Proxima checagem
Daqui {N} dias. Metricas a checar: {lista}
```

Salvar em `05_WORKSPACE/clientes/<cliente>/_relatorios/<YYYY-MM-DD>-plano-escala.md`.

## Tratamento de erros

| Erro | Causa provavel | Acao |
|---|---|---|
| Sem vencedor identificado | Ainda nao validou nenhum criativo/campanha | Abortar, redirecionar pra validacao primeiro |
| Dados de ROAS Incremental indisponiveis | `@attribution-auditor` nao configurado ainda | Usar so Standard ROAS, marcar limitacao no relatorio |

## Confirmacao antes de acoes destrutivas/reais

Qualquer aumento de budget acima de 20% ou duplicacao de adset/campanha e uma mudanca real de investimento do cliente: **nunca executar automaticamente** — apresentar o plano, pedir confirmacao explicita, so entao instruir a execucao (via CLI ou manual no Ads Manager).

## Handoff

- `@scaling-strategist` -> `@creative-analyst`: gerar lateralizacoes pra metodo Oxigenio.
- `@scaling-strategist` -> `meta-dr-specialist`: executar o plano de escala aprovado.

## Referencias

- Agente: `11_TRAFFIC_STACK/agents/scaling-strategist.md`
- Diretriz: `04_DIRETRIZES/traffic-diretrizes.md`
- Gate: `00_OS/gates.md#gate-traffic`
