# Obsidian e o Kit V30

> **Correção (31/08/2026):** este arquivo dizia antes que o próprio repositório
> `KPA-calixto` podia ser aberto como vault do Obsidian. Isso estava
> incompleto/errado como orientação principal: o usuário desta instância já
> tem um **vault real, em uso ativo**, na própria máquina (ex: `obsidian-template`),
> com estrutura própria (`_contexto`, `02_Projects`, `06_Decisions`,
> `07_Executions`, `08_Lessons`, `99_Inbox`, `Agentes/`, `pessoas/`, etc.) —
> não relacionada a este repositório. O kit NUNCA deve presumir que o repo é
> o vault; o vault é sempre externo e local ao operador.

## Como o kit se conecta ao vault real

- `KPA_OBSIDIAN_VAULT` (no `.env` local) deve apontar para o caminho, **na
  máquina do usuário**, do vault Obsidian que ele já usa — nunca para a pasta
  deste repositório.
- `scripts/obsidian_memory_adapter.py` é o adapter de filesystem que lê/escreve
  nesse vault (busca em `02_Projects/`, `05_Knowledge/`, `06_Decisions/`,
  `08_Lessons/` por padrão — raízes compatíveis com um vault real do tipo
  mostrado acima).
- `05_MEMORY/obsidian-structure.md` documenta a estrutura recomendada de vault
  e como mapear conceitos do kit (Cérebro 1/2/3) pra pastas existentes do
  vault do usuário, sem forçar reorganização.
- **Nunca presumir o caminho do vault.** Se `KPA_OBSIDIAN_VAULT` estiver vazio,
  perguntar ao usuário o caminho local exato antes de qualquer leitura/escrita
  de memória de longo prazo — nunca inventar ou usar o path deste repositório
  como fallback.

## `.obsidian/` deste repositório

A pasta `.obsidian/app.json` (config mínima, `{}`) existe aqui só por
compatibilidade histórica — permite que ESTE repo também seja aberto como um
vault secundário do Obsidian, se algum dia fizer sentido (ex: um vault
dedicado só ao kit, separado do vault pessoal do operador). **Isso não é o
fluxo recomendado nem o padrão em uso** — o vault de memória de longo prazo do
usuário é o externo, descrito acima.
