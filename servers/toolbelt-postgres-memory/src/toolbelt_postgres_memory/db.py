"""PostgreSQL data layer for the toolbelt-postgres-memory server.

All writes go to the toolbelt-owned schema. Every query is parameterized; the
only value interpolated into SQL text is the schema name, which is validated
as an identifier by config.load_config().

Requires: psycopg (version 3).
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import psycopg

from .config import Config

_SCHEMA_SQL = Path(__file__).parent / "schemas" / "init.sql"


@dataclass(frozen=True)
class MemoryRecord:
    id: int
    workspace: str
    kind: str
    content: str
    created_at: datetime


@dataclass(frozen=True)
class AuditEvent:
    id: int
    workspace: str
    tool: str
    action: str
    detail: str
    created_at: datetime


class Database:
    """Thin PostgreSQL access layer scoped to the toolbelt schema."""

    def __init__(self, config: Config) -> None:
        self._dsn = config.database_url
        self._schema = config.schema

    def _connect(self) -> psycopg.Connection:
        return psycopg.connect(self._dsn)

    def _q(self, sql: str) -> str:
        """Interpolate the validated schema name into a SQL statement."""
        return sql.replace("{schema}", self._schema)

    def init_schema(self) -> None:
        """Create the toolbelt schema and tables. Idempotent."""
        sql = self._q(_SCHEMA_SQL.read_text(encoding="utf-8"))
        with self._connect() as conn, conn.cursor() as cur:
            cur.execute(sql)
            conn.commit()

    def create_memory_record(
        self, workspace: str, kind: str, content: str
    ) -> MemoryRecord:
        sql = self._q(
            "INSERT INTO {schema}.memory_records (workspace, kind, content) "
            "VALUES (%s, %s, %s) RETURNING id, workspace, kind, content, created_at"
        )
        with self._connect() as conn, conn.cursor() as cur:
            cur.execute(sql, (workspace, kind, content))
            row = cur.fetchone()
            conn.commit()
        return MemoryRecord(*row)

    def search_memory_records(
        self,
        workspace: str | None = None,
        query: str | None = None,
        kind: str | None = None,
        limit: int = 20,
    ) -> list[MemoryRecord]:
        clauses: list[str] = []
        params: list[object] = []
        if workspace:
            clauses.append("workspace = %s")
            params.append(workspace)
        if kind:
            clauses.append("kind = %s")
            params.append(kind)
        if query:
            clauses.append("content ILIKE %s")
            params.append(f"%{query}%")
        where = (" WHERE " + " AND ".join(clauses)) if clauses else ""
        params.append(max(1, min(limit, 100)))
        sql = self._q(
            "SELECT id, workspace, kind, content, created_at "
            "FROM {schema}.memory_records" + where +
            " ORDER BY created_at DESC LIMIT %s"
        )
        with self._connect() as conn, conn.cursor() as cur:
            cur.execute(sql, params)
            rows = cur.fetchall()
        return [MemoryRecord(*row) for row in rows]

    def create_audit_event(
        self, workspace: str, tool: str, action: str, detail: str = ""
    ) -> AuditEvent:
        sql = self._q(
            "INSERT INTO {schema}.tool_audit_events "
            "(workspace, tool, action, detail) VALUES (%s, %s, %s, %s) "
            "RETURNING id, workspace, tool, action, detail, created_at"
        )
        with self._connect() as conn, conn.cursor() as cur:
            cur.execute(sql, (workspace, tool, action, detail))
            row = cur.fetchone()
            conn.commit()
        return AuditEvent(*row)

    def list_audit_events(
        self, workspace: str | None = None, limit: int = 20
    ) -> list[AuditEvent]:
        where = " WHERE workspace = %s" if workspace else ""
        params: list[object] = [workspace] if workspace else []
        params.append(max(1, min(limit, 100)))
        sql = self._q(
            "SELECT id, workspace, tool, action, detail, created_at "
            "FROM {schema}.tool_audit_events" + where +
            " ORDER BY created_at DESC LIMIT %s"
        )
        with self._connect() as conn, conn.cursor() as cur:
            cur.execute(sql, params)
            rows = cur.fetchall()
        return [AuditEvent(*row) for row in rows]
