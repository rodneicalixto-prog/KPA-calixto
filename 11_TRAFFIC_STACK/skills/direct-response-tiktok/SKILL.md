# Skill: Direct Response para TikTok

```yaml
skill:
  id: direct-response-tiktok
  version: "1.0.0"
  updated: "2026-08-26"
  category: paid-traffic
  agents: ["traffic-orchestrator", "creative-analyst", "funnel-analyst", "attribution-auditor"]
  description: "Operação de Direct Response no TikTok com foco em criativo nativo, teste controlado, mensuração e segurança"
```

## Escopo

Esta skill orienta diagnóstico e experimentação. Ela não autoriza publicação, alteração de orçamento, pausa, exclusão ou escrita via API. Números de conta, limites e especificações da plataforma devem ser conferidos na documentação oficial vigente antes da execução.

## Princípios

1. **Criativo primeiro:** formular a hipótese criativa antes de escolher a configuração de entrega.
2. **Nativo, não disfarçado:** adaptar ritmo, enquadramento e linguagem ao contexto da plataforma sem fingir depoimento ou ocultar publicidade.
3. **Uma variável útil por teste:** preservar o DNA vencedor e mudar hook, corpo, prova, CTA, ator ou formato de maneira rastreável.
4. **Economia ponta a ponta:** retenção e clique são sinais intermediários; CPA, receita validada e margem governam escala.
5. **Tracking antes da opinião:** divergências entre plataforma, analytics e backend bloqueiam conclusões econômicas fortes.

## Contexto mínimo

- cliente, oferta, público e país;
- objetivo e evento de otimização;
- conta e fonte de dados identificadas, sem credenciais no documento;
- janela, timezone e moeda;
- baseline e meta econômica do cliente;
- inventário de criativos com hipótese e data de entrada;
- restrições de marca, compliance e aprovação.

Ausências devem ser marcadas como `[DADO AUSENTE]`; não substituir por benchmark genérico.

## Taxonomia criativa

Cada peça recebe um identificador estável e estes campos:

| Campo | Exemplos de classificação |
|---|---|
| Hook | pergunta, demonstração, tensão, contrarian, resultado comprovado |
| Corpo | tutorial, história, comparação, lista, objeção |
| Prova | demonstração, dado verificável, caso aprovado, nenhuma |
| CTA | próximo passo, oferta, captura, compra |
| Formato | creator-led, demo, tela, slideshow, entrevista |
| Awareness | unaware, problem-aware, solution-aware, product-aware, most-aware |

O nome recomendado é `[cliente]_[oferta]_[angulo]_[hook]_[formato]_[versao]_[data]`.

## Leitura do funil

| Camada | Sinais | Decisão possível |
|---|---|---|
| Entrega | gasto, impressões, alcance, frequência | Há entrega suficiente e comparável? |
| Atenção | início, retenção por marco, conclusão | Qual promessa ou trecho perde atenção? |
| Intenção | clique, CTR, visita qualificada | O criativo gera ação coerente? |
| Conversão | avanço, checkout, lead, compra | A mensagem continua funcionando fora do anúncio? |
| Economia | CPA, receita validada, ROAS, margem | O resultado é sustentável? |

## Pipeline de diagnóstico

1. Validar fonte, evento, deduplicação, moeda, timezone e janela.
2. Comparar coortes equivalentes; não misturar versões, objetivos ou períodos incompatíveis.
3. Localizar o primeiro estágio que desviou do baseline.
4. Segmentar por criativo, campanha, placement, dispositivo e dia quando houver volume.
5. Classificar cada conclusão como `fato`, `inferência` ou `lacuna`.
6. Propor no máximo três hipóteses priorizadas por impacto, confiança e esforço.
7. Definir mudança mínima, métrica primária, guardrail, janela e critério de saída.
8. Solicitar aprovação humana antes de qualquer ativação.

## Lateralização

Preservar explicitamente o elemento responsável pela hipótese vencedora e alterar um eixo relevante:

- mesmo hook, novo desenvolvimento;
- mesmo mecanismo, novo hook;
- mesma estrutura, novo contexto de uso;
- mesmo roteiro, novo creator aprovado;
- mesma promessa comprovada, nova demonstração;
- mesmo ângulo, novo formato nativo.

Alterações cosméticas sem nova hipótese não contam como lateralização.

## Saída obrigatória

1. fonte e qualidade dos dados;
2. tabela do funil com atual, baseline e variação;
3. ranking de criativos com volume mínimo declarado;
4. padrões vencedores e perdedores separados de inferências;
5. backlog de testes com uma variável principal;
6. riscos de compliance e tracking;
7. ações propostas, responsável e aprovação necessária;
8. próxima janela de leitura.

## Stop rules

- Tracking inconsistente: interromper decisão econômica e encaminhar para `@attribution-auditor`.
- Claim, prova ou direito de uso incerto: manter a peça bloqueada.
- Ausência de baseline ou meta: permitir exploração, mas não declarar vencedor econômico.
- Qualquer escrita, publicação ou mudança de verba: exigir confirmação humana explícita.
- Dados pessoais ou credenciais no material: remover e registrar incidente conforme a política do projeto.

