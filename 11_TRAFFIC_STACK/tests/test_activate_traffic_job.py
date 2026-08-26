#!/usr/bin/env python3
"""Testes da ativação explícita de jobs de tráfego."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


STACK = Path(__file__).resolve().parents[1]
INITIALIZER = STACK / "tools" / "init_traffic_client.py"
PREFLIGHT = STACK / "tools" / "preflight_traffic_client.py"
ACTIVATE = STACK / "tools" / "activate_traffic_job.py"
EXPORT = Path(__file__).parent / "fixtures" / "google-ads-valid.json"


class ActivateTrafficJobTests(unittest.TestCase):
    def workspace(self, root: Path, *, preflight: bool) -> Path:
        subprocess.run(
            [sys.executable, str(INITIALIZER), "--slug", "demo", "--name", "Demo", "--output-root", str(root)],
            check=True,
            capture_output=True,
            text=True,
        )
        workspace = root / "demo"
        if preflight:
            subprocess.run(
                [sys.executable, str(PREFLIGHT), str(workspace), "--export", str(EXPORT), "--collector-source", "fixture", "--conversion-action", "purchase", "--owner", "Operador", "--apply"],
                check=True,
                capture_output=True,
                text=True,
            )
        return workspace

    def activate(self, workspace: Path, confirmation: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(ACTIVATE), str(workspace), "--job", "weekly_review", "--confirm", confirmation],
            check=False,
            capture_output=True,
            text=True,
        )

    def test_requires_exact_confirmation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = self.workspace(Path(directory), preflight=True)
            result = self.activate(workspace, "sim")
            schedule = json.loads((workspace / "traffic-schedule.json").read_text())
        self.assertEqual(result.returncode, 1)
        self.assertFalse(schedule["jobs"][0]["enabled"])

    def test_requires_approved_preflight(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = self.workspace(Path(directory), preflight=False)
            result = self.activate(workspace, "ATIVAR SOMENTE LEITURA")
        self.assertEqual(result.returncode, 1)
        self.assertIn("preflight_status", result.stderr)

    def test_activates_only_selected_read_only_job(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = self.workspace(Path(directory), preflight=True)
            result = self.activate(workspace, "ATIVAR SOMENTE LEITURA")
            schedule = json.loads((workspace / "traffic-schedule.json").read_text())
            state = json.loads((workspace / "traffic-state.json").read_text())
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(schedule["jobs"][0]["enabled"])
        self.assertFalse(schedule["safety"]["allow_platform_writes"])
        self.assertEqual(state["schedule_status"], "enabled:weekly_review")


if __name__ == "__main__":
    unittest.main()

