# Security Model

## Core principles

- Least privilege by default
- Explicit capability escalation
- Defense-in-depth via profile gating and catalog metadata

## Defaults

- Filesystem: path-restricted
- Database: read-only
- Online MCPs: trusted providers or inward/retrieval-only
- Unknown MCPs: sandbox only

## Write controls

Write actions are not enabled unless the selected profile explicitly allows them.
