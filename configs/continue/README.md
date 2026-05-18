# Continue Configuration Templates

Reusable MCP configuration templates for Continue-compatible clients.

These templates are **starting points**, not generated output. The main
configuration path is `scripts/render_config.py`, which generates real MCP
server blocks from catalog `runtime` metadata.

## Templates

| Template | Profile | Intended use |
| --- | --- | --- |
| `base.readonly.yaml` | `readonly-research` | Read-only research and documentation |
| `sandbox.yaml` | `sandbox` | Evaluating experimental or unknown servers |
| `write-enabled.yaml` | `writer` | Workflows that need file or repo mutation |

Additional profiles (`local-inspect`, `local-dev`, `executor`,
`admin-controlled`) do not have hand-written templates; generate them with
`render_config.py`.

## Template format

```yaml
version: 1
profile: <profile-id>
mcpServers:
  <catalog-entry-id>:
    command: <command>
    args: []
    env: {}
```

- `profile` must be one of the seven profiles in
  [../../profiles/](../../profiles/).
- each key under `mcpServers` must match a catalog entry id under
  [../../catalog/servers/](../../catalog/servers/).
- generated entries are included only when the catalog entry has a `runtime`
  block.

## Important

A template's `mode` is declarative intent. It records how a server should be
used; it does not enforce that limit at runtime. See
[../../docs/REPOSITORY_PRINCIPLES.md](../../docs/REPOSITORY_PRINCIPLES.md),
Principle 11.

## Applying a template

See [../../docs/CONTINUE_SETUP.md](../../docs/CONTINUE_SETUP.md).
