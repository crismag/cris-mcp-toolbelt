# Local Ollama MCP Stack

This page describes how a local Ollama setup combines with MCP servers from the
catalog to support local-first AI-assisted development.

## The idea

A local model on its own can reason about code you paste into it. With MCP
servers, the same local model can also inspect files, read git history, recall
project context, fetch public documentation, and run validation — all under
profile-gated capability control.

The "stack" is therefore: a **local model runtime** (Ollama) + a set of
**catalog MCP servers** + a **profile** that decides how much capability those
servers may expose.

## A local development stack

For everyday local development, a practical stack is:

| Layer | Catalog entry | Capability class | Role |
| --- | --- | --- | --- |
| Reasoning | `sequential-thinking` | passive | Planning and decomposition |
| Files | `filesystem-controlled` | modifying | Read and (gated) write workspace files |
| Source control | `git-controlled` | modifying | Inspect and (gated) commit |
| Memory | `memory-local` | modifying | Persist project context and decisions |
| Documentation | `public-fetch` | interactive | Retrieve public technical docs |
| Local models | `ollama-local` | modifying | List, inspect, and run local models |

This stack maps cleanly onto the `local-dev` profile: passive and interactive
capability is available; modifying capability is profile-gated, confirmed, and
audited.

## How local models use the tools

A local model working under the `local-dev` profile can:

- **Read files** through `filesystem-controlled` (inspect mode by default) to
  understand a codebase before suggesting changes.
- **Review history** through `git-controlled` — status, diff, and log — to see
  what changed and draft commit summaries.
- **Recall context** through `memory-local` — project conventions, accepted
  decisions, and known TODOs persist across sessions.
- **Fetch public docs** through `public-fetch` to check current, accurate
  technical guidance.
- **Run validation** through a command-execution server (when an `executor`
  profile is selected) to run tests and linters.

Writes, commits, and command execution remain profile-gated: the model can
*propose* them, but activation is an intentional, audited step.

## Choosing a profile for the stack

| Goal | Profile |
| --- | --- |
| Understand a codebase, no changes | `local-inspect` |
| Day-to-day development with gated writes | `local-dev` |
| Apply file or repository changes | `writer` |
| Run tests, linters, and validators | `executor` |
| Try an unreviewed MCP server | `sandbox` |

## Safety notes

- The stack does not change the safety model: profiles and activation policy
  still apply, and they remain declarative intent rather than runtime
  enforcement.
- Keep secrets out of prompts and out of files the model can read; the
  `filesystem-controlled` entry blocks common sensitive paths, but prompt
  hygiene is still the user's responsibility.
- `ollama-local` model pull and delete are controlled actions — see
  [MODEL_ROUTING_GUIDE.md](MODEL_ROUTING_GUIDE.md).

## See also

- [OLLAMA_LOCAL_AI_SETUP.md](OLLAMA_LOCAL_AI_SETUP.md) — setting up Ollama.
- [MODEL_ROUTING_GUIDE.md](MODEL_ROUTING_GUIDE.md) — assigning models to tasks.
- [../examples/local-ollama-dev-workflow.md](../examples/local-ollama-dev-workflow.md)
  — a worked example.
