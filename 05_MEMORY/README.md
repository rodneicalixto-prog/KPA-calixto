# KPA — Obsidian Memory Layer

## Papel
O Obsidian é a memória de longo prazo do KPA. O ledger KPA continua sendo a fonte autoritativa do estado operacional atual.

## Regra de precedência
1. Ledger/STATE operacional atual
2. Decisões explícitas do projeto
3. Obsidian / memória histórica
4. Mega-Brain / skills
5. Inferência do modelo

Memória histórica nunca sobrescreve automaticamente uma decisão operacional mais recente.

## Ciclo
pedido -> Orquestrador -> Memory Router -> Context Builder -> Skill/Agente -> execução -> Quality Gate -> Memory Writer -> Obsidian

## Escrita automática
Após uma entrega significativa, registrar:
- o que foi feito;
- resultado/gate;
- o que funcionou;
- o que falhou;
- decisão tomada e motivo;
- links para projeto, tarefa e skill;
- próxima ação.

## Segurança
- Nunca gravar senhas, tokens, cookies, secrets ou chaves.
- Credenciais são apenas referenciadas por nome lógico.
- Escrita automática deve ficar restrita às pastas permitidas.
