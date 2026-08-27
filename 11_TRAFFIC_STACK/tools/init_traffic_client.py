#!/usr/bin/env python3
"""Inicializa um workspace de cliente da Traffic Stack sem credenciais."""

from __future__ import annotations

import argparse
from datetime import date
import json
from pathlib import Path
import re
import shutil
import sys
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


STACK = Path(__file__).resolve().parents[1]
REPO_ROOT = STACK.parent
CLIENT_TEMPLATE = STACK / "templates" / "cliente-template"
SCHEDULE_TEMPLATE = STACK / "templates" / "schedule-runtime-template.json"
SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
CURRENCY_PATTERN = re.compile(r"^[A-Z]{3}$")
ACCOUNT_SUFFIX_PATTERN = re.compile(r"^\d{4}$")
PORTABLE_IANA_TIMEZONES = frozenset({"America/Sao_Paulo", "Etc/UTC", "UTC"})


def is_supported_timezone(value: str) -> bool:
    """Valida IANA usando o SO e preserva os timezones do kit sem tzdata."""
    try:
        ZoneInfo(value)
        return True
    except (ZoneInfoNotFoundError, ValueError):
        return value in PORTABLE_IANA_TIMEZONES


def validate_inputs(
    slug: str,
    name: str,
    timezone: str,
    currency: str,
    account_suffix: str | None,
) -> list[str]:
    errors: list[str] = []
    if not SLUG_PATTERN.fullmatch(slug):
        errors.append("slug: use letras minúsculas, números e hífens, sem caminhos")
    if not name.strip() or any(character in name for character in "\r\n"):
        errors.append("name: nome público não vazio e em uma linha")
    if not is_supported_timezone(timezone):
        errors.append("timezone: identificador IANA inválido ou não suportado")
    if not CURRENCY_PATTERN.fullmatch(currency):
        errors.append("currency: use três letras maiúsculas")
    if account_suffix is not None and not ACCOUNT_SUFFIX_PATTERN.fullmatch(account_suffix):
        errors.append("account-suffix: informe somente os quatro últimos dígitos")
    return errors


def replace_text(path: Path, replacements: dict[str, str]) -> None:
    content = path.read_text(encoding="utf-8")
    for source, target in replacements.items():
        content = content.replace(source, target)
    path.write_text(content, encoding="utf-8")


def build_workspace(
    destination: Path,
    *,
    slug: str,
    name: str,
    timezone: str,
    currency: str,
    account_suffix: str | None,
) -> None:
    destination.mkdir(parents=True, exist_ok=False)
    for template in CLIENT_TEMPLATE.iterdir():
        if template.is_file():
            shutil.copyfile(template, destination / template.name)

    replacements = {
        "[NOME]": name,
        'client: "[A_PREENCHER]"': f'client: "{slug}"',
        "[A_PREENCHER]": "[A PREENCHER]",
        'timezone: "America/Sao_Paulo"': f'timezone: "{timezone}"',
        'currency: "BRL"': f'currency: "{currency}"',
        'act_id: "[ACT_ID_SEM_TOKEN]"': (
            f'act_id: "masked-{account_suffix}"'
            if account_suffix
            else 'act_id: "[A PREENCHER LOCALMENTE]"'
        ),
    }
    for path in destination.iterdir():
        if path.is_file():
            replace_text(path, replacements)

    schedule = json.loads(SCHEDULE_TEMPLATE.read_text(encoding="utf-8"))
    schedule["client"] = name
    schedule["state_file"] = "traffic-state.json"
    for job in schedule["jobs"]:
        job["output_html"] = (
            f"06_OUTPUTS/{slug}/traffic/diagnostico-google-ads.html"
        )
    (destination / "traffic-schedule.json").write_text(
        json.dumps(schedule, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    state = {
        "schema_version": "1.0",
        "client_slug": slug,
        "client_name": name,
        "created_at": date.today().isoformat(),
        "timezone": timezone,
        "currency": currency,
        "account_suffix": account_suffix or "[A PREENCHER LOCALMENTE]",
        "preflight_status": "pending",
        "collector_status": "not_configured",
        "schedule_status": "draft_disabled",
        "contains_credentials": False,
    }
    (destination / "traffic-state.json").write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--slug", required=True)
    parser.add_argument("--name", required=True, help="Nome público do cliente")
    parser.add_argument("--timezone", default="America/Sao_Paulo")
    parser.add_argument("--currency", default="BRL")
    parser.add_argument(
        "--account-suffix",
        help="Somente os quatro últimos dígitos; nunca informe o ID completo",
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        default=REPO_ROOT / "05_WORKSPACE" / "clientes",
        help="Raiz onde a pasta do cliente será criada",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    errors = validate_inputs(
        args.slug,
        args.name,
        args.timezone,
        args.currency,
        args.account_suffix,
    )
    if errors:
        print("inicialização bloqueada:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    destination = args.output_root.expanduser().resolve() / args.slug
    if destination.exists():
        print(f"inicialização bloqueada: destino já existe: {destination}", file=sys.stderr)
        return 1
    try:
        build_workspace(
            destination,
            slug=args.slug,
            name=args.name.strip(),
            timezone=args.timezone,
            currency=args.currency,
            account_suffix=args.account_suffix,
        )
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        print(f"falha ao criar workspace: {error}", file=sys.stderr)
        if destination.exists():
            shutil.rmtree(destination)
        return 2
    print(f"Workspace criado: {destination}")
    print("Próximo passo: preencher preflight e configurar coletor somente leitura.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
