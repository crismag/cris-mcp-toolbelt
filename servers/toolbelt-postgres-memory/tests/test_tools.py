"""Tests for the memory and audit tool functions.

These use an in-memory fake database, so they exercise the tool layer —
including the safety guard on memory writes — without psycopg or PostgreSQL.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

import pytest

from toolbelt_postgres_memory.safety import BlockedRecordError
from toolbelt_postgres_memory.tools import audit, memory


@dataclass
class _Row:
    id: int
    workspace: str
    kind: str = ""
    content: str = ""
    tool: str = ""
    action: str = ""
    detail: str = ""
    created_at: datetime = datetime(2026, 1, 1, tzinfo=timezone.utc)


class FakeDB:
    """In-memory stand-in for db.Database."""

    def __init__(self) -> None:
        self.memory: list[_Row] = []
        self.audit: list[_Row] = []

    def create_memory_record(self, workspace, kind, content):
        row = _Row(len(self.memory) + 1, workspace, kind=kind, content=content)
        self.memory.append(row)
        return row

    def search_memory_records(self, workspace=None, query=None, kind=None, limit=20):
        rows = self.memory
        if workspace:
            rows = [r for r in rows if r.workspace == workspace]
        if kind:
            rows = [r for r in rows if r.kind == kind]
        if query:
            rows = [r for r in rows if query in r.content]
        return rows[:limit]

    def create_audit_event(self, workspace, tool, action, detail=""):
        row = _Row(
            len(self.audit) + 1, workspace, tool=tool, action=action, detail=detail
        )
        self.audit.append(row)
        return row

    def list_audit_events(self, workspace=None, limit=20):
        rows = self.audit
        if workspace:
            rows = [r for r in rows if r.workspace == workspace]
        return rows[:limit]


def test_create_memory_record_returns_json_safe_dict():
    db = FakeDB()
    result = memory.create_memory_record(db, "ws", "decision", "use postgres")
    assert result["id"] == 1
    assert result["kind"] == "decision"
    assert isinstance(result["created_at"], str)  # isoformatted


def test_create_memory_record_blocks_secret_kind():
    db = FakeDB()
    with pytest.raises(BlockedRecordError):
        memory.create_memory_record(db, "ws", "access_token", "value")
    assert db.memory == []


def test_create_memory_record_blocks_secret_content():
    db = FakeDB()
    with pytest.raises(BlockedRecordError):
        memory.create_memory_record(db, "ws", "note", "key is sk-" + "z" * 30)
    assert db.memory == []


def test_create_memory_record_rejects_empty_workspace():
    db = FakeDB()
    with pytest.raises(ValueError):
        memory.create_memory_record(db, "  ", "note", "content")


def test_search_memory_records():
    db = FakeDB()
    memory.create_memory_record(db, "ws", "decision", "use postgres")
    memory.create_memory_record(db, "ws", "note", "remember the schema")
    results = memory.search_memory_records(db, workspace="ws", query="postgres")
    assert len(results) == 1
    assert results[0]["content"] == "use postgres"


def test_create_and_list_audit_events():
    db = FakeDB()
    audit.create_audit_event(db, "ws", "filesystem-controlled", "write", "edited a file")
    events = audit.list_audit_events(db, workspace="ws")
    assert len(events) == 1
    assert events[0]["tool"] == "filesystem-controlled"
    assert isinstance(events[0]["created_at"], str)


def test_create_audit_event_rejects_empty_tool():
    db = FakeDB()
    with pytest.raises(ValueError):
        audit.create_audit_event(db, "ws", "  ", "action")
