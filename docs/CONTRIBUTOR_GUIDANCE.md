# Contributor Guidance

Thank you for contributing to `cris-mcp-toolbelt`. This guide explains how to
make changes that pass review. It complements the root
[CONTRIBUTING.md](../CONTRIBUTING.md) and is governed by
[REPOSITORY_PRINCIPLES.md](REPOSITORY_PRINCIPLES.md).

## Before Contributing

- Read [CONTEXT.md](CONTEXT.md) and [REPOSITORY_PRINCIPLES.md](REPOSITORY_PRINCIPLES.md).
- Confirm your change keeps the repository public-safe: no private project
  names, private paths, internal systems, secrets, or personal infrastructure.
- Use generic placeholders: `{PROJECT_ROOT}`, `{WORKSPACE_ROOT}`,
  `{TARGET_REPOSITORY}`, `{USER_HOME}`, `{MCP_CONFIG_DIR}`, `{DATABASE_URL}`,
  `{POSTGRES_URL}`, `{MYSQL_URL}`, `{OLLAMA_BASE_URL}`, `{GITHUB_TOKEN}`.
- Use controlled-capability language. Capabilities are configurable, classified,
  scoped, and activated — not "dangerous" or "crippled".
- Prefer small, focused pull requests. One catalog entry or one profile change
  per PR is easier to review than a large mixed change.
- Run the available validation before opening a PR (see Pull Request Checklist).

## Completion Before Release

An MCP server is shared publicly only when it is **complete and functional for
deployment**. A catalog entry is published when its server is done — not while
it is still being built.

- In-progress or experimental MCP work is not merged to the public repository
  until it is finished and usable.
- A catalog entry should describe a server that a user can actually deploy and
  run by following its `source_url` and documentation.
- If you want to propose a server that is not yet complete, open an issue using
  the new-MCP-server template rather than adding a half-finished catalog entry.

## Adding a New MCP Server Entry

Catalog entries describe an MCP server, what it can do, and how its capabilities
are activated. Place each entry as its own file under `catalog/servers/`.

Every catalog entry must include these fields:

| Field | Purpose |
| --- | --- |
| `id` | Stable, unique identifier |
| `name` | Human-readable name |
| `description` | What the server does |
| `category` | Capability category (retrieval, filesystem, database, ...) |
| `provider` | Who publishes the server |
| `homepage` | Project homepage |
| `source_url` | Where the server's source or docs live |
| `license` | The server's license |
| `transport` | How the server is reached (for example stdio, http) |
| `auth_required` | Whether credentials are required |
| `capabilities` | What the server can do |
| `controlled_capabilities` | High-impact capabilities requiring intentional activation |
| `capability_class` | `passive`, `interactive`, `modifying`, `executing`, or `administrative` |
| `default_access` | `disabled`, `readonly`, `inspect`, `enabled`, `sandbox`, `write_opt_in`, `executor_opt_in`, or `admin_opt_in` |
| `allowed_profiles` | Profiles permitted to use the server |
| `activation_policy` | How high-impact capability is activated |
| `scope_controls` | Path, SQL, command, or network limits |
| `data_exposure` | What data the server can read or transmit |
| `trust_level` | `unknown`, `experimental`, `community`, or `trusted` |
| `review_status` | `proposed`, `reviewed`, `approved`, or `deprecated` |
| `security_notes` | Threats and mitigations |
| `tags` | Search and grouping tags |

In the description, capability fields, and security notes, state plainly:

- **Authentication behavior** — does it require credentials, and of what kind?
- **Filesystem access behavior** — does it read or write files, and where?
- **Network access behavior** — does it make outbound requests, and to where?
- **Write or mutation behavior** — can it change state, and how?
- **Shell execution behavior** — can it run commands on the host?
- **Suggested trust level** — your honest assessment, with reasoning.
- **Suggested default profile** — the most restrictive profile that still works.

New entries should start at `trust_level: unknown` or `experimental` and
`review_status: proposed`. Do not self-assign `trusted` or `approved`.

## Adding or Updating a Profile

- Profiles define capability exposure; changing one changes safety posture.
- The seven profiles are `readonly-research`, `local-inspect`, `local-dev`,
  `sandbox`, `writer`, `executor`, and `admin-controlled`.
- Keep the field set consistent with existing profiles so it can be validated.
- A new profile must document its intent, defaults, and intended use.
- Default access should be read-only or inspect unless the profile is explicitly
  a write, executor, or admin profile.
- A profile change PR must include a security rationale.

## Adding a Client Configuration Template

- Place templates under `configs/<client>/` (for example `configs/continue/`,
  `configs/generic/`).
- A template must reference a profile and must not grant capability beyond what
  that profile allows.
- Use placeholder paths and placeholder connection values, never real ones.
- Document the client and the template in the relevant `docs/` setup file.

## Adding Scripts

- Keep scripts small, readable, and dependency-light.
- Each script must print a clear usage message and exit non-zero on error.
- Scripts must default to safe behavior; high-impact capability requires an
  explicit flag or profile argument.
- Do not add scripts that enable write, execution, or unknown servers by
  default.

## Adding Documentation

- Match the existing professional, concise, public open-source tone.
- Use controlled-capability language consistently.
- Cross-link related documents instead of duplicating content.
- Avoid marketing language and avoid describing unbuilt features as if complete.
- Use tables and examples where they aid clarity; avoid destructive commands in
  examples.

## Security Review Expectations

Any change to catalog entries, profiles, capability classes, activation policy,
scope controls, trust levels, or scripts must include an explicit security
rationale in the PR description. Explain what capability the change exposes, why
it is acceptable, and what scope controls and activation policy apply. A change
with no security rationale will not be merged.

## Pull Request Checklist

- [ ] The change is public-safe (no private references, paths, or secrets).
- [ ] Placeholders are used instead of real values.
- [ ] Controlled-capability language is used; no alarmist framing.
- [ ] A new MCP server entry describes a complete, deployable server.
- [ ] Catalog entries include all required fields, including `capability_class`,
      `controlled_capabilities`, `activation_policy`, and `scope_controls`.
- [ ] New catalog entries start at `unknown`/`experimental` trust and
      `proposed` review status.
- [ ] Profiles keep conservative defaults unless explicitly a write, executor,
      or admin profile.
- [ ] Catalog validation passes (`python3 scripts/validate_catalog.py`).
- [ ] Policy linting passes once `policy_lint.py` exists.
- [ ] Markdown and YAML are well-formatted.
- [ ] A security rationale is included for any capability or trust change.
- [ ] Documentation is updated for any policy-impacting change.

## Examples of Good Contributions

- A new catalog entry for a real, completed, deployable MCP server with a
  verifiable `source_url`, a license, full capability classification, an
  activation policy, scope controls, honest security notes, and a conservative
  suggested trust level.
- A `local-inspect` or `executor` profile that fills a gap in the seven-profile
  set with a consistent, documented shape.
- A generic client configuration template that references an existing profile
  and uses placeholder values.
- A formatting cleanup PR that normalizes long lines without changing meaning.

## Examples of Contributions That Will Be Rejected

- A catalog entry for an unfinished or non-deployable MCP server.
- A catalog entry marked `trusted` or `approved` without review.
- A profile that enables modifying, executing, or administrative capability by
  default, or unknown servers outside `sandbox`.
- Any file containing a real token, key, credential, or realistic-looking fake
  secret.
- A private path, internal project name, or company-internal system reference.
- A config template that grants more capability than its referenced profile.
- A capability or trust change with no security rationale.
- A large, mixed PR that bundles unrelated changes and is hard to review.
