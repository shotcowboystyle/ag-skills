---
name: meta-wearables-route-planner
description: Entry point for any Meta Wearables app or feature. Picks the route (DAT iOS, DAT Android, native Display, Ray-Ban Display Web App, phone fallback, or blocked), designs the architecture (shared domain, adapters, state owner, fallback, test seams), and runs new-project intake. Use when starting a wearable app or feature, when a request names Ray-Ban Meta, Oakley Meta, Meta Glasses, Display, Gen 2, Gen 3, or the Meta Wearables SDK, or when deciding how iOS, Android, Display, and Web App code share behavior.
allowed-tools: Read, Grep, Glob
last_verified: 2026-08-22
---

# Meta Wearables route planner

## Overview

Turn a wearable idea into a verified route and an architecture before package
imports, UI, permissions, or marketing copy harden around an assumption. This
skill plans; the lane skills build. Hand off once the route is chosen:

| Lane | Skill |
| --- | --- |
| "Full SDK", parity, API atlas, surface manifest | [meta-wearables-sdk-audit](../meta-wearables-sdk-audit/SKILL.md) |
| DAT iOS/Android setup, registration, Android API atlas | [meta-wearables-dat-integration](../meta-wearables-dat-integration/SKILL.md) |
| Camera, audio, native Display, input, sensors, transport | [meta-wearables-device-capabilities](../meta-wearables-device-capabilities/SKILL.md) |
| Ray-Ban Display Web Apps | [meta-wearables-web-apps](../meta-wearables-web-apps/SKILL.md) |
| Swift, Kotlin, Web App scaffolding | [meta-wearables-implementation-recipes](../meta-wearables-implementation-recipes/SKILL.md) |
| Failures, readiness, compatibility | [meta-wearables-diagnostics](../meta-wearables-diagnostics/SKILL.md) |
| On-device claims, privacy, attestation, Developer Center, release | [meta-wearables-trust-and-release](../meta-wearables-trust-and-release/SKILL.md) |
| Connected, physical, signed proof | [meta-wearables-device-proof](../meta-wearables-device-proof/SKILL.md) |

Apply the [shared rules](../meta-wearables-knowledge-base/references/shared-rules.md) — evidence ladder, device labels, secrets, claims.

## Read before acting

- Inspect the real workspace: Xcode project, Gradle build, hosted Web App,
  min SDK, package graph, permissions, and existing device integrations. If
  none exists, this is a bootstrap.
- Read [platform and route selection](../meta-wearables-knowledge-base/references/70-meta-wearables/00-platform-and-route-selection.md),
  the [device models and capability matrix](../meta-wearables-knowledge-base/references/70-meta-wearables/05-device-models-and-capability-matrix.md),
  [application architecture and platform boundaries](../meta-wearables-knowledge-base/references/70-meta-wearables/19-application-architecture-and-platform-boundaries.md),
  and the [Meta source registry](../meta-wearables-knowledge-base/references/sources/meta-wearables-source-registry.md).
- Resolve user wording through the `terminology_contract` in the
  [surface manifest](../meta-wearables-sdk-audit/references/surface-manifest.yaml)
  before picking a route. Keep ambiguous terms ambiguous.
- [Route details](references/route-details.md) maps request wording to the
  knowledge-base page to read and lists assumptions to reject.
- Refresh the official [DAT iOS](https://github.com/facebook/meta-wearables-dat-ios)
  and [DAT Android](https://github.com/facebook/meta-wearables-dat-android)
  repositories before relying on a version-sensitive symbol.

## Route map

| User outcome | Route | First gate |
| --- | --- | --- |
| iOS app uses glasses capabilities | native DAT iOS | package/API and registration |
| Android app uses glasses capabilities | native DAT Android | Gradle/API and registration |
| glanceable native surface from the phone app | DAT Display | `supportsDisplay()` and physical model |
| HTML/CSS/JS on Ray-Ban Display | Web App | public HTTPS URL, 600×600, focus/input |
| wearer input, motion, orientation, location | Display, Web App, or phone | source/permission gate plus physical task |
| setup, consent, unavailable, unsupported | phone-first fallback | useful phone flow without wearable |
| "Gen 3" or unnamed future model | blocked / `to-verify` | device type, firmware, capability |

Native DAT and Web Apps can coexist in one product but stay separate routes.

## Workflow

1. **Intake.** Rewrite the request as an outcome (capture, show, notify,
   navigate, control, configure). Record surface, fallback, capabilities, device
   wording, processing location, evidence level, and worst-case failure.
2. **Pick the route** from the map. Name rejected alternatives. Resolve
   "regular SDK" and "Gen 3" or return them blocked; never branch into every lane.
3. **Draw the boundaries** with the [architecture contract](references/architecture-contract.md):
   shared domain/policy, one wearable coordinator that reduces SDK events into
   state, separate iOS, Android, Display, and Web App adapters, presenters, and
   test fakes. DAT imports, `Flow`/`AsyncSequence`, `DatResult`, and Web APIs
   stay inside adapters.
4. **Model state before effects:** registration, permission, device selection,
   session, capability, transport, thermal, cancellation, and fallback. Give
   each session an owner, an epoch, and a stop path so stale frames or Display
   actions cannot cross sessions. Fallback is typed state, not a retry spinner.
5. **Label the data path** of every frame, sample, transcript, sensor value,
   Display payload, and log as glasses-native, phone-local, remote, mixed, or
   unknown.
6. **Pick one vertical slice** from the [playbooks](references/vertical-slice-playbooks.md):
   native Display, camera-to-phone, audio-first, Web App, or shared outcome.
   Carry its manifest row IDs, state machine, fallback, and proof ladder.
7. **No target yet?** Fill the [project bootstrap packet](references/project-bootstrap-packet.md)
   in a new sibling folder — never inside this skills repository — and pick the first slice.
8. **Hand off** each lane to its owning skill with sources, versions, open
   gates, and the next proof task. Stop unless the user asked for the build.

## Fast path

For one feature: route, four boxes (domain, adapter, presenter, fake), one
playbook, one adapter method and typed fallback before any parity work.

## Required output

1. Route, rejected alternatives, and the terminology status of "Gen 3" and
   "regular SDK" from the manifest.
2. Exact SDK repository, tag or commit, package/artifact, and device/model/capability table.
3. Module boundary diagram, ownership table, and shared state machine with
   platform adapter interfaces; symbols marked `source`, `compile`, or `to-verify`.
4. Data-flow, privacy, thermal, lifecycle, and fallback contract.
5. Selected vertical slice with manifest and evidence row IDs.
6. Bootstrap packet with sibling path, when no target exists.
7. Test seams (reducer, fake, MockDevice, browser, connected, physical) and the
   firmware/companion/channel/signing gates.
8. Lane handoffs and the next evidence task.

## Hard boundaries

- Never put DAT imports, Meta AI registration, or Web App browser APIs in a
  SwiftUI/Compose view or the shared domain model.
- Never treat one common interface as parity; return per-platform
  unsupported or `to-verify` states where platforms differ.
- Never call a phone-local fallback glasses-native, or a Web App a native DAT module.
- Never hide a camera, audio, Display, sensor, or remote failure behind an
  unbounded retry or a generic loading state.
- Plan only. Do not create accounts, request credentials, deploy, or contact
  testers without an explicit request.
