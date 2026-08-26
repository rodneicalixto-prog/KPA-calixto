from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import re
from typing import Iterable

SECRET_PATTERNS = [
    re.compile(r"(?i)(api[_-]?key|token|password|secret|authorization)\s*[:=]\s*\S+"),
]

@dataclass
class MemoryRecord:
    project: str
    task_id: str
    title: str
    summary: str
    result: str
    worked: str = ""
    failed: str = ""
    decision: str = ""
    next_action: str = ""
    links: tuple[str, ...] = ()

class ObsidianMemoryAdapter:
    """Filesystem adapter for an Obsidian vault. No Obsidian plugin is required."""

    def __init__(self, vault_path: str | Path):
        self.vault = Path(vault_path).expanduser().resolve()
        if not self.vault.exists() or not self.vault.is_dir():
            raise FileNotFoundError(f"Vault not found: {self.vault}")

    def _safe_text(self, value: str) -> str:
        out = value or ""
        for pattern in SECRET_PATTERNS:
            out = pattern.sub("[REDACTED]", out)
        return out.strip()

    def search(self, terms: Iterable[str], roots: Iterable[str] = ("02_Projects", "05_Knowledge", "06_Decisions", "08_Lessons"), limit: int = 12):
        needles = [t.lower().strip() for t in terms if t and t.strip()]
        scored = []
        for root in roots:
            base = self.vault / root
            if not base.exists():
                continue
            for path in base.rglob("*.md"):
                try:
                    text = path.read_text(encoding="utf-8")
                except UnicodeDecodeError:
                    text = path.read_text(encoding="utf-8", errors="replace")
                haystack = f"{path.name}\n{text}".lower()
                score = sum(haystack.count(n) for n in needles)
                if score:
                    scored.append((score, path, text))
        scored.sort(key=lambda x: (-x[0], str(x[1])))
        return [
            {"score": score, "path": str(path.relative_to(self.vault)), "content": text}
            for score, path, text in scored[:limit]
        ]

    def write_execution(self, record: MemoryRecord) -> Path:
        date = datetime.now().astimezone()
        project_dir = self.vault / "07_Executions" / self._slug(record.project)
        project_dir.mkdir(parents=True, exist_ok=True)
        filename = f"{date:%Y-%m-%d_%H%M}-{self._slug(record.task_id)}.md"
        path = project_dir / filename
        links = "\n".join(f"- [[{x}]]" for x in record.links) or "- none"
        body = f"""---
type: kpa_execution
project: {self._safe_text(record.project)}
task_id: {self._safe_text(record.task_id)}
date: {date.isoformat()}
status: approved_memory_write
---

# {self._safe_text(record.title)}

## Resumo
{self._safe_text(record.summary)}

## Resultado
{self._safe_text(record.result)}

## Funcionou
{self._safe_text(record.worked) or '-'}

## Falhou / ressalvas
{self._safe_text(record.failed) or '-'}

## Decisão
{self._safe_text(record.decision) or '-'}

## Próxima ação
{self._safe_text(record.next_action) or '-'}

## Links
{links}
"""
        path.write_text(body, encoding="utf-8")
        return path

    @staticmethod
    def _slug(value: str) -> str:
        value = re.sub(r"[^A-Za-z0-9._-]+", "-", value.strip())
        return value.strip("-") or "item"
