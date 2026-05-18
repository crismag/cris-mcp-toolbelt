#!/usr/bin/env bash
# Enable cris-mcp-toolbelt for a target repository using a safety profile.
#
# Renders an MCP client configuration (via render_config.py) into the target
# repository's MCP config directory. render_config.py prints an activation
# summary and backs up any existing config before overwriting it.
#
# Usage:
#   enable_for_workspace.sh <target-repository> [profile]
#
# profile defaults to readonly-research. The MCP config directory defaults to
# .continue/mcpServers and can be overridden with the MCP_CONFIG_DIR env var.
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [[ $# -lt 1 || $# -gt 2 ]]; then
  echo "Usage: $0 <target-repository> [profile]" >&2
  exit 1
fi

TARGET_REPOSITORY="$1"
PROFILE="${2:-readonly-research}"
MCP_CONFIG_DIR="${MCP_CONFIG_DIR:-.continue/mcpServers}"

case "$PROFILE" in
  readonly-research|local-inspect|local-dev|sandbox|writer|executor|admin-controlled) ;;
  *)
    echo "Error: unsupported profile '$PROFILE'." >&2
    echo "Allowed: readonly-research, local-inspect, local-dev, sandbox, writer, executor, admin-controlled" >&2
    exit 1
    ;;
esac

if [[ ! -d "$TARGET_REPOSITORY" ]]; then
  echo "Error: target repository does not exist: $TARGET_REPOSITORY" >&2
  exit 1
fi

OUTPUT="$TARGET_REPOSITORY/$MCP_CONFIG_DIR/cris-mcp-toolbelt.yaml"

python3 "$ROOT_DIR/scripts/render_config.py" \
  --profile "$PROFILE" \
  --client continue \
  --output "$OUTPUT"

echo
echo "Enabled cris-mcp-toolbelt for '$TARGET_REPOSITORY' with profile '$PROFILE'."
