"""MCP server entry point for toolbelt-postgres-memory.

Exposes four tools over the Model Context Protocol:
  - create_memory_record
  - search_memory_records
  - create_audit_event
  - list_audit_events

All four operate on a toolbelt-owned PostgreSQL schema. Memory writes are
guarded against secret-like content. Configuration comes from the environment;
see config.py.

Requires: mcp, psycopg.
"""

from __future__ import annotations

import sys

from mcp.server.fastmcp import FastMCP

from .config import ConfigError, load_config
from .db import Database
from .tools import audit, memory

app = FastMCP("toolbelt-postgres-memory")

_db: Database | None = None


def database() -> Database:
    """Return the process-wide Database, building it on first use."""
    global _db
    if _db is None:
        _db = Database(load_config())
    return _db


@app.tool()
def create_memory_record(workspace: str, kind: str, content: str) -> dict:
    """Store a project memory record (a fact, decision, or convention).

    Records whose kind or content looks like a secret, credential, private
    key, or access token are refused.
    """
    return memory.create_memory_record(database(), workspace, kind, content)


@app.tool()
def search_memory_records(
    workspace: str = "", query: str = "", kind: str = "", limit: int = 20
) -> list[dict]:
    """Search stored memory records, most recent first.

    Any of workspace, query, or kind may be left empty to widen the search.
    """
    return memory.search_memory_records(
        database(), workspace=workspace, query=query, kind=kind, limit=limit
    )


@app.tool()
def create_audit_event(
    workspace: str, tool: str, action: str, detail: str = ""
) -> dict:
    """Record an audit event for a tool activation or high-impact action."""
    return audit.create_audit_event(database(), workspace, tool, action, detail)


@app.tool()
def list_audit_events(workspace: str = "", limit: int = 20) -> list[dict]:
    """List recorded audit events, most recent first."""
    return audit.list_audit_events(database(), workspace=workspace, limit=limit)


def main() -> int:
    """Initialize the schema, then run the MCP server over stdio."""
    try:
        database().init_schema()
    except ConfigError as exc:
        print(f"configuration error: {exc}", file=sys.stderr)
        return 2
    except Exception as exc:  # noqa: BLE001 - surface any startup failure clearly
        print(f"failed to initialize the toolbelt schema: {exc}", file=sys.stderr)
        return 1

    app.run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
