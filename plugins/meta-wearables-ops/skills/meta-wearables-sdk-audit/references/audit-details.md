# Meta Wearables SDK audit — details

## Read when the request mentions…

| Wording in the request | Read |
| --- | --- |
| IMU, EMG, temple, browser sensor, Display input | [Input, sensors, and physical interaction](../../meta-wearables-knowledge-base/references/70-meta-wearables/24-input-sensors-and-physical-interaction.md) |
| Gen 2/Gen 3, firmware, companion versions, support tables | [Version-dependency and device-compatibility evidence](../../meta-wearables-knowledge-base/references/70-meta-wearables/26-version-dependency-and-device-compatibility-evidence.md) |
| processing location, consent, raw data, thermal, retention | [On-device compliance and runtime contract](../../meta-wearables-knowledge-base/references/70-meta-wearables/17-on-device-compliance-and-runtime-contract.md) |
| firmware, on-glasses DAT-app provisioning, Developer Mode vs release channel, recovery | [Operational readiness and recovery](../../meta-wearables-knowledge-base/references/70-meta-wearables/18-operational-readiness-and-recovery.md) |
| iOS + Android + Display + Web Apps, shared state, phone fallback | [Application architecture and platform boundaries](../../meta-wearables-knowledge-base/references/70-meta-wearables/19-application-architecture-and-platform-boundaries.md) |
| app identity, permission rationale, versions, testers, telemetry | [Developer Center project and release operations](../../meta-wearables-knowledge-base/references/70-meta-wearables/21-developer-center-project-and-release-operations.md) |
| identity keys, callbacks, attestation, signing, Web App origin, App Store gates | [Security, attestation, and credential boundaries](../../meta-wearables-knowledge-base/references/70-meta-wearables/25-security-attestation-and-credential-boundaries.md) |
| Wi-Fi/local network, Bluetooth, HFP/A2DP, backpressure, latency, recovery | [Transport, audio, and runtime reliability](../../meta-wearables-knowledge-base/references/70-meta-wearables/22-transport-audio-and-runtime-reliability.md) |
| a DAT failure, DAT Inspector/MCP, event or error diagnosis | [Debugging, observability, and diagnostic evidence](../../meta-wearables-knowledge-base/references/70-meta-wearables/23-debugging-observability-and-diagnostic-evidence.md) |
| overall progress or "full SDK" readiness | [Completion audit and next proof](../../meta-wearables-knowledge-base/references/70-meta-wearables/32-completion-audit-and-next-proof.md) |

## Module inventory

Inventory runtime modules per platform before comparing concepts:

- iOS: `MWDATCore`, `MWDATCamera`, `MWDATDisplay`, `MWDATMockDevice`, and the
  test-only `MWDATMockDeviceTestClient`.
- Android: `mwdat-core`, `mwdat-camera`, `mwdat-display`, `mwdat-mockdevice`.
- Web Apps: a separate hosted runtime, not a module.

Keep test-process products apart from runtime capability claims. Inventory the
exact upstream plugin roles from each manifest `source_inventory.<lane>.plugin_roles`
list; a role count without exact-name coverage is incomplete. Treat upstream
`AGENTS.md`, `README.md`, `install-skills.sh`, `.codex-plugin/plugin.json`, and
docs MCP references as source routing inputs only.

## Full-audit checklist

Expand the required output with these rows when the request is a full-SDK or
parity audit. Mark every row not in scope as "not selected".

- Full-reference journey sections: setup/hardware, iOS, Android, Display,
  lifecycle/permissions, HFP/A2DP, MockDevice, AI/MCP/tooling,
  organization/project/release-channel administration, Web Apps.
- Exact upstream iOS, Android, and Web Apps plugin-role lists and counts, with
  the local skill that covers each.
- Preflight contract reference and applicable `PRE-*` task statuses from the
  [target-preflight packet](../../meta-wearables-device-proof/references/target-preflight.md).
- iOS and Android atlas snapshots with artifact/source/compile status, including
  the Android `Session`/`DeviceSession` conflict.
- Stale or conflicting source ledger with migration actions (for example
  `DAMEnabled`/`DAM_ENABLED` versus the 0.9 changelog).
- Product label, SDK identity, and runtime capability as separate columns, with
  Gen 2, Meta Glasses, Display, and Gen 3 treatment.
- Version-dependency tuple (phone, companion, on-glasses DAT app, firmware,
  artifact, runtime), first-party versus community signal, and `COMP-*` rows.
- Organization/project, permission-rationale, version/build, tester/channel,
  telemetry, and account-recovery gates when distribution is in scope.
- Transport hop, audio route, queue/backpressure, thermal, and recovery contract.
- Debug-server/MCP baseline, first-failure graph, redaction review, and `DBG`
  rows when diagnosis is in scope.
- Operational tuple, Developer Mode versus release channel, provisioning state,
  first failure, bounded recovery, and post-action evidence.

## Atlas workflow (iOS)

1. Freeze the snapshot: repository commit/tag, changelog release, API reference
   URL, `llms.txt` retrieval date, MCP query. Keep a moving `main` commit apart
   from the reproducible package tag.
2. Map public module names to the package products the target actually exposes.
   Mark index-only names `to-verify`.
3. Trace `Wearables.configure()` → registration/callback → permission → device
   selection → session → capability → stream/Display state → teardown → fallback.
4. Map camera/photo, HFP/A2DP audio, Display DSL/input/video, IMU, MockDevice,
   samples, and debugging separately; record conflicts such as optional
   signatures or stale minimum-OS prose.
5. Keep DAT native mobile and Web Apps as distinct journeys. When the Web App
   toolkit and the full-reference index disagree, keep both revisions and route
   the feature to [device proof](../../meta-wearables-device-proof/SKILL.md).

## Sources

- [DAT iOS repository](https://github.com/facebook/meta-wearables-dat-ios) and [AGENTS.md](https://github.com/facebook/meta-wearables-dat-ios/blob/main/AGENTS.md)
- [DAT iOS README](https://github.com/facebook/meta-wearables-dat-ios#readme)
- [DAT iOS changelog](https://github.com/facebook/meta-wearables-dat-ios/blob/main/CHANGELOG.md)
- [DAT iOS API reference](https://wearables.developer.meta.com/docs/reference/ios_swift/dat/latest)
- [DAT Android repository](https://github.com/facebook/meta-wearables-dat-android) and [AGENTS.md](https://github.com/facebook/meta-wearables-dat-android/blob/main/AGENTS.md)
- [DAT Android changelog](https://github.com/facebook/meta-wearables-dat-android/blob/main/CHANGELOG.md)
- [Web Apps toolkit](https://github.com/facebook/meta-wearables-webapp)
- [Full Wearables platform reference](https://wearables.developer.meta.com/llms.txt?full=true)
- [Wearables MCP](https://mcp.developer.meta.com/wearables)
- [Ray-Ban Meta Gen 2 announcement](https://about.fb.com/news/2025/09/ray-ban-meta-gen-2-better-battery-life-video-capture/)
- [Meta Glasses announcement](https://about.fb.com/news/2026/06/meta-essilorluxottica-partner-launch-meta-glasses/)
