"""Catalog validation tests.

Verifies the real catalog passes validation, and that the catalog schema
accepts a valid fixture and rejects an invalid one.
"""

from __future__ import annotations

import json

import yaml
from jsonschema import Draft202012Validator

from conftest import FIXTURES, ROOT, run


def _schema_validator() -> Draft202012Validator:
    schema = json.loads(
        (ROOT / "catalog" / "schema.json").read_text(encoding="utf-8")
    )
    return Draft202012Validator(schema)


def test_real_catalog_validates():
    result = run("scripts/validate_catalog.py")
    assert result.returncode == 0, result.stdout + result.stderr


def test_valid_fixture_passes_schema():
    validator = _schema_validator()
    entry = yaml.safe_load((FIXTURES / "valid-server.yaml").read_text())
    errors = list(validator.iter_errors(entry))
    assert errors == [], [e.message for e in errors]


def test_invalid_fixture_fails_schema():
    validator = _schema_validator()
    entry = yaml.safe_load((FIXTURES / "invalid-server.yaml").read_text())
    errors = list(validator.iter_errors(entry))
    assert errors, "invalid-server.yaml should have produced schema errors"


def test_every_catalog_entry_id_matches_filename():
    servers_dir = ROOT / "catalog" / "servers"
    for file in sorted(servers_dir.glob("*.yaml")):
        entry = yaml.safe_load(file.read_text(encoding="utf-8"))
        assert entry["id"] == file.stem, f"{file.name}: id != file name"
