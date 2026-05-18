"""JSONL audit log for command-runner-controlled."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def record_event(audit_log: Path, event: dict[str, Any]) -> dict[str, Any]:
    """Append an audit event and return the persisted event."""
    persisted = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        **event,
    }
    audit_log.parent.mkdir(parents=True, exist_ok=True)
    with audit_log.open("a", encoding="utf-8") as file:
        file.write(json.dumps(persisted, sort_keys=True) + "\n")
    return persisted


def list_events(audit_log: Path, limit: int = 20) -> list[dict[str, Any]]:
    """Return most recent audit events first."""
    if not audit_log.exists():
        return []
    safe_limit = max(1, min(limit, 100))
    lines = audit_log.read_text(encoding="utf-8").splitlines()
    events: list[dict[str, Any]] = []
    for line in reversed(lines[-safe_limit:]):
        if not line.strip():
            continue
        events.append(json.loads(line))
    return events
