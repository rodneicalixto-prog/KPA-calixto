# Playbook de Funil Quiz

## Objetivo

Encontrar a etapa responsável pela perda entre o clique no anúncio e a conversão final em funis com perguntas, captura de lead e página de resultado.

## Eventos esperados

`ad_click -> quiz_view -> quiz_start -> question_answered -> quiz_complete -> lead -> result_view -> checkout -> purchase`

Cada evento deve registrar, quando permitido, `session_id`, origem/UTM, versão do quiz, número da pergunta e timestamp. Dados pessoais não devem aparecer no relatório.

## Métricas por etapa

| Etapa | Fórmula |
|---|---|
| Início | `quiz_start / quiz_view` |
| Retenção por pergunta | `respostas da pergunta N / respostas da pergunta N-1` |
| Conclusão | `quiz_complete / quiz_start` |
| Captura | `lead / quiz_complete` |
| Resultado para checkout | `checkout / result_view` |
| Conversão final | `purchase / quiz_start` |

## Sequência operacional

1. Validar a ordem e unicidade dos eventos em uma sessão de teste.
2. Construir coortes por versão do quiz, campanha, dispositivo e dia.
3. Calcular drop-off absoluto e relativo em cada pergunta.
4. Identificar o primeiro ponto de queda anormal contra o baseline da mesma origem.
5. Revisar nesse ponto: clareza, esforço, sensibilidade da pergunta, interface e tempo de carregamento.
6. Separar problema de aquisição de problema interno: CTR baixo precede o quiz; abandono após `quiz_start` pertence ao quiz.
7. Propor um teste isolado e definir amostra/janela antes da execução.

## Diagnósticos comuns

- **Muitas views, poucos starts:** promessa de entrada incongruente ou CTA inicial fraco.
- **Queda concentrada em uma pergunta:** esforço, ambiguidade ou dado sensível pedido cedo demais.
- **Boa conclusão, baixa captura:** valor do resultado não justifica fornecer contato.
- **Boa captura, pouco checkout:** transição ou oferta da página de resultado está fraca.
- **Eventos fora de ordem/duplicados:** auditoria de tracking precede qualquer otimização.

## Saída obrigatória

- mapa do funil com volumes e taxas;
- drop-off por pergunta e segmento;
- gargalo primário com evidência;
- hipótese, variante, métrica primária e guardrail do teste;
- lacunas de instrumentação;
- responsável e data da próxima leitura.

## Guardrails

- Não remover consentimento nem ocultar finalidade da captura.
- Não coletar dado sensível sem necessidade e base adequada.
- Não comparar versões com mix de tráfego incompatível sem sinalizar o viés.
- Não mudar várias perguntas no mesmo teste quando o objetivo é descobrir causalidade.

