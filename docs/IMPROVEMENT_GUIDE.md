# Repository Improvement Guide

This guide describes the next useful work for `cris-mcp-toolbelt`. It is
prioritized guidance, not implementation code. Use it together with
[ROADMAP.md](ROADMAP.md) and [REPOSITORY_PRINCIPLES.md](REPOSITORY_PRINCIPLES.md).

## Current State Summary

The v0.1.0 catalog and governance foundation is released:

- `catalog/schema.json` and 13 catalog entries live under `catalog/servers/`.
- All seven safety profiles exist and validate against `profiles/schema.json`.
- Catalog validation, profile validation, policy linting, configuration
  rendering, workspace enablement, and CI are in place.
- Documentation covers governance, security, local Ollama workflows, database
  access, client setup, and contribution/release expectations.
- First-party server implementations are isolated under `servers/`; the
  repository's core identity remains a catalog + governance hub.

Current development is focused on making local coding agents more capable with
the optional `command-runner-controlled` first-party server. It has unit-tested
allowlisted command execution, dry-run support, workspace restrictions,
environment filtering, and JSONL audit records, but it should not be promoted
in the catalog until it is verified through a real MCP client.

## Immediate Issues to Fix

- Keep README and docs status text aligned with the v0.1.0 release and the
  v0.2.0 "Usable Local Coding Assistant Stack" roadmap.
- Run `python3 scripts/check_docs_links.py` locally and in CI so public
  Markdown links stay valid as docs are added, renamed, or reorganized.
- Integration-test `servers/command-runner-controlled` through a real MCP
  client using `TOOLBELT_WORKSPACE_ROOT`.
- Verify YAML command policies and JSONL audit logs in a real workspace.
- Keep `command-runner-controlled` at `review_status: proposed` and
  `trust_level: unknown` until the MCP-client verification is complete.

## Priority 1: Documentation and Public Consistency

- Keep [README.md](../README.md), [CONTEXT.md](CONTEXT.md),
  [ROADMAP.md](ROADMAP.md), and this guide synchronized.
- Keep public docs free of links into `dev_plans/` or other local-only planning
  material.
- Prefer controlled-capability language: use `controlled_capabilities`, avoid
  alarmist framing, and describe profiles as declarative governance rather than
  runtime enforcement.
- Keep first-party server docs clear that `servers/` is optional and isolated
  from the catalog/profile tooling.

## Priority 2: Command Runner Verification

- Install `servers/command-runner-controlled` in a clean environment.
- Run its unit tests from the server directory.
- Configure an MCP client with `TOOLBELT_WORKSPACE_ROOT`.
- Configure a workspace-local command policy at
  `.cris-mcp-toolbelt/command-runner.config.yaml`.
- Exercise `list_allowed_commands`, `dry_run_command`,
  `run_allowed_command`, and `list_audit_events`.
- Confirm non-allowlisted commands, blocked patterns, and out-of-workspace
  working directories are refused.

## Priority 3: Catalog Promotion Readiness

- Keep `command-runner-controlled` at `review_status: proposed` and
  `trust_level: unknown` until it is complete, tested, documented, and verified
  deployable.
- Replace `example.com` placeholders with real repository paths or release
  URLs only after verification.
- Keep the catalog allowlist, blocked patterns, and rendered runtime config in
  sync with the server defaults.

## Priority 4: Test and CI Coverage

- Keep root tests scoped to catalog, profile, policy, and public-safety checks.
- Keep first-party server tests self-contained under each server directory.
- Run documentation link checking in CI with
  `python3 scripts/check_docs_links.py`.
- Consider a future CI job for first-party servers once their dependencies are
  intentionally included in CI.

## Priority 5: PostgreSQL Memory Server Verification

- Install `servers/toolbelt-postgres-memory` in a clean environment.
- Run its unit tests from the server directory.
- Start a local PostgreSQL instance, set `TOOLBELT_POSTGRES_URL`, and verify
  schema initialization.
- Exercise all four tools through an MCP-capable client:
  `create_memory_record`, `search_memory_records`, `create_audit_event`, and
  `list_audit_events`.
- Confirm blocked record kinds and secret-like content are refused before
  storage.

## Priority 6: Memory-Backed Audit Integration

Later, connect the memory/audit server to the profile model:

- Record high-impact tool activations by workspace and profile.
- Add the planned `workspaces`, `model_usage`, and `database_connections`
  tables and matching tools.
- Document how the audit workflow complements declarative
  `activation_policy` metadata.
- Keep the memory backend opt-in and keep file-based memory as the
  zero-dependency default.

## Acceptance Criteria for the Next Release

- [ ] Documentation accurately describes the released v0.1.0 foundation and
      current v0.2.0 work.
- [ ] Documentation link checking passes locally and in CI.
- [ ] `command-runner-controlled` is integration-tested through an MCP client.
- [ ] `docs/USE_WITH_LOCAL_OLLAMA_CODING_ASSISTANT.md` matches the verified
      Continue/Ollama flow.
- [ ] Catalog metadata matches what is actually implemented and verified.
- [ ] No private references, secrets, write-by-default behavior, or destructive
      example commands are introduced.

## Deferred Improvements

- Profile-integrated, memory-backed audit workflows.
- `pgvector`-based retrieval for the memory backend.
- A community registry workflow and trusted-provider index.
- Advanced local agent orchestration, model routing, and run audit records.

See [ROADMAP.md](ROADMAP.md) for where each deferred item is scheduled.
