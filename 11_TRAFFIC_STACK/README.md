# 11_TRAFFIC_STACK — Traffic Stack do Kit Piloto Automático V30

> Stack expandida de agentes especializados em tráfego pago Direct Response, análise de campanhas, criativos, funil, atribuição, escala e inteligência competitiva. Opera sobre o CLI nativo `meta` (WSL no Windows / nativo no macOS-Linux) e complementa os agents do V30.

## Por que esta camada existe

O resto do V30 (CoS + agents de copy + pipeline) é orientado a **planejamento e criação** de campanhas (briefing → estrutura → copy → criativos → subir). A Traffic Stack é orientada a **operação contínua** sobre campanhas vivas:

- Diagnóstico de queda de performance
- Análise de criativos (hook rate, retention, padrões vencedores)
- Auditoria de tracking (Pixel + CAPI saúde)
- Escala de vencedores (ABO/CBO/lateralização)
- Inteligência competitiva (Meta Ad Library, swipe, benchmark)
- Análise de funil end-to-end (ads → LP → VSL → quiz → checkout)

E faz isso conectada ao CLI `meta` oficial, permitindo puxar dados reais e gerar relatórios de campanhas vivas — não só planejar campanhas novas. Pra instalar o CLI do zero, rode `/meta-cli-install` dentro do Claude Code (cobre Windows via WSL Ubuntu e macOS/Linux nativo).

## Arquitetura

```
┌────────────────────────────────────────────────────────────────┐
│  L0 — Orquestração                                              │
│  @traffic-orchestrator (chief da stack)                         │
└──────────────┬──────────────────────────────────────────────────┘
               │
   ┌───────────┴───────────┬─────────────┬────────────┬──────────┐
   ▼                       ▼             ▼            ▼          ▼
┌──────────────┐  ┌─────────────────┐  ┌──────────┐  ┌──────────────┐  ┌──────────────┐
│ Execução     │  │ Análise         │  │ Tracking │  │ Otimização   │  │ Intel        │
├──────────────┤  ├─────────────────┤  ├──────────┤  ├──────────────┤  ├──────────────┤
│ @meta-dr-    │  │ @creative-      │  │ @attrib- │  │ @traffic-    │  │ @competitor- │
│ specialist   │  │ analyst         │  │ ution-   │  │ diagnostician│  │ spy          │
│              │  │                 │  │ auditor  │  │              │  │              │
│              │  │ @funnel-analyst │  │          │  │ @scaling-    │  │              │
│              │  │                 │  │          │  │ strategist   │  │              │
└──────────────┘  └─────────────────┘  └──────────┘  └──────────────┘  └──────────────┘
                          │
                          ▼
                  Reaproveita @traffic-analyst (V30)
                  para relatórios consolidados
```

### Os 8 agentes

| # | Agente | Responsabilidade |
|---|---|---|
| 1 | `@traffic-orchestrator` | Recebe pedido, detecta cliente, lê context, roteia |
| 2 | `@meta-dr-specialist` | Direct Response Meta — broad targeting, criativo-first, kill criteria, lateralização Oxigênio |
| 3 | `@creative-analyst` | Hook rate, retention curve, padrões vencedores, gera lateralizações |
| 4 | `@funnel-analyst` | Funil completo: ads → LP → VSL → quiz → checkout. Identifica drop-off |
| 5 | `@attribution-auditor` | Pixel + CAPI saúde, match quality, deduplicação, atribuição |
| 6 | `@traffic-diagnostician` | Investigação forensic de queda — root cause analysis |
| 7 | `@scaling-strategist` | Quando escalar, quanto, qual método (ABO/CBO/Oxigênio/horizontal) |
| 8 | `@competitor-spy` | Meta Ad Library, BigSpy, swipe, engenharia reversa de funis |

## Estrutura de pastas

```
11_TRAFFIC_STACK/
├── README.md                             # Este arquivo
├── agents/                               # 8 definições de agente
│   ├── traffic-orchestrator.md
│   ├── meta-dr-specialist.md
│   ├── creative-analyst.md
│   ├── funnel-analyst.md
│   ├── attribution-auditor.md
│   ├── traffic-diagnostician.md
│   ├── scaling-strategist.md
│   └── competitor-spy.md
├── tasks/                                # Tasks operacionais
│   ├── diagnosticar-campanha-meta-cli.md
│   ├── diagnosticar-google-ads.md
│   ├── operacao-agendada-trafego.md
│   ├── analisar-criativos.md             # DNA do vencedor, lateralizacao, kill list
│   ├── investigar-queda.md               # Root cause analysis em 6 camadas
│   ├── escalar-vencedores.md             # ABO/CBO/Oxigenio/horizontal/multi-account
│   └── espionar-concorrente.md           # Meta Ad Library, swipe, engenharia reversa
├── skills/
│   ├── direct-response-br/SKILL.md       # DR brasileiro: ABO, CBO, Oxigênio, kill criteria
│   ├── direct-response-tiktok/SKILL.md   # Diagnóstico e experimentação TikTok DR
│   └── meta-cli-install/SKILL.md         # Instalação segura do CLI Meta
├── playbooks/
│   ├── direct-response-flow.md
│   ├── quiz-funnel-flow.md
│   └── vsl-flow.md
├── templates/
    ├── relatorio-diagnostico-tmpl.html
    ├── relatorio-criativos-tmpl.html
    ├── relatorio-meta-ads-tmpl.html       # Relatório Meta responsivo e imprimível
    ├── google-ads-insights-schema.yaml     # Contrato normalizado somente leitura
    ├── meta-ads-insights-schema.json       # Contrato de export Meta somente leitura
    ├── schedule-template.yaml             # Agenda desativada e read-only por padrão
    ├── schedule-runtime-template.json     # Configuração executável, desativada por padrão
    └── cliente-template/                 # Template pra novo cliente em 05_WORKSPACE/clientes/
        ├── CLAUDE.md
        ├── act-mapping.yaml
        ├── icp.md
        ├── funil.md
        └── baseline-kpis.md
├── tests/
│   ├── validate_stack.py                  # Validação estrutural sem dependências externas
│   ├── test_activate_traffic_job.py        # Testes da ativação explícita
│   ├── test_google_ads_export.py          # Testes do contrato Google Ads
│   ├── test_google_ads_report.py          # Testes end-to-end do relatório
│   ├── test_meta_ads_export.py             # Testes do gate de export Meta Ads
│   ├── test_meta_ads_report.py             # Testes end-to-end do relatório Meta
│   ├── test_init_traffic_client.py         # Testes de criação segura do workspace
│   ├── test_preflight_traffic_client.py    # Testes do preflight read-only
│   ├── test_scheduled_traffic.py           # Testes do executor local
│   └── fixtures/google-ads-valid.json      # Export anonimizado para execução local
├── tools/
│   ├── validate_google_ads_export.py      # Gate executável para export normalizado
│   ├── validate_meta_ads_export.py        # Gate seguro para export Meta normalizado
│   ├── render_meta_ads_report.py          # Renderer HTML Meta após o gate
│   ├── activate_traffic_job.py            # Ativação após preflight e confirmação exata
│   ├── render_google_ads_report.py        # Renderer HTML após aprovação do gate
│   ├── init_traffic_client.py             # Inicializador sem credenciais e sem overwrite
│   ├── preflight_traffic_client.py        # Gate antes de configurar execução
│   ├── deploy_traffic_kit.py               # Implanta manifesto local sem ativar integrações
│   └── run_scheduled_traffic.py           # Executor allowlisted, dry-run por padrão
```

## Integração com o resto do V30

- **Reusa `@traffic-analyst`** (V30) — relatórios consolidados, dashboards, projeções
- **Reusa diretrizes** em `04_DIRETRIZES/` carregadas sob demanda — conhecimento técnico Meta
- **Reusa `@cos`** (entry point V30) — `@cos` roteia tráfego pra `@traffic-orchestrator`
- **Lê `05_WORKSPACE/clientes/<cliente>/`** sempre — context obrigatório por cliente
- **Conecta com CLI nativo `meta`** — toda análise puxa dados reais

## Multi-conta — como funciona

A stack é multi-conta por design:

1. **`00_OS/clients-map.yaml`** — mapeia cada `act_id` Meta para um cliente do V30 (criar conforme necessário)
2. **`05_WORKSPACE/clientes/<cliente>/act-mapping.yaml`** — mapeia todas as contas de um cliente (alguns têm múltiplas)
3. **CLI** — `meta ads <recurso> <ação> --ad-account-id act_XXXXXXXXXXXXXXX` por comando
4. **Token** — System User Token (gerado no Business Manager) precisa ter acesso a TODAS as contas. NUNCA hardcoded — vive no `.env` (gitignored) ou no `~/.profile` do WSL

## Convenções

- Todos os agentes operam em **pt-BR** (greeting, output, prompts)
- Saída padrão: **HTML visual** (relatórios) ou **markdown estruturado** (briefings táticos)
- **Ações destrutivas** (pause, delete, budget mudança >20%): confirmação manual obrigatória, mesmo em auto mode
- **Dados reais sempre** — nenhum agente inventa número. Se CLI falhar, agente reporta erro e para
- **Frameworks Tier 1 padronizados** — todos seguem (1) DRE 5 níveis (2) Funil 4 estágios (3) Diagnóstico Onde Quebrou (4) Andrômeda Era (Meta v25)

## Roadmap

### Sprint 1 (concluído — Maio 2026)
- [x] Estrutura `11_TRAFFIC_STACK/` criada
- [x] 8 agentes definidos
- [x] Task `diagnosticar-campanha-meta-cli.md`
- [x] Skill `direct-response-br`
- [ ] Cliente piloto definido pelo operador

### Sprint 2 (concluído parcialmente — Agosto 2026)
- [x] Template de cliente para `05_WORKSPACE/clientes/`
- [x] Inicializador executável de workspace do cliente
- [x] Preflight executável e persistência atômica do estado
- [ ] Instanciar cliente piloto em `05_WORKSPACE/clientes/` (depende da definição do operador)
- [x] Templates HTML de relatório
- [x] Playbooks de funil (DR, Quiz, VSL)

### Sprint 3 (atual — Agosto 2026)
- [x] Contrato de integração Google Ads somente leitura e schema normalizado
- [x] Gate executável e testes do export normalizado Google Ads
- [x] Execução offline de ponta a ponta até relatório HTML
- [ ] Ativar coletor Google Ads para cliente piloto (depende de setup e acessos)
- [x] Skill `direct-response-tiktok`
- [x] Contrato e template de auto-execução agendada (desativada e read-only por padrão)
- [x] Executor local com dry-run, allowlist e bloqueio de configurações inseguras
- [x] Gate de ativação explícita após preflight aprovado
- [ ] Instalar recorrência diária/semanal para cliente piloto (depende do scheduler do operador)

## Validação

Execute a validação estrutural sem instalar dependências:

```bash
python3 11_TRAFFIC_STACK/tests/validate_stack.py
python3 -m unittest discover -s 11_TRAFFIC_STACK/tests -p 'test_*.py'
```

## Inicializar cliente

Crie o workspace sem informar credenciais nem o ID completo da conta:

```bash
python3 11_TRAFFIC_STACK/tools/init_traffic_client.py \
  --slug cliente-exemplo \
  --name "Cliente Exemplo" \
  --account-suffix 1234
```

O inicializador não sobrescreve pastas existentes. A agenda nasce em `draft`, desativada e sem permissão de escrita.

Implante e registre todos os componentes locais do kit, mantendo integrações externas desativadas:

```bash
python3 11_TRAFFIC_STACK/tools/deploy_traffic_kit.py \
  05_WORKSPACE/clientes/cliente-exemplo --apply
```

O manifesto diferencia componentes instalados de integrações ainda pendentes. Ele nunca instala credenciais, ativa jobs ou escreve em plataformas.

Depois de receber um export normalizado, audite o workspace sem alterá-lo:

```bash
python3 11_TRAFFIC_STACK/tools/preflight_traffic_client.py \
  05_WORKSPACE/clientes/cliente-exemplo \
  --export caminho/export.json \
  --collector-source "exportacao-validada" \
  --conversion-action "purchase" \
  --owner "Responsável"
```

Acrescente `--apply` somente depois de revisar o resultado. Mesmo aplicado, o preflight mantém todos os jobs desativados.

Ative um job somente após o preflight:

```bash
python3 11_TRAFFIC_STACK/tools/activate_traffic_job.py \
  05_WORKSPACE/clientes/cliente-exemplo \
  --job weekly_review \
  --confirm "ATIVAR SOMENTE LEITURA"
```

O comando habilita somente o job selecionado. Ele não instala cron, não coleta dados e não concede acesso à plataforma.

## Versão

- **v2.2.0** — 2026-08-26 — Relatório HTML Meta Ads validado e seguro
- **v2.1.0** — 2026-08-26 — Contrato e gate de export Meta Ads somente leitura
- **v2.0.0** — 2026-08-26 — Implantação auditável do kit local por cliente
- **v1.9.0** — 2026-08-26 — Ativação explícita e state gate no executor local
- **v1.8.0** — 2026-08-26 — Preflight executável para ativação read-only
- **v1.7.0** — 2026-08-26 — Inicializador seguro de workspace para cliente piloto
- **v1.6.0** — 2026-08-26 — Executor local seguro para jobs de tráfego
- **v1.5.0** — 2026-08-26 — Execução offline e relatório HTML para Google Ads
- **v1.4.0** — 2026-08-26 — Gate executável e testes para exports Google Ads
- **v1.3.0** — 2026-08-26 — Contrato Google Ads somente leitura e schema normalizado
- **v1.2.0** — 2026-08-26 — Skill TikTok DR, contrato de agendamento seguro e validação automatizada
- **v1.1.0** — 2026-08-26 — Templates de cliente e relatório; playbooks DR, Quiz e VSL
- **v1.0.0** — 2026-05-04 — Criação inicial
