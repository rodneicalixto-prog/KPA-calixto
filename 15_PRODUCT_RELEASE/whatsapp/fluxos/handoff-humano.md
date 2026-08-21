# WhatsApp — Handoff Humano

Status: draft

## Objetivo

Transferir conversa para humano com contexto suficiente, sem o cliente precisar repetir tudo.

## Quando acionar

- preco, desconto ou contrato;
- reclamacao;
- dado sensivel;
- risco juridico/saude/financeiro;
- pedido fora do escopo;
- cliente irritado;
- automacao nao sabe responder;
- decisao que muda prazo, verba ou promessa.

## Mensagem para o cliente

```text
Vou encaminhar isso para uma pessoa do time revisar com cuidado.

Ja vou mandar o contexto junto para voce nao precisar repetir tudo.
```

## Resumo para humano

```yaml
cliente:
canal: WhatsApp
objetivo:
contexto:
historico_curto:
ultima_mensagem:
risco:
acao_recomendada:
urgencia:
dados_pendentes:
```

## Regra

Depois do handoff, a automacao nao deve continuar respondendo o mesmo assunto ate o humano encerrar ou devolver o controle.

