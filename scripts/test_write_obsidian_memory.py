#!/usr/bin/env python3
"""Testes da escrita explícita e segura no Obsidian."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


TOOL = Path(__file__).with_name("write_obsidian_memory.py")
POWERSHELL_WRAPPER = Path(__file__).with_name("write-obsidian-memory.ps1")


def payload() -> dict:
    return {
        "project": "KPA V30", "task_id": "kit-complete", "title": "Kit concluído",
        "summary": "Core concluído", "result": "Validação aprovada", "worked": "Gates",
        "failed": "Integrações externas pendentes", "decision": "Tráfego depois",
        "next_action": "Codex x Ads", "links": ["KIT_STATUS"],
        "gate_status": "approved_with_concerns", "contains_credentials": False,
    }


class WriteObsidianMemoryTests(unittest.TestCase):
    def test_powershell_wrapper_resolves_repo_from_script_location(self) -> None:
        content = POWERSHELL_WRAPPER.read_text(encoding="utf-8")
        self.assertIn("$PSScriptRoot", content)
        self.assertIn("Test-Path", content)
        self.assertIn('"--apply"', content)

    def test_dry_run_does_not_require_vault(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            record = Path(directory) / "record.json"
            record.write_text(json.dumps(payload()), encoding="utf-8")
            result = subprocess.run([sys.executable, str(TOOL), str(record)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Dry-run", result.stdout)

    def test_apply_writes_execution_note(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            vault = root / "vault"
            vault.mkdir()
            record = root / "record.json"
            record.write_text(json.dumps(payload()), encoding="utf-8")
            result = subprocess.run([sys.executable, str(TOOL), str(record), "--vault", str(vault), "--apply"], capture_output=True, text=True)
            notes = list((vault / "07_Executions" / "KPA-V30").glob("*.md"))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(notes), 1)

    def test_repeated_apply_is_idempotent_for_same_task_and_day(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            vault = root / "vault"
            vault.mkdir()
            record = root / "record.json"
            record.write_text(json.dumps(payload()), encoding="utf-8")
            command = [sys.executable, str(TOOL), str(record), "--vault", str(vault), "--apply"]
            first = subprocess.run(command, capture_output=True, text=True)
            second = subprocess.run(command, capture_output=True, text=True)
            notes = list((vault / "07_Executions" / "KPA-V30").glob("*.md"))
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertEqual(len(notes), 1)

    def test_credentials_flag_blocks_write(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            value = payload(); value["contains_credentials"] = True
            record = root / "record.json"
            record.write_text(json.dumps(value), encoding="utf-8")
            result = subprocess.run([sys.executable, str(TOOL), str(record), "--vault", str(root), "--apply"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn("contains_credentials", result.stderr)


if __name__ == "__main__":
    unittest.main()
