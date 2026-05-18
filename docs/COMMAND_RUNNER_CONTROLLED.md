# Command Runner Controlled

`command-runner-controlled` is a first-party MCP server for safe local command
execution. It is designed for coding assistants that need the feedback loop:

```text
inspect code -> propose change -> run checks -> inspect failure -> fix -> rerun
```

Command execution is high-impact because it can mutate files, consume network
or compute resources, expose environment data, or publish/deploy code. This
server therefore uses command IDs plus structured args, not arbitrary shell
strings.

## What It Supports

- Allowlisted command IDs.
- Per-command allowed args.
- Workspace-root enforcement.
- Blocked destructive patterns.
- Suspicious shell-operator rejection.
- Timeout enforcement.
- stdout/stderr/exit-code/duration capture.
- Output truncation.
- JSONL audit logs for allowed and denied requests.
- Dry-run validation and preview.

## What It Intentionally Does Not Support

- Unrestricted shell execution.
- Arbitrary command strings from the assistant.
- Shell chaining by default.
- Destructive commands by default.
- Access outside the configured workspace.
- Secret-bearing paths such as `.env`, `.ssh`, `.aws`, or paths containing
  `secret` or `token`.

## Workspace Config

The server reads a YAML config:

```yaml
version: 1
workspace:
  root: "{WORKSPACE_ROOT}"
  require_workspace: true
execution:
  default_timeout_seconds: 120
  max_output_bytes: 200000
  dry_run: false
allowlist:
  commands:
    - id: pytest
      command: "python -m pytest"
      allowed_args:
        - "tests/"
        - "-q"
      description: "Run Python tests"
blocked_patterns:
  - "rm -rf"
  - "sudo"
  - "git reset --hard"
audit:
  enabled: true
  path: ".cris-mcp-toolbelt/audit/command-runner.jsonl"
```

See
[../servers/command-runner-controlled/examples/command-runner.config.yaml](../servers/command-runner-controlled/examples/command-runner.config.yaml)
for a fuller starter config.

## MCP Tools

- `list_allowed_commands`
- `dry_run_command`
- `run_allowed_command`
- `list_audit_events`

`run_allowed_command` takes a command ID and structured args:

```json
{
  "command_id": "pytest",
  "args": ["tests/", "-q"]
}
```

## Audit Logs

Audit records are JSONL. By default they are written under:

```text
{WORKSPACE_ROOT}/.cris-mcp-toolbelt/audit/command-runner.jsonl
```

Denied commands are audited too, including the rejection reason.
