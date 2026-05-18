"""Executor tests."""

from __future__ import annotations

import sys

from command_runner_controlled.executor import (
    dry_run_command,
    list_audit_events,
    run_allowed_command,
)
from command_runner_controlled.models import AuditConfig, CommandSpec, Config, ExecutionConfig


def _config(tmp_path, *, dry_run=False, max_output_bytes=200_000, timeout=5):
    return Config(
        workspace_root=tmp_path.resolve(),
        require_workspace=True,
        execution=ExecutionConfig(
            default_timeout_seconds=timeout,
            max_output_bytes=max_output_bytes,
            dry_run=dry_run,
        ),
        allowlist={
            "version": CommandSpec(
                "version", sys.executable, ("--version",), "Print Python version"
            ),
            "slow": CommandSpec(
                "slow",
                sys.executable,
                ("-c", "import time; time.sleep(2)"),
                "Sleep",
            ),
            "large": CommandSpec(
                "large",
                sys.executable,
                ("-c", "print('x' * 1000)"),
                "Large output",
            ),
        },
        blocked_patterns=("rm -rf",),
        audit=AuditConfig(True, tmp_path / "audit.jsonl"),
    )


def test_dry_run_does_not_execute(tmp_path):
    result = dry_run_command(_config(tmp_path), "version", ["--version"])

    assert result["ok"] is True
    assert result["allowed"] is True
    assert "would_run" in result


def test_run_allowed_command_executes_and_audits(tmp_path):
    config = _config(tmp_path)
    result = run_allowed_command(config, "version", ["--version"])

    assert result["ok"] is True
    assert result["exit_code"] == 0
    assert "Python" in result["stdout"]
    events = list_audit_events(config)
    assert events[0]["event_type"] == "command_requested"
    assert events[0]["allowed"] is True


def test_denied_command_writes_audit(tmp_path):
    config = _config(tmp_path)
    result = run_allowed_command(config, "missing", [])

    assert result["ok"] is False
    events = list_audit_events(config)
    assert events[0]["event_type"] == "command_denied"
    assert events[0]["allowed"] is False


def test_configured_dry_run_prevents_execution(tmp_path):
    result = run_allowed_command(_config(tmp_path, dry_run=True), "version", ["--version"])

    assert result["ok"] is True
    assert result["dry_run"] is True
    assert "would_run" in result


def test_timeout_behavior(tmp_path):
    result = run_allowed_command(
        _config(tmp_path, timeout=1),
        "slow",
        ["-c", "import time; time.sleep(2)"],
    )

    assert result["ok"] is False
    assert result["timed_out"] is True


def test_output_truncation_behavior(tmp_path):
    result = run_allowed_command(
        _config(tmp_path, max_output_bytes=20),
        "large",
        ["-c", "print('x' * 1000)"],
    )

    assert result["truncated"] is True
    assert len(result["stdout"].encode("utf-8")) <= 20
