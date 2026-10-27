---
description: Full quality certification with badge
argument-hint: <path>
---

Run PluginEval at deep depth and assign a quality badge. For a skill directory, deep depth runs the static layer plus the experimental LLM judge and Monte Carlo layers. For a plugin directory, only the static layer runs.

For a skill, this makes 55 model calls through your Max plan. For a plugin directory, it makes none.

## Running

Resolve the path to absolute first, and stop if it does not exist:

```bash
target="$(cd "{argument}" && pwd)"
uv run --directory "${CLAUDE_PLUGIN_ROOT}" plugin-eval certify "$target" --output markdown
```
