# Profile selection

Pick the most conservative profile that still does the job. See
[../profiles/README.md](../profiles/README.md) for full details.

- `readonly-research`: safest baseline — public docs and read-only research
- `local-inspect`: read-only inspection of a local workspace, no network
- `local-dev`: controlled local development with profile-gated writes
- `sandbox`: experimentation with unknown or unreviewed MCP servers
- `writer`: explicit file, database, or repository mutation
- `executor`: controlled command execution with allowlists
- `admin-controlled`: high-impact operations, explicitly configured
