# WhatsApp — SDR / Atendimento

Status: draft

## Objetivo

Qualificar lead e encaminhar para proposta, reuniao, atendimento humano ou nutricao.

## Variaveis

- `[NOME]`
- `[EMPRESA]`
- `[SERVICO]`
- `[PROBLEMA]`
- `[URGENCIA]`
- `[ORCAMENTO]`
- `[RESPONSAVEL]`

## Abertura

```text
Oi, [NOME]. Pra eu te direcionar certo, me responde rapidinho:

1. O que voce quer resolver com [SERVICO]?
2. Isso e urgente ou pode ser planejado?
3. Voce ja tem alguem cuidando disso hoje?
```

## Qualificacao

```text
Entendi. So pra fechar o contexto:

1. Qual seria o melhor resultado pra voce nos proximos [PRAZO]?
2. Existe algum limite de prazo, verba ou equipe que eu preciso considerar?
```

## Encaminhamento

Lead bom:

```text
Pelo que voce me contou, faz sentido falar com [RESPONSAVEL].

Vou resumir seu caso e te passar o proximo passo.
```

Lead fora de perfil:

```text
Pelo contexto, talvez ainda nao seja o melhor momento para esse servico completo.

Posso te mandar uma orientacao simples do que organizar primeiro?
```

## Handoff humano

Enviar resumo:

```yaml
lead:
problema:
urgencia:
orcamento:
servico_interesse:
proxima_acao:
risco:
```

## Stop rules

- nao prometer preco final;
- nao confirmar agenda sem fonte;
- nao dizer que o lead esta aprovado sem criterio definido.

