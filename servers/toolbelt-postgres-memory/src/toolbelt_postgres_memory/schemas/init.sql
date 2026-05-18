-- toolbelt-postgres-memory: schema initialization.
--
-- Creates the toolbelt-owned schema and the tables used by the v0.2.0 memory
-- and audit tools. The literal token {schema} is replaced by db.py with a
-- validated identifier; it is not user input.
--
-- This script is idempotent: it is safe to run repeatedly.

CREATE SCHEMA IF NOT EXISTS {schema};

-- Project memory: facts, decisions, conventions, and reusable context.
CREATE TABLE IF NOT EXISTS {schema}.memory_records (
    id          BIGINT      GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    workspace   TEXT        NOT NULL,
    kind        TEXT        NOT NULL,
    content     TEXT        NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS memory_records_workspace_idx
    ON {schema}.memory_records (workspace);
CREATE INDEX IF NOT EXISTS memory_records_kind_idx
    ON {schema}.memory_records (kind);

-- Audit trail of tool activations and high-impact actions.
CREATE TABLE IF NOT EXISTS {schema}.tool_audit_events (
    id          BIGINT      GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    workspace   TEXT        NOT NULL,
    tool        TEXT        NOT NULL,
    action      TEXT        NOT NULL,
    detail      TEXT        NOT NULL DEFAULT '',
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS tool_audit_events_workspace_idx
    ON {schema}.tool_audit_events (workspace);

-- Note: the workspaces, model_usage, and database_connections tables named in
-- the catalog entry are planned for a later version and are intentionally not
-- created here. v0.2.0 keeps the memory store modest.
