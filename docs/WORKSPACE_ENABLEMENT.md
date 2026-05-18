# Workspace Enablement

Workspace enablement renders an MCP client configuration into a target
repository, using a selected safety profile. It is built on the configuration
renderer — see [Config rendering](#config-rendering) below.

## Quick command

```bash
{PROJECT_ROOT}/scripts/enable_for_workspace.sh {TARGET_REPOSITORY} <profile>
```

- `<profile>` is one of the seven profiles; it defaults to `readonly-research`.
- The output file is:

  ```text
  {TARGET_REPOSITORY}/{MCP_CONFIG_DIR}/cris-mcp-toolbelt.yaml
  ```

- `{MCP_CONFIG_DIR}` defaults to `.continue/mcpServers` and can be overridden
  with the `MCP_CONFIG_DIR` environment variable.

The script validates the profile and the target repository, then calls
`render_config.py` to render and write the config.

## Config rendering

`scripts/render_config.py` is the underlying tool. It can be used directly:

```bash
# Preview without writing anything
python3 scripts/render_config.py --profile local-dev --dry-run

# Render for a specific client to a file
python3 scripts/render_config.py --profile local-dev --client continue \
    --output {TARGET_REPOSITORY}/{MCP_CONFIG_DIR}/cris-mcp-toolbelt.yaml

# Render only specific catalog servers
python3 scripts/render_config.py --profile writer \
    --servers filesystem-controlled,git-controlled --dry-run
```

What it does:

1. Loads the chosen profile and the catalog.
2. Selects the catalog servers the profile may use — a server must list the
   profile in `allowed_profiles` and its `capability_class` must be in the
   profile's `allowed_capability_classes`. Specific servers can be chosen with
   `--servers`.
3. Prints an **activation summary**: the profile, its allowed capability
   classes, and every selected server with its capability class and mode.
4. Renders the configuration.
5. With `--dry-run`, prints the config and writes nothing.
6. Otherwise, **backs up** any existing target file to `<file>.bak` before
   writing.

## Safety behavior

- Unknown or unsupported profiles are rejected.
- Servers a profile is not permitted to use are excluded; requesting one
  explicitly with `--servers` is an error.
- An existing config is backed up before being overwritten.
- `--dry-run` allows previewing the result before any file is written.

## Important

The rendered profile and per-server modes are declarative intent. They record
how servers should be used; they are not enforced at runtime. See
[REPOSITORY_PRINCIPLES.md](REPOSITORY_PRINCIPLES.md), Principle 11.

## See also

- [CONTINUE_SETUP.md](CONTINUE_SETUP.md)
- [../configs/continue/README.md](../configs/continue/README.md)
- [../examples/generated-config-example.md](../examples/generated-config-example.md)
