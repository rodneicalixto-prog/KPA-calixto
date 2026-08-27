#!/usr/bin/env python3
"""Audita o runtime local antes de conectar Codex a plataformas de anúncios."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import sys
import tempfile
from typing import Any
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


PORTABLE_TIMEZONES = frozenset({"America/Sao_Paulo", "Etc/UTC", "UTC"})
ENV_REF = re.compile(r"^[A-Z][A-Z0-9_]{1,79}$")
REQUIRED_SAFETY = {
    "read_only": True,
    "allow_platform_writes": False,
    "contains_credentials": False,
    "require_human_approval": True,
}


def timezone_supported(value: str) -> bool:
    try:
        ZoneInfo(value)
        return True
    except (ZoneInfoNotFoundError, ValueError):
        return value in PORTABLE_TIMEZONES


def load_config(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("configuração deve ser um objeto JSON")
    return value


def audit(config: dict[str, Any], repo_root: Path) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    if config.get("version") != "1.0":
        errors.append("version: deve ser 1.0")
    if config.get("runtime") != "codex":
        errors.append("runtime: deve ser codex")
    timezone_name = config.get("timezone")
    if not isinstance(timezone_name, str) or not timezone_supported(timezone_name):
        errors.append("timezone: IANA inválido ou não suportado")
    paths = config.get("paths")
    resolved_paths: dict[str, str] = {}
    if not isinstance(paths, dict):
        errors.append("paths: objeto obrigatório")
    else:
        for name in ("workspace", "outputs", "logs"):
            relative = paths.get(name)
            if not isinstance(relative, str) or not relative.strip() or Path(relative).is_absolute():
                errors.append(f"paths.{name}: caminho relativo obrigatório")
                continue
            resolved = (repo_root / relative).resolve()
            try:
                resolved.relative_to(repo_root)
            except ValueError:
                errors.append(f"paths.{name}: caminho fora do repositório")
                continue
            if not resolved.is_dir():
                errors.append(f"paths.{name}: diretório inexistente")
            resolved_paths[name] = Path(relative).as_posix()
    refs = config.get("environment_refs")
    ref_status: dict[str, str] = {}
    if not isinstance(refs, list) or any(not isinstance(ref, str) for ref in refs):
        errors.append("environment_refs: lista de nomes obrigatória")
    else:
        for ref in refs:
            if not ENV_REF.fullmatch(ref):
                errors.append(f"environment_refs: nome inválido: {ref!r}")
            else:
                ref_status[ref] = "configured" if os.environ.get(ref) else "pending"
    safety = config.get("safety")
    if not isinstance(safety, dict):
        errors.append("safety: objeto obrigatório")
    else:
        for key, expected in REQUIRED_SAFETY.items():
            if safety.get(key) is not expected:
                errors.append(f"safety.{key}: deve ser {str(expected).lower()}")
    platforms = config.get("platforms")
    if not isinstance(platforms, dict):
        errors.append("platforms: objeto obrigatório")
    else:
        for platform in ("meta_ads", "google_ads"):
            if platforms.get(platform) != "disabled":
                errors.append(f"platforms.{platform}: deve permanecer disabled no preflight")
    refs_pending = any(status == "pending" for status in ref_status.values())
    report = {
        "version": "1.0",
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "status": (
            "blocked"
            if errors
            else "ready_with_external_refs_pending"
            if refs_pending
            else "ready"
        ),
        "python": {"executable": sys.executable, "version": list(sys.version_info[:3])},
        "timezone": timezone_name,
        "paths": resolved_paths,
        "environment_refs": ref_status,
        "platform_access_performed": False,
        "platform_writes_enabled": False,
        "errors": errors,
    }
    return report, errors


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
    parser.add_argument("config", type=Path)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--apply", action="store_true", help="Grava o relatório ao lado da configuração")
    args = parser.parse_args()
    try:
        config = load_config(args.config)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as error:
        print(f"preflight bloqueado: {error}", file=sys.stderr)
        return 2
    report, errors = audit(config, args.repo_root.expanduser().resolve())
    if errors:
        print("preflight bloqueado:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("Runtime Codex aprovado sem acesso a plataformas.")
    for ref, status in report["environment_refs"].items():
        print(f"Referência {ref}: {status}")
    if not args.apply:
        print("Dry-run: nenhum arquivo alterado.")
        return 0
    output = args.config.with_name("codex-ads-runtime-preflight.json")
    atomic_write(output, report)
    print(f"Relatório gravado: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
