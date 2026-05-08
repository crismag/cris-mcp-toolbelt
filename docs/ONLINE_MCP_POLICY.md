# Online MCP Policy

Online MCP servers must satisfy one of:

1. Trusted provider with strong security posture
2. Inward/retrieval-only capabilities with no write operations by default

Policy requirements:

- Document provider metadata
- Document data handling expectations
- Restrict default permissions to read-only
- Gate elevated scopes behind explicit write-enabled profiles
