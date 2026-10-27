# ag-skills

Agents, skills, and commands for seven coding tools: Claude Code, OpenAI Codex CLI,
Cursor, OpenCode, Google Antigravity CLI (`agy`), GitHub Copilot, and Pi.

The marketplace (`claude-code-workflows`) holds 81 plugins (80 local + 1 external),
176 agents, 299 skills, and 189 commands. Sources live under `plugins/` in Claude Code
format; adapters in `tools/adapters/` emit each other tool's format. Skills follow the
[Agent Skills](https://agentskills.io/specification) `SKILL.md` spec.

## Install

```bash
# Claude Code
/plugin marketplace add shotcowboystyle/ag-skills
/plugin install email-deliverability@claude-code-workflows

# Skills only, any agent
gh skill install shotcowboystyle/ag-skills email-dns-setup
npx skills add shotcowboystyle/ag-skills --skill email-dns-setup
```

Codex, Cursor, OpenCode, Antigravity, Copilot, and Pi setup: [docs/harnesses.md](docs/harnesses.md).

## Docs

- [AGENTS.md](AGENTS.md) — repo map and working rules (`CLAUDE.md` links to it)
- [ARCHITECTURE.md](ARCHITECTURE.md) — adapter framework overview
- [docs/plugins.md](docs/plugins.md) — plugin catalog
- [docs/agents.md](docs/agents.md) and [docs/agent-skills.md](docs/agent-skills.md) — agent and skill reference
- [docs/usage.md](docs/usage.md) — commands and workflows
- [docs/authoring.md](docs/authoring.md) — how to write a plugin
- [CONTRIBUTING.md](CONTRIBUTING.md)

## Quality gates

```bash
make validate STRICT=1   # structural validation of every harness output
make garden STRICT=1     # drift detection (dead links, stale counts, oversize skills)
make lint                # ruff + ty
make test                # pytest (plugin-eval + tools/tests)
make smoke-test          # real-CLI checks; skips CLIs not on PATH
make generate-all        # regenerate harness artifacts before committing source changes
```

## Standalone skills (`skills/`)

`skills/` holds skills that are not part of a plugin, checked by a small Node toolchain:

```bash
pnpm install
pnpm new <name> "<description>"         # scaffold skills/<name>
pnpm check                              # validate + node:test (CI runs this)
pnpm install-skill <name> [--to <dir>]  # symlink into ~/.claude/skills (or another agent's dir)
```

`pnpm validate` fails on a missing `SKILL.md`, invalid YAML, a missing or malformed
`name`/`description`, a name that differs from the directory, wrong types on optional
fields, an empty body, or broken relative links. It warns on unknown frontmatter keys,
bodies over 500 lines, and non-executable files in `scripts/`.
