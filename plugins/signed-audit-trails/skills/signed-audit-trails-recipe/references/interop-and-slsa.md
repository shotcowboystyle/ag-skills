# Interop and SLSA composition for the signed audit trail recipe

Detail behind the interop and SLSA notes in `SKILL.md`.

## Cross-implementation interop

The receipt format has four independent implementations today:

| Implementation | Language | Use case |
|----------------|----------|----------|
| [protect-mcp](https://www.npmjs.com/package/protect-mcp) | TypeScript | Claude Code, Cursor, MCP hosts |
| [protect-mcp-adk](https://pypi.org/project/protect-mcp-adk/) | Python | Google Agent Development Kit |
| [sb-runtime](https://github.com/ScopeBlind/sb-runtime) | Rust | OS-level sandbox (Landlock + seccomp) |
| APS governance hook | Python | CrewAI, LangChain |

A receipt produced by any of them verifies against
[`@veritasacta/verify`](https://www.npmjs.com/package/@veritasacta/verify).
The auditor does not need to trust the operator's tooling choice: the format
is the contract.

## Composition with SLSA provenance for agent-built software

When Claude Code builds and releases software (running `npm install`,
`npm build`, `npm publish` as tool calls), the receipt chain is the
per-step build log. SLSA Provenance v1 has an extension point for this: the
`byproducts` field can reference the receipt chain alongside the build
attestation.

The [agent-commit build type](https://refs.arewm.com/agent-commit/v0.2)
documents the pattern using the ResourceDescriptor shape:

```json
{
  "name": "decision-receipts",
  "digest": { "sha256": "..." },
  "uri": "oci://registry/org/build-xyz/receipts:sha256-...",
  "annotations": {
    "predicateType": "https://veritasacta.com/attestation/decision-receipt/v0.1",
    "signerRole": "supervisor-hook"
  }
}
```

The SLSA provenance is signed by the builder identity; the receipt
attestation is signed by the supervisor-hook identity. Two trust domains,
cross-referenced at the byproduct layer. See
[slsa-framework/slsa#1594](https://github.com/slsa-framework/slsa/issues/1594)
for the composition discussion.

## References

- [`draft-farley-acta-signed-receipts`](https://datatracker.ietf.org/doc/draft-farley-acta-signed-receipts/) — IETF draft, receipt wire format
- [RFC 8032](https://datatracker.ietf.org/doc/html/rfc8032) — Ed25519
- [RFC 8785](https://datatracker.ietf.org/doc/html/rfc8785) — JCS
- [Cedar policy language](https://docs.cedarpolicy.com/)
- [protect-mcp on npm](https://www.npmjs.com/package/protect-mcp)
- [@veritasacta/verify on npm](https://www.npmjs.com/package/@veritasacta/verify)
- [in-toto/attestation#549](https://github.com/in-toto/attestation/pull/549) — Decision Receipt predicate proposal
- [agent-commit build type](https://refs.arewm.com/agent-commit/v0.2) — SLSA provenance for agent-produced commits
- [Microsoft Agent Governance Toolkit](https://github.com/microsoft/agent-governance-toolkit) (`examples/protect-mcp-governed/`)
- [AWS Cedar for Agents](https://github.com/cedar-policy/cedar-for-agents)
