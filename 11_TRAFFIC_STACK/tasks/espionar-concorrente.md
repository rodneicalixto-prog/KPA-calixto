# Task: Espionar Concorrente (Inteligencia Competitiva)

> Task usada por `@competitor-spy` e `@traffic-orchestrator` quando o pedido envolve analisar concorrente, fazer engenharia reversa de funil, montar swipe ou levantar benchmark de nicho. Nao depende do CLI `meta` — usa fontes publicas (Meta Ad Library e similares).

## Quando esta task e executada

- `*espiar [concorrente]` em `@traffic-orchestrator`
- `*spy [concorrente]`, `*reverse-funnel [URL]`, `*swipe [nicho]`, `*benchmark [nicho]`, `*new-entrants` em `@competitor-spy`

## Pre-requisitos (validar antes de executar)

1. **Cliente carregado** — precisa do nicho pra contextualizar benchmark e relevancia.
2. **`05_WORKSPACE/clientes/<cliente>/icp.md`** lido, pra avaliar overlap real com o publico do cliente.
3. **Concorrente ou nicho identificado** — se nao vier explicito no pedido, perguntar.

Esta task nao usa credencial nenhuma do cliente (Meta Ad Library e publica) — nunca pedir login/senha de conta de concorrente.

## Pipeline de execucao

### Etapa 1 — `*spy [concorrente]`: analise de criativos rodando

1. Acessar Meta Ad Library (`https://www.facebook.com/ads/library/`) filtrando pela pagina/marca do concorrente, pais e idioma do cliente.
2. Rodar o checklist de 12 pontos do agente:
   1. Quantos criativos rodando agora?
   2. Quantos rodando ha +30 dias (vencedores estabelecidos)?
   3. Variacao genuina entre criativos ou spam da mesma coisa?
   4. Tipos de hook usados (mapear top 5, usando a taxonomia de `analisar-criativos.md`/`creative-analyst.md`)?
   5. Formatos predominantes (video cru, video editado, imagem, carrossel)?
   6. Idiomas/regioes?
   7. Estrutura do funil (ad -> LP/VSL/quiz/link direto)?
   8. Oferta principal (preco, garantia, bonus)?
   9. Upsells/orderbumps?
   10. Plataforma de checkout visivel?
   11. Tracking visivel (Pixel/CAPI/Heap/Hotjar)?
   12. Sazonalidade/cadencia de publicacao?
3. Classificar: investimento estimado (Alto/Medio/Baixo, com base em volume), sofisticacao (Profissional/Intermediario/Amador), ameaca (Alta/Media/Baixa, com base em overlap com o ICP do cliente).

### Etapa 2 — `*reverse-funnel [URL]`: engenharia reversa do funil completo

1. Pegar a URL da LP/VSL a partir do anuncio na Ad Library.
2. Acessar em navegador anonimo/incognito (sem cookies do concorrente).
3. Documentar o fluxo:
   - Hero (headline, sub-headline, hero asset).
   - Body (bullets, prova social, autoridade, garantia).
   - CTA principal (texto, cor, posicao).
   - Upsell/orderbump, se houver.
   - Pixel + ferramentas via View Source.
4. Se houver VSL: medir tempo ate o pitch e tempo total.
5. Se houver quiz: contar perguntas e tipos.
6. Iniciar o checkout **sem pagar** e documentar os steps.
7. Nunca finalizar compra nem fornecer dado real do cliente pra "testar" o funil do concorrente.
8. Compilar o swipe organizado.

### Etapa 3 — `*swipe [nicho]`: coleta e organizacao

1. Repetir Etapa 1 pra varios concorrentes do nicho (nao so um).
2. Organizar por padrao (hook, formato, oferta) — nao so empilhar prints soltos.
3. Salvar em `05_WORKSPACE/clientes/<cliente>/_swipe/<concorrente>/`.

### Etapa 4 — `*benchmark [nicho]`: benchmark de metricas

Como Meta Ad Library nao expoe CTR/CPM reais, usar fontes pt-BR (Reportana/RD Station, AppsFlyer Industry Reports, Hotmart Stats quando disponivel, comunidades de marketing pt-BR) pra estimar: CPM medio do nicho, CPL benchmark, tickets praticados, garantias praticadas (7d/14d/30d/365d). Marcar toda estimativa como estimativa, nunca apresentar como dado exato do concorrente.

### Etapa 5 — `*new-entrants`: quem esta lancando agora

Buscar na Ad Library por palavras-chave do nicho, filtrando por data de inicio recente do anuncio, pra identificar operadores novos ou lancamentos recentes.

### Etapa 6 — Output — Relatorio de Inteligencia

```markdown
## Inteligencia Competitiva — {Concorrente} | {Data}

### Resumo executivo
- Investimento estimado: {Alto/Medio/Baixo}
- Sofisticacao: {Profissional/Intermediario/Amador}
- Ameaca: {Alta/Media/Baixa}

### Analise dos criativos (Meta Ad Library)
- Total rodando hoje: {N}
- Rodando ha +30 dias (vencedores): {N}
- Top 5 hooks identificados: {lista}
- Padroes estruturais: {DNA observado}

### Engenharia reversa do funil
- Estrutura: ads -> {LP/VSL/quiz} -> {checkout/upsell}
- Oferta principal: R$X (com {bonus, garantia})
- Upsells: {sim/nao, lista}
- Tracking detectado: {Pixel ID, CAPI, GTM}

### Gaps de oportunidade (o que ELES nao fazem)
- {gap 1}
- {gap 2}

### Licoes pro cliente
- O que copiar (com adaptacao): {lista}
- O que evitar (erros deles): {lista}

### Swipe coletado
Salvo em: 05_WORKSPACE/clientes/{cliente}/_swipe/{concorrente}/
```

Salvar tambem em `05_WORKSPACE/clientes/<cliente>/_intel/<concorrente>-<data>.md`.

## Regras (do agente)

- Volume de criativos rodando = proxy de investimento/validacao, nao prova absoluta.
- Tempo no ar >30 dias = vencedor estabelecido.
- Nunca recomendar copiar criativo do concorrente literalmente — lateralizar com adaptacao, sim.
- Nunca concluir "eles vendem mais" sem dado — sao estimativas, nao certezas.
- Nunca confundir volume de criativos com qualidade da oferta.

## Tratamento de erros

| Erro | Causa provavel | Acao |
|---|---|---|
| Concorrente sem anuncios ativos na Ad Library | Pausou campanhas ou nao roda Meta Ads | Reportar; sugerir checar outras plataformas (Google, TikTok) se relevante |
| LP do concorrente fora do ar | Link antigo/expirado | Reportar como funil desatualizado, nao bloquear o resto da analise |

## Handoff

- `@competitor-spy` -> `@creative-analyst`: padroes dos vencedores concorrentes pra cruzar com o DNA proprio.
- `@competitor-spy` -> `meta-dr-specialist`: incorporar licoes no DR do cliente.
- `@competitor-spy` -> `Strategist` (squad oficial): quando o gap competitivo e estrategico, nao so tatico.
- `@competitor-spy` -> `@traffic-diagnostician` (camada 6 - Externo): quando a queda de performance e explicada por concorrencia subindo.

## Referencias

- Agente: `11_TRAFFIC_STACK/agents/competitor-spy.md`
- ICP do cliente: `05_WORKSPACE/clientes/<cliente>/icp.md`
- Gate: `00_OS/gates.md#gate-traffic`
