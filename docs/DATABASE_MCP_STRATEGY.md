# Database MCP Strategy

This page describes how `cris-mcp-toolbelt` approaches database access through
MCP servers. Database access is a high-impact capability and is treated
accordingly.

## Two distinct roles

Databases appear in the toolbelt in two separate roles. Keep them distinct.

| Role | Purpose | Catalog entries |
| --- | --- | --- |
| Internal memory backend | Optional storage for the toolbelt's own memory, audit, and registry data | `toolbelt-postgres-memory` |
| Application database access | Controlled inspection of, and optional changes to, a project's own databases | `sqlite-controlled`, `postgres-controlled`, `mysql-controlled` |

The internal memory backend is about the toolbelt's data. Application database
access is about the user's project data. They have different owners, different
risks, and different default postures.

## Internal memory backend

PostgreSQL is the preferred internal memory backend for workspace registry,
memory records, audit events, catalog state, and model-usage history. It is
**opt-in**: the file-based `memory-local` server remains the zero-dependency
default. See [POSTGRES_MEMORY_BACKEND.md](POSTGRES_MEMORY_BACKEND.md).

## Application database connectors

Three controlled connectors cover common databases:

- **SQLite** — lightweight local databases (`sqlite-controlled`).
- **PostgreSQL** — application databases (`postgres-controlled`).
- **MySQL / MariaDB** — application databases (`mysql-controlled`).

All three default to read-only access. See
[APPLICATION_DATABASE_ACCESS.md](APPLICATION_DATABASE_ACCESS.md).

## Database capability modes

Database work is described with a consistent set of capability modes:

| Mode | Capability class | Default? |
| --- | --- | --- |
| `schema_inspect` | passive | yes |
| `readonly_query` | passive | yes |
| `analysis_query` | passive | yes |
| `controlled_write` | modifying | no — profile-gated |
| `migration_draft` | passive | yes (drafting only) |
| `migration_execute` | modifying | no — profile-gated |
| `admin_operation` | administrative | no — admin-controlled only |

Inspection, read-only queries, analysis, and drafting migrations are passive
and may be enabled by default. Writing data, executing migrations, and admin
operations are high-impact and require an intentional profile.

## Default posture

- Read-only by default for every connector.
- Mutation (`controlled_write`, `migration_execute`) requires the `writer` or
  `admin-controlled` profile.
- Admin operations require the `admin-controlled` profile.
- Production databases are disabled by default — see
  [DATABASE_SECURITY_MODEL.md](DATABASE_SECURITY_MODEL.md).
- Credentials are sourced from the environment only and are never committed.

## See also

- [POSTGRES_MEMORY_BACKEND.md](POSTGRES_MEMORY_BACKEND.md)
- [APPLICATION_DATABASE_ACCESS.md](APPLICATION_DATABASE_ACCESS.md)
- [DATABASE_SECURITY_MODEL.md](DATABASE_SECURITY_MODEL.md)
