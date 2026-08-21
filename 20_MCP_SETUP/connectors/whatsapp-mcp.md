# WhatsApp MCP — verygoodplugins/whatsapp-mcp

> MCP nativo pra WhatsApp Web. Le mensagens, envia, gerencia conversas — direto do Claude Code.

## Por que esse e nao o do Rube

- WhatsApp do Rube cobre WhatsApp Business API (precisa empresa verificada, App Review, $$$).
- `verygoodplugins/whatsapp-mcp` usa WhatsApp Web (qualquer numero pessoal funciona).
- Ideal pro mentorado: SDR pessoal, atendimento de loja pequena, gestao de WhatsApp comercial sem API oficial.

## Pre-requisito

- WhatsApp Web funcional no celular (versao recente do app).
- Numero comercial dedicado (recomendado — nao usar pessoal).

## Setup

### Passo 1 — Clone e instalar

```bash
# Onde voce gosta de manter ferramentas externas
cd ~/mcps
git clone https://github.com/verygoodplugins/whatsapp-mcp.git
cd whatsapp-mcp
npm install
```

OU via NPM (se publicado):

```bash
npm install -g @verygoodplugins/whatsapp-mcp
```

### Passo 2 — Adicionar no Claude Code

```bash
claude mcp add whatsapp --command "node /caminho/pra/whatsapp-mcp/index.js"
```

OU em `~/.claude.json`:

```json
{
  "mcpServers": {
    "whatsapp": {
      "command": "node",
      "args": ["/caminho/pra/whatsapp-mcp/index.js"]
    }
  }
}
```

### Passo 3 — Primeiro login

```bash
claude mcp list
```

Da pra ver `whatsapp`. Agora dentro do Claude Code:

```text
whatsapp_qr
```

Vai aparecer um QR Code no terminal. No celular:
1. Abre WhatsApp
2. Menu → Aparelhos conectados → Conectar aparelho
3. Aponta camera pro QR

Conectado.

### Passo 4 — Validar

```text
whatsapp_list_chats
```

Espera ver suas conversas listadas.

## Tools disponiveis

| Tool | O que faz |
|---|---|
| `whatsapp_qr` | Gera QR pra conectar dispositivo |
| `whatsapp_list_chats` | Lista conversas ativas |
| `whatsapp_get_messages` | Le mensagens de uma conversa |
| `whatsapp_send_message` | Envia mensagem texto |
| `whatsapp_send_image` | Envia imagem |
| `whatsapp_send_document` | Envia documento |
| `whatsapp_get_contact` | Detalhes de contato |
| `whatsapp_search` | Busca em conversas |

## Casos de uso

### SDR automatizado (com fluxos do `12_WHATSAPP_STACK/`)

```text
Le as ultimas 20 mensagens nao lidas no WhatsApp.
Pra cada lead novo, classifica usando o framework do sdr-attendant.md.
Me lista os qualificados pra eu responder.
```

### Follow-up de propostas

```text
Pega o relatorio de propostas enviadas no HubSpot (via Rube).
Pra cada lead sem resposta ha +3 dias, monta mensagem de follow-up
seguindo `15_PRODUCT_RELEASE/whatsapp/fluxos/follow-up-vendas.md`.
Me mostra rascunho antes de enviar.
```

### Triagem de atendimento

```text
Le mensagens novas no WhatsApp.
Pra cada uma:
- e duvida tecnica? → encaminhar resposta padrao
- e pedido de orcamento? → marca como lead, encaminha pro humano
- e cliente reclamando? → ALERTA, escala imediatamente
```

## Seguranca

- **Numero comercial separado.** NAO usar pessoal. Risco de banimento por uso intensivo.
- **Sem disparo em massa automatico.** WhatsApp pode banir conta. Sempre confirmacao manual antes de cada envio em lote.
- **Backup da sessao.** O MCP guarda sessao em arquivo local. Backup regular.
- **2 fatores ativos** na conta WhatsApp.

## Limitacoes

- WhatsApp Web tem rate limit. Aprox **20 mensagens/min** sustentavel sem flag.
- Mensagens automatizadas devem parecer humanas (variar tom, esperar segundos entre).
- Nao usar pra spam ou prospeccao fria sem permissao — viola TOS.

## Troubleshooting

| Problema | Solucao |
|---|---|
| QR expira | Gera novo: `whatsapp_qr` |
| Sessao caiu | Re-scan QR |
| Conta banida | NAO ha como reverter. Usar numero novo + ser mais conservador |
| Envio falha | Verificar se WhatsApp do celular esta online (precisa estar) |

## Referencias

- https://github.com/verygoodplugins/whatsapp-mcp
- Se mentorado precisar WhatsApp Business API oficial, usar Composio Rube (`connectors/composio-rube.md`).
