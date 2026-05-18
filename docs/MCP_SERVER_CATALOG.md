# MCP Server Catalog

Catalog entries live under `catalog/servers/` — one YAML file per MCP server —
and should be community-reviewable.

The authoritative format and field list are defined in:

- [`catalog/schema.json`](../catalog/schema.json) — JSON Schema for an entry
- [`catalog/README.md`](../catalog/README.md) — catalog layout and field guide

Each entry declares standardized capability, activation, runtime, and scope
metadata, including `id`, `name`, `description`, `category`, `provider`,
`source_url`, `license`, `runtime`, `capability_class`,
`controlled_capabilities`, `default_access`, `allowed_profiles`,
`activation_policy`, `scope_controls`, `trust_level`, `review_status`, and
`security_notes`.

External MCP sources are cataloged using the same schema. See
[MCP_SOURCE_CATALOG_EXPANSION.md](MCP_SOURCE_CATALOG_EXPANSION.md) for source
verification rules, trust lifecycle, and the difference between reference
entries and project-owned `*-controlled` entries.

## Rules

- Conservative defaults: read-only and inspect first.
- Modifying, executing, and administrative capability is activated through a
  profile, never enabled by default.
- Unknown or unreviewed servers are allowed only in the `sandbox` profile.
- New entries start at `trust_level: unknown` or `experimental` and
  `review_status: proposed`.
- Runtime metadata uses placeholders instead of machine-specific paths,
  connection strings, or tokens.
- External sources may be cataloged as `review_status: proposed` before local
  MCP smoke testing, but they must remain conservative until tested.
- Runtime metadata is included only when the access route is verified; otherwise
  use `runtime: null`.

## Validation

```bash
python3 scripts/validate_catalog.py
```
