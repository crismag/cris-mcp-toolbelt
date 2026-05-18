"""PostgreSQL-backed memory and audit MCP server for cris-mcp-toolbelt.

This is a first-party MCP server. It exposes a small set of tools for storing
and retrieving project memory and audit events in a toolbelt-owned PostgreSQL
schema. It writes only to that schema and refuses to store secret-like records.
"""

__version__ = "0.0.1"
