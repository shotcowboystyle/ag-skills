# Android DAT surface contract

Use this contract when producing or reviewing an Android DAT API atlas. It is
an evidence schema, not a promise that every source-level name compiles in every
0.9 artifact.

## Authority order

1. The exact resolved Maven artifact and generated API reference used by the target.
2. The same release's changelog and official samples. The
   [0.9.0 DisplayAccess sample](https://github.com/facebook/meta-wearables-dat-android/tree/main/samples/DisplayAccess)
   is the current anchor for `DeviceSession` and Display shapes.
3. The current Developer Center and raw full reference.
4. Moving `main` guidance, plugin skills, `AGENTS.md`, and historical examples.

Record disagreement instead of selecting the easiest snippet. Keep a moving
`main` commit separate from the reproducible artifact version.

## Capability lanes

| Lane | Atlas responsibility | Proof that is still separate |
| --- | --- | --- |
| Core | initialization, registration, permissions, devices, selectors, sessions, state, errors | actual app configuration and companion/device run |
| Camera | `StreamConfiguration`, camera ownership, stream frames, photo capture, bounded consumers | camera permission, connected transport, physical optics/media |
| Native Display | builder tree, text/image/button/icon/video, button groups, taps/clicks, state/errors | display-capable runtime, legibility, physical input, firmware/link behavior |
| Audio | distinguish the phone `AudioRecord` sample from a glasses HFP route | explicit audio profile, consent, route observation, physical audio result |
| MockDevice | deterministic registration, permissions, lifecycle, phone/file media, gestures | no radio, optics, HFP, thermal, firmware, or physical proof |
| Diagnostics | typed failures, state/event digest, public MCP or local debug evidence | no companion introspection or release authorization |

Android-specific topic routes: [security and credential boundaries](../../meta-wearables-knowledge-base/references/70-meta-wearables/25-security-attestation-and-credential-boundaries.md)
for GitHub Packages credentials, manifest identity, and Play review;
[source-pinned surface manifest route](../../meta-wearables-knowledge-base/references/70-meta-wearables/27-source-pinned-surface-manifest.md)
for normalized rows; [public plugin matrix](../../meta-wearables-knowledge-base/references/70-meta-wearables/13-public-plugin-and-skill-matrix.md)
for upstream role coverage.

## Required snapshot

| Field | Required value |
| --- | --- |
| `platform` | Android |
| `artifact_revision` | Exact four Maven versions used by the target, or explicit `to-verify` |
| `repo_revision` | Android DAT tag/commit plus moving `main` if consulted |
| `api_reference` | Official Android API reference URL and access state |
| `toolchain` | Android Studio, Gradle, Kotlin/Java, min/compile SDK |
| `companion_tuple` | Meta AI app and glasses firmware if known; otherwise `not-run` |
| `capability` | Core, camera, Display, audio, MockDevice, diagnostics, or release |
| `symbol_status` | `artifact`, `source`, `source-conflict`, `compile`, `unsupported`, or `to-verify` |
| `evidence_level` | `source`, `static`, `compile`, `mock`, `connected`, `physical`, `signed`, `release`, or `production` |

## Surface row template

For every important symbol or capability, record:

```text
surface_id: AND-<lane>-<number>
artifact: com.meta.wearable:<name>:<version>
source_url: <official URL>
source_revision: <tag or commit>
symbol_or_behavior: <exact name or behavior>
status: artifact | source | source-conflict | compile | unsupported | to-verify
platform_boundary: <Android-only / shared concept / not shared>
failure_contract: <DatResult, Flow, exception, callback, or unknown>
privacy_data_path: <glasses-native / phone-local / remote / mixed / unknown>
evidence_level: <one level>
first_failure: <state/error or not-run>
next_action: <compile, mock, connected, physical, source refresh, or none>
```

## Minimum Android fixture

Input: an Android app that wants camera frames, photo capture, native Display
button actions, a phone-only fallback, and a future iOS/Web App implementation.

Expected atlas output:

- four artifact rows for `mwdat-core`, `mwdat-camera`, `mwdat-display`, and
  `mwdat-mockdevice`, each pinned or marked `to-verify`;
- Gradle GitHub Packages and `read:packages` handling without a credential in
  source, plus manifest metadata and runtime permission rows;
- `Wearables.initialize`, registration, device selection, session, camera,
  Display, `DatResult`, and `Flow`/`StateFlow` routes with selected-artifact
  signatures or explicit source conflicts;
- a 0.9 migration row for camera consolidation, builder changes, Java-visible
  `DatResult`, DAM behavior, and removed error/API names;
- separate camera, Display tap, phone-microphone, MockDevice, and physical
  evidence rows;
- a shared domain/Android adapter handoff with cancellation, bounded media,
  stale-event rejection, and typed phone fallback;
- explicit Gen 2 source/runtime mapping and Gen 3 `to-verify` treatment;
- no claim that source, compile, mock, or signed APK evidence is physical or
  production proof.

## Review decision

Use `ready-for-implementation` only when the selected artifact/API symbols,
configuration gates, and fallback contract are sufficiently known for the target.
Use `source-ready-compile-gate` when source coverage is strong but the target
has not compiled. Use `blocked-by-access` for authenticated API/version tables
or missing credentials. Use `not-run-physical` whenever the named glasses,
companion, firmware, or release channel is unavailable.

## Sources

- [DAT Android repository](https://github.com/facebook/meta-wearables-dat-android)
- [DAT Android changelog](https://github.com/facebook/meta-wearables-dat-android/blob/main/CHANGELOG.md)
- [Android API reference](https://wearables.developer.meta.com/docs/reference/android/dat/latest)
- [DAT Android AGENTS.md](https://github.com/facebook/meta-wearables-dat-android/blob/main/AGENTS.md)
- [Wearables MCP](https://mcp.developer.meta.com/wearables)
- [DAT-filtered full reference](https://wearables.developer.meta.com/llms.txt?full=true&product=dat)
