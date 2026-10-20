#!/usr/bin/env bash
# PostToolUse hook for protect-mcp.
#
# Passes the stdin payload to protect-mcp, which signs a receipt holding the
# tool name and a SHA-256 of the tool input, linked to the previous receipt by
# hash, and appends it to receipts.jsonl. PostToolUse hooks never block the
# tool call.
set -uo pipefail

exec npx protect-mcp@0.31.1 sign \
  --receipts "${PROTECT_MCP_RECEIPTS:-./receipts/}" \
  --key "${PROTECT_MCP_KEY:-./protect-mcp.key}"
