# Roadmap

This roadmap describes the planned evolution of `cris-mcp-toolbelt` from a
documentation-first skeleton into usable, community-ready tooling. It is a
direction, not a guarantee of dates.

The roadmap is organized around the eight development phases. A more detailed
activity breakdown is maintained in the project's internal development plans;
see also [CONTEXT.md](CONTEXT.md) and [IMPROVEMENT_GUIDE.md](IMPROVEMENT_GUIDE.md).

## Release Principle

An MCP server is published in the catalog only when it is complete and
functional for deployment. In-progress work stays out of public releases until
it is done.

## Phase Overview

| Phase | Name | Main outcome |
| --- | --- | --- |
| Phase 0 | Repository Alignment and Hygiene | Clean, readable, public-safe foundation |
| Phase 1 | Catalog Schema and Core MCP Entries | First real MCP catalog with capability metadata |
| Phase 2 | Profiles and Capability Governance | Profile-gated activation model |
| Phase 3 | Local Ollama Development Workflow | Local model and MCP workflow docs and examples |
| Phase 4 | Database Memory and Application DB Access | Database strategy and controlled access |
| Phase 5 | Config Rendering and Workspace Enablement | Generate client configs from profiles |
| Phase 6 | Tests, CI, and Release Readiness | Contribution-ready validation layer |
| Phase 7 | Advanced Local Agent Orchestration | Model routing, audit records, task workflows |

## v0.1.0 — Safety-First Foundation

**Goal.** Turn the skeleton into a consistent, validated, contributable
foundation with conservative defaults. Covers Phases 0–2 in full and the
documentation portions of Phases 3, 4, and 6.

**Scope.**
- Repository cleanup, hygiene, and controlled-capability language.
- README improvement.
- `catalog/schema.json` and catalog entries under `catalog/servers/`.
- Core catalog entries for the target MCP servers.
- The seven profiles.
- Catalog validation and policy linting.
- Database strategy documentation.
- Local Ollama workflow documentation.
- Basic examples.
- CI validation.
- Release checklist.

**Acceptance criteria.**
- All catalog entries validate against the schema and pass policy linting in CI.
- Core entries declare `capability_class`, `controlled_capabilities`,
  `activation_policy`, and `scope_controls`.
- All seven profiles validate and keep conservative defaults.
- CI fails on validation errors.
- Every published catalog entry describes a complete, deployable server.
- No private references, secrets, or capability enabled unsafely by default.
- The seven core context documents are present and current.

**Deferred.** The full configuration renderer, real database migrations, a full
shell-execution MCP, automatic GitHub mutation, production database support,
cloud deployment actions, package publishing, and administrative operations.

## v0.2.0 — Catalog Expansion and Local Ollama Workflow

**Goal.** Broaden the catalog with completed, reviewed MCP servers and make the
local Ollama development workflow practical. Advances Phases 3 and 4.

**Scope.**
- Additional reviewed catalog entries across capability categories.
- Local Ollama MCP stack documentation and a model routing guide.
- Continue-compatible configuration guidance and a local-dev example.
- Database security model and controlled application-database inspection
  examples for PostgreSQL, MySQL/MariaDB, and SQLite.

**Acceptance criteria.**
- Every catalog entry has verifiable provenance, a stated license, and a
  complete, deployable server.
- Trust levels are applied via the lifecycle in
  [MAINTAINER_GUIDANCE.md](MAINTAINER_GUIDANCE.md).
- Application database access defaults to read-only; mutation requires `writer`
  or `admin-controlled`.

**Deferred.** Automated config rendering and capability-drift linting beyond
basic policy lint.

## v0.3.0 — Config Rendering and Workspace Enablement

**Goal.** Generate client configuration from a profile plus selected catalog
entries instead of hand-maintained templates. Delivers Phase 5.

**Scope.**
- `render_config.py` with dry-run mode and backup-before-overwrite behavior.
- A defined config template format and generic plus Continue templates.
- An improved `enable_for_workspace.sh` with profile and capability-mode
  selection and a clear activation summary.

**Acceptance criteria.**
- Rendered configs never grant capability beyond the referenced profile.
- Rendering is reproducible, supports dry-run, fails safely, and is validated in
  CI.

**Deferred.** Advanced orchestration and audit tooling.

## v0.4.0 — Database Memory and Helper Tooling

**Goal.** Add database-backed memory and reviewed helper tooling. Completes
Phase 4 tooling.

**Scope.**
- PostgreSQL documented as the preferred internal memory backend, with a
  database initialization script.
- Database helper scripts (`inspect_db_schema.py`, `export_schema_context.py`,
  `validate_db_profile.py`).
- A small set of documented, optional helper tools under `tools/`.

**Acceptance criteria.**
- Database-backed memory is opt-in; file-based memory remains the zero-dependency
  default.
- Helper tools default to safe behavior and are profile-aware.
- No credentials are committed; production access is not enabled by default.

**Deferred.** Advanced local agent orchestration.

## v0.5.0 — Advanced Local Agent Orchestration

**Goal.** Prepare higher-level local AI orchestration using models, memory,
MCPs, and audit records. Delivers Phase 7.

**Scope.**
- A model router helper and model role assignments.
- Activity and run audit records.
- Task profile, project memory, and validation command examples.
- Repo review and implementation planning workflow examples.

**Acceptance criteria.**
- Local models have clear role assignments.
- Tool usage is profile-gated and high-impact actions are auditable.
- No unrestricted automation is enabled.

**Deferred.** A community registry workflow.

## Future Ideas

These are not yet scheduled and may change or be dropped:

- A community-maintained catalog submission and review workflow.
- A community-maintained trusted-provider index.
- Richer local-first AI workflow starter packs.
- Additional client configuration targets as the ecosystem evolves.
- Optional metrics on catalog coverage and profile usage.
