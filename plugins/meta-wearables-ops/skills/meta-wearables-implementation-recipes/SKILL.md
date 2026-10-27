---
name: meta-wearables-implementation-recipes
description: Turn a selected Meta Wearables API row and vertical-slice playbook into source-aligned Swift, Kotlin/Java, or Ray-Ban Display Web App implementation scaffolding with explicit compile, privacy, lifecycle, fallback, and physical-device gates. Use when building or reviewing a concrete iOS DAT, Android DAT, native Display, Web App, or cross-platform wearable feature after route selection.
last_verified: 2026-08-22
allowed-tools: Bash(uv run *), Read, Grep, Glob
---

# Meta Wearables implementation recipes

Use this skill after route selection and the full-surface audit. It turns one outcome into a narrow adapter implementation handoff. It never flattens DAT, native Display, Web Apps, and phone fallback into one fictional SDK.

Apply the [shared rules](../meta-wearables-knowledge-base/references/shared-rules.md) — evidence ladder, device labels, secrets, claims.

## Read before acting

- Inspect the actual target project, package graph, deployment/min SDK, privacy configuration, entitlements/manifest, and existing adapter.
- Filter exact `IOS-*`, `AND-*`, `WEB-*`, compatibility, and evidence rows from the [source-pinned API manifest](../meta-wearables-sdk-audit/references/surface-manifest.yaml).
- Choose one [vertical-slice playbook](../meta-wearables-route-planner/references/vertical-slice-playbooks.md) and read the [architecture contract](../meta-wearables-route-planner/references/architecture-contract.md) for ownership, epochs, cancellation, fallback, and test seams.
- Read the [iOS API atlas](../meta-wearables-knowledge-base/references/70-meta-wearables/10-dat-ios-api-surface-atlas.md), [Android API atlas](../meta-wearables-knowledge-base/references/70-meta-wearables/20-dat-android-api-surface-atlas.md), or [Web Apps route](../meta-wearables-knowledge-base/references/70-meta-wearables/06-web-apps-display-and-input.md) for the selected target.
- Carry the selected entry from the [capability/evidence plan](../meta-wearables-sdk-audit/references/capability-evidence-plan.yaml) — owner skills, route, privacy path, fallback, evidence levels, proof task IDs — into the handoff.
- Read the [on-device compliance contract](../meta-wearables-knowledge-base/references/70-meta-wearables/17-on-device-compliance-and-runtime-contract.md) before describing camera, audio, sensor, storage, or network processing.
- When a build, connected, physical, signed, or release claim is in scope, read the [target-preflight reference](../meta-wearables-device-proof/references/target-preflight.md) and carry its `PRE-*` status into the handoff.
- Pick a starter from the [starter table](references/starters.md). Load [implementation-recipes.md](references/implementation-recipes.md) only for the selected surface (iOS DAT 0.9 session/camera/Display, Android DAT 0.9 `DeviceSession`/`Camera`/Display, Web App focus/input/host-exit, shared domain outcome).

## Scripts

`$SKILL` below is this skill's directory — the folder holding this SKILL.md. Find it by name in your tool's skills folder (some tools prefix it, e.g. `meta-wearables-ops__meta-wearables-implementation-recipes`).

Validate the [implementation-handoff packet](references/implementation-handoff-template.yaml) before scaffolding. The manifest and plan default to the sibling sdk-audit copies; `owner_roles` must name skills in this plugin:

```bash
uv run $SKILL/scripts/validate_implementation_handoff.py <packet>
```

With no packet argument it checks the bundled template; add `--allow-placeholders` for it. A real `ready-for-implementation` packet must resolve its target tuple and every `to-verify` field; `--allow-placeholders` is for drafts only.

After editing the bundled recipe reference, run `uv run $SKILL/scripts/validate_recipe_reference.py`. Missing sections, unbalanced code fences, lost markers, or secret-like literals are blockers.

## Workflow

1. Create and validate the handoff packet: route, API rows, evidence tasks, owners, target tuple, lifecycle, privacy/data path, tests, fallback, next proof task.
2. Freeze the outcome, primary surface, phone fallback, exact target tuple, package/artifact or hosted revision, requested proof level, and open gates.
3. Select one playbook and one starter; carry the playbook's API/evidence row IDs into the recipe.
4. Resolve the release's generated API before writing imports. Mark unresolved names `to-verify` with a clear placeholder.
5. Build the smallest adapter: registration/permission, device and capability gate, session ownership, bounded data path, user projection, stop/cancellation, typed fallback.
6. Run the shared-domain starter tests (and the Web App starter tests for a Web route), then add reducer/fake/MockDevice/browser cases before asking for a target build.
7. Stop when a `to-verify` symbol or missing artifact blocks compile — do not hide it behind placeholder code.

## Required output

1. Selected playbook, normalized API/evidence row IDs, and the handoff packet path with its validator receipt.
2. Exact target/package/artifact/hosted revision tuple and remaining `to-verify` symbols.
3. Adapter skeleton with explicit compile-gate comments and the starter test result.
4. State owner, session epoch, resource stop order, cancellation, and fallback.
5. Processing location, consent, retention/deletion, network, and thermal path.
6. Reducer/fake/MockDevice/browser/build/connected/physical test cases.
7. Next proof task, unresolved questions, and source-refresh trigger.

## Hard boundaries

- Use the 0.9 consolidated `Camera` ownership path; do not generate removed `addStream` code from older examples.
- Keep iOS `AsyncSequence`/publisher, Android `Flow`/`DatResult`, and Web App browser events inside their adapters; translate them to typed product events.
- Do not invent a native MWDATAudio module. Name phone microphone, HFP input, A2DP output, and remote processing separately.

## Related skills

- [Route planner](../meta-wearables-route-planner/SKILL.md) — route choice and architecture
- [SDK audit](../meta-wearables-sdk-audit/SKILL.md) — API rows and capability plan
- [DAT integration](../meta-wearables-dat-integration/SKILL.md) — iOS and Android DAT
- [Web Apps](../meta-wearables-web-apps/SKILL.md)
- [Device proof](../meta-wearables-device-proof/SKILL.md)
- [Trust and release](../meta-wearables-trust-and-release/SKILL.md) — on-device compliance

## Sources

- [DAT iOS repository](https://github.com/facebook/meta-wearables-dat-ios) and [changelog](https://github.com/facebook/meta-wearables-dat-ios/blob/main/CHANGELOG.md)
- [DAT Android repository](https://github.com/facebook/meta-wearables-dat-android) and [changelog](https://github.com/facebook/meta-wearables-dat-android/blob/main/CHANGELOG.md)
- [Meta Wearables Web Apps toolkit](https://github.com/facebook/meta-wearables-webapp)
- [Full Wearables platform reference](https://wearables.developer.meta.com/llms.txt?full=true)
