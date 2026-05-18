#!/usr/bin/env python3
"""Render an MCP client configuration from a profile and catalog entries.

Given a safety profile, this script selects the catalog servers that profile
may use, derives each server's mode, and renders a client configuration. It
prints an activation summary, supports a dry run, and backs up an existing
target file before overwriting it.

Requires: PyYAML.

Examples:
  python3 scripts/render_config.py --profile readonly-research --dry-run
  python3 scripts/render_config.py --profile local-dev --client continue \\
      --output {TARGET_REPOSITORY}/{MCP_CONFIG_DIR}/cris-mcp-toolbelt.yaml
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    print("error: PyYAML is required (pip install pyyaml)", file=sys.stderr)
    raise SystemExit(2) from None

ROOT = Path(__file__).resolve().parents[1]


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


def select_servers(
    catalog: dict[str, dict], profile: dict, requested: list[str] | None
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
            selected.append(catalog[sid])
        return selected
    return [e for e in catalog.values() if entry_allowed(e, profile)]


def render(profile: dict, servers: list[dict], client: str) -> dict:
    """Build the rendered configuration mapping."""
    mcp_servers = [
        {
            "ref": s["id"],
            "capability_class": s["capability_class"],
            "mode": s["default_access"],
        }
        for s in servers
    ]
    return {
        "version": 1,
        "generated_by": "cris-mcp-toolbelt render_config.py",
        "client": client,
        "profile": profile["id"],
        "mcpServers": mcp_servers,
    }


def validate_rendered(config: dict, catalog: dict[str, dict]) -> list[str]:
    """Minimal self-check of the rendered configuration."""
    errors: list[str] = []
    for server in config["mcpServers"]:
        if server["ref"] not in catalog:
            errors.append(f"rendered ref '{server['ref']}' not in catalog")
        if not server.get("mode"):
            errors.append(f"rendered server '{server['ref']}' has no mode")
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
        choices=["continue", "generic"],
        default="generic",
        help="Target client format.",
    )
    parser.add_argument(
        "--servers",
        help="Comma-separated catalog server ids. Default: all the profile allows.",
    )
    parser.add_argument("--output", help="Path to write the rendered config.")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the rendered config and never write a file.",
    )
    args = parser.parse_args()

    profile = load_profile(args.profile)
    catalog = load_catalog()
    requested = [s.strip() for s in args.servers.split(",")] if args.servers else None
    servers = select_servers(catalog, profile, requested)

    config = render(profile, servers, args.client)
    errors = validate_rendered(config, catalog)
    if errors:
        for err in errors:
            print(f"error: {err}", file=sys.stderr)
        return 1

    print_summary(profile, servers)
    print()

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
