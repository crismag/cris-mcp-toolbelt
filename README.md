# cris-mcp-toolbelt

A public, reusable, profile-driven **MCP capability control toolkit** for
AI-assisted development workflows.

`cris-mcp-toolbelt` helps developers safely configure, catalog, validate,
activate, and govern Model Context Protocol (MCP) servers for local and remote
AI coding agents — including local Ollama-based development environments.

It turns MCP usage from:

> random tools connected directly to an AI agent

into:

> cataloged tools + safety profiles + reusable configs + validation + governance

## Philosophy: configurable control, not crippled tools

MCP servers are powerful capability providers. The goal of this toolbelt is not
to remove that power — it is to make it **intentional**.

Some capabilities are passive and can be enabled by default. Others are
high-impact and should be activated deliberately through profiles, scope limits,
confirmations, allowlists, and audit records.

> Capabilities are not excluded. They are classified, scoped, configured,
> activated, and audited.

## What this repository provides

- **Catalog** — MCP server entries with standardized capability, activation, and
  scope metadata.
- **Profiles** — named safety profiles that control capability exposure.
- **Client configuration templates** — reusable starting points for MCP-capable
  clients.
- **Helper scripts** — small, dependency-light scripts to enable a workspace,
  validate the catalog, and check the local environment.
- **Documentation and governance** — capability model, security model,
  contribution standards, and review expectations.

## Capability model

Every capability is assigned a class so risk is described consistently:

| Class | Meaning |
| --- | --- |
| `passive` | Reads or inspects information only |
| `interactive` | Interacts with systems without mutation by default |
| `modifying` | Changes files, databases, repositories, or app state |
| `executing` | Runs code, commands, scripts, or build tools |
| `administrative` | Performs high-impact admin operations |

## Profiles

Capability is granted through named profiles:

| Profile | Intent |
| --- | --- |
| `readonly-research` | Public documentation and read-only research |
| `local-inspect` | Local workspace and repository inspection only |
| `local-dev` | Controlled local development assistance |
| `sandbox` | Experimental or unknown MCP servers in limited scope |
| `writer` | Explicit file, database, or repo mutation under scope controls |
| `executor` | Controlled command execution with allowlists |
| `admin-controlled` | High-impact operations that must be explicitly configured |

Defaults stay conservative: passive capability may be enabled where low-risk;
modifying, executing, and administrative capability requires an intentional
profile choice.

## Quick start

```bash
cp .env.example .env
{PROJECT_ROOT}/scripts/enable_for_workspace.sh {TARGET_REPOSITORY} readonly-research
{PROJECT_ROOT}/scripts/doctor.sh
{PROJECT_ROOT}/scripts/test_mcp_servers.sh
python3 {PROJECT_ROOT}/scripts/validate_catalog.py
```

Placeholders used throughout this repository:

`{PROJECT_ROOT}`, `{WORKSPACE_ROOT}`, `{TARGET_REPOSITORY}`, `{USER_HOME}`,
`{MCP_CONFIG_DIR}`, `{DATABASE_URL}`, `{POSTGRES_URL}`, `{MYSQL_URL}`,
`{OLLAMA_BASE_URL}`, `{GITHUB_TOKEN}`.

## Repository layout

- `docs/` — context, architecture, security, governance, and setup docs
- `catalog/` — MCP catalog entries with capability and security metadata
- `profiles/` — safety profiles that gate capability exposure
- `configs/` — reusable client configuration templates
- `scripts/` — helper scripts for validation and workspace enablement
- `examples/` — usage examples
- `tools/` — custom tool guidance

## Documentation

Start with the core context documents in [docs/](docs/):

- [CONTEXT.md](docs/CONTEXT.md) — what this repository is and why it exists
- [REPOSITORY_PRINCIPLES.md](docs/REPOSITORY_PRINCIPLES.md) — principles guiding all work
- [ROADMAP.md](docs/ROADMAP.md) — planned milestones
- [CONTRIBUTOR_GUIDANCE.md](docs/CONTRIBUTOR_GUIDANCE.md) — how to contribute
- [MAINTAINER_GUIDANCE.md](docs/MAINTAINER_GUIDANCE.md) — review and release process
- [AI_AGENT_GUIDE.md](docs/AI_AGENT_GUIDE.md) — guidance for AI coding agents
- [IMPROVEMENT_GUIDE.md](docs/IMPROVEMENT_GUIDE.md) — prioritized next work
- [CONFIG_RENDERING.md](docs/CONFIG_RENDERING.md) — generated client configs
- [COMMAND_RUNNER_CONTROLLED.md](docs/COMMAND_RUNNER_CONTROLLED.md) — safe command execution
- [MCP_SOURCE_CATALOG_EXPANSION.md](docs/MCP_SOURCE_CATALOG_EXPANSION.md) — adding external MCP sources safely

## Project status

The v0.1.0 catalog and governance foundation is released: catalog entries,
profiles, validation tooling, configuration rendering, examples, contribution
templates, and CI are in place. Current development is focused on the optional
first-party `servers/` layer, starting with controlled command execution for
local coding-agent feedback loops. See [ROADMAP.md](docs/ROADMAP.md) for the
plan.

For the practical local setup, see
[USE_WITH_LOCAL_OLLAMA_CODING_ASSISTANT.md](docs/USE_WITH_LOCAL_OLLAMA_CODING_ASSISTANT.md).

The catalog promotes an MCP server only when it is complete, tested,
documented, and verified deployable.

## Important: scope of safety controls

Profiles, activation policy, and scope controls are **declarative intent**. This
repository does not sit between an AI client and an MCP server at runtime — it
configures and governs, it does not enforce. These controls describe how a
capability *should* be activated and scoped; they are organizational and
advisory, not a runtime sandbox.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) and
[docs/CONTRIBUTOR_GUIDANCE.md](docs/CONTRIBUTOR_GUIDANCE.md).

## License

MIT. See [LICENSE](LICENSE).
