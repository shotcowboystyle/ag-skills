---
name: ios-release-proof
description: Plan, run, and audit evidence for iOS features and releases — Swift Testing and XCTest/XCUIAutomation, accessibility tasks, AI evaluation, performance, physical-device and system-surface runs, privacy manifests and required-reason APIs, signing, archives, and TestFlight. Use when deciding whether an iOS feature is actually verified, writing tests or a test plan, diagnosing a device-only failure, or preparing a build or release evidence report.
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
last_verified: 2026-08-19
---

# iOS Release Proof

Route every claim to the smallest Apple-native evidence layer that can support
it, run that layer, and report what it proves and what it does not. Never turn
a compile, preview, simulator run, model output, archive, or TestFlight upload
into a universal production or App Review claim.

`claim -> target/configuration -> fixture -> deterministic test -> UI/system test -> device -> signed release -> remaining gap`

## Read before acting

- Inspect the Xcode project/workspace, targets, schemes, configurations, test
  plans, host apps, deployment targets, SDK, device families, extensions,
  entitlements, privacy manifests, usage descriptions, packages, bundle IDs,
  signing, and existing test results.
- Read the [evidence vocabulary](../ios-knowledge-base/references/00-foundations/05-evidence-and-verification-language.md)
  and the checklist for the claim: [build/device/release](../ios-knowledge-base/references/60-verification/01-build-device-and-release-checklist.md),
  [accessibility](../ios-knowledge-base/references/60-verification/02-accessibility-and-adaptability-checklist.md),
  [AI evaluation](../ios-knowledge-base/references/60-verification/03-ai-evaluation-and-safety-checklist.md),
  [permission/entitlement/privacy](../ios-knowledge-base/references/60-verification/04-permission-entitlement-and-privacy-checklist.md),
  [system surface](../ios-knowledge-base/references/60-verification/05-system-surface-checklist.md).
  Grep `60-verification/` for the framework's proof matrix.
- Load `references/test-matrix.md` for fixtures, plans, and test routes;
  `references/device-gates.md` for physical-device and route-specific gates;
  `references/privacy-performance.md` for privacy manifests, required-reason
  APIs, and measurement; `references/release-audit.md` for archive/TestFlight.
- Re-open the official Apple pages listed in those files before a
  version-sensitive API, policy, or App Store claim. The knowledge base was
  last checked against iOS 26 / Xcode 26 in August 2026.

## Evidence ladder

Record each claim at the strongest level actually observed:

| Level | Can support | Cannot support alone |
| --- | --- | --- |
| Official source | Documented API, constraint, availability, policy | This target's configuration, build, or behavior |
| Static inspection | Target membership, plist/entitlement intent, route | A successful build, valid signing, device behavior |
| Compile/unit/fixture | API compatibility, deterministic logic | Hardware, permissions, model quality, system UI, APNs |
| Preview/simulator/UI test | Layout, fixtures, automatable flows | Sensors, assistive-tech ergonomics, paired devices, thermal |
| Physical debug device | Hardware, permissions, assistive tech, system surfaces | Distribution signing, TestFlight, production servers |
| Signed archive/TestFlight | Packaging, real entitlements, store-like build | App Review, production rollout, all devices/regions |
| Production | The tested live route and environment | Every OS, device, account, language, or future SDK |

Never write "works", "private", "accessible", "fast", or "release-ready"
without naming target, OS, device, build, environment, operation, and level.

## Workflow

1. **State the claim** as an observable operation ("widget refreshed", "VoiceOver
   task completed", "signed build launched"), with consequence of failure,
   target, device family, and non-goals.
2. **Map configuration:** usage descriptions, capabilities, entitlements,
   privacy manifest owner, accounts, server/APNs environment, model/language
   assets, paired hardware, region, deployment target.
3. **Choose the layer.** Swift Testing for Swift logic and async coordination;
   XCTest/XCUIAutomation for UI workflows, accessibility audits, and
   performance; a physical device or system host for hardware, assistive, and
   system behavior; an archive/TestFlight build for signed evidence.
4. **Build the fixture matrix:** empty, loading, partial, stale, denied,
   unavailable, cancelled, interrupted, retry, conflict, migration,
   model-refusal, malformed-output, commit. Stable fixture IDs and reset policy.
5. **Inject dependencies:** time, randomness, network, persistence, accounts,
   permissions, model availability, system clients. No live services in
   deterministic tests.
6. **Write deterministic tests** with independent fixtures, parameterized
   cases, `#require`/`#expect`, bounded time limits. UI tests only for user
   workflows, querying semantic identifiers and asserting the next state.
7. **Audit accessibility and design:** automated audits per critical screen,
   then VoiceOver, alternate input, Dynamic Type, contrast, and reduced
   motion/effects on a named device. Test Liquid Glass grouping and fallback,
   not pixels.
8. **Evaluate generated output:** schema, source revision, allowed operations,
   privacy, refusal, cancellation, idempotency — separate from quality scoring.
9. **Run performance and system gates** with a fixed workload, baseline,
   device, OS, and configuration. Record extension, widget, intent,
   notification, background, or accessory evidence at its owning boundary.
10. **Audit the signed release:** target membership, bundle IDs, versions,
    entitlements, privacy resources, extensions, signing, exact TestFlight
    build; fresh-install and update runs; remaining App Review/production gaps.

## Fast path

List the claims, give each the lowest evidence level that can support it, and
run only the first unmet gate. Escalate only when a claim crosses a process,
device, signing, or system boundary. Stop when the claim is supported or the
missing hardware, account, signing, or system access is explicit.

## Evidence report

```text
Claim and consequence:
Target/scheme/test plan/configuration:
Bundle ID, version/build, SDK, deployment target:
OS/device(s), settings, account/server/APNs state:
Privacy manifest and entitlements:
Operation exercised and fixture IDs:
Tests, commands, artifacts:
Observed result and negative cases:
What this proves:
What this does not prove:
Next smallest gate:
```

List skipped, excluded, or known-issue tests as scope, not passes.

## Hard boundaries

- Never promote a lower evidence level to a stronger one.
- Never print credentials, tokens, or private payloads; redact logs and
  screenshots; keep raw prompts, health/contact/call data, and user media out
  of artifacts.
- Never use localized strings, element indexes, screenshots alone, or sleeps
  as the primary UI contract when semantic state is available.
- Never globally serialize Swift Testing to hide shared state; isolate fixtures.
- Never report an accessibility audit as complete accessibility, or a passing
  UI test as VoiceOver task success.
- Never add tracking, entitlements, background modes, accounts, servers,
  telemetry, or test-only production behavior to make a check pass; record the
  missing boundary instead.
