# Workspace Enablement

The enablement script creates/updates MCP config for a target workspace using a selected safety profile.

Command:

```bash
{PROJECT_ROOT}/scripts/enable_for_workspace.sh {TARGET_REPOSITORY} readonly-research
```

Output file:

`{TARGET_REPOSITORY}/{MCP_CONFIG_DIR}/cris-mcp-toolbelt.yaml`

Safety guarantees:

- Rejects unsafe/unknown profiles
- Uses path-restricted local access
- Defaults to read-only profile
