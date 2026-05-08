# cris-mcp-toolbelt

A generic, reusable, community-expandable MCP toolbelt for AI-assisted development.

This repository is designed for public use and includes:

- Curated MCP tool categories
- Reusable configuration templates for public MCP servers
- A place for custom MCP tools and helper scripts
- A safe workspace enablement layer for any repository
- A companion toolbelt for local AI workflows using Ollama (or similar runtimes)
- Governance, contribution standards, catalog metadata, and security review expectations

## Safety-first defaults

- Public-repository friendly, generic examples only
- No hardcoded secrets
- Read-only by default
- Online MCPs limited to trusted providers or inward/retrieval-only defaults
- Filesystem access path-restricted
- Database access read-only by default
- Write actions require an explicit write-enabled profile
- Unknown MCP servers allowed only in sandbox profile

## Quick start

```bash
cp .env.example .env
{TOOLBELT_HOME}/scripts/enable_for_workspace.sh {TARGET_WORKSPACE} readonly-research
{TOOLBELT_HOME}/scripts/doctor.sh
{TOOLBELT_HOME}/scripts/test_mcp_servers.sh
python3 {TOOLBELT_HOME}/scripts/validate_catalog.py
```

Example placeholder paths:

- `{WORKSPACE_ROOT}/cris-mcp-toolbelt`
- `{TARGET_WORKSPACE}/.continue/mcpServers/cris-mcp-toolbelt.yaml`
- `{TOOLBELT_HOME}/scripts/enable_for_workspace.sh {TARGET_WORKSPACE} readonly-research`

## Repository layout

- `docs/` architecture, setup, security, policy, governance, roadmap
- `configs/continue/` reusable Continue MCP templates
- `profiles/` safety profiles (read-only, sandbox, write-enabled)
- `catalog/` MCP catalog entries with metadata and security notes
- `scripts/` safe helper scripts
- `examples/` usage examples
- `tools/` custom tool guidance

## License

MIT. See `LICENSE`.
