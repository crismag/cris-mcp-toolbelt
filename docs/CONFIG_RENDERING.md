# Config Rendering

`scripts/render_config.py` renders MCP client configuration from a profile and
the catalog.

## Governance Summary Mode

The default generic mode keeps the abstract governance summary:

```bash
python3 scripts/render_config.py --profile readonly-research --dry-run
```

Output shape:

```yaml
version: 1
generated_by: cris-mcp-toolbelt render_config.py
client: generic-yaml
profile: readonly-research
mcpServers:
  - ref: public-fetch
    capability_class: interactive
    mode: readonly
```

## Continue Client Mode

Continue mode renders real MCP server blocks:

```bash
python3 scripts/render_config.py \
  --profile local-dev \
  --client continue \
  --workspace-root /path/to/project \
  --output .continue/mcpServers.yaml
```

Output shape:

```yaml
mcpServers:
  filesystem-controlled:
    command: npx
    args:
      - "-y"
      - "@modelcontextprotocol/server-filesystem"
      - "/path/to/project"
```

Executor profile output includes `command-runner-controlled`:

```yaml
mcpServers:
  command-runner-controlled:
    command: python
    args:
      - "-m"
      - command_runner_controlled.server
      - "--config"
      - "/path/to/project/.cris-mcp-toolbelt/command-runner.config.yaml"
```

## Placeholders

The renderer supports placeholders including `{WORKSPACE_ROOT}`,
`{PROJECT_ROOT}`, `{USER_HOME}`, `{POSTGRES_URL}`, `{MYSQL_URL}`,
`{OLLAMA_BASE_URL}`, and `{GITHUB_TOKEN}`. For real client modes, unresolved
placeholders fail clearly unless `--allow-unresolved-placeholders` is passed.

## Profile Enforcement

The renderer refuses to render a server not listed in the selected profile's
`allowed_profiles`.
