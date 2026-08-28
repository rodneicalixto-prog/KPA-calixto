# Composio Rube — 1000+ apps em 1 install

> ⚠️ **Rube (rube.app) foi descontinuado pela Composio** (confirmado em 2026-08-27: `rube.app` para de resolver DNS, e o link que a Composio manda agora e `composio.dev/?utm_source=rube-deprecation&utm_campaign=shutdown`). O caminho atual e ativar o **connector Composio nativo do claude.ai** (Settings -> Connectors), nao mais `claude mcp add --transport http rube ...`. Esse connector ja aparece `Connected` automaticamente em qualquer sessao da conta, sem precisar rodar comando nenhum no terminal.
>
> **O que fazer agora:**
> 1. No claude.ai (ou no app Claude Desktop), va em Settings -> Connectors.
> 2. Ative/confirme o connector **Composio**, se ainda nao estiver ativo.
> 3. Ele fica disponivel em qualquer sessao Claude Code/Desktop da mesma conta — nao precisa reconfigurar por projeto.
> 4. **Confirmado em uso real (2026-08-27):** o connector novo funciona por busca dinamica sobre 500+ apps via **`COMPOSIO_SEARCH_TOOLS`** (nao `RUBE_SEARCH_TOOLS`) e `COMPOSIO_MANAGE_CONNECTIONS` pra ver/gerenciar contas conectadas. Ele nao lista todas as tools de uma vez — retorna as certas conforme a tarefa que voce descrever (ex: "buscar ferramentas do Gmail pra enviar email"). Pra ver o que ja esta conectado: peca `Lista as ferramentas disponiveis do connector Composio`.
>
> O restante deste arquivo documenta o setup **antigo** (`rube.app` direto via `claude mcp add`, comandos `RUBE_*`), mantido so como referencia historica — os comandos `RUBE_*` abaixo devem ser lidos como `COMPOSIO_*` no connector atual, mas nao foram todos confirmados 1:1.

## Por que Rube primeiro (historico — nao usar mais)

- 1 instalacao = 1000+ apps disponiveis sob demanda.
- OAuth gerenciado pela Composio (token nao vive no kit).
- Tools sob demanda via `RUBE_SEARCH_TOOLS` (nao polui contexto).
- Atualizado constantemente, suporta protocolos novos.

## Setup

### Passo 1 — Conta na Composio

1. Acessa https://rube.app
2. Cria conta (gratuita pra comecar).
3. Conecta 1-3 apps que voce ja usa (Gmail / Drive / Slack / Notion / etc.).

### Passo 2 — Adicionar MCP no Claude Code

```bash
# Adiciona o MCP do Rube
claude mcp add --transport http rube https://rube.app/mcp
```

OU editar `~/.claude.json` manualmente:

```json
{
  "mcpServers": {
    "rube": {
      "type": "http",
      "url": "https://rube.app/mcp"
    }
  }
}
```

### Passo 3 — Validar

```bash
claude mcp list
```

Espera ver `rube` listado.

Dentro do Claude Code, pede:

```text
Lista as ferramentas disponiveis no Rube
```

Claude vai usar `RUBE_SEARCH_TOOLS` pra mostrar.

### Passo 4 — Conectar app especifico

A primeira vez que o Claude tentar usar (ex: enviar email), ele chama `RUBE_MANAGE_CONNECTIONS` que abre URL de OAuth no browser. Voce loga, autoriza, pronto.

## Apps cobertos (selecao)

| Categoria | Apps |
|---|---|
| Produtividade | Notion, Asana, Linear, ClickUp, Trello, Monday |
| Comunicacao | Slack, Microsoft Teams, Discord, Telegram |
| Email | Gmail, Outlook, ProtonMail |
| Storage | Google Drive, Dropbox, OneDrive |
| Social | X/Twitter, LinkedIn, Instagram (postagem), Facebook (postagem) |
| Vendas/CRM | HubSpot, Salesforce, Pipedrive, Close |
| Dev | GitHub, GitLab, Jira |
| Calendar | Google Calendar, Outlook Calendar, Calendly |
| Design | Figma, Canva |
| Analytics | Google Analytics, Mixpanel, Posthog |

Lista completa: https://composio.dev/integrations

## Comandos Rube via Claude Code

Dentro do Claude Code, qualquer um destes funciona:

```text
RUBE_SEARCH_TOOLS                    # busca tool especifico (ex: "send slack message")
RUBE_GET_TOOL_SCHEMAS                # schema completo de tool antes de chamar
RUBE_MULTI_EXECUTE_TOOL              # executa 1 ou mais tools em paralelo
RUBE_MANAGE_CONNECTIONS              # cria/atualiza conexao OAuth
RUBE_CREATE_UPDATE_RECIPE            # cria receita reutilizavel
RUBE_EXECUTE_RECIPE                  # roda receita salva
RUBE_FIND_RECIPE                     # busca receita
RUBE_MANAGE_RECIPE_SCHEDULE          # agenda receita (cron)
RUBE_REMOTE_BASH_TOOL                # bash isolado pra processamento
RUBE_REMOTE_WORKBENCH                # ambiente isolado pra dev
RUBE_WAIT_FOR_CONNECTIONS            # poll ate OAuth concluir
```

## Casos de uso comuns

### Enviar email pelo Gmail

```text
Me ajuda a mandar um email pro cliente X pelo Gmail conectado no Rube,
assunto "Proposta semanal", corpo "[texto da proposta]"
```

Claude vai:
1. `RUBE_SEARCH_TOOLS gmail send`
2. Validar conexao Gmail
3. Pedir confirmacao
4. Enviar

### Atualizar deal no HubSpot

```text
Pega o deal "Empresa X" no HubSpot e atualiza estagio pra "Proposta Enviada"
```

### Postar no LinkedIn

```text
Posta no meu LinkedIn esse texto: [texto]. Confirma antes de postar.
```

### Criar receita automatica

```text
Cria uma receita Rube: toda segunda-feira as 9h, gera resumo dos deals do HubSpot
da semana e manda pro meu Slack canal #vendas.
```

## Seguranca

- **OAuth via browser, sempre.** Composio nunca pede token no chat.
- **Tokens ficam no Composio**, nao no `.env` do kit.
- **Permissoes granulares.** Voce pode revogar acesso a app especifico sem desconectar tudo.
- **Audit log**: https://app.composio.dev/audit-logs

## Limitacoes

- Action que custa dinheiro (anuncios pagos, transferencia bancaria) **sempre pede confirmacao no Claude Code**.
- Action que afeta cliente direto (envio massivo, post publico) **sempre pede confirmacao**.
- Read-only roda full-auto. Write/delete pede confirmacao.

## Troubleshooting

| Problema | Solucao |
|---|---|
| `rube` nao aparece em `claude mcp list` | Reiniciar Claude Code |
| OAuth nao abre browser | Copiar URL do terminal e abrir manual |
| Tool retorna 401 | Token expirou — `RUBE_MANAGE_CONNECTIONS` reautentica |
| Action falha "permission denied" | Re-autorizar com escopo correto |

## Referencias

- https://rube.app
- https://docs.composio.dev
- https://github.com/composiohq/composio
