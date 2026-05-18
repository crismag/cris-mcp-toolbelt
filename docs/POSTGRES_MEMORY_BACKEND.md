# PostgreSQL Memory Backend

PostgreSQL is the preferred **internal memory backend** for `cris-mcp-toolbelt`.
This page describes that role. It is distinct from application database access
(see [APPLICATION_DATABASE_ACCESS.md](APPLICATION_DATABASE_ACCESS.md)).

## Opt-in, not required

The file-based `memory-local` server is the zero-dependency default. The
PostgreSQL backend is an **optional upgrade** for users who want durable,
queryable, multi-workspace memory and audit storage. Using it should never be
required to clone and run the toolbelt.

## What it stores

The `toolbelt-postgres-memory` catalog entry
([catalog/servers/toolbelt-postgres-memory.yaml](../catalog/servers/toolbelt-postgres-memory.yaml))
describes a toolbelt-owned schema for:

- workspace registry
- memory records (project facts, decisions, conventions)
- tool audit events
- catalog and profile usage
- model-usage history

## Scope: toolbelt-owned only

The backend writes only to its own `toolbelt` schema and an allowlisted set of
tables. It does not read or modify a user's application data. The catalog
entry's `scope_controls` enumerate the allowed schema and tables.

Blocked record types — secrets, credentials, private keys, access tokens — must
never be stored in memory records.

## Status

`toolbelt-postgres-memory` is a planned first-party server. It is catalogued as
`review_status: proposed` and `trust_level: unknown`; it is not yet complete or
deployable. Per the project release policy, it is published for use only when
it is complete and functional for deployment.

## Setup (planned)

When the backend is available, initialization will use a helper script:

```bash
python3 scripts/init_toolbelt_db.py --database-url {POSTGRES_URL}
```

`scripts/init_toolbelt_db.py` currently exists as a stub. The connection string
is supplied through the `{POSTGRES_URL}` placeholder / environment variable and
is never committed.

## Future: vector storage

A future option is to add `pgvector`-based embedding storage for retrieval
workflows. This is a roadmap idea, not a v0.1.0 requirement, and would remain
opt-in.

## See also

- [DATABASE_MCP_STRATEGY.md](DATABASE_MCP_STRATEGY.md)
- [DATABASE_SECURITY_MODEL.md](DATABASE_SECURITY_MODEL.md)
- [../examples/local-postgres-memory-workflow.md](../examples/local-postgres-memory-workflow.md)
