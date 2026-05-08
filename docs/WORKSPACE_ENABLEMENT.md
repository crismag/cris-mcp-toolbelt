# Workspace Enablement

The enablement script creates/updates MCP config for a target workspace using a selected safety profile.

Command:

```bash
{TOOLBELT_HOME}/scripts/enable_for_workspace.sh {TARGET_WORKSPACE} readonly-research
```

Output file:

`{TARGET_WORKSPACE}/.continue/mcpServers/cris-mcp-toolbelt.yaml`

Safety guarantees:

- Rejects unsafe/unknown profiles
- Uses path-restricted local access
- Defaults to read-only profile
