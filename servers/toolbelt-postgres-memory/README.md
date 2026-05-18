# toolbelt-postgres-memory

A PostgreSQL-backed **memory and audit** MCP server for `cris-mcp-toolbelt`.

It is the project's first first-party MCP server — a dogfooding server that
stores project memory (facts, decisions, conventions) and an audit trail of
tool activations in a toolbelt-owned PostgreSQL schema.

## Status

Catalog entry: `toolbelt-postgres-memory` — currently `proposed` / `unknown`.
This server is promoted toward `experimental` only when it is complete,
tested, documented, and verified deployable. See
[../README.md](../README.md) for the first-party server release policy.

## Tools (v0.2.0)

| Tool | Purpose |
| --- | --- |
| `create_memory_record` | Store a memory record (fact, decision, convention) |
| `search_memory_records` | Search stored memory records, most recent first |
| `create_audit_event` | Record an audit event for a tool activation |
| `list_audit_events` | List recorded audit events, most recent first |

## Safety

- Writes go only to the toolbelt-owned schema (default `toolbelt`).
- Memory writes are refused when the record's `kind` is a blocked kind
  (secret, credential, private key, access token, password, ...) or when the
  content contains a recognizable secret-like token. See `safety.py`.
- The connection string is read from the environment only — never committed.

## Requirements

- Python 3.11+
- PostgreSQL (a local instance is fine)
- Dependencies: `mcp`, `psycopg` (declared in `pyproject.toml`)

## Install

```bash
cd servers/toolbelt-postgres-memory
python3 -m pip install -e ".[dev]"
```

## Configure

The server reads its connection string from the environment. Set one of:

```bash
export TOOLBELT_POSTGRES_URL=...   # preferred
# or
export POSTGRES_URL=...
```

Optionally set `TOOLBELT_SCHEMA` (default `toolbelt`). No connection string is
ever read from a committed file.

## Run

```bash
toolbelt-postgres-memory
```

On startup the server creates its schema and tables (idempotent), then serves
over stdio. Register it with an MCP-capable client — see
[examples/mcp-config.example.yaml](examples/mcp-config.example.yaml).

## Schema

The schema is defined in
[`src/toolbelt_postgres_memory/schemas/init.sql`](src/toolbelt_postgres_memory/schemas/init.sql)
and applied automatically on startup. v0.2.0 creates two tables:
`memory_records` and `tool_audit_events`. The `workspaces`, `model_usage`, and
`database_connections` tables named in the catalog entry are planned for a
later version.

## Test

```bash
python3 -m pytest tests/ -q
```

The unit tests cover the safety guards, configuration, and the tool layer
(with an in-memory fake database); they require neither `psycopg` nor a running
PostgreSQL. Integration testing against a real database is done locally.

## Layout

```text
toolbelt-postgres-memory/
├── pyproject.toml
├── README.md
├── src/toolbelt_postgres_memory/
│   ├── server.py      # MCP server entry point (4 tools)
│   ├── config.py      # environment-based configuration
│   ├── db.py          # psycopg data layer
│   ├── safety.py      # blocked-record guards
│   ├── tools/         # memory and audit tool implementations
│   └── schemas/       # init.sql
├── tests/
└── examples/
```
