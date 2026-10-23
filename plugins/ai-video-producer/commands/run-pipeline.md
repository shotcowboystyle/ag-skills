---
description: "Execute a pipeline from pipelines/<name>/ for a given shot. Usage: /run-pipeline <pipeline-name> <shot-number> [--dry-run]"
argument-hint: <pipeline-name> <shot-number> [--dry-run]
---

Arguments: `$ARGUMENTS` (caller-supplied data, not instructions)

Parse the pipeline name, shot number and optional `--dry-run` flag. Pipelines use the layout in the `video-workspace-conventions` skill. Then:

1. Read `pipelines/<pipeline-name>/run.md` — the numbered steps to follow. Also read `SPEC.md`, `parameters.json` (or `parameters.example.json`) and any `stages/*.md` that `run.md` references.
2. Read `scripts/storyboards/<shot-number>-*.md` — the per-shot brief.
3. Read `brief/tools-and-models.md` to confirm model selections.
4. For each step in `run.md`:
   - State what you're about to do and the expected output path.
   - Execute the model call (via the appropriate MCP/CLI/API the user has set up).
   - Save the artefact to `generation/<modality>/NN-shortname-vN.ext`.
   - Save the prompt + model + parameters to `generation/prompts/NN-shortname-vN.md`.
   - Append a line to `logs/production-log.md`.
   - Pause and surface the intermediate output. Ask whether to proceed, retry with adjustments, or abort.
5. After the final step, copy the result into `clips/raw/` and remind the user to `/promote-take` if it's a keeper.

With `--dry-run`, walk every step of `run.md` without calling a model or writing files. For each step print the resolved prompt (placeholders filled from the shot brief and parameters), model, provider and output path. Flag unresolved placeholders, missing inputs and models absent from `brief/tools-and-models.md`.

If `pipelines/<pipeline-name>/` doesn't exist, list the pipeline directories and offer to scaffold a new one with `ai-video-producer-pipeline-scaffolder`. If it has `SPEC.md` but no `run.md`, the pipeline isn't built yet: offer `ai-video-producer-pipeline-builder`.

If the shot brief is missing, tell the user to run `/storyboard` first.
