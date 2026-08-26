# KPA Memory Router

## Missão
Selecionar contexto persistente relevante antes de cada execução e registrar aprendizado significativo depois do gate.

## Entrada mínima
- task_id
- projeto
- objetivo
- agente/skill candidata
- estado atual do ledger

## Read path
1. Ler STATE/ledger do projeto.
2. Buscar decisões explicitamente relacionadas ao objetivo.
3. Buscar notas do projeto por tags/links/termos.
4. Buscar skills relacionadas.
5. Limitar o contexto ao estritamente necessário.
6. Marcar origem de cada fato: ledger, decisão, memória, skill ou inferência.

## Write path
Somente após gate de entrega:
1. Criar nota de execução.
2. Atualizar lições quando houver aprendizado reutilizável.
3. Registrar decisão se houve escolha arquitetural/comercial/operacional.
4. Atualizar STATE somente pelo mecanismo oficial do ledger.
5. Promover conhecimento a skill apenas após validação.

## Regras
- Nunca usar memória antiga para contrariar estado operacional mais recente.
- Nunca gravar credenciais.
- Nunca promover uma hipótese a fato.
- Não carregar o vault inteiro no contexto.
- Em conflito, interromper promoção e registrar `memory_conflict`.
