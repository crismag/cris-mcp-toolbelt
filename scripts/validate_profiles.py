#!/usr/bin/env python3
"""Validate cris-mcp-toolbelt profiles against profiles/schema.json.

Each <id>.profile.yaml file under profiles/ is parsed and validated against the
JSON Schema. A few lightweight cross-field consistency checks are also applied.

Requires: PyYAML, jsonschema.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    print("error: PyYAML is required (pip install pyyaml)", file=sys.stderr)
    raise SystemExit(2) from None

try:
    from jsonschema import Draft202012Validator
except ImportError:  # pragma: no cover
    print("error: jsonschema is required (pip install jsonschema)", file=sys.stderr)
    raise SystemExit(2) from None

# A capability class implied by a non-trivial setting must be declared in
# allowed_capability_classes.
IMPLIED_CLASSES = [
    ("filesystem mode 'read-write'", "modifying",
     lambda p: (p.get("filesystem") or {}).get("mode") == "read-write"),
    ("database mode 'read-write'", "modifying",
     lambda p: (p.get("database") or {}).get("mode") == "read-write"),
    ("database mode 'admin'", "administrative",
     lambda p: (p.get("database") or {}).get("mode") == "admin"),
    ("command_execution enabled/allowlisted", "executing",
     lambda p: (p.get("command_execution") or {}).get("mode") in {"allowlisted", "enabled"}),
    ("write_actions 'enabled'", "modifying",
     lambda p: p.get("write_actions") == "enabled"),
]


def consistency_checks(profile: dict) -> list[str]:
    """Cross-field checks beyond pure schema validation."""
    errors: list[str] = []
    classes = set(profile.get("allowed_capability_classes") or [])

    for label, required_class, predicate in IMPLIED_CLASSES:
        if predicate(profile) and required_class not in classes:
            errors.append(
                f"{label} requires capability class '{required_class}' "
                f"in allowed_capability_classes"
            )

    # Only the sandbox profile may allow unknown MCP servers.
    if profile.get("allow_unknown_mcp") and profile.get("id") != "sandbox":
        errors.append("allow_unknown_mcp may be true only for the sandbox profile")

    return errors


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    schema_path = root / "profiles" / "schema.json"
    profiles_dir = root / "profiles"

    if not schema_path.exists():
        print(f"error: schema not found at {schema_path}", file=sys.stderr)
        return 1

    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)

    files = sorted(profiles_dir.glob("*.profile.yaml"))
    if not files:
        print("error: no profiles found under profiles/", file=sys.stderr)
        return 1

    failed = False
    for file in files:
        errors: list[str] = []
        try:
            profile = yaml.safe_load(file.read_text(encoding="utf-8"))
        except yaml.YAMLError as exc:
            print(f"[FAIL] {file.name}")
            print(f"  - YAML parse error: {exc}")
            failed = True
            continue

        if not isinstance(profile, dict):
            print(f"[FAIL] {file.name}")
            print("  - top-level YAML must be a mapping")
            failed = True
            continue

        for err in sorted(validator.iter_errors(profile), key=lambda e: list(e.path)):
            location = "/".join(str(p) for p in err.path) or "(root)"
            errors.append(f"{location}: {err.message}")

        errors.extend(consistency_checks(profile))

        expected_id = file.name[: -len(".profile.yaml")]
        if profile.get("id") and profile["id"] != expected_id:
            errors.append(
                f"id '{profile['id']}' does not match file name '{expected_id}'"
            )

        if errors:
            failed = True
            print(f"[FAIL] {file.name}")
            for err in errors:
                print(f"  - {err}")
        else:
            print(f"[OK] {file.name}")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
