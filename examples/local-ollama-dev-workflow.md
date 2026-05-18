# Example: Local Ollama Development Workflow

A worked example of using `cris-mcp-toolbelt` with local Ollama models for
day-to-day development. It uses placeholders only and assumes no specific
machine.

## Goal

Implement a small feature in a local repository with AI assistance, while
keeping capability profile-gated.

## Setup

1. Set the Ollama endpoint in the environment:

   ```bash
   cp .env.example .env
   # set OLLAMA_BASE_URL in .env
   ```

2. Enable the workspace with the `local-dev` profile:

   ```bash
   {PROJECT_ROOT}/scripts/enable_for_workspace.sh {TARGET_REPOSITORY} local-dev
   ```

3. The `local-dev` profile exposes passive, interactive, and profile-gated
   modifying capability. Filesystem writes are scoped to `{WORKSPACE_ROOT}`,
   database access is read-only, and command execution is disabled.

## The stack

This workflow uses these catalog servers (see
[../docs/LOCAL_OLLAMA_MCP_STACK.md](../docs/LOCAL_OLLAMA_MCP_STACK.md)):

- `sequential-thinking` — planning
- `filesystem-controlled` — read and gated write of workspace files
- `git-controlled` — inspect history, draft commits
- `memory-local` — recall project context
- `public-fetch` — retrieve public documentation
- `ollama-local` — local model access

## Steps

1. **Plan.** Use a planning model (for example `qwen2.5:14b`) with
   `sequential-thinking` to break the feature into steps. See
   [../docs/MODEL_ROUTING_GUIDE.md](../docs/MODEL_ROUTING_GUIDE.md).

2. **Understand the code.** Use `filesystem-controlled` (inspect mode) and
   `git-controlled` (status, diff, log) so the model can read the relevant
   files and recent history.

3. **Recall context.** Use `memory-local` to retrieve project conventions and
   accepted decisions from previous sessions.

4. **Implement.** Use a coding model (for example `qwen2.5-coder:14b`) to draft
   changes. Writing files is a profile-gated modifying action: under
   `local-dev` it requires confirmation and is audited.

5. **Check public guidance.** Use `public-fetch` to confirm current API or
   library documentation if needed.

6. **Run validation (optional).** Running tests and linters is an executing
   capability. To run them through an MCP server, re-enable the workspace with
   the `executor` profile, which permits allowlisted command execution.

7. **Draft a commit.** Use `git-controlled` to draft a commit summary from the
   diff. Creating the commit is a profile-gated action.

## What stays controlled

- File writes, commits, and command execution are never automatic — the model
  proposes them; activation is an intentional, confirmed, audited step.
- Switching from `local-dev` to `executor` or `writer` is a deliberate profile
  change, visible in the workspace config.
- No data leaves the machine unless a workflow explicitly uses an online MCP
  server.

## See also

- [../docs/OLLAMA_LOCAL_AI_SETUP.md](../docs/OLLAMA_LOCAL_AI_SETUP.md)
- [../docs/LOCAL_OLLAMA_MCP_STACK.md](../docs/LOCAL_OLLAMA_MCP_STACK.md)
- [../docs/MODEL_ROUTING_GUIDE.md](../docs/MODEL_ROUTING_GUIDE.md)
- [profile-selection.md](profile-selection.md)
