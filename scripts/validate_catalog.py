#!/usr/bin/env python3
"""Minimal, dependency-free catalog validator."""

from __future__ import annotations

from pathlib import Path
import sys

REQUIRED_KEYS = {
    "id:",
    "name:",
    "description:",
    "category:",
    "provider:",
    "source_url:",
    "trust_level:",
    "default_access:",
    "profile_allowlist:",
    "security_notes:",
}


def validate_file(path: Path) -> list[str]:
    content = path.read_text(encoding="utf-8")
    errors: list[str] = []
    for key in REQUIRED_KEYS:
        if key not in content:
            errors.append(f"missing required key '{key[:-1]}'")
    if "{TARGET_WORKSPACE}" in content and path.name != "local-files.yaml":
        errors.append("placeholder {TARGET_WORKSPACE} should only appear in path-scoped entries")
    if "default_access: read-write" in content and "writer" not in content:
        errors.append("read-write access must include writer profile")
    return errors


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    catalog_dir = root / "catalog"
    if not catalog_dir.exists():
        print("catalog directory not found", file=sys.stderr)
        return 1

    files = sorted(catalog_dir.glob("*.yaml"))
    if not files:
        print("no catalog files found", file=sys.stderr)
        return 1

    failed = False
    for file in files:
        errs = validate_file(file)
        if errs:
            failed = True
            print(f"[FAIL] {file.name}")
            for err in errs:
                print(f"  - {err}")
        else:
            print(f"[OK] {file.name}")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
