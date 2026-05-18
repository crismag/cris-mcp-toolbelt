#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 || $# -gt 2 ]]; then
  echo "Usage: $0 <target-workspace> [profile]" >&2
  exit 1
fi

TARGET_WORKSPACE="$1"
PROFILE="${2:-readonly-research}"

case "$PROFILE" in
  readonly-research|sandbox|writer) ;;
  *)
    echo "Error: unsupported profile '$PROFILE'. Allowed: readonly-research, sandbox, writer" >&2
    exit 1
    ;;
esac

if [[ ! -d "$TARGET_WORKSPACE" ]]; then
  echo "Error: target workspace does not exist: $TARGET_WORKSPACE" >&2
  exit 1
fi

mkdir -p "$TARGET_WORKSPACE/.continue/mcpServers"
cat > "$TARGET_WORKSPACE/.continue/mcpServers/cris-mcp-toolbelt.yaml" <<CFG
version: 1
profile: $PROFILE
source: cris-mcp-toolbelt
placeholders:
  BASE_PATH: {BASE_PATH}
  WORKSPACE_ROOT: {WORKSPACE_ROOT}
  TOOLBELT_HOME: {TOOLBELT_HOME}
  TARGET_WORKSPACE: {TARGET_WORKSPACE}
mcpServers:
  - catalog_ref: filesystem-controlled
    default_access: read-only
    allowed_paths:
      - {TARGET_WORKSPACE}
CFG

echo "Enabled cris-mcp-toolbelt for '$TARGET_WORKSPACE' with profile '$PROFILE'"
echo "Wrote: $TARGET_WORKSPACE/.continue/mcpServers/cris-mcp-toolbelt.yaml"
