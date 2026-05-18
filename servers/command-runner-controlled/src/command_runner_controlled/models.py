"""Dataclasses used by command-runner-controlled."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class CommandSpec:
    """One allowlisted command policy entry."""

    id: str
    command: str
    allowed_args: tuple[str, ...]
    description: str = ""


@dataclass(frozen=True)
class ExecutionConfig:
    """Execution limits."""

    default_timeout_seconds: int = 120
    max_output_bytes: int = 200_000
    dry_run: bool = False


@dataclass(frozen=True)
class AuditConfig:
    """Audit-log configuration."""

    enabled: bool
    path: Path


@dataclass(frozen=True)
class Config:
    """Resolved server configuration."""

    workspace_root: Path
    require_workspace: bool
    execution: ExecutionConfig
    allowlist: dict[str, CommandSpec]
    blocked_patterns: tuple[str, ...]
    audit: AuditConfig


@dataclass(frozen=True)
class CommandPlan:
    """Validated command execution plan."""

    command_id: str
    command: str
    argv: tuple[str, ...]
    cwd: Path
    timeout_seconds: int
