# ag-skills

Create, test, and validate portable AI agent skills. Skills follow the
[Agent Skills](https://agentskills.io/specification) `SKILL.md` format, so one
skill directory works in Claude Code, Codex, Cursor, and any other agent that
reads the spec.

## Skills

| Skill | What it does |
|---|---|
| [email-dns-setup](skills/email-dns-setup/SKILL.md) | Plan, generate, audit and verify mail DNS (MX, SPF, DKIM, DMARC, MTA-STS, TLS-RPT, BIMI) for any domain on any registrar/DNS host with any mailbox provider or sending service. Includes a read-only `dig` audit script. |

## Layout

```
skills/<name>/          one skill per directory
  SKILL.md              frontmatter + instructions (required)
  scripts/              runnable helpers
  references/           long-form docs the skill links to
  assets/               templates and files the skill hands out
  tests/*.test.mjs      node:test checks for this skill
tools/                  validator, scaffolder, linker
tests/                  validator unit tests and fixtures
```

## Commands

```bash
pnpm install
pnpm new <name> "<description>"   # scaffold skills/<name>
pnpm validate                     # lint every skill against the spec
pnpm test                         # node:test across tests/ and skills/*/tests/
pnpm check                        # validate + test (CI runs this)
pnpm install-skill <name> [--to <dir>]  # symlink into ~/.claude/skills (or another agent's dir)
```

## Validation rules

Errors fail the build: missing `SKILL.md`, invalid YAML, missing or malformed
`name`/`description`, name not matching the directory, wrong types on optional
fields, empty body, broken relative links. Warnings print only: unknown
frontmatter keys, body over 500 lines, non-executable files in `scripts/`.
