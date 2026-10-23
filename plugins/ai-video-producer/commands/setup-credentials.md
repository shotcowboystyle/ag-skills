---
description: One-time setup for fal.ai, Replicate, WaveSpeed, and MiniMax credentials, plus runner toolchain bootstrap. Writes ~/.config/ai-video-producer/.env, sources it from the user's shell profile, and installs the npm + pip dependencies needed by the SDK runners in the provider-runners skill.
---

Set up persistent credentials for the bundled MCP servers (fal.ai, Replicate, MiniMax) and SDK runners (fal-js, WaveSpeed Python), then bootstrap the runner toolchains.

## Steps

1. Check if `~/.config/ai-video-producer/.env` already exists.
   - If yes, list only the key names that have a value, without loading values into the conversation: `grep -oE '^[A-Z_]+=.' ~/.config/ai-video-producer/.env | cut -d= -f1`. Ask the user if they want to update any.
   - If no, create the directory: `mkdir -p ~/.config/ai-video-producer`.

2. Prompt the user for each missing value:
   - `FAL_KEY` — fal.ai API key (https://fal.ai/dashboard/keys). Used by the hosted MCP server at `https://mcp.fal.ai/mcp` **and** by the `fal_run.mjs` runner.
   - `REPLICATE_API_TOKEN` — Replicate API token (https://replicate.com/account/api-tokens). Used by the local `replicate-mcp` npm package.
   - `WAVESPEED_API_KEY` — WaveSpeedAI key (https://wavespeed.ai/accesskey). Used by the `wavespeed_run.py` runner.
   - `MINIMAX_API_KEY` — MiniMax key. Used by the bundled `minimax-mcp` server. Region matters: Global keys come from https://www.minimax.io/platform/user-center/basic-information/interface-key, Mainland from https://platform.minimaxi.com/user-center/basic-information/interface-key.
   - `MINIMAX_API_HOST` — `https://api.minimax.io` (Global) or `https://api.minimaxi.com` (Mainland). Must match the key region or the MCP returns "Invalid API key".
   - `MINIMAX_MCP_BASE_PATH` — local output directory MiniMax should write generated media into (default: `$HOME/Videos/minimax`).
   - `MINIMAX_API_RESOURCE_MODE` — `url` (default) or `local`.

   Accept blank to skip a key. Each provider degrades independently (skipping `WAVESPEED_API_KEY` just means the wavespeed runner won't work; skipping `MINIMAX_API_KEY` disables the minimax MCP).

3. Write `~/.config/ai-video-producer/.env` with `KEY=value` lines. Mode `600`.

4. Ensure the env loader is in the user's shell profile. Detect the shell from `$SHELL` (default `~/.bashrc`; for zsh use `~/.zshrc`). The loader line:

   ```
   # AI Video Producer credentials
   [ -f "$HOME/.config/ai-video-producer/.env" ] && set -a && . "$HOME/.config/ai-video-producer/.env" && set +a
   ```

   - If the line is already present, do nothing.
   - If not, append it. Tell the user to either start a new shell or `source` their profile to pick up the values for the current session.

5. Verify by running (in a subshell that sources the profile):
   ```
   bash -lc 'for k in FAL_KEY REPLICATE_API_TOKEN WAVESPEED_API_KEY MINIMAX_API_KEY MINIMAX_API_HOST; do v="${!k}"; echo "$k: ${v:+set}${v:-MISSING}"; done'
   ```
   Report which are `set` and which are `MISSING`. Do not print the actual key values.

6. **Bootstrap runner toolchains.** The SDK runners need their own deps installed once per machine. They live in this plugin's `provider-runners` skill folder (find the installed folder by name; some tools prefix it, e.g. `ai-video-producer__provider-runners`). Work from that folder and:

   - **fal-js**: `npm install` — installs `@fal-ai/client` for `fal_run.mjs`. Skip if `node_modules/@fal-ai/client` already exists.
   - **WaveSpeed Python**: prefer a venv. Check for `.venv`; if absent, create with `python3 -m venv .venv`. Then `.venv/bin/pip install -r requirements.txt`. If the user has a global preference for `pipx`/system pip, ask before creating the venv.

   Skip whichever toolchain corresponds to a key the user left blank.

7. Tell the user how to confirm the runners work:
   ```
   node fal_run.mjs 2>&1 | head -3              # should print usage
   .venv/bin/python wavespeed_run.py --help     # should print usage
   ```

8. Remind the user that:
   - The coding agent reads env vars from the process it inherits — so any new agent session started from a shell that has sourced `.env` will see the keys.
   - To use the keys *right now* in this session, the user can either restart the agent from a fresh shell, or export the values manually for the current process.
   - The bundled `.mcp.json` is loaded automatically by Claude Code (and Cursor). In other tools, register the same three servers in that tool's MCP config; the provider-runners scripts work everywhere without MCP.
   - The MiniMax MCP runs via `uvx`; if `uvx` isn't on PATH, install with `curl -LsSf https://astral.sh/uv/install.sh | sh`.

## Discipline

- Never echo or log the secret values themselves.
- Never write keys into the plugin directory or the user's home dotfiles directly — only into `~/.config/ai-video-producer/.env`.
- Don't add the loader line more than once. Grep the profile first.
- Don't `chmod 600` if the file already has tighter permissions.
