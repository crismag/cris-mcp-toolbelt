#!/usr/bin/env python3
"""Check local Markdown links in public repository documentation.

The checker is intentionally dependency-free so it can run in CI beside the
other lightweight validation scripts. It validates local Markdown links across
tracked documentation areas and ignores external URLs, email links, and pure
anchor links.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote

IGNORED_DIRS = {
    ".git",
    ".pytest_cache",
    "__pycache__",
    "dev_plans",
}

EXTERNAL_PREFIXES = (
    "http://",
    "https://",
    "mailto:",
    "tel:",
)

LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")


def markdown_files(root: Path) -> list[Path]:
    """Return public Markdown files to check."""
    files: list[Path] = []
    for path in root.rglob("*.md"):
        if any(part in IGNORED_DIRS for part in path.relative_to(root).parts):
            continue
        files.append(path)
    return sorted(files)


def iter_markdown_links(path: Path) -> list[tuple[int, str]]:
    """Yield line number and raw Markdown destination for inline links."""
    links: list[tuple[int, str]] = []
    in_fence = False
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        for match in LINK_RE.finditer(line):
            links.append((line_no, match.group(1)))
    return links


def local_target(root: Path, source: Path, destination: str) -> Path | None:
    """Resolve a local Markdown destination to a filesystem path."""
    if destination.startswith(EXTERNAL_PREFIXES):
        return None
    if destination.startswith("#"):
        return source

    path_part = destination.split("#", 1)[0]
    if not path_part:
        return source

    if path_part.startswith("<") and path_part.endswith(">"):
        path_part = path_part[1:-1]

    path_part = unquote(path_part)
    if path_part.startswith("/"):
        return (root / path_part.lstrip("/")).resolve()
    return (source.parent / path_part).resolve()


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    failures: list[str] = []

    for file in markdown_files(root):
        for line_no, destination in iter_markdown_links(file):
            target = local_target(root, file, destination)
            if target is None:
                continue
            if not target.exists():
                rel_file = file.relative_to(root)
                failures.append(
                    f"{rel_file}:{line_no}: missing link target: {destination}"
                )

    if failures:
        print("[FAIL] documentation links")
        for failure in failures:
            print(f"  - {failure}")
        return 1

    print("[OK] documentation links")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
