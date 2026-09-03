# SDR Planos de Saude - SPIN Audio V3 — correcoes + incidente de loop (2026-09-02)

Workflow n8n: `SDR Planos de Saude - SPIN Audio V3` (id `b1GmvNZRp7tS67mK`), instancia `https://n8nopen.openwave.online`.

## Status atual

- Workflow **desativado** (`active: false`) desde 2026-09-02T02:25 UTC, apos o incidente de loop abaixo. Nao reativar sem aplicar a correcao pendente (secao "Pendente antes de reativar").
- 3 correcoes ja aplicadas e testadas com sucesso via injecao direta no webhook (execucoes com status `success`).

## Correcoes aplicadas nesta sessao

1. **`Enviar texto` respondia so pro webhook do WhatsApp, nunca pro de trafego pago.**
   `remoteJid` dependia de `$('Webhook - Evolution WhatsApp')`, que nunca executa quando o disparo vem do `Webhook - Lead Trafego Pago` — a expressao falhava e nenhuma resposta saia pra lead de anuncio. Trocado pra resolver o telefone a partir do `Motor SDR Planos` (funciona nos dois triggers).

2. **Corretor nunca era avisado.** `IF - Avisar Corretor?` e o node que mandava o resumo pro corretor estavam orfaos (desconectados do `Motor SDR Planos`) desde uma refatoracao anterior — `deveAvisarCorretor` era calculado no codigo mas nada consumia. Reconectado `Motor SDR Planos -> IF - Avisar Corretor? -> Evolution - Avisar Corretor` (node novo, mesmo tipo/credencial do `Enviar texto`).

3. **`OutputParser` (formata resposta da IA em JSON pra quebrar em varias mensagens) quebrava a execucao inteira quando o modelo devolvia algo fora do formato esperado**, sem fallback — lead ficava sem resposta nenhuma. Ativado `autoFix: true` + conectado um Model sub-node (`GPT 4.1 mini3`) no `OutputParser` (autoFix exige model proprio, nao herda do Chain).

Confirmado ponta a ponta via injecao direta no endpoint do webhook (`/webhook/sdr-planos-saude-mvp-v3`): execucao completou sem erro, com as 3 correcoes ativas.

## Incidente: loop de disparo (2026-09-02, ~02:22-02:27 UTC)

Durante o teste real com o usuario, o workflow entrou em loop: **149 execucoes em ~5 minutos** (pico de 39 execucoes num unico minuto), trocando mensagens com o numero `5511915100571`.

Evidencia (execucao `52787`, entre outras): a deteccao de eco do node `Anti-loop e Normalizar` **pegou pelo menos uma mensagem como eco do proprio bot** (`invalidReasons: ["bot-echo"]`), mas deixou passar varias outras seguidas (`valido: true`, `botEcho: false`) com `fromMe: false` — ou seja, chegavam like mensagens genuinamente recebidas, nao reconhecidas como eco.

Achado adicional que reforca a hipotese de loop bot-a-bot: o **conteudo** das mensagens trocadas nesse trecho saiu do escopo (planos de saude) e passou a mencionar "plano 500 MB" — linguagem de plano de internet, nao de saude. Combinado com a cadencia de resposta quase instantanea (varias execucoes por segundo), o cenario mais provavel e que o numero `5511915100571` tambem e uma instancia automatizada (bot), e as duas automacoes ficaram respondendo uma a outra em cascata, com o conteudo degradando a cada rodada.

Acao tomada: workflow desativado via API (`POST /api/v1/workflows/{id}/deactivate`) apos duas tentativas — a primeira reverteu sozinha porque o editor do n8n estava aberto na tela do usuario e resalvou o workflow como ativo; a segunda, com o usuario desativando manualmente pelo toggle do editor, ficou definitiva. Confirmado por 10+ minutos sem nova execucao.

## Pendente antes de reativar

1. **Reforcar a deteccao de eco em `Anti-loop e Normalizar`** — o mecanismo atual (similaridade de texto + assinatura de outbox com TTL) tem brecha comprovada. Considerar: bloquear automaticamente qualquer numero que troque mais de N mensagens num intervalo curto (circuit breaker por volume, independente de conteudo) alem da deteccao por similaridade.
2. **Confirmar se `5511915100571` e de fato outro bot** (ou pedir pro usuario confirmar a origem do numero) antes de reativar — se for outro sistema automatizado, a correcao de eco sozinha pode nao bastar; pode ser necessario um passo manual de confirmacao antes do primeiro envio pra numeros desconhecidos.
3. **Rotacionar chaves hardcoded** (Evolution API key e OpenAI key, ambas em texto plano nos nodes `Config - SDR Saude` e `Config - Trafego Pago`) e migrar pra credencial nativa do n8n. Nao rotacionado nesta sessao — acao do usuario na origem (paineis Evolution/OpenAI), nenhuma chave foi exposta neste documento.
4. Limpar nodes orfaos legados que ficaram sem uso apos as correcoes acima (`IF - Deve Responder?`, `Evolution - Responder Lead`, `Evolution - Enviar Resumo Corretor`, bloco Supabase desligado) — cosmetico, nao bloqueia reativacao.

## Nunca reativar sem

- Confirmar que o item 1 (circuit breaker de volume) foi implementado e testado.
- Confirmacao explicita do usuario pra `active: true` em producao (regra padrao do kit pra qualquer automacao real).
