---
description: Compare two skills head-to-head
argument-hint: <skill-a> <skill-b>
---

Run a pairwise comparison between two skills and report which is better on each quality dimension.

## Running

Resolve both paths to absolute first, and stop if either does not exist:

```bash
a="$(cd "<skill-a>" && pwd)"
b="$(cd "<skill-b>" && pwd)"
uv run --directory "${CLAUDE_PLUGIN_ROOT}" plugin-eval compare "$a" "$b"
```
