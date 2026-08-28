# Handoff Schema — NEY (Terra Fibra)

```yaml
lead_id: "[A PREENCHER]"
nome: "[A PREENCHER]"
telefone: "[A PREENCHER]"
origem: "campanha Meta Ads — conjunto ativo no momento (ver funil.md)"
intencao: "consultar cobertura / interesse em plano 500 Mega"
cidade: "[A PREENCHER]"
bairro: "[A PREENCHER]"
cep: "[A PREENCHER]"
area_status: "dentro | fora | ambiguo"
dor_principal: "[A PREENCHER]"
objecao_principal: "[A PREENCHER]"
fit: "alto | medio | baixo | desconhecido"
ultima_mensagem_do_lead: "[A PREENCHER]"
resumo_da_conversa: "[A PREENCHER]"
proxima_acao_recomendada: "confirmar cobertura exata por geolocalizacao e apresentar plano disponivel"
prioridade: "alta | media | baixa"
tags: []
campos_pendentes: []
responsavel_humano: "Rodnei (ou quem ele designar)"
```

## Regra

Handoff so acontece pra `dentro_area` (qualificado) ou `duvida_fora_do_escopo`. Lead `fora_area` e encerrado pelo bot e so vira dado agregado em `lead-quality.md`, nao handoff individual — a menos que Rodnei peça retomar contato manualmente por uma expansao futura de cobertura.
