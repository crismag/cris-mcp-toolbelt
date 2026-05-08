#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

status=0
for f in "$ROOT_DIR"/catalog/*.yaml; do
  [[ -f "$f" ]] || continue
  echo "Checking catalog entry: $(basename "$f")"
  if ! grep -q '^id:' "$f"; then
    echo "  [error] missing id"
    status=1
  fi
  if ! grep -q '^security_notes:' "$f"; then
    echo "  [error] missing security_notes"
    status=1
  fi
  if ! grep -q '^default_access:' "$f"; then
    echo "  [error] missing default_access"
    status=1
  fi
  if grep -qE '(secret|token|password)\s*:' "$f"; then
    echo "  [error] potential secret-like key found"
    status=1
  fi
done

if [[ $status -ne 0 ]]; then
  echo "MCP server tests failed." >&2
  exit 1
fi

echo "MCP server tests passed."
