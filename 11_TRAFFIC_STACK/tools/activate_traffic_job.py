#!/usr/bin/env python3
"""Ativa um job local após preflight aprovado e confirmação explícita."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys
import tempfile
from typing import Any


CONFIRMATION = "ATIVAR SOMENTE LEITURA"


def load_object(path: Path, label: str) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{label}: objeto JSON obrigatório")
    return value


def atomic_write(path: Path, value: dict[str, Any]) -> None:
    descriptor, name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary = Path(name)
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


def validate(schedule: dict[str, Any], state: dict[str, Any], job_id: str) -> list[str]:
    errors: list[str] = []
    safety = schedule.get("safety", {})
    required_safety = {
        "read_only": True,
        "allow_platform_writes": False,
        "require_human_approval": True,
    }
    for field, expected in required_safety.items():
        if safety.get(field) is not expected:
            errors.append(f"safety.{field}: deve ser {str(expected).lower()}")
    required_state = {
        "preflight_status": "approved",
        "collector_status": "validated_read_only",
        "contains_credentials": False,
    }
    for field, expected in required_state.items():
        if state.get(field) != expected:
            errors.append(f"state.{field}: deve ser {expected!r}")
    jobs = schedule.get("jobs")
    if not isinstance(jobs, list):
        errors.append("jobs: lista obrigatória")
        return errors
    matches = [job for job in jobs if isinstance(job, dict) and job.get("id") == job_id]
    if len(matches) != 1:
        errors.append(f"jobs: id {job_id!r} deve existir exatamente uma vez")
    elif matches[0].get("input_export") in (None, "", "[CAMINHO_EXPORT_JSON]"):
        errors.append("job.input_export: export validado obrigatório")
    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workspace", type=Path)
    parser.add_argument("--job", required=True)
    parser.add_argument("--confirm", required=True, help=f"Digite exatamente: {CONFIRMATION}")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.confirm != CONFIRMATION:
        print("ativação bloqueada: confirmação explícita inválida", file=sys.stderr)
        return 1
    workspace = args.workspace.expanduser().resolve()
    schedule_path = workspace / "traffic-schedule.json"
    state_path = workspace / "traffic-state.json"
    try:
        schedule = load_object(schedule_path, "traffic-schedule.json")
        state = load_object(state_path, "traffic-state.json")
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as error:
        print(f"ativação bloqueada: {error}", file=sys.stderr)
        return 2
    errors = validate(schedule, state, args.job)
    if errors:
        print("ativação bloqueada:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    for job in schedule["jobs"]:
        if job["id"] == args.job:
            job["enabled"] = True
    state["schedule_status"] = f"enabled:{args.job}"
    try:
        atomic_write(schedule_path, schedule)
        atomic_write(state_path, state)
    except OSError as error:
        print(f"falha ao persistir ativação: {error}", file=sys.stderr)
        return 2
    print(f"Job ativado em modo somente leitura: {args.job}")
    print("A ativação não instala cron nem concede acesso à plataforma.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

