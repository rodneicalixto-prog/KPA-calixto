# Test Cases — NEY (Terra Fibra)

```yaml
flow_name: "ney-triagem-cobertura"
status: "draft"
```

## Antes do teste

- [ ] Variaveis preenchidas em `variables-and-tags.md`.
- [ ] Responsavel humano do handoff definido (Rodnei, conforme `handoff-schema.md`).
- [ ] Lista de 21 cidades de `coverage.md` carregada e correta.
- [ ] Nenhum disparo em massa habilitado.

## Cenarios obrigatorios

| # | Cenario | Entrada simulada | Esperado | Resultado |
|---|---|---|---|---|
| 1 | Lead dentro da area, dados completos | "Aguaí, Centro, 13860-000" | `area_status = dentro`, mensagem de confirmacao, handoff qualificado gerado | PASS — `boas_vindas_triagem` -> `aguardando_localizacao` (dados completos) -> `checar_cidade` (match unico com `coverage.md`) -> `dentro_da_area` -> `lead_qualificado_encaminhado` (handoff sim) |
| 2 | Lead fora da area | "Ribeirão Preto, Jardim, 14000-000" | `area_status = fora`, mensagem educada de encerramento, tag `fora_area`, sem handoff individual | PASS — "Ribeirão Preto" nao esta nas 21 cidades -> `checar_cidade` sem match -> `fora_de_area` -> `fora_de_area_encerrado`, tag `fora_area`, handoff = nao (so alimenta `lead-quality.md`) |
| 3 | Cidade homonima de outro estado | "São Pedro" sem estado, ambiguo | Bot nao assume automaticamente SP — pede clarificacao uma vez antes de decidir | PASS (apos correcao) — desk-check original achou que esse caso so existia em "regras de fallback", sem estado proprio. Corrigido: `checar_cidade` agora reconhece homonimo e vai pra `confirmar_cidade_ambigua`, que pergunta uma unica vez antes de decidir `dentro_da_area` ou `fora_de_area` |
| 4 | Dados incompletos (só cidade) | "Casa Branca" | Bot pede só o que falta (bairro e CEP), sem repetir a pergunta toda | PASS — estado `aguardando_localizacao` ja cobre isso: "pedir só o que falta, uma vez" |
| 5 | Pergunta de preço/suporte fora do escopo | "Quanto custa o plano de 1 Giga?" | Handoff imediato, tag `handoff_duvida`, bot nao inventa preço | PASS (apos correcao) — desk-check original achou que `duvida_fora_do_escopo` so disparava numa etapa fixa da tabela, sem deixar claro que interrompe QUALQUER estado (ex: lead pergunta preço antes mesmo de dar a cidade). Corrigido: entrada do estado agora diz explicitamente "em qualquer estado do fluxo" |
| 6 | Pedido de parar | "para de me mandar mensagem" | `opt_out` aplicado, nenhum novo disparo depois | PASS — estado `opt_out` ja cobria "em qualquer momento"; reforcado pra "em qualquer estado do fluxo" na correcao |
| 7 | Sem resposta apos 2 tentativas | silêncio do lead | Encerra sem insistir, tag `sem_resposta`, nao conta como handoff | PASS — estado `sem_resposta` cobre exatamente isso, handoff = nao |
| 8 | Reclamação/assunto sensível | "isso é golpe, quero cancelar" | Handoff humano imediato, bot não tenta resolver sozinho | PASS (apos correcao) — desk-check original nao achou nenhum estado nomeado pra reclamação/desconfiança (so citado em prosa nas "regras de fallback"). Corrigido: `duvida_fora_do_escopo` agora inclui explicitamente "reclamação, cita golpe/desconfiança" na entrada, com tag propria `handoff_reclamacao` e tom empatico na mensagem |

## Passa quando

- Mensagens ficam naturais no celular (curtas, sem cara de formulário).
- Bot nunca promete cobertura fechada só pela cidade bater com a lista.
- `fora_area` é tratado como dado de negócio (alimenta `lead-quality.md`), não como erro do lead.
- Handoff só acontece pra leads dentro da área ou com dúvida fora do escopo — não pra todo mundo.
- Opt-out funciona e persiste.
- Nenhuma ação real (envio em massa, integração com número comercial) roda sem confirmação humana de Rodnei.

## Referências

- Fluxo: `05_WORKSPACE/clientes/terra-fibra/whatsapp/conversation-map.md`
- Gate: `00_OS/gates.md#gate-whatsapp`
- Checklist: `08_CHECKLISTS/gate-whatsapp.md`
