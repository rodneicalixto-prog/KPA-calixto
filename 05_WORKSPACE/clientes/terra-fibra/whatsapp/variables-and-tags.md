# Variables and Tags — NEY (Terra Fibra)

> Status: draft. Sem token/credencial aqui.

```yaml
flow_name: "ney-triagem-cobertura"
owner_bot: "NEY"
```

## Variaveis de memoria

| Variavel | Tipo | Preenchida por | Obrigatoria | Descricao |
|---|---|---|---|---|
| lead_cidade | string | usuario | sim | Cidade informada na triagem |
| lead_bairro | string | usuario | sim | Bairro informado |
| lead_cep | string | usuario | sim | CEP informado |
| area_status | enum | bot | sim | `dentro` \| `fora` \| `ambiguo` — resultado do match contra `coverage.md` |
| tentativas_followup | int | bot | nao | Contador de tentativas de follow-up por falta de resposta (max 2) |
| origem_anuncio | string | sistema | nao | Nome do anuncio/conjunto de origem, quando disponivel |

## Tags/segmentos

| Tag | Quando aplicar | Usada por |
|---|---|---|
| `dentro_area` | Cidade bate com uma das 21 cidades de `coverage.md` | handoff, relatorio |
| `fora_area` | Cidade nao bate com a lista — usar pra alimentar `lead-quality.md` e decisao futura de expansao | relatorio de expansao |
| `qualificado` | Dentro da area + dados completos | SDR/handoff |
| `handoff_duvida` | Pergunta fora do escopo do bot (preco fechado, suporte tecnico, reclamacao) | handoff |
| `sem_resposta` | 2 tentativas de follow-up sem retorno | reativacao/relatorio |
| `opt_out` | Pediu pra parar | bloqueia qualquer novo disparo |

## Regras

- Nenhuma variavel guarda numero de casa na primeira interacao (regra ja aprovada no change set: `request_house_number_initially: false`).
- `area_status = fora` nunca e tratado como erro do lead — e sinal de segmentacao ainda ampla demais no Meta (ver `lead-quality.md`), deve alimentar decisao de negocio, nao ser descartado.
- `opt_out` sempre bloqueia qualquer novo disparo automatico pro contato, permanentemente.

## Referencias

- Agente: `12_WHATSAPP_STACK/agents/prospecting-bot.md`, `12_WHATSAPP_STACK/agents/sdr-attendant.md`
- Cobertura: `05_WORKSPACE/clientes/terra-fibra/coverage.md`
- Gate: `00_OS/gates.md#gate-whatsapp`
