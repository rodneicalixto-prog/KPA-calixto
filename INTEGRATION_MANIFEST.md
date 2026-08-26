# KPA V30 — Manifesto de Integração Obsidian

## Componentes adicionados
- `00_OS/memory-router.md`
- `02_AGENTS/kpa-memory-curator.md`
- `05_MEMORY/README.md`
- `05_MEMORY/memory-policy.yaml`
- `05_MEMORY/obsidian-structure.md`
- `scripts/obsidian_memory_adapter.py`

## Alteração arquitetural
O KPA deixa de tratar o runtime como Claude-específico. O executor passa a ser `Runtime LLM`, podendo ser GPT ou Claude.

## Autoridade de dados
O ledger continua autoritativo para estado operacional. O Obsidian guarda memória histórica e aprendizado de longo prazo.

## Integração no Orquestrador
Antes da execução:
1. carregar ledger/STATE;
2. acionar Memory Router;
3. montar contexto relevante;
4. escolher agente/skill;
5. executar.

Depois da execução:
1. executar gates existentes;
2. executar `GATE-MEMORY`;
3. gravar nota de execução no Obsidian;
4. atualizar lições/decisões quando aplicável;
5. somente o mecanismo do ledger atualiza estado operacional.

## Variável de ambiente esperada
`KPA_OBSIDIAN_VAULT=/caminho/para/seu/vault`

Nunca versionar o valor real se ele revelar caminhos privados que não devam ser compartilhados.
