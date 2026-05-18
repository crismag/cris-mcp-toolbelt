"""Policy validation tests."""

from __future__ import annotations

import pytest

from command_runner_controlled.config import load_config
from command_runner_controlled.policy import PolicyError, validate_request


def _config(tmp_path):
    config_file = tmp_path / ".cris-mcp-toolbelt" / "command-runner.config.yaml"
    config_file.parent.mkdir()
    config_file.write_text(
        f"""
version: 1
workspace:
  root: "{tmp_path}"
  require_workspace: true
execution:
  default_timeout_seconds: 5
  max_output_bytes: 100
  dry_run: false
allowlist:
  commands:
    - id: pytest
      command: "python -m pytest"
      allowed_args: ["tests/", "-q"]
      description: "Run tests"
blocked_patterns:
  - "rm -rf"
  - "sudo"
audit:
  enabled: true
  path: ".cris-mcp-toolbelt/audit/command-runner.jsonl"
""",
        encoding="utf-8",
    )
    return load_config(str(config_file))


def test_allowed_command_passes(tmp_path):
    plan = validate_request(_config(tmp_path), "pytest", ["tests/", "-q"])

    assert plan.command_id == "pytest"
    assert plan.argv == ("python", "-m", "pytest", "tests/", "-q")


def test_unknown_command_is_rejected(tmp_path):
    with pytest.raises(PolicyError, match="unknown command_id"):
        validate_request(_config(tmp_path), "unknown", [])


def test_blocked_pattern_is_rejected(tmp_path):
    with pytest.raises(PolicyError, match="blocked pattern"):
        validate_request(_config(tmp_path), "pytest", ["rm -rf"])


def test_shell_chaining_is_rejected(tmp_path):
    with pytest.raises(PolicyError, match="suspicious shell operator"):
        validate_request(_config(tmp_path), "pytest", ["tests/", "&&"])


def test_workspace_escape_is_rejected(tmp_path):
    with pytest.raises(PolicyError, match="path escapes workspace"):
        validate_request(_config(tmp_path), "pytest", ["../outside"])


def test_blocked_path_marker_is_rejected(tmp_path):
    with pytest.raises(PolicyError, match="blocked path marker"):
        validate_request(_config(tmp_path), "pytest", [".env"])


def test_timeout_above_configured_limit_is_rejected(tmp_path):
    with pytest.raises(PolicyError, match="timeout exceeds"):
        validate_request(_config(tmp_path), "pytest", [], timeout_seconds=99)
