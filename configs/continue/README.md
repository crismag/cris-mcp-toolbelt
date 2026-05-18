# Continue Configuration Templates

Reusable MCP configuration templates for Continue-compatible clients.

These templates are **starting points**, not generated output. Each references
a profile and lists catalog entries by `ref`. A future config renderer
(`render_config.py`, planned) will generate configs from a profile plus
selected catalog entries; until then, copy and adapt a template by hand.

## Templates

| Template | Profile | Intended use |
| --- | --- | --- |
| `base.readonly.yaml` | `readonly-research` | Read-only research and documentation |
| `sandbox.yaml` | `sandbox` | Evaluating experimental or unknown servers |
| `write-enabled.yaml` | `writer` | Workflows that need file or repo mutation |

Additional profiles (`local-inspect`, `local-dev`, `executor`,
`admin-controlled`) do not yet have templates; adapt the closest existing one.

## Template format

```yaml
version: 1
profile: <profile-id>
mcpServers:
  - ref: <catalog-entry-id>
    mode: <read-only | read-write | restricted>
```

- `profile` must be one of the seven profiles in
  [../../profiles/](../../profiles/).
- each `ref` must match a catalog entry id under
  [../../catalog/servers/](../../catalog/servers/).
- `mode` must not exceed what the referenced profile allows.

## Important

A template's `mode` is declarative intent. It records how a server should be
used; it does not enforce that limit at runtime. See
[../../docs/REPOSITORY_PRINCIPLES.md](../../docs/REPOSITORY_PRINCIPLES.md),
Principle 11.

## Applying a template

See [../../docs/CONTINUE_SETUP.md](../../docs/CONTINUE_SETUP.md).
