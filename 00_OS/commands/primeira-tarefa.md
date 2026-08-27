# Command - primeira-tarefa

## Objetivo

Gerar a primeira entrega util de um mentorado/cliente, escolhida com base na familia operacional.

## Passos

1. Confirmar a familia operacional classificada (`.claude/config.md` ou rodar `nichos/family-classifier.md` se ainda nao existir).
2. Escolher a primeira tarefa default pra familia (tabela de referencia em `00_OS/commands/instalar-kpa30.md`, Etapa 8).
3. Confirmar com o usuario ou seguir direto se ja fez essa pergunta antes.
4. Rodar a tarefa e gerar o output real (nao so o plano).
5. Salvar em `06_OUTPUTS/<data>_primeira-tarefa/`.

## Saida

```yaml
familia:
tarefa_gerada:
output_path:
next_step:
```
