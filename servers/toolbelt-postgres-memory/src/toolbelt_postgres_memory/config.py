"""Configuration for the toolbelt-postgres-memory server.

Configuration is sourced from the environment. No connection string or secret
is ever read from a committed file.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

# Environment variable holding the PostgreSQL connection string. The value is
# never committed; see .env.example at the repository root.
DATABASE_URL_VARS = ("TOOLBELT_POSTGRES_URL", "POSTGRES_URL")

# The toolbelt-owned schema. The server writes only inside this schema.
DEFAULT_SCHEMA = "toolbelt"
SCHEMA_VAR = "TOOLBELT_SCHEMA"


class ConfigError(RuntimeError):
    """Raised when required configuration is missing or invalid."""


@dataclass(frozen=True)
class Config:
    """Resolved server configuration."""

    database_url: str
    schema: str = DEFAULT_SCHEMA


def load_config(env: dict[str, str] | None = None) -> Config:
    """Build a Config from the environment.

    Raises ConfigError if no database URL is set.
    """
    env = os.environ if env is None else env

    database_url = ""
    for var in DATABASE_URL_VARS:
        value = env.get(var, "").strip()
        if value:
            database_url = value
            break

    if not database_url:
        raise ConfigError(
            "no database URL set; export one of: "
            + ", ".join(DATABASE_URL_VARS)
        )

    schema = env.get(SCHEMA_VAR, "").strip() or DEFAULT_SCHEMA
    if not schema.isidentifier():
        raise ConfigError(f"invalid schema name: {schema!r}")

    return Config(database_url=database_url, schema=schema)
