#!/usr/bin/env python3
"""Valida export normalizado e somente leitura do Meta Ads."""

from __future__ import annotations

import argparse
from datetime import date
import json
from pathlib import Path
import re
import sys
from typing import Any
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


MASKED_ID = re.compile(r"^\*{3}\d{4}$")
STATUSES = {"active", "paused", "archived", "unknown"}
PORTABLE_IANA_TIMEZONES = frozenset({"America/Sao_Paulo", "Etc/UTC", "UTC"})


def is_supported_timezone(value: str) -> bool:
    """Valida IANA usando o SO e preserva os timezones do kit sem tzdata."""
    try:
        ZoneInfo(value)
        return True
    except (ZoneInfoNotFoundError, ValueError):
        return value in PORTABLE_IANA_TIMEZONES


def validate_payload(value: Any) -> list[str]:
    if not isinstance(value, dict):
        return ["root: objeto JSON obrigatório"]
    errors: list[str] = []
    expected = {"schema_version": "1.0", "platform": "meta_ads", "mode": "read_only"}
    for field, required in expected.items():
        if value.get(field) != required:
            errors.append(f"{field}: deve ser {required!r}")
    if not MASKED_ID.fullmatch(str(value.get("account_id_masked", ""))):
        errors.append("account_id_masked: use somente *** e os 4 últimos dígitos")
    window = value.get("window")
    if not isinstance(window, dict):
        errors.append("window: objeto obrigatório")
    else:
        try:
            start = date.fromisoformat(window["start"])
            end = date.fromisoformat(window["end"])
            if end < start:
                errors.append("window: end não pode anteceder start")
        except (KeyError, TypeError, ValueError):
            errors.append("window: start e end devem usar AAAA-MM-DD")
        timezone = window.get("timezone")
        if not isinstance(timezone, str) or not timezone.strip():
            errors.append("window.timezone: obrigatório")
        else:
            if not is_supported_timezone(timezone):
                errors.append("window.timezone: identificador IANA inválido ou não suportado")
    attribution = value.get("attribution")
    if not isinstance(attribution, dict) or not isinstance(attribution.get("definition_confirmed"), bool):
        errors.append("attribution.definition_confirmed: booleano obrigatório")
    safety = value.get("safety")
    required_safety = {
        "contains_credentials": False,
        "contains_personal_data": False,
        "platform_writes_allowed": False,
        "human_approval_required": True,
    }
    if not isinstance(safety, dict):
        errors.append("safety: objeto obrigatório")
    else:
        for field, required in required_safety.items():
            if safety.get(field) is not required:
                errors.append(f"safety.{field}: deve ser {str(required).lower()}")
    campaigns = value.get("campaigns")
    if not isinstance(campaigns, list) or not campaigns:
        errors.append("campaigns: lista não vazia obrigatória")
        return errors
    for index, campaign in enumerate(campaigns):
        prefix = f"campaigns[{index}]"
        if not isinstance(campaign, dict):
            errors.append(f"{prefix}: objeto obrigatório")
            continue
        if not isinstance(campaign.get("campaign_name"), str) or not campaign["campaign_name"].strip():
            errors.append(f"{prefix}.campaign_name: obrigatório")
        if not MASKED_ID.fullmatch(str(campaign.get("campaign_id_masked", ""))):
            errors.append(f"{prefix}.campaign_id_masked: ID mascarado obrigatório")
        if campaign.get("status") not in STATUSES:
            errors.append(f"{prefix}.status: valor inválido")
        for field in ("spend_brl", "impressions", "reach", "link_clicks", "results"):
            metric = campaign.get(field)
            if isinstance(metric, bool) or not isinstance(metric, (int, float)) or metric < 0:
                errors.append(f"{prefix}.{field}: número não negativo obrigatório")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("export", type=Path)
    args = parser.parse_args()
    try:
        payload = json.loads(args.export.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        print(f"erro de leitura: {error}", file=sys.stderr)
        return 2
    errors = validate_payload(payload)
    if errors:
        print("export bloqueado:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("Export Meta Ads aprovado em modo somente leitura.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
