# Test Cases — NEY (Terra Fibra)

```yaml
flow_name: "ney-triagem-cobertura"
status: "draft"
```

## Antes do teste

- [ ] Variaveis preenchidas em `variables-and-tags.md`.
- [ ] Responsavel humano do handoff definido (Rodnei, conforme `handoff-schema.md`).
- [ ] Lista de 21 cidades de `coverage.md` carregada e correta.
- [ ] Nenhum disparo em massa habilitado.

## Cenarios obrigatorios

| # | Cenario | Entrada simulada | Esperado | Resultado |
|---|---|---|---|---|
| 1 | Lead dentro da area, dados completos | "Aguaí, Centro, 13860-000" | `area_status = dentro`, mensagem de confirmacao, handoff qualificado gerado | [A PREENCHER] |
| 2 | Lead fora da area | "Ribeirão Preto, Jardim, 14000-000" | `area_status = fora`, mensagem educada de encerramento, tag `fora_area`, sem handoff individual | [A PREENCHER] |
| 3 | Cidade homonima de outro estado | "São Pedro" sem estado, ambiguo | Bot nao assume automaticamente SP — pede clarificacao uma vez antes de decidir | [A PREENCHER] |
| 4 | Dados incompletos (só cidade) | "Casa Branca" | Bot pede só o que falta (bairro e CEP), sem repetir a pergunta toda | [A PREENCHER] |
| 5 | Pergunta de preço/suporte fora do escopo | "Quanto custa o plano de 1 Giga?" | Handoff imediato, tag `handoff_duvida`, bot nao inventa preço | [A PREENCHER] |
| 6 | Pedido de parar | "para de me mandar mensagem" | `opt_out` aplicado, nenhum novo disparo depois | [A PREENCHER] |
| 7 | Sem resposta apos 2 tentativas | silêncio do lead | Encerra sem insistir, tag `sem_resposta`, nao conta como handoff | [A PREENCHER] |
| 8 | Reclamação/assunto sensível | "isso é golpe, quero cancelar" | Handoff humano imediato, bot não tenta resolver sozinho | [A PREENCHER] |

## Passa quando

- Mensagens ficam naturais no celular (curtas, sem cara de formulário).
- Bot nunca promete cobertura fechada só pela cidade bater com a lista.
- `fora_area` é tratado como dado de negócio (alimenta `lead-quality.md`), não como erro do lead.
- Handoff só acontece pra leads dentro da área ou com dúvida fora do escopo — não pra todo mundo.
- Opt-out funciona e persiste.
- Nenhuma ação real (envio em massa, integração com número comercial) roda sem confirmação humana de Rodnei.

## Referências

- Fluxo: `05_WORKSPACE/clientes/terra-fibra/whatsapp/conversation-map.md`
- Gate: `00_OS/gates.md#gate-whatsapp`
- Checklist: `08_CHECKLISTS/gate-whatsapp.md`
