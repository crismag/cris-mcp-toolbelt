"""Public-safety scan (private leakage detection).

Scans the public-facing files of the repository for content that must never
appear in a public repository: machine-specific absolute paths, private
project or domain references, and secret-like tokens.

The tests/ directory is excluded because this file necessarily contains the
forbidden patterns as regular expressions.
"""

from __future__ import annotations

import re

from conftest import ROOT

# Directories and root files that ship publicly and must be clean.
SCAN_DIRS = ["docs", "catalog", "profiles", "configs", "scripts", "examples", ".github"]
SCAN_ROOT_GLOBS = ["*.md"]

# Patterns that must not appear in public files.
FORBIDDEN = {
    "absolute /mnt path": re.compile(r"/mnt/"),
    "absolute home path": re.compile(r"/home/[A-Za-z0-9_]+/"),
    "private domain term": re.compile(r"\b(church|congregation|parish)\b", re.I),
    "private project ref": re.compile(r"\bcris-cie\b"),
    "GitHub token": re.compile(r"ghp_[A-Za-z0-9]{20,}"),
    "secret key token": re.compile(r"sk-[A-Za-z0-9]{20,}"),
    "AWS access key": re.compile(r"AKIA[0-9A-Z]{16}"),
    "private key block": re.compile(r"BEGIN [A-Z ]*PRIVATE KEY"),
}

TEXT_SUFFIXES = {".md", ".yaml", ".yml", ".json", ".sh", ".py", ".txt", ".example"}


def _files_to_scan():
    for rel in SCAN_DIRS:
        base = ROOT / rel
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if path.is_file() and path.suffix in TEXT_SUFFIXES:
                yield path
    for pattern in SCAN_ROOT_GLOBS:
        yield from ROOT.glob(pattern)


def test_no_private_references_in_public_files():
    violations: list[str] = []
    for path in _files_to_scan():
        text = path.read_text(encoding="utf-8", errors="replace")
        for line_no, line in enumerate(text.splitlines(), start=1):
            for label, pattern in FORBIDDEN.items():
                if pattern.search(line):
                    rel = path.relative_to(ROOT)
                    violations.append(f"{rel}:{line_no} [{label}] {line.strip()}")
    assert not violations, "public-safety violations:\n" + "\n".join(violations)
