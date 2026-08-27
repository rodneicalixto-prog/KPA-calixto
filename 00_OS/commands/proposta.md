# Command - proposta

## Objetivo

Montar uma proposta comercial pra um prospect, com promessa amarrada a mecanismo e prova.

## Passos

1. Carregar o briefing do prospect (`/briefing` se ainda nao existir).
2. Rodar `kpa-strategist` pra alinhar promessa, mecanismo e prova disponivel — promessa sem mecanismo nao passa no gate.
3. Escrever a proposta: oferta, prova, investimento, condicoes, proximos passos.
4. Rodar `GATE-COPY`.
5. Marcar preco/condicoes comerciais como `[A PREENCHER]` se ainda nao confirmados pelo usuario — nunca inventar valor.

## Saida

```yaml
proposta_path:
gate_result:
pendencias:
```
