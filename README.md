# ag-skills

Portable, agent-agnostic skills. Each skill is a folder under `skills/` with a `SKILL.md`
(YAML frontmatter `name` + `description`, then instructions) and optional `references/`,
`scripts/` and `assets/`, following the open Agent Skills layout so the same folder works in
Claude Code, Claude.ai, Codex, Cursor and anything else that reads `SKILL.md`.

## Skills

| Skill | What it does |
|---|---|
| [email-dns-setup](skills/email-dns-setup/SKILL.md) | Plan, generate, audit and verify mail DNS (MX, SPF, DKIM, DMARC, MTA-STS, TLS-RPT, BIMI) for any domain on any registrar/DNS host with any mailbox provider or sending service. Includes a read-only `dig` audit script. |

## Using a skill

- **Claude Code**: symlink or copy `skills/<name>` into `~/.claude/skills/` (personal) or
  `.claude/skills/` (per project).
- **Claude.ai / Cowork**: zip the skill folder and upload it under Settings → Skills.
- **Other agents**: point the agent at `skills/<name>/SKILL.md`.

Scripts under `skills/*/scripts/` are read-only diagnostics unless their header says otherwise.
