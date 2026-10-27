# Agent Teams Plugin

Orchestrate multi-agent teams for parallel code review, hypothesis-driven debugging, and coordinated feature development using Claude Code's experimental [Agent Teams](https://code.claude.com/docs/en/agent-teams) feature.

## Setup

Claude Code only. The plugin's `plugin.json` declares `"harnesses": ["claude-code"]`, so the generators skip it for every other harness.

### Prerequisites

1. Enable the experimental Agent Teams feature, in your shell or in `settings.json`:

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

Without the flag, or in non-interactive mode (`claude -p`), the `/team-*` commands still run: they spawn the same roles as ordinary subagents and merge the results in the main session.

2. Optionally pick a display mode with `teammateMode` in `~/.claude/settings.json` (or `claude --teammate-mode <mode>` for one session):

```json
{
  "teammateMode": "auto"
}
```

- `"in-process"` — all teammates run in your terminal; select one in the agent panel (default)
- `"auto"` — split panes when already inside tmux, or in iTerm2 with the `it2` CLI; in-process otherwise
- `"tmux"` — split panes; detects tmux or iTerm2 from your terminal
- `"iterm2"` — iTerm2 native split panes; needs the [`it2` CLI](https://github.com/mkusaka/it2) and iTerm2's Python API enabled

Split panes don't work in VS Code's integrated terminal, Windows Terminal or Ghostty.

### How teams work

Each session has exactly one team, created automatically and named after the session. The session that runs a `/team-*` command is the lead: teammates can't spawn teammates. A teammate is an `Agent` call with a `name`; teammates are addressed by that name. Claude Code cleans up the team when the session ends. The task list stays at `~/.claude/tasks/{team-name}/`.

### Installation

First, add the marketplace (if you haven't already):

```
/plugin marketplace add shotcowboystyle/ag-skills
```

Then install the plugin:

```
/plugin install agent-teams@claude-code-workflows
```

## Features

- **Preset Teams** — Spawn pre-configured teams for common workflows (review, debug, feature, fullstack, research, security, migration)
- **Multi-Reviewer Code Review** — Parallel review across security, performance, architecture, testing, and accessibility dimensions
- **Hypothesis-Driven Debugging** — Competing hypothesis investigation with evidence-based root cause analysis
- **Parallel Feature Development** — Coordinated multi-agent implementation with file ownership boundaries
- **Parallel Research** — Multiple Explore agents investigating different questions or codebase areas simultaneously
- **Security Audit** — Comprehensive parallel security review across OWASP, auth, dependencies, and configuration
- **Migration Support** — Coordinated codebase migration with parallel implementation streams and correctness verification
- **Task Coordination** — Dependency-aware task management with workload balancing
- **Team Communication** — Structured messaging protocols for efficient agent collaboration

## Commands

| Command          | Description                                                |
| ---------------- | ---------------------------------------------------------- |
| `/team-spawn`    | Spawn a team using presets or custom composition           |
| `/team-status`   | Display team members, tasks, and progress                  |
| `/team-shutdown` | Gracefully shut down a team and clean up resources         |
| `/team-review`   | Multi-reviewer parallel code review                        |
| `/team-debug`    | Competing hypotheses debugging with parallel investigation |
| `/team-feature`  | Parallel feature development with file ownership           |
| `/team-delegate` | Task delegation dashboard and workload management          |

## Agents

| Agent              | Role                                                                              | Color  |
| ------------------ | --------------------------------------------------------------------------------- | ------ |
| `team-lead`        | Lead for the main session (`claude --agent agent-teams:team-lead`) — splits work, spawns, merges; not spawned as a teammate | Blue   |
| `team-reviewer`    | Multi-dimensional code reviewer — operates on assigned review dimension           | Green  |
| `team-debugger`    | Hypothesis investigator — gathers evidence to confirm/falsify assigned hypothesis | Red    |
| `team-implementer` | Parallel builder — implements within strict file ownership boundaries             | Yellow |

## Skills

| Skill                          | Description                                                              |
| ------------------------------ | ------------------------------------------------------------------------ |
| `team-composition-patterns`    | Team sizing heuristics, preset compositions, agent type selection        |
| `task-coordination-strategies` | Task decomposition, dependency graphs, workload monitoring               |
| `parallel-debugging`           | Hypothesis generation, evidence collection, result arbitration           |
| `multi-reviewer-patterns`      | Review dimension allocation, finding deduplication, severity calibration |
| `parallel-feature-development` | File ownership strategies, conflict avoidance, integration patterns      |
| `team-communication-protocols` | Messaging by name, integration handoffs, plan approval, shutdown         |

## Quick Start

### Multi-Reviewer Code Review

```
/team-review src/ --reviewers security,performance,architecture
```

Spawns 3 reviewers, each analyzing the codebase from their assigned dimension, then consolidates findings into a prioritized report.

### Hypothesis-Driven Debugging

```
/team-debug "API returns 500 on POST /users with valid payload" --hypotheses 3
```

Generates 3 competing hypotheses, spawns investigators for each, collects evidence, and presents the most likely root cause with a fix.

### Parallel Feature Development

```
/team-feature "Add user authentication with OAuth2" --team-size 3 --plan-first
```

Decomposes the feature into work streams with file ownership boundaries, gets your approval, then spawns implementers to build in parallel.

### Parallel Research

```
/team-spawn research
```

Spawns 3 researchers to investigate different aspects in parallel — across your codebase (Grep/Read) and the web (WebSearch/WebFetch). Each reports findings with citations.

### Security Audit

```
/team-spawn security
```

Spawns 4 security reviewers covering OWASP vulnerabilities, auth/access control, dependency supply chain, and secrets/configuration. Produces a consolidated security report.

### Codebase Migration

```
/team-spawn migration
```

You lead the migration plan; it spawns 2 implementers to migrate code in parallel streams, and a reviewer to verify correctness of the migrated code.

### Custom Team

```
/team-spawn custom --members 4
```

Interactively configure team composition with custom roles and agent types.

## Best Practices

1. **Start with presets** — Use `/team-spawn review`, `/team-spawn debug`, or `/team-spawn feature` before building custom teams
2. **Use `--plan-first`** — For feature development, always review the decomposition before spawning implementers
3. **File ownership is critical** — Never assign the same file to multiple implementers; use interface contracts at boundaries
4. **Monitor with `/team-status`** — Check progress regularly and use `/team-delegate --rebalance` if work is uneven
5. **Graceful shutdown** — Use `/team-shutdown` to stop teammates mid-session rather than killing processes; the team itself is cleaned up when the session ends
6. **Keep teams small** — 2-4 teammates is optimal; larger teams increase coordination overhead
