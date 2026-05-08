# Getting Started

## 1) Clone and prepare

```bash
cp .env.example .env
```

## 2) Enable a workspace with read-only defaults

```bash
{TOOLBELT_HOME}/scripts/enable_for_workspace.sh {TARGET_WORKSPACE} readonly-research
```

## 3) Run health checks

```bash
{TOOLBELT_HOME}/scripts/doctor.sh
{TOOLBELT_HOME}/scripts/test_mcp_servers.sh
python3 {TOOLBELT_HOME}/scripts/validate_catalog.py
```

## 4) Iterate safely

- Keep unknown servers in sandbox profile.
- Use write profile only when necessary.
- Document all new catalog entries with security notes.
