#!/usr/bin/env python3
"""Gera relatório HTML seguro a partir de export Meta Ads aprovado."""

from __future__ import annotations

import argparse
from html import escape
import importlib.util
import json
from pathlib import Path
import re
import sys
from typing import Any


STACK = Path(__file__).resolve().parents[1]
DEFAULT_TEMPLATE = STACK / "templates" / "relatorio-meta-ads-tmpl.html"
VALIDATOR_PATH = Path(__file__).with_name("validate_meta_ads_export.py")
TOKENS = ("CLIENTE", "JANELA", "CONTA", "INVESTIMENTO", "RESULTADOS", "CUSTO_RESULTADO", "CTR_LINK", "RESUMO", "CAMPANHAS", "LACUNAS")


def validator() -> Any:
    spec = importlib.util.spec_from_file_location("meta_validator", VALIDATOR_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("validador Meta Ads indisponível")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def br_number(value: float, digits: int = 2) -> str:
    return f"{value:,.{digits}f}".replace(",", "_").replace(".", ",").replace("_", ".")


def build(payload: dict[str, Any], client: str) -> dict[str, str]:
    campaigns = payload["campaigns"]
    spend = sum(float(row["spend_brl"]) for row in campaigns)
    impressions = sum(int(row["impressions"]) for row in campaigns)
    clicks = sum(int(row["link_clicks"]) for row in campaigns)
    results = sum(float(row["results"]) for row in campaigns)
    cpr = spend / results if results else None
    ctr = clicks / impressions * 100 if impressions else None
    rows = []
    for row in campaigns:
        cells = (
            escape(row["campaign_name"]), escape(row["status"]), f"R$ {br_number(float(row['spend_brl']))}",
            br_number(float(row["impressions"]), 0), br_number(float(row["reach"]), 0),
            br_number(float(row["link_clicks"]), 0), br_number(float(row["results"]), 0),
        )
        rows.append("<tr>" + "".join(f"<td>{cell}</td>" for cell in cells) + "</tr>")
    attribution = payload["attribution"]
    confirmed = attribution["definition_confirmed"]
    return {
        "CLIENTE": escape(client),
        "JANELA": f"{escape(payload['window']['start'])} a {escape(payload['window']['end'])}",
        "CONTA": escape(payload["account_id_masked"]),
        "INVESTIMENTO": f"R$ {br_number(spend)}",
        "RESULTADOS": br_number(results, 0),
        "CUSTO_RESULTADO": "N/A" if cpr is None else f"R$ {br_number(cpr)}",
        "CTR_LINK": "N/A" if ctr is None else f"{br_number(ctr)}%",
        "RESUMO": escape(f"Export somente leitura aprovado com {len(campaigns)} campanha(s) e {br_number(results, 0)} resultado(s)."),
        "CAMPANHAS": "".join(rows),
        "LACUNAS": escape("Definição de atribuição confirmada." if confirmed else "Definição do resultado/atribuição ainda requer confirmação humana no Meta Ads Manager."),
    }


def render(template: str, replacements: dict[str, str]) -> str:
    output = template
    for token in TOKENS:
        marker = "{{" + token + "}}"
        if marker not in output:
            raise ValueError(f"template sem placeholder: {marker}")
        output = output.replace(marker, replacements[token])
    if re.search(r"\{\{[A-Z0-9_]+\}\}", output):
        raise ValueError("template contém placeholders não resolvidos")
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("export", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--client", required=True)
    parser.add_argument("--template", type=Path, default=DEFAULT_TEMPLATE)
    args = parser.parse_args()
    try:
        payload = json.loads(args.export.read_text(encoding="utf-8"))
        template = args.template.read_text(encoding="utf-8")
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        print(f"erro de entrada: {error}", file=sys.stderr)
        return 2
    errors = validator().validate_payload(payload)
    if errors:
        print("relatório bloqueado pelo contrato Meta Ads:", file=sys.stderr)
        return 1
    try:
        html = render(template, build(payload, args.client))
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(html, encoding="utf-8")
    except (KeyError, OSError, ValueError) as error:
        print(f"erro ao gerar relatório: {error}", file=sys.stderr)
        return 2
    print(f"Relatório Meta Ads gerado: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
