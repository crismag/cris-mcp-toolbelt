# Application Database Access

This page covers controlled access to a project's own databases through the
catalog connectors. It is distinct from the internal memory backend (see
[POSTGRES_MEMORY_BACKEND.md](POSTGRES_MEMORY_BACKEND.md)).

All three connectors default to read-only access. Mutation is profile-gated;
admin operations require the `admin-controlled` profile.

## SQLite (`sqlite-controlled`)

A lightweight connector for local SQLite database files.

- **Use for:** local development databases, inspecting schema and metadata,
  generating SQL reports, drafting migration plans.
- **Default:** read-only. Allowed statements are `SELECT`, `EXPLAIN`, `PRAGMA`.
- **Write mode:** `INSERT`, `UPDATE`, `DELETE`, `CREATE`, `ALTER` require the
  `writer` profile. `DROP` and `VACUUM INTO` are blocked by default.
- **Scope:** an explicit database path is required.

## PostgreSQL (`postgres-controlled`)

A connector for PostgreSQL application databases.

- **Use for:** inspecting schemas, listing tables, generating ERD notes,
  drafting reports, suggesting indexes, supporting migration planning.
- **Default:** read-only. Allowed statements are `SELECT` and `EXPLAIN`; schema
  metadata is readable.
- **Write mode:** `INSERT`, `UPDATE`, `DELETE`, `CREATE`, `ALTER` require the
  `writer` profile.
- **Admin mode:** `DROP`, `GRANT`, `REVOKE`, `CREATE USER`, `ALTER USER`
  require the `admin-controlled` profile.
- **Connection:** sourced from the environment only; production is disabled by
  default.

## MySQL / MariaDB (`mysql-controlled`)

A connector for MySQL or MariaDB application databases.

- **Use for:** inspecting application schemas, listing tables, describing
  columns, drafting SQL reports, finding orphan records, suggesting migration
  strategy.
- **Default:** read-only. Allowed statements are `SELECT`, `SHOW`, `DESCRIBE`,
  `EXPLAIN`.
- **Write mode:** `INSERT`, `UPDATE`, `DELETE`, `CREATE`, `ALTER` require the
  `writer` profile.
- **Admin mode:** `DROP`, `GRANT`, `REVOKE`, `CREATE USER`, `ALTER USER`
  require the `admin-controlled` profile.
- **Connection:** sourced from the environment only; production is disabled by
  default.

## Connection placeholders

Connection strings are referenced through placeholders and supplied via the
environment — never committed:

- `{DATABASE_URL}` — generic database URL
- `{POSTGRES_URL}` — PostgreSQL connection string
- `{MYSQL_URL}` — MySQL / MariaDB connection string

## Choosing a profile

| Goal | Profile |
| --- | --- |
| Inspect schema, run read-only queries | `local-inspect` or `local-dev` |
| Apply data or schema changes | `writer` |
| Run admin operations (DROP, GRANT, users) | `admin-controlled` |

## See also

- [DATABASE_MCP_STRATEGY.md](DATABASE_MCP_STRATEGY.md)
- [DATABASE_SECURITY_MODEL.md](DATABASE_SECURITY_MODEL.md)
- [../examples/postgres-app-controlled-inspection.md](../examples/postgres-app-controlled-inspection.md)
- [../examples/mysql-app-controlled-inspection.md](../examples/mysql-app-controlled-inspection.md)
