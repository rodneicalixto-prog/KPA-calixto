# Obsidian Outbox — espelho local do vault real

Este container remoto não enxerga o vault Obsidian real do usuário
(`Desktop\Jarvis V8\obsidian-template`, no Windows local — ver `OBSIDIAN.md`
na raiz do repo). Esta pasta existe pra resolver isso na prática: é um
**espelho da mesma estrutura de raízes** que `scripts/obsidian_memory_adapter.py`
já usa (`02_Projects`, `05_Knowledge`, `06_Decisions`, `07_Executions`,
`08_Lessons`, `99_Inbox`).

## Fluxo

1. Toda vez que uma sessão neste container (Claude Code / agente do kit)
   termina um trabalho relevante, grava uma nota aqui via
   `scripts/write_obsidian_memory.py --vault 05_MEMORY/obsidian-outbox --apply`
   (mesmo formato/validação — `GATE-MEMORY` — que seria usado contra o vault
   real).
2. Periodicamente, o usuário **copia o conteúdo desta pasta pro vault real**
   na própria máquina (copiar/colar, `robocopy`, ou script local dele) —
   essa etapa é sempre manual e local, nunca automática daqui.
3. Depois de sincronizado, o conteúdo já copiado pode ser limpo desta pasta
   (ela é só uma caixa de saída, não o arquivo definitivo).

## Por que não escrever direto no vault real

Este ambiente é um container remoto na nuvem — não tem acesso ao
sistema de arquivos Windows do usuário (`C:\Users\...`). Só o
`scripts/obsidian_memory_adapter.py` rodando **localmente na máquina do
usuário**, com `KPA_OBSIDIAN_VAULT` apontando pro caminho real, consegue
escrever no vault de verdade.

## Nunca commitar segredo aqui

Mesma regra do resto do kit (`00_OS/commands/instalar-kpa30.md`, `.env`):
nenhuma nota gravada aqui deve conter token, senha ou credencial — o
adapter já redige padrões óbvios (`SECRET_PATTERNS` em
`obsidian_memory_adapter.py`), mas não é uma garantia absoluta.
