#!/usr/bin/env python3
"""Testes do executor local e seguro de jobs de tráfego."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


STACK = Path(__file__).resolve().parents[1]
RUNNER = STACK / "tools" / "run_scheduled_traffic.py"
FIXTURE = Path(__file__).parent / "fixtures" / "google-ads-valid.json"


def config(output: Path, state_file: Path, *, enabled: bool = False) -> dict:
    return {
        "version": "1.0",
        "status": "draft",
        "client": "Cliente Piloto Anonimizado",
        "state_file": str(state_file),
        "jobs": [
            {
                "id": "weekly_review",
                "enabled": enabled,
                "mode": "weekly_review",
                "input_export": str(FIXTURE),
                "output_html": str(output),
            }
        ],
        "safety": {
            "read_only": True,
            "allow_platform_writes": False,
            "require_human_approval": True,
        },
    }


class ScheduledTrafficTests(unittest.TestCase):
    def run_job(self, payload: dict, directory: str, *flags: str) -> subprocess.CompletedProcess[str]:
        config_path = Path(directory) / "schedule.json"
        config_path.write_text(json.dumps(payload), encoding="utf-8")
        return subprocess.run(
            [sys.executable, str(RUNNER), str(config_path), "--job", "weekly_review", *flags],
            check=False,
            capture_output=True,
            text=True,
        )

    def test_dry_run_does_not_write_output(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "report.html"
            state = Path(directory) / "state.json"
            result = self.run_job(config(output, state), directory)
            exists = output.exists()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Dry-run aprovado", result.stdout)
        self.assertFalse(exists)

    def test_execute_requires_enabled_job(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "report.html"
            state = Path(directory) / "state.json"
            result = self.run_job(config(output, state), directory, "--execute")
            exists = output.exists()
        self.assertEqual(result.returncode, 1)
        self.assertIn("enabled deve ser true", result.stderr)
        self.assertFalse(exists)

    def test_execute_generates_report_for_enabled_job(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "report.html"
            state = Path(directory) / "state.json"
            state.write_text(json.dumps({"preflight_status": "approved", "collector_status": "validated_read_only", "contains_credentials": False}), encoding="utf-8")
            result = self.run_job(config(output, state, enabled=True), directory, "--execute")
            html = output.read_text(encoding="utf-8")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Cliente Piloto Anonimizado", html)
        self.assertNotIn("{{", html)

    def test_unsafe_config_is_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "report.html"
            state = Path(directory) / "state.json"
            payload = config(output, state, enabled=True)
            payload["safety"]["allow_platform_writes"] = True
            result = self.run_job(payload, directory, "--execute")
            exists = output.exists()
        self.assertEqual(result.returncode, 1)
        self.assertIn("allow_platform_writes", result.stderr)
        self.assertFalse(exists)

    def test_execute_requires_approved_preflight_state(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "report.html"
            state = Path(directory) / "state.json"
            state.write_text(json.dumps({"preflight_status": "pending", "collector_status": "not_configured", "contains_credentials": False}), encoding="utf-8")
            result = self.run_job(config(output, state, enabled=True), directory, "--execute")
        self.assertEqual(result.returncode, 1)
        self.assertIn("preflight_status", result.stderr)


if __name__ == "__main__":
    unittest.main()
