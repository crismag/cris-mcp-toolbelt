# Security Policy

## Supported scope

This repository is documentation-first and safety-first for MCP tool configuration and workspace enablement.

## Reporting a vulnerability

Please report security issues privately to project maintainers. Include:

- Affected file(s)
- Impact and risk
- Reproduction steps
- Suggested mitigation

Do not publish exploit details until maintainers confirm remediation.

## Baseline controls

- Read-only defaults
- Profile-gated write capabilities
- Path-restricted local filesystem access
- Read-only database defaults
- Trusted-provider policy for online MCPs
- Unknown MCPs sandboxed by default
