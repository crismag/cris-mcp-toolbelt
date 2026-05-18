# Catalog

The catalog describes MCP servers and how their capabilities are activated.

## Layout

- `schema.json` — JSON Schema for a catalog entry.
- `servers/` — one YAML file per MCP server (`<id>.yaml`).

Each entry's `id` must match its file name (without the `.yaml` extension).

## Entry format

Every entry under `servers/` declares the following fields:

| Field | Purpose |
| --- | --- |
| `id` | Stable, unique identifier (kebab-case); matches the file name |
| `name` | Human-readable name |
| `description` | What the server does |
| `category` | Capability category (for example `local-development`, `database`) |
| `provider` | Who publishes the server |
| `homepage` | Project homepage |
| `source_url` | Where the server's source or documentation lives |
| `license` | The server's license |
| `transport` | `stdio`, `http`, `sse`, or `websocket` |
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
| `security_notes` | `threats` and `mitigations` lists |
| `tags` | Search and grouping tags |

See [schema.json](schema.json) for the authoritative definition and allowed
values.

## Capability classes

| Class | Meaning |
| --- | --- |
| `passive` | Reads or inspects information only |
| `interactive` | Interacts with systems without mutation by default |
| `modifying` | Changes files, databases, repositories, or app state |
| `executing` | Runs code, commands, scripts, or build tools |
| `administrative` | Performs high-impact admin operations |

## Naming convention

Entries that support both read-only and write modes through profile-gated
activation use the `-controlled` suffix (for example `filesystem-controlled`).
The default mode stays conservative; write or execute modes are activated
through a profile.

## Lifecycle

New entries start at `trust_level: unknown` or `experimental` and
`review_status: proposed`. Trust and review status advance only through
maintainer review — see
[../docs/MAINTAINER_GUIDANCE.md](../docs/MAINTAINER_GUIDANCE.md).

An MCP server is published in the catalog only when it is complete and
functional for deployment.

## Important: declarative intent

`activation_policy` and `scope_controls` describe how a capability *should* be
activated and scoped. They are declarative intent — this repository does not
enforce them at runtime. See
[../docs/REPOSITORY_PRINCIPLES.md](../docs/REPOSITORY_PRINCIPLES.md), Principle 11.

## Validation

```bash
python3 scripts/validate_catalog.py
```

This validates every entry under `servers/` against `schema.json` and applies
cross-field consistency checks.
