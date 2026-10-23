---
name: provider-runners
description: Plugin-wide SDK runners that execute fal.ai and WaveSpeedAI models — take a model id plus JSON input, queue and poll the job, download the outputs, and print one JSON envelope. The execution path every ai-video-producer generation skill (text-to-image-to-video, text-to-video-direct, voice-to-lip-sync, upscale-and-interpolate) uses for fal and WaveSpeed models. Use when a pipeline step needs to run a hosted fal.ai or WaveSpeed model.
---

# Provider runners

Thin SDK wrappers the generation skills shell out to. The scripts sit next to this file. Find the installed skill folder by name; some tools prefix it, e.g. `ai-video-producer__provider-runners`.

| Provider | Runner | Auth env var | Bootstrap (in this folder) |
|----------|--------|--------------|----------------------------|
| fal.ai | `fal_run.mjs` | `FAL_KEY` | `npm install` |
| WaveSpeed | `wavespeed_run.py` | `WAVESPEED_API_KEY` | `python3 -m venv .venv && .venv/bin/pip install -r requirements.txt` |

Replicate and MiniMax have no runner: use their MCP servers (`replicate-mcp`, `minimax-mcp`) where the harness has them registered.

`/setup-credentials` stores the keys and bootstraps both toolchains. `env.example` lists every variable.

## Before calling

Check the key is in the environment without printing it:

```
printenv FAL_KEY >/dev/null && echo "FAL_KEY set" || echo "FAL_KEY missing"
```

If it's missing, stop and point the user at `/setup-credentials`. Don't read or source credential files yourself.

## Invocation contract

```
node <folder>/fal_run.mjs             <model_id> <input.json|-|inline-json> [--output <dir>] [--no-download]
<folder>/.venv/bin/python <folder>/wavespeed_run.py <model_id> <input.json|-|inline-json> [--output <dir>] [--no-download] [--sync]
```

- `<input>` is a path to a JSON file, `-` for stdin, or an inline JSON string.
- `--output <dir>` downloads returned media into that directory (e.g. `generation/text-to-image/`) and lists the files in `output_files`.
- Without `--output`, only the URLs in `data` come back.
- fal ids look like `fal-ai/<slug>`; WaveSpeed ids like `wavespeed-ai/<family>/<variant>`.

stdout is one JSON envelope; progress goes to stderr:

```
{ "model": "...", "output_files": [absolute paths], "data": <raw provider output> }
```

Rename the downloaded file to the skill's naming scheme (`NN-shortname-vN.<ext>`) and log the call as the calling skill says. A non-zero exit means the call failed: show the stderr line and don't retry a paid call without asking.
