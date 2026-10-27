---
name: ios-route-planner
description: Turn an iOS app idea or feature request into an Apple-native route before code is written — framework and symbol choices, state/data boundary, native surface, permission/entitlement/privacy matrix, fallback states, and a proportional verification plan. Use when starting a new iOS/iPadOS/watchOS/CarPlay/App Clip/visionOS app or feature, choosing between Apple frameworks, or untangling framework, permission, or system-surface confusion in an existing project.
allowed-tools: Read, Grep, Glob, Write
last_verified: 2026-08-19
---

# iOS Route Planner

## Overview

Turn an idea into a route record and evidence plan before framework choices harden
into implementation. This skill plans; the domain skills build. Hand off once the
route is chosen:

| Lane | Skill |
| --- | --- |
| Targets, modules, extensions, schemes | [ios-project-target-architect](../ios-project-target-architect/SKILL.md) |
| SwiftUI screens and Liquid Glass | [ios-native-design](../ios-native-design/SKILL.md) |
| Foundation Models, Vision, Core ML, Speech, Translation | [ios-on-device-intelligence](../ios-on-device-intelligence/SKILL.md) |
| Camera, audio, media, NFC, MusicKit, ShazamKit | [ios-media-and-inputs](../ios-media-and-inputs/SKILL.md) |
| Persistence, sync, HealthKit, accessories | [ios-data-and-device-services](../ios-data-and-device-services/SKILL.md) |
| StoreKit, Apple Pay, sign-in, Keychain, crypto | [ios-commerce-identity-and-security](../ios-commerce-identity-and-security/SKILL.md) |
| Widgets, Live Activities, extensions, background | [ios-system-surfaces-and-background](../ios-system-surfaces-and-background/SKILL.md) |
| Watch, CarPlay, App Clips, calling, push | [ios-companion-communications](../ios-companion-communications/SKILL.md) |
| AR, RealityKit, Metal, SpriteKit, Game Center | [ios-spatial-graphics-and-games](../ios-spatial-graphics-and-games/SKILL.md) |
| Tests, device proof, privacy manifest, TestFlight | [ios-release-proof](../ios-release-proof/SKILL.md) |

`outcome -> narrow Apple route -> state/data boundary -> native surface -> permission/entitlement -> lifecycle/fallback -> verification evidence`

## Read before acting

- Inspect the actual repository and target: Xcode project/workspace, schemes,
  deployment target, platforms/device families, modules, persistence, networking,
  extensions, entitlements, `Info.plist`, privacy manifest, existing system
  surfaces, and current tests. If no target exists, label the work bootstrap.
- Start from the [knowledge-base index](../ios-knowledge-base/references/README.md),
  the [framework selection questionnaire](../ios-knowledge-base/references/00-foundations/06-framework-selection-questionnaire.md),
  and the [idea-to-route recipe](../ios-knowledge-base/references/50-capability-recipes/00-idea-to-route.md).
- The [capability-first SDK atlas](../ios-knowledge-base/references/40-framework-routes/10-capability-first-apple-sdk-atlas.md),
  [framework catalog](../ios-knowledge-base/references/40-framework-routes/00-framework-catalog.md), and
  [availability and device matrix](../ios-knowledge-base/references/40-framework-routes/08-framework-availability-and-device-matrix.md)
  are large. Grep them for the framework or capability name; do not read them whole.
- Before relying on a symbol, availability condition, entitlement, or system
  behavior, re-open the official page listed in the matching
  [source registry](../ios-knowledge-base/references/sources/README.md) file.
  The knowledge base was last checked against iOS 26 / Xcode 26 in August 2026.

## Route workflow

1. **Intake.** State the outcome in one sentence. Record entry point, primary
   action, accepted result, consequence of error, offline requirement, privacy
   sensitivity, supported platforms, and non-goals.
2. **Classify the capability:** present/edit, persist/sync, capture/analyze,
   communicate, locate/map/weather, use protected data, control a device,
   transact/authenticate, expose to the system, share/export, run in the
   background, spatial/graphics/game, or companion surface.
3. **Select the narrowest Apple route** that owns the capability. Prefer
   system-owned surfaces and first-party frameworks before a custom service.
   Name concrete symbols and rejected alternatives, and list which signatures
   still need an Xcode check.
4. **Draw the handoff:** `input -> framework operation -> normalized evidence ->
   deterministic validation -> domain truth -> derived presentation -> system/companion handoff`.
   Keep UI state, persistence, model output, and external system state distinct.
5. **Build the state matrix before the happy path:** ready, denied, restricted,
   unsupported, unavailable, loading, partial, stale, interrupted, cancelled,
   empty, invalid, conflict, completed — where relevant. Keep a manual or
   local-first path when it satisfies the goal.
6. **List configuration:** permissions, usage descriptions, entitlements,
   background modes, App Groups, associated domains, accounts/services, language
   or model assets, hardware, server dependencies. Mark each `to-verify`; never
   infer it from a framework name.
7. **Choose proportional evidence:** source, compile, fixture, simulator,
   physical device, two-device/accessory/vehicle, system surface, signed
   artifact, TestFlight/App Store, production. Name what each proves and what it
   cannot.
8. **Record the route** in the project's planning docs or the
   [design brief template](../ios-knowledge-base/references/90-templates/design-brief.md),
   then stop unless the user asked for the build. If they did, hand the first
   narrow slice to the owning lane skill.

## Fast path

For one feature, compare only the plausible lanes against outcome ownership,
target availability, setup cost, fallback, and required proof. Pick the route
with the least irreversible configuration; record the rest as rejected or
deferred. Freeze `outcome -> trusted input -> smallest transformation ->
user-visible destination` and plan one slice with one source, one failure path,
and one proof task.

## Route record

| Field | Required content |
| --- | --- |
| Outcome and consequence | User task, primary action, acceptable failure, reversibility |
| Selected route | Frameworks, symbols, platforms, rejected alternatives, open API questions |
| Data boundary | Source, normalization, persistence, sync, retention, deletion |
| UI/system boundary | Screen, extension, Watch/CarPlay/spatial surface, deep link, fallback |
| State/lifecycle | Permission, availability, cancel/interrupt/background/account states |
| Trust boundary | Validation, authorization, confirmation, idempotency, side effects |
| Configuration | Entitlements, usage strings, privacy manifest, modes, domains, servers |
| Tests | Fixtures, unit/UI/accessibility/performance, device and system runs |
| Evidence gaps | Claims not yet proven and the next smallest verification |

## Change boundary

May inspect the project and write scoped planning, route, permission, and
verification documents. Do not infer authorization for new accounts, cloud
storage, analytics, paid services, background execution, health data,
production credentials, deployment, or contacting users.

The capability decision table and refusal list are in `references/details.md`.
