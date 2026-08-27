# Plano de ativação — Codex × Meta Ads × Google Ads

**Status:** planejado; nenhuma credencial ou escrita em plataforma ativada.  
**Prioridade:** próxima etapa após a conclusão e sincronização da memória do KPA.  
**Responsável pela aprovação:** Rodnei.

## Objetivo

Permitir que o Codex colete dados em modo somente leitura, normalize métricas, produza diagnósticos e execute tarefas recorrentes auditáveis. Alterações de campanha continuam fora do escopo inicial.

## Fase 0 — Runtime e identidade

- [ ] definir onde o Codex executor rodará: Windows local, WSL ou runner dedicado;
- [ ] criar `.env` somente local com referências lógicas, nunca versionadas;
- [ ] validar Obsidian como memória histórica e ledger como estado autoritativo;
- [ ] registrar timezone operacional `America/Sao_Paulo`;
- [ ] validar logs, diretórios de input/output e política de retenção.

**Gate:** runtime executa diagnóstico local sem acessar plataformas e sem expor segredos.

## Fase 1 — Meta Ads read-only

- [ ] escolher conector suportado: Meta CLI, Marketing API ou MCP auditado;
- [ ] conceder apenas permissões mínimas de leitura;
- [ ] obter export real anonimizado e validar pelo contrato Meta;
- [ ] confirmar ação de resultado, janela de atribuição e timezone;
- [ ] reconciliar campanhas, conjuntos, anúncios, investimento e resultados;
- [ ] gerar relatório HTML e memória de execução.

**Gate:** três coletas consecutivas consistentes, sem qualquer endpoint de escrita disponível ao job.

## Fase 2 — Google Ads read-only

- [ ] configurar conta de desenvolvedor/conector em leitura;
- [ ] validar customer ID apenas fora do Git e armazenar somente versão mascarada nos outputs;
- [ ] confirmar ações de conversão e status `primary/secondary`;
- [ ] validar export pelo contrato Google Ads;
- [ ] reconciliar custo, cliques, conversões e valor de conversão;
- [ ] gerar relatório HTML e memória de execução.

**Gate:** três coletas consecutivas consistentes e nenhuma mutation disponível ao job.

## Fase 3 — Métricas unificadas

Normalizar por plataforma, conta, campanha, data e definição de conversão:

| Grupo | Métricas mínimas |
|---|---|
| Entrega | investimento, impressões, alcance, frequência, CPM |
| Tráfego | cliques, CTR, CPC, visualizações de página quando disponíveis |
| Conversão | resultados, taxa de conversão, custo por resultado |
| Qualidade | qualificadas, fora de área, sem resposta, vendas/instalações |
| Negócio | receita confirmada, CAC, ROAS e payback quando houver fonte confiável |

Nunca comparar plataformas sem alinhar janela, moeda, timezone e definição de conversão.

## Fase 4 — Motor de decisão

Cada regra deve possuir:

- métrica e fonte;
- janela e baseline;
- mínimo de dados;
- severidade;
- recomendação;
- evidências;
- aprovação necessária;
- rollback quando aplicável.

Primeiras decisões automatizáveis sem escrita:

1. alertar ausência ou atraso de dados;
2. detectar divergência entre plataforma e CRM/WhatsApp;
3. identificar gasto sem conversão após mínimo configurado;
4. sinalizar conversões fora da área de cobertura;
5. produzir lista priorizada de investigação;
6. gerar relatório e nota Obsidian após gate.

## Fase 5 — Scheduler

- [ ] executar dry-run manual;
- [ ] habilitar coleta diária somente leitura;
- [ ] habilitar revisão semanal consolidada;
- [ ] configurar retries limitados e alerta de falha;
- [ ] impedir execução se preflight, contrato ou segurança falharem;
- [ ] registrar cada execução no ledger e no Obsidian.

## Escritas futuras — fora do escopo inicial

Pausar, publicar, alterar orçamento, segmentação, criativo ou conversão exige um projeto separado, confirmação humana por ação e trilha de auditoria. Nenhuma aprovação genérica habilita escrita automática.

## Critério de conclusão

- Meta e Google coletam em leitura com três execuções consistentes;
- métricas unificadas passam por reconciliação;
- decisões geram recomendações com evidências;
- scheduler executa sem credenciais em logs;
- memória Obsidian e ledger são atualizados sem duplicação;
- zero chamadas de escrita em plataformas.
