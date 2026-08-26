# Revisão do change set Meta — Terra Fibra

**Arquivo estruturado:** `05_WORKSPACE/clientes/terra-fibra/meta-change-set-draft.json`  
**Status:** aprovado por Rodnei em 26/08/2026, ainda não aplicado.

## O que o rascunho fará quando aprovado

1. Preservar o conjunto original `CS | Todas cidades | WhatsApp` para rollback.
2. Criar uma cópia chamada `CS | Cobertura validada | WhatsApp | v1`.
3. Manter o orçamento observado de R$ 21,54/dia durante a validação, sem escala.
4. Trocar `Todas cidades` pelas 21 cidades informadas pela operação.
5. Revisar a opção de presença geográfica e qualquer expansão automática.
6. Usar comunicação de `regiões selecionadas`, sem prometer cobertura integral.
7. Consultar cidade, bairro e CEP no WhatsApp antes de avançar.
8. Manter o novo conjunto como rascunho até aprovação final de Rodnei.

## O que o rascunho não fará

- não reativará a campanha;
- não publicará os 15 rascunhos existentes;
- não descartará alterações antigas;
- não aumentará orçamento;
- não prometerá cobertura por cidade sem geolocalização;
- não armazenará IDs completos ou credenciais.

## Revisão manual no Meta

Ao selecionar cada cidade, confirmar que o resultado da busca corresponde ao município de **São Paulo, Brasil**. Não selecionar regiões homônimas, raios automáticos ou agrupamentos sem revisão.

Para cada uma das 21 cidades:

- [ ] município correto selecionado;
- [ ] estado SP confirmado;
- [ ] nenhum raio adicional aplicado sem intenção;
- [ ] estimativa de público revisada;
- [ ] cobertura operacional ainda válida.

## Bloqueios atuais

1. Os IDs internos de localização do Meta ainda não foram resolvidos.
2. A opção de presença geográfica mais restritiva ainda não foi confirmada na interface.
3. Expansões automáticas/Advantage ainda não foram auditadas.
4. Os 15 rascunhos desconhecidos continuam sem auditoria e em quarentena.

## Aprovação necessária

Decisões registradas por Rodnei em 26/08/2026:

```text
Aprovo as 21 cidades: sim
Aprovo manter orçamento de R$ 21,54/dia no teste: sim
Aprovo a copy de consulta de cobertura: sim
Aprovo o fluxo WhatsApp cidade/bairro/CEP: sim
Os 15 rascunhos foram auditados: não
```

As quatro aprovações permitem preparar a configuração manual. Elas **não** autorizam publicar, reativar a campanha ou operar os 15 rascunhos. O gate permanece bloqueado até a auditoria dos rascunhos e a conferência das entidades geográficas, da presença e da expansão na interface do Meta.
