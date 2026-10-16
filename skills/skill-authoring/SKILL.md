---
name: skill-authoring
description: Write, review, and validate portable agent skills in SKILL.md format. Use when creating a new skill, editing an existing one, or asked whether a skill follows the Agent Skills spec.
license: MIT
metadata:
  author: shotcowboystyle
  version: "0.1.0"
---

# Skill authoring

## When to use

- User asks to create, edit, or review a skill.
- A skill fails `pnpm validate`.

## Steps

1. Scaffold: `pnpm new <kebab-name> "<description>"`.
2. Write `SKILL.md`. Frontmatter rules are in [references/spec.md](references/spec.md).
3. Put long material in `references/`, runnable helpers in `scripts/`, templates in `assets/`. Link them from the body.
4. Add a `tests/*.test.mjs` for any script logic.
5. Run `pnpm check`. Fix every error; treat warnings as review comments.
6. Install locally to try it: `pnpm install-skill <name>`.

## Description guidance

The description is the only text the agent sees before deciding to load the skill. State what it does and when to use it, in the third person, under 1024 characters.
