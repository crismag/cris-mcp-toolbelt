# Example: PostgreSQL Application Database Controlled Inspection

A worked example of read-only inspection of a PostgreSQL application database.
It uses placeholders only and assumes no specific machine.

## Goal

Let an AI agent understand a PostgreSQL application database — schema, tables,
relationships — without any risk of modifying it.

## Setup

1. Create a **read-only** PostgreSQL account scoped to the database to inspect.
   Read-only access is ultimately backed by this account's privileges.

2. Set the connection string in the environment:

   ```bash
   cp .env.example .env
   # set POSTGRES_URL in .env
   ```

3. Enable the workspace with the `local-inspect` profile:

   ```bash
   {PROJECT_ROOT}/scripts/enable_for_workspace.sh {TARGET_REPOSITORY} local-inspect
   ```

   `local-inspect` exposes only passive capability and read-only database
   access.

## Steps

1. **Inspect the schema.** The `postgres-controlled` connector runs `SELECT`
   and `EXPLAIN` statements and reads schema metadata — listing tables,
   describing columns, and mapping relationships.

2. **Generate analysis.** Ask the agent to produce ERD notes, summarize the
   schema, or suggest indexes based on read-only queries.

3. **Draft a migration plan.** Drafting a migration is passive — the agent
   writes a plan; it does not execute anything.

## What stays controlled

- Default access is read-only: only `SELECT`, `EXPLAIN`, and schema metadata.
- Write statements (`INSERT`, `UPDATE`, `DELETE`, `CREATE`, `ALTER`) require the
  `writer` profile; admin statements require `admin-controlled`.
- Production databases are disabled by default — connecting to production is a
  separate, deliberate decision.
- Query results are data exposure: avoid running queries against tables of
  personal or sensitive data without a deliberate decision.

## Optionally applying changes

To execute a drafted migration, re-enable the workspace with the `writer`
profile (or `admin-controlled` for admin statements) and use a database account
with the matching privileges. This is an intentional, audited profile change.

## See also

- [../docs/APPLICATION_DATABASE_ACCESS.md](../docs/APPLICATION_DATABASE_ACCESS.md)
- [../docs/DATABASE_SECURITY_MODEL.md](../docs/DATABASE_SECURITY_MODEL.md)
