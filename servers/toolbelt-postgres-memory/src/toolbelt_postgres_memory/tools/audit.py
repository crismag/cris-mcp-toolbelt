"""Audit-event tools: create and list.

These functions take a database-like object (anything exposing
create_audit_event / list_audit_events, such as db.Database) so they can be
unit-tested with a fake.
"""

from __future__ import annotations

from typing import Any


def _event_to_dict(event: Any) -> dict[str, Any]:
    return {
        "id": event.id,
        "workspace": event.workspace,
        "tool": event.tool,
        "action": event.action,
        "detail": event.detail,
        "created_at": event.created_at.isoformat(),
    }


def create_audit_event(
    db: Any, workspace: str, tool: str, action: str, detail: str = ""
) -> dict[str, Any]:
    """Record an audit event for a tool activation or high-impact action."""
    workspace = workspace.strip()
    tool = tool.strip()
    action = action.strip()
    if not workspace:
        raise ValueError("workspace must not be empty")
    if not tool:
        raise ValueError("tool must not be empty")
    if not action:
        raise ValueError("action must not be empty")

    event = db.create_audit_event(workspace, tool, action, detail)
    return _event_to_dict(event)


def list_audit_events(
    db: Any, workspace: str | None = None, limit: int = 20
) -> list[dict[str, Any]]:
    """List audit events, most recent first."""
    events = db.list_audit_events(workspace=workspace or None, limit=limit)
    return [_event_to_dict(e) for e in events]
