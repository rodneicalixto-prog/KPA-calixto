# Conversation Map — NEY (bot de vendas Terra Fibra)

> Status: **draft**. Nao ativar disparo real nem integrar ao numero comercial sem confirmacao explicita de Rodnei. Gerado porque `whatsapp_status` estava `nao_mapeado_neste_workspace` mesmo com a copy e as 3 primeiras perguntas ja aprovadas em `meta-change-set-draft.json`.

```yaml
flow_name: "ney-triagem-cobertura"
owner_bot: "NEY"
goal: "Confirmar rapido se o lead esta dentro das 21 cidades cobertas, sem prometer cobertura antes da validacao por endereco, e encaminhar so os leads com fit real pro humano"
entry_points:
  - "clique no anuncio 'CS | Cobertura validada | WhatsApp | v1' (ou no conjunto ativo no momento)"
success_states:
  - "lead_qualificado_encaminhado"
handoff_states:
  - "lead_qualificado_encaminhado"
  - "duvida_fora_do_escopo"
stop_states:
  - "fora_de_area_encerrado"
  - "opt_out"
```

## Por que este fluxo existe

`lead-quality.md` mostra 8 de 9 conversas (88,89%) classificadas como "fora de area" entre 24/08 e 26/08/2026. O problema nao e so segmentacao no Meta (que ja tem correcao aprovada e bloqueada em `meta-change-set-draft.json`) — e tambem o bot nunca filtrou por localizacao antes de prosseguir. Este fluxo aplica a pergunta de cidade/bairro/CEP **logo na primeira mensagem**, que ja era a especificacao aprovada por Rodnei (`whatsapp.first_questions` no change set), so que nunca virou um fluxo de verdade.

## Estados

| Estado | Entrada | Mensagem/acao | Proxima transicao | Tags | Handoff? |
|---|---|---|---|---|---|
| `boas_vindas_triagem` | lead clicou no anuncio e abriu o WhatsApp | "Olá! Pra eu confirmar se a Terra Fibra atende seu endereço, me envie:\n\n1. Cidade\n2. Bairro\n3. CEP\n\nNão precisa enviar número da casa neste primeiro contato." (copy ja aprovada) | `aguardando_localizacao` | `entrada` | nao |
| `aguardando_localizacao` | lead respondeu (total ou parcialmente) | Se faltou cidade, bairro ou CEP: pedir só o que falta, uma vez. Se passar 24h sem resposta completa: aplicar sequencia de follow-up (ver `04_DIRETRIZES/whatsapp-diretrizes.md`), maximo 2 tentativas | `checar_cidade` ou `sem_resposta` | `aguardando_dado` | nao |
| `checar_cidade` | cidade informada | Comparar contra a lista de `coverage.md` (21 cidades, `exemplos/familias`... nao, usar `05_WORKSPACE/clientes/terra-fibra/coverage.md`). Match exato (sem homonimo de outro estado) -> `dentro_da_area`. Sem match -> `fora_de_area` | `dentro_da_area` / `fora_de_area` | `cidade_verificada` | nao |
| `dentro_da_area` | cidade bate com a lista de 21 | "Show! [Cidade] é uma das nossas áreas de cobertura. Só confirmando: sua cobertura real depende do endereço exato — o time vai validar o bairro/CEP que você mandou e já te retorna com o plano disponível pra sua região." | `lead_qualificado_encaminhado` | `dentro_area`, `qualificado` | sim |
| `fora_de_area` | cidade nao bate com a lista de 21 | "Nesse momento a Terra Fibra ainda não atende [Cidade]. Anotei seu interesse — se a gente expandir pra sua região, te aviso por aqui. Obrigado pelo contato!" | `fora_de_area_encerrado` | `fora_area` | nao (mas registrar pra inteligencia de expansao — ver `lead-quality.md`) |
| `duvida_fora_do_escopo` | lead pergunta preço, suporte tecnico, ou algo que o bot nao deve responder sozinho | "Essa parte eu preciso confirmar com o time — já te encaminho." | `lead_qualificado_encaminhado` | `handoff_duvida` | sim |
| `sem_resposta` | lead nao respondeu apos 2 tentativas de follow-up | Encerrar sem insistir mais. Nao contar como "sem resposta" na proxima reconciliacao sem esse status | `fora_de_area_encerrado` (arquivado) | `sem_resposta` | nao |
| `lead_qualificado_encaminhado` | dentro da area OU duvida fora do escopo | Gerar handoff (`handoff-schema.md`) com cidade/bairro/CEP e resumo pro humano (Rodnei ou quem ele designar) | fim do fluxo do bot | `handoff_enviado` | sim |
| `opt_out` | lead pede pra parar em qualquer momento | Aplicar stop imediato, nao enviar mais nenhuma mensagem automatica pro contato | fim do fluxo | `opt_out` | nao |

## Regras de fallback

- Se a cidade informada nao aparecer clara ou for ambigua (ex: nome de bairro em vez de cidade), pedir clarificacao curta uma unica vez antes de decidir dentro/fora.
- Se o lead pedir humano a qualquer momento: handoff imediato, sem insistir na triagem automatica.
- Se o assunto for sensivel (reclamacao, problema tecnico grave, cobranca): handoff imediato, pular a triagem de cidade se ja tiver sido feita.
- Se o lead pedir pra parar (`para`, `sair`, `descadastrar`): aplicar `opt_out` e nunca mais disparar mensagem automatica pro contato.
- Nunca prometer cobertura fechada so pela cidade bater com a lista — a validacao final e por endereco (geolocalizacao), como definido em `coverage.md`.
- Nunca inventar prazo de instalacao, preco ou disponibilidade que o time nao confirmou.

## Referencias

- Copy e primeiras perguntas ja aprovadas: `05_WORKSPACE/clientes/terra-fibra/meta-change-set-draft.json` (chave `whatsapp`) e `06_OUTPUTS/terra-fibra/traffic/execucao-manual-meta-checklist.md` (secao 4).
- Lista de cidades cobertas: `05_WORKSPACE/clientes/terra-fibra/coverage.md`.
- Agente de referencia: `12_WHATSAPP_STACK/agents/prospecting-bot.md` (triagem) e `12_WHATSAPP_STACK/agents/sdr-attendant.md` (qualificacao).
- Skill: `12_WHATSAPP_STACK/skills/whatsapp-conversation-design/SKILL.md`.
- Gate: `00_OS/gates.md#gate-whatsapp`.
