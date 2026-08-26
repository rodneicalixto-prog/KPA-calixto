# Playbook de Funil VSL

## Objetivo

Diagnosticar a passagem `anuncio -> pagina -> reprodução -> oferta -> checkout -> compra`, conectando retenção do vídeo à economia do funil.

## Eventos esperados

`page_view`, `video_start`, `video_25`, `video_50`, `video_75`, `offer_reveal`, `cta_click`, `checkout`, `purchase`.

O player e o analytics devem usar a mesma versão da VSL e registrar dispositivo, origem e timestamp sem expor dados pessoais.

## Métricas principais

| Etapa | Métrica |
|---|---|
| Página para vídeo | `video_start / page_view` |
| Retenção | marcos 25%, 50% e 75% sobre `video_start` |
| Exposição à oferta | `offer_reveal / video_start` |
| Resposta ao CTA | `cta_click / offer_reveal` |
| Checkout | `checkout / cta_click` |
| Compra | `purchase / checkout`, CPA e ROAS |

## Sequência operacional

1. Validar eventos e o timestamp real de revelação da oferta/CTA.
2. Comparar coortes por criativo, dispositivo, página e versão da VSL.
3. Localizar a maior perda antes de avaliar copy ou oferta.
4. Inspecionar retenção ao redor de hook, mecanismo, prova, oferta e CTA.
5. Separar falha de reprodução/carregamento de abandono intencional.
6. Relacionar retenção com compra: maior consumo não implica melhor conversão automaticamente.
7. Definir um teste por hipótese, com janela e critério de interrupção.

## Árvore de decisão

- **Poucos starts:** revisar carregamento, autoplay, thumbnail e congruência do topo.
- **Queda antes do mecanismo:** encurtar contexto e tornar a tensão específica mais cedo.
- **Queda na prova:** revisar credibilidade, relevância e sequência, sem criar claims.
- **Oferta vista, CTA pouco clicado:** revisar valor, risco, clareza e transição para ação.
- **CTA clicado, compra baixa:** investigar checkout, pagamento, preço e confiança.
- **Retenção impossível/inconsistente:** corrigir instrumentação antes de editar a VSL.

## Saída obrigatória

- curva de retenção e eventos de negócio na mesma linha do tempo;
- gargalo primário e segmentos afetados;
- trechos candidatos a teste por timestamp;
- hipótese e mudança mínima proposta;
- CPA/ROAS e guardrails de qualidade;
- próxima leitura com responsável.

## Guardrails

- Não usar retenção isolada como sinal de receita.
- Não inventar depoimentos, provas ou resultados.
- Não publicar nova VSL nem trocar orçamento sem aprovação.
- Preservar a versão anterior e documentar rollback.

