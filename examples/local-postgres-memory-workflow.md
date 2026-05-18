# Example: Local PostgreSQL Memory Backend Workflow

A worked example of using PostgreSQL as the toolbelt's internal memory backend.
It uses placeholders only and assumes no specific machine.

> Status: `toolbelt-postgres-memory` is a planned first-party server. This
> example describes the intended workflow; the backend is published for use
> only when it is complete and functional for deployment.

## Goal

Give the toolbelt durable, queryable memory and audit storage, instead of the
default file-based `memory-local` server.

## When to use this

Use the PostgreSQL backend only if you want durable, multi-workspace memory and
audit history. For most local development the file-based `memory-local` server
is sufficient and requires no database.

## Setup

1. Provision a PostgreSQL database and a least-privilege account scoped to a
   `toolbelt` schema.

2. Set the connection string in the environment — never in a committed file:

   ```bash
   cp .env.example .env
   # set POSTGRES_URL in .env
   ```

3. Initialize the toolbelt schema (planned helper, currently a stub):

   ```bash
   python3 scripts/init_toolbelt_db.py --database-url {POSTGRES_URL}
   ```

## Steps

1. **Enable the workspace** with the `local-dev` profile.

2. **The backend stores toolbelt-owned data only** — workspace registry, memory
   records, audit events, model-usage history — in the `toolbelt` schema. It
   does not read or write application data.

3. **Record project context.** As decisions and conventions accumulate, they
   are stored as memory records and recalled in later sessions.

4. **Review audit events.** Tool activations are recorded as audit events,
   giving a history of high-impact actions.

## What stays controlled

- The backend writes only to the allowlisted `toolbelt` schema and tables.
- Secrets, credentials, private keys, and access tokens are blocked record
  types and must never be stored.
- The connection string is supplied from the environment and never committed.
- Read-only versus write access is ultimately backed by the database account's
  privileges — use a least-privilege account.

## See also

- [../docs/POSTGRES_MEMORY_BACKEND.md](../docs/POSTGRES_MEMORY_BACKEND.md)
- [../docs/DATABASE_SECURITY_MODEL.md](../docs/DATABASE_SECURITY_MODEL.md)
