# Command - briefing

## Objetivo

Coletar as informacoes minimas de um cliente/projeto novo (ou de uma nova entrega de um cliente existente) pra abrir uma task com contexto suficiente.

## Passos

1. Rodar ou consultar `00_OS/access-preflight.md` se ainda nao rodou pro cliente.
2. Cliente novo: usar `15_PRODUCT_RELEASE/templates/primeiro-briefing.md` como base. Cliente recorrente: usar `10_TEMPLATES_OPERACIONAIS/cliente-template/context.md`.
3. Preencher com o que o usuario ja deu; marcar o resto como `[A PREENCHER]`, nunca inventar.
4. Se a familia operacional ainda nao foi classificada, rodar `nichos/family-classifier.md`.
5. Salvar em `05_WORKSPACE/clientes/<cliente>/briefing.md` (ou `context.md` se ja existir workspace).
6. Rodar `GATE-INTAKE`.

## Saida

```yaml
briefing_file:
familia:
gaps:
next_step:
```
