"""Tests for environment-based configuration."""

from __future__ import annotations

import pytest

from toolbelt_postgres_memory.config import (
    DEFAULT_SCHEMA,
    Config,
    ConfigError,
    load_config,
)


def test_loads_postgres_url():
    cfg = load_config({"POSTGRES_URL": "postgresql://localhost/db"})
    assert isinstance(cfg, Config)
    assert cfg.database_url == "postgresql://localhost/db"
    assert cfg.schema == DEFAULT_SCHEMA


def test_toolbelt_url_takes_precedence():
    cfg = load_config(
        {
            "TOOLBELT_POSTGRES_URL": "postgresql://localhost/toolbelt",
            "POSTGRES_URL": "postgresql://localhost/other",
        }
    )
    assert cfg.database_url == "postgresql://localhost/toolbelt"


def test_missing_url_raises():
    with pytest.raises(ConfigError):
        load_config({})


def test_blank_url_raises():
    with pytest.raises(ConfigError):
        load_config({"POSTGRES_URL": "   "})


def test_custom_schema():
    cfg = load_config(
        {"POSTGRES_URL": "postgresql://localhost/db", "TOOLBELT_SCHEMA": "tb_test"}
    )
    assert cfg.schema == "tb_test"


def test_invalid_schema_raises():
    with pytest.raises(ConfigError):
        load_config(
            {"POSTGRES_URL": "postgresql://localhost/db", "TOOLBELT_SCHEMA": "bad-schema"}
        )
