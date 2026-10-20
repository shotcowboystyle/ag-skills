---
name: protect-mcp-setup
description: Configure Cedar policy enforcement and Ed25519 signed receipts for Claude Code tool calls. Use when setting up projects that need a signed audit trail, policy-gated tool execution, or evidence of which tools an agent ran.
last_verified: 2026-10-20
---

# protect-mcp — Policy Enforcement + Signed Receipts

Each Claude Code tool call is evaluated against a Cedar policy before it runs,
and each call that runs gets an Ed25519-signed receipt that can be verified
offline with your public key.

**Claude Code only.** Enforcement and signing run in Claude Code's
`PreToolUse` and `PostToolUse` hooks. Other coding tools get this skill, the
agents, and the commands, which can write policies and verify receipts, but
nothing there evaluates a policy or signs a receipt.

## Overview

Claude Code runs powerful tools: `Bash`, `Edit`, `Write`, `WebFetch`. By
default there is no policy gate and no signed record of what ran.
`protect-mcp` adds both:

- **Cedar policies** evaluate every tool call before execution. A call runs
  only when at least one `permit` matches and no `forbid` matches.
- **Ed25519 receipts** record the tool name and a SHA-256 of the tool input,
  each linked to the previous receipt by hash.
- **Offline verification** with `npx @veritasacta/verify` and your public key.
  No server and no account.

Read [Threat model](#threat-model) before relying on the receipts as evidence.

## Setup

```bash
# 1. Install the plugin. This registers both hooks.
claude plugin marketplace add shotcowboystyle/ag-skills
claude plugin install protect-mcp@claude-code-workflows

# 2. Create ./protect.cedar from the starter policy below.

# 3. Create the signing key once. An existing key is never replaced.
#    See references/receipt-format.md to rotate it.
if [ ! -e ./protect-mcp.key ]; then
  d=$(mktemp -d) && npx protect-mcp@0.31.1 init --dir "$d" && mv "$d/keys/gateway.json" ./protect-mcp.key
fi
chmod 600 ./protect-mcp.key
grep -qxF '/protect-mcp.key' .gitignore 2>/dev/null || echo '/protect-mcp.key' >> .gitignore

# 4. Use Claude Code normally. Every tool call is policy-evaluated and
#    produces a signed receipt in ./receipts/receipts.jsonl.
```

## Hook Configuration

Installing the plugin adds both hooks from `hooks/hooks.json`, each running a
script bundled with the plugin. Claude Code passes the hook event to the command as JSON on stdin.
`evaluate.sh` reads `tool_name` and `tool_input` from it and runs
`protect-mcp evaluate`. `sign.sh` passes the payload to `protect-mcp sign`.

| Variable | Default | Effect |
|---|---|---|
| `PROTECT_MCP_POLICY` | `./protect.cedar` | Policy file |
| `PROTECT_MCP_RECEIPTS` | `./receipts/` | Directory for `receipts.jsonl` |
| `PROTECT_MCP_KEY` | `./protect-mcp.key` | Signing key |
| `PROTECT_MCP_FAIL_CLOSED` | unset | `1` denies every call when the policy file is missing |

When the policy file is missing, the hook prints a warning and **allows every
call**. Set `PROTECT_MCP_FAIL_CLOSED=1` in the shell that starts Claude Code to
deny instead. Create the policy file first: with fail-closed set and no policy,
Claude cannot write one for you. A policy file that does not parse denies
every call either way. The evaluator also denies when it cannot run.

**PreToolUse** runs before the tool. If Cedar denies the call, the hook exits 2
and Claude Code blocks it.

**PostToolUse** runs after the tool completes and appends a signed receipt. It
does not record the tool output.

## Cedar Policy File

Cedar denies by default. A call is allowed when at least one `permit` matches
and no `forbid` matches. A matching `forbid` always wins, so the forbids below
hold even if you add broader permits later.

Create `./protect.cedar` at the project root and replace `/path/to/project`
with the project's absolute path:

```cedar
// Read-only tools. Add WebFetch with your own URL rule.
permit (principal, action == Action::"MCP::Tool::call", resource) when {
    resource == Tool::"Read" || resource == Tool::"Glob" || resource == Tool::"Grep"
};

// Never read the signing key, .env files, or SSH keys. Grep and Glob take
// `path`; keep the key gitignored as well, since Grep skips gitignored files.
forbid (principal, action == Action::"MCP::Tool::call", resource) when {
    (resource == Tool::"Read" || resource == Tool::"Grep" || resource == Tool::"Glob") &&
    context has input &&
    ((context.input has file_path &&
      (context.input.file_path like "*protect-mcp.key*" ||
       context.input.file_path like "*.env*" || context.input.file_path like "*.ssh*")) ||
     (context.input has path &&
      (context.input.path like "*protect-mcp.key*" ||
       context.input.path like "*.env*" || context.input.path like "*.ssh*")))
};

// Shell: read-only git subcommands and a few harmless built-ins. No `cat`:
// use Read, which the forbid above covers. No interpreter or package-manager
// prefix (`npm`, `node`, `python`, `make`): they run arbitrary code.
permit (principal, action == Action::"MCP::Tool::call", resource == Tool::"Bash") when {
    context has input && context.input has command &&
    (context.input.command like "git status*" || context.input.command like "git diff*" ||
     context.input.command like "git log*" || context.input.command like "git show*" ||
     context.input.command like "ls*" || context.input.command like "pwd*" ||
     context.input.command like "echo *" || context.input.command like "test *")
};

// No chaining (`&` also denies `2>&1`), `$` expansion, redirection (`>` or
// `<`, which covers `<(`), file output (`git diff --output`), reads outside
// git (`git diff --no-index`), rm -rf, or naming the secrets above
forbid (principal, action == Action::"MCP::Tool::call", resource == Tool::"Bash") when {
    context has input && context.input has command &&
    (context.input.command like "*;*" || context.input.command like "*&*" ||
     context.input.command like "*|*" || context.input.command like "*$*" ||
     context.input.command like "*`*" || context.input.command like "*>*" ||
     context.input.command like "*<*" || context.input.command like "*\n*" ||
     context.input.command like "*--output*" || context.input.command like "*--no-index*" ||
     context.input.command like "*rm -rf*" || context.input.command like "*protect-mcp.key*" ||
     context.input.command like "*.env*" || context.input.command like "*.ssh*")
};

// Writes only inside the project (paths are absolute), never via `..`
permit (principal, action == Action::"MCP::Tool::call", resource) when {
    (resource == Tool::"Write" || resource == Tool::"Edit") &&
    context has input && context.input has file_path &&
    context.input.file_path like "/path/to/project/*"
};

// Never write the policy, the key, the receipts, secrets, or Claude Code
// settings (which can turn the hooks off)
forbid (principal, action == Action::"MCP::Tool::call", resource) when {
    (resource == Tool::"Write" || resource == Tool::"Edit") &&
    context has input && context.input has file_path &&
    (context.input.file_path like "*/../*" || context.input.file_path like "*/.." ||
     context.input.file_path like "*protect.cedar*" ||
     context.input.file_path like "*protect-mcp.key*" ||
     context.input.file_path like "*/receipts/*" ||
     context.input.file_path like "*.env*" || context.input.file_path like "*.ssh*" ||
     context.input.file_path like "*/.claude/*")
};
```

String matching is best-effort. `like` checks the raw string, not a resolved
path or a parsed command, so a symlink or a reworded command can get past a
rule. To allow a project command such as `npm test`, permit it by exact
prefix, and remember that it runs whatever the project's files say, which the
agent can edit.

## Verification

Verify every receipt against the public key in `./protect-mcp.key`:

```bash
PUB=$(node -p 'JSON.parse(require("fs").readFileSync("./protect-mcp.key")).publicKey')
npx @veritasacta/verify@0.10.26 --replay-chain ./receipts/receipts.jsonl --key "$PUB"
# Exit 0 = every signature and chain link verified
# Exit 1 = a receipt failed: tampered, wrong key, or a deleted or reordered line
# Exit 2 = could not verify: unreadable file, malformed line, or no key
```

Always pass `--key`. Each receipt carries a `public_key` field, and without
`--key` the verifier checks the signature against that embedded key, so a
receipt signed with any key passes.

The plugin's slash commands do the same inside Claude Code. `/verify-receipt`
takes one receipt in its own file, e.g., from
`tail -n 1 ./receipts/receipts.jsonl > receipt.json`.

```
/verify-receipt receipt.json
/audit-chain --last 20
```

`npx` downloads the verifier on first use. Run
`npm install --no-save @veritasacta/verify@0.10.26` in the project before you
go offline.

## Receipt Format

Each receipt is one line of `./receipts/receipts.jsonl`, holding the tool name,
a SHA-256 of the tool input, and a hash link to the previous line. See
[`references/receipt-format.md`](references/receipt-format.md).

## Threat Model

A receipt that verifies shows that someone holding the key signed it, that it
was not changed, and that no line between the first and last was deleted. It
does not show that the file is complete at the end, what the tool returned, or
that the agent did not sign receipts itself after reading the key. Read
[`references/threat-model.md`](references/threat-model.md) before relying on
receipts as evidence.

## Related

- **npm**: [protect-mcp](https://www.npmjs.com/package/protect-mcp)
- **Verify CLI**: [@veritasacta/verify](https://www.npmjs.com/package/@veritasacta/verify)
- **Source**: [github.com/ScopeBlind/scopeblind-gateway](https://github.com/ScopeBlind/scopeblind-gateway)
- **Protocol**: [veritasacta.com](https://veritasacta.com)
