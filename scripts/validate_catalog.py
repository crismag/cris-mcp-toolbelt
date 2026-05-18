#!/usr/bin/env python3
"""Validate cris-mcp-toolbelt catalog entries against catalog/schema.json.

Each YAML file under catalog/servers/ is parsed and validated against the
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

def consistency_checks(entry: dict) -> tuple[list[str], object]:
    """Lightweight cross-field checks beyond pure schema validation.

    Deeper capability/activation linting (for example which profile may
    activate which capability) is the job of policy_lint.py.
    """
    errors: list[str] = []

    entry_id = entry.get("id")
    activation = entry.get("activation_policy") or {}
    runtime = entry.get("runtime")

    # activation_policy.allowed_profiles must be a subset of allowed_profiles.
    top_profiles = set(entry.get("allowed_profiles") or [])
    act_profiles = set(activation.get("allowed_profiles") or [])
    extra = act_profiles - top_profiles
    if extra:
        errors.append(
            f"activation_policy.allowed_profiles not in allowed_profiles: {sorted(extra)}"
        )

    if runtime is not None and entry.get("transport") != "stdio":
        errors.append("runtime command blocks are currently supported only for stdio")

    return errors, entry_id


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    schema_path = root / "catalog" / "schema.json"
    servers_dir = root / "catalog" / "servers"

    if not schema_path.exists():
        print(f"error: schema not found at {schema_path}", file=sys.stderr)
        return 1
    if not servers_dir.exists():
        print("error: catalog/servers directory not found", file=sys.stderr)
        return 1

    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)

    files = sorted(servers_dir.glob("*.yaml"))
    if not files:
        print("error: no catalog entries found under catalog/servers/", file=sys.stderr)
        return 1

    failed = False
    for file in files:
        errors: list[str] = []
        try:
            entry = yaml.safe_load(file.read_text(encoding="utf-8"))
        except yaml.YAMLError as exc:
            print(f"[FAIL] {file.name}")
            print(f"  - YAML parse error: {exc}")
            failed = True
            continue

        if not isinstance(entry, dict):
            print(f"[FAIL] {file.name}")
            print("  - top-level YAML must be a mapping")
            failed = True
            continue

        for err in sorted(validator.iter_errors(entry), key=lambda e: list(e.path)):
            location = "/".join(str(p) for p in err.path) or "(root)"
            errors.append(f"{location}: {err.message}")

        cross_errors, entry_id = consistency_checks(entry)
        errors.extend(cross_errors)

        if entry_id and entry_id != file.stem:
            errors.append(f"id '{entry_id}' does not match file name '{file.stem}'")

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
