# Online MCP Usage Policy

`cris-mcp-toolbelt` may use online MCP servers only under controlled trust rules.

## Default Rule

Online MCP servers are treated as untrusted unless they are:

1. Officially maintained by a reputable provider, or
2. Used only for read-only/inward data retrieval of public or explicitly authorized data.

## Allowed by Default

- Public documentation lookup
- Public repository inspection
- Public web search
- Public URL fetching
- Read-only API calls with limited scopes
- Read-only metadata discovery

## Disabled by Default

- File write operations
- Shell execution
- Database mutations
- Email sending
- Calendar changes
- Git commits/pushes
- Issue/PR creation
- Cloud resource modification
- Any action using broad or admin tokens

## Sensitive Data Rule

Do not send private source code, credentials, customer data, church/member data, financial data, or production database content to unknown online MCP servers.

## Token Rule

Use separate tokens for MCP usage.

Prefer:

- read-only scopes
- short-lived tokens
- project-specific tokens
- dedicated OAuth apps
- environment variables

Never hardcode tokens inside repository files.
