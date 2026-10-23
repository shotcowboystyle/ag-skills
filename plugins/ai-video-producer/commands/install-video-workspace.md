---
description: Scaffold the AI video production workspace (folder skeleton + project AGENTS.md) into the current directory.
---

Set up the current working directory as an AI video production workspace.

## Steps

1. Confirm the current directory is empty (or near-empty — only `.git`, `README.md`, `LICENSE`, `.gitignore` allowed). If not, ask the user whether to proceed anyway.

2. Create the folder skeleton:

```
brief/
characters/
scripts/{drafts,final,storyboards,tts}/
assets/{reference-images,voices,voice-clones,sfx,music,source-media,fonts,luts,overlays}/
generation/{text-to-image,image-to-image,image-to-video,text-to-video,voice,lip-sync,upscale,prompts}/
clips/{raw,selected,edited,b-roll,normalised,converted}/
pipelines/
timeline/
budgets/
research/
output/{drafts,proofs,final}/
exports/{thumbnails,captions,subtitles}/
logs/
```

Drop a `.gitkeep` in every leaf directory so the structure survives commits.

3. Write a project-level `AGENTS.md` to the workspace root that documents the lifecycle, folder conventions, and slash commands. Use the `video-workspace-conventions` skill from this plugin as the source of truth — read its `SKILL.md` and adapt the content into the project AGENTS.md. Also write a one-line `CLAUDE.md` containing `@AGENTS.md`, so Claude Code reads the same file every other tool reads.

4. Seed `pipelines/` with starter pipelines from this plugin's skills (text-to-image-to-video, voice-to-lip-sync, text-to-video-direct, upscale-and-interpolate), using the pipeline layout from `video-workspace-conventions`. For each skill, create `pipelines/<name>/` with:
   - `run.md` — the skill's Inputs and Steps sections, copied verbatim.
   - `SPEC.md` — Purpose (from the skill's description and "When to use"), Stages (one per model call in the steps), and an empty Open questions section.
   - `runs/.gitkeep`.

   The user can edit these per project without touching the plugin.

5. Initialise git if not already a repo, add a sensible `.gitignore` (exclude large generated media if the user prefers — ask).

6. Tell the user to run `/onboard` next.
