#!/usr/bin/env python3
"""Gera relatório HTML a partir de um export Google Ads aprovado."""

from __future__ import annotations

import argparse
from decimal import Decimal
from html import escape
import importlib.util
import json
from pathlib import Path
import sys
from typing import Any


STACK = Path(__file__).resolve().parents[1]
DEFAULT_TEMPLATE = STACK / "templates" / "relatorio-diagnostico-tmpl.html"
VALIDATOR_PATH = Path(__file__).with_name("validate_google_ads_export.py")
PLACEHOLDERS = (
    "CLIENTE",
    "JANELA_ANALISE",
    "DATA_GERACAO",
    "ACT_ID",
    "SPEND",
    "DELTA_SPEND",
    "CPA",
    "DELTA_CPA",
    "ROAS",
    "DELTA_ROAS",
    "PURCHASES",
    "DELTA_PURCHASES",
    "RESUMO_EXECUTIVO",
    "FUNNEL_ROWS",
    "GARGALO",
    "EVIDENCIAS",
    "ACTION_ROWS",
    "LACUNAS_RISCOS",
    "FONTES_DADOS",
)


def load_validator() -> Any:
    spec = importlib.util.spec_from_file_location("google_ads_export_validator", VALIDATOR_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("não foi possível carregar o validador Google Ads")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def decimal(value: Any) -> Decimal:
    return Decimal(str(value))


def format_number(value: Decimal, digits: int = 2) -> str:
    rendered = f"{value:,.{digits}f}"
    return rendered.replace(",", "_").replace(".", ",").replace("_", ".")


def format_money(value: Decimal, currency: str) -> str:
    prefix = "R$" if currency == "BRL" else currency
    return f"{prefix} {format_number(value)}"


def aggregate(rows: list[dict[str, Any]]) -> dict[str, Decimal | None]:
    impressions = sum((decimal(row["impressions"]) for row in rows), Decimal(0))
    clicks = sum((decimal(row["clicks"]) for row in rows), Decimal(0))
    cost = sum((decimal(row["cost"]) for row in rows), Decimal(0))
    conversions = sum((decimal(row["conversions"]) for row in rows), Decimal(0))
    value = sum((decimal(row["conversion_value"]) for row in rows), Decimal(0))
    return {
        "impressions": impressions,
        "clicks": clicks,
        "cost": cost,
        "conversions": conversions,
        "value": value,
        "ctr": clicks / impressions if impressions else None,
        "cpc": cost / clicks if clicks else None,
        "cpa": cost / conversions if conversions else None,
        "roas": value / cost if cost else None,
    }


def metric_or_na(value: Decimal | None, suffix: str = "") -> str:
    if value is None:
        return "N/A"
    return f"{format_number(value)}{suffix}"


def campaign_rows(rows: list[dict[str, Any]], currency: str) -> str:
    rendered: list[str] = []
    for row in sorted(rows, key=lambda item: decimal(item["cost"]), reverse=True):
        values = (
            "Campanha",
            escape(str(row["campaign_name"])),
            format_money(decimal(row["cost"]), currency),
            "N/A",
            f"{format_number(decimal(row['conversions']))} conversões",
            (
                f"{escape(str(row['channel_type']))} · CPA "
                f"{metric_or_na(None if row['cost_per_conversion'] == 'not_applicable' else decimal(row['cost_per_conversion']))} · "
                f"ROAS {metric_or_na(None if row['value_per_cost'] == 'not_applicable' else decimal(row['value_per_cost']), 'x')}"
            ),
        )
        rendered.append(
            "<tr>" + "".join(f"<td>{value}</td>" for value in values) + "</tr>"
        )
    return "".join(rendered)


def build_replacements(payload: dict[str, Any], client: str) -> dict[str, str]:
    run = payload["run"]
    rows = payload["rows"]
    totals = aggregate(rows)
    currency = str(run["currency"])
    cpa = totals["cpa"]
    roas = totals["roas"]
    quality = payload["quality"]
    notes = quality.get("notes", [])
    summary = (
        f"Export somente leitura aprovado com {len(rows)} campanha(s). "
        "A qualidade declarada está completa e conciliada."
    )
    evidence = (
        f"Foram consolidadas {format_number(totals['impressions'], 0)} impressões e "
        f"{format_number(totals['clicks'], 0)} cliques."
    )
    gaps = "; ".join(escape(str(note)) for note in notes) if notes else "Nenhuma lacuna declarada na coleta."
    return {
        "CLIENTE": escape(client),
        "JANELA_ANALISE": f"{escape(str(run['window_start']))} a {escape(str(run['window_end']))}",
        "DATA_GERACAO": escape(str(run["collected_at"])),
        "ACT_ID": f"••••{escape(str(run['customer_id_masked']))}",
        "SPEND": format_money(totals["cost"], currency),
        "DELTA_SPEND": "Sem comparativo informado",
        "CPA": "N/A" if cpa is None else format_money(cpa, currency),
        "DELTA_CPA": "Sem baseline informado",
        "ROAS": metric_or_na(roas, "x"),
        "DELTA_ROAS": "Sem baseline informado",
        "PURCHASES": format_number(totals["conversions"]),
        "DELTA_PURCHASES": "Conversões atribuídas",
        "RESUMO_EXECUTIVO": escape(summary),
        "FUNNEL_ROWS": campaign_rows(rows, currency),
        "GARGALO": "Não determinado sem baseline ou período anterior",
        "EVIDENCIAS": escape(evidence),
        "ACTION_ROWS": (
            "<tr><td>Próxima leitura</td><td>Comparar com baseline aprovado</td>"
            "<td>Responsável humano</td><td>Mesma janela, moeda e conversão</td></tr>"
        ),
        "LACUNAS_RISCOS": gaps,
        "FONTES_DADOS": escape(str(run["source"])),
    }


def render(template: str, replacements: dict[str, str]) -> str:
    output = template
    for placeholder in PLACEHOLDERS:
        token = "{{" + placeholder + "}}"
        if token not in output:
            raise ValueError(f"template sem placeholder obrigatório: {token}")
        output = output.replace(token, replacements[placeholder])
    if "{{" in output or "}}" in output:
        raise ValueError("template renderizado ainda contém placeholders")
    return output


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("export", type=Path, help="Export JSON normalizado")
    parser.add_argument("output", type=Path, help="Arquivo HTML de saída")
    parser.add_argument("--client", required=True, help="Nome público do cliente no relatório")
    parser.add_argument("--template", type=Path, default=DEFAULT_TEMPLATE)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        payload = json.loads(args.export.read_text(encoding="utf-8"))
        template = args.template.read_text(encoding="utf-8")
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        print(f"erro de entrada: {error}", file=sys.stderr)
        return 2
    errors = load_validator().validate_payload(payload)
    if errors:
        print("relatório bloqueado pelo contrato Google Ads:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    try:
        html = render(template, build_replacements(payload, args.client))
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(html, encoding="utf-8")
    except (KeyError, OSError, ValueError) as error:
        print(f"erro ao gerar relatório: {error}", file=sys.stderr)
        return 2
    print(f"Relatório gerado: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
