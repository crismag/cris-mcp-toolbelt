# Roadmap

This roadmap describes the planned evolution of `cris-mcp-toolbelt`. It is a
direction, not a guarantee of dates. See [CONTEXT.md](CONTEXT.md) and
[IMPROVEMENT_GUIDE.md](IMPROVEMENT_GUIDE.md) for context.

The repository's core identity is a **catalog + governance hub**. First-party
MCP servers are an optional, isolated layer under `servers/` — see
[../servers/README.md](../servers/README.md).

## Release Principle

A first-party MCP server is promoted in the catalog (from `proposed` /
`unknown` toward `experimental` and beyond) only when it is complete, tested,
documented, and deployable. In-progress work stays out of public releases until
it is done.

## Milestone Overview

| Version | Theme | Status |
| --- | --- | --- |
| v0.1.0 | Catalog and governance foundation | Released |
| v0.2.0 | Usable Local Coding Assistant Stack | In progress |
| v0.3.0 | First-party PostgreSQL memory MCP | In progress |
| v0.4.0 | Memory-backed audit and profile integration | Planned |

## v0.1.0 — Catalog and Governance Foundation

**Status: released.**

**Goal.** A consistent, validated, contributable foundation with conservative
defaults.

**Delivered.**
- `catalog/schema.json` and 13 catalog entries under `catalog/servers/`.
- The seven safety profiles with a profile schema.
- Catalog validation, profile validation, and policy linting.
- Configuration rendering (`render_config.py`) and workspace enablement.
- Local Ollama workflow and database strategy documentation.
- Tests, CI, contribution templates, and a release checklist.
- The seven core context documents.

## v0.2.0 — Usable Local Coding Assistant Stack

**Status: in progress.**

**Goal.** Make the repo produce a working local MCP stack for
VSCode/Continue/Ollama-based coding assistance, with a safe feedback loop:
edit, run checks, inspect failures, fix, and rerun.

**Scope.**
- Real `render_config.py` output for Continue.
- Real rendered examples for `local-dev`, `readonly-research`, and `executor`.
- The `command-runner-controlled` server: allowlisted local command execution
  with four tools — `list_allowed_commands`, `dry_run_command`,
  `run_allowed_command`, `list_audit_events`.
- Workspace-root restriction, no shell-by-default behavior, blocked destructive
  patterns, timeout controls, dry-run mode, filtered environment, command
  policy file support, and JSONL audit records.
- Tests for allowed commands, blocked commands, outside-workspace paths, and
  audit recording.
- Documentation for using the stack with a local Ollama coding assistant.

**Acceptance criteria.**
- The repository keeps its catalog + governance identity; first-party server
  support is optional and isolated.
- Continue configs render real MCP `command` / `args` / `env` blocks.
- The server is complete, tested, documented, and verified through a real MCP
  client against a local workspace.
- The `command-runner-controlled` catalog entry is promoted from
  `proposed`/`unknown` to `experimental` once the server is working, with its
  `source_url` and `homepage` updated to the real implementation.

**Deferred.** Memory-backed audit integration.

## v0.3.0 — First-Party PostgreSQL Memory MCP

**Status: in progress.**

**Goal.** Build the PostgreSQL-backed memory and audit server as an optional
toolbelt-owned persistence backend.

**Scope.**
- The `toolbelt-postgres-memory` server: PostgreSQL-backed memory and audit
  with four tools — `create_memory_record`, `search_memory_records`,
  `create_audit_event`, `list_audit_events`.
- Schema initialization SQL and safe local development configuration.
- Record-safety guards (no secrets, credentials, private keys, or access
  tokens stored).
- Unit tests and an example MCP client configuration.

**Acceptance criteria.**
- The server is complete, tested, documented, and verified deployable against
  a real PostgreSQL instance.
- The `toolbelt-postgres-memory` catalog entry is promoted from
  `proposed`/`unknown` to `experimental` once the server is working, with its
  `source_url` and `homepage` updated to the real implementation.

**Deferred.** Profile integration and a memory-backed audit workflow.

## v0.4.0 — Memory-Backed Audit and Profile Integration

**Status: planned.**

**Goal.** Connect the memory/audit server to the profile model so that tool
activations are auditable in practice.

**Scope.**
- Integrate audit events with the seven profiles: high-impact activations are
  recorded through the memory/audit server.
- Add the planned `workspaces`, `model_usage`, and `database_connections`
  tables and the tools that manage them.
- Document the memory-backed audit workflow and how it complements the
  declarative `activation_policy` in the catalog.

**Acceptance criteria.**
- Audit events can be recorded and reviewed per workspace and per profile.
- The memory backend remains opt-in; file-based memory stays the
  zero-dependency default.
- No credentials are stored; blocked record types remain refused.

**Deferred.** Advanced orchestration.

## Future Ideas

These are not yet scheduled and may change or be dropped:

- A community-maintained catalog submission and review workflow.
- A community-maintained trusted-provider index.
- Advanced local agent orchestration — model routing and run audit records.
- `pgvector`-based retrieval for the memory backend.
- Richer local-first AI workflow starter packs.
- Additional client configuration targets as the ecosystem evolves.
