#!/usr/bin/env python3
"""Testes do preflight de workspaces de tráfego."""

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
EXPORT = Path(__file__).parent / "fixtures" / "google-ads-valid.json"
META_EXPORT = Path(__file__).parent / "fixtures" / "meta-ads-terra-fibra-valid.json"


class PreflightTrafficClientTests(unittest.TestCase):
    def create_workspace(self, root: Path) -> Path:
        result = subprocess.run(
            [
                sys.executable,
                str(INITIALIZER),
                "--slug",
                "cliente-demo",
                "--name",
                "Cliente Demo",
                "--account-suffix",
                "1234",
                "--output-root",
                str(root),
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return root / "cliente-demo"

    def command(self, workspace: Path, *flags: str) -> list[str]:
        return [
            sys.executable,
            str(PREFLIGHT),
            str(workspace),
            "--export",
            str(EXPORT),
            "--collector-source",
            "exportacao-validada",
            "--conversion-action",
            "purchase",
            "--owner",
            "Operador",
            *flags,
        ]

    def test_dry_run_does_not_change_state(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = self.create_workspace(Path(directory))
            before = (workspace / "traffic-state.json").read_bytes()
            result = subprocess.run(self.command(workspace), check=False, capture_output=True, text=True)
            after = (workspace / "traffic-state.json").read_bytes()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Dry-run", result.stdout)
        self.assertEqual(before, after)

    def test_apply_marks_preflight_ready_but_keeps_jobs_disabled(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = self.create_workspace(Path(directory))
            result = subprocess.run(
                self.command(workspace, "--apply"), check=False, capture_output=True, text=True
            )
            state = json.loads((workspace / "traffic-state.json").read_text(encoding="utf-8"))
            schedule = json.loads((workspace / "traffic-schedule.json").read_text(encoding="utf-8"))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(state["preflight_status"], "approved")
        self.assertEqual(state["collector_status"], "validated_read_only")
        self.assertEqual(state["owner"], "Operador")
        self.assertTrue(all(job["enabled"] is False for job in schedule["jobs"]))
        self.assertEqual(schedule["jobs"][0]["input_export"], str(EXPORT.resolve()))

    def test_blocks_unsafe_schedule_without_writing_state(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = self.create_workspace(Path(directory))
            schedule_path = workspace / "traffic-schedule.json"
            schedule = json.loads(schedule_path.read_text(encoding="utf-8"))
            schedule["safety"]["allow_platform_writes"] = True
            schedule_path.write_text(json.dumps(schedule), encoding="utf-8")
            before = (workspace / "traffic-state.json").read_bytes()
            result = subprocess.run(
                self.command(workspace, "--apply"), check=False, capture_output=True, text=True
            )
            after = (workspace / "traffic-state.json").read_bytes()
        self.assertEqual(result.returncode, 1)
        self.assertIn("escrita em plataforma", result.stderr)
        self.assertEqual(before, after)

    def test_accepts_meta_ads_read_only_export(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = self.create_workspace(Path(directory))
            command = self.command(workspace)
            command[command.index(str(EXPORT))] = str(META_EXPORT)
            result = subprocess.run(command, check=False, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Preflight aprovado", result.stdout)


if __name__ == "__main__":
    unittest.main()
