# Model Routing Guide

Different development tasks suit different local models. Model routing means
assigning each task type to the model best suited for it, instead of using one
model for everything.

This guide gives **example** routing. It is not a requirement: the toolbelt
does not mandate any model set, and any locally available models can be used.

## Why route by role

- Coding-specialized models handle code generation and refactoring better than
  general models.
- General reasoning models handle planning and architecture discussion better
  than narrow coding models.
- Embedding models are needed for retrieval, not generation.
- Smaller models give faster turnaround for quick utility tasks.

## Example role mapping

The following is an example roster for a local Ollama setup. Substitute the
models available in your own environment.

| Role | Example model | Use for |
| --- | --- | --- |
| Coding and refactor | `qwen2.5-coder:14b` | Implementation, refactoring, code review |
| Planning and reasoning | `qwen2.5:14b` | Task planning, general reasoning |
| Architecture and deep reasoning | `cogito:14b` | Architecture, design trade-offs, migrations |
| Writing and documentation | `gemma4:latest` | Docs, summaries, review notes |
| Fast coding utilities | `deepseek-coder:latest` | Quick snippets, small edits |
| Embeddings and retrieval | `nomic-embed-text:latest` | Indexing, retrieval support |

## Mapping roles to tasks

| Task | Suggested role |
| --- | --- |
| Plan a feature before implementation | Planning and reasoning |
| Decompose a complex refactor | Architecture and deep reasoning |
| Write or refactor code | Coding and refactor |
| Draft commit messages or release notes | Writing and documentation |
| Quick one-off code utility | Fast coding utilities |
| Build a retrieval index over docs | Embeddings and retrieval |

## Routing and the MCP stack

Model routing pairs naturally with the local MCP stack
([LOCAL_OLLAMA_MCP_STACK.md](LOCAL_OLLAMA_MCP_STACK.md)):

1. Use a planning or architecture model with `sequential-thinking` to plan.
2. Use a coding model with `filesystem-controlled` and `git-controlled` to
   implement under the `local-dev` profile.
3. Use a writing model with `public-fetch` and `memory-local` to document
   decisions.
4. Use an embeddings model with retrieval workflows.

## Safety notes

- Routing is a productivity choice and does not change the safety model.
  Profiles still gate capability regardless of which model is selected.
- Model `pull` and `delete` through the `ollama-local` entry are controlled
  capabilities: `pull` requires confirmation, `delete` is disabled by default.
- A larger model does not earn broader capability — capability is set by the
  profile, not the model.
