"""Command policy validation."""

from __future__ import annotations

import shlex
from pathlib import Path

from .models import CommandPlan, Config

SUSPICIOUS_OPERATORS = ("&&", "||", ";", "`", "$(", ">", ">>", "<", "|")
BLOCKED_PATH_MARKERS = (".env", ".ssh", ".aws", "secret", "token")


class PolicyError(ValueError):
    """Raised when a command request violates policy."""


def _contains(value: str, patterns: tuple[str, ...]) -> str:
    normalized = " ".join(value.split()).lower()
    for pattern in patterns:
        if pattern.lower() in normalized:
            return pattern
    return ""


def _path_escape_or_blocked(arg: str, workspace_root: Path) -> str:
    lowered = arg.lower()
    for marker in BLOCKED_PATH_MARKERS:
        if marker in lowered:
            return f"blocked path marker: {marker}"

    if "/" not in arg and "\\" not in arg and not arg.startswith("."):
        return ""
    candidate = Path(arg).expanduser()
    if not candidate.is_absolute():
        candidate = workspace_root / candidate
    resolved = candidate.resolve()
    try:
        resolved.relative_to(workspace_root)
    except ValueError:
        return "path escapes workspace"
    return ""


def validate_request(
    config: Config,
    command_id: str,
    args: list[str] | tuple[str, ...] | None = None,
    timeout_seconds: int | None = None,
) -> CommandPlan:
    """Validate command id, args, timeout, blocked patterns, and workspace scope."""
    command_id = command_id.strip()
    if command_id not in config.allowlist:
        raise PolicyError(f"unknown command_id: {command_id}")

    spec = config.allowlist[command_id]
    requested_args = tuple(str(arg) for arg in (args or []))
    timeout = timeout_seconds or config.execution.default_timeout_seconds
    if timeout < 1 or timeout > config.execution.default_timeout_seconds:
        raise PolicyError("timeout exceeds configured limit")

    command_text = " ".join((spec.command, *requested_args))
    blocked = _contains(command_text, config.blocked_patterns)
    if blocked:
        raise PolicyError(f"blocked pattern: {blocked}")

    allowed_args = set(spec.allowed_args)
    for arg in requested_args:
        path_issue = _path_escape_or_blocked(arg, config.workspace_root)
        if path_issue:
            raise PolicyError(path_issue)
        if arg not in allowed_args:
            operator = _contains(arg, SUSPICIOUS_OPERATORS)
            if operator:
                raise PolicyError(f"suspicious shell operator: {operator}")
            raise PolicyError(f"arg not allowed for {command_id}: {arg}")

    argv = tuple(shlex.split(spec.command)) + requested_args
    return CommandPlan(
        command_id=command_id,
        command=" ".join(shlex.quote(part) for part in argv),
        argv=argv,
        cwd=config.workspace_root,
        timeout_seconds=timeout,
    )
