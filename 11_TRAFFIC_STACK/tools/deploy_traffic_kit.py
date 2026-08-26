#!/usr/bin/env python3
"""Implanta o kit local de tráfego sem habilitar coletores ou escritas em plataformas."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import tempfile
from typing import Any


REQUIRED_WORKSPACE_FILES = (
    "CLAUDE.md",
    "act-mapping.yaml",
    "baseline-kpis.md",
    "funil.md",
    "icp.md",
    "traffic-schedule.json",
    "traffic-state.json",
)
REQUIRED_SAFETY = {
    "read_only": True,
    "allow_platform_writes": False,
    "require_human_approval": True,
}


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: objeto JSON obrigatório")
    return value


def audit(workspace: Path) -> tuple[dict[str, Any] | None, list[str]]:
    errors: list[str] = []
    if not workspace.is_dir():
        return None, [f"workspace inexistente: {workspace}"]
    for name in REQUIRED_WORKSPACE_FILES:
        if not (workspace / name).is_file():
            errors.append(f"arquivo obrigatório ausente: {name}")
    if errors:
        return None, errors
    try:
        state = read_json(workspace / "traffic-state.json")
        schedule = read_json(workspace / "traffic-schedule.json")
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as error:
        return None, [str(error)]
    safety = schedule.get("safety")
    if not isinstance(safety, dict):
        errors.append("traffic-schedule.json: safety obrigatório")
    else:
        for key, expected in REQUIRED_SAFETY.items():
            if safety.get(key) is not expected:
                errors.append(f"traffic-schedule.json: safety.{key} deve ser {expected}")
    if any(job.get("enabled") is not False for job in schedule.get("jobs", [])):
        errors.append("traffic-schedule.json: implantação exige todos os jobs desativados")
    if state.get("contains_credentials") is not False:
        errors.append("traffic-state.json: contains_credentials deve ser false")
    if errors:
        return None, errors
    manifest = {
        "version": "1.0",
        "deployment_status": "local_kit_installed_external_integrations_pending",
        "client": state.get("client_name"),
        "workspace_slug": workspace.name,
        "components": {
            "client_workspace": "installed",
            "diagnostic_playbooks": "installed",
            "report_templates": "installed",
            "manual_meta_workflow": "installed",
            "drafts_inventory": "installed" if (workspace / "meta-drafts-inventory.csv").is_file() else "not_installed",
            "meta_export_contract": "installed",
            "meta_collector": "pending_real_export_and_read_only_validation",
            "google_ads_collector": "not_requested",
            "scheduler": "installed_disabled_pending_validated_collector",
            "platform_writes": "blocked",
        },
        "safety": REQUIRED_SAFETY,
        "activation_blockers": [
            "15 Meta account drafts not audited",
            "Meta location entities, presence and expansion not verified",
            "Meta real export and read-only collector not validated",
        ],
    }
    return manifest, []


def atomic_write(path: Path, value: dict[str, Any]) -> None:
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            json.dump(value, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        temporary.replace(path)
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workspace", type=Path)
    parser.add_argument("--apply", action="store_true", help="Grava traffic-kit-deployment.json")
    args = parser.parse_args()
    workspace = args.workspace.expanduser().resolve()
    manifest, errors = audit(workspace)
    if errors:
        print("implantação bloqueada:")
        for error in errors:
            print(f"- {error}")
        return 1
    assert manifest is not None
    print("Kit local validado em modo somente leitura.")
    if not args.apply:
        print("Dry-run: nenhum arquivo alterado.")
        return 0
    output = workspace / "traffic-kit-deployment.json"
    atomic_write(output, manifest)
    print(f"Manifesto gravado: {output}")
    print("Coletores, scheduler e escritas em plataforma permanecem desativados.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
