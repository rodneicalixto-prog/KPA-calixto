# Token Policy

> Regras NAO-NEGOCIAVEIS pra qualquer token de qualquer MCP.

## 1. Nunca pedir token no chat

Toda autenticacao = OAuth via browser. Se um MCP exigir token manual:

- ❌ Nao colar no chat
- ❌ Nao salvar em arquivo do kit
- ✅ Salvar em `.env` local (gitignored)
- ✅ Salvar em variavel de ambiente do shell (`~/.profile`, `~/.zshrc`)
- ✅ Usar gerenciador de senhas (1Password, Bitwarden) se precisar compartilhar entre maquinas

## 2. Nunca expor em log

Se token aparecer em output do terminal ou log:

```bash
# REDIGIR com:
ACCESS_TOKEN=EAA<REDACTED>
```

Em comandos:

```bash
# Errado:
echo $ACCESS_TOKEN

# Certo:
echo "Token presente: $([ -n "$ACCESS_TOKEN" ] && echo "sim" || echo "nao")"
```

## 3. Rotacao periodica

| Token | Rotacao |
|---|---|
| Meta Ads System User Token | 60 dias |
| Composio Rube | gerenciado pela Composio (auto-refresh) |
| Slack Bot Token | 90 dias |
| GitHub PAT | 90 dias |
| Firecrawl API | 180 dias |

## 4. Escopo minimo

Cada token = so o escopo necessario.

- Slack: `chat:write` + canais especificos (NAO `admin`)
- GitHub: `repo` privado especifico (NAO `repo` global)
- Google Drive: `drive.file` em pasta especifica (NAO `drive` total)
- Meta Ads: `ads_management` + `ads_read` (NAO `business_management` se nao for usar)

## 5. Em caso de vazamento

Acoes em ordem:

1. **Revoga o token IMEDIATAMENTE** no provedor.
2. Gera token novo com escopo minimo.
3. Atualiza `.env` local.
4. Audita log de acessos do provedor pra ver se houve uso indevido.
5. Documenta o incidente em `_DONO_PRODUTO/07_LOGS/incidents.md` (so do dono, nao expor publicamente).

## 6. Checklist antes de adicionar novo MCP

- [ ] MCP usa OAuth (preferido) ou exige token manual?
- [ ] Se manual: ja tem `.env` configurado + gitignored?
- [ ] Token vai pro `.env`, nao pro kit?
- [ ] Escopo do token e o minimo necessario?
- [ ] Rotacao agendada?
- [ ] Audit log disponivel no provedor?

## 7. Permissoes destrutivas

MCPs com permissao de **write/delete/post/disparo** exigem confirmacao no Claude Code antes de cada acao:

- Slack post em canal publico
- Email enviar
- WhatsApp enviar
- Meta Ads pause/edit
- HubSpot/Salesforce update
- GitHub push/PR merge
- Drive delete

Claude pergunta antes. Mentorado confirma. Sem exceção.
