---
name: shellcheck-configuration
description: Configure and run ShellCheck - a project .shellcheckrc, inline directives, severity and output formats, pre-commit and CI wiring that actually fails on findings. Use when setting up shell linting for a repo, fixing or suppressing ShellCheck warnings, or checking scripts for portability.
last_verified: 2026-10-27
---

# ShellCheck Configuration

## When to Use This Skill

- Adding ShellCheck to a repository, pre-commit hook or CI job
- Deciding whether to fix or suppress a warning
- Checking that a `#!/bin/sh` script avoids Bash-only syntax

## Project `.shellcheckrc`

ShellCheck looks for `.shellcheckrc` (or `shellcheckrc`) in the script's directory and each
parent directory, then falls back to `~/.shellcheckrc`. Put one at the repository root:

```ini
# Follow `source` statements, resolving paths relative to each script.
external-sources=true
source-path=SCRIPTDIR

# Optional checks worth having (list them all with: shellcheck --list-optional).
enable=check-unassigned-uppercase
enable=deprecate-which
enable=avoid-nullary-conditions

# SC1091: sourced file is generated at deploy time and not in the repo.
disable=SC1091
```

- Write each comment on its own line, and give every `disable=` a reason.
- **Do not set `shell=` in a repo that mixes `sh` and `bash` scripts.** It overrides every
  shebang, so `#!/bin/sh` scripts stop getting POSIX warnings. Let shebangs decide, and add
  `# shellcheck shell=bash` to files that have none (sourced libraries).
- `enable=all` turns on every optional check. Use it for new code, then disable what does
  not fit, with reasons.

## Running It

```bash
shellcheck -x script.sh                  # -x: follow sourced files
shellcheck -S warning scripts/*.sh       # ignore info and style findings
shellcheck -f gcc script.sh              # file:line:col: level: message [SCxxxx]
shellcheck -f json1 script.sh            # machine-readable
shellcheck -f diff script.sh | git apply # apply the fixes ShellCheck can make itself
export SHELLCHECK_OPTS='-S warning -x'   # default flags for every run
```

Exit status is 0 when there are no findings at or above the chosen severity, 1 otherwise.

## Inline Directives

A directive applies to the next command. Placed right after the shebang, before any
command, it applies to the whole file.

```bash
#!/usr/bin/env bash
# shellcheck disable=SC2034 # COLORS is read by scripts that source this file
COLORS=(red green)

# shellcheck source=lib/common.sh
. "$(dirname -- "$0")/lib/common.sh"
```

## Findings You Will See Most

| Code | Meaning | Usual fix |
|---|---|---|
| SC2086 | unquoted variable is split and globbed | `"$var"` |
| SC2046 | unquoted `$(…)` is split and globbed | quote it, or read into an array with `mapfile` |
| SC2155 | `local x=$(cmd)` masks `cmd`'s exit status | `local x; x=$(cmd)` |
| SC2181 | testing `$?` after the fact | `if cmd; then` |
| SC2015 | `a && b \|\| c` runs `c` when `b` fails | `if a; then b; else c; fi` |
| SC2016 | `$var` inside single quotes does not expand | double quotes, or suppress if literal is intended |
| SC2034 | variable assigned but never used | remove it, or `export` / suppress if used externally |
| SC2154 | variable used but never assigned | assign it, or `: "${VAR:?}"` for required env vars |
| SC2115 | `rm -rf "$dir/"` can expand to `/` | `"${dir:?}/"` |
| SC2206 | unquoted expansion in an array assignment | `read -ra arr <<<"$s"` or `mapfile -t arr` |
| SC1091 | sourced file not found | pass `-x`, set `source-path`, or add `# shellcheck source=` |
| SC3010, SC3043, SC3030 | `[[ ]]`, `local` or arrays in a POSIX `sh` script | `[ ]`, function-prefixed names, `set --` |

Every code has a wiki page: `https://www.shellcheck.net/wiki/SC2086`.

## CI and Pre-commit

Fail the job when any file has findings. `find -exec shellcheck {} \;` exits 0 even when
ShellCheck fails; use `xargs` or `-exec … +` instead.

```yaml
# GitHub Actions step
- name: ShellCheck
  run: git ls-files -z '*.sh' '*.bash' | xargs -0 --no-run-if-empty shellcheck -x
```

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/koalaman/shellcheck-precommit
    rev: v0.11.0
    hooks:
      - id: shellcheck
        args: [-x]
```

Scripts without a `.sh` extension are missed by the globs above. `shfmt -f .` lists every
file with a shell shebang.

## More

`references/details.md` covers installation, output formats, parallel runs and GitLab CI.
