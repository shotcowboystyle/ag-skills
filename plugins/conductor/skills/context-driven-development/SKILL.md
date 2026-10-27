---
name: context-driven-development
description: >-
  Creates and maintains project context artifacts (product.md, tech-stack.md, workflow.md, tracks.md)
  in a `conductor/` directory. Scaffolds new projects from scratch, extracts context from existing
  codebases, validates artifact consistency before implementation, and synchronizes documents as the
  project evolves. Use when setting up a project, creating or updating product docs, managing a tech
  stack file, defining development workflows, tracking work units, onboarding to an existing codebase,
  or running project scaffolding.
version: 1.1.0
---

# Context-Driven Development

Keep the project's context in `conductor/`, next to the code, so every session and every
teammate starts from the same product goals, stack and workflow. The flow is
**Context → Spec & Plan → Implement**.

| Artifact | Holds | Update when |
| --- | --- | --- |
| `product.md` | What and why: problem, users, features, goals | A feature ships or the goals change |
| `product-guidelines.md` | Voice, terminology, copy standards | Terms or tone change |
| `tech-stack.md` | Languages, frameworks, key dependencies with versions | A dependency is added, removed or upgraded a major version |
| `workflow.md` | TDD policy, coverage target, commit convention, checkpoints | The team changes how it works |
| `tracks.md` | Registry of tracks and their status | A track is created, changes status or is archived |
| `index.md` | Links to all of the above and to active tracks | A file or track is added |

## When to Use This Skill

- Setting up Conductor in a new or existing project
- Starting a session or a track and checking the context is current
- Updating context after a dependency change or a finished track

## Procedure

### Set up context (`/conductor:setup`)

1. **Detect the project type.** Brownfield if any of `.git`, a package manifest
   (`package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`) or `src/` exists; greenfield
   otherwise.
2. **Brownfield: read before asking.** Take languages, frameworks and versions from the
   manifests and lockfiles, test and lint tools from their configs, and the commit
   convention from `git log`. Ask only about what the code doesn't show: the product goal,
   the users, and the workflow rules the team wants.
3. **Greenfield: ask**, one question at a time, about the product, users, stack and workflow.
4. **Write the six artifacts** and the selected style guides. Record progress in
   `setup_state.json` after each file so setup can resume.
5. **Validate**: the command runs `conductor-validator` in `setup` mode. Fix every
   CRITICAL finding before the first track.

### Before starting a track

1. Read `index.md`, then `product.md`, `tech-stack.md` and `workflow.md`.
2. Compare `tech-stack.md` with the manifests. A dependency in one and not the other is
   stale context: propose the fix before writing code.
3. `/conductor:implement` validates the track with `conductor-validator` in `track` mode
   and stops on a CRITICAL finding.

### While working

- A new dependency goes into `tech-stack.md` in the same commit that adds it, with its
  version and why it was chosen over what was already there.
- Context changes go in small edits next to the code change that caused them, not in a
  rewrite later.

### After a track completes

1. Move the shipped features from planned to implemented in `product.md`.
2. Check `tech-stack.md` against the manifests again.
3. Note any `workflow.md` rule that the track showed was wrong, and propose the change.
4. Set the track to `[x]` in `tracks.md` (the `track-management` skill).

### Ending a session mid-track

Leave the current task `[~]` with a note under it saying where you stopped, commit the work
in progress on the track's branch, and update `metadata.json`. The next session reads
`index.md`, `tracks.md` and the track's `plan.md` and continues from that note.

## References

- `references/details.md`: what each artifact contains, the directory layout, the
  validation checklist, anti-patterns, and tool integration (hooks, CI).
- `references/artifact-templates.md`: starter templates for each artifact.
