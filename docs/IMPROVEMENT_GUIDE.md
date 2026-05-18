# Repository Improvement Guide

This guide describes the next phases of work for `cris-mcp-toolbelt`. It is
prioritized guidance, not implementation code. Use it together with
[ROADMAP.md](ROADMAP.md) and [REPOSITORY_PRINCIPLES.md](REPOSITORY_PRINCIPLES.md).
A detailed phase breakdown is maintained in the project's internal development
plans.

## Current State Summary

The repository is an early documentation-first skeleton:

- `profiles/` contains read-only, sandbox, and writer profiles only.
- `catalog/` contains example entries as flat files, not under `servers/`.
- `configs/continue/` contains Continue client templates only.
- `scripts/` contains `doctor.sh`, `enable_for_workspace.sh`,
  `test_mcp_servers.sh`, and `validate_catalog.py`.
- `docs/` contains architecture, security, governance, setup, and the seven
  core context documents.
- Catalog validation is dependency-free and uses substring matching.
- There is no continuous integration and no contribution templates.

The structure is sound; the gap is depth, schema rigor, and validation.

## Immediate Issues to Fix

- Long single-line Markdown, YAML, and script content should be normalized to
  readable, consistently wrapped formatting.
- Catalog entries are illustrative examples only and are not yet organized under
  `catalog/servers/` or backed by a schema.
- Catalog validation matches strings rather than parsing structure, so it can
  pass malformed YAML.
- `configs/` covers only one client.
- The profile set is incomplete: four of the seven target profiles are missing
  (`local-inspect`, `executor`, `admin-controlled`, and a documented
  `local-dev`).
- Documentation should consistently use controlled-capability language rather
  than alarmist framing.

## Priority 1: Formatting and Repository Hygiene

- Normalize line length and wrapping across `docs/`, `catalog/`, `profiles/`,
  and `configs/`.
- Ensure every file ends with a single newline and uses consistent indentation.
- Confirm `.gitignore` excludes `.env` and other local-only files.
- Improve `README.md` to state purpose, the configurable-control philosophy,
  safety posture, quick start, and links to `docs/`.
- Add a `catalog/README.md` explaining the catalog layout and schema.
- Replace any alarmist capability framing with controlled-capability language.

## Priority 2: Catalog Schema and Validation

Add a formal `catalog/schema.json` describing required fields, optional fields,
and allowed enum values. Each catalog entry should carry:

```yaml
id:
name:
description:
category:
provider:
homepage:
source_url:
license:
transport:
auth_required:
capabilities:
controlled_capabilities:
capability_class:
default_access:
allowed_profiles:
activation_policy:
scope_controls:
data_exposure:
trust_level:
review_status:
security_notes:
tags:
```

Allowed enum values:

- `capability_class`: `passive`, `interactive`, `modifying`, `executing`,
  `administrative`.
- `default_access`: `disabled`, `readonly`, `inspect`, `enabled`, `sandbox`,
  `write_opt_in`, `executor_opt_in`, `admin_opt_in`.
- `trust_level`: `unknown`, `experimental`, `community`, `trusted`.
- `review_status`: `proposed`, `reviewed`, `approved`, `deprecated`.

Then:

- Move catalog entries into `catalog/servers/` (one file per server).
- Upgrade `validate_catalog.py` from substring matching to real YAML parsing
  and schema validation, with clear per-file error messages, enum validation,
  required-field validation, and profile-reference validation.
- Add `policy_lint.py` to check capability and activation consistency — for
  example, a `modifying` capability that is not gated to a write-capable
  profile, or a high-impact entry with no `scope_controls`.

## Priority 3: Safety Profiles

- Add the missing profiles so all seven exist: `readonly-research`,
  `local-inspect`, `local-dev`, `sandbox`, `writer`, `executor`,
  `admin-controlled`.
- Give every profile a consistent field set so they can be compared and
  validated against a shared shape.
- Document each profile's intent, defaults, and intended use.
- Keep defaults conservative: passive capability may be enabled where low-risk;
  modifying requires `writer` or `admin-controlled`; executing requires
  `executor` or `writer`; administrative is modeled but not enabled by default.

## Priority 4: Scripts and Tooling

- Keep scripts small, dependency-light, and POSIX-friendly where practical.
- Upgrade `validate_catalog.py` and add `policy_lint.py` (see Priority 2).
- Add `render_config.py` to render a client configuration from a profile plus
  selected catalog entries, with dry-run and backup-before-overwrite behavior
  (scheduled later — see roadmap).
- Add database helper script stubs (`init_toolbelt_db.py`,
  `inspect_db_schema.py`, `export_schema_context.py`, `validate_db_profile.py`)
  as the database strategy matures.
- Ensure each script prints a clear usage message and exits non-zero on error.

## Priority 5: Documentation Expansion

- Keep the seven core context documents current:
  [CONTEXT.md](CONTEXT.md), [IMPROVEMENT_GUIDE.md](IMPROVEMENT_GUIDE.md),
  [REPOSITORY_PRINCIPLES.md](REPOSITORY_PRINCIPLES.md),
  [CONTRIBUTOR_GUIDANCE.md](CONTRIBUTOR_GUIDANCE.md),
  [MAINTAINER_GUIDANCE.md](MAINTAINER_GUIDANCE.md),
  [AI_AGENT_GUIDE.md](AI_AGENT_GUIDE.md), and [ROADMAP.md](ROADMAP.md).
- Add database strategy documentation (PostgreSQL as the preferred internal
  memory backend; PostgreSQL, MySQL/MariaDB, and SQLite as controlled
  application-database connectors) and a database security model.
- Add local Ollama workflow documentation and a model routing guide.
- Cross-link related documents instead of duplicating content.

## Priority 6: Examples

- Add example walkthroughs per profile: read-only research, local inspect,
  local development, sandbox, writer, and executor.
- Add a local Ollama development workflow example and controlled database
  inspection examples.
- Each example uses placeholders only, avoids destructive commands, and explains
  what capability is granted and why.

## Priority 7: Tests and CI

- Add a `tests/` directory with catalog validation, profile validation, and
  policy lint tests, plus valid and invalid fixtures.
- Add a CI workflow under `.github/` that runs catalog validation, schema
  checks, policy linting, shell and Python syntax checks, and a private-leakage
  scan on every pull request.
- CI should fail on validation errors so unsafe or malformed entries cannot
  merge.

## Priority 8: Community Contribution Readiness

- Add issue templates (new MCP server, profile request, security review).
- Add a pull request template that includes the capability-control checklist.
- Add a release checklist describing the steps to cut a tagged version.
- Ensure [CONTRIBUTING.md](../CONTRIBUTING.md) points to
  [CONTRIBUTOR_GUIDANCE.md](CONTRIBUTOR_GUIDANCE.md).

## Suggested Implementation Order

1. Priority 1 — formatting, hygiene, and controlled-capability language.
2. Priority 2 — catalog schema, `catalog/servers/`, and validation.
3. Priority 3 — the full set of seven profiles.
4. Priority 7 — CI, so validation runs automatically from here on.
5. Priority 5 — database strategy and local Ollama documentation.
6. Priority 6 — examples per profile.
7. Priority 8 — contribution templates and release checklist.
8. Priority 4 — additional tooling (`render_config.py`, database stubs).

## Acceptance Criteria for v0.1.0

- [ ] Formatting is consistent and content is public-safe across the repository.
- [ ] `README.md` states purpose, configurable-control philosophy, and quick
      start.
- [ ] `catalog/schema.json` exists and describes all fields and enums.
- [ ] Catalog entries live under `catalog/servers/` and validate against schema.
- [ ] Core catalog entries declare `capability_class`,
      `controlled_capabilities`, `activation_policy`, and `scope_controls`.
- [ ] All seven profiles exist with a consistent, validated shape.
- [ ] `validate_catalog.py` performs real YAML and schema validation, and
      `policy_lint.py` checks capability and activation consistency.
- [ ] Database strategy and local Ollama workflow docs exist.
- [ ] CI runs validation on every pull request and fails on errors.
- [ ] Issue templates, a PR template, and a release checklist exist.
- [ ] No private references, secrets, write-by-default behavior, or destructive
      example commands anywhere.

## Deferred Improvements

These are intentionally out of scope for v0.1.0:

- The full configuration renderer (`render_config.py` beyond stubs).
- Real database migrations and production database support.
- A full shell-execution MCP implementation.
- Automatic GitHub mutation and cloud deployment actions.
- Package publishing and administrative operations.
- A community registry workflow and trusted-provider index.
- Advanced local agent orchestration (model router, run audit records).

See [ROADMAP.md](ROADMAP.md) for where each deferred item is scheduled.
