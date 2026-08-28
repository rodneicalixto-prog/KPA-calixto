# Achados de segurança — workflow n8n "NEY V2 - SDR WhatsApp"

**Cliente:** Terra Fibra Óptica
**Workflow auditado:** `NEY V2 - SDR WhatsApp` (n8n, id `yxzgVcFonnTC60qh`, Project "Terra Fibra")
**Data da auditoria:** 2026-08-28
**Como foi feito:** leitura do JSON completo do workflow (84 nós) via MCP n8n (`get_workflow_details`), depois do compartilhamento do Project ser liberado pro acesso da sessão.
**Status:** aberto — correção depende de ação manual do usuário (n8n, OpenAI, Google Cloud). Nenhuma chave foi manipulada, rotacionada ou reimpressa por esta auditoria.

> Nenhum valor de chave/token real aparece neste documento, nem parcialmente mascarado. Os achados são localizados por nó/workflow, não por valor.

---

## 🔴 Achado 1 — Chave da API OpenAI em texto plano no workflow

**Onde:** nó `NEY IA - Decidir Próximo Passo`, no parâmetro de header HTTP (`Authorization: Bearer sk-proj-...`), chamando `api.openai.com/v1/responses`. A chave está escrita direto no JSON do node — não usa uma credential nativa do n8n.

**Risco:**
- Qualquer pessoa com acesso de leitura ao workflow no n8n (ou a um export/backup dele) vê a chave.
- Se o JSON vazar (backup, cópia, compartilhamento indevido do Project), a chave é usada em nome da conta OpenAI vinculada — custo e uso indevido ficam na conta da agência/cliente.
- Credenciais hardcoded em node são o item nº 1 do checklist "nunca fazer" do próprio playbook de automação n8n da agência.

**Correção (ordem importa — rotacionar antes de trocar, pra não derrubar o bot em produção):**
1. No painel da OpenAI (platform.openai.com → API keys), gerar uma **chave nova**.
2. No n8n, criar uma **credential nativa** (Header Auth, ou a credential de API Key da OpenAI se o node suportar) com a chave nova.
3. Editar o nó `NEY IA - Decidir Próximo Passo` pra usar essa credential em vez do header hardcoded.
4. **Testar 1 mensagem real no WhatsApp** com o bot antes de considerar concluído (confirmar que a resposta da IA continua saindo normal).
5. Só depois de confirmar que o novo fluxo funciona, **revogar a chave antiga** na OpenAI.

---

## 🔴 Achado 2 — Chave da Google Geocoding API em texto plano no workflow

**Onde:** direto na URL do nó `Geocodificar Endereço Google` (parâmetro `key=...` da query string pra `maps.googleapis.com/maps/api/geocode/json`), e possivelmente também em `Geocodificar Endereço Google Form`.

**Risco:** mesmo raciocínio do Achado 1 — chave visível pra qualquer leitor do workflow/export, uso indevido em nome da conta do Google Cloud da agência/cliente se vazar.

**Correção:**
1. No Google Cloud Console, **restringir a chave atual** por API (só Geocoding API) e, se possível, por IP/referrer.
2. Gerar uma chave nova e **rotacionar**.
3. Mover a chave pra uma credential n8n (Query Auth ou Header Auth) usada pelos nós `Geocodificar Endereço Google` e `Geocodificar Endereço Google Form`, em vez de escrita direto na URL.
4. Testar geocodificação de 1 endereço real via WhatsApp antes de revogar a chave antiga.

---

## 🟡 Achado 3 — Expressão n8n possivelmente mal fechada (bug, não segurança)

**Onde:** nó `Consultar Condomínio Oficial`, no corpo da chamada RPC (`buscar_condominio_oficial`):

```
"={{ JSON.stringify({p_cidade:$json.cidade,p_nome:$json.condominio}) "
```

Falta o `}}` de fechamento da expressão n8n — a string termina sem fechar.

**Risco:** se isso não for só um artefato de como o export do workflow foi gerado, a expressão pode estar sendo enviada como texto literal em vez de ser avaliada, quebrando silenciosamente a consulta de condomínio oficial (que é a "fonte soberana" de liberação de condomínio no fluxo, segundo a própria sticky note do workflow).

**Correção sugerida:**
1. Abrir o nó `Consultar Condomínio Oficial` direto no n8n e conferir o valor real do campo (pode já estar correto na UI e o `}}` ter se perdido só na exportação via API).
2. Se o bug for real, corrigir pra `"={{ JSON.stringify({p_cidade:$json.cidade,p_nome:$json.condominio}) }}"`.
3. Testar manualmente o nó (Execute Node) com um payload de exemplo (cidade + nome de condomínio conhecido na base) pra confirmar que o RPC retorna o resultado esperado.

---

## O que esta auditoria NÃO fez

- Não alterou nenhum node, credential ou valor no workflow.
- Não rotacionou, revogou ou visualizou o valor completo de nenhuma chave.
- Não ativou/desativou o workflow.

Essas ações continuam 100% na mão do usuário, feitas diretamente nas plataformas n8n, OpenAI e Google Cloud.

## Referência

Achado no contexto de uma auditoria mais ampla da lógica de negócio do workflow (verificação de cidade/cobertura, integração Sheets/Supabase, IA de decisão) — ver `07_LOGS/decisions.md` (entrada 2026-08-28) para o resumo completo dessa auditoria.
