# GATE-MEMORY

## Objetivo
Evitar que o KPA transforme saída incompleta, hipótese, dado sensível ou estado antigo em memória permanente.

## Critérios obrigatórios
- [ ] projeto identificado
- [ ] task_id identificado
- [ ] data/hora registrada
- [ ] resultado passou pelo gate funcional correspondente
- [ ] fatos e inferências estão separados
- [ ] memória não contradiz silenciosamente o ledger
- [ ] nenhum secret/credencial está presente
- [ ] links relevantes foram registrados
- [ ] próxima ação foi registrada quando existir

## Saídas
- `approved`
- `approved_with_concerns`
- `blocked`

`blocked` impede escrita automática no Obsidian.
