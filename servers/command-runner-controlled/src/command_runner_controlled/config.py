"""Configuration loading for command-runner-controlled."""

from __future__ import annotations

import os
import shlex
from pathlib import Path
from typing import Any

import yaml

from .models import AuditConfig, CommandSpec, Config, ExecutionConfig

WORKSPACE_ROOT_VAR = "TOOLBELT_WORKSPACE_ROOT"
CONFIG_PATH_VAR = "TOOLBELT_COMMAND_RUNNER_CONFIG"
DEFAULT_CONFIG_PATH = ".cris-mcp-toolbelt/command-runner.config.yaml"

DEFAULT_BLOCKED_PATTERNS = (
    "rm -rf",
    "sudo",
    "chmod -R",
    "chown -R",
    "git push --force",
    "git reset --hard",
    "npm publish",
    "curl | sh",
    "wget | sh",
)

DEFAULT_COMMANDS = (
    CommandSpec("pytest", "python -m pytest", ("tests/", "-q"), "Run Python tests"),
    CommandSpec(
        "validate-catalog",
        "python scripts/validate_catalog.py",
        (),
        "Validate MCP catalog",
    ),
    CommandSpec(
        "validate-profiles",
        "python scripts/validate_profiles.py",
        (),
        "Validate MCP profiles",
    ),
    CommandSpec(
        "policy-lint",
        "python scripts/policy_lint.py",
        (),
        "Run cross-artifact policy lint",
    ),
)


class ConfigError(RuntimeError):
    """Raised when configuration is missing or invalid."""


def _substitute_workspace(value: str, workspace_root: Path) -> str:
    return value.replace("{WORKSPACE_ROOT}", str(workspace_root))


def _resolve_workspace(raw: dict[str, Any], env: dict[str, str]) -> Path:
    configured = str((raw.get("workspace") or {}).get("root") or "").strip()
    env_value = env.get(WORKSPACE_ROOT_VAR, "").strip()
    if configured and env_value:
        configured = configured.replace("{WORKSPACE_ROOT}", env_value)
    workspace_value = configured or env_value
    if not workspace_value:
        raise ConfigError(
            f"workspace.root or {WORKSPACE_ROOT_VAR} must point at a workspace"
        )
    workspace_root = Path(workspace_value).expanduser().resolve()
    if not workspace_root.exists() or not workspace_root.is_dir():
        raise ConfigError(f"workspace root is not a directory: {workspace_root}")
    return workspace_root


def _load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if data is None:
        return {}
    if not isinstance(data, dict):
        raise ConfigError(f"config must be a mapping: {path}")
    return data


def _command_specs(raw: dict[str, Any]) -> dict[str, CommandSpec]:
    entries = ((raw.get("allowlist") or {}).get("commands") or [])
    if not entries:
        return {spec.id: spec for spec in DEFAULT_COMMANDS}
    if not isinstance(entries, list):
        raise ConfigError("allowlist.commands must be a list")

    specs: dict[str, CommandSpec] = {}
    for item in entries:
        if not isinstance(item, dict):
            raise ConfigError("each allowlist command must be a mapping")
        command_id = str(item.get("id") or "").strip()
        command = str(item.get("command") or "").strip()
        if not command_id:
            raise ConfigError("allowlist command is missing id")
        if not command:
            raise ConfigError(f"allowlist command '{command_id}' is missing command")
        try:
            shlex.split(command)
        except ValueError as exc:
            raise ConfigError(f"invalid command for '{command_id}': {exc}") from exc
        allowed_args = item.get("allowed_args") or []
        if not isinstance(allowed_args, list):
            raise ConfigError(f"allowed_args for '{command_id}' must be a list")
        specs[command_id] = CommandSpec(
            id=command_id,
            command=command,
            allowed_args=tuple(str(arg) for arg in allowed_args),
            description=str(item.get("description") or ""),
        )
    return specs


def _config_path(
    explicit_path: str | None, env: dict[str, str], workspace_root: Path | None = None
) -> Path | None:
    value = explicit_path or env.get(CONFIG_PATH_VAR, "").strip()
    if value:
        return Path(value).expanduser().resolve()
    if workspace_root is not None:
        default = workspace_root / DEFAULT_CONFIG_PATH
        if default.exists():
            return default.resolve()
    return None


def load_config(
    config_path: str | None = None, env: dict[str, str] | None = None
) -> Config:
    """Build a Config from YAML plus environment fallback."""
    env = os.environ if env is None else env

    preliminary_path = _config_path(config_path, env)
    raw = _load_yaml(preliminary_path) if preliminary_path else {}
    workspace_root = _resolve_workspace(raw, env)

    if preliminary_path is None:
        default_path = _config_path(None, env, workspace_root)
        raw = _load_yaml(default_path) if default_path else raw

    workspace = raw.get("workspace") or {}
    execution = raw.get("execution") or {}
    audit = raw.get("audit") or {}

    default_timeout = int(execution.get("default_timeout_seconds", 120))
    max_output_bytes = int(execution.get("max_output_bytes", 200_000))
    if default_timeout < 1:
        raise ConfigError("execution.default_timeout_seconds must be greater than zero")
    if max_output_bytes < 1:
        raise ConfigError("execution.max_output_bytes must be greater than zero")

    audit_path_raw = str(
        audit.get("path") or ".cris-mcp-toolbelt/audit/command-runner.jsonl"
    )
    audit_path = Path(_substitute_workspace(audit_path_raw, workspace_root))
    if not audit_path.is_absolute():
        audit_path = workspace_root / audit_path

    return Config(
        workspace_root=workspace_root,
        require_workspace=bool(workspace.get("require_workspace", True)),
        execution=ExecutionConfig(
            default_timeout_seconds=default_timeout,
            max_output_bytes=max_output_bytes,
            dry_run=bool(execution.get("dry_run", False)),
        ),
        allowlist=_command_specs(raw),
        blocked_patterns=tuple(raw.get("blocked_patterns") or DEFAULT_BLOCKED_PATTERNS),
        audit=AuditConfig(enabled=bool(audit.get("enabled", True)), path=audit_path),
    )
