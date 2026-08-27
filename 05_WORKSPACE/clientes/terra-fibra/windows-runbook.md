# Runbook Windows — Terra Fibra

## Agora: export manual

Na tela mostrada, a campanha já está selecionada e o período está em **Últimos 30 dias: 27 de jul de 2026 a 25 de ago de 2026**.

1. Feche o painel lateral **Salvar edições** para ampliar a tabela.
2. Clique em **Colunas: Desempenho** e escolha **Personalizar colunas**.
3. Marque: veiculação, orçamento, valor gasto, resultados, custo por resultado, alcance, impressões, frequência, CPM, cliques no link, CPC do link e CTR do link.
4. Aplique as colunas.
5. Clique no ícone de **Exportar**/download acima da tabela.
6. Escolha CSV e mantenha o mesmo período da tela.
7. Salve localmente, por exemplo em `C:\KPA\dados\terra-fibra\meta-2026-07-27-a-2026-08-25.csv`.
8. Não coloque o CSV no Git se ele contiver IDs completos ou dados pessoais.

## Preparar automação no Windows

Recomendação: usar **Agendador de Tarefas do Windows**, não cron, porque o computador informado é Windows.

Antes de criar a tarefa agendada:

- [ ] concluir uma execução manual com o export;
- [ ] validar o evento `Conversas por mensagem`;
- [ ] confirmar o nome completo da campanha;
- [ ] validar Python com `py --version` no PowerShell;
- [ ] escolher uma pasta local fixa para o repositório e para os exports;
- [ ] validar o Meta CLI ou definir um processo de export manual recorrente;
- [ ] concluir o preflight sem erros.

Configuração recomendada depois do preflight:

| Campo | Valor inicial |
|---|---|
| Nome da tarefa | `KPA - Terra Fibra - Revisão semanal` |
| Gatilho | Segunda-feira, 09:00 |
| Fuso | Horário local do Windows / America/Sao_Paulo |
| Programa | `py` |
| Argumentos | caminho absoluto de `run_scheduled_traffic.py`, configuração, `--job weekly_review --execute` |
| Iniciar em | raiz local do repositório KPA |
| Executar se usuário não estiver conectado | somente após revisar onde as credenciais locais ficam armazenadas |
| Repetir em falha | não habilitar até o primeiro teste controlado |

Não criar a tarefa ainda: o coletor Meta continua não validado e o workspace não possui job Meta executável.

