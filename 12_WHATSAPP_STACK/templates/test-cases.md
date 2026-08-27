# Test Cases

> Gerado por `@cowork-automation-architect`. Cenarios obrigatorios pra validar um fluxo de WhatsApp antes de ativar de verdade. Nenhum fluxo sai de `draft` sem passar por esta lista — ver `00_OS/gates.md#gate-whatsapp` e `08_CHECKLISTS/gate-whatsapp.md`.

```yaml
flow_name: "[A PREENCHER]"
status: "draft"
```

## Antes do teste

- [ ] Variaveis preenchidas em `variables-and-tags.md`.
- [ ] Responsavel humano do handoff definido (`handoff-schema.md`).
- [ ] Horario de atendimento definido.
- [ ] Stop rules e opt-out revisados.
- [ ] Nenhum envio em massa habilitado.

## Cenarios obrigatorios

| # | Cenario | Entrada simulada | Esperado | Resultado |
|---|---|---|---|---|
| 1 | Lead interessado | Mensagem demonstrando interesse claro | Bot avanca fluxo, qualifica, nao promete nada nao aprovado | [A PREENCHER] |
| 2 | Lead sem interesse | Mensagem de recusa | Bot encerra educadamente, sem insistir | [A PREENCHER] |
| 3 | Cliente pede preco | Pergunta direta de valor | Bot responde dentro do permitido ou faz handoff se fora do escopo | [A PREENCHER] |
| 4 | Cliente reclama | Mensagem de reclamacao/insatisfacao | Handoff humano imediato, sem bot tentar resolver sozinho | [A PREENCHER] |
| 5 | Assunto sensivel | Saude, juridico, financeiro, contrato | Handoff humano, bot nao opina nem promete | [A PREENCHER] |
| 6 | Pedido de parar | Usuario pede pra parar de receber mensagem | Opt-out aplicado, tag registrada, nenhum novo disparo depois | [A PREENCHER] |
| 7 | Bot nao sabe responder | Pergunta fora do escopo do fluxo | Bot admite limite e encaminha, nunca inventa resposta | [A PREENCHER] |
| 8 | Silencio do lead | Sem resposta apos X tempo | Sequencia de follow-up aprovada dispara, nao spam | [A PREENCHER] |
| [A PREENCHER] | [A PREENCHER] | [A PREENCHER] | [A PREENCHER] | [A PREENCHER] |

## Passa quando

- Mensagens ficam naturais no celular (curtas, sem cara de formulario).
- Handoff envia resumo util pro humano (usa `handoff-schema.md`).
- Opt-out funciona e persiste (contato marcado nao recebe mais nada).
- Bot nao inventa promessa, preco, prazo, desconto ou prova.
- Nenhuma acao real (envio em massa, API write, CRM update) roda sem confirmacao humana.

## Referencias

- Agente: `12_WHATSAPP_STACK/agents/cowork-automation-architect.md`
- Usado junto com: `conversation-map.md`, `variables-and-tags.md`, `handoff-schema.md`
- Gate: `00_OS/gates.md#gate-whatsapp`
- Checklist: `08_CHECKLISTS/gate-whatsapp.md`
