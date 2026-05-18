# command-runner-controlled

An allowlisted command execution MCP server for `cris-mcp-toolbelt`.

It gives coding agents a controlled feedback loop for local development:
tests, linters, type checks, build checks, repository status, and validation
scripts.

## Status

Catalog entry: `command-runner-controlled` — currently `proposed` / `unknown`.
This server is implemented with unit tests, but it should be promoted only
after it is installed and verified through a real MCP client.

## Tools

| Tool | Purpose |
| --- | --- |
| `list_allowed_commands` | Show workspace, allowlisted command IDs, blocked patterns, limits, and audit path |
| `dry_run_command` | Validate and preview an allowlisted command |
| `run_allowed_command` | Run an allowlisted command by ID with structured args |
| `list_audit_events` | Read recent JSONL audit events |

## Safety Model

- No shell execution. Commands are executed with `subprocess.run(..., shell=False)`.
- The assistant supplies a `command_id` plus structured `args`, not an arbitrary
  command string.
- A workspace root is required.
- Commands must match an allowlisted ID and each requested arg must be listed
  in that command's `allowed_args`.
- Destructive patterns and suspicious shell operators are rejected.
- Path-like args must stay inside the workspace and must not point at common
  secret locations.
- Child processes receive a small filtered environment.
- Every allowed, denied, and dry-run request is audited.

## Configure

Create:

```text
{WORKSPACE_ROOT}/.cris-mcp-toolbelt/command-runner.config.yaml
```

Use the starter config:

```bash
cp servers/command-runner-controlled/examples/command-runner.config.yaml \
  {WORKSPACE_ROOT}/.cris-mcp-toolbelt/command-runner.config.yaml
```

Then replace `{WORKSPACE_ROOT}` with the actual workspace path and edit the
allowlist for the project.

## Install

```bash
cd servers/command-runner-controlled
python3 -m pip install -e ".[dev]"
```

## Run

```bash
python -m command_runner_controlled.server \
  --config {WORKSPACE_ROOT}/.cris-mcp-toolbelt/command-runner.config.yaml
```

Register it with an MCP-capable client using the config rendered by:

```bash
python3 scripts/render_config.py \
  --profile executor \
  --client continue \
  --workspace-root {WORKSPACE_ROOT} \
  --dry-run
```

## Test

```bash
python3 -m pytest tests/ -q
```
