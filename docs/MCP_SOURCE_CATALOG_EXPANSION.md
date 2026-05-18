# MCP Source Catalog Expansion

`cris-mcp-toolbelt` catalogs existing MCP servers before rebuilding them. The
catalog layer makes upstream capability visible, classifies risk, records
installation routes, and keeps activation profile-driven.

The project stance remains: configurable control, not crippled tools. Powerful
servers can be cataloged, but high-impact capability stays disabled or
profile-gated until it is scoped, configured, and audited.

## Verification Rules

Before adding or updating an external MCP source, verify:

- Official repository or homepage.
- Install command or access route.
- Transport type when documented.
- Authentication and token requirements.
- License, or `unknown` when not published.
- Runtime command when a single safe runtime is documented.
- Maintenance status, especially whether the source is archived.
- Capability class: passive, interactive, modifying, executing, or
  administrative.

Do not invent source URLs. If runtime, license, or safety behavior is unclear,
keep the entry conservative:

```yaml
trust_level: unknown
review_status: proposed
default_access: disabled
runtime: null
```

Use `security_notes.mitigations` to record important uncertainty when the schema
does not have a separate notes field.

## Trust Lifecycle

`proposed` means the entry is cataloged but not locally verified. A source may
be link-verified and still remain proposed.

`reviewed` requires a real local or remote MCP test:

- Server starts or remote endpoint connects.
- Tools list successfully.
- One safe tool call succeeds.
- Risky behavior is unavailable, denied, scoped, or documented.
- Runtime config renders correctly for the target client.

Do not use `approved` until maintainers have reviewed the entry and its runtime
behavior.

## Safety Classification

Catalog entries should be conservative by default:

- `passive`: context-only or reasoning-only tools.
- `interactive`: network reads, documentation lookup, search, or non-mutating
  external interactions.
- `modifying`: files, notes, database rows, issues, pull requests, messages, or
  persistent memory can change.
- `executing`: commands, tests, browser automation, builds, scripts, or code can
  run.
- `administrative`: cloud resources, identity, infrastructure, production
  services, or high-impact remote systems can change.

Set `audit_required: true` for modifying, executing, and administrative entries.
Use `runtime: null` for archived sources, remote-only servers that do not map to
the current renderer, or servers with multiple deployment routes that need a
separate setup decision.

## Expansion Packs

The initial external expansion covers:

- Local coding assistant core: filesystem, git, GitHub, sequential thinking,
  fetch.
- Web search and reading: SearXNG, Firecrawl, Context7.
- Knowledge and personal context: Obsidian, memory.
- Databases: SQLite, PostgreSQL, Supabase.
- Browser and UI testing: Playwright, Puppeteer.
- Cloud and productivity: Cloudflare, Google Drive, Slack.

Reference entries intentionally coexist with local `*-controlled` entries. The
controlled entries are the project-owned safety posture; reference entries track
upstream implementations and access routes.

## Local Verification Checklist

Use this checklist before moving an entry beyond `proposed`:

```bash
python3 scripts/validate_catalog.py
python3 scripts/validate_profiles.py
python3 scripts/policy_lint.py
python3 scripts/render_config.py --profile readonly-research --client generic --dry-run
python3 scripts/render_config.py --profile local-dev --client continue --workspace-root "$PWD" --dry-run
python3 scripts/render_config.py --profile executor --client continue --workspace-root "$PWD" --dry-run
python3 scripts/check_docs_links.py
python3 -m pytest tests/ -q
```

For first-party local servers, also run the server's own tests.

## Source Notes

The official `modelcontextprotocol/servers` repository contains maintained
reference servers such as Fetch, Filesystem, Git, Memory, and Sequential
Thinking. The separate `modelcontextprotocol/servers-archived` repository is
read-only and explicitly unmaintained; entries from it must stay proposed and
should usually keep `runtime: null` until a maintained replacement is selected.

Remote or cloud-backed MCP servers such as Supabase and Cloudflare need
least-privilege tokens, project/account scoping, and read-only modes where
available. Browser automation and command execution are executing capability;
they require explicit executor or writer profiles.
