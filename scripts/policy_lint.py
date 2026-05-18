#!/usr/bin/env python3
"""Cross-artifact policy linter for cris-mcp-toolbelt.

Where validate_catalog.py and validate_profiles.py check each file against its
schema, policy_lint.py checks consistency *between* the catalog and the
profiles, and checks capability-governance rules.

Checks applied to each catalog entry:
  1. Every profile referenced (allowed_profiles and
     activation_policy.allowed_profiles) has a profile file.
  2. High-impact entries (capability_class modifying / executing /
     administrative) set activation_policy.audit_required to true.
  3. High-impact entries declare at least one controlled_capability.
  4. Executing entries restrict activation to executor, writer, or
     admin-controlled profiles.
  5. Administrative entries include admin-controlled among the profiles
     allowed to activate them.

Requires: PyYAML.
"""

from __future__ import annotations

import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    print("error: PyYAML is required (pip install pyyaml)", file=sys.stderr)
    raise SystemExit(2) from None

ROOT = Path(__file__).resolve().parents[1]
HIGH_IMPACT = {"modifying", "executing", "administrative"}
EXECUTING_PROFILES = {"executor", "writer", "admin-controlled"}


def known_profiles() -> set[str]:
    return {
        p.name[: -len(".profile.yaml")]
        for p in (ROOT / "profiles").glob("*.profile.yaml")
    }


def load_catalog() -> list[tuple[str, dict]]:
    servers_dir = ROOT / "catalog" / "servers"
    out: list[tuple[str, dict]] = []
    for file in sorted(servers_dir.glob("*.yaml")):
        entry = yaml.safe_load(file.read_text(encoding="utf-8"))
        out.append((file.name, entry))
    return out


def lint_entry(entry: dict, profiles: set[str]) -> list[str]:
    errors: list[str] = []
    cls = entry.get("capability_class")
    activation = entry.get("activation_policy") or {}
    act_profiles = set(activation.get("allowed_profiles") or [])
    referenced = set(entry.get("allowed_profiles") or []) | act_profiles

    # 1. Referenced profiles must exist.
    missing = referenced - profiles
    if missing:
        errors.append(f"references unknown profile(s): {sorted(missing)}")

    if cls in HIGH_IMPACT:
        # 2. High-impact entries must be audited.
        if not activation.get("audit_required"):
            errors.append(
                f"capability_class '{cls}' requires activation_policy."
                f"audit_required: true"
            )
        # 3. High-impact entries must declare controlled capabilities.
        if not (entry.get("controlled_capabilities") or []):
            errors.append(
                f"capability_class '{cls}' requires at least one "
                f"controlled_capability"
            )

    # 4. Executing entries restrict activation profiles.
    if cls == "executing":
        leaked = act_profiles - EXECUTING_PROFILES
        if leaked:
            errors.append(
                f"executing entry must not be activatable from {sorted(leaked)}"
            )

    # 5. Administrative entries must allow the admin-controlled profile.
    if cls == "administrative" and "admin-controlled" not in act_profiles:
        errors.append(
            "administrative entry must include admin-controlled in "
            "activation_policy.allowed_profiles"
        )

    return errors


def main() -> int:
    profiles = known_profiles()
    if not profiles:
        print("error: no profiles found", file=sys.stderr)
        return 1

    catalog = load_catalog()
    if not catalog:
        print("error: no catalog entries found", file=sys.stderr)
        return 1

    failed = False
    for name, entry in catalog:
        if not isinstance(entry, dict):
            print(f"[FAIL] {name}")
            print("  - not a mapping")
            failed = True
            continue
        errors = lint_entry(entry, profiles)
        if errors:
            failed = True
            print(f"[FAIL] {name}")
            for err in errors:
                print(f"  - {err}")
        else:
            print(f"[OK] {name}")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
