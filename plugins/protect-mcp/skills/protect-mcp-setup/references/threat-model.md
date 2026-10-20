# protect-mcp threat model

What a receipt that verifies against your public key shows:

- Someone holding the private key signed that payload, and no signed field
  changed afterward.
- The tool named in it ran, with an input whose SHA-256 matches
  `input_hash`. Hash the input you expect and compare.
- Lines between the first and last were not deleted, inserted, or reordered:
  `--replay-chain` reports a broken link.

What it does not show:

- **That the record is complete.** Lines removed from the end of the file, or
  the whole file, leave a valid chain. Copy receipts somewhere the agent and
  operator cannot write, and compare line counts.
- **What the tool returned.** The output is not recorded.
- **That the agent did not forge it.** The hooks and the agent run as the same
  OS user, so the key the hook reads is a file the agent could read through any
  gap in the policy, such as a permitted interpreter, a project script it can
  edit, or a reworded shell command. The starter policy blocks the obvious
  paths and is not a guarantee. Receipts protect against later tampering by
  someone without the key, not against a compromised session.
- **That a denied call was attempted.** Only calls that ran get a receipt.
- **That the policy was enforced.** With no policy file and
  `PROTECT_MCP_FAIL_CLOSED` unset, every call is allowed and still signed.
