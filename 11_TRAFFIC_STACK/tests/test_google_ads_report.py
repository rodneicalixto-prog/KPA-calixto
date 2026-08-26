#!/usr/bin/env python3
"""Testes end-to-end da geração de relatório Google Ads."""

from __future__ import annotations

from html.parser import HTMLParser
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


STACK = Path(__file__).resolve().parents[1]
RENDERER = STACK / "tools" / "render_google_ads_report.py"
FIXTURE = Path(__file__).parent / "fixtures" / "google-ads-valid.json"


class GeneratedDocumentParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.has_main = False
        self.title_text = ""
        self._inside_title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "main":
            self.has_main = True
        elif tag == "title":
            self._inside_title = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._inside_title = False

    def handle_data(self, data: str) -> None:
        if self._inside_title:
            self.title_text += data


class GoogleAdsReportTests(unittest.TestCase):
    def test_cli_generates_complete_escaped_report(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "report.html"
            result = subprocess.run(
                [
                    sys.executable,
                    str(RENDERER),
                    str(FIXTURE),
                    str(output),
                    "--client",
                    "Cliente <Demo>",
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            html = output.read_text(encoding="utf-8")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("{{", html)
        self.assertIn("Cliente &lt;Demo&gt;", html)
        self.assertNotIn("Cliente <Demo>", html)
        self.assertIn("R$ 350,00", html)
        self.assertIn("17,50", html)
        self.assertIn("4,29x", html)
        parser = GeneratedDocumentParser()
        parser.feed(html)
        parser.close()
        self.assertTrue(parser.has_main)
        self.assertIn("Cliente <Demo>", parser.title_text)

    def test_cli_blocks_invalid_export_without_creating_output(self) -> None:
        payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
        payload["mode"] = "write"
        with tempfile.TemporaryDirectory() as directory:
            invalid = Path(directory) / "invalid.json"
            output = Path(directory) / "report.html"
            invalid.write_text(json.dumps(payload), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(RENDERER), str(invalid), str(output), "--client", "Demo"],
                check=False,
                capture_output=True,
                text=True,
            )
            output_exists = output.exists()

        self.assertEqual(result.returncode, 1)
        self.assertIn("bloqueado", result.stderr)
        self.assertFalse(output_exists)


if __name__ == "__main__":
    unittest.main()

