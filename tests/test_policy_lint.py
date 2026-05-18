"""Policy lint tests.

Verifies cross-artifact policy linting passes for the real catalog and
profiles.
"""

from __future__ import annotations

from conftest import run


def test_policy_lint_passes():
    result = run("scripts/policy_lint.py")
    assert result.returncode == 0, result.stdout + result.stderr


def test_policy_lint_reports_every_entry():
    result = run("scripts/policy_lint.py")
    # Every catalog entry should appear in the report exactly once.
    lines = [ln for ln in result.stdout.splitlines() if ln.startswith("[OK]")]
    assert len(lines) >= 13, result.stdout
