"""Safety guards for stored records.

The toolbelt memory store must never retain secrets, credentials, private
keys, or access tokens. These guards reject such records before they reach the
database. They are dependency-free and unit-tested.
"""

from __future__ import annotations

import re

# Record kinds that must never be stored.
BLOCKED_KINDS = {
    "secret",
    "secrets",
    "credential",
    "credentials",
    "private_key",
    "private-key",
    "privatekey",
    "access_token",
    "access-token",
    "accesstoken",
    "password",
    "api_key",
    "api-key",
    "apikey",
    "token",
}

# Patterns that indicate secret-like content.
_SECRET_PATTERNS = (
    re.compile(r"ghp_[A-Za-z0-9]{20,}"),
    re.compile(r"gho_[A-Za-z0-9]{20,}"),
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}"),
    re.compile(r"AIza[0-9A-Za-z_-]{30,}"),
)


class BlockedRecordError(ValueError):
    """Raised when a record may not be stored."""


def is_blocked_kind(kind: str) -> bool:
    """True if the record kind is one the store must refuse."""
    return kind.strip().lower() in BLOCKED_KINDS


def looks_like_secret(text: str) -> bool:
    """True if the text contains a recognizable secret-like token."""
    return any(pattern.search(text) for pattern in _SECRET_PATTERNS)


def assert_storable(kind: str, content: str) -> None:
    """Raise BlockedRecordError if a record may not be stored.

    A record is rejected when its kind is a blocked kind, or when its content
    contains a recognizable secret-like token.
    """
    if is_blocked_kind(kind):
        raise BlockedRecordError(
            f"record kind '{kind}' is blocked; this store does not retain "
            f"secrets, credentials, private keys, or access tokens"
        )
    if looks_like_secret(content):
        raise BlockedRecordError(
            "record content looks like a secret or credential; it will not "
            "be stored"
        )
