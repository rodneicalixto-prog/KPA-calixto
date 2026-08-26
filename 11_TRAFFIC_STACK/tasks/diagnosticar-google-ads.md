# Task: Diagnosticar Google Ads em Modo Somente Leitura

## Objetivo

Normalizar uma exportação validada do Google Ads, verificar sua qualidade e produzir diagnóstico usando os mesmos gates da Traffic Stack. Esta task não assume a existência de um CLI oficial específico e não executa comandos de escrita.

## Contrato do adaptador

O coletor escolhido pelo operador deve:

1. autenticar fora do repositório;
2. receber conta, janela e nível de agregação explicitamente;
3. operar apenas com permissão de leitura;
4. devolver dados no formato de `templates/google-ads-insights-schema.yaml`;
5. registrar fonte, horário, timezone e moeda;
6. retornar código diferente de zero ou status `failed` quando a coleta for incompleta;
7. nunca imprimir token, segredo ou identificador de conta completo nos logs.

Podem ser usados um conector aprovado, exportação manual ou wrapper local mantido pelo operador. O método precisa ser registrado em `source`; a task não inventa um comando universal.

## Preflight bloqueante

- cliente e conta identificados;
- acesso somente leitura testado pelo operador;
- janela, timezone e moeda confirmados;
- ação de conversão e regra de valor documentadas;
- baseline do cliente disponível ou marcado como `[DADO AUSENTE]`;
- saída compatível com o schema;
- responsável humano e diretório de saída definidos.

Se qualquer item que comprometa interpretação ou segurança falhar, devolver `data_quality: blocked`.

Antes do diagnóstico, valide o JSON normalizado:

```bash
python3 11_TRAFFIC_STACK/tools/validate_google_ads_export.py caminho/export.json
```

Os códigos de saída são `0` para aprovado, `1` para contrato bloqueado e `2` para erro de leitura ou JSON inválido.

Depois da aprovação, gere o relatório sem executar ações na conta:

```bash
python3 11_TRAFFIC_STACK/tools/render_google_ads_report.py \
  caminho/export.json \
  06_OUTPUTS/cliente/traffic/diagnostico-google-ads.html \
  --client "Nome público do cliente"
```

O renderer escapa conteúdo vindo do export, recalcula os totais consolidados e se recusa a produzir o arquivo quando o gate falha.

## Validação dos dados

1. Confirmar que `window_start <= window_end` e que o timezone é conhecido.
2. Rejeitar métricas negativas para impressões, cliques, custo, conversões e valor.
3. Confirmar `clicks <= impressions` quando ambas representam o mesmo escopo.
4. Recalcular CTR, CPC, custo por conversão e valor/custo a partir dos campos-base.
5. Sinalizar divisão por zero como `not_applicable`, nunca como zero econômico.
6. Conciliar totais com a fonte; diferenças permanecem visíveis em `quality.notes`.
7. Não somar linhas de níveis diferentes no mesmo total.
8. Não comparar campanhas de canais/objetivos incompatíveis sem segmentação explícita.

No contrato normalizado, taxas como `ctr` usam razão decimal (`0.10` representa 10%). Valores monetários usam a moeda declarada em `run.currency`, nunca unidades mínimas implícitas.

## Pipeline de diagnóstico

1. Salvar a entrada normalizada em área de trabalho definida pelo cliente.
2. Executar o gate de qualidade acima.
3. Comparar janela atual, período anterior equivalente e baseline, quando disponíveis.
4. Separar leitura por campanha e `channel_type`.
5. Localizar o primeiro estágio observável que desviou do baseline.
6. Classificar conclusões como `fato`, `inferência` ou `lacuna`.
7. Produzir no máximo três ações propostas com evidência, responsável e critério de sucesso.
8. Gerar o relatório pelo template de diagnóstico sem executar as ações.

## Saída obrigatória

- identidade mascarada da conta e origem da coleta;
- janela, moeda, timezone e definição de conversão;
- resultado do gate de qualidade;
- tabela atual versus baseline/período anterior;
- gargalo primário e evidências;
- fatos, inferências e lacunas em blocos separados;
- ações propostas para 24 horas e 7 dias;
- aprovação necessária e próxima leitura.

## Guardrails

- Nenhuma credencial entra no kit, relatório ou log.
- Nenhuma recomendação é aplicada automaticamente.
- Mudança de budget, bid, status, anúncio ou segmentação exige aprovação explícita.
- A task para quando a definição de conversão ou a moeda estiver ambígua.
- Especificações e autenticação devem ser conferidas na documentação oficial vigente do método escolhido.
