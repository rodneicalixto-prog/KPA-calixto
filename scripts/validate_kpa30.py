#!/usr/bin/env python3
"""Valida a distribuição completa e pública do KPA V30 sem dependências externas."""

from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
REQUIRED = (
    "README.md", "00_INDEX.md", "INICIO_RAPIDO.md", "CLAUDE.md",
    "00_OS/cos.md", "01_PIPELINE/kpa-v30-pipeline.yaml", "02_AGENTS/README.md",
    "03_TASKS/README.md", "04_DIRETRIZES/README.md", "05_WORKSPACE/README.md",
    "06_OUTPUTS/README.md", "07_LOGS/README.md", "10_TEMPLATES_OPERACIONAIS/README.md",
    "11_TRAFFIC_STACK/README.md", "12_WHATSAPP_STACK/README.md",
    "13_ADAPTIVE_SQUADS/README.md", "15_PRODUCT_RELEASE/COMECE_AQUI.md",
    "15_PRODUCT_RELEASE/GUIA_DE_USO.md", "15_PRODUCT_RELEASE/COMANDOS.md",
    "15_PRODUCT_RELEASE/curso/README.md", "18_AUTOMATION_STACK/README.md",
    "20_MCP_SETUP/README.md", "21_BUILDER_KIT/README.md", "22_CLAUDE_DESKTOP/README.md",
    "KIT_STATUS.json", ".env.example",
    "scripts/obsidian_memory_adapter.py", "scripts/write_obsidian_memory.py",
    "scripts/write-obsidian-memory.ps1", "05_MEMORY/OBSIDIAN-WINDOWS.md",
)


def validate(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    for relative in REQUIRED:
        path = root / relative
        if not path.is_file():
            errors.append(f"ausente: {relative}")
        elif path.stat().st_size == 0:
            errors.append(f"vazio: {relative}")
    status_path = root / "KIT_STATUS.json"
    if status_path.is_file():
        try:
            status = json.loads(status_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as error:
            errors.append(f"KIT_STATUS.json inválido: {error}")
        else:
            safety = status.get("global_safety", {})
            if status.get("release_status") != "core_complete_external_integrations_optional":
                errors.append("KIT_STATUS.json: release_status inesperado")
            if safety.get("credentials_in_repository") is not False:
                errors.append("KIT_STATUS.json: credenciais devem permanecer fora do repositório")
            if safety.get("external_writes_enabled_by_default") is not False:
                errors.append("KIT_STATUS.json: escritas externas devem iniciar desativadas")
            if safety.get("human_approval_for_irreversible_actions") is not True:
                errors.append("KIT_STATUS.json: aprovação humana obrigatória")
    if (root / ".env").is_file():
        errors.append(".env real presente no repositório de distribuição")
    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("KPA V30 inválido:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"KPA V30 válido: {len(REQUIRED)} artefatos críticos verificados.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
