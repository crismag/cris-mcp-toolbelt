#!/usr/bin/env python3
"""Inspect a database schema, read-only.

STATUS: STUB. This script does not yet connect to a database. It defines the
intended interface so that the workflow and documentation can reference it.
Real inspection is deferred — see docs/ROADMAP.md.

Intended behavior (when implemented):
  - Connect read-only to the database given by --database-url.
  - List tables, describe columns, and report relationships.
  - Use only read-only / metadata statements (SELECT, EXPLAIN, SHOW,
    DESCRIBE, PRAGMA depending on --kind).
  - Never run write or admin statements.
"""

from __future__ import annotations

import argparse
import sys


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--database-url",
        default="{DATABASE_URL}",
        help="Database connection string (placeholder; supply via environment).",
    )
    parser.add_argument(
        "--kind",
        choices=["postgres", "mysql", "sqlite"],
        default="postgres",
        help="Database kind.",
    )
    parser.parse_args()

    print("[stub] inspect_db_schema.py is not yet implemented.")
    print("[stub] Intended: read-only schema inspection (no write or admin SQL).")
    print("[stub] See docs/APPLICATION_DATABASE_ACCESS.md and docs/ROADMAP.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
