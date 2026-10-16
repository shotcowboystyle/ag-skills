# Agent Skills frontmatter

Source: https://agentskills.io/specification

| Field | Required | Rule |
|---|---|---|
| `name` | yes | 1-64 chars, `^[a-z0-9]+(-[a-z0-9]+)*$`, equals directory name |
| `description` | yes | 1-1024 chars, what it does and when to use it |
| `license` | no | string, license name or path to bundled file |
| `compatibility` | no | string, up to 500 chars, environment requirements |
| `metadata` | no | map of string to string |
| `allowed-tools` | no | space-separated tool list (experimental) |

Body: markdown, keep under 500 lines. Optional subdirectories: `scripts/`, `references/`, `assets/`.
