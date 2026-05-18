"""Shared test fixtures and path constants for the cris-mcp-toolbelt suite."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = Path(__file__).resolve().parent / "fixtures"


@pytest.fixture(scope="session")
def repo_root() -> Path:
    return ROOT


@pytest.fixture(scope="session")
def fixtures_dir() -> Path:
    return FIXTURES


def run(*args: str) -> subprocess.CompletedProcess:
    """Run a repo script and capture its result."""
    return subprocess.run(
        [sys.executable, *args] if args[0].endswith(".py") else list(args),
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
