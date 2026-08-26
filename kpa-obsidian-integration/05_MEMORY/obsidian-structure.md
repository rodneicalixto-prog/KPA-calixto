# Estrutura recomendada do Vault KPA

```text
00_System/
  KPA.md
  Orchestrator.md
  Memory-Rules.md
  Quality-Gates.md
01_Identity/
02_Projects/
  <Projeto>/
    PROJECT.md
    STATE.md
    DECISIONS.md
    TASKS.md
    KNOWLEDGE.md
03_Agents/
04_Skills/
05_Knowledge/
06_Decisions/
07_Executions/
08_Lessons/
99_Inbox/
```

## Compatibilidade com o vault existente
As notas `Cerebro 1 — Claude`, `Cerebro 2 — Mega-Brain`, `Cerebro 3 — Obsidian`, `Visao de Tela` e `Voz em Tempo Real` podem permanecer onde estão.

A adaptação conceitual é:
- Cérebro 1 -> Runtime LLM (GPT/Claude)
- Cérebro 2 -> Mega-Brain / Skills
- Cérebro 3 -> Obsidian / Long-term Memory
- Visão/Voz -> Tools/Capabilities do KPA
