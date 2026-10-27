---
name: session-guard
description: >-
  Use when a long session shows drift: the agent contradicts an earlier
  decision, breaks a rule it followed before, lets naming or style conventions
  slide, loses context after compaction, or lets task scope grow. Re-anchors on
  the project's rule files and writes a checkpoint so work continues on solid
  ground.
---

# Session Guard

## Overview

Long sessions can drift: early decisions fall out of context, compaction summarizes away
rules that were only stated in conversation, and output starts to contradict itself. This
skill reacts to those signals. It re-reads the source of truth, writes a checkpoint, and
continues. It never halts work on a tool-call count alone.

## When to Use

Trigger on a **drift signal**, not on task size:

| Signal | Example | Action |
|--------|---------|--------|
| Contradicts an earlier decision | Renames a module the user chose to keep | VERIFY, then CHECKPOINT |
| Breaks a rule it followed earlier | Adds `console.log` after the user banned it | RE-ANCHOR |
| Convention drift | `snake_case` files appear in a `kebab-case` tree | RE-ANCHOR |
| Compaction happened | Earlier turns are summarized, or the user ran a compact command | RE-ANCHOR, then CHECKPOINT |
| Stale state | A file read differs from what you remembered | RE-READ, don't trust memory |
| Scope growth | The task has picked up goals the user never asked for | CHECKPOINT, ask before expanding |

A long session with none of these signals needs no intervention.

## Protocol

### RE-ANCHOR

1. Re-read the project's rule files (`AGENTS.md`, `CLAUDE.md`, `CONTEXT.md`, or the
   equivalent). Don't rely on what you remember of them.
2. State the 3-5 rules that apply to the next action, in one line:
   "Active rules: [naming], [file layout], [error handling], [testing]".
3. Check the planned next action against those rules before running it.
4. If a prior decision is uncertain, re-read the file or message where it was made.
   Don't guess.

### VERIFY

Find the decision you are contradicting (in a file, commit, or the user's message). If
the earlier decision stands, revert the drift. If the user changed it, follow the newer
instruction and say so.

### CHECKPOINT

Write a short checkpoint, then **keep working**:

- Goal, in one sentence
- Done so far, as a list of files or steps
- Decisions that must survive compaction, with their source
- Next step

Put the checkpoint in a file the user expects (a handoff or progress note), or in your
reply if the project has no such file. Ask before creating new files outside the task.

Offer a fresh session only when the checkpoint shows the remaining work is a separate
task. That is a suggestion to the user, never a reason to stop mid-task.

## Compaction-safe pattern

Compaction keeps recent messages and drops older conversation detail: decisions made
early, rules stated only in chat, and the contents of earlier tool output. What a
specific harness preserves varies; needs measurement for your setup.

Keep rules that matter in files the agent can re-read (`AGENTS.md`, `CLAUDE.md`,
`CONTEXT.md`), not only in conversation.

## Common Mistakes

- Trusting memory of the rules after compaction. Re-read the file.
- Re-reading everything "to be safe". Re-read only the files the next action depends on.
- Stopping work because the session is long. Length alone is not a signal; drift is.
- Treating a checkpoint as a handoff. A checkpoint records state, then work continues.
