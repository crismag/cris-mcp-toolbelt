"""Server import smoke tests."""

from __future__ import annotations

import command_runner_controlled.server as server


def test_server_exposes_expected_tools():
    assert callable(server.list_allowed_commands)
    assert callable(server.run_allowed_command)
    assert callable(server.dry_run_command)
    assert callable(server.list_audit_events)
