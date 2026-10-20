# protect-mcp test fixtures

Round-trip tests for the `protect-mcp` plugin's `PreToolUse` and `PostToolUse`
hooks. Exercises the full evaluate → sign → verify loop against deterministic
fixtures, including the tamper-detection path.

## Layout

```
test/
├── fixtures/
│   ├── test-policy.cedar                  # Cedar policy used by all tests
│   ├── pretool-allow-read.json            # Read should be permitted
│   ├── pretool-allow-bash-safe.json       # Bash "git status" should be permitted
│   ├── pretool-deny-bash-destructive.json # Bash "rm -rf /" should be denied
│   ├── pretool-deny-write.json            # Write should be denied
│   └── posttool-signing-input.json        # Input for receipt signing
├── expected/
│   └── receipt-schema.json                # Expected receipt shape (JSON Schema)
├── run-tests.sh                           # Full round-trip (requires node / npx)
└── verify-fixtures.sh                     # Static validation (python3 only)
```

## Running

### Full round-trip (local development)

```bash
./run-tests.sh
```

Requires `node` (>= 18), `npx`, and `python3`. Fetches `protect-mcp@0.31.1`
and `@veritasacta/verify@0.10.26` from npm on first run. Runs `npx` from a temp
directory, because npm refuses to run inside a repository whose `package.json`
pins another package manager in `devEngines`.

| # | Scenario | Expected exit |
|---|----------|----------------|
| 1-2 | `evaluate` on `Read`, `Bash git status`         | 0 (permit)  |
| 3-4 | `evaluate` on `Bash rm -rf /`, `Write`          | 2 (forbid)  |
| 5 | `sign` appends three receipts                     | 0 (success) |
| 6 | Receipt has the schema's fields, a chain link, and the input hash | 0 (valid) |
| 7 | `@veritasacta/verify` accepts the receipt         | 0 (valid)   |
| 8 | Tampered receipt is rejected                      | 1 (tampered)|
| 9 | `--replay-chain` accepts the intact chain          | 0 (valid)   |
| 10 | `--replay-chain` rejects a deleted middle line    | 1 (chain break) |
| 11-12 | `hooks.json` PreToolUse on `Read` / `Write`, payload on stdin | 0 / 2 |
| 13 | `hooks.json` PostToolUse, payload on stdin         | receipt written |
| 14 | `hooks.json` PreToolUse when `npx` cannot run      | 2 (forbid)  |
| 15-16 | Missing policy, default / `PROTECT_MCP_FAIL_CLOSED=1` | 0 / 2 |
| 17 | The starter policy in `SKILL.md` against secret reads and protected writes | 0 / 2 per case |

Test 8 is the critical regression guard: flipping the `decision` field in a
signed receipt must invalidate the Ed25519 signature, so `@veritasacta/verify`
must exit 1 rather than 0.

### Static validation (CI-safe)

```bash
./verify-fixtures.sh
```

Only requires `python3`. Validates that every fixture is well-formed JSON and
has the expected structure. No network calls, no npm fetches. Safe to run in
sandboxed or offline CI.

## What the tests prove

- **Policy evaluation:** Cedar `permit` and `forbid` rules produce the
  expected exit codes (0 / 2).
- **Receipt schema:** signed receipts include every required field from
  [`draft-farley-acta-signed-receipts`](https://datatracker.ietf.org/doc/draft-farley-acta-signed-receipts/).
- **Signature integrity:** `@veritasacta/verify` validates authentic
  receipts and rejects tampered ones, with the documented exit codes.
- **Chain integrity:** a deleted middle line breaks the chain. A line cut
  from the end does not, and no test claims otherwise.
- **Starter policy:** the policy users copy from `SKILL.md` blocks reads of
  the key, `.env*` and `~/.ssh`, and writes to the policy, key, receipts and
  `.claude/`.
- **End-to-end integration:** the plugin's two hooks compose into a
  working allow/deny + sign + verify pipeline.

## Extending

To add a new test case:

1. Drop a `pretool-*.json` or `posttool-*.json` fixture into `fixtures/`
2. Add a matching rule to `fixtures/test-policy.cedar` if the test needs one
3. Add an assertion block to `run-tests.sh` mirroring the existing ones

Follow the naming convention `pretool-<allow|deny>-<scenario>.json` so the
intent is obvious from `ls fixtures/`.

## Exit codes

| Script             | Exit | Meaning |
|--------------------|------|---------|
| `run-tests.sh`     | 0    | All tests passed |
| `run-tests.sh`     | 1    | One or more tests failed |
| `run-tests.sh`     | 77   | Required tool missing (skipped in CI) |
| `verify-fixtures.sh` | 0  | All fixtures valid |
| `verify-fixtures.sh` | 1  | Fixture malformed |
| `verify-fixtures.sh` | 77 | `python3` missing (skipped) |

77 is the autotools convention for "skip this test" and is interpreted as a
skip by most CI frameworks.
