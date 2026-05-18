# Contributing

Thanks for helping grow this community MCP toolbelt.

This file is a quick summary. The full, authoritative contributor reference is
[docs/CONTRIBUTOR_GUIDANCE.md](docs/CONTRIBUTOR_GUIDANCE.md). Before contributing,
also read [docs/CONTEXT.md](docs/CONTEXT.md) and
[docs/REPOSITORY_PRINCIPLES.md](docs/REPOSITORY_PRINCIPLES.md).

## Contribution principles

- Keep everything public-safe and reusable.
- Use generic examples and placeholders only — no private project names,
  internal systems, private paths, or secrets.
- Use controlled-capability language: capabilities are configurable, classified,
  scoped, and activated — not "dangerous" or "crippled".
- Prefer conservative defaults: read-only and inspect first, explicit activation
  for high-impact capability.
- Keep pull requests small and focused.

## Adding an MCP catalog entry

Catalog entries live under `catalog/servers/`. An MCP server is added to the
catalog only when it is **complete and functional for deployment**.

Every entry must declare the full metadata set — including `capability_class`,
`controlled_capabilities`, `default_access`, `allowed_profiles`,
`activation_policy`, `scope_controls`, `trust_level`, `review_status`, and
`security_notes`. The complete field list and requirements are in
[docs/CONTRIBUTOR_GUIDANCE.md](docs/CONTRIBUTOR_GUIDANCE.md).

New entries start at `trust_level: unknown` or `experimental` and
`review_status: proposed`.

## Adding or updating profiles

The seven profiles are `readonly-research`, `local-inspect`, `local-dev`,
`sandbox`, `writer`, `executor`, and `admin-controlled`. Profile changes affect
safety posture and require an explicit security rationale in the pull request.

## Security review expectations

Any change to catalog entries, profiles, capability metadata, activation policy,
scope controls, or trust levels must include a security rationale. Also:

- Follow [docs/ONLINE_MCP_POLICY.md](docs/ONLINE_MCP_POLICY.md) for online MCP
  usage and catalog additions.
- Explain data exposure risks.
- Confirm path restrictions for local file access.
- Confirm read-only database defaults.
- Gate modifying, executing, and administrative capability behind the
  appropriate profiles.
- Route unknown MCP servers to the `sandbox` profile only.

## Development checks

```bash
bash scripts/doctor.sh
bash scripts/test_mcp_servers.sh
python3 scripts/validate_catalog.py
python3 scripts/validate_profiles.py
python3 scripts/policy_lint.py
python3 -m pytest tests/ -q
```

## Pull requests

- Keep changes focused and documented.
- Update relevant docs when behavior or policy changes.
- Add or update catalog metadata and security notes for new MCP servers.
- Include a security rationale for any capability or trust change.

See [docs/CONTRIBUTOR_GUIDANCE.md](docs/CONTRIBUTOR_GUIDANCE.md) for the full
pull request checklist and examples of good and rejected contributions.
