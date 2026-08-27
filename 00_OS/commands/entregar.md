# Command - entregar

## Objetivo

Empacotar uma entrega final aprovada e comunicar o handoff pro usuario/cliente.

## Passos

1. Confirmar que a entrega passou pelo gate aplicavel (`00_OS/gates.md`) — nunca empacotar algo com verdict `fail` ou `rework`.
2. Gerar o pacote final em `06_OUTPUTS/<data>_<nome-da-entrega>/`.
3. Escrever o handoff seguindo o contrato de `00_OS/handoffs.md` (from, to, output, used_inputs, assumptions, open_gaps, gate_result, next_step, files).
4. Atualizar `07_LOGS/task-ledger.md`.
5. Comunicar ao usuario em ate 3 frases: o que foi entregue, onde esta salvo, qual o proximo passo.

## Saida

```yaml
output_path:
handoff:
gate_result:
pendencias:
```
