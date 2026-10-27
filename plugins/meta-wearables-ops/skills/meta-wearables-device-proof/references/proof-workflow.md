# Device proof workflow detail

The SKILL.md workflow is the summary. This file holds the full step list, the
physical script minimum, and the knowledge-base reading list.

## Full proof workflow

1. Freeze the source snapshot: SDK version, repository commit/tag, docs date, target commit, build configuration.
2. Record the exact `DeviceType`, product/model name, firmware, phone OS, app build, and account/access condition when known.
3. Run the target preflight: freeze the actual iOS scheme/target and
   `Package.resolved`, Android module/variant and resolved Maven graph, or Web
   App revision/origin/input configuration. Redact secrets before storing it.
4. Run static/config checks for package products, callback, permissions, entitlements, privacy manifest, URL, and fallback.
5. Run unit/integration tests with deterministic mock events: register, permission denied, session start/stop, disconnect, error, camera/audio stop, Display unsupported, and input actions.
6. Run the browser simulator for Web Apps and record URL, canvas, focus, input, loading, error, and performance observations.
   Keep text composer, offline cache, Escape/back, extended gestures, and
   sensors as separate `source-conflict`/`to-verify` rows because the current
   public index and toolkit `main` disagree about them.
7. Run connected-device tests when a supported device is available. Capture only sanitized evidence: model/firmware, test ID, result, timestamp, and relevant error code.
8. Run the physical script on the exact target before claiming real camera, audio, Display, button/D-pad/EMG, Wi-Fi, latency, or comfort behavior.
9. For a failure or update-required result, preserve the first failing state,
   apply one documented recovery, and record the post-action state; distinguish
   `recovery-attempted` from `recovery-observed`.
10. Fill one sanitized result record per packet task. Use the packet's artifact and redaction contract; never retain raw media or device identifiers merely to make a run reproducible.
11. Mark every unrun step `not run` or `to verify`; never convert it to pass because a neighboring step passed.

When iOS UI tests need cross-process MockDevice control, use the
[MockDevice test-client starter](../../meta-wearables-implementation-recipes/assets/meta-wearables-ios-mockdevice-test-client-starter/MetaWearablesMockDeviceTestClientStarter.swift)
and record the app-process test-server setup, UI-test client, sanitized
state/actions, and teardown separately. `MWDATMockDeviceTestClient` is
test-only evidence, never a physical-device result.

## Physical script minimum

- registration and permission recovery;
- session connect, disconnect, and reconnect;
- phone fallback with the glasses absent;
- camera/audio start and clean stop if in scope;
- Display render, focus, primary action, back/dismiss, timeout, and disconnect if in scope;
- Web App launch, 600×600 layout, focus, D-pad/available input, loading, error, and exit if in scope;
- thermal/battery/latency observations proportional to the feature;
- companion/firmware/on-glasses DAT-app, mode/channel, first failure, recovery action, and post-action state;
- no private media or identifiers in screenshots/logs.

## Reading list

Knowledge-base routes under `../../meta-wearables-knowledge-base/references/70-meta-wearables/`:

- [MockDevice testing and evidence](../../meta-wearables-knowledge-base/references/70-meta-wearables/07-mockdevice-testing-and-evidence.md), [device models and capabilities](../../meta-wearables-knowledge-base/references/70-meta-wearables/05-device-models-and-capability-matrix.md), [privacy/publishing](../../meta-wearables-knowledge-base/references/70-meta-wearables/08-privacy-publishing-and-release.md) — always.
- [Device-generation and runtime-support matrix](../../meta-wearables-knowledge-base/references/70-meta-wearables/16-device-generation-and-runtime-support-matrix.md) — before naming a generation or interpreting a model enum.
- [Version, dependency, and device compatibility](../../meta-wearables-knowledge-base/references/70-meta-wearables/26-version-dependency-and-device-compatibility-evidence.md) — firmware support, compatibility failures, Gen 2/Gen 3 promotion.
- [On-device compliance and runtime contract](../../meta-wearables-knowledge-base/references/70-meta-wearables/17-on-device-compliance-and-runtime-contract.md) — local processing, raw data, thermal safety, fallback.
- [Input, sensors, and physical interaction](../../meta-wearables-knowledge-base/references/70-meta-wearables/24-input-sensors-and-physical-interaction.md) — Display actions, D-pad/EMG/temple, motion, geolocation.
- [Operational readiness and recovery](../../meta-wearables-knowledge-base/references/70-meta-wearables/18-operational-readiness-and-recovery.md) — firmware, companion, DAT-app provisioning, release channel, update-required, recovery.
- [Application architecture and platform boundaries](../../meta-wearables-knowledge-base/references/70-meta-wearables/19-application-architecture-and-platform-boundaries.md) — shared reducers, adapter fakes, fallback seams.
- [Transport, audio, and runtime reliability](../../meta-wearables-knowledge-base/references/70-meta-wearables/22-transport-audio-and-runtime-reliability.md) — Bluetooth/Wi-Fi, HFP/A2DP, sustained streaming, link recovery.
- [Debugging, observability, and diagnostic evidence](../../meta-wearables-knowledge-base/references/70-meta-wearables/23-debugging-observability-and-diagnostic-evidence.md) — readiness, first failure, event digests, redacted diagnostics.
- [Security, attestation, and credential boundaries](../../meta-wearables-knowledge-base/references/70-meta-wearables/25-security-attestation-and-credential-boundaries.md) — callback identity, attestation, signed artifacts, tester/channel access.
- [Device and release evidence packet](../../meta-wearables-knowledge-base/references/70-meta-wearables/12-device-and-release-evidence-packet.md) — full route matrix inside this workspace.

Official sources to refresh before relying on an older fixture:
[DAT iOS MockDevice skill](https://github.com/facebook/meta-wearables-dat-ios/tree/main/plugins/mwdat-ios/skills/mockdevice-testing),
[Mock Device Kit](https://wearables.developer.meta.com/docs/mock-device-kit),
[iOS testing guidance](https://wearables.developer.meta.com/docs/testing-mdk-ios),
[DAT iOS changelog](https://github.com/facebook/meta-wearables-dat-ios/blob/main/CHANGELOG.md).
