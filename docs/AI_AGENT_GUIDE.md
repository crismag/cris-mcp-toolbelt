# AI Agent Guide

This guide is for AI coding agents working on `cris-mcp-toolbelt`. Follow it
together with [REPOSITORY_PRINCIPLES.md](REPOSITORY_PRINCIPLES.md),
[CONTRIBUTOR_GUIDANCE.md](CONTRIBUTOR_GUIDANCE.md), and [CONTEXT.md](CONTEXT.md).

## Role of AI Agents in This Repository

AI agents are contributors, not maintainers. An agent may propose improvements —
formatting cleanup, documentation, schema work, validation logic, examples — but
capability and trust decisions belong to human maintainers. Agents should make
small, reviewable changes and explain them clearly.

## Repository Safety Constraints

This is a public, safety-first repository. Every change must:

- Stay public-safe: no private project names, private paths, internal systems,
  personal infrastructure, or secrets.
- Keep conservative defaults intact: read-only and inspect first; no
  modifying, executing, or administrative capability enabled by default; no
  unknown servers outside `sandbox`.
- Use controlled-capability language. Capabilities are configurable, classified,
  scoped, and activated — not "dangerous" or "crippled". Avoid overusing
  *dangerous*, *unsafe tool*, *crippled*, or *blocked forever*.
- Use generic placeholders: `{PROJECT_ROOT}`, `{WORKSPACE_ROOT}`,
  `{TARGET_REPOSITORY}`, `{USER_HOME}`, `{MCP_CONFIG_DIR}`, `{DATABASE_URL}`,
  `{POSTGRES_URL}`, `{MYSQL_URL}`, `{OLLAMA_BASE_URL}`, `{GITHUB_TOKEN}`.

## Capability and Profile Model

Use the shared vocabulary consistently:

- **Capability classes:** `passive`, `interactive`, `modifying`, `executing`,
  `administrative`.
- **Profiles:** `readonly-research`, `local-inspect`, `local-dev`, `sandbox`,
  `writer`, `executor`, `admin-controlled`.
- High-impact capability is recorded as `controlled_capabilities` with an
  `activation_policy` and `scope_controls`.
- `activation_policy` and `scope_controls` are declarative intent, not runtime
  enforcement — never describe them as if they technically block an action.

## Release Awareness

A catalog entry is published only when the MCP server it describes is complete
and functional for deployment. Do not add catalog entries for unfinished
servers; propose those as issues instead.

## Files AI Agents May Improve

With normal review, agents may improve:

- Documentation under `docs/`.
- `README.md` and other top-level prose.
- Formatting of YAML and Markdown files.
- `catalog/schema.json` and catalog structure (proposing, not finalizing trust).
- `validate_catalog.py`, `policy_lint.py`, and other validation logic.
- Examples under `examples/`.

## Files Requiring Extra Care

Treat these as sensitive; propose changes conservatively and flag them clearly
for maintainer review:

- `profiles/` — capability exposure. Never weaken a default.
- `catalog/servers/` entries — capability classes, trust levels, activation
  policy, and scope controls must be conservative and evidence-based.
- `scripts/` that enable workspaces or change capability.
- `.env.example` — must contain only obviously non-secret placeholders.

## Public-Safe Writing Rules

- Do not introduce private project names or private paths.
- Do not invent claims about specific MCP servers — only state what is
  verifiable from a real `source_url`.
- Do not add fake security guarantees or imply a server is safe without review.
- Do not add secrets, and do not add placeholders that look like real secrets.
- Do not describe unbuilt features as if they already exist.
- Do not use destructive commands in examples.

## Implementation Style

- Prefer small, focused changes over large rewrites.
- Match the existing professional, concise, public open-source tone.
- Keep scripts dependency-light and readable.
- Cross-link documents instead of duplicating content.
- Use tables and examples where they aid clarity.

## Validation Requirements

Before claiming success, actually run the available checks:

- `find docs -name "*.md" -type f` to confirm expected docs exist.
- `python3 scripts/validate_catalog.py` to validate the catalog.
- `policy_lint.py` once it exists.
- Markdown and YAML formatting review for any file changed.

Report results honestly. If a check was not run, say so. If a check failed,
report the failure and its output.

## Do Not Do These Things

- Do not enable modifying, executing, or administrative capability by default.
- Do not bypass or weaken profile governance or activation policy.
- Do not promote a catalog entry to a higher trust or review status on your own
  judgment.
- Do not add an unknown or unreviewed server to a non-sandbox profile.
- Do not add a catalog entry for an incomplete or non-deployable server.
- Do not commit secrets or realistic-looking fake secrets.
- Do not introduce private references or machine-specific paths.
- Do not describe activation policy or scope controls as runtime enforcement.
- Do not claim validation or tests passed unless they were actually run.

## Recommended Work Pattern

1. Inspect the current files relevant to the task.
2. Identify formatting, schema, capability, or consistency issues.
3. Make minimal, aligned improvements that respect the principles.
4. Validate Markdown, YAML, and scripts that were changed.
5. Run catalog validation and policy linting.
6. Summarize the exact changes made and any remaining TODOs.

## Final Response Expectations

When finished, provide a concise summary that includes:

- Files created or updated.
- Key guidance or changes added.
- Public-safety checks performed.
- Validation actually run and its result.
- Remaining recommended next steps.

Do not overstate completion. Honest, reviewable reporting is part of the task.
