# Getting Started

## 1) Clone and prepare

```bash
cp .env.example .env
```

## 2) Enable a workspace with read-only defaults

```bash
{PROJECT_ROOT}/scripts/enable_for_workspace.sh {TARGET_REPOSITORY} readonly-research
```

## 3) Run health checks

```bash
{PROJECT_ROOT}/scripts/doctor.sh
{PROJECT_ROOT}/scripts/test_mcp_servers.sh
python3 {PROJECT_ROOT}/scripts/validate_catalog.py
python3 {PROJECT_ROOT}/scripts/validate_profiles.py
```

## 4) Iterate safely

- Keep unknown servers in sandbox profile.
- Use write profile only when necessary.
- Document all new catalog entries with security notes.
