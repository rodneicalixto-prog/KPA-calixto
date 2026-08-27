#!/usr/bin/env python3
"""Testes do contrato executável para exports Google Ads."""

from __future__ import annotations

from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from zoneinfo import ZoneInfoNotFoundError


MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "validate_google_ads_export.py"
SPEC = importlib.util.spec_from_file_location("validate_google_ads_export", MODULE_PATH)
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


def valid_payload() -> dict:
    return {
        "schema_version": "1.0",
        "platform": "google_ads",
        "mode": "read_only",
        "run": {
            "run_id": "cliente_weekly_20260826T120000Z",
            "collected_at": "2026-08-26T12:00:00Z",
            "window_start": "2026-08-18",
            "window_end": "2026-08-25",
            "timezone": "America/Sao_Paulo",
            "currency": "BRL",
            "customer_id_masked": "1234",
            "source": "fixture_test",
        },
        "rows": [
            {
                "level": "campaign",
                "entity_id": "campaign-1",
                "entity_name": "Pesquisa principal",
                "campaign_id": "campaign-1",
                "campaign_name": "Pesquisa principal",
                "status": "ENABLED",
                "channel_type": "SEARCH",
                "impressions": 1000,
                "clicks": 100,
                "cost": 250,
                "conversions": 10,
                "conversion_value": 1000,
                "ctr": 0.1,
                "average_cpc": 2.5,
                "cost_per_conversion": 25,
                "value_per_cost": 4,
            }
        ],
        "quality": {
            "complete": True,
            "totals_reconciled": True,
            "conversion_definition_confirmed": True,
            "notes": [],
        },
        "safety": {
            "contains_credentials": False,
            "contains_personal_data": False,
            "platform_writes_allowed": False,
            "human_approval_required": True,
        },
    }


class ValidateGoogleAdsExportTests(unittest.TestCase):
    def test_accepts_consistent_read_only_export(self) -> None:
        self.assertEqual(VALIDATOR.validate_payload(valid_payload()), [])

    def test_accepts_default_timezone_when_windows_has_no_tzdata(self) -> None:
        with patch.object(VALIDATOR, "ZoneInfo", side_effect=ZoneInfoNotFoundError("missing")):
            errors = VALIDATOR.validate_payload(valid_payload())
        self.assertFalse(any("timezone" in error for error in errors), errors)

    def test_rejects_write_mode_and_unsafe_flags(self) -> None:
        payload = valid_payload()
        payload["mode"] = "write"
        payload["safety"]["platform_writes_allowed"] = True
        errors = VALIDATOR.validate_payload(payload)
        self.assertIn("mode: deve ser read_only", errors)
        self.assertIn("safety.platform_writes_allowed: deve ser false", errors)

    def test_rejects_unmasked_customer_id_and_secret_key(self) -> None:
        payload = valid_payload()
        payload["run"]["customer_id_masked"] = "123-456-7890"
        payload["run"]["developer_token"] = "não-deveria-estar-aqui"
        errors = VALIDATOR.validate_payload(payload)
        self.assertTrue(any("customer_id_masked" in error for error in errors))
        self.assertTrue(any("possível segredo" in error for error in errors))

    def test_rejects_inconsistent_metrics(self) -> None:
        payload = valid_payload()
        payload["rows"][0]["clicks"] = 1200
        payload["rows"][0]["ctr"] = 0.1
        errors = VALIDATOR.validate_payload(payload)
        self.assertTrue(any("clicks não pode exceder impressions" in error for error in errors))
        self.assertTrue(any("ctr: divergente" in error for error in errors))

    def test_rejects_unconfirmed_data_quality(self) -> None:
        payload = valid_payload()
        payload["quality"]["totals_reconciled"] = False
        errors = VALIDATOR.validate_payload(payload)
        self.assertIn("quality.totals_reconciled: deve ser true para aprovação", errors)

    def test_requires_not_applicable_for_zero_denominator(self) -> None:
        payload = deepcopy(valid_payload())
        row = payload["rows"][0]
        row["clicks"] = 0
        row["conversions"] = 0
        row["ctr"] = 0
        row["average_cpc"] = "not_applicable"
        row["cost_per_conversion"] = "not_applicable"
        self.assertEqual(VALIDATOR.validate_payload(payload), [])

    def test_cli_exit_codes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            valid_path = Path(directory) / "valid.json"
            invalid_path = Path(directory) / "invalid.json"
            malformed_path = Path(directory) / "malformed.json"
            valid_path.write_text(json.dumps(valid_payload()), encoding="utf-8")
            invalid_payload = valid_payload()
            invalid_payload["mode"] = "write"
            invalid_path.write_text(json.dumps(invalid_payload), encoding="utf-8")
            malformed_path.write_text("{", encoding="utf-8")

            valid_result = subprocess.run(
                [sys.executable, str(MODULE_PATH), str(valid_path)],
                check=False,
                capture_output=True,
                text=True,
            )
            invalid_result = subprocess.run(
                [sys.executable, str(MODULE_PATH), str(invalid_path)],
                check=False,
                capture_output=True,
                text=True,
            )
            malformed_result = subprocess.run(
                [sys.executable, str(MODULE_PATH), str(malformed_path)],
                check=False,
                capture_output=True,
                text=True,
            )

        self.assertEqual(valid_result.returncode, 0)
        self.assertIn("aprovado", valid_result.stdout)
        self.assertEqual(invalid_result.returncode, 1)
        self.assertIn("bloqueado", invalid_result.stderr)
        self.assertEqual(malformed_result.returncode, 2)
        self.assertIn("não foi possível ler JSON", malformed_result.stderr)


if __name__ == "__main__":
    unittest.main()
