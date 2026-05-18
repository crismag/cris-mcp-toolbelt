# servers/

First-party MCP **server implementations**.

This directory is an optional, isolated layer. The core identity of
`cris-mcp-toolbelt` is a **catalog + governance hub**; the `servers/` directory
adds real MCP servers beside that hub without contaminating it.

## Isolation rules

- Each server lives in its own subdirectory and is **self-contained**: its own
  `pyproject.toml`, dependencies, tests, and examples.
- The repository's catalog, profiles, and governance tooling do **not** depend
  on anything under `servers/`. You can use the catalog and profiles without
  installing any server.
- A server's dependencies (an MCP SDK, a database driver, ...) are declared in
  that server's `pyproject.toml`, never at the repository root.

## `servers/` vs `catalog/servers/`

These are different things — keep them distinct:

| Path | Contents |
| --- | --- |
| `catalog/servers/` | Catalog **metadata** — one YAML entry per MCP server |
| `servers/` | First-party MCP server **implementations** — actual code |

The catalog remains authoritative. A first-party server has both: a catalog
entry under `catalog/servers/<id>.yaml` and an implementation under
`servers/<id>/`.

## Release policy

A first-party MCP server is promoted in the catalog (from
`proposed`/`unknown` toward `experimental` and beyond) only when it is
complete, tested, documented, and deployable. Until then its catalog entry
stays `proposed`.

## Servers

| Server | Status |
| --- | --- |
| `command-runner-controlled` | In development — allowlisted local command execution |
| `toolbelt-postgres-memory` | In development — PostgreSQL-backed memory and audit |
