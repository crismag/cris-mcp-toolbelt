# Architecture

The toolbelt is split into five layers:

1. **Documentation layer** (`docs/`): policies, setup, governance, and security model.
2. **Configuration layer** (`configs/continue/`, `profiles/`): reusable templates and explicit access profiles.
3. **Catalog layer** (`catalog/`): MCP server metadata, trust model, and security notes.
4. **Workspace enablement layer** (`scripts/enable_for_workspace.sh`): safe, repeatable project wiring.
5. **Validation layer** (`scripts/doctor.sh`, `scripts/test_mcp_servers.sh`,
   `scripts/validate_catalog.py`): sanity and policy checks.

Default posture: least privilege, read-only, explicit opt-in for writes.
