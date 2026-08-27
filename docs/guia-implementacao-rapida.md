# Guia de Implementação Rápida | BÔNUS

> Tempo total: 15-20 minutos. Siga na ordem.

## Checklist de Instalação

### Passo 1: Instalar Node.js (2 min)
- [ ] Acesse nodejs.org
- [ ] Baixe a versão LTS
- [ ] Instale (Next, Next, Next, Finish)
- [ ] Abra o terminal e digite: `node --version`
- [ ] Se aparecer um número (ex: v20.11.0), está instalado

### Passo 2: Instalar o Claude Code (3 min)
- [ ] No terminal, digite: `npm install -g @anthropic-ai/claude-code`
- [ ] Aguarde a instalação (30-60 segundos)
- [ ] Digite: `claude --version`
- [ ] Se aparecer a versão, está instalado

### Passo 3: Fazer login (1 min)
- [ ] No terminal, digite: `claude login`
- [ ] O navegador vai abrir
- [ ] Faça login com sua conta Anthropic
- [ ] Volte pro terminal. Deve mostrar "Logged in successfully"

### Passo 4: Rodar o wizard de instalação (5-10 min)
- [ ] No terminal, navegue até a pasta do kit: `cd kit-piloto-automatico-v30`
- [ ] Digite: `claude`
- [ ] Dentro do Claude Code, digite: `instalar kpa30`
- [ ] Responda as perguntas do wizard (dependências, `.env`, MCPs, seu negócio)
- [ ] **Você não precisa copiar nenhuma pasta de agente manualmente** — os agentes, skills e comandos (`.claude/agents/`, `.claude/commands/`) já vêm prontos no kit

### Passo 5: Testar o primeiro comando (2 min)
- [ ] No terminal, dentro da pasta do kit: `claude`
- [ ] Dentro do Claude Code, digite: `Faça um briefing para um cliente de clínica odontológica que quer atrair mais pacientes`
- [ ] O comando `/briefing` deve gerar um briefing estruturado
- [ ] Se funcionou, o kit inteiro está pronto (o mesmo CoS roteia pra qualquer outro comando)

### Passo 6: Escolher seus templates (3 min)
- [ ] Pra operar clientes reais: abra `10_TEMPLATES_OPERACIONAIS/`
- [ ] Pra material de release simples (designer, geral, gestão): abra `templates/` na raiz do kit
- [ ] Identifique seu segmento principal
- [ ] Copie o template do seu segmento
- [ ] Abra um template e preencha com dados de um cliente real
- [ ] Se o template fez sentido pra sua entrega, está pronto

### Passo 7: Ativar a automação de WhatsApp (2 min)
- [ ] Siga o guia em `docs/setup-whatsapp.md`
- [ ] Conecte seu número comercial
- [ ] Ative o fluxo de atendimento com o comando `whatsapp system`
- [ ] Mande uma mensagem teste pro seu número
- [ ] Se recebeu resposta automática, está ativo

---

## Pronto. Seu kit está instalado.

**Próximos passos:**
1. Use os comandos diariamente (`/briefing`, `/criar`, `/revisar`, `/entregar`, `/relatorio` — lista completa em `22_CLAUDE_DESKTOP/commands-keywords.md`)
2. Personalize os templates com sua marca
3. Explore os prompts em `prompts/` conforme a necessidade
4. Ajuste os fluxos de WhatsApp pro seu contexto
5. Precisa de um agente, skill ou comando que o kit ainda não tem? Peça pro Forge: `forge: criar agente especialista em X`

**Dica:** Comece pelo comando `/briefing` com um cliente real. É a forma mais rápida de sentir o poder do kit.
