# protect-mcp

Cedar policy enforcement + Ed25519 signed receipts for every Claude Code tool call.

[![npm version](https://img.shields.io/npm/v/protect-mcp)](https://www.npmjs.com/package/protect-mcp)
[![Downloads](https://img.shields.io/npm/dm/protect-mcp)](https://www.npmjs.com/package/protect-mcp)
[![License](https://img.shields.io/badge/license-MIT-blue)](../../LICENSE)

Every Claude Code tool call is evaluated against a Cedar policy before it
runs, and every call that runs gets an Ed25519-signed receipt that can be
verified offline with your public key.

**Claude Code only.** Enforcement and signing run in Claude Code's
`PreToolUse` and `PostToolUse` hooks. Other coding tools get the skill, agents,
and commands, which can write policies and verify receipts, but nothing there
evaluates a policy or signs a receipt.

## What You Get

- **Cedar policy enforcement**: block tool calls that violate your rules before they execute. A call runs only when at least one `permit` matches and no `forbid` matches.
- **Ed25519 signed receipts**: every tool call that runs gets a receipt holding the tool name and a SHA-256 of its input, signed over the RFC 8785 JCS canonical payload.
- **Chained receipts file**: receipts are appended to `./receipts/receipts.jsonl`, each linked to the previous one by hash, so a modified, deleted, or reordered line fails verification. Lines cut from the end of the file are not detected.
- **Offline verification**: `npx @veritasacta/verify@0.10.26 --replay-chain` with your public key needs no vendor lookup or account. `npx` downloads the verifier on first use, so run `npm install --no-save @veritasacta/verify@0.10.26` in the project before you go offline.

Receipts are evidence against later tampering by someone without the key. They
are not proof against the agent itself: the hook and the agent run as the same
OS user. See the threat model in
[`skills/protect-mcp-setup/references/threat-model.md`](skills/protect-mcp-setup/references/threat-model.md).

## Quick Start

```bash
# 1. Install this plugin. This registers the hooks.
claude plugin marketplace add shotcowboystyle/ag-skills
claude plugin install protect-mcp@claude-code-workflows

# 2. Create ./protect.cedar from the starter policy in
#    skills/protect-mcp-setup/SKILL.md. With no policy file every call is
#    allowed; set PROTECT_MCP_FAIL_CLOSED=1 to deny instead.

# 3. Create the signing key once. An existing key is never replaced. To rotate
#    it, archive the key and receipts.jsonl first.
if [ ! -e ./protect-mcp.key ]; then
  d=$(mktemp -d) && npx protect-mcp@0.31.1 init --dir "$d" && mv "$d/keys/gateway.json" ./protect-mcp.key
fi
chmod 600 ./protect-mcp.key
grep -qxF '/protect-mcp.key' .gitignore 2>/dev/null || echo '/protect-mcp.key' >> .gitignore

# 4. Run Claude Code normally. Every tool call is now policy-evaluated
#    and produces a signed receipt in ./receipts/
```

## What's Included

```
plugins/protect-mcp/
├── skills/protect-mcp-setup/SKILL.md     — Full setup and usage guide
├── agents/policy-enforcer.md              — Cedar policy author (Opus)
├── agents/receipt-verifier.md             — Chain verification expert (Sonnet)
├── commands/verify-receipt.md             — /verify-receipt <path>
├── commands/audit-chain.md                — /audit-chain [--last N]
└── hooks/hooks.json                       — PreToolUse + PostToolUse hooks
```

## How It Works

```
┌─────────────────────────────────────────────┐
│        Claude Code tool call                │
│   (Bash, Edit, Write, Read, WebFetch...)    │
└────────────────┬────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────┐
│  PreToolUse hook → Cedar policy evaluation  │
│                                             │
│  permit / forbid based on:                  │
│    - principal (the agent)                  │
│    - action (the tool)                      │
│    - resource (the target)                  │
│    - context (command patterns, paths, etc) │
│                                             │
│  Cedar deny → exit 2, tool blocked          │
│  Cedar permit → tool executes               │
└────────────────┬────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────┐
│         Tool executes (or doesn't)          │
└────────────────┬────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────┐
│  PostToolUse hook → Ed25519 signed receipt  │
│                                             │
│  Receipt payload fields:                    │
│    - tool_name, decision, request_id        │
│    - payload_digest.input_hash (SHA-256)    │
│    - previousReceiptHash (chain link)       │
│    - public_key, issued_at                  │
│  signature over the whole payload           │
│                                             │
│  Appended to ./receipts/receipts.jsonl      │
└─────────────────────────────────────────────┘
```

## Cedar Policy

The starter policy in
[`skills/protect-mcp-setup/SKILL.md`](skills/protect-mcp-setup/SKILL.md#cedar-policy-file)
allows read-only tools and a few read-only shell commands, forbids reading the
signing key, `.env*` and `~/.ssh`, and forbids writes to the policy, the key,
the receipts and `.claude/`. `test/run-tests.sh` checks it.

Ask the `policy-enforcer` agent to help you author policies for your
project's threat model.

## Verification

Every receipt can be verified by any party, offline, with the `publicKey`
value from `./protect-mcp.key`:

```bash
PUB=$(node -p 'JSON.parse(require("fs").readFileSync("./protect-mcp.key")).publicKey')
npx @veritasacta/verify@0.10.26 --replay-chain ./receipts/receipts.jsonl --key "$PUB"
# Exit 0 = every signature and chain link verified
# Exit 1 = a receipt failed: tampered, wrong key, or a deleted or reordered line
# Exit 2 = could not verify: unreadable file, malformed line, or no key
```

Always pass `--key`. Without it the verifier trusts the `public_key` field in
each receipt, so a receipt signed with any key passes.

Use the `receipt-verifier` agent for help interpreting verification failures.

## Standards

- **Ed25519** — [RFC 8032](https://datatracker.ietf.org/doc/html/rfc8032)
- **JCS** — [RFC 8785](https://datatracker.ietf.org/doc/html/rfc8785)
- **Cedar** — [AWS's open authorization engine](https://www.cedarpolicy.com/)
- **IETF Internet-Draft** — [draft-farley-acta-signed-receipts](https://datatracker.ietf.org/doc/draft-farley-acta-signed-receipts/)

## Related

- **npm**: [protect-mcp](https://www.npmjs.com/package/protect-mcp)
- **Verification CLI**: [@veritasacta/verify](https://www.npmjs.com/package/@veritasacta/verify)
- **Cedar integration**: Contributor to [cedar-policy/cedar-for-agents](https://github.com/cedar-policy/cedar-for-agents) (PR #64 merged)
- **Microsoft AGT**: Integrated in [microsoft/agent-governance-toolkit](https://github.com/microsoft/agent-governance-toolkit) (PR #667 merged)
- **Source**: [github.com/ScopeBlind/scopeblind-gateway](https://github.com/ScopeBlind/scopeblind-gateway)
- **Protocol docs**: [veritasacta.com](https://veritasacta.com)

## License

MIT. See [LICENSE](../../LICENSE).
