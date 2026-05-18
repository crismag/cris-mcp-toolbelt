"""Tests for the record-safety guards."""

from __future__ import annotations

import pytest

from toolbelt_postgres_memory.safety import (
    BlockedRecordError,
    assert_storable,
    is_blocked_kind,
    looks_like_secret,
)


@pytest.mark.parametrize("kind", ["secret", "Credential", "ACCESS_TOKEN", "api-key"])
def test_blocked_kinds_are_blocked(kind):
    assert is_blocked_kind(kind)


@pytest.mark.parametrize("kind", ["decision", "convention", "note", "todo"])
def test_normal_kinds_are_allowed(kind):
    assert not is_blocked_kind(kind)


@pytest.mark.parametrize(
    "text",
    [
        "ghp_" + "a" * 30,
        "sk-" + "b" * 30,
        "AKIA" + "C" * 16,
        "-----BEGIN RSA PRIVATE KEY-----",
    ],
)
def test_secret_like_content_is_detected(text):
    assert looks_like_secret(text)


def test_ordinary_content_is_not_flagged():
    assert not looks_like_secret("The login flow uses a session cookie.")


def test_assert_storable_rejects_blocked_kind():
    with pytest.raises(BlockedRecordError):
        assert_storable("password", "anything")


def test_assert_storable_rejects_secret_content():
    with pytest.raises(BlockedRecordError):
        assert_storable("note", "token is ghp_" + "x" * 30)


def test_assert_storable_allows_normal_record():
    # Should not raise.
    assert_storable("decision", "We chose PostgreSQL for the memory backend.")
