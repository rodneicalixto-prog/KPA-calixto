#!/usr/bin/env python3
"""Testes do preflight de runtime Codex para Ads."""

from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


STACK = Path(__file__).resolve().parents[1]
TOOL = STACK / "tools" / "preflight_codex_ads_runtime.py"
TEMPLATE = STACK / "templates" / "codex-ads-runtime.json"


class CodexAdsRuntimePreflightTests(unittest.TestCase):
    def prepare(self, root: Path, *, unsafe: bool = False) -> Path:
        for name in ("05_WORKSPACE", "06_OUTPUTS", "07_LOGS"):
            (root / name).mkdir()
        config = json.loads(TEMPLATE.read_text(encoding="utf-8"))
        config["safety"]["allow_platform_writes"] = unsafe
        path = root / "runtime.json"
        path.write_text(json.dumps(config), encoding="utf-8")
        return path

    def run_tool(
        self,
        config: Path,
        root: Path,
        *flags: str,
        environment: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(TOOL), str(config), "--repo-root", str(root), *flags],
            capture_output=True, text=True, check=False, env=environment,
        )

    def test_dry_run_performs_no_platform_access_or_write(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config = self.prepare(root)
            result = self.run_tool(config, root)
            exists = (root / "codex-ads-runtime-preflight.json").exists()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("sem acesso a plataformas", result.stdout)
        self.assertFalse(exists)

    def test_apply_writes_safe_report(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config = self.prepare(root)
            result = self.run_tool(config, root, "--apply")
            report = json.loads((root / "codex-ads-runtime-preflight.json").read_text())
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(report["platform_access_performed"])
        self.assertFalse(report["platform_writes_enabled"])
        self.assertEqual(report["status"], "ready_with_external_refs_pending")

    def test_configured_external_reference_marks_runtime_ready(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config = self.prepare(root)
            environment = os.environ.copy()
            environment["KPA_OBSIDIAN_VAULT"] = str(root / "vault")
            result = self.run_tool(
                config,
                root,
                "--apply",
                environment=environment,
            )
            report = json.loads((root / "codex-ads-runtime-preflight.json").read_text())
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(report["environment_refs"]["KPA_OBSIDIAN_VAULT"], "configured")
        self.assertEqual(report["status"], "ready")

    def test_unsafe_config_is_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config = self.prepare(root, unsafe=True)
            result = self.run_tool(config, root, "--apply")
        self.assertEqual(result.returncode, 1)
        self.assertIn("allow_platform_writes", result.stderr)


if __name__ == "__main__":
    unittest.main()
