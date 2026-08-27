# Task: Analisar Criativos via CLI Nativo

> Task usada por `@creative-analyst` e `@traffic-orchestrator` quando o usuário pede analise de performance de criativos, DNA do vencedor, lateralizacao ou kill list. Conecta o CLI `meta` nativo aos frameworks de `@creative-analyst`.

## Quando esta task e executada

- `*criativos [janela]` em `@traffic-orchestrator`
- `*analise`, `*dna`, `*lateralizar [ID]`, `*kill-creative`, `*hook-retention [ID]`, `*scatter` em `@creative-analyst`

## Pre-requisitos (validar antes de executar)

1. **Cliente carregado** — `05_WORKSPACE/clientes/<cliente>/CLAUDE.md` lido
2. **`act_id` resolvido** — via `05_WORKSPACE/clientes/<cliente>/act-mapping.yaml`
3. **CLI `meta` funcionando** — `meta auth status` retorna `Authenticated`
4. **Janela definida** — default `last_14d` (criativos precisam de massa estatistica, nao usar `last_7d` como em diagnostico geral)

Se algum falhar, ABORTAR com mensagem clara. Nao inventar dados.

## Pipeline de execucao

### Etapa 1 — Listar ads ativos

```powershell
meta ads ad list `
  --ad-account-id act_<ID> `
  --filter "effective_status=ACTIVE" `
  -o json
```

**Parsear:** lista de ads com `id`, `name`, `adset_id`, `creative_id`.

### Etapa 2 — Insights por ad (nivel `ad`, janela definida)

```powershell
meta ads insights get `
  --ad-account-id act_<ID> `
  --date-preset last_<N>d `
  --level ad `
  --fields spend,impressions,clicks,ctr,actions,action_values,purchase_roas,video_thruplay_watched_actions,video_p25_watched_actions,video_p75_watched_actions,cost_per_action_type `
  -o json
```

**Filtrar:** `impressions >= 1000` (regra do agente — abaixo disso nao tem significancia estatistica).

**Calcular:**
- `hook_rate = video_thruplay_watched_actions / impressions` (bom: >25%, otimo: >35%)
- `retention_25 = video_p25_watched_actions / video_thruplay_watched_actions`
- `retention_75 = video_p75_watched_actions / video_p25_watched_actions` (bom: >40%, otimo: >55%)

**Sortear:** ROAS desc, CPA asc.

### Etapa 3 — `*analise`: Top 10 vencedores + Top 10 perdedores

Tabela: `ad_id | nome | spend | impr | hook_rate | retention_25 | retention_75 | CTR | CPA | ROAS`.

### Etapa 4 — `*dna`: aplicar framework "DNA do Vencedor — 5 Camadas"

1. Rodar Etapa 3 (top 10 vencedores).
2. Para cada vencedor, puxar creative: `meta ads creative get {creative_id}`.
3. Classificar cada um nas 5 camadas do agente: `hook_0_3s`, `pattern_interrupt`, `body_problema_solucao`, `cta_estrutura`, `formato`.
4. Identificar padrao comum entre os vencedores (minimo 3 vencedores estatisticamente significativos — abaixo disso, nao concluir DNA).
5. Output: tabela DNA + conclusao estrutural (ex: "DNA do vencedor = ROSTO em 0-3s + texto pergunta + estrutura problema/solucao + CTA indireto").

### Etapa 5 — `*lateralizar [ID]`: gerar briefings de variacao genuina

1. Puxar creative do ID via CLI.
2. Aplicar framework "Lateralizacao Genuina (nao fake)" — distinguir fake (mesmo video em ratio diferente, so cor do botao) de genuina (mesmo hook/body diferente, mesma estrutura/angulo diferente, etc).
3. Gerar 5-10 briefings, formato: `LATERAL #1: Manter HOOK '{hook_vencedor}', trocar BODY pra storytelling 1a pessoa`.
4. Output: briefing pra Production Lead / `@designer` (squad oficial) — nunca produzir o asset aqui, so o briefing.

### Etapa 6 — `*kill-creative`: aplicar Kill Criteria

Marcar como candidato a pausa qualquer ad que bata **qualquer um** destes triggers:

- Hook rate <15% por 3 dias consecutivos com R$200+ gasto.
- Retention 25% <30% (audiencia fugindo cedo).
- Frequencia >7 sem nova venda nos ultimos 7 dias.
- CPA 2x+ acima do alvo do cliente por 5 dias.
- ROAS <50% do alvo por 7 dias.

Alerta amarelo (nao mata ainda, mas monitora): hook rate caindo 30%+ semana-a-semana, frequencia subindo + CTR caindo, CPA subindo 50%+ semana-a-semana.

### Etapa 7 — `*scatter`: matriz de decisao

Plotar (ou descrever em tabela se nao houver renderizacao grafica): eixo X hook rate, eixo Y retention 25%, tamanho = spend, cor = CPA vs alvo. Classificar cada ad num quadrante (Q1 vencedor, Q2 hook bom/conteudo fraco, Q3 conteudo bom/hook fraco, Q4 matar).

### Etapa 8 — Cruzar com baseline e salvar

Carregar `05_WORKSPACE/clientes/<cliente>/baseline-kpis.md` para comparar CPA/ROAS/CTR contra o alvo do cliente (nunca benchmark generico).

Salvar:
- Markdown: `05_WORKSPACE/clientes/<cliente>/_relatorios/<YYYY-MM-DD>-criativos.md`
- JSON cru: `05_WORKSPACE/clientes/<cliente>/_relatorios/_raw/<YYYY-MM-DD>-creative-insights.json`

## Tratamento de erros

| Erro CLI | Causa provavel | Acao |
|----------|----------------|------|
| `Invalid OAuth access token` | Token expirou | Orientar `meta auth login` |
| `Empty response` | Janela sem dados (ads pausados antes) | Reportar; sugerir janela maior |
| Menos de 3 vencedores com significancia | Conta nova ou pouco spend | Nao concluir DNA — reportar gap, sugerir aguardar mais dados |

**NUNCA** inventar hook rate ou retention quando o dado nao esta disponivel (ex: `fb_ad_preview` com API limitada) — reportar como `sem_dado`.

## Confirmacao antes de acoes destrutivas

`*kill-creative` so **lista** candidatos a pausa. Pausar de fato segue a mesma regra do diagnostico geral: nunca executar automaticamente, listar, pedir confirmacao explicita (`Confirma pausar [N] ads? (s/n)`), so entao rodar `meta ads ad update <AD_ID> --status PAUSED`.

## Handoff

- `@creative-analyst` -> `Production Lead` / `@designer`: briefings de lateralizacao (Etapa 5).
- `@creative-analyst` -> `@scaling-strategist`: vencedores validados prontos pra escalar.

## Logs

Apendice em todo relatorio: comandos executados, tempo total, registros retornados (N ads analisados, M com significancia estatistica).

## Referencias

- Agente: `11_TRAFFIC_STACK/agents/creative-analyst.md`
- Diretriz: `04_DIRETRIZES/traffic-diretrizes.md`
- Gate: `00_OS/gates.md#gate-traffic`
- Skill de apoio: `11_TRAFFIC_STACK/skills/direct-response-br/SKILL.md`
