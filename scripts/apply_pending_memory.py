#!/usr/bin/env python3
"""Aplica todos os registros pendentes de 05_MEMORY/pending/ no vault Obsidian.

Pensado pra rodar sozinho (hook SessionEnd do Claude Code) ou manualmente:

    python3 scripts/apply_pending_memory.py

Carrega KPA_OBSIDIAN_VAULT do .env na raiz do repo se a variável ainda não
estiver setada no processo. Sem vault resolvido e com pendentes na fila, sai
com código 1 e avisa — nunca falha silenciosamente, nunca trava a sessão.
Registros aplicados com sucesso são movidos pra 05_MEMORY/applied/ (nunca
apagados), tornando a operação idempotente.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from write_obsidian_memory import to_record, validate_payload  # noqa: E402
from obsidian_memory_adapter import ObsidianMemoryAdapter  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
PENDING_DIR = REPO_ROOT / "05_MEMORY" / "pending"
APPLIED_DIR = REPO_ROOT / "05_MEMORY" / "applied"


def load_dotenv_vault() -> None:
    """Preenche KPA_OBSIDIAN_VAULT a partir do .env se ainda não estiver no ambiente."""
    if os.environ.get("KPA_OBSIDIAN_VAULT"):
        return
    env_path = REPO_ROOT / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        if key.strip() == "KPA_OBSIDIAN_VAULT" and value.strip():
            os.environ["KPA_OBSIDIAN_VAULT"] = value.strip()
            return


def main() -> int:
    load_dotenv_vault()

    if not PENDING_DIR.exists():
        return 0
    records = sorted(PENDING_DIR.glob("*.json"))
    if not records:
        return 0

    vault_value = os.environ.get("KPA_OBSIDIAN_VAULT", "")
    if not vault_value:
        print(
            f"[apply_pending_memory] {len(records)} registro(s) pendente(s), "
            "mas KPA_OBSIDIAN_VAULT nao configurada — nada aplicado. "
            "Configure no .env ou rode com --vault via write_obsidian_memory.py.",
            file=sys.stderr,
        )
        return 1

    applied, blocked = 0, 0
    for record_path in records:
        try:
            value = json.loads(record_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as error:
            print(f"[apply_pending_memory] {record_path.name}: registro invalido ({error})", file=sys.stderr)
            blocked += 1
            continue

        errors = validate_payload(value)
        if errors:
            print(f"[apply_pending_memory] {record_path.name}: bloqueado pelo GATE-MEMORY — {'; '.join(errors)}", file=sys.stderr)
            blocked += 1
            continue

        try:
            written_path = ObsidianMemoryAdapter(vault_value).write_execution(to_record(value))
        except (OSError, ValueError) as error:
            print(f"[apply_pending_memory] {record_path.name}: falha ao gravar ({error})", file=sys.stderr)
            blocked += 1
            continue

        APPLIED_DIR.mkdir(parents=True, exist_ok=True)
        record_path.rename(APPLIED_DIR / record_path.name)
        print(f"[apply_pending_memory] {record_path.name} -> {written_path}")
        applied += 1

    print(f"[apply_pending_memory] {applied} aplicado(s), {blocked} bloqueado(s)/com erro.")
    return 1 if blocked and not applied else 0


if __name__ == "__main__":
    raise SystemExit(main())
