---
name: meta-wearables-device-capabilities
description: Design, implement, or review what a native DAT app does with Meta smart glasses hardware — camera streams and photo capture, HFP microphone and A2DP audio routes, native DAT Display views and ButtonGroup input, D-pad/EMG/temple input and IMU/motion/location sensors, and the Bluetooth/Wi-Fi transport, backpressure, thermal, disconnect, and recovery behavior underneath them. Use when a request involves glasses camera, microphone, audio route, native Display UI, wearer input or sensors, dropped frames, link instability, latency, or reliability claims.
allowed-tools: Read, Grep, Glob
last_verified: 2026-08-22
---

# Meta Wearables device capabilities

## Overview

Own each hardware capability as its own contract — source, owner, permission, bounded queue, stop order, phone fallback, evidence — on top of a started DAT session. Keep this chain explicit:

`runtime capability gate -> permission/consent -> owned capability -> bounded consumer -> teardown -> phone fallback`

Ray-Ban Display **Web App** HTML surfaces are not native Display; they belong to [Web Apps](../meta-wearables-web-apps/SKILL.md). Package setup, registration, and sessions belong to [DAT integration](../meta-wearables-dat-integration/SKILL.md).

Apply the [shared rules](../meta-wearables-knowledge-base/references/shared-rules.md) — evidence ladder, device labels, secrets, claims.

## Lanes

| Lane | Detail | Knowledge base |
| --- | --- | --- |
| Camera and photo | [camera-audio.md](references/camera-audio.md) | [session, camera, audio](../meta-wearables-knowledge-base/references/70-meta-wearables/03-device-session-camera-and-audio.md) |
| Audio (HFP in, A2DP out) | [camera-audio.md](references/camera-audio.md) | [transport and audio](../meta-wearables-knowledge-base/references/70-meta-wearables/22-transport-audio-and-runtime-reliability.md) |
| Native Display | [display.md](references/display.md) | [Display access](../meta-wearables-knowledge-base/references/70-meta-wearables/04-display-access-and-glasses-ui.md) |
| Input and sensors | [input-sensor-contract.md](references/input-sensor-contract.md) | [input and sensors](../meta-wearables-knowledge-base/references/70-meta-wearables/24-input-sensors-and-physical-interaction.md) |
| Transport and reliability | [transport-contract.md](references/transport-contract.md) | [transport and audio](../meta-wearables-knowledge-base/references/70-meta-wearables/22-transport-audio-and-runtime-reliability.md) |

## Read before acting

- Inspect the actual DAT version, platform audio setup (`AVAudioSession` or Android audio route), Bluetooth/local-network keys, existing media pipeline, persistence, upload, and background behavior.
- Read [on-device compliance](../meta-wearables-knowledge-base/references/70-meta-wearables/17-on-device-compliance-and-runtime-contract.md) for processing location, raw-media boundaries, retention, and thermal fallback, and [application architecture](../meta-wearables-knowledge-base/references/70-meta-wearables/19-application-architecture-and-platform-boundaries.md) for ownership, session epochs, and phone fallback seams.
- Read [device-generation runtime support](../meta-wearables-knowledge-base/references/70-meta-wearables/16-device-generation-and-runtime-support-matrix.md) before using Gen 2, Display, or Gen 3 language.
- Start from a [camera](../meta-wearables-implementation-recipes/assets/meta-wearables-ios-camera-starter/MetaWearablesCameraStarter.swift) or [Display](../meta-wearables-implementation-recipes/assets/meta-wearables-ios-display-starter/MetaWearablesDisplayStarter.swift) seed in [implementation recipes](../meta-wearables-implementation-recipes/SKILL.md); Android equivalents sit beside them.

## Workflow

1. Freeze the tuple: platform, DAT tag or artifact, Meta AI app, runtime device identity, firmware/DAT-app, mode/channel, requested capability.
2. Gate on the runtime capability response (for example `supportsDisplay()`), registration, session readiness, and permission. Never gate on a product name.
3. Name the source of every signal: glasses camera vs phone camera; HFP glasses mic vs phone mic vs A2DP playback vs remote transcription; native Display tap vs Web App focus event vs phone sensor.
4. Classify each transport hop — Bluetooth control, Wi-Fi/local network, HFP, A2DP, Internet — from the observed route. Keep processing location (glasses-native, phone-local, remote, mixed) separate from transport.
5. Define ownership and bounded queues: drop, coalesce, or block policy; timestamps; session epoch; stop order (stop capability, cancel consumers, then stop the session).
6. Model failure states — denied, unsupported, doff/fold, `hingesClosed`, timeout, disconnect, thermal, peak power — with a visible fallback and one bounded recovery. Never auto-retry a thermal or power shutdown.
7. For Display, project a small sanitized phone-owned snapshot, model focus/dismiss/timeout, and clear the view on every terminal path.
8. For input and sensors, normalize events with source, action, epoch, and bounded payload; reject stale epochs, debounce duplicates, and stop listeners on exit or denial.
9. Test with MockDevice and fixtures first (denied, stale, slow consumer, stop-while-streaming, reconnect), then record connected and physical runs separately.

## Fast path

Take one capability slice: gate → one owned stream, view, or listener → one event → teardown → phone fallback. Measure queue, latency, and thermal budgets at the adapter boundary. A working camera stream must not become a prerequisite for unrelated audio, Display, or input work.

## Hard boundaries

- Never call a phone microphone, A2DP playback, or phone camera a glasses capture.
- Never send raw media or raw IMU/EMG/location traces off-device without documented consent, retention, and deletion; sensor availability is not consent.
- Never claim native DAT IMU, EMG, Neural Band, or temple-gesture APIs from a conceptual reference label; keep them `to-verify` until the selected artifact exposes them.
- Never infer Android Wi-Fi transport from iOS configuration or an `INTERNET` permission.
- Never treat a Bluetooth link, registration, or `supportsDisplay()` as proof of camera, HFP, Wi-Fi, Display legibility, or input timing.
- Never hide permission, link, timeout, thermal, or power failure behind a spinner or unbounded retry.

## Required output

1. Capability, permission, and runtime-gate matrix per lane, with unresolved rows marked `to-verify`.
2. Source labeling for every signal (glasses vs phone vs remote) and the transport/processing-location diagram.
3. Ownership, bounded-queue, epoch, and stop-order contract for each stream, view, or listener.
4. Display state machine and phone handoff when Display is in scope.
5. Failure/recovery table with the first failing state and typed fallback.
6. Privacy and retention table for raw media and sensor data.
7. Evidence plan using the `TRN-*` and `INP-*` rows plus mock, connected, and physical camera/audio/Display scripts.

## Related skills

Hardware proof: [device proof](../meta-wearables-device-proof/SKILL.md). Link, firmware, and readiness failures: [diagnostics](../meta-wearables-diagnostics/SKILL.md). On-device and privacy claims: [trust and release](../meta-wearables-trust-and-release/SKILL.md). Cross-surface architecture: [route planner](../meta-wearables-route-planner/SKILL.md).
