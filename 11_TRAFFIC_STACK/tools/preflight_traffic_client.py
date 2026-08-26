#!/usr/bin/env python3
"""Audita e prepara um workspace de tráfego para execução somente leitura."""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
from pathlib import Path
import re
import sys
import tempfile
from typing import Any


VALIDATOR_PATHS = {
    "google_ads": Path(__file__).with_name("validate_google_ads_export.py"),
    "meta_ads": Path(__file__).with_name("validate_meta_ads_export.py"),
}
SAFE_TEXT_PATTERN = re.compile(r"^[^\r\n]{1,200}$")
REQUIRED_FILES = (
    "CLAUDE.md",
    "act-mapping.yaml",
    "baseline-kpis.md",
    "funil.md",
    "icp.md",
    "traffic-schedule.json",
    "traffic-state.json",
)


def load_validator(platform: str) -> Any:
    path = VALIDATOR_PATHS.get(platform)
    if path is None:
        raise RuntimeError(f"plataforma de export não suportada: {platform!r}")
    spec = importlib.util.spec_from_file_location(f"{platform}_export_validator", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"não foi possível carregar o validador {platform}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_json(path: Path, label: str, errors: list[str]) -> dict[str, Any] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        errors.append(f"{label}: não foi possível ler JSON: {error}")
        return None
    if not isinstance(value, dict):
        errors.append(f"{label}: objeto JSON obrigatório")
        return None
    return value


def safe_text(value: str, field: str, errors: list[str]) -> None:
    if not SAFE_TEXT_PATTERN.fullmatch(value.strip()):
        errors.append(f"{field}: texto obrigatório em uma linha, máximo 200 caracteres")


def audit(
    workspace: Path,
    export: Path,
    collector_source: str,
    conversion_action: str,
    owner: str,
) -> tuple[dict[str, Any] | None, dict[str, Any] | None, list[str]]:
    errors: list[str] = []
    if not workspace.is_dir():
        return None, None, [f"workspace inexistente: {workspace}"]
    for filename in REQUIRED_FILES:
        if not (workspace / filename).is_file():
            errors.append(f"workspace: arquivo obrigatório ausente: {filename}")
    safe_text(collector_source, "collector-source", errors)
    safe_text(conversion_action, "conversion-action", errors)
    safe_text(owner, "owner", errors)
    state = load_json(workspace / "traffic-state.json", "traffic-state.json", errors)
    schedule = load_json(workspace / "traffic-schedule.json", "traffic-schedule.json", errors)
    export_payload = load_json(export, "export", errors)
    if export_payload is not None:
        platform = export_payload.get("platform")
        try:
            validator = load_validator(platform)
        except RuntimeError as error:
            errors.append(f"export: {error}")
        else:
            errors.extend(f"export: {error}" for error in validator.validate_payload(export_payload))
    if state is not None:
        if state.get("contains_credentials") is not False:
            errors.append("traffic-state.json: contains_credentials deve ser false")
        if state.get("client_name") in (None, "", "[A PREENCHER]"):
            errors.append("traffic-state.json: client_name obrigatório")
    if schedule is not None:
        safety = schedule.get("safety", {})
        if safety.get("read_only") is not True:
            errors.append("traffic-schedule.json: read_only deve ser true")
        if safety.get("allow_platform_writes") is not False:
            errors.append("traffic-schedule.json: escrita em plataforma deve estar bloqueada")
        if safety.get("require_human_approval") is not True:
            errors.append("traffic-schedule.json: aprovação humana deve ser obrigatória")
        if any(job.get("enabled") is not False for job in schedule.get("jobs", [])):
            errors.append("traffic-schedule.json: todos os jobs devem permanecer desativados no preflight")
    return state, schedule, errors


def atomic_write_json(path: Path, value: dict[str, Any]) -> None:
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workspace", type=Path)
    parser.add_argument("--export", required=True, type=Path)
    parser.add_argument("--collector-source", required=True)
    parser.add_argument("--conversion-action", required=True)
    parser.add_argument("--owner", required=True)
    parser.add_argument("--apply", action="store_true", help="Persiste o preflight; padrão é dry-run")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    workspace = args.workspace.expanduser().resolve()
    export = args.export.expanduser().resolve()
    state, schedule, errors = audit(
        workspace,
        export,
        args.collector_source,
        args.conversion_action,
        args.owner,
    )
    if errors:
        print("preflight bloqueado:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    assert state is not None and schedule is not None
    print("Preflight aprovado em modo somente leitura.")
    print(f"Workspace: {workspace}")
    print(f"Export: {export}")
    if not args.apply:
        print("Dry-run: nenhum arquivo foi alterado.")
        return 0
    state.update(
        {
            "preflight_status": "approved",
            "collector_status": "validated_read_only",
            "collector_source": args.collector_source.strip(),
            "conversion_action": args.conversion_action.strip(),
            "owner": args.owner.strip(),
            "schedule_status": "draft_disabled",
        }
    )
    for job in schedule["jobs"]:
        job["input_export"] = str(export)
        job["owner"] = args.owner.strip()
        job["enabled"] = False
    atomic_write_json(workspace / "traffic-schedule.json", schedule)
    atomic_write_json(workspace / "traffic-state.json", state)
    print("Preflight persistido; jobs continuam desativados.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
