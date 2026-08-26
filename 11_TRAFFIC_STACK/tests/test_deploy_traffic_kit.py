#!/usr/bin/env python3
"""Testes da implantação local e segura do Traffic Kit."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


STACK = Path(__file__).resolve().parents[1]
TOOL = STACK / "tools" / "deploy_traffic_kit.py"


def workspace(root: Path, *, unsafe: bool = False) -> Path:
    target = root / "cliente"
    target.mkdir()
    for name in ("CLAUDE.md", "act-mapping.yaml", "baseline-kpis.md", "funil.md", "icp.md"):
        (target / name).write_text("ok\n", encoding="utf-8")
    (target / "traffic-state.json").write_text(
        json.dumps({"client_name": "Cliente", "contains_credentials": False}), encoding="utf-8"
    )
    (target / "traffic-schedule.json").write_text(json.dumps({
        "jobs": [],
        "safety": {
            "read_only": True,
            "allow_platform_writes": unsafe,
            "require_human_approval": True,
        },
    }), encoding="utf-8")
    return target


class DeployTrafficKitTests(unittest.TestCase):
    def run_tool(self, target: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(TOOL), str(target), *args],
            check=False, capture_output=True, text=True,
        )

    def test_dry_run_does_not_write(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = workspace(Path(directory))
            result = self.run_tool(target)
            exists = (target / "traffic-kit-deployment.json").exists()
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertFalse(exists)

    def test_apply_writes_safe_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = workspace(Path(directory))
            result = self.run_tool(target, "--apply")
            manifest = json.loads((target / "traffic-kit-deployment.json").read_text())
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(manifest["components"]["platform_writes"], "blocked")
        self.assertIn("pending", manifest["components"]["meta_collector"])

    def test_unsafe_schedule_is_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = workspace(Path(directory), unsafe=True)
            result = self.run_tool(target, "--apply")
            exists = (target / "traffic-kit-deployment.json").exists()
        self.assertEqual(result.returncode, 1)
        self.assertIn("allow_platform_writes", result.stdout)
        self.assertFalse(exists)

    def test_non_list_jobs_is_blocked_without_traceback(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = workspace(Path(directory))
            schedule_path = target / "traffic-schedule.json"
            schedule = json.loads(schedule_path.read_text(encoding="utf-8"))
            schedule["jobs"] = "disabled"
            schedule_path.write_text(json.dumps(schedule), encoding="utf-8")
            result = self.run_tool(target, "--apply")
        self.assertEqual(result.returncode, 1)
        self.assertIn("jobs deve ser uma lista", result.stdout)
        self.assertNotIn("Traceback", result.stderr)

    def test_non_object_job_is_blocked_without_traceback(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = workspace(Path(directory))
            schedule_path = target / "traffic-schedule.json"
            schedule = json.loads(schedule_path.read_text(encoding="utf-8"))
            schedule["jobs"] = ["weekly_review"]
            schedule_path.write_text(json.dumps(schedule), encoding="utf-8")
            result = self.run_tool(target, "--apply")
        self.assertEqual(result.returncode, 1)
        self.assertIn("jobs[0] deve ser um objeto", result.stdout)
        self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
