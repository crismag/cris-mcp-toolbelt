"""MCP server entry point for command-runner-controlled."""

from __future__ import annotations

import sys
import argparse

from mcp.server.fastmcp import FastMCP

from .config import Config, ConfigError, load_config
from . import executor

app = FastMCP("command-runner-controlled")

_config: Config | None = None
_config_path: str | None = None


def config() -> Config:
    """Return process-wide configuration, building it on first use."""
    global _config
    if _config is None:
        _config = load_config(_config_path)
    return _config


@app.tool()
def list_allowed_commands() -> dict:
    """List command allowlist, blocked patterns, workspace, and audit log."""
    return executor.list_allowed_commands(config())


@app.tool()
def dry_run_command(command_id: str, args: list[str] | None = None) -> dict:
    """Validate and preview an allowlisted command without running it."""
    return executor.dry_run_command(config(), command_id, args=args)


@app.tool()
def run_allowed_command(
    command_id: str, args: list[str] | None = None, timeout_seconds: int | None = None
) -> dict:
    """Run an allowlisted command by id with structured args."""
    return executor.run_allowed_command(
        config(),
        command_id,
        args=args,
        timeout_seconds=timeout_seconds,
    )


@app.tool()
def list_audit_events(limit: int = 20) -> list[dict]:
    """List recent command-runner audit events."""
    return executor.list_audit_events(config(), limit=limit)


def main() -> int:
    """Validate configuration, then run the MCP server over stdio."""
    global _config_path
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--config", help="Path to command-runner config YAML.")
    args = parser.parse_args()
    _config_path = args.config

    try:
        config()
    except ConfigError as exc:
        print(f"configuration error: {exc}", file=sys.stderr)
        return 2

    app.run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
