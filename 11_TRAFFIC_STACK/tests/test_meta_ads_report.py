#!/usr/bin/env python3
"""Testes end-to-end do relatório Meta Ads."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


STACK = Path(__file__).resolve().parents[1]
TOOL = STACK / "tools" / "render_meta_ads_report.py"
FIXTURE = Path(__file__).parent / "fixtures" / "meta-ads-terra-fibra-valid.json"


class MetaAdsReportTests(unittest.TestCase):
    def test_generates_escaped_report(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "report.html"
            result = subprocess.run([sys.executable, str(TOOL), str(FIXTURE), str(output), "--client", "Terra <Fibra>"], capture_output=True, text=True)
            html = output.read_text(encoding="utf-8")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Terra &lt;Fibra&gt;", html)
        self.assertNotIn("{{", html)
        self.assertIn("R$ 25,92", html)

    def test_invalid_export_does_not_write(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
            payload["safety"]["platform_writes_allowed"] = True
            source = Path(directory) / "unsafe.json"
            output = Path(directory) / "report.html"
            source.write_text(json.dumps(payload), encoding="utf-8")
            result = subprocess.run([sys.executable, str(TOOL), str(source), str(output), "--client", "Terra Fibra"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
