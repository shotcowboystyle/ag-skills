---
name: block-no-verify-hook
description: Configure a PreToolUse hook to prevent AI agents from skipping git pre-commit hooks with --no-verify and other bypass flags. Use when setting up Claude Code projects that enforce commit quality gates.
---

# Block No-Verify Hook

PreToolUse hook configuration that intercepts and blocks bypass-flag usage before execution, ensuring AI agents cannot skip pre-commit hooks, GPG signing, or other git safety mechanisms.

## Overview

AI coding agents (Claude Code, Codex, etc.) can run shell commands with flags like `--no-verify` that bypass pre-commit hooks. This defeats the purpose of linting, formatting, testing, and security checks configured in pre-commit hooks. The block-no-verify hook adds a PreToolUse guard that rejects any tool call containing bypass flags before execution.

PreToolUse hooks are a Claude Code feature. For other harnesses, see [Other harnesses](#other-harnesses).

## Problem

When AI agents commit code, they may use bypass flags to avoid hook failures:

```bash
# These commands skip pre-commit hooks entirely. Never run them without the user's approval.
git commit --no-verify -m "quick fix"
git push --no-verify
git commit --no-gpg-sign -m "unsigned commit"
git merge --no-verify feature-branch
```

## Solution

Add a `PreToolUse` hook to `.claude/settings.json` that inspects every Bash tool call and blocks git commands containing bypass flags.

### Configuration

The hook entry to merge into your settings (see [Installation](#installation)):

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "if grep -qE '\"command\"[[:space:]]*:[[:space:]]*\"(([^\"\\\\]|\\\\.)*([[:space:]/(;&|]|\\\\[tn]))?git([[:space:]]|\\\\t)(([^\"\\\\;&|]|\\\\[^n])*([[:space:]]|\\\\t))?((commit|push|merge|rebase|pull|am|cherry-pick|revert)([[:space:]]|\\\\t)(([^\"\\\\;&|]|\\\\[^n])*([[:space:]]|\\\\t))?--no-(ver(i[a-z]*)?|g[a-z-]*)([[:space:]=;&|)\"]|\\\\)|commit([[:space:]]|\\\\t)(([^\"\\\\;&|]|\\\\[^n])*([[:space:]]|\\\\t))?-[a-zA-Z]*n)'; then echo 'BLOCKED: --no-verify and --no-gpg-sign flags are not allowed. Run the commit without bypass flags so that pre-commit hooks execute properly.' >&2; exit 2; fi"
          }
        ]
      }
    ]
  }
}
```

### How It Works

1. **Matcher**: The hook targets only `Bash` tool calls, so it does not interfere with other tools (Read, Edit, Grep, etc.).
2. **Inspection**: Claude Code sends the tool call to the hook as JSON on stdin and sets no `$TOOL_INPUT` variable. The hook searches the `command` value in that JSON with `grep -E`, so it needs no `jq` or `node`, and text in other fields, such as `cwd` or the tool call's description, can't trigger it.
3. **Matching**: The pattern looks for the word `git`, then a subcommand that takes a bypass flag (`commit`, `push`, `merge`, `rebase`, `pull`, `am`, `cherry-pick`, `revert`), then the flag, all within one shell command. A `;`, `&`, `|` or newline ends the command, so `git commit -m x && echo -n` passes. The flag must be a whole word: `--no-verify`, `--no-gpg-sign`, or a shorter prefix git accepts, e.g., `--no-veri` or `--no-g`. A word that only starts the same way, such as `--no-git-tag-version` in `npm version patch --no-git-tag-version`, passes. After `commit` it also blocks a short option group with `n`, e.g., `-n` or `-nm`, because `-n` is the short form of `--no-verify` there. `git` may follow a space, `/`, `(` or a shell separator, so `sudo git ...`, `if git ...` and `/usr/bin/git ...` are caught. A false match, such as a commit message that mentions a flag, blocks the call, which is the safe way to fail.
4. **Result**: On a match the hook prints an error and exits 2, which makes Claude Code reject the tool call. Otherwise it exits 0 and the command runs.
5. **Limits**: The hook checks text, so it stops an agent that reaches for a bypass flag out of habit. It doesn't stop an agent that sets out to evade it, e.g., by building the flag from pieces, by calling git through a variable (`g=git; $g commit --no-verify`), or by running `git -c core.hooksPath=/dev/null commit`. Pair it with the server-side checks in [Other harnesses](#other-harnesses).

## Blocked Flags

| Flag | Purpose | Why Blocked |
|------|---------|-------------|
| `--no-verify` | Skips pre-commit and commit-msg hooks | Bypasses linting, formatting, testing, security checks |
| `-n` (on `git commit`) | Short form of `--no-verify` | Same as above |
| `--no-gpg-sign` | Skips GPG commit signing | Bypasses commit signing policy |

## Installation

The `/block-no-verify` command (`/block-no-verify --global` for every project) does this merge for you. To install by hand, run the script below. It never replaces the settings file wholesale:

1. It copies an existing settings file to `settings.json.bak.<timestamp>` first.
2. It keeps every existing setting and hook.
3. It removes an earlier copy of this hook and adds the current one, so it is safe to run again.

```bash
f=.claude/settings.json  # use f=~/.claude/settings.json to enforce across all projects
mkdir -p "$(dirname "$f")"
[ -f "$f" ] && cp "$f" "$f.bak.$(date +%Y%m%d%H%M%S)"
python3 - "$f" << 'EOF'
import json, os, sys
path = sys.argv[1]
hook = {"type": "command", "command": "if grep -qE '\"command\"[[:space:]]*:[[:space:]]*\"(([^\"\\\\]|\\\\.)*([[:space:]/(;&|]|\\\\[tn]))?git([[:space:]]|\\\\t)(([^\"\\\\;&|]|\\\\[^n])*([[:space:]]|\\\\t))?((commit|push|merge|rebase|pull|am|cherry-pick|revert)([[:space:]]|\\\\t)(([^\"\\\\;&|]|\\\\[^n])*([[:space:]]|\\\\t))?--no-(ver(i[a-z]*)?|g[a-z-]*)([[:space:]=;&|)\"]|\\\\)|commit([[:space:]]|\\\\t)(([^\"\\\\;&|]|\\\\[^n])*([[:space:]]|\\\\t))?-[a-zA-Z]*n)'; then echo 'BLOCKED: --no-verify and --no-gpg-sign flags are not allowed. Run the commit without bypass flags so that pre-commit hooks execute properly.' >&2; exit 2; fi"}
settings = json.load(open(path)) if os.path.exists(path) else {}
entries = settings.setdefault("hooks", {}).setdefault("PreToolUse", [])
for entry in entries:
    entry["hooks"] = [h for h in entry.get("hooks", []) if "BLOCKED: --no-verify" not in h.get("command", "")]
entries[:] = [e for e in entries if e["hooks"]]
entries.append({"matcher": "Bash", "hooks": [hook]})
with open(path, "w") as out:
    json.dump(settings, out, indent=2)
    out.write("\n")
EOF
```

If the existing file isn't valid JSON, the script stops with an error before it writes anything. Fix the file and run the script again.

## Verification

Test that the hook blocks bypass flags:

```bash
# This should be blocked by the hook:
git commit --no-verify -m "test"

# This should succeed normally:
git commit -m "test"
```

## Extending the Hook

To block more commands, add another entry to the `PreToolUse` array rather than growing the pattern. This one blocks `git push --force` and `-f` but allows `--force-with-lease`:

```json
{
  "matcher": "Bash",
  "hooks": [
    {
      "type": "command",
      "command": "if grep -qE '\"command\"[[:space:]]*:[[:space:]]*\"(([^\"\\\\]|\\\\.)*([[:space:]/(;&|]|\\\\[tn]))?git([[:space:]]|\\\\t)(([^\"\\\\;&|]|\\\\[^n])*([[:space:]]|\\\\t))?push([[:space:]]|\\\\t)(([^\"\\\\;&|]|\\\\[^n])*([[:space:]]|\\\\t))?(--force|-[a-zA-Z]*f)([[:space:]=;&|)\"]|\\\\)'; then echo 'BLOCKED: force push is not allowed.' >&2; exit 2; fi"
    }
  ]
}
```

## Other harnesses

Codex, Cursor, Copilot and the other harnesses have no PreToolUse hook that can run this check. Use git and your code host instead:

1. **Git hooks**: Install the checks as `pre-commit` and `pre-push` hooks, for example with [pre-commit](https://pre-commit.com/) or a `core.hooksPath` directory. They run for every harness and for people. `--no-verify` skips them, so they can't be the only gate.
2. **Branch protection**: Run the same checks in CI and require them to pass before a merge into the protected branch, with direct pushes turned off. Require signed commits there if you sign them. A bypass flag then can't get code past the server.

## Best Practices

1. **Commit the settings file** -- Add `.claude/settings.json` to version control so all team members benefit from the hook.
2. **Pair with pre-commit hooks** -- The hook only ensures pre-commit hooks run; make sure they check something meaningful.
3. **Test after setup** -- Run the commands under [Verification](#verification).
