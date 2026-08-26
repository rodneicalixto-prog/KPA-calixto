#!/usr/bin/env python3
"""Testes do gate Meta Ads somente leitura."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


STACK = Path(__file__).resolve().parents[1]
TOOL = STACK / "tools" / "validate_meta_ads_export.py"
FIXTURE = Path(__file__).parent / "fixtures" / "meta-ads-terra-fibra-valid.json"
spec = importlib.util.spec_from_file_location("meta_validator", TOOL)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class MetaAdsExportTests(unittest.TestCase):
    def test_valid_fixture(self) -> None:
        payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
        self.assertEqual(module.validate_payload(payload), [])

    def test_blocks_full_ids_and_writes(self) -> None:
        payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
        payload["account_id_masked"] = "615957335160862"
        payload["safety"]["platform_writes_allowed"] = True
        errors = module.validate_payload(payload)
        self.assertTrue(any("account_id_masked" in error for error in errors))
        self.assertTrue(any("platform_writes_allowed" in error for error in errors))

    def test_cli_exit_codes(self) -> None:
        valid = subprocess.run([sys.executable, str(TOOL), str(FIXTURE)], capture_output=True, text=True)
        with tempfile.TemporaryDirectory() as directory:
            malformed = Path(directory) / "bad.json"
            malformed.write_text("{", encoding="utf-8")
            bad = subprocess.run([sys.executable, str(TOOL), str(malformed)], capture_output=True, text=True)
        self.assertEqual(valid.returncode, 0, valid.stderr)
        self.assertEqual(bad.returncode, 2)


if __name__ == "__main__":
    unittest.main()
