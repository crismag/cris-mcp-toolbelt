#!/usr/bin/env python3
"""Render an MCP client configuration from a profile and catalog entries.

Given a safety profile, this script selects the catalog servers that profile
may use and renders real MCP client server blocks from each entry's runtime
metadata. It prints an activation summary, supports a dry run, and backs up an
existing target file before overwriting it.

Requires: PyYAML.

Examples:
  python3 scripts/render_config.py --profile readonly-research --dry-run
  python3 scripts/render_config.py --profile local-dev --client claude-desktop \\
      --output {TARGET_REPOSITORY}/{MCP_CONFIG_DIR}/cris-mcp-toolbelt.yaml
"""

from __future__ import annotations

import argparse
import copy
import json
import os
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    print("error: PyYAML is required (pip install pyyaml)", file=sys.stderr)
    raise SystemExit(2) from None

ROOT = Path(__file__).resolve().parents[1]
PLACEHOLDER_RE = re.compile(r"\{[A-Z0-9_]+\}")


def load_profile(profile_id: str) -> dict:
    path = ROOT / "profiles" / f"{profile_id}.profile.yaml"
    if not path.exists():
        raise SystemExit(f"error: unknown profile '{profile_id}' ({path} not found)")
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def load_catalog() -> dict[str, dict]:
    servers_dir = ROOT / "catalog" / "servers"
    if not servers_dir.exists():
        raise SystemExit("error: catalog/servers directory not found")
    entries: dict[str, dict] = {}
    for file in sorted(servers_dir.glob("*.yaml")):
        entry = yaml.safe_load(file.read_text(encoding="utf-8"))
        if isinstance(entry, dict) and entry.get("id"):
            entries[entry["id"]] = entry
    return entries


def entry_allowed(entry: dict, profile: dict) -> bool:
    """True if the profile may use this catalog entry.

    Selection is gated on allowed_profiles membership only. A server's
    capability_class is its ceiling, not its default — a write-capable server
    can still be used read-only by a lower-tier profile. Which capability a
    profile may *activate* is governed by activation_policy and policy linting,
    not by config rendering.
    """
    return profile["id"] in (entry.get("allowed_profiles") or [])


def entry_renderable(entry: dict) -> bool:
    """True when the catalog entry has a client-renderable runtime block."""
    runtime = entry.get("runtime")
    return isinstance(runtime, dict) and bool(runtime.get("command"))


def select_servers(
    catalog: dict[str, dict],
    profile: dict,
    requested: list[str] | None,
    require_runtime: bool,
) -> list[dict]:
    """Select catalog entries to render, validating each against the profile."""
    if requested:
        selected = []
        for sid in requested:
            if sid not in catalog:
                raise SystemExit(f"error: unknown catalog server '{sid}'")
            if not entry_allowed(catalog[sid], profile):
                raise SystemExit(
                    f"error: server '{sid}' is not permitted by profile "
                    f"'{profile['id']}'"
                )
            if require_runtime and not entry_renderable(catalog[sid]):
                raise SystemExit(
                    f"error: server '{sid}' has no runtime command yet and "
                    "cannot be rendered into a client config"
                )
            selected.append(catalog[sid])
        return selected
    selected = [e for e in catalog.values() if entry_allowed(e, profile)]
    if require_runtime:
        selected = [e for e in selected if entry_renderable(e)]
    return selected


def runtime_block(entry: dict) -> dict:
    """Return the MCP runtime block clients expect."""
    runtime = copy.deepcopy(entry["runtime"])
    block = {
        "command": runtime["command"],
        "args": runtime.get("args") or [],
    }
    env = runtime.get("env") or {}
    if env:
        block["env"] = env
    return block


def substitute_placeholders(value: object, placeholders: dict[str, str]) -> object:
    """Recursively substitute known placeholders in rendered runtime values."""
    if isinstance(value, str):
        for key, replacement in placeholders.items():
            value = value.replace("{" + key + "}", replacement)
        return value
    if isinstance(value, list):
        return [substitute_placeholders(item, placeholders) for item in value]
    if isinstance(value, dict):
        return {
            key: substitute_placeholders(item, placeholders)
            for key, item in value.items()
        }
    return value


def unresolved_placeholders(value: object) -> list[str]:
    """Return unresolved placeholder tokens in a rendered value."""
    found: list[str] = []
    if isinstance(value, str):
        found.extend(PLACEHOLDER_RE.findall(value))
    elif isinstance(value, list):
        for item in value:
            found.extend(unresolved_placeholders(item))
    elif isinstance(value, dict):
        for item in value.values():
            found.extend(unresolved_placeholders(item))
    return sorted(set(found))


def governance_summary(profile: dict, servers: list[dict], client: str) -> dict:
    """Build the abstract governance summary format."""
    return {
        "version": 1,
        "generated_by": "cris-mcp-toolbelt render_config.py",
        "client": client,
        "profile": profile["id"],
        "mcpServers": [
            {
                "ref": s["id"],
                "capability_class": s["capability_class"],
                "mode": s["default_access"],
            }
            for s in servers
        ],
    }


def render(
    profile: dict, servers: list[dict], client: str, placeholders: dict[str, str]
) -> dict:
    """Build the rendered client configuration mapping."""
    if client in {"generic", "generic-yaml", "generic-json"}:
        return governance_summary(profile, servers, client)

    mcp_servers = {
        s["id"]: substitute_placeholders(runtime_block(s), placeholders)
        for s in servers
    }

    if client in {"continue", "claude-desktop", "claude-code"}:
        return {"mcpServers": mcp_servers}

    return {"mcpServers": mcp_servers}


def validate_rendered(config: dict, catalog: dict[str, dict]) -> list[str]:
    """Minimal self-check of the rendered configuration."""
    errors: list[str] = []
    servers = config["mcpServers"]
    if isinstance(servers, list):
        for server in servers:
            if server["ref"] not in catalog:
                errors.append(f"rendered ref '{server['ref']}' not in catalog")
        return errors
    for server_id, server in servers.items():
        if server_id not in catalog:
            errors.append(f"rendered server '{server_id}' not in catalog")
        if not server.get("command"):
            errors.append(f"rendered server '{server_id}' has no command")
        if "args" not in server:
            errors.append(f"rendered server '{server_id}' has no args")
    return errors


def print_summary(profile: dict, servers: list[dict]) -> None:
    print(f"Activation summary — profile: {profile['id']}")
    print(f"  intent: {profile.get('description', '').strip()}")
    print(f"  allowed capability classes: "
          f"{', '.join(profile.get('allowed_capability_classes', []))}")
    print(f"  write actions: {profile.get('write_actions')}")
    print(f"  servers selected: {len(servers)}")
    for s in servers:
        controlled = s.get("controlled_capabilities") or []
        note = f" (controlled: {len(controlled)})" if controlled else ""
        print(f"    - {s['id']}  [{s['capability_class']}]  "
              f"mode={s['default_access']}{note}")
    print("  note: activation policy and scope controls are declarative "
          "intent, not runtime enforcement.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--profile", required=True, help="Profile id.")
    parser.add_argument(
        "--client",
        choices=[
            "continue",
            "claude-desktop",
            "claude-code",
            "generic",
            "generic-yaml",
            "generic-json",
        ],
        default="generic-yaml",
        help="Target client format.",
    )
    parser.add_argument(
        "--servers",
        help="Comma-separated catalog server ids. Default: all the profile allows.",
    )
    parser.add_argument("--output", help="Path to write the rendered config.")
    parser.add_argument(
        "--workspace-root",
        help="Workspace path used to replace {WORKSPACE_ROOT}.",
    )
    parser.add_argument(
        "--allow-unresolved-placeholders",
        action="store_true",
        help="Allow unresolved placeholders in rendered runtime configs.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the rendered config and never write a file.",
    )
    args = parser.parse_args()

    profile = load_profile(args.profile)
    catalog = load_catalog()
    client = "generic-yaml" if args.client == "generic" else args.client
    requested = [s.strip() for s in args.servers.split(",")] if args.servers else None
    require_runtime = client not in {"generic-yaml", "generic-json"}
    servers = select_servers(catalog, profile, requested, require_runtime)
    workspace_root = str(Path(args.workspace_root).resolve()) if args.workspace_root else ""
    placeholders = {
        "PROJECT_ROOT": str(ROOT),
        "WORKSPACE_ROOT": workspace_root,
        "TARGET_REPOSITORY": workspace_root,
        "USER_HOME": str(Path.home()),
        "MCP_CONFIG_DIR": os.environ.get("MCP_CONFIG_DIR", ".continue/mcpServers"),
        "DATABASE_URL": os.environ.get("DATABASE_URL", ""),
        "POSTGRES_URL": os.environ.get("POSTGRES_URL", ""),
        "MYSQL_URL": os.environ.get("MYSQL_URL", ""),
        "OLLAMA_BASE_URL": os.environ.get("OLLAMA_BASE_URL", ""),
        "GITHUB_TOKEN": os.environ.get("GITHUB_TOKEN", ""),
    }
    placeholders = {key: value for key, value in placeholders.items() if value}

    config = render(profile, servers, client, placeholders)
    errors = validate_rendered(config, catalog)
    unresolved = unresolved_placeholders(config)
    required_unresolved = [
        item for item in unresolved if item in {"{WORKSPACE_ROOT}", "{PROJECT_ROOT}", "{USER_HOME}"}
    ]
    if unresolved and client not in {"generic-yaml", "generic-json"}:
        if required_unresolved and not args.allow_unresolved_placeholders:
            errors.append(
                "unresolved placeholders: "
                + ", ".join(required_unresolved)
                + " (pass --allow-unresolved-placeholders to keep them)"
            )
    if errors:
        for err in errors:
            print(f"error: {err}", file=sys.stderr)
        return 1

    print_summary(profile, servers)
    print()

    if client in {"claude-desktop", "claude-code", "generic-json"}:
        rendered = json.dumps(config, indent=2) + "\n"
    else:
        header = (
            "# Generated by cris-mcp-toolbelt render_config.py — do not edit by hand.\n"
            "# Regenerate with render_config.py to change.\n"
        )
        rendered = f"{header}{yaml.safe_dump(config, sort_keys=False)}"

    if args.dry_run or not args.output:
        print("--- rendered config ---")
        print(rendered, end="")
        if args.dry_run:
            print("--- dry run: no file written ---")
        return 0

    target = Path(args.output)
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        backup = target.with_suffix(target.suffix + ".bak")
        backup.write_text(target.read_text(encoding="utf-8"), encoding="utf-8")
        print(f"backed up existing config to {backup}")
    target.write_text(rendered, encoding="utf-8")
    print(f"wrote {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
