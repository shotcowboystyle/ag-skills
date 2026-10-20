#!/usr/bin/env bash
# run-tests.sh — exercise protect-mcp hooks against the fixtures in this directory.
#
# Requires: bash, node (>= 18), npx, python3. Fetches protect-mcp@0.31.1 and
# @veritasacta/verify@0.10.26 from the npm registry on first run, then caches them.
#
# Exit codes:
#   0   all tests passed
#   1   one or more tests failed
#   77  required tools missing (treated as "skipped" by automake / CI)

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
FIX="$SCRIPT_DIR/fixtures"
PM="protect-mcp@0.31.1"
VERIFY="@veritasacta/verify@0.10.26"

# --- Preflight ---------------------------------------------------------------

need() {
    command -v "$1" >/dev/null 2>&1 || {
        echo "SKIP: '$1' not found. Install Node.js 18+ (provides node and npx) and python3."
        exit 77
    }
}
need node
need npx
need python3

# Temp workspace for produced receipts. Cleaned at the end. npx runs from here,
# because npm refuses to run inside a repository whose package.json pins another
# package manager in devEngines.
WORKDIR="$(mktemp -d)"
trap 'rm -rf "$WORKDIR"' EXIT
cd "$WORKDIR"
RECEIPTS_DIR="$WORKDIR/receipts"

PASS=0
FAIL=0

if [ -t 1 ]; then
    GREEN='\033[0;32m'; RED='\033[0;31m'; NC='\033[0m'
else
    GREEN=''; RED=''; NC=''
fi

pass() { echo -e "${GREEN}PASS${NC}: $1"; PASS=$((PASS+1)); }
fail() { echo -e "${RED}FAIL${NC}: $1"; FAIL=$((FAIL+1)); }

check_exit() {
    local actual="$1" expected="$2" label="$3"
    if [ "$actual" -eq "$expected" ]; then pass "$label"; else fail "$label (exit $actual, expected $expected)"; fi
}

field() { python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); v=d[sys.argv[2]]; print(v if isinstance(v,str) else json.dumps(v))' "$1" "$2"; }

evaluate() { # policy fixture expected label
    npx --yes "$PM" evaluate --policy "$1" --tool "$(field "$2" tool_name)" --input "$(field "$2" tool_input)" >/dev/null 2>&1
    check_exit $? "$3" "$4"
}

# --- Tests 1-4: evaluate against the test policy -----------------------------
echo ""
echo "=== Tests 1-4: protect-mcp evaluate ==="
evaluate "$FIX/test-policy.cedar" "$FIX/pretool-allow-read.json" 0 "Read is permitted by test-policy.cedar"
evaluate "$FIX/test-policy.cedar" "$FIX/pretool-allow-bash-safe.json" 0 "Bash 'git status' is permitted"
evaluate "$FIX/test-policy.cedar" "$FIX/pretool-deny-bash-destructive.json" 2 "Bash 'rm -rf /' is denied with exit 2"
evaluate "$FIX/test-policy.cedar" "$FIX/pretool-deny-write.json" 2 "Write is denied with exit 2"

# --- Test 5: sign produces chained receipts ----------------------------------
echo ""
echo "=== Test 5: protect-mcp sign appends receipts ==="
# protect-mcp init generates keys/gateway.json under --dir.
npx --yes "$PM" init --dir "$WORKDIR/init" >/dev/null 2>&1
KEY="$WORKDIR/init/keys/gateway.json"
PUBKEY="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["publicKey"])' "$KEY" 2>/dev/null || true)"

SIGN_RC=0
for i in 1 2 3; do
    npx --yes "$PM" sign --receipts "$RECEIPTS_DIR/" --key "$KEY" < "$FIX/posttool-signing-input.json" >/dev/null 2>&1 || SIGN_RC=$?
done
CHAIN="$RECEIPTS_DIR/receipts.jsonl"
RECEIPT_FILE="$WORKDIR/receipt-latest.json"
if [ "$SIGN_RC" -eq 0 ] && [ "$(wc -l < "$CHAIN" 2>/dev/null || echo 0)" -eq 3 ]; then
    tail -n 1 "$CHAIN" > "$RECEIPT_FILE"
    pass "Three receipts appended to receipts.jsonl"
else
    RECEIPT_FILE=""
    fail "Sign did not append three receipts (exit $SIGN_RC)"
fi

# --- Test 6: receipt matches the expected shape ------------------------------
echo ""
echo "=== Test 6: Receipt schema validation ==="
if [ -n "$RECEIPT_FILE" ]; then
    python3 - "$RECEIPT_FILE" "$SCRIPT_DIR/expected/receipt-schema.json" "$FIX/posttool-signing-input.json" <<'PY'
import hashlib, json, sys
r = json.load(open(sys.argv[1]))
s = json.load(open(sys.argv[2]))
fixture = json.load(open(sys.argv[3]))
p = r.get("payload", {})
missing = [f for f in s["required"] if f not in r]
missing += [f"payload.{f}" for f in s["properties"]["payload"]["required"] if f not in p]
missing += [f"signature.{f}" for f in s["properties"]["signature"]["required"] if f not in r.get("signature", {})]
if missing:
    print(f"missing required fields: {missing}"); sys.exit(1)
if p["decision"] not in ("allow", "deny"):
    print(f"invalid decision: {p['decision']}"); sys.exit(1)
if not p.get("previousReceiptHash", "").startswith("sha256:"):
    print("third receipt has no previousReceiptHash"); sys.exit(1)
# The input hash is SHA-256 over the JCS form; for this flat ASCII input that
# equals sorted-key compact JSON.
want = hashlib.sha256(json.dumps(fixture["tool_input"], sort_keys=True, separators=(",", ":")).encode()).hexdigest()
if p.get("payload_digest", {}).get("input_hash") != want:
    print("input_hash does not match the fixture's tool_input"); sys.exit(1)
PY
    check_exit $? 0 "Receipt conforms to the schema, is chained, and hashes the input"
else
    fail "No receipt available to validate"
fi

# --- Tests 7-8: single-receipt verification ---------------------------------
echo ""
echo "=== Tests 7-8: Offline verification and tamper detection ==="
if [ -n "$RECEIPT_FILE" ]; then
    npx --yes "$VERIFY" "$RECEIPT_FILE" --key "$PUBKEY" >/dev/null 2>&1
    check_exit $? 0 "Valid receipt verifies with exit 0"

    TAMPERED="$WORKDIR/tampered.json"
    python3 -c '
import json, sys
r = json.load(open(sys.argv[1]))
# Flip the decision (a signed payload field). Signature will no longer validate.
r["payload"]["decision"] = "deny" if r["payload"]["decision"] == "allow" else "allow"
json.dump(r, open(sys.argv[2], "w"))
' "$RECEIPT_FILE" "$TAMPERED"
    npx --yes "$VERIFY" "$TAMPERED" --key "$PUBKEY" >/dev/null 2>&1
    check_exit $? 1 "Tampered receipt rejected with exit 1"
else
    fail "No receipt available to verify"
    fail "No receipt available to tamper with"
fi

# --- Tests 9-10: chain replay ------------------------------------------------
echo ""
echo "=== Tests 9-10: Chain replay ==="
if [ -n "$RECEIPT_FILE" ]; then
    npx --yes "$VERIFY" --replay-chain "$CHAIN" --key "$PUBKEY" >/dev/null 2>&1
    check_exit $? 0 "Intact chain verifies with exit 0"

    sed '2d' "$CHAIN" > "$WORKDIR/deleted.jsonl"
    npx --yes "$VERIFY" --replay-chain "$WORKDIR/deleted.jsonl" --key "$PUBKEY" >/dev/null 2>&1
    check_exit $? 1 "Chain with a deleted middle line rejected with exit 1"
else
    fail "No chain available to replay"
    fail "No chain available to cut"
fi

# --- Tests 11-13: hooks.json commands with the payload on stdin -------------
# Claude Code runs the command string from hooks.json with the event JSON on
# stdin and sets no TOOL_NAME variable. Run the exact command the same way.
hook_cmd() { python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["hooks"][sys.argv[2]][0]["hooks"][0]["command"])' "$PLUGIN_ROOT/hooks/hooks.json" "$1"; }
PRE_CMD="$(hook_cmd PreToolUse)"
POST_CMD="$(hook_cmd PostToolUse)"
pre_hook() { # fixture expected label [env...]
    local fixture="$1" expected="$2" label="$3"; shift 3
    env CLAUDE_PLUGIN_ROOT="$PLUGIN_ROOT" "$@" bash -c "$PRE_CMD" < "$fixture" >/dev/null 2>&1
    check_exit $? "$expected" "$label"
}

echo ""
echo "=== Tests 11-13: hooks.json from a stdin payload ==="
pre_hook "$FIX/pretool-allow-read.json" 0 "hooks.json PreToolUse allows Read" PROTECT_MCP_POLICY="$FIX/test-policy.cedar"
pre_hook "$FIX/pretool-deny-write.json" 2 "hooks.json PreToolUse denies Write" PROTECT_MCP_POLICY="$FIX/test-policy.cedar"

HOOK_RECEIPTS="$WORKDIR/hook-receipts/"
CLAUDE_PLUGIN_ROOT="$PLUGIN_ROOT" PROTECT_MCP_RECEIPTS="$HOOK_RECEIPTS" PROTECT_MCP_KEY="$KEY" \
    bash -c "$POST_CMD" < "$FIX/posttool-signing-input.json" >/dev/null 2>&1
if grep -q '"tool_name":"Read"' "$HOOK_RECEIPTS/receipts.jsonl" 2>/dev/null \
    && grep -q '"input_hash"' "$HOOK_RECEIPTS/receipts.jsonl"; then
    pass "hooks.json PostToolUse wrote a receipt naming Read with an input hash"
else
    fail "hooks.json PostToolUse did not write a receipt for Read"
fi

# --- Test 14: an evaluator that cannot run must block, not fail open ----------
# Simulate npx failing to execute (exit 126, as when a huge tool input exceeds the
# argument-length limit). The hook must map that to exit 2.
echo ""
echo "=== Test 14: hooks.json PreToolUse blocks when the evaluator cannot run ==="
FAKE_BIN="$WORKDIR/fakebin"; mkdir -p "$FAKE_BIN"
printf '#!/bin/sh\nexit 126\n' > "$FAKE_BIN/npx"; chmod +x "$FAKE_BIN/npx"
pre_hook "$FIX/pretool-allow-read.json" 2 "evaluator exit 126 is mapped to a blocking exit 2" \
    PATH="$FAKE_BIN:$PATH" PROTECT_MCP_POLICY="$FIX/test-policy.cedar"

# --- Tests 15-16: missing policy file ----------------------------------------
echo ""
echo "=== Tests 15-16: Missing policy file ==="
pre_hook "$FIX/pretool-allow-read.json" 0 "missing policy allows by default" PROTECT_MCP_POLICY="$WORKDIR/none.cedar"
pre_hook "$FIX/pretool-allow-read.json" 2 "missing policy denies with PROTECT_MCP_FAIL_CLOSED=1" \
    PROTECT_MCP_POLICY="$WORKDIR/none.cedar" PROTECT_MCP_FAIL_CLOSED=1

# --- Test 17: the starter policy in SKILL.md ---------------------------------
echo ""
echo "=== Test 17: Starter policy from SKILL.md ==="
STARTER="$WORKDIR/starter.cedar"
python3 - "$PLUGIN_ROOT/skills/protect-mcp-setup/SKILL.md" "$STARTER" <<'PY'
import re, sys
text = open(sys.argv[1]).read()
block = re.search(r"## Cedar Policy File.*?```cedar\n(.*?)```", text, re.S).group(1)
open(sys.argv[2], "w").write(block.replace("/path/to/project", "/proj"))
PY
while IFS='|' read -r expected tool input; do
    npx --yes "$PM" evaluate --policy "$STARTER" --tool "$tool" --input "$input" >/dev/null 2>&1
    check_exit $? "$expected" "starter: $tool $input"
done <<'CASES'
0|Read|{"file_path":"/proj/README.md"}
2|Read|{"file_path":"/proj/protect-mcp.key"}
2|Read|{"file_path":"/proj/.env.local"}
2|Read|{"file_path":"/home/u/.ssh/id_ed25519"}
2|Grep|{"pattern":"k","path":"/proj/protect-mcp.key"}
0|Bash|{"command":"git status"}
2|Bash|{"command":"cat protect-mcp.key"}
2|Bash|{"command":"git diff --no-index /dev/null /proj/protect-mcp.key"}
0|Write|{"file_path":"/proj/src/a.ts","content":"x"}
2|Write|{"file_path":"/proj/protect.cedar","content":"x"}
2|Edit|{"file_path":"/proj/.claude/settings.json"}
2|Write|{"file_path":"/proj/receipts/receipts.jsonl","content":"x"}
CASES

# --- Summary ----------------------------------------------------------------
echo ""
echo "─────────────────────────────────────────────"
echo "  $PASS passed, $FAIL failed"
echo "─────────────────────────────────────────────"
[ "$FAIL" -eq 0 ]
