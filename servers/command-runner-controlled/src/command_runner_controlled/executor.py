"""Execution layer for command-runner-controlled."""

from __future__ import annotations

import os
import subprocess
import time
from typing import Any

from .audit import list_events, record_event
from .models import CommandPlan, Config
from .policy import PolicyError, validate_request

ALLOWED_ENV_KEYS = ("PATH", "HOME", "LANG", "LC_ALL", "TERM", "CI")


def _filtered_env() -> dict[str, str]:
    return {key: value for key in ALLOWED_ENV_KEYS if (value := os.environ.get(key))}


def _truncate_output(value: str, max_bytes: int) -> tuple[str, bool]:
    encoded = value.encode("utf-8")
    if len(encoded) <= max_bytes:
        return value, False
    return encoded[:max_bytes].decode("utf-8", errors="replace"), True


def _audit(config: Config, event: dict[str, Any]) -> dict[str, Any] | None:
    if not config.audit.enabled:
        return None
    return record_event(config.audit.path, event)


def list_allowed_commands(config: Config) -> dict[str, Any]:
    """Return public command policy metadata."""
    return {
        "workspace": str(config.workspace_root),
        "commands": [
            {
                "id": spec.id,
                "command": spec.command,
                "allowed_args": list(spec.allowed_args),
                "description": spec.description,
            }
            for spec in config.allowlist.values()
        ],
        "blocked_patterns": list(config.blocked_patterns),
        "default_timeout_seconds": config.execution.default_timeout_seconds,
        "max_output_bytes": config.execution.max_output_bytes,
        "dry_run": config.execution.dry_run,
        "audit_path": str(config.audit.path),
    }


def dry_run_command(
    config: Config, command_id: str, args: list[str] | None = None
) -> dict[str, Any]:
    """Validate and preview a command without executing it."""
    try:
        plan = validate_request(config, command_id, args=args)
    except PolicyError as exc:
        _audit(
            config,
            {
                "event_type": "command_denied",
                "workspace": str(config.workspace_root),
                "command_id": command_id,
                "command": command_id,
                "allowed": False,
                "reason": str(exc),
            },
        )
        return {"ok": False, "allowed": False, "reason": str(exc)}

    _audit_request(config, plan, allowed=True, reason="matched allowlist")
    return {"ok": True, "would_run": plan.command, "allowed": True}


def _audit_request(
    config: Config,
    plan: CommandPlan,
    allowed: bool,
    reason: str,
    exit_code: int | None = None,
    duration_ms: int | None = None,
) -> dict[str, Any] | None:
    event: dict[str, Any] = {
        "event_type": "command_requested" if allowed else "command_denied",
        "workspace": str(config.workspace_root),
        "command_id": plan.command_id,
        "command": plan.command,
        "allowed": allowed,
        "reason": reason,
    }
    if exit_code is not None:
        event["exit_code"] = exit_code
    if duration_ms is not None:
        event["duration_ms"] = duration_ms
    return _audit(config, event)


def run_allowed_command(
    config: Config,
    command_id: str,
    args: list[str] | None = None,
    timeout_seconds: int | None = None,
) -> dict[str, Any]:
    """Validate, audit, and execute an allowlisted command."""
    try:
        plan = validate_request(
            config, command_id, args=args, timeout_seconds=timeout_seconds
        )
    except PolicyError as exc:
        _audit(
            config,
            {
                "event_type": "command_denied",
                "workspace": str(config.workspace_root),
                "command_id": command_id,
                "command": command_id,
                "allowed": False,
                "reason": str(exc),
            },
        )
        return {"ok": False, "allowed": False, "reason": str(exc)}

    if config.execution.dry_run:
        event = _audit_request(config, plan, allowed=True, reason="dry run")
        return {
            "ok": True,
            "allowed": True,
            "dry_run": True,
            "would_run": plan.command,
            "audit_event": event,
        }

    started = time.monotonic()
    try:
        completed = subprocess.run(
            list(plan.argv),
            cwd=plan.cwd,
            env=_filtered_env(),
            capture_output=True,
            text=True,
            timeout=plan.timeout_seconds,
            shell=False,
            check=False,
        )
        duration_ms = int((time.monotonic() - started) * 1000)
        stdout, stdout_truncated = _truncate_output(
            completed.stdout, config.execution.max_output_bytes
        )
        stderr, stderr_truncated = _truncate_output(
            completed.stderr, config.execution.max_output_bytes
        )
        event = _audit_request(
            config,
            plan,
            allowed=True,
            reason="matched allowlist",
            exit_code=completed.returncode,
            duration_ms=duration_ms,
        )
        return {
            "ok": completed.returncode == 0,
            "command_id": plan.command_id,
            "command": plan.command,
            "exit_code": completed.returncode,
            "stdout": stdout,
            "stderr": stderr,
            "duration_ms": duration_ms,
            "truncated": stdout_truncated or stderr_truncated,
            "audit_event": event,
        }
    except subprocess.TimeoutExpired as exc:
        duration_ms = int((time.monotonic() - started) * 1000)
        stdout = exc.stdout or ""
        stderr = exc.stderr or ""
        if isinstance(stdout, bytes):
            stdout = stdout.decode("utf-8", errors="replace")
        if isinstance(stderr, bytes):
            stderr = stderr.decode("utf-8", errors="replace")
        stdout, stdout_truncated = _truncate_output(
            stdout, config.execution.max_output_bytes
        )
        stderr, stderr_truncated = _truncate_output(
            stderr, config.execution.max_output_bytes
        )
        event = _audit_request(
            config,
            plan,
            allowed=True,
            reason="timeout",
            duration_ms=duration_ms,
        )
        return {
            "ok": False,
            "command_id": plan.command_id,
            "command": plan.command,
            "exit_code": None,
            "stdout": stdout,
            "stderr": stderr,
            "duration_ms": duration_ms,
            "timed_out": True,
            "truncated": stdout_truncated or stderr_truncated,
            "audit_event": event,
        }


def list_audit_events(config: Config, limit: int = 20) -> list[dict[str, Any]]:
    """List recent command audit events."""
    return list_events(config.audit.path, limit=limit)
