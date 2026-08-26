#!/usr/bin/env python3
"""Executa localmente um job de tráfego configurado, sem acessar plataformas."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys
from typing import Any


RENDERER = Path(__file__).with_name("render_google_ads_report.py")
REQUIRED_SAFETY = {
    "read_only": True,
    "allow_platform_writes": False,
    "require_human_approval": True,
}
SUPPORTED_MODES = {"weekly_review"}


def validate_config(config: Any, job_id: str) -> tuple[dict[str, Any] | None, list[str]]:
    errors: list[str] = []
    if not isinstance(config, dict):
        return None, ["root: objeto JSON obrigatório"]
    if config.get("version") != "1.0":
        errors.append("version: versão suportada é 1.0")
    client = config.get("client")
    if not isinstance(client, str) or not client.strip() or client == "[A_PREENCHER]":
        errors.append("client: nome público obrigatório")
    state_file = config.get("state_file")
    if not isinstance(state_file, str) or not state_file.strip() or "[" in state_file:
        errors.append("state_file: caminho preenchido obrigatório")
    safety = config.get("safety")
    if not isinstance(safety, dict):
        errors.append("safety: objeto obrigatório")
    else:
        for field, expected in REQUIRED_SAFETY.items():
            if safety.get(field) is not expected:
                errors.append(f"safety.{field}: deve ser {str(expected).lower()}")

    jobs = config.get("jobs")
    if not isinstance(jobs, list):
        return None, errors + ["jobs: lista obrigatória"]
    matches = [job for job in jobs if isinstance(job, dict) and job.get("id") == job_id]
    if len(matches) != 1:
        errors.append(f"jobs: id {job_id!r} deve existir exatamente uma vez")
        return None, errors
    job = matches[0]
    if job.get("mode") not in SUPPORTED_MODES:
        errors.append(f"job.mode: suportado apenas {sorted(SUPPORTED_MODES)}")
    for field in ("input_export", "output_html"):
        value = job.get(field)
        if not isinstance(value, str) or not value.strip() or "[" in value or "]" in value:
            errors.append(f"job.{field}: caminho preenchido obrigatório")
    return job, errors


def load_config(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None, f"configuração não encontrada: {path}"
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        return None, f"configuração inválida: {error}"
    if not isinstance(value, dict):
        return None, "configuração deve ser um objeto JSON"
    return value, None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("config", type=Path, help="Configuração JSON do runtime")
    parser.add_argument("--job", required=True, help="ID exato do job")
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Executa o renderer; sem esta flag apenas valida e mostra o plano",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    config, load_error = load_config(args.config)
    if load_error:
        print(load_error, file=sys.stderr)
        return 2
    assert config is not None
    job, errors = validate_config(config, args.job)
    if errors:
        print("job bloqueado:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    assert job is not None
    input_export = Path(job["input_export"]).expanduser()
    output_html = Path(job["output_html"]).expanduser()
    print(f"Job: {job['id']}")
    print(f"Modo: {job['mode']}")
    print(f"Entrada: {input_export}")
    print(f"Saída: {output_html}")
    print("Acesso à plataforma: não")
    if not args.execute:
        print("Dry-run aprovado; nada foi escrito.")
        return 0
    if job.get("enabled") is not True:
        print("job bloqueado: enabled deve ser true para --execute", file=sys.stderr)
        return 1
    state_path = Path(str(config["state_file"])).expanduser()
    if not state_path.is_absolute():
        state_path = args.config.expanduser().resolve().parent / state_path
    state, state_error = load_config(state_path)
    if state_error:
        print(f"job bloqueado: {state_error}", file=sys.stderr)
        return 1
    assert state is not None
    required_state = {
        "preflight_status": "approved",
        "collector_status": "validated_read_only",
        "contains_credentials": False,
    }
    state_errors = [
        f"state.{field}: deve ser {expected!r}"
        for field, expected in required_state.items()
        if state.get(field) != expected
    ]
    if state_errors:
        print("job bloqueado:", file=sys.stderr)
        for error in state_errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    command = [
        sys.executable,
        str(RENDERER),
        str(input_export),
        str(output_html),
        "--client",
        str(config["client"]),
    ]
    sys.stdout.flush()
    result = subprocess.run(command, check=False)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
