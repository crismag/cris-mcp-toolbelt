"""Memory-record tools: create and search.

These functions take a database-like object (anything exposing
create_memory_record / search_memory_records, such as db.Database) so they can
be unit-tested with a fake. They apply the safety guards before any write.
"""

from __future__ import annotations

from typing import Any

from ..safety import assert_storable


def _record_to_dict(record: Any) -> dict[str, Any]:
    return {
        "id": record.id,
        "workspace": record.workspace,
        "kind": record.kind,
        "content": record.content,
        "created_at": record.created_at.isoformat(),
    }


def create_memory_record(
    db: Any, workspace: str, kind: str, content: str
) -> dict[str, Any]:
    """Store a memory record.

    Raises safety.BlockedRecordError if the record is secret-like.
    """
    workspace = workspace.strip()
    kind = kind.strip()
    if not workspace:
        raise ValueError("workspace must not be empty")
    if not kind:
        raise ValueError("kind must not be empty")
    if not content.strip():
        raise ValueError("content must not be empty")

    assert_storable(kind, content)
    record = db.create_memory_record(workspace, kind, content)
    return _record_to_dict(record)


def search_memory_records(
    db: Any,
    workspace: str | None = None,
    query: str | None = None,
    kind: str | None = None,
    limit: int = 20,
) -> list[dict[str, Any]]:
    """Search stored memory records, most recent first."""
    records = db.search_memory_records(
        workspace=workspace or None,
        query=query or None,
        kind=kind or None,
        limit=limit,
    )
    return [_record_to_dict(r) for r in records]
