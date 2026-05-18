# MCP Server Catalog

Catalog entries live under `catalog/servers/` — one YAML file per MCP server —
and should be community-reviewable.

The authoritative format and field list are defined in:

- [`catalog/schema.json`](../catalog/schema.json) — JSON Schema for an entry
- [`catalog/README.md`](../catalog/README.md) — catalog layout and field guide

Each entry declares standardized capability, activation, and scope metadata,
including `id`, `name`, `description`, `category`, `provider`, `source_url`,
`license`, `capability_class`, `controlled_capabilities`, `default_access`,
`allowed_profiles`, `activation_policy`, `scope_controls`, `trust_level`,
`review_status`, and `security_notes`.

## Rules

- Conservative defaults: read-only and inspect first.
- Modifying, executing, and administrative capability is activated through a
  profile, never enabled by default.
- Unknown or unreviewed servers are allowed only in the `sandbox` profile.
- New entries start at `trust_level: unknown` or `experimental` and
  `review_status: proposed`.
- An MCP server is published in the catalog only when it is complete and
  functional for deployment.

## Validation

```bash
python3 scripts/validate_catalog.py
```
