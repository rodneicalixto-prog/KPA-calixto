# Playbook de Funil Direct Response

## Objetivo

Diagnosticar e otimizar o caminho `anuncio -> pagina -> checkout -> compra` sem confundir sintoma com causa. Este playbook opera somente com dados reais e mantém alterações de verba ou publicação sob aprovação humana.

## Entradas mínimas

- cliente e `act_id` identificados;
- janela de análise e evento de conversão definidos;
- gasto, impressões, cliques, sessões, checkouts e compras;
- meta de CPA ou ROAS e baseline do cliente;
- mudanças relevantes ocorridas na janela.

Se uma entrada não existir, marcar como `[DADO AUSENTE]` e limitar a conclusão ao estágio observável.

## Funil e métricas

| Estágio | Métricas primárias | Pergunta de decisão |
|---|---|---|
| Entrega | CPM, alcance, frequência | O anúncio está alcançando pessoas suficientes sem saturação? |
| Atenção | hook rate, retenção, CTR | A promessa interrompe e sustenta atenção? |
| Página | sessões, LP view/clique, taxa de avanço | A página mantém a mensagem e conduz ao checkout? |
| Conversão | checkout, compra, CVR, CPA, ROAS | A oferta converte com economia sustentável? |

## Sequência operacional

1. Validar Pixel/CAPI, evento, UTMs, moeda e deduplicação antes de atribuir queda ao criativo.
2. Comparar a janela atual com baseline e período anterior equivalente.
3. Localizar o primeiro estágio que piorou; efeitos posteriores não são causa raiz por padrão.
4. Segmentar por campanha, conjunto, anúncio, posicionamento e dispositivo.
5. Formular no máximo três hipóteses, cada uma com evidência, teste e critério de saída.
6. Priorizar uma mudança por teste para preservar capacidade de atribuição.
7. Observar uma janela compatível com volume e ciclo de conversão antes de decidir.

## Árvore de decisão

- **CPM subiu, CTR estável:** investigar leilão, público, frequência e posicionamento.
- **CTR caiu:** revisar hook, fadiga, promessa e aderência criativo-público.
- **CTR estável, avanço da página caiu:** revisar velocidade, congruência e CTA.
- **Checkout estável, compra caiu:** revisar pagamento, confiança, preço e falhas técnicas.
- **Métricas de plataforma divergentes do backend:** parar otimização econômica e auditar atribuição.

## Saída obrigatória

1. resumo executivo;
2. tabela por estágio com atual, baseline, variação e status;
3. gargalo primário e evidências;
4. lacunas de dados;
5. ações para 24 horas e 7 dias, com responsável;
6. condição de sucesso, kill criterion e próxima leitura.

## Guardrails

- Não inventar benchmark ou preencher lacuna com média de mercado.
- Não pausar, publicar ou alterar orçamento sem confirmação.
- Não escalar com tracking inconclusivo.
- Não declarar causalidade quando os dados sustentam apenas correlação.

