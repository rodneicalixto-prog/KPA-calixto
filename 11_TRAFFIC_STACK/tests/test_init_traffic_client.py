#!/usr/bin/env python3
"""Testes do inicializador de clientes da Traffic Stack."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


STACK = Path(__file__).resolve().parents[1]
INITIALIZER = STACK / "tools" / "init_traffic_client.py"


class InitTrafficClientTests(unittest.TestCase):
    def command(self, root: Path, *extra: str) -> list[str]:
        return [
            sys.executable,
            str(INITIALIZER),
            "--slug",
            "cliente-demo",
            "--name",
            "Cliente Demo",
            "--output-root",
            str(root),
            *extra,
        ]

    def test_creates_complete_safe_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            result = subprocess.run(
                self.command(root, "--account-suffix", "1234"),
                check=False,
                capture_output=True,
                text=True,
            )
            client = root / "cliente-demo"
            files = {path.name for path in client.iterdir()}
            schedule = json.loads((client / "traffic-schedule.json").read_text(encoding="utf-8"))
            state = json.loads((client / "traffic-state.json").read_text(encoding="utf-8"))
            mapping = (client / "act-mapping.yaml").read_text(encoding="utf-8")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(
            {
                "CLAUDE.md",
                "act-mapping.yaml",
                "baseline-kpis.md",
                "funil.md",
                "icp.md",
                "traffic-schedule.json",
                "traffic-state.json",
            }.issubset(files)
        )
        self.assertEqual(schedule["client"], "Cliente Demo")
        self.assertFalse(schedule["jobs"][0]["enabled"])
        self.assertFalse(schedule["safety"]["allow_platform_writes"])
        self.assertEqual(state["preflight_status"], "pending")
        self.assertFalse(state["contains_credentials"])
        self.assertIn('act_id: "masked-1234"', mapping)

    def test_rejects_path_traversal_slug(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run(
                [
                    sys.executable,
                    str(INITIALIZER),
                    "--slug",
                    "../fora",
                    "--name",
                    "Cliente Demo",
                    "--output-root",
                    directory,
                ],
                check=False,
                capture_output=True,
                text=True,
            )
        self.assertEqual(result.returncode, 1)
        self.assertIn("slug", result.stderr)

    def test_refuses_to_overwrite_existing_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            first = subprocess.run(self.command(root), check=False, capture_output=True, text=True)
            marker = root / "cliente-demo" / "marker.txt"
            marker.write_text("preservar", encoding="utf-8")
            second = subprocess.run(self.command(root), check=False, capture_output=True, text=True)
            marker_value = marker.read_text(encoding="utf-8")
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(second.returncode, 1)
        self.assertIn("destino já existe", second.stderr)
        self.assertEqual(marker_value, "preservar")

    def test_rejects_full_account_id(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run(
                self.command(Path(directory), "--account-suffix", "1234567890"),
                check=False,
                capture_output=True,
                text=True,
            )
        self.assertEqual(result.returncode, 1)
        self.assertIn("quatro últimos dígitos", result.stderr)


if __name__ == "__main__":
    unittest.main()

