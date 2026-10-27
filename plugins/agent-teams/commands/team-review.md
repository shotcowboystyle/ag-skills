---
description: "Launch a multi-reviewer parallel code review with specialized review dimensions"
argument-hint: "<target> [--reviewers security,performance,architecture,testing,accessibility] [--base-branch main]"
last_verified: 2026-10-27
---

# Team Review

Orchestrate a multi-reviewer parallel code review where each reviewer focuses on a specific quality dimension. Produces a consolidated, deduplicated report organized by severity.

## Pre-flight Checks

1. Pick the mode. Run `echo "${CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS:-}"`:
   - `1` in an interactive session → **team mode**: teammates share a task list and message you.
   - Anything else, or `claude -p` → **subagent mode**: tell the user "Agent Teams is off; running the roles as plain subagents." Spawn each role with `Agent` and no `name`, in parallel where the work allows, and use each returned answer as that role's result. Skip `TaskCreate`, `TaskList` and shutdown.
2. Parse `$ARGUMENTS`:
   - `<target>`: file path, directory, git diff range (e.g., `main...HEAD`), or PR number (e.g., `#123`)
   - `--reviewers`: comma-separated dimensions (default: `security,performance,architecture`)
   - `--base-branch`: base branch for diff comparison (default: `main`)

## Phase 1: Target Resolution

1. Determine target type:
   - **File/Directory**: Use as-is for review scope
   - **Git diff range**: Use Bash to run `git diff {range} --name-only` to get changed files
   - **PR number**: Use Bash to run `gh pr diff {number} --name-only` to get changed files
2. Collect the full diff content for distribution to reviewers
3. Display review scope to user: "{N} files to review across {M} dimensions"

## Phase 2: Team Spawn

In team mode the session's team already exists and you are its lead.

1. For each requested dimension, use the `Agent` tool to spawn a reviewer:
   - `name`: `{dimension}-reviewer` (e.g., "security-reviewer"); team mode only
   - `subagent_type`: "agent-teams:team-reviewer"
   - `prompt`: Include the dimension assignment, target files, and diff content. Reviewers don't see your conversation.
2. Team mode: use `TaskCreate` for each reviewer's task:
   - Subject: "Review {target} for {dimension} issues"
   - Description: Include file list, diff content, and dimension-specific checklist

## Phase 3: Monitor and Collect

1. Wait for every reviewer. Team mode: reviewer messages and idle notifications arrive on their own; read `TaskList` when one arrives, not on a timer. Subagent mode: each `Agent` call returns the findings.
2. As each reviewer completes, collect their structured findings
3. Track progress: "{completed}/{total} reviews complete"

## Phase 4: Consolidation

1. **Deduplicate**: Merge findings that reference the same file:line location
2. **Resolve conflicts**: If reviewers disagree on severity, use the higher rating
3. **Organize by severity**: Group findings as Critical, High, Medium, Low
4. **Cross-reference**: Note findings that appear in multiple dimensions

## Phase 5: Report and Cleanup

1. Present consolidated report:

   ```
   ## Code Review Report: {target}

   Reviewed by: {dimensions}
   Files reviewed: {count}

   ### Critical ({count})
   [findings...]

   ### High ({count})
   [findings...]

   ### Medium ({count})
   [findings...]

   ### Low ({count})
   [findings...]

   ### Summary
   Total findings: {count} (Critical: N, High: N, Medium: N, Low: N)
   ```

2. Team mode: ask each reviewer by name to shut down. Claude Code removes the team when the session ends.
