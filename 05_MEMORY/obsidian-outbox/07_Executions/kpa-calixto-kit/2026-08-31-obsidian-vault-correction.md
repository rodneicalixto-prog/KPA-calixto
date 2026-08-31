---
type: kpa_execution
project: kpa-calixto-kit
task_id: obsidian-vault-correction
date: 2026-08-31T18:35:27.488898+00:00
status: approved_memory_write
---

# Correção: repo KPA-calixto não é o vault Obsidian real

## Resumo
OBSIDIAN.md sugeria abrir o próprio repositório KPA-calixto como vault Obsidian. O usuário já tem um vault real em uso na máquina Windows local (obsidian-template, em Desktop\Jarvis V8), com estrutura própria (02_Projects, 06_Decisions, 07_Executions, 08_Lessons, 99_Inbox, Agentes/, pessoas/, Sistemas/). Existiam 3 vaults com o mesmo nome 'obsidian-template' em pastas diferentes, mais um vault separado 'Calixto Mentalidades' — usuário confirmou qual é o ativo.

## Resultado
OBSIDIAN.md reescrito para nunca presumir o caminho do vault. .claude/config.md atualizado com a correção e o caminho confirmado. .env local (não versionado) com KPA_OBSIDIAN_VAULT apontando para Desktop\Jarvis V8\obsidian-template. Criada esta pasta 05_MEMORY/obsidian-outbox/ como espelho local de staging, já que este container remoto não acessa o filesystem Windows do usuário diretamente.

## Funcionou
Perguntar ao usuário via opções estruturadas antes de assumir qual dos 4 vaults candidatos era o real evitou gravar um caminho errado permanentemente na documentação.

## Falhou / ressalvas
Erro inicial: assumi sem confirmar que o próprio repositório podia servir de vault Obsidian, só com base numa leitura literal do OBSIDIAN.md antigo — sem checar se o usuário já tinha um vault real em uso antes de afirmar isso.

## Decisão
Vault real e ativo: Desktop\Jarvis V8\obsidian-template (Windows local do usuário). O repo KPA-calixto nunca deve ser tratado como vault por padrão. Escritas de memória feitas neste container remoto vão para 05_MEMORY/obsidian-outbox/ (mesma estrutura de raízes do vault real) até o usuário sincronizar manualmente para o vault de verdade.

## Próxima ação
Usuário sincroniza periodicamente 05_MEMORY/obsidian-outbox/ para o vault real na própria máquina. Rodar scripts/write_obsidian_memory.py --vault 05_MEMORY/obsidian-outbox --apply ao fim de cada task relevante executada neste container.

## Links
- [[OBSIDIAN.md]]
- [[.claude/config.md]]
- [[scripts/obsidian_memory_adapter.py]]
