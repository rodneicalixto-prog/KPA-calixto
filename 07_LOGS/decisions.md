# Decisions

Registre decisoes que afetam o rumo do projeto.

| Data | Decisao | Premissa | Impacto | Reversivel |
|---|---|---|---|---|
| 2026-08-21 | Instalar a partir do repositório GitHub `rodneicalixto-prog/KPA-calixto` | Os anexos excediam tamanho e o repo continha a estrutura completa | Kit passou a operar localmente no workspace clonado | Sim, basta trocar a origem ou atualizar o clone |
| 2026-08-21 | Marcar instalacao como partial | Claude CLI nao foi detectado e MCPs exigem login/OAuth local | Configuracao base e contexto foram salvos; conectores ficam pendentes | Sim, concluir MCPs depois com `claude mcp add` ou Claude Desktop |
| 2026-08-21 | Usar `agencia-servico-digital` como familia inicial | O KPA organiza funis, campanhas, criativos, automacoes, WhatsApp e entregas | Primeira tarefa default vira briefing/processo de cliente novo | Sim, alterar `.claude/config.md` se o foco mudar |
| 2026-08-21 | Restaurar `15_PRODUCT_RELEASE/` a partir do Google Drive | A pasta era grande para anexar e estava ausente no clone do GitHub | Release publica voltou ao repositório local com 157 arquivos importados + manifesto | Sim, substituir por nova exportacao do Drive |

> Quando uma decisao for tomada com impacto no produto/projeto, anote aqui. Inclua premissa (por que decidiu assim), impacto (o que muda) e reversibilidade (consegue desfazer? como?).
