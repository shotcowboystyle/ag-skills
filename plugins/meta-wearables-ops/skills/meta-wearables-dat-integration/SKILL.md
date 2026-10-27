---
name: meta-wearables-dat-integration
description: Integrate or review the native Meta Wearables Device Access Toolkit (DAT) in an iOS (Swift, SPM) or Android (Kotlin, Gradle/Maven) companion app — package and artifact resolution, Info.plist or Manifest configuration, registration, permissions, URL/intent callbacks, device sessions, typed state and errors, MockDevice fixtures, 0.9 migrations, and the Android API atlas. Use when adding, upgrading, or reviewing DAT iOS or DAT Android code, resolving an exact DAT symbol or artifact, or comparing iOS and Android parity.
allowed-tools: Read, Grep, Glob
last_verified: 2026-08-22
---

# Meta Wearables DAT integration

## Overview

Build the smallest native adapter around the official DAT package for each platform. Keep registration, permission, and session state out of view code, keep the phone useful without glasses, and trace every SDK assumption to a pinned package or artifact. iOS and Android are separate integrations: SPM products versus Maven artifacts, Swift `throws`/async streams versus `DatResult` and `Flow`.

Apply the [shared rules](../meta-wearables-knowledge-base/references/shared-rules.md) — evidence ladder, device labels, secrets, claims.

## Read before acting

- Inspect the real target first: Xcode project, deployment target, package graph, `Info.plist`, entitlements, privacy manifest; or Gradle wrapper/version catalog, resolved Maven artifacts, Manifest, min/target SDK, R8 rules. Record existing adapters.
- Read [registration, permissions, and configuration](../meta-wearables-knowledge-base/references/70-meta-wearables/02-registration-permissions-and-configuration.md), [MockDevice testing](../meta-wearables-knowledge-base/references/70-meta-wearables/07-mockdevice-testing-and-evidence.md), and [application architecture](../meta-wearables-knowledge-base/references/70-meta-wearables/19-application-architecture-and-platform-boundaries.md) before placing the adapter behind shared product state.
- iOS: read [DAT iOS foundations](../meta-wearables-knowledge-base/references/70-meta-wearables/01-dat-ios-sdk-foundations.md), the [iOS surface map](../meta-wearables-sdk-audit/references/ios-surface-map.md), and [iOS integration details](references/ios-integration.md).
- Android: read [Android parity and boundaries](../meta-wearables-knowledge-base/references/70-meta-wearables/14-dat-android-parity-and-boundaries.md), the [Android API atlas route](../meta-wearables-knowledge-base/references/70-meta-wearables/20-dat-android-api-surface-atlas.md), the [Android 0.9 migration fixture](references/android-api-migration.md), and the [Android surface contract](references/android-surface-contract.md).
- Pin the official [DAT iOS](https://github.com/facebook/meta-wearables-dat-ios) or [DAT Android](https://github.com/facebook/meta-wearables-dat-android) tag and check its changelog against the resolved package. Prefer the release tag over moving `main`.

## Integration workflow

1. Freeze the tuple: platform, OS/min SDK, toolchain, exact DAT tag or four Maven versions, Meta AI app version, device wording, requested capability.
2. Resolve only the products or artifacts the feature needs. Android lanes are `mwdat-core`, `mwdat-camera`, `mwdat-display`, `mwdat-mockdevice`; never copy an iOS product name into Gradle or invent a module.
3. Initialize once (`Wearables.initialize(context)` on Android) and expose explicit states: unconfigured, registration required, registering, permission required, ready, starting session, connected, stopping, disconnected, unsupported, denied, failed.
4. Put callback/deep-link configuration, permission requests, and registration recovery at the app-integration boundary. Views and composables only project state.
5. Start a session only from an intentional user flow. Attach camera or Display only after the session starts; on exit, disconnect, doff/fold, error, or cancellation stop the capability, cancel collectors, then stop the session.
6. Treat stream completion and typed failures as contract: test `stateStream`/`errorStream` completion on iOS; on Android use `DatResult` failures instead of `getOrThrow()` and collect `Flow`/`StateFlow` with lifecycle-aware cancellation.
7. Audit analytics/crash opt-outs, always-on device-access management, privacy disclosures, and package credentials against the selected release's wording.
8. Add MockDevice fixtures and an unavailable phone-only path before wiring camera, audio, or Display features.

## 0.9 migration traps

- Camera moved to `addCamera(config)` → `Camera.stream` → `Camera.stop()`; the direct `addStream`/`removeStream` path is gone on both platforms.
- Android: `DatResult` is now a Java-visible reference type; Display uses `ButtonGroup`, local `Bitmap`, and tap callbacks; `DisplayComponent`, `VideoScope`, and `DAM_ENABLED` are historical.
- Upstream `AGENTS.md` and plugin examples still show 0.8 coordinates and `Session`; the 0.9.0 changelog and DisplayAccess sample establish `DeviceSession`. Resolve the name from the selected artifact.
- iOS: `ListenerTokenBag`, synchronous `MockCameraKit.setCameraFeed`, `hingesClosed`, `DeviceType.supportsDisplay`, and the raised minimum OS. See [iOS details](references/ios-integration.md#09-migration-review).

These are review prompts, not permission to use a symbol without compiling against the selected tag.

## Android API atlas

For exact-symbol, parity, or full-SDK requests, resolve symbols in authority order: resolved artifact and generated API reference, then the same release's changelog and samples, then the Developer Center, then moving `main` and upstream skills. Record disagreements as `source-conflict` and emit rows using the [Android surface contract](references/android-surface-contract.md). Load normalized rows from the [source-pinned surface manifest](../meta-wearables-sdk-audit/references/surface-manifest.yaml) and filter to platform, artifact, and status first.

## Starters

Begin from the source-aligned camera and MockDevice seeds in [implementation recipes](../meta-wearables-implementation-recipes/SKILL.md); each platform reference lists them. They are seeds, not proof.

## Hard boundaries

- No registration or permission calls in a view initializer; pairing is not permanent authorization — model denial, revocation, and re-registration.
- Never call the Android SDK "full" without checking all four artifacts against the [capability/conflict matrix](../meta-wearables-knowledge-base/references/70-meta-wearables/15-full-sdk-capability-and-source-conflict-matrix.md).
- Never treat an `AGENTS.md`, plugin role, `llms.txt`, MCP answer, or sample as a compiled artifact.
- Never assume iOS background execution, Meta AI voice commands, or raw glasses audio because DAT exists.

## Required output

1. Pinned package tag/commit or exact Maven coordinates, with the resolved module graph.
2. Target configuration audit: identity, callbacks, permissions, credentials handling, privacy settings.
3. Adapter state machine and lifecycle/teardown table (`DatResult`/`Flow` contract on Android).
4. 0.9 migration table with the selected package's compile outcome.
5. MockDevice and build-test plan, plus the phone-only unavailable path.
6. iOS/Android parity rows labeled same-concept or platform-specific.
7. Unresolved API, device-generation, and release-channel questions.

## Related skills

Camera, audio, Display, input, and transport: [device capabilities](../meta-wearables-device-capabilities/SKILL.md). iOS atlas and full-SDK audit: [SDK audit](../meta-wearables-sdk-audit/SKILL.md). Failures and readiness: [diagnostics](../meta-wearables-diagnostics/SKILL.md). Attestation and release: [trust and release](../meta-wearables-trust-and-release/SKILL.md). Hardware proof: [device proof](../meta-wearables-device-proof/SKILL.md).
