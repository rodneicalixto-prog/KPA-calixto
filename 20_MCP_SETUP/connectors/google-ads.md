# Google Ads — Conector de Leitura

## Objetivo

Disponibilizar dados de campanha para a Traffic Stack sem conceder permissão de alteração. Este documento define critérios de escolha e validação; ele não prescreve um pacote ou comando universal.

## Rotas aceitas

1. conector aprovado pelo operador com OAuth e escopo somente leitura;
2. exportação manual conferida na interface;
3. wrapper local mantido pelo operador sobre uma API oficial.

Escolha uma rota, registre-a no campo `source` e valide-a com uma conta de teste. Como interfaces, versões e requisitos podem mudar, confira a documentação oficial vigente antes de instalar ou autenticar.

## Preflight

- [ ] cliente e conta identificados sem expor o ID completo em logs;
- [ ] responsável humano definido;
- [ ] OAuth ou segredo armazenado fora do repositório;
- [ ] escopo de leitura confirmado;
- [ ] conta de teste selecionada;
- [ ] moeda e timezone conhecidos;
- [ ] ações de conversão documentadas;
- [ ] revogação de acesso testável;
- [ ] política de retenção de exports definida.

## Teste de aceitação

1. Coletar uma janela curta em modo somente leitura.
2. Confirmar que nenhum token aparece em stdout, stderr ou arquivo gerado.
3. Conferir gasto, impressões, cliques e conversões contra a interface para a mesma janela, timezone e moeda.
4. Normalizar o resultado usando `11_TRAFFIC_STACK/templates/google-ads-insights-schema.yaml`.
5. Rodar o gate de qualidade de `11_TRAFFIC_STACK/tasks/diagnosticar-google-ads.md`.
6. Revogar ou desconectar o acesso de teste e confirmar o procedimento.

## Ativação

Somente após o teste de aceitação, registrar o conector no contexto local do cliente. Acesso de escrita não faz parte desta integração; se futuramente necessário, exige task, credencial e confirmação separadas.

## Falhas

- **Autenticação:** parar e encaminhar ao responsável; não repetir indefinidamente.
- **Divergência de totais:** bloquear diagnóstico econômico até conciliar janela, timezone, moeda e conversões.
- **Schema incompatível:** manter o export bruto, marcar `failed` e corrigir o adaptador.
- **Credencial em log:** interromper, remover o artefato, revogar/rotacionar e registrar incidente.

