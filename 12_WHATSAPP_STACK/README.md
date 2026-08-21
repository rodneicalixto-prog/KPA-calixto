# 12_WHATSAPP_STACK — Sistema de WhatsApp e Cowork

Stack operacional para transformar estrategia, copy e atendimento em fluxos de WhatsApp que rodam com pouca intervencao humana.

Esta camada existe porque WhatsApp nao e so "mais um canal de copy". Ele mistura venda, atendimento, qualificacao, suporte, contexto do cliente e risco de automacao ruim. O V30 trata WhatsApp como sistema com papeis separados, gates e documentos prontos para runtime no Cowork.

## Objetivo

Criar chatbots e documentos operacionais para:

1. prospeccao;
2. atendimento estilo SDR;
3. sucesso do cliente;
4. follow-up de vendas;
5. especificacao para rodar no Cowork depois.

## Arquitetura

```text
CoS
  -> whatsapp-orchestrator
      -> prospecting-bot
      -> sdr-attendant
      -> customer-success-bot
      -> sales-followup-bot
      -> cowork-automation-architect
      -> conversation-qa
```

## Agentes

| Agente | Responsabilidade |
|---|---|
| `@whatsapp-orchestrator` | Define rota, objetivo da conversa, insumos e handoff entre bots |
| `@prospecting-bot` | Abordagem fria/morna, abertura de conversa e permissao para continuar |
| `@sdr-attendant` | Atendimento consultivo, qualificacao, objeções, agendamento e handoff comercial |
| `@customer-success-bot` | Onboarding, uso do produto, check-ins, riscos de churn e reativacao |
| `@sales-followup-bot` | Follow-up de oportunidades, recuperacao de no-show e fechamento |
| `@cowork-automation-architect` | Gera documentos, schemas, estados e regras para rodar no Cowork |
| `@conversation-qa` | Valida fluxo contra tom, LGPD, clareza, risco e gate de automacao |

## Contexto obrigatorio por cliente

Antes de criar qualquer fluxo real, carregar ou criar:

- `05_WORKSPACE/clientes/<cliente>/context.md`
- `05_WORKSPACE/clientes/<cliente>/state.md`
- `05_WORKSPACE/clientes/<cliente>/proofs.md`
- `05_WORKSPACE/clientes/<cliente>/whatsapp-context.md`
- oferta, publico, tom, restricoes e claims proibidos

Se faltar dado, usar `[A PREENCHER]` e produzir fluxo em modo `draft`. Nao inventar promessa, prova, preco, garantia, agenda, SLA ou politica de atendimento.

## Comandos operacionais

| Pedido | Rota |
|---|---|
| `*whatsapp-map` | mapa geral dos bots e estados |
| `*prospeccao` | fluxo de prospeccao |
| `*sdr` | atendimento/qualificacao estilo SDR |
| `*sucesso` | customer success e onboarding |
| `*follow-up` | follow-up de vendas |
| `*cowork-docs` | pacote tecnico para Cowork |
| `*qa-whatsapp` | revisao dos fluxos |

## Entregaveis

Um pacote WhatsApp completo precisa gerar:

- mapa de intencoes;
- arvore de conversa;
- mensagens por estado;
- variaveis e memoria do contato;
- criterios de qualificacao;
- regras de handoff humano;
- limites do bot;
- objeções e respostas aprovadas;
- mensagens de follow-up por timing;
- documento Cowork com triggers, estados, tags e payloads;
- checklist de QA.

## Regras inegociaveis

- Bot nao finge ser humano.
- Bot nao inventa disponibilidade, desconto, prazo ou prova.
- Mensagem precisa ter proximo passo claro.
- Atendimento nao deve virar monologo. Cada bloco deve caber numa tela de celular.
- Follow-up deve ter motivo contextual, nao "passando pra lembrar".
- Prospecção precisa permissao ou contexto antes de pitch.
- Handoff humano deve ser acionado quando ha compra, reclamacao, risco legal, dado sensivel, pedido fora do escopo ou alta intencao.
- Automacao real so vai para Cowork depois de `GATE-WHATSAPP` e `conversation-qa`.

## Como encaixa no V30

- Research gera VOC e objeções.
- Strategist define promessa, MUP, MUS e prova.
- Copy Director aprova nucleo persuasivo.
- WhatsApp Stack transforma isso em conversa operacional.
- Cowork Architect gera docs para runtime.
- QA valida antes de uso real.

## Saidas padrao

```text
05_WORKSPACE/clientes/<cliente>/whatsapp/
├── whatsapp-context.md
├── conversation-map.md
├── prospecting-flow.md
├── sdr-flow.md
├── success-flow.md
├── followup-flow.md
├── cowork-agent-spec.yaml
└── qa-whatsapp.md
```

