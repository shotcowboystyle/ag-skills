---
description: Evaluate a plugin or skill for quality
argument-hint: <path> [--depth quick|standard]
---

Run the PluginEval quality evaluation on a plugin or skill directory.

## Usage

/eval <path> — evaluate at standard depth (static + LLM judge)
/eval <path> --depth quick — static analysis only (instant)

## Process

### Step 1: Resolve the path

Take the path and depth from `{argument}` (depth defaults to `standard`). Resolve the path
to absolute before running anything, and stop if it does not exist:

```bash
target="$(cd "<path>" && pwd)"
```

### Step 2: Run the engine

The engine runs every layer for the depth, blends the layer scores, applies the
anti-pattern penalty and assigns the badge. Do not recompute any of it:

```bash
uv run --directory "${CLAUDE_PLUGIN_ROOT}" plugin-eval score "$target" \
  --depth <depth> --output json
```

If stderr says the LLM judge could not measure dimensions, the composite came from the
remaining layers. Report that and the fix (`uv sync --extra llm` in the plugin root, plus a
configured model). Do not dispatch `eval-judge` to fill the gap.

### Step 3: Present Results

Report only numbers from the JSON: `composite.score`, `composite.badge`,
`composite.confidence_label`, `composite.anti_pattern_penalty`, `composite.dimensions`,
each entry in `layers`, and each layer's `anti_patterns`.

```
## Overall Score: {composite.score}/100 {composite.badge}
## Layer Breakdown
| Layer | Score |
|-------|-------|
## Dimension Scores
| Dimension | Weight | Score | Grade |
|-----------|--------|-------|-------|
## Anti-Patterns Detected
## Recommendations
```
