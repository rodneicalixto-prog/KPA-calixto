# Intake Meta Ads — Terra Fibra

## O que foi identificado no link

O link recebido é do **Meta Ads Manager**, não do Google Ads. Por segurança, o link completo e os identificadores completos não são persistidos no repositório.

Informações derivadas dos parâmetros do link:

- plataforma: Meta Ads;
- conta de anúncios: final `0862`;
- Business Manager: final `0720`;
- campanha selecionada: final `1882`;
- filtro presente no link: campanhas com impressões maiores que zero e status de entrega ativo;
- responsável: Rodnei.
- sistema do operador: Windows;
- nome visível da campanha: `TERRA FIBRA | 500MEGA | TRAFEGO WHATS | ...` (texto truncado na captura);
- resultado exibido: conversas por mensagem;
- destino: WhatsApp;
- janela visível: 27/07/2026 a 25/08/2026;
- leitura preliminar: 4 conversas, R$ 6,48 por conversa e R$ 25,92 gastos.
- conjunto de anúncios: `CS | Todas cidades | WhatsApp`;
- anúncio: `Novo anúncio de Tráfego`;
- alcance: 219;
- impressões: 246;
- frequência: 1,12;
- CPM: R$ 105,37;
- cliques no link: 7;
- CPC do link: R$ 3,70;
- CTR do link: 2,85%;
- cliques (todos): 6;
- CPC (todos): R$ 4,32;
- CTR (todos): 2,44%;
- orçamento diário exibido: R$ 21,54.

Esses dados identificam o contexto, mas não comprovam acesso nem retornam métricas. A página exige uma sessão autenticada do Meta Ads Manager.

## Próximo passo no navegador

1. Abra o link recebido em um navegador no qual Rodnei já esteja autenticado no Meta.
2. Confirme que o nome da conta é **Terra Fibra** e que o ID termina em `0862`.
3. Confirme que a campanha selecionada termina em `1882`.
4. Não envie senha, cookie, token ou captura contendo identificadores completos.
5. Abra a campanha para copiar o nome completo; a captura atual mostra o final truncado.

## Coleta inicial sem API

Enquanto o Meta CLI não estiver autenticado, faça uma exportação manual somente leitura:

1. Mantenha selecionada a campanha indicada pelo link.
2. Escolha os últimos 7 dias completos.
3. Em **Colunas**, use Desempenho ou personalize para incluir:
   - nome e status da campanha;
   - valor gasto;
   - impressões, alcance e frequência;
   - cliques no link, CTR do link, CPC e CPM;
   - resultados e custo por resultado;
   - valor de conversão e ROAS, quando configurados.
4. Use **Exportar** para baixar CSV.
5. Guarde o CSV fora do Git se ele contiver IDs completos.
6. Compare os totais do arquivo com os totais exibidos na interface para a mesma janela.

Ao conferir o CSV, investigar por que a interface exibiu 7 cliques no link e 6 cliques (todos). Não alterar os números para fazê-los coincidir; preservar os campos e suas definições originais.

## Identificar o evento de conversão

Na coluna **Resultados**, anote exatamente o rótulo apresentado. Exemplos possíveis incluem lead, conversa iniciada, formulário, compra ou evento personalizado, mas nenhum deles deve ser assumido.

Registre:

| Campo | Valor |
|---|---|
| Nome visível da campanha | `TERRA FIBRA | 500MEGA | TRAFEGO WHATS | ...` — confirmar nome completo |
| Resultado/evento exibido | Conversas por mensagem |
| Quantidade na janela visível de 30 dias | 4 |
| Custo por resultado | R$ 6,48 |
| Destino | WhatsApp |

## Meta CLI

A rota automatizada prevista pelo kit usa a task `11_TRAFFIC_STACK/tasks/diagnosticar-campanha-meta-cli.md`.

Antes de qualquer coleta:

- [ ] `meta auth status` confirma autenticação local;
- [ ] a conta terminada em `0862` está acessível em modo leitura;
- [ ] a janela de análise foi definida;
- [ ] o evento de resultado foi confirmado;
- [ ] nenhum token foi colocado no workspace;
- [ ] qualquer alteração de campanha continua bloqueada.

## Scheduler recomendado

- iniciar com uma execução manual;
- depois, `weekly_review` nas manhãs de segunda-feira, timezone `America/Sao_Paulo`;
- ativar `daily_health` somente após validar coleta, evento e baseline;
- não criar recorrência enquanto `collector_status` estiver como `meta_cli_not_validated`.

## Privacidade da evidência

A captura recebida também mostra uma janela do WhatsApp com números de telefone e conversas que não são necessários para o diagnóstico. Ela não foi salva no repositório. Em novas capturas, envie apenas a área do Meta Ads Manager ou cubra os dados pessoais antes de compartilhar.
