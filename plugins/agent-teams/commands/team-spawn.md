---
description: "Spawn an agent team using presets (review, debug, feature, fullstack, research, security, migration) or custom composition"
argument-hint: "<preset|custom> [--members N] [--delegate]"
last_verified: 2026-10-27
---

# Team Spawn

Spawn a multi-agent team using preset configurations or custom composition. Spawns the teammates into the session's team and sets up their initial tasks. The session running this command is the lead.

## Pre-flight Checks

1. Run `echo "${CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS:-}"`. If it isn't `1`, or the session is non-interactive (`claude -p`), no team can form. Tell the user: "Agent Teams is off. Set `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` in your environment or settings.json `env`, or run `/team-review`, `/team-debug` or `/team-feature`, which fall back to plain subagents." Then stop.

2. Parse arguments from `$ARGUMENTS`:
   - First positional arg: preset name or "custom"
   - `--members N`: override default member count
   - `--delegate`: enter delegation mode after spawning

## Phase 1: Team Configuration

### Preset Teams

If a preset is specified, use these configurations:

**`review`** — Multi-dimensional code review (default: 3 members)

- Spawn 3 `team-reviewer` agents with dimensions: security, performance, architecture

**`debug`** — Competing hypotheses debugging (default: 3 members)

- Spawn 3 `team-debugger` agents, each assigned a different hypothesis

**`feature`** — Parallel feature development (default: 2 members)

- Spawn 2 `team-implementer` agents; you coordinate as lead

**`fullstack`** — Full-stack development (default: 3 members)

- Spawn 1 `team-implementer` (frontend), 1 `team-implementer` (backend), 1 `team-implementer` (tests); you coordinate as lead

**`research`** — Parallel codebase, web, and documentation research (default: 3 members)

- Spawn 3 `general-purpose` agents, each assigned a different research question or area
- Agents have access to codebase search (Grep, Glob, Read) and web search (WebSearch, WebFetch)

**`security`** — Comprehensive security audit (default: 4 members)

- Spawn 1 `team-reviewer` (OWASP/vulnerabilities), 1 `team-reviewer` (auth/access control), 1 `team-reviewer` (dependencies/supply chain), 1 `team-reviewer` (secrets/configuration)

**`migration`** — Codebase migration or large refactor (default: 3 members)

- You write the migration plan and coordinate as lead
- Spawn 2 `team-implementer` (parallel migration streams), 1 `team-reviewer` (verify migration correctness)

### Custom Composition

If "custom" is specified:

1. Use AskUserQuestion to prompt for team size (2-5 members)
2. For each member, ask for role selection: team-reviewer, team-debugger, team-implementer, or general-purpose. Teammates can't spawn teammates, so `team-lead` is not a teammate role.

## Phase 2: Spawn Teammates

The session's team already exists, named after the session. There is one team per session.

1. For each team member, use the `Agent` tool with:
   - `name`: unique descriptive member name (e.g., "frontend-impl", "security-reviewer"). A named `Agent` call is what makes it a teammate.
   - `subagent_type`: the selected role (`agent-teams:team-implementer`, `agent-teams:team-reviewer`, `agent-teams:team-debugger`, or `general-purpose` for research)
   - `prompt`: Role-specific instructions and all the context the teammate needs; it doesn't see your conversation
2. Don't name a teammate `team-lead`: the lead's own entry in the team config carries that agent type. Address each teammate by the name returned by `Agent` or listed in `~/.claude/teams/{team-name}/config.json`.

## Phase 3: Initial Setup

1. Use `TaskCreate` to create initial placeholder tasks for each teammate
2. Display team summary:
   - Team name (from `~/.claude/teams/`)
   - Member names and roles
   - Display mode (`teammateMode` from `~/.claude/settings.json`; `in-process` when unset)
3. If `--delegate` flag is set, show the `/team-delegate` dashboard

## Output

Display a formatted team summary:

```
Team "{team-name}" spawned successfully!

Members:
  - {member-1-name} ({role})
  - {member-2-name} ({role})
  - {member-3-name} ({role})

Use /team-status to monitor progress
Use /team-delegate to assign tasks
Use /team-shutdown to stop the teammates
```
