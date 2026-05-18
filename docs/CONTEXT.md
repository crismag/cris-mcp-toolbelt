# cris-mcp-toolbelt Context

## Purpose

`cris-mcp-toolbelt` is a public, reusable, profile-driven MCP capability control
toolkit for AI-assisted development workflows.

It helps developers safely configure, catalog, validate, activate, and govern
Model Context Protocol (MCP) servers for local and remote AI coding agents,
including local Ollama-based development environments.

The goal is not to cripple MCP tools. The goal is:

> Configurable control, not permanent exclusion.

MCP servers are treated as powerful capability providers. Some capabilities are
passive and may be enabled by default. Other capabilities are high-impact and
should be activated intentionally through profiles, scope limits, confirmations,
allowlists, and audit records.

## Target Users

- Developers using MCP-capable AI coding agents who want a safe, repeatable
  setup instead of hand-editing client configuration.
- Teams that need a shared, reviewable standard for which MCP servers are
  approved and at what capability level.
- Open-source contributors who want to publish or catalog MCP servers with
  clear, comparable capability and activation metadata.
- Local-first developers who run models on their own hardware (for example via
  Ollama) and want MCP integration without relying on a hosted provider.

## Problems This Repository Solves

- **Unmanaged capability.** MCP clients are often configured ad hoc, with no
  record of what a server can access. This repository makes capability explicit
  through profiles and catalog metadata.
- **No comparable capability signal.** There is no common way to describe what
  an MCP server can do or how high-impact it is. The catalog schema standardizes
  that description.
- **Unscoped activation.** It is easy to grant write, shell, or admin access
  without intending to. Profiles and activation policy make escalation explicit
  and conservative by default.
- **Non-portable setup.** Client configuration differs across tools. Reusable
  templates reduce per-client guesswork.
- **No contribution standard.** Without a review process, a community catalog
  becomes untrustworthy. Governance and validation make contributions reviewable.

## What This Repository Provides

- **Catalog** — MCP server entries with standardized capability, activation, and
  scope metadata under `catalog/servers/`.
- **Profiles** — named safety profiles that control capability exposure.
- **Client configuration templates** — reusable starting points for MCP-capable
  clients.
- **Helper scripts** — small, dependency-light scripts to enable a workspace,
  validate the catalog, and check the local environment.
- **Documentation** — architecture, security model, governance, contribution,
  and roadmap guidance.
- **Governance patterns** — capability classes, trust levels, review status, and
  review expectations for community contributions.

## What This Repository Is Not

- It is **not** a private automation system or an internal company tool.
- It is **not** an MCP server runtime, and it does not enforce policy at
  runtime — see [Configurable Control, Not Runtime Enforcement](#configurable-control-not-runtime-enforcement).
- It is **not** a hosted service, registry API, or package manager.
- It does **not** ship secrets, credentials, or production configuration.
- It does **not** guarantee that any cataloged server is secure — it provides
  metadata and review process, not a security warranty.
- It is **not** tied to any single AI client, model, or local model runtime.

## Core Design Philosophy

1. **Configurable, not crippled.** Capabilities are classified, scoped,
   configured, activated, and audited — never permanently excluded.
2. **Least privilege by default.** Every default is the most restrictive option
   that is still useful.
3. **Intentional escalation.** High-impact capability is opt-in through a named
   profile and an activation policy, never implicit.
4. **Defense in depth.** Profiles, capability metadata, and scope controls
   reinforce each other.
5. **Public-safe and generic.** Everything in the repository is suitable for a
   public audience and uses generic placeholders.
6. **Validation before trust.** Catalog entries and profiles are validated and
   reviewed before they are relied upon.
7. **Documentation before complexity.** Behavior is documented before it is
   automated.

## Capability Model

The repository classifies every capability so catalog entries, profiles, and
documentation describe risk consistently:

| Capability class | Meaning | Examples |
| --- | --- | --- |
| `passive` | Reads or inspects information only | file read, schema inspect, git diff |
| `interactive` | Interacts with systems without mutation by default | browser navigation, public fetch |
| `modifying` | Changes files, databases, repositories, or app state | file write, DB update, issue write |
| `executing` | Runs code, commands, scripts, tests, or build tools | shell, pytest, npm test |
| `administrative` | Performs high-impact admin operations | deployments, credential changes |

High-impact capabilities are recorded as `controlled_capabilities` on a catalog
entry, paired with an `activation_policy` and `scope_controls`.

## Safety Profiles

Capability is granted through named profiles. The repository targets seven:

| Profile | Intent |
| --- | --- |
| `readonly-research` | Public documentation and read-only research |
| `local-inspect` | Local workspace and repository inspection only |
| `local-dev` | Controlled local development assistance |
| `sandbox` | Experimental or unknown MCP servers in limited scope |
| `writer` | Explicit file, database, or repo mutation under scope controls |
| `executor` | Controlled command execution with allowlists |
| `admin-controlled` | High-impact operations that must be explicitly configured |

Defaults stay conservative: passive capabilities may be enabled where low-risk;
modifying, executing, and administrative capabilities require an intentional
profile choice.

## Configurable Control, Not Runtime Enforcement

The catalog's `activation_policy`, `scope_controls`, and confirmation and audit
fields are **declarative intent**. This repository does not sit between an AI
client and an MCP server at runtime. Until configuration rendering exists, and
even then only as far as a target client supports it, these fields describe how
a capability *should* be activated and scoped — they are organizational and
advisory controls, not a runtime sandbox. Documentation must never imply
otherwise.

## Local-First AI Workflow Support

The repository supports developers who run models locally. Local model runtimes
such as Ollama are treated as one supported option, not a requirement:

- No single local runtime is assumed or mandated.
- Local-first setups do not require a hosted AI provider.
- The `local-dev` and `local-inspect` profiles describe local-development
  capability without enabling broad write, execution, or network access.

## Public Repository Constraints

Because the repository is public, all content must be safe to publish:

- No private project names, internal systems, or client names.
- No private or machine-specific filesystem paths.
- No real tokens, API keys, or credentials — not even realistic-looking fakes.
- Use generic placeholders: `{PROJECT_ROOT}`, `{WORKSPACE_ROOT}`,
  `{TARGET_REPOSITORY}`, `{USER_HOME}`, `{MCP_CONFIG_DIR}`, `{DATABASE_URL}`,
  `{POSTGRES_URL}`, `{MYSQL_URL}`, `{OLLAMA_BASE_URL}`, `{GITHUB_TOKEN}`.
- Catalog entries use generic provider names and example source URLs until a
  real, reviewed entry is contributed.

## Current Repository Maturity

The repository is currently an early-stage **documentation-first skeleton**:

- Profiles, catalogs, configs, scripts, and docs exist as a structural skeleton.
- Catalog entries are illustrative examples, not reviewed real servers.
- Catalog validation is intentionally dependency-free and uses simple checks.
- Client configuration coverage is limited.
- There is no continuous integration yet.

It is honest scaffolding: the structure and intent are in place, but the
repository is not yet clone-and-run for real workflows.

## Target v0.1.0 Outcome

Version 0.1.0 turns the skeleton into a usable, safe, contributable foundation.
By v0.1.0 the repository should provide:

- Consistent formatting and public-safe content across the repository.
- A formal `catalog/schema.json` and a catalog organized under
  `catalog/servers/`.
- Core catalog entries for the target MCP servers with capability classes,
  `controlled_capabilities`, activation policy, and scope controls.
- The seven profiles with consistent, validated shape.
- Schema-aware catalog validation and policy linting.
- Database strategy and local Ollama workflow documentation.
- Basic continuous integration that runs validation on every change.
- Contribution templates and a release checklist.

See [ROADMAP.md](ROADMAP.md) for milestones. A detailed phase breakdown is
maintained in the project's internal development plans.
