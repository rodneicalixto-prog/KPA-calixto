# Setup de WhatsApp | Kit Piloto Automático com IA

> Guia rápido pra conectar seu WhatsApp e ativar o primeiro fluxo automático de atendimento.

## O que você vai fazer

1. Conectar seu número de WhatsApp ao Claude Code (via MCP).
2. Desenhar o primeiro fluxo (prospecção, SDR, sucesso ou follow-up).
3. Testar em modo rascunho antes de ativar de verdade.

## Passo 1 — Conectar o WhatsApp (2 min)

O kit usa o WhatsApp Web via MCP (não precisa de conta comercial verificada nem aprovação da Meta).

1. Tenha o WhatsApp funcionando no seu celular (recomendado: número comercial dedicado, não o pessoal).
2. No terminal, dentro da pasta do kit, rode:

```bash
claude mcp add whatsapp -- node ~/mcps/whatsapp-mcp/index.js
```

Se ainda não instalou o conector, o passo a passo completo (clone do repositório, instalação) está em `20_MCP_SETUP/connectors/whatsapp-mcp.md`.

3. Confirme que conectou: `claude mcp list` deve mostrar `whatsapp` ativo.

## Passo 2 — Ativar o fluxo de atendimento (5 min)

Dentro do Claude Code (ou no Claude Desktop, digitando a palavra-chave), diga:

```text
whatsapp system
```

ou

```text
criar fluxo de whatsapp pra [prospecção / SDR / sucesso do cliente / follow-up]
```

Isso aciona o comando `/whatsapp-system` (`00_OS/commands/whatsapp-system.md`), que:

- lê o contexto do seu negócio;
- desenha o fluxo (objetivo, estados, handoff humano, stop rules);
- entrega tudo em modo **`draft`** — nada roda de verdade ainda.

## Passo 3 — Testar antes de ativar

Todo fluxo novo precisa passar pelo checklist antes de virar realidade:

- `12_WHATSAPP_STACK/templates/test-cases.md` — cenários obrigatórios (lead interessado, reclamação, pedido de parar, etc.).
- `00_OS/gates.md` (seção `GATE-WHATSAPP`) — critérios de aprovação.

Só depois de passar no teste é que você confirma a ativação real (disparo de mensagem, automação rodando sozinha).

## Problemas comuns

| Sintoma | Solução |
|---|---|
| `whatsapp` não aparece em `claude mcp list` | Reinicie o Claude Code; confira se o `node` do comando aponta pro caminho certo do `whatsapp-mcp/index.js` |
| QR Code não aparece / expira rápido | Feche e reabra o WhatsApp Web no celular; tente de novo |
| Mensagem não chega no destino | Confirme que o número de teste está salvo nos contatos e que o WhatsApp Web está com sessão ativa |
| Fluxo "trava" e não sabe responder | Normal em rascunho — ajuste o `conversation-map.md` do fluxo e rode o teste de novo |

## Próximo passo

Depois do primeiro fluxo funcionando, veja `12_WHATSAPP_STACK/README.md` pra conhecer os outros bots (prospecção, SDR, sucesso, follow-up, docs Cowork).
