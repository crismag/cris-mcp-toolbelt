# MCP Server Catalog

Catalog entries live in `catalog/*.yaml` and should be community-reviewable.

Minimum metadata:

- `id`, `name`, `description`, `category`
- `provider`, `source_url`
- `trust_level`, `default_access`, `profile_allowlist`
- `security_notes`

Rules:

- Read-only by default.
- Write access only in explicit write-enabled profiles.
- Unknown servers allowed only in sandbox profile.
