# Contributing

Thanks for helping grow this community MCP toolbelt.

## Contribution principles

- Keep everything public-safe and reusable.
- Use generic examples only.
- Do not include private project names, internal systems, or secrets.
- Prefer read-only defaults and explicit safety controls.

## Required for MCP catalog additions

Every new `catalog/*.yaml` entry must include:

- Unique `id`
- `name` and short `description`
- `category`
- `trust_level`
- `default_access` (read-only unless clearly justified)
- Security notes (threats, mitigations, and profile gating)
- Provider/source metadata

## Security review expectations

Contributors must:

- Explain data exposure risks.
- Confirm path restrictions for local file access.
- Confirm read-only database defaults.
- Gate write actions behind explicit write-enabled profiles.
- Route unknown MCPs to sandbox profile only.

## Development checks

```bash
bash scripts/doctor.sh
bash scripts/test_mcp_servers.sh
python3 scripts/validate_catalog.py
```

## Pull requests

- Keep changes focused and documented.
- Update relevant docs when behavior/policy changes.
- Add or update catalog metadata and security notes for new MCP servers.
