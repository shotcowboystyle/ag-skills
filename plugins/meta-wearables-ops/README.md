[Part of the shotcowboystyle marketplace](../../README.md)

## Meta Wearables Ops Plugin

**Version:** 0.3.0

Meta smart-glasses engineering — Wearables Device Access SDK integration on iOS and Android, camera, display, sensors, transport reliability, on-device compliance, and device-backed release proof.

Pairs with [`ios-ops`](../ios-ops/README.md), which owns general Apple-platform work.
Each works on its own.

## Installation

Part of the [ag-skills](../../README.md) marketplace. In Claude Code:

```bash
/plugin marketplace add shotcowboystyle/ag-skills
/plugin install meta-wearables-ops@claude-code-workflows
```

For Codex CLI, Cursor, OpenCode, Antigravity CLI, GitHub Copilot, and Pi, see
[docs/harnesses.md](../../docs/harnesses.md).

## Skills

Start with **meta-wearables-route-planner** for a new app or feature; it hands each lane to one owning skill.

| Skill | Owns |
| --- | --- |
| **meta-wearables-route-planner** | Route selection (DAT iOS/Android, native Display, Web Apps, phone fallback), app architecture, new-project intake |
| **meta-wearables-dat-integration** | Native DAT iOS and Android: packages and artifacts, configuration, registration, sessions, MockDevice, Android API atlas |
| **meta-wearables-sdk-audit** | Full-SDK coverage audits, iOS API atlas, source-pinned surface manifest and capability/evidence plan |
| **meta-wearables-device-capabilities** | Camera and audio, native Display, input and sensors, transport and runtime reliability |
| **meta-wearables-web-apps** | Ray-Ban Display Web Apps: 600×600 contract, focus and D-pad/EMG input, hosting, simulator vs physical evidence |
| **meta-wearables-implementation-recipes** | Swift, Kotlin/Java, and Web App starters for a selected API row and vertical slice |
| **meta-wearables-diagnostics** | First-failure diagnosis, operational readiness and recovery, device and version compatibility |
| **meta-wearables-trust-and-release** | On-device compliance, privacy and consent, identity/attestation/credentials, Developer Center projects and release channels |
| **meta-wearables-device-proof** | Target preflight and the mock → connected → physical evidence ledger |
| **meta-wearables-knowledge-base** | Reference library and shared rules the other skills cite (not a task skill) |

## Knowledge base

`skills/meta-wearables-knowledge-base/references/` ships with the plugin and is what the skills route into.
Skills link into it with relative paths that resolve inside the installed tree.
[`shared-rules.md`](skills/meta-wearables-knowledge-base/references/shared-rules.md) holds the evidence
ladder, device-label rules, and secrets policy every skill applies. Provenance lives in
`skills/meta-wearables-knowledge-base/references/sources/`, which records which upstream documents back the
corpus and when they were last checked (2026-08-22, DAT 0.9.0).

To refresh it after an SDK release, follow `references/sources/refresh-procedure.md`, run the two source
checkers in the knowledge-base skill's `scripts/` with `uv run`, update the affected documents, bump the
`last_verified` field of each skill, and rerun the quality gates.

## Scripts

Bundled scripts declare their dependencies inline (PEP 723). Run them with
`uv run <skill-dir>/scripts/<script>.py` from any directory; stock `python3` lacks PyYAML.

## Conventions

- **Cite or say you cannot.** Substantive claims trace to a knowledge-base document or to
  upstream documentation. Uncited claims are marked unverified.
- **Written is not verified.** Documentation says one thing; a device shows another. The
  two are never conflated.
- **Never invent a proof.** An unrun verification leaves its row empty.

## Author

Curtis Blanton — [shotcowboystyle.com](https://shotcowboystyle.com)

## License

MIT
