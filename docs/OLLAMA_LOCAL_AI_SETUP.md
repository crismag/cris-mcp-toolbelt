# Ollama Local AI Setup

`cris-mcp-toolbelt` supports local-first AI-assisted development. Local model
runtimes such as Ollama are one supported option — the toolbelt does not assume
or require any single runtime.

This page covers a local Ollama setup. For how Ollama fits with MCP servers see
[LOCAL_OLLAMA_MCP_STACK.md](LOCAL_OLLAMA_MCP_STACK.md); for assigning models to
tasks see [MODEL_ROUTING_GUIDE.md](MODEL_ROUTING_GUIDE.md).

## Why local-first

- Sensitive data stays on the local machine; no hosted AI provider is required.
- Model calls do not leave the network unless a workflow explicitly chooses an
  online MCP server.
- Local model runtimes pair well with the `local-inspect` and `local-dev`
  profiles.

## Prerequisites

- A local Ollama installation (or a compatible local runtime).
- One or more locally available models. The toolbelt does not mandate a
  specific model set — see [MODEL_ROUTING_GUIDE.md](MODEL_ROUTING_GUIDE.md) for
  example routing.
- An MCP-capable client (for example a Continue-compatible client).

## Configuration

The Ollama endpoint is referenced through the `{OLLAMA_BASE_URL}` placeholder.
Set it in your environment rather than hardcoding it:

```bash
cp .env.example .env
# then set OLLAMA_BASE_URL in .env
```

The `ollama-local` catalog entry
([catalog/servers/ollama-local.yaml](../catalog/servers/ollama-local.yaml))
describes the Ollama MCP server's capabilities and activation policy.

## Recommended profile

Start with `local-inspect` or `local-dev`:

- `local-inspect` — read-only inspection of a local workspace, no network.
- `local-dev` — controlled local development, including profile-gated writes.

Promote to `writer` or `executor` only when a workflow genuinely needs
modifying or executing capability.

## Safety notes for local model execution

- Local execution is not unrestricted. Profiles still gate filesystem,
  database, command, and network capability.
- Prompt content sent to a local model stays local, but is still data — do not
  rely on a local model to "see" secrets safely; keep secrets out of prompts.
- Model pull and delete are controlled actions on the `ollama-local` entry:
  pull requires confirmation, delete is disabled by default.
- Large models and generation can consume significant local resources; treat
  resource usage as a controlled capability.
