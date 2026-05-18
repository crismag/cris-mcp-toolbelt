# Example: MySQL / MariaDB Application Database Controlled Inspection

A worked example of read-only inspection of a MySQL or MariaDB application
database. It uses placeholders only and assumes no specific machine.

## Goal

Let an AI agent understand a MySQL or MariaDB application database — schema,
tables, columns — without any risk of modifying it.

## Setup

1. Create a **read-only** MySQL/MariaDB account scoped to the database to
   inspect. Read-only access is ultimately backed by this account's privileges.

2. Set the connection string in the environment:

   ```bash
   cp .env.example .env
   # set MYSQL_URL in .env
   ```

3. Enable the workspace with the `local-inspect` profile:

   ```bash
   {PROJECT_ROOT}/scripts/enable_for_workspace.sh {TARGET_REPOSITORY} local-inspect
   ```

## Steps

1. **Inspect the schema.** The `mysql-controlled` connector runs `SELECT`,
   `SHOW`, `DESCRIBE`, and `EXPLAIN` statements — listing tables, describing
   columns, and mapping relationships.

2. **Generate analysis.** Ask the agent to summarize the schema, find orphan
   records through read-only queries, or draft a SQL report.

3. **Draft a migration strategy.** Drafting is passive — the agent proposes a
   strategy; it does not execute anything.

## What stays controlled

- Default access is read-only: only `SELECT`, `SHOW`, `DESCRIBE`, `EXPLAIN`.
- Write statements (`INSERT`, `UPDATE`, `DELETE`, `CREATE`, `ALTER`) require the
  `writer` profile; admin statements require `admin-controlled`.
- Production databases are disabled by default.
- Query results are data exposure: avoid running queries against tables of
  personal or sensitive data without a deliberate decision.

## Optionally applying changes

To execute changes, re-enable the workspace with the `writer` profile (or
`admin-controlled` for admin statements) and use a database account with the
matching privileges. This is an intentional, audited profile change.

## See also

- [../docs/APPLICATION_DATABASE_ACCESS.md](../docs/APPLICATION_DATABASE_ACCESS.md)
- [../docs/DATABASE_SECURITY_MODEL.md](../docs/DATABASE_SECURITY_MODEL.md)
