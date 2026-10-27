---
description: "Gracefully shut down the session's agent teammates and summarize their results"
argument-hint: "[--force]"
last_verified: 2026-10-27
---

# Team Shutdown

Ask every teammate in the session's team to shut down, then summarize what the team finished. Claude Code removes the team config when the session ends and keeps the task list on disk, so there is no cleanup step.

## Phase 1: Pre-Shutdown

1. Parse `$ARGUMENTS`:
   - `--force`: don't wait for teammates to approve the shutdown
2. Find the team: list `~/.claude/teams/` and read `~/.claude/teams/{team-name}/config.json`. No team directory means no teammates are running; say so and stop.
3. Call `TaskList` to check for in-progress tasks.
4. If there are in-progress tasks and `--force` is not set:
   - Display warning: "Warning: {N} tasks are still in progress"
   - List the in-progress tasks
   - Ask user: "Proceed with shutdown? In-progress work may be lost."

## Phase 2: Graceful Shutdown

For each teammate in the config's `members` (skip the lead's own entry):

1. Ask the teammate by name to shut down: "Team shutdown requested. Please finish current work and report your status."
2. Wait for each answer. A teammate approves and exits, or rejects with a reason; report rejections to the user. A teammate finishes its current tool call first, so this can take time.
3. With `--force`, don't wait. The user can stop an in-process teammate by selecting it in the agent panel and pressing `x`.

## Phase 3: Summary

```
Team "{team-name}" shutdown complete.

Members shut down: {N}/{total}
Tasks completed: {completed}/{total}
Tasks remaining: {remaining}

Task list kept at ~/.claude/tasks/{team-name}/
```
