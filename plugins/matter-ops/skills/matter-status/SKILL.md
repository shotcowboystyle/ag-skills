---
name: matter-status
description: Use when picking a matter back up or handing it over — reports what the workspace contains, what is unfinished, which citations remain unverified, and which material has been logged but never analysed. Triggers - "where is this matter up to", "what is outstanding", "matter status".
allowed-tools: Bash(find *), Bash(grep *), Bash(wc *), Bash(git status *), Bash(git log *), Read
---

# Matter Status

Report what the workspace holds, what is unfinished, and what needs checking.

## When to use

- Picking a matter back up after time away.
- Handing it to someone else.
- Before drafting, to find what is still missing.

## Procedure

### 1. Identify the matter

Read the fact block from the workspace `AGENTS.md`: matter or subject, jurisdiction,
parties, scope, confidentiality. Report them first — everything else is read against
them.

### 2. Count what is there

```bash
find . -name '*.md' -not -path './.git/*' | wc -l
wc -l < sources/register.jsonl
wc -l < entities/register.jsonl
```

Report per directory: documents in `input/`, analyses written, sources registered,
findings, timeline entries, entities, exports produced. Name the directories that are
empty — an empty `analyses/` next to a full `input/` is the most useful thing this skill
can surface.

### 3. Find the loose ends

- **Unverified citations** — search the analyses and findings for `[verify]` and report
  each with its file and line.
- **Unanalysed material** — anything in `input/` or in the evidence register with no
  corresponding analysis.
- **Unpreserved sources** — register entries with no archived copy.
- **Timeline gaps** — periods with no entries, and any conflicting dates.
- **Alias drift** — entities absent from the redaction mapping, or the reverse.

### 4. Check the working state

```bash
git -C . status --short
git -C . log -1 --format='%h %ad %s' --date=short
```

Report uncommitted changes and when the matter was last touched. A workspace with a
month of uncommitted work is worth flagging.

### 5. Report

Lead with the three things most worth doing next, chosen from the loose ends above.
Then the counts. Keep it short enough to read in one screen — a status report nobody
finishes is not a status report.

## Output

- A written summary. Nothing is created or modified.

## Notes

- Read-only, always. This skill never fixes what it finds.
- If the workspace has an evidence register, read it but never write to it — it belongs
  to the companion evidence agent.
