# Task: Operação Agendada de Tráfego

## Objetivo

Produzir leituras recorrentes e tarefas propostas sem executar mudanças em plataformas. O agendamento automatiza coleta e diagnóstico; decisões e escritas continuam humanas.

## Entradas

- cliente e contas mapeadas;
- timezone, frequência e janela de análise;
- comando de coleta somente leitura validado;
- baseline de KPIs;
- canal de saída e responsável humano;
- política de retenção e localização dos logs.

## Modos

| Modo | Frequência sugerida | Entrega |
|---|---|---|
| `daily_health` | diária | falhas de coleta, tracking, pacing e anomalias |
| `weekly_review` | semanal | diagnóstico do funil, criativos e backlog priorizado |
| `monthly_baseline` | mensal | proposta de atualização do baseline, nunca atualização silenciosa |

## Pipeline

1. Validar preflight e confirmar que os conectores são somente leitura.
2. Criar `run_id` com cliente, modo e timestamp.
3. Coletar dados brutos e registrar fonte, janela, timezone e checksum quando possível.
4. Validar completude, duplicidade, moeda e divergência de eventos.
5. Se o gate de dados falhar, emitir relatório de falha e não gerar recomendação econômica.
6. Executar diagnóstico usando o playbook do funil correspondente.
7. Gerar relatório em `06_OUTPUTS/<cliente>/traffic/` e log operacional em `07_LOGS/`.
8. Criar somente propostas de ação com responsável e aprovação necessária.
9. Registrar próxima execução e política de retry.

## Retry e idempotência

- no máximo duas novas tentativas para erro transitório;
- backoff configurável no scheduler;
- o mesmo `run_id` não pode publicar dois relatórios finais;
- uma execução atrasada não deve sobrepor a janela da execução seguinte;
- falha de autenticação encerra o job e solicita correção humana, sem loop de tentativas.

## Saída mínima

```yaml
run_id: "[cliente]_[modo]_[timestamp]"
status: "success | partial | failed"
data_quality: "approved | blocked"
sources: []
window: "[A PREENCHER]"
findings: []
proposed_actions: []
approval_required: true
next_run: "[A PREENCHER]"
```

## Guardrails

- Scheduler não recebe permissão de escrita em contas de anúncio.
- Tokens permanecem em secret store ou `.env` gitignored.
- Logs não contêm payloads pessoais nem credenciais.
- Recomendações não são aplicadas automaticamente.
- Pausa, publicação, budget e exclusão exigem confirmação humana explícita.

## Execução local

Preencha uma cópia de `templates/schedule-runtime-template.json` e valide o plano sem escrever saída:

```bash
python3 11_TRAFFIC_STACK/tools/run_scheduled_traffic.py schedule.json \
  --job weekly_review
```

Para executar o renderer offline, marque apenas o job revisado como `enabled: true` e acrescente `--execute`. O runner não recebe comando arbitrário, não usa shell e aceita somente modos implementados explicitamente.
