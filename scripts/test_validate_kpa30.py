#!/usr/bin/env python3
"""Testes do validador da distribuição KPA V30."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


TOOL = Path(__file__).with_name("validate_kpa30.py")
spec = importlib.util.spec_from_file_location("validate_kpa30", TOOL)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ValidateKpa30Tests(unittest.TestCase):
    def populate(self, root: Path) -> None:
        for relative in module.REQUIRED:
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("ok\n", encoding="utf-8")
        (root / "KIT_STATUS.json").write_text(json.dumps({
            "release_status": "core_complete_external_integrations_optional",
            "global_safety": {
                "credentials_in_repository": False,
                "external_writes_enabled_by_default": False,
                "human_approval_for_irreversible_actions": True,
            },
        }), encoding="utf-8")

    def test_complete_distribution_passes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.populate(root)
            errors = module.validate(root)
        self.assertEqual(errors, [])

    def test_env_and_missing_file_are_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.populate(root)
            (root / "README.md").unlink()
            (root / ".env").write_text("SECRET=x", encoding="utf-8")
            errors = module.validate(root)
        self.assertTrue(any("README.md" in error for error in errors))
        self.assertTrue(any(".env real" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
