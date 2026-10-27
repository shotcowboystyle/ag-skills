---
name: meta-wearables-knowledge-base
description: Reference-only library for the meta-wearables-ops skills — source-pinned Meta Wearables DAT iOS/Android and Web Apps documents, the shared rules (evidence ladder, device labels, secrets), and the official source registry. Not a task skill. Use when another meta-wearables-ops skill links here or when citing a specific reference document, and only then; for planning, building, debugging, or releasing a wearable feature, use the owning task skill (start with meta-wearables-route-planner).
allowed-tools: Read, Grep, Glob, Bash(uv run *)
last_verified: 2026-08-22
---

# Meta Wearables knowledge base

Reference library for the meta-wearables-ops skills. It does not run a workflow
on its own. Every document lives under `references/` in this skill's directory.
Other skills link here with `../meta-wearables-knowledge-base/references/<path>`;
if your tool installs skills under prefixed directory names, find this skill by
name and resolve the same `references/<path>` inside it.

## Where to start

- [Shared rules](references/shared-rules.md) — the evidence ladder, device-label
  rules, secrets policy, and claim rules every skill applies.
- [Lane overview](references/70-meta-wearables/README.md) — source snapshot and
  reading order.
- [Source registry](references/sources/meta-wearables-source-registry.md) and
  [freshness log](references/sources/meta-wearables-source-freshness-log.md) —
  check these before calling an SDK claim current. Pin exact package revisions in
  real apps.

Grep the tree for the API or capability name instead of reading it front to back.

## Refreshing sources (maintainers)

After an SDK release, follow the [refresh procedure](references/sources/refresh-procedure.md).
`$SKILL` is this skill's directory. Two checkers compare the pinned refs in the
surface manifest against the public repositories:

```bash
uv run $SKILL/scripts/check_source_revisions.py
uv run $SKILL/scripts/check_source_tree_inventory.py
```

Both need network access and only read public Git refs and archives.
