# Receipt format written by protect-mcp 0.31.1

The plugin's `sign.sh` hook passes the hook payload to
`protect-mcp@0.31.1 sign`, which appends one receipt per line to
`./receipts/receipts.jsonl`. Each line looks like this one:

```json
{
  "payload": {
    "type": "protectmcp:decision",
    "tool_name": "Bash",
    "decision": "allow",
    "reason": "post_execution_receipt",
    "policy_digest": "none",
    "scope": "tu-1792528984317-uahv",
    "mode": "enforce",
    "request_id": "tu-1792528984317-uahv",
    "spec": "draft-farley-acta-signed-receipts-03",
    "issuer_certification": "self-signed",
    "public_key": "58af98eea75750d25bc6fe819a0f1d591239f4d5380974afebfb933d342cdf36",
    "issuer_name": "protect-mcp",
    "previousReceiptHash": "sha256:383f58ca0f2dbd82458640ef5775da54a6df9acd57464abcff1e08839e6895c2",
    "payload_digest": {
      "input_hash": "4cf29611a66934862f29acfcc817e30b905c1ab73d5e65831413eb6b454d49db",
      "input_size": 16,
      "canonical": "jcs"
    },
    "issued_at": "2026-10-20T20:43:04.317Z",
    "issuer_id": "generated"
  },
  "signature": {
    "alg": "EdDSA",
    "kid": "generated",
    "sig": "910b9e2471e4a7dd..."
  }
}
```

- `payload_digest.input_hash` is the SHA-256 of the JCS-canonical tool input.
  The input itself and the tool output are not recorded. To check a claim
  about what ran, canonicalize the input you expect and compare hashes.
- `previousReceiptHash` links the receipt to the line before it. The first
  receipt in a file has none. `--replay-chain` reports a deleted, inserted, or
  reordered line as `chain_break`. It cannot tell that lines were removed from
  the end of the file.
- The signature covers the whole payload, so changing any payload field after
  signing makes verification fail.
- `public_key` is the signer's claim about itself. Always verify with
  `--key` set to the `publicKey` value from your own `./protect-mcp.key`.
  Without `--key`, the verifier uses the embedded key, and a receipt signed
  with any key passes.
- When the key file is missing, `sign` still appends a line, with
  `"signed": false` and no signature. Verification rejects it.

## Rotating the signing key

Each receipts file verifies against one public key, so the setup command
never replaces an existing `./protect-mcp.key`. To rotate the key, first move
`./protect-mcp.key` and `./receipts/receipts.jsonl` to an archive, then run
the setup command again. Verify the archived receipts with the old public
key and the new receipts with the new one.

## Receipts from protect-mcp 0.7.x

Earlier versions of this plugin signed with protect-mcp 0.7.4, which wrote a
`v: 2` envelope with no chain link and no input hash. `@veritasacta/verify@0.10.26`
still checks their signatures. Move the old `receipts.jsonl` to an archive
before you upgrade, so the new chain starts in a fresh file.
