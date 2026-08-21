# Primeira Tarefa — Briefing Operacional KPA Calixto

## Objetivo

Deixar o KPA pronto para receber um cliente ou projeto piloto e transformar pedido solto em tarefa pequena, com rota, responsavel, entregavel e gate.

## Contexto inicial

```yaml
projeto: "KPA Calixto"
familia_operacional: "agencia-servico-digital"
oferta: "Kit Piloto Automatico V30"
canal_principal: "WhatsApp, Instagram, GitHub e automacoes"
gargalo_atual: "organizar instalacao, contexto e primeira operacao sem depender de anexos grandes"
status: "onboarded_partial"
```

## Perguntas minimas para abrir um projeto

1. Qual cliente ou projeto vamos operar agora?
2. Qual resultado precisa sair primeiro: copy, funil, WhatsApp, automacao, trafego, site ou diagnostico?
3. Quais arquivos, links ou provas ja existem?
4. O que nao pode ser feito sem confirmacao humana?
5. Qual prazo real da primeira entrega?

## Rota recomendada

| Tipo de pedido | Rota KPA | Gate |
|---|---|---|
| "Organiza isso" | CoS + task manager | delivery |
| Copy, criativos, LP, VSL | Copy Director | copy |
| WhatsApp, SDR, follow-up | WhatsApp Orchestrator | whatsapp |
| n8n, processo, automacao | Automation Architect | automation |
| Trafego, Meta Ads, metricas | Traffic Analyst | traffic |
| Revisao critica | QA Editor | review |

## Safe defaults

- Operar em modo `draft` quando envolver WhatsApp, CRM, campanha, automacao ou publicacao.
- Usar `[A PREENCHER]` para dado ausente que nao bloqueia a entrega.
- Registrar premissas em `07_LOGS/decisions.md`.
- Salvar entregas finais em `06_OUTPUTS/`.
- Manter contexto curto em `05_WORKSPACE/current-context.md`.

## Proxima acao recomendada

Escolher um projeto piloto e pedir:

```text
KPA, abrir primeira task para [cliente/projeto] com objetivo de [resultado desejado].
```

Se o primeiro foco for WhatsApp ou automacao, rodar antes:

```text
preflight acessos
```

