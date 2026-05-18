#!/usr/bin/env python3
"""Validate that a profile's database settings are consistent.

STATUS: STUB. This script defines the intended interface and performs only a
minimal check. Full database-policy linting is deferred to policy_lint.py —
see docs/ROADMAP.md.

Intended behavior (when implemented):
  - Cross-check a profile's database mode against catalog entries that target
    that profile, ensuring no database connector grants more than the profile
    allows.
  - Confirm that write or admin database modes appear only in the writer,
    executor, or admin-controlled profiles.

Current behavior: reports the database mode declared by the named profile.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    print("error: PyYAML is required (pip install pyyaml)", file=sys.stderr)
    raise SystemExit(2) from None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--profile",
        required=True,
        help="Profile id, for example local-dev.",
    )
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    profile_path = root / "profiles" / f"{args.profile}.profile.yaml"
    if not profile_path.exists():
        print(f"error: profile not found: {profile_path}", file=sys.stderr)
        return 1

    profile = yaml.safe_load(profile_path.read_text(encoding="utf-8"))
    db_mode = (profile.get("database") or {}).get("mode", "unknown")
    print(f"profile '{args.profile}': database mode = {db_mode}")
    print("[stub] full database-policy linting is not yet implemented.")
    print("[stub] See docs/DATABASE_SECURITY_MODEL.md and docs/ROADMAP.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
