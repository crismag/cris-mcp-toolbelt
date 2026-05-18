# Use With A Local Ollama Coding Assistant

This workflow builds a usable local coding assistant stack: Continue or VSCode
as the client, Ollama as the local model runtime, and MCP servers from this
toolbelt for code context plus safe validation.

## Goal

Give the assistant the core coding loop:

```text
inspect code -> propose edit -> run checks -> inspect failure -> fix -> rerun
```

The key MCP server for the feedback loop is
`command-runner-controlled`. The PostgreSQL memory server remains second: it is
valuable for audit records, project memory, model usage records, workspace
registry data, and tool usage history, but command execution makes the coding
assistant immediately more useful.

## 1. Render The Local Development Stack

Generate a Continue config for code context and gated local development tools:

```bash
python3 scripts/render_config.py \
  --profile local-dev \
  --client continue \
  --output {TARGET_REPOSITORY}/{MCP_CONFIG_DIR}/cris-mcp-toolbelt.yaml
```

This gives the assistant workspace files, git context, public docs, browser/UI
testing, local memory, database inspection, and planning tools according to the
catalog and profile.

## 2. Render The Executor Stack

Generate the executor config when you want the assistant to run allowlisted
checks:

```bash
python3 scripts/render_config.py \
  --profile executor \
  --client continue \
  --output {TARGET_REPOSITORY}/{MCP_CONFIG_DIR}/cris-mcp-toolbelt.executor.yaml
```

The rendered executor config starts `command-runner-controlled` with the
workspace command policy at
`{WORKSPACE_ROOT}/.cris-mcp-toolbelt/command-runner.config.yaml`.

## 3. Add A Workspace Command Policy

Create the workspace-local command-runner config:

```bash
mkdir -p {WORKSPACE_ROOT}/.cris-mcp-toolbelt
cp servers/command-runner-controlled/examples/command-runner.config.yaml \
  {WORKSPACE_ROOT}/.cris-mcp-toolbelt/command-runner.config.yaml
```

Edit the `allowlist.commands` section for the project's real checks, for
example:

```yaml
allowlist:
  commands:
    - id: pytest
      command: "python -m pytest"
      allowed_args: ["tests/", "-q"]
      description: "Run Python tests"
```

The server refuses commands outside the allowlist, blocked destructive
patterns, and working directories outside the workspace.

## 4. Audit File

By default, command events are recorded at:

```text
{WORKSPACE_ROOT}/.cris-mcp-toolbelt/audit/command-runner.jsonl
```

The audit log records dry-runs, real executions, and blocked attempts.

## 5. Suggested Assistant Behavior

Ask the assistant to:

- inspect relevant files and git status;
- propose edits;
- call `dry_run_command` before running unfamiliar checks;
- call `run_allowed_command` only for allowlisted command IDs after
  confirmation;
- inspect failures and propose the next patch.

## See Also

- [LOCAL_OLLAMA_MCP_STACK.md](LOCAL_OLLAMA_MCP_STACK.md)
- [OLLAMA_LOCAL_AI_SETUP.md](OLLAMA_LOCAL_AI_SETUP.md)
- [WORKSPACE_ENABLEMENT.md](WORKSPACE_ENABLEMENT.md)
- [../examples/rendered/local-dev.continue.yaml](../examples/rendered/local-dev.continue.yaml)
- [../examples/rendered/executor.continue.yaml](../examples/rendered/executor.continue.yaml)
