#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

required=(
  "README.md"
  "CONTRIBUTING.md"
  "CODE_OF_CONDUCT.md"
  "SECURITY.md"
  ".env.example"
  "docs/SECURITY_MODEL.md"
  "profiles/readonly-research.profile.yaml"
  "catalog/trusted-retrieval.yaml"
)

missing=0
for file in "${required[@]}"; do
  if [[ ! -f "$ROOT_DIR/$file" ]]; then
    echo "[missing] $file"
    missing=1
  else
    echo "[ok] $file"
  fi
done

if [[ $missing -ne 0 ]]; then
  echo "Doctor failed: required files are missing." >&2
  exit 1
fi

echo "Doctor passed."
