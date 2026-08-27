# Guia de Referência Rápida | Kit Piloto Automático V30

## Instalação (15-20 minutos)

### Passo 1: Instalar o Node.js e o Claude Code
```bash
node --version   # precisa ser v18 ou maior; se faltar, instale em nodejs.org
npm install -g @anthropic-ai/claude-code
```

### Passo 2: Fazer login
```bash
claude login
```
Vai abrir o navegador. Faça login com sua conta Anthropic.

### Passo 3: Rodar o wizard de instalação
Dentro da pasta do kit:
```bash
cd kit-piloto-automatico-v30
claude
```
Dentro do Claude Code, digite:
```
instalar kpa30
```
Isso aciona o wizard único (`/instalar-kpa30`), que cobre em ~15-20 min: dependências, `.env`, MCPs, onboarding do seu negócio e a primeira entrega. **Não precisa copiar pasta de agente nenhuma manualmente** — os agentes, skills e comandos já vêm prontos em `.claude/agents/` e `.claude/commands/`.

### Passo 4: Testar
Ainda dentro do wizard (ou depois, a qualquer momento), digite:
```
briefing
```
Se o comando `/briefing` responder pedindo os dados do cliente, está tudo instalado.

---

## Comandos do Dia a Dia

| O que você quer fazer | Comando |
|-----------------------|---------|
| Montar briefing de cliente novo | `/briefing` |
| Criar conteúdo/copy (ad, email, post, LP) | `/criar` |
| Revisar o que foi criado | `/revisar` |
| Empacotar e entregar | `/entregar` |
| Montar relatório de performance | `/relatorio` |
| Montar proposta comercial | `/proposta` |
| Onboardar cliente novo (pós-fechamento) | `/onboarding` |
| Mensagem de follow-up | `/follow-up` |
| Diagnosticar operação/campanha | `/diagnostico` |
| Automatizar um processo | `/automatizar-processo` |
| Configurar WhatsApp/Cowork | `/whatsapp-system` |
| Conectar MCPs (Drive, Slack, etc.) | `/mcp-setup` |
| Classificar nicho do negócio | `/setup-nicho` |
| Criar agente/skill/comando novo | `forge: <o que você precisa>` |

A lista completa (com as palavras-chave equivalentes no Claude Desktop, sem `/`) está em `22_CLAUDE_DESKTOP/commands-keywords.md`.

---

## Como Usar os Templates

1. Pra template operacional (contexto, estado, entrega de cliente): pasta `10_TEMPLATES_OPERACIONAIS/`.
2. Pra template de release simples (designer, geral, gestão): pasta `templates/` na raiz do kit.
3. Copie o template que precisa.
4. Preencha os campos marcados com `[A PREENCHER]`.
5. Entregue pro cliente.

---

## Como Usar os Prompts

1. Abra a pasta `prompts/` na raiz do kit.
2. Escolha o prompt (briefing, criação, revisão, relatório, whatsapp).
3. Copie o prompt que precisa.
4. Cole no Claude Code, Claude Desktop ou outra IA.
5. Substitua os placeholders (`[NOME DO CLIENTE]`, `[NICHO]`, etc.).
6. Use o resultado.

---

## Automação de WhatsApp

1. Configure seguindo o guia em `docs/setup-whatsapp.md`.
2. Conecte seu número.
3. Ative os fluxos com `/whatsapp-system` (atendimento, follow-up, onboarding).
4. Os fluxos ficam em modo `draft` até você confirmar a ativação real.

---

## Precisa de Ajuda?

- Consulte `docs/troubleshooting.md` pra problemas comuns.
- Consulte `docs/glossario.md` pra termos que não conhece.
- Consulte `docs/faq.md` pra perguntas frequentes.
- Peça `"que comando eu uso pra isso?"` — o CoS sugere.
