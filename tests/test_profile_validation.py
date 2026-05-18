"""Profile validation tests.

Verifies the real profiles pass validation and that all seven expected
profiles are present.
"""

from __future__ import annotations

from conftest import ROOT, run

EXPECTED_PROFILES = {
    "readonly-research",
    "local-inspect",
    "local-dev",
    "sandbox",
    "writer",
    "executor",
    "admin-controlled",
}


def test_real_profiles_validate():
    result = run("scripts/validate_profiles.py")
    assert result.returncode == 0, result.stdout + result.stderr


def test_all_seven_profiles_present():
    found = {
        p.name[: -len(".profile.yaml")]
        for p in (ROOT / "profiles").glob("*.profile.yaml")
    }
    assert found == EXPECTED_PROFILES, f"profile set mismatch: {found}"
