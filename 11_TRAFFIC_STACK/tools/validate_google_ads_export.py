#!/usr/bin/env python3
"""Valida exports normalizados do Google Ads sem acessar a plataforma."""

from __future__ import annotations

import argparse
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
import json
from pathlib import Path
import re
import sys
from typing import Any
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


NON_NEGATIVE_FIELDS = (
    "impressions",
    "clicks",
    "cost",
    "conversions",
    "conversion_value",
)
DERIVED_FIELDS = (
    "ctr",
    "average_cpc",
    "cost_per_conversion",
    "value_per_cost",
)
SECRET_KEY_PATTERN = re.compile(
    r"(?:access[_-]?token|refresh[_-]?token|client[_-]?secret|developer[_-]?token|api[_-]?key)",
    re.IGNORECASE,
)
MASKED_CUSTOMER_ID_PATTERN = re.compile(r"^(?:\*{2,}|x{2,}|X{2,})?\d{4}$")
MONEY_QUANTUM = Decimal("0.000001")


def decimal_value(value: Any, path: str, errors: list[str]) -> Decimal | None:
    if isinstance(value, bool):
        errors.append(f"{path}: booleano não é número")
        return None
    try:
        number = Decimal(str(value))
    except (InvalidOperation, ValueError):
        errors.append(f"{path}: número inválido")
        return None
    if not number.is_finite():
        errors.append(f"{path}: número deve ser finito")
        return None
    return number


def find_secret_keys(value: Any, path: str = "root") -> list[str]:
    findings: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}"
            if SECRET_KEY_PATTERN.search(str(key)):
                findings.append(child_path)
            findings.extend(find_secret_keys(child, child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            findings.extend(find_secret_keys(child, f"{path}[{index}]"))
    return findings


def validate_run(run: Any, errors: list[str]) -> None:
    if not isinstance(run, dict):
        errors.append("run: objeto obrigatório")
        return
    required = ("run_id", "collected_at", "window_start", "window_end", "timezone", "currency", "customer_id_masked", "source")
    for field in required:
        if not run.get(field):
            errors.append(f"run.{field}: obrigatório")

    try:
        start = date.fromisoformat(str(run.get("window_start", "")))
        end = date.fromisoformat(str(run.get("window_end", "")))
        if start > end:
            errors.append("run: window_start deve ser anterior ou igual a window_end")
    except ValueError:
        errors.append("run: janela deve usar datas ISO AAAA-MM-DD")

    try:
        collected_at = datetime.fromisoformat(str(run.get("collected_at", "")).replace("Z", "+00:00"))
        if collected_at.tzinfo is None:
            errors.append("run.collected_at: timezone obrigatório")
    except ValueError:
        errors.append("run.collected_at: timestamp ISO 8601 inválido")

    try:
        ZoneInfo(str(run.get("timezone", "")))
    except (ZoneInfoNotFoundError, ValueError):
        errors.append("run.timezone: timezone IANA inválido")

    currency = str(run.get("currency", ""))
    if not re.fullmatch(r"[A-Z]{3}", currency):
        errors.append("run.currency: usar código ISO 4217 com três letras maiúsculas")

    customer_id = str(run.get("customer_id_masked", ""))
    if not MASKED_CUSTOMER_ID_PATTERN.fullmatch(customer_id):
        errors.append("run.customer_id_masked: informar somente os quatro últimos dígitos")


def expected_derived(row: dict[str, Any], field: str, errors: list[str], index: int) -> Decimal | None:
    values: dict[str, Decimal] = {}
    for base_field in NON_NEGATIVE_FIELDS:
        parsed = decimal_value(row.get(base_field), f"rows[{index}].{base_field}", errors)
        if parsed is None:
            return None
        values[base_field] = parsed
    if field == "ctr":
        return values["clicks"] / values["impressions"] if values["impressions"] else None
    if field == "average_cpc":
        return values["cost"] / values["clicks"] if values["clicks"] else None
    if field == "cost_per_conversion":
        return values["cost"] / values["conversions"] if values["conversions"] else None
    return values["conversion_value"] / values["cost"] if values["cost"] else None


def validate_rows(rows: Any, errors: list[str]) -> None:
    if not isinstance(rows, list) or not rows:
        errors.append("rows: lista não vazia obrigatória")
        return
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            errors.append(f"rows[{index}]: objeto obrigatório")
            continue
        for field in ("level", "entity_id", "entity_name", "campaign_id", "campaign_name", "status", "channel_type"):
            if not row.get(field):
                errors.append(f"rows[{index}].{field}: obrigatório")
        parsed: dict[str, Decimal] = {}
        for field in NON_NEGATIVE_FIELDS:
            value = decimal_value(row.get(field), f"rows[{index}].{field}", errors)
            if value is not None:
                parsed[field] = value
                if value < 0:
                    errors.append(f"rows[{index}].{field}: não pode ser negativo")
        if parsed.get("clicks", Decimal(0)) > parsed.get("impressions", Decimal(0)):
            errors.append(f"rows[{index}]: clicks não pode exceder impressions")

        for field in DERIVED_FIELDS:
            actual = row.get(field)
            expected = expected_derived(row, field, errors, index)
            path = f"rows[{index}].{field}"
            if expected is None:
                if actual != "not_applicable":
                    errors.append(f"{path}: usar not_applicable quando o denominador for zero")
                continue
            parsed_actual = decimal_value(actual, path, errors)
            if parsed_actual is not None and abs(parsed_actual - expected) > MONEY_QUANTUM:
                errors.append(f"{path}: divergente dos campos-base")


def validate_quality_and_safety(payload: dict[str, Any], errors: list[str]) -> None:
    quality = payload.get("quality")
    if not isinstance(quality, dict):
        errors.append("quality: objeto obrigatório")
    else:
        for field in ("complete", "totals_reconciled", "conversion_definition_confirmed"):
            if not isinstance(quality.get(field), bool):
                errors.append(f"quality.{field}: booleano obrigatório")
            elif quality[field] is not True:
                errors.append(f"quality.{field}: deve ser true para aprovação")
        if not isinstance(quality.get("notes"), list):
            errors.append("quality.notes: lista obrigatória")

    safety = payload.get("safety")
    expected_safety = {
        "contains_credentials": False,
        "contains_personal_data": False,
        "platform_writes_allowed": False,
        "human_approval_required": True,
    }
    if not isinstance(safety, dict):
        errors.append("safety: objeto obrigatório")
    else:
        for field, expected in expected_safety.items():
            if safety.get(field) is not expected:
                errors.append(f"safety.{field}: deve ser {str(expected).lower()}")


def validate_payload(payload: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(payload, dict):
        return ["root: objeto JSON obrigatório"]
    if payload.get("schema_version") != "1.0":
        errors.append("schema_version: versão suportada é 1.0")
    if payload.get("platform") != "google_ads":
        errors.append("platform: deve ser google_ads")
    if payload.get("mode") != "read_only":
        errors.append("mode: deve ser read_only")
    for path in find_secret_keys(payload):
        errors.append(f"{path}: chave com possível segredo não permitida")
    validate_run(payload.get("run"), errors)
    validate_rows(payload.get("rows"), errors)
    validate_quality_and_safety(payload, errors)
    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("export", type=Path, help="Arquivo JSON normalizado a validar")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        payload = json.loads(args.export.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"arquivo não encontrado: {args.export}", file=sys.stderr)
        return 2
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        print(f"não foi possível ler JSON: {error}", file=sys.stderr)
        return 2
    errors = validate_payload(payload)
    if errors:
        print("Export Google Ads bloqueado:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"Export Google Ads aprovado: {len(payload['rows'])} linha(s) validada(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
