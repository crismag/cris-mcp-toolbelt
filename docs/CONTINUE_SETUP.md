# Continue Setup

How to set up MCP servers for a Continue-compatible client using a profile.

## Steps

1. **Pick a profile.** One of the seven profiles in
   [../profiles/](../profiles/): `readonly-research`, `local-inspect`,
   `local-dev`, `sandbox`, `writer`, `executor`, or `admin-controlled`. Start
   with the most conservative profile that still does the job.

2. **Enable the workspace.** Run the workspace enablement script:

   ```bash
   {PROJECT_ROOT}/scripts/enable_for_workspace.sh {TARGET_REPOSITORY} <profile>
   ```

3. **Or render directly.** For Continue output with real MCP server blocks:

   ```bash
   python3 scripts/render_config.py \
     --profile local-dev \
     --client continue \
     --workspace-root {TARGET_REPOSITORY} \
     --output {TARGET_REPOSITORY}/{MCP_CONFIG_DIR}/cris-mcp-toolbelt.yaml
   ```

   Preview first with `--dry-run`.

4. **Open the generated Continue MCP config** in the target repository:

   ```text
   {TARGET_REPOSITORY}/{MCP_CONFIG_DIR}/cris-mcp-toolbelt.yaml
   ```

5. **Review it.** Confirm only the expected servers are enabled.

## Templates

Reusable templates live in [../configs/continue/](../configs/continue/). See
[../configs/continue/README.md](../configs/continue/README.md) for the template
format and which profile each template targets.

## Local Ollama workflows

To combine a Continue-compatible client with local Ollama models, see
[OLLAMA_LOCAL_AI_SETUP.md](OLLAMA_LOCAL_AI_SETUP.md) and
[LOCAL_OLLAMA_MCP_STACK.md](LOCAL_OLLAMA_MCP_STACK.md). For the command-runner
feedback loop, see
[USE_WITH_LOCAL_OLLAMA_CODING_ASSISTANT.md](USE_WITH_LOCAL_OLLAMA_CODING_ASSISTANT.md).

## Note

The profile and catalog scope controls are declarative intent. They describe
how servers should be used; runtime enforcement belongs to the MCP server and
client.
