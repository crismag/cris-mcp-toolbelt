# Pull Request

## Summary

<!-- What does this change do, and why? -->

## Type of change

- [ ] Documentation
- [ ] Catalog entry (new or changed)
- [ ] Profile (new or changed)
- [ ] Script or tooling
- [ ] Other

## Capability-control checklist

- [ ] The change is public-safe: no private project names, paths, or secrets.
- [ ] Generic placeholders are used instead of real values.
- [ ] Controlled-capability language is used; no alarmist framing.
- [ ] Conservative defaults are preserved (read-only / inspect first; no
      modifying, executing, or administrative capability enabled by default).
- [ ] Unknown or unreviewed MCP servers are routed to the `sandbox` profile
      only.

## For catalog or profile changes

- [ ] A new MCP server entry describes a complete, deployable server.
- [ ] Catalog entries declare all required fields, including `capability_class`,
      `controlled_capabilities`, `activation_policy`, and `scope_controls`.
- [ ] New catalog entries start at `unknown`/`experimental` trust and
      `proposed` review status.
- [ ] A security rationale is included for any capability or trust change.

## Validation

- [ ] `python3 scripts/validate_catalog.py` passes.
- [ ] `python3 scripts/validate_profiles.py` passes.
- [ ] `python3 scripts/policy_lint.py` passes.
- [ ] `python3 -m pytest tests/ -q` passes.

## Documentation

- [ ] Relevant docs are updated for any policy-impacting change.
