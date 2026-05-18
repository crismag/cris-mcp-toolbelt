"""Config rendering tests."""

from __future__ import annotations

import json
from pathlib import Path

import yaml

from conftest import run

ROOT = Path.cwd()


def _rendered_payload(stdout: str) -> str:
    marker = "--- rendered config ---"
    assert marker in stdout, stdout
    payload = stdout.split(marker, 1)[1]
    payload = payload.split("--- dry run: no file written ---", 1)[0]
    return "\n".join(
        line for line in payload.splitlines() if not line.startswith("#")
    ).strip()


def test_continue_render_emits_runtime_server_blocks():
    result = run(
        "scripts/render_config.py",
        "--profile",
        "local-inspect",
        "--client",
        "continue",
        "--servers",
        "filesystem-controlled,sequential-thinking",
        "--workspace-root",
        str(ROOT),
        "--dry-run",
    )
    assert result.returncode == 0, result.stdout + result.stderr

    config = yaml.safe_load(_rendered_payload(result.stdout))
    servers = config["mcpServers"]
    assert servers["filesystem-controlled"]["command"] == "npx"
    assert servers["filesystem-controlled"]["args"][-1] == str(ROOT)
    assert servers["sequential-thinking"]["args"] == [
        "-y",
        "@modelcontextprotocol/server-sequential-thinking",
    ]


def test_claude_render_emits_json_mcp_servers():
    result = run(
        "scripts/render_config.py",
        "--profile",
        "readonly-research",
        "--client",
        "claude-desktop",
        "--servers",
        "public-fetch",
        "--dry-run",
    )
    assert result.returncode == 0, result.stdout + result.stderr

    config = json.loads(_rendered_payload(result.stdout))
    assert list(config) == ["mcpServers"]
    assert config["mcpServers"]["public-fetch"] == {
        "command": "uvx",
        "args": ["mcp-server-fetch"],
    }


def test_generic_json_includes_toolbelt_metadata():
    result = run(
        "scripts/render_config.py",
        "--profile",
        "local-dev",
        "--client",
        "generic-json",
        "--servers",
        "memory-local",
        "--dry-run",
    )
    assert result.returncode == 0, result.stdout + result.stderr

    config = json.loads(_rendered_payload(result.stdout))
    assert config["client"] == "generic-json"
    assert config["profile"] == "local-dev"
    assert config["mcpServers"][0]["ref"] == "memory-local"
    assert config["mcpServers"][0]["mode"] == "enabled"


def test_executor_renders_command_runner():
    result = run(
        "scripts/render_config.py",
        "--profile",
        "executor",
        "--servers",
        "command-runner-controlled",
        "--client",
        "continue",
        "--workspace-root",
        str(ROOT),
        "--dry-run",
    )
    assert result.returncode == 0, result.stdout + result.stderr

    config = yaml.safe_load(_rendered_payload(result.stdout))
    server = config["mcpServers"]["command-runner-controlled"]
    assert server["command"] == "python"
    assert server["args"][:3] == ["-m", "command_runner_controlled.server", "--config"]
