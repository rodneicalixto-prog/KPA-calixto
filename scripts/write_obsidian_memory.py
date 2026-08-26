#!/usr/bin/env python3
"""Valida e grava uma memória KPA em um vault Obsidian explicitamente configurado."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys
from typing import Any

from obsidian_memory_adapter import MemoryRecord, ObsidianMemoryAdapter


REQUIRED_TEXT = ("project", "task_id", "title", "summary", "result", "decision", "next_action")


def validate_payload(value: Any) -> list[str]:
    if not isinstance(value, dict):
        return ["root: objeto JSON obrigatório"]
    errors: list[str] = []
    for field in REQUIRED_TEXT:
        text = value.get(field)
        if not isinstance(text, str) or not text.strip():
            errors.append(f"{field}: texto obrigatório")
    if value.get("gate_status") not in {"approved", "approved_with_concerns"}:
        errors.append("gate_status: deve ser approved ou approved_with_concerns")
    if value.get("contains_credentials") is not False:
        errors.append("contains_credentials: deve ser false")
    links = value.get("links", [])
    if not isinstance(links, list) or any(not isinstance(item, str) for item in links):
        errors.append("links: lista de textos obrigatória")
    return errors


def to_record(value: dict[str, Any]) -> MemoryRecord:
    return MemoryRecord(
        project=value["project"], task_id=value["task_id"], title=value["title"],
        summary=value["summary"], result=value["result"], worked=value.get("worked", ""),
        failed=value.get("failed", ""), decision=value["decision"],
        next_action=value["next_action"], links=tuple(value.get("links", [])),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("record", type=Path, help="Registro JSON aprovado pelo GATE-MEMORY")
    parser.add_argument("--vault", type=Path, help="Sobrescreve KPA_OBSIDIAN_VAULT")
    parser.add_argument("--apply", action="store_true", help="Grava a nota; padrão é dry-run")
    args = parser.parse_args()
    try:
        value = json.loads(args.record.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        print(f"registro inválido: {error}", file=sys.stderr)
        return 2
    errors = validate_payload(value)
    if errors:
        print("memória bloqueada:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("GATE-MEMORY aprovado.")
    if not args.apply:
        print("Dry-run: nenhuma nota foi gravada.")
        return 0
    vault_value = str(args.vault) if args.vault else os.environ.get("KPA_OBSIDIAN_VAULT", "")
    if not vault_value:
        print("gravação bloqueada: configure KPA_OBSIDIAN_VAULT ou --vault", file=sys.stderr)
        return 1
    try:
        path = ObsidianMemoryAdapter(vault_value).write_execution(to_record(value))
    except (OSError, ValueError) as error:
        print(f"gravação bloqueada: {error}", file=sys.stderr)
        return 1
    print(f"Memória gravada: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
