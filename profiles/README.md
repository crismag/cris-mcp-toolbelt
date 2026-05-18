# Profiles

A profile is a named safety profile that controls how much capability an MCP
server is allowed to expose. Capability is granted by selecting a profile — not
by editing scattered configuration flags.

## Layout

- `schema.json` — JSON Schema for a profile file.
- `<id>.profile.yaml` — one file per profile.

## The seven profiles

| Profile | Intent | Highest class | Unknown MCP |
| --- | --- | --- | --- |
| `readonly-research` | Public documentation and read-only research | interactive | no |
| `local-inspect` | Local workspace and repository inspection only | passive | no |
| `local-dev` | Controlled local development assistance | modifying | no |
| `sandbox` | Experimental or unknown MCP servers in limited scope | interactive | yes |
| `writer` | Explicit file, database, or repo mutation | modifying | no |
| `executor` | Controlled command execution with allowlists | executing | no |
| `admin-controlled` | High-impact operations, explicitly configured | administrative | no |

## Profile fields

Each profile declares: `id`, `name`, `description`, `intent`,
`allow_unknown_mcp`, `allowed_capability_classes`, `filesystem`, `database`,
`command_execution`, `network`, `write_actions`, `activation_defaults`, and
`notes`. See [schema.json](schema.json) for allowed values.

## Capability classes

A profile's `allowed_capability_classes` lists which capability classes it may
expose: `passive`, `interactive`, `modifying`, `executing`, `administrative`.
A profile must declare any class implied by its settings — for example a
`read-write` filesystem mode requires the `modifying` class.

## Conservative defaults

- `readonly-research` and `local-inspect` expose no modifying, executing, or
  administrative capability.
- `allow_unknown_mcp` is `true` only for `sandbox`.
- `writer`, `executor`, and `admin-controlled` are intentional choices, never
  defaults.

## Validation

```bash
python3 scripts/validate_profiles.py
```

This validates every `*.profile.yaml` against `schema.json` and applies
cross-field consistency checks.
