#!/usr/bin/env python3
"""Valida a integridade estrutural dos artefatos da Traffic Stack."""

from __future__ import annotations

from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[2]
STACK = ROOT / "11_TRAFFIC_STACK"

EXPECTED_FILES = (
    "agents/attribution-auditor.md",
    "agents/competitor-spy.md",
    "agents/creative-analyst.md",
    "agents/funnel-analyst.md",
    "agents/meta-dr-specialist.md",
    "agents/scaling-strategist.md",
    "agents/traffic-diagnostician.md",
    "agents/traffic-orchestrator.md",
    "playbooks/direct-response-flow.md",
    "playbooks/quiz-funnel-flow.md",
    "playbooks/vsl-flow.md",
    "skills/direct-response-br/SKILL.md",
    "skills/direct-response-tiktok/SKILL.md",
    "skills/meta-cli-install/SKILL.md",
    "tasks/diagnosticar-campanha-meta-cli.md",
    "tasks/diagnosticar-google-ads.md",
    "tasks/operacao-agendada-trafego.md",
    "templates/cliente-template/CLAUDE.md",
    "templates/cliente-template/act-mapping.yaml",
    "templates/cliente-template/baseline-kpis.md",
    "templates/cliente-template/funil.md",
    "templates/cliente-template/icp.md",
    "templates/google-ads-insights-schema.yaml",
    "templates/meta-ads-insights-schema.json",
    "templates/relatorio-criativos-tmpl.html",
    "templates/relatorio-diagnostico-tmpl.html",
    "templates/relatorio-meta-ads-tmpl.html",
    "templates/schedule-template.yaml",
    "templates/schedule-runtime-template.json",
    "tests/fixtures/google-ads-valid.json",
    "tests/fixtures/meta-ads-terra-fibra-valid.json",
    "tests/test_activate_traffic_job.py",
    "tests/test_init_traffic_client.py",
    "tests/test_preflight_traffic_client.py",
    "tests/test_google_ads_export.py",
    "tests/test_google_ads_report.py",
    "tests/test_meta_ads_export.py",
    "tests/test_meta_ads_report.py",
    "tests/test_scheduled_traffic.py",
    "tests/test_deploy_traffic_kit.py",
    "tools/validate_google_ads_export.py",
    "tools/validate_meta_ads_export.py",
    "tools/render_meta_ads_report.py",
    "tools/activate_traffic_job.py",
    "tools/render_google_ads_report.py",
    "tools/init_traffic_client.py",
    "tools/preflight_traffic_client.py",
    "tools/run_scheduled_traffic.py",
    "tools/deploy_traffic_kit.py",
)

REQUIRED_PLACEHOLDERS = {
    "relatorio-diagnostico-tmpl.html": {
        "CLIENTE",
        "JANELA_ANALISE",
        "RESUMO_EXECUTIVO",
        "FUNNEL_ROWS",
        "ACTION_ROWS",
        "FONTES_DADOS",
    },
    "relatorio-criativos-tmpl.html": {
        "CLIENTE",
        "JANELA_ANALISE",
        "RESUMO_EXECUTIVO",
        "RANKING_ROWS",
        "CREATIVE_CARDS",
        "VARIATION_ROWS",
        "FONTES_DADOS",
    },
    "relatorio-meta-ads-tmpl.html": {
        "CLIENTE", "JANELA", "CONTA", "INVESTIMENTO", "RESULTADOS",
        "CUSTO_RESULTADO", "CTR_LINK", "RESUMO", "CAMPANHAS", "LACUNAS",
    },
}


class DocumentParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.html_language: str | None = None
        self.has_viewport = False
        self.has_main = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        if tag == "html":
            self.html_language = attributes.get("lang")
        elif tag == "meta" and attributes.get("name") == "viewport":
            self.has_viewport = True
        elif tag == "main":
            self.has_main = True


def validate_expected_files(errors: list[str]) -> None:
    for relative_path in EXPECTED_FILES:
        path = STACK / relative_path
        if not path.is_file():
            errors.append(f"arquivo ausente: {relative_path}")
        elif path.stat().st_size == 0:
            errors.append(f"arquivo vazio: {relative_path}")


def validate_html(errors: list[str]) -> None:
    for filename, required in REQUIRED_PLACEHOLDERS.items():
        path = STACK / "templates" / filename
        if not path.is_file():
            continue
        content = path.read_text(encoding="utf-8")
        parser = DocumentParser()
        parser.feed(content)
        parser.close()
        if parser.html_language != "pt-BR":
            errors.append(f"{filename}: lang deve ser pt-BR")
        if not parser.has_viewport:
            errors.append(f"{filename}: meta viewport ausente")
        if not parser.has_main:
            errors.append(f"{filename}: elemento main ausente")
        placeholders = set(re.findall(r"\{\{([A-Z0-9_]+)\}\}", content))
        missing = sorted(required - placeholders)
        if missing:
            errors.append(f"{filename}: placeholders ausentes: {', '.join(missing)}")


def validate_safety(errors: list[str]) -> None:
    schedule = (STACK / "templates" / "schedule-template.yaml").read_text(encoding="utf-8")
    required_rules = (
        "status: \"draft\"",
        "read_only: true",
        "allow_platform_writes: false",
        "require_human_approval: true",
        "enabled: false",
    )
    for rule in required_rules:
        if rule not in schedule:
            errors.append(f"schedule-template.yaml: regra de segurança ausente: {rule}")

    runtime_path = STACK / "templates" / "schedule-runtime-template.json"
    try:
        runtime = json.loads(runtime_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, ValueError) as error:
        errors.append(f"schedule-runtime-template.json: JSON inválido: {error}")
    else:
        safety = runtime.get("safety", {})
        if runtime.get("status") != "draft":
            errors.append("schedule-runtime-template.json: status deve ser draft")
        if any(job.get("enabled") is not False for job in runtime.get("jobs", [])):
            errors.append("schedule-runtime-template.json: jobs devem iniciar desativados")
        if safety.get("read_only") is not True:
            errors.append("schedule-runtime-template.json: read_only deve ser true")
        if safety.get("allow_platform_writes") is not False:
            errors.append("schedule-runtime-template.json: escrita deve estar bloqueada")

    google_schema = (STACK / "templates" / "google-ads-insights-schema.yaml").read_text(
        encoding="utf-8"
    )
    google_rules = (
        "mode: \"read_only\"",
        "customer_id_masked:",
        "conversion_definition_confirmed: false",
        "contains_credentials: false",
        "contains_personal_data: false",
        "platform_writes_allowed: false",
        "human_approval_required: true",
    )
    for rule in google_rules:
        if rule not in google_schema:
            errors.append(
                f"google-ads-insights-schema.yaml: regra obrigatória ausente: {rule}"
            )

    meta_path = STACK / "templates" / "meta-ads-insights-schema.json"
    try:
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, ValueError) as error:
        errors.append(f"meta-ads-insights-schema.json: JSON inválido: {error}")
    else:
        meta_safety = meta.get("safety", {})
        if meta.get("platform") != "meta_ads" or meta.get("mode") != "read_only":
            errors.append("meta-ads-insights-schema.json: plataforma/modo inválidos")
        if meta_safety.get("platform_writes_allowed") is not False:
            errors.append("meta-ads-insights-schema.json: escrita deve estar bloqueada")
        if meta_safety.get("contains_credentials") is not False:
            errors.append("meta-ads-insights-schema.json: credenciais devem estar ausentes")


def main() -> int:
    errors: list[str] = []
    validate_expected_files(errors)
    validate_html(errors)
    validate_safety(errors)
    if errors:
        print("Traffic Stack inválida:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"Traffic Stack válida: {len(EXPECTED_FILES)} artefatos verificados.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
