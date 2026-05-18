"""Audit tests."""

from __future__ import annotations

from command_runner_controlled.audit import list_events, record_event


def test_audit_log_is_jsonl_and_recent_first(tmp_path):
    audit_log = tmp_path / "audit.jsonl"
    record_event(audit_log, {"event_type": "one"})
    record_event(audit_log, {"event_type": "two"})

    events = list_events(audit_log)

    assert [event["event_type"] for event in events] == ["two", "one"]
    assert "created_at" in events[0]
