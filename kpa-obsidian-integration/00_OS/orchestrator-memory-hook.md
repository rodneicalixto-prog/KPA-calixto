# Hook do Orquestrador — Obsidian Memory Layer

## PRE_EXECUTION

Executar após classificação/roteamento e antes de carregar especialistas:

```text
ledger_state = load_authoritative_state(project)
context = memory_router.read(
  project=project,
  objective=task.objective,
  task_id=task.id,
  skills=route.skills,
  ledger_state=ledger_state
)
```

O contexto retornado deve distinguir:
- `authoritative_state`
- `decisions`
- `historical_memory`
- `skills`
- `inferences`
- `conflicts`

Se houver conflito entre memória histórica e ledger, prevalece ledger e o conflito é marcado.

## POST_GATE

Executar somente se a entrega passou pelo gate aplicável:

```text
memory_gate = validate_memory_payload(delivery)
if memory_gate.approved:
    memory_writer.write_execution(...)
    memory_writer.write_decision(...)  # quando aplicável
    memory_writer.write_lesson(...)    # quando aplicável
```

## Promoção para skill
Nunca automática. Uma lição pode gerar `skill_candidate`, mas só entra no Mega-Brain após validação explícita do KPA.
