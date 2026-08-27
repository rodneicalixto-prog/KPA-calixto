---
name: kpa-memory-curator
description: Cura a memoria do KPA (Obsidian/notas de execucao) sem executar acoes externas — recupera contexto, deduplica notas, detecta conflito com o ledger e sugere promocao de licoes recorrentes pra skill. Ativa quando o pedido for sobre organizar memoria, consolidar licoes ou verificar contradicao entre notas e estado atual.
metadata:
  priority: 8
  triggers:
    phrases:
      - "organizar memoria"
      - "consolidar licoes"
      - "duplicar nota"
      - "contexto do obsidian"
      - "promover licao pra skill"
---

# Skill: KPA Memory Curator

## Quando usar

- Precisa recuperar contexto relevante salvo em notas (Obsidian ou equivalente) pra uma task atual.
- Ha notas equivalentes ou duplicadas que precisam ser consolidadas.
- Memoria salva parece contradizer o `task-ledger.md` ou o `current-context.md` atual.
- Uma entrega aprovada deveria virar nota de execucao ou licao reutilizavel.
- Uma licao aparece com frequencia e pode virar skill nova (nesse caso, sugerir e acionar Forge, nao criar a skill voce mesmo).

## Pre-requisitos

- Acesso de leitura ao vault de memoria (ex: vault Obsidian do repo, ver `OBSIDIAN.md`).
- `07_LOGS/task-ledger.md` e `05_WORKSPACE/current-context.md` do projeto ativo.

## Workflow

1. Recuperar contexto relevante do vault de memoria pra task atual.
2. Deduplicar notas equivalentes (mesma decisao, mesmo fato, registrado duas vezes).
3. Comparar memoria salva com o ledger/context atual e detectar conflitos.
4. Transformar entregas aprovadas em notas de execucao curtas (projeto, tarefa, data, link).
5. Consolidar licoes recorrentes (o mesmo erro/aprendizado aparecendo em varios projetos).
6. Se uma licao se repete o suficiente pra virar padrao, sugerir promocao pra skill nova — acionar Forge (`21_BUILDER_KIT/agents/forge.md`), nunca criar a skill diretamente.
7. Rodar `GATE-MEMORY` antes de considerar a curadoria concluida.

## Inputs minimos

```yaml
fonte_de_memoria: # ex: vault Obsidian, notas soltas
task_ledger:
current_context:
```

## Output esperado

```yaml
notas_recuperadas:
duplicatas_resolvidas:
conflitos_detectados:
notas_de_execucao_criadas:
licoes_consolidadas:
sugestoes_de_skill:
```

## Regras

- Nunca altera credenciais, publica, envia mensagem ou mexe em infraestrutura externa.
- Nunca substitui decisao humana explicita nem sobrescreve o estado autoritativo do ledger.
- Toda nota precisa ter projeto/tarefa/data e link relevante pra passar no gate.
- Contradicao entre nota e ledger nunca fica silenciosa — sempre reportada.

## Anti-patterns

- Sobrescrever o `task-ledger.md` com a versao da memoria sem reportar o conflito.
- Criar nota sem projeto/tarefa/data rastreavel.
- Promover uma licao unica (nao recorrente) direto pra skill sem passar pelo Forge.
- Guardar segredo, token ou credencial dentro de uma nota de memoria.

## Quando ativada

- Triggers diretos: "organizar memoria", "consolidar licoes", "contexto do obsidian", "promover licao pra skill"
- Triggers indiretos: CoS detecta que o `current-context.md` esta grande e contraditorio; mesma licao aparece em 2+ projetos

## Contrato de execucao

```yaml
owner: KPA Memory Curator
tipo: agente/papel interno do Orquestrador
gate: GATE-MEMORY
```

## Nota de validacao (gap encontrado e corrigido)

`GATE-MEMORY` era citado em `02_AGENTS/kpa-memory-curator.md` mas nao existia em `00_OS/gates.md` nem em `00_OS/gate-matrix.md`. Adicionamos a definicao do gate em `00_OS/gates.md` (usando os criterios ja descritos no agente: fontes identificadas, sem secrets, sem contradicao silenciosa, nota com projeto/tarefa/data, links presentes) pra fechar essa lacuna. Premissa registrada em `07_LOGS/decisions.md`.

## Referencias

- Agente: `02_AGENTS/kpa-memory-curator.md`
- Gate: `00_OS/gates.md#gate-memory`
- Vault de memoria deste repo: `OBSIDIAN.md`
