# Database Security Model

Database access is a high-impact capability. This page defines the controls
that apply to every database connector and to the internal memory backend.

## Connection and credential policy

- Connection strings are sourced from the environment only, through
  placeholders such as `{DATABASE_URL}`, `{POSTGRES_URL}`, and `{MYSQL_URL}`.
- Credentials are never committed to the repository — not as values and not as
  realistic-looking placeholders.
- Use least-privilege database accounts: a read-only account for inspection
  workflows, a separate scoped account for write workflows.
- Production databases are disabled by default. Connecting to production is a
  deliberate, separately configured action and should use the
  `admin-controlled` profile.

## SQL policy

Each connector declares an SQL policy in its catalog `scope_controls`:

- **Default mode is read-only.** Allowed statements are limited to queries and
  metadata inspection (`SELECT`, `EXPLAIN`, and database-specific equivalents
  such as `SHOW`, `DESCRIBE`, `PRAGMA`).
- **Writer statements** (`INSERT`, `UPDATE`, `DELETE`, `CREATE`, `ALTER`)
  require the `writer` profile.
- **Admin statements** (`DROP`, `GRANT`, `REVOKE`, `CREATE USER`, `ALTER USER`)
  require the `admin-controlled` profile.
- Particularly high-impact statements may be blocked by default even within a
  write profile (for example `DROP`, `VACUUM INTO`).

These are high-impact, controlled statements — not forbidden ones. They are
classified, gated, and audited, consistent with the project's
configurable-control philosophy.

## Scope controls

- An explicit database path or connection target is always required; no
  connector operates against an unspecified database.
- The internal memory backend is scoped to its own `toolbelt` schema and an
  allowlisted set of tables; it does not touch application data.
- Schema-metadata access is treated as passive inspection and may be enabled by
  default.

## Data exposure

- Treat query results as data exposure: rows returned to an agent enter its
  context.
- Do not run read-only queries against tables holding personal data,
  credentials, or other sensitive records without a deliberate decision.
- Blocked record types — secrets, credentials, private keys, access tokens —
  must never be written into the internal memory backend.

## Auditing

- Write and admin database activations are audited.
- Migration execution is audited; migration drafting is passive and is not a
  mutation.

## Declarative intent

The SQL policy, connection policy, and scope controls are declarative intent.
The toolbelt does not sit between a client and a database at runtime. Enforcing
read-only access ultimately depends on the database account's privileges — use
a least-privilege account so the policy is backed by real database permissions.

## See also

- [DATABASE_MCP_STRATEGY.md](DATABASE_MCP_STRATEGY.md)
- [APPLICATION_DATABASE_ACCESS.md](APPLICATION_DATABASE_ACCESS.md)
- [SECURITY_MODEL.md](SECURITY_MODEL.md)
