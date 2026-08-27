# Command - relatorio

## Objetivo

Gerar relatorio de performance ou status (trafego, operacao semanal, cliente especifico) com dados reais.

## Passos

1. Identificar o escopo: trafego pago, operacao semanal geral, ou cliente especifico.
2. Se for trafego: usar `02_AGENTS/skills/kpa-traffic-analyst/SKILL.md` (launch review/operacao semanal) ou, pra diagnostico mais fundo, `11_TRAFFIC_STACK/tasks/diagnosticar-campanha-meta-cli.md`.
3. Coletar dados reais via CLI/MCP conectado — nunca inventar numero. Se o dado nao existir, reportar o gap.
4. Usar o template correspondente (ex: `11_TRAFFIC_STACK/templates/relatorio-diagnostico-tmpl.html` pra trafego) quando existir; caso contrario, markdown estruturado.
5. Salvar em `05_WORKSPACE/clientes/<cliente>/_relatorios/<data>-<tipo>.md` ou `06_OUTPUTS/` se nao for de um cliente especifico.

## Saida

```yaml
relatorio_path:
periodo:
principais_achados:
next_step:
```
