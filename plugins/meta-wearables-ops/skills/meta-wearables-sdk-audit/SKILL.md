---
name: meta-wearables-sdk-audit
description: Audit Meta Wearables SDK coverage and resolve exact API surface — full-SDK and cross-platform parity audits across DAT iOS, DAT Android, native Display, and Web Apps; the iOS DAT API atlas (MWDAT modules, symbols, 0.9 migration); and the source-pinned surface manifest plus capability/evidence plan with their validators. Use when a request says "full SDK", "regular SDK", "all capabilities", or parity, when an implementation needs exact MWDAT modules or symbols, or when the surface manifest or capability/evidence plan is edited.
allowed-tools: Read, Grep, Glob, Bash(uv run *)
last_verified: 2026-08-22
---

# Meta Wearables SDK audit

## Overview

Run this before implementation when "full SDK", "regular SDK", "all
capabilities", or parity could hide an unverified module, a stale upstream
example, or an unsupported device claim — and whenever code needs an exact,
version-sensitive DAT symbol. Two modes:

- **Coverage audit** — map every requested capability to source rows, gates,
  fallbacks, and evidence.
- **iOS API atlas** — resolve exact MWDAT products and symbols. The Android API
  atlas lives in [meta-wearables-dat-integration](../meta-wearables-dat-integration/SKILL.md).

Apply the [shared rules](../meta-wearables-knowledge-base/references/shared-rules.md) — evidence ladder, device labels, secrets, claims.

`$SKILL` below is this skill's directory — the folder holding this SKILL.md.
Find it by name in your tool's skills folder (some tools prefix it, e.g.
`meta-wearables-ops__meta-wearables-sdk-audit`).

## Read before acting

- Inspect the real iOS package graph or Android Gradle dependency graph, target
  settings, Info.plist, entitlements, privacy files, and existing DAT adapter.
- Read the [full capability and source-conflict matrix](../meta-wearables-knowledge-base/references/70-meta-wearables/15-full-sdk-capability-and-source-conflict-matrix.md),
  the [device-generation and runtime-support matrix](../meta-wearables-knowledge-base/references/70-meta-wearables/16-device-generation-and-runtime-support-matrix.md),
  the [iOS API surface atlas](../meta-wearables-knowledge-base/references/70-meta-wearables/10-dat-ios-api-surface-atlas.md),
  the [Android API surface atlas](../meta-wearables-knowledge-base/references/70-meta-wearables/20-dat-android-api-surface-atlas.md),
  the [Android parity route](../meta-wearables-knowledge-base/references/70-meta-wearables/14-dat-android-parity-and-boundaries.md),
  the [upstream skill and tooling map](../meta-wearables-knowledge-base/references/70-meta-wearables/11-upstream-skill-and-tooling-map.md),
  the [public plugin and skill matrix](../meta-wearables-knowledge-base/references/70-meta-wearables/13-public-plugin-and-skill-matrix.md),
  and the [surface manifest route](../meta-wearables-knowledge-base/references/70-meta-wearables/27-source-pinned-surface-manifest.md).
  Grep these large pages; do not read them whole.
- Load the [surface manifest](references/surface-manifest.yaml) and the
  [capability/evidence plan](references/capability-evidence-plan.yaml). They
  are routing snapshots, never generated API or hardware proof.
- [Audit details](references/audit-details.md) maps request wording to the
  knowledge-base page to read and holds the module inventory and full-audit checklist.
- Grade answers against the [iOS surface fixture](references/ios-surface-map.md)
  and the [capability audit fixture](references/capability-audit-fixture.md).
- Refresh the official [DAT iOS](https://github.com/facebook/meta-wearables-dat-ios)
  and [DAT Android](https://github.com/facebook/meta-wearables-dat-android)
  repositories and changelogs, the [Web Apps toolkit](https://github.com/facebook/meta-wearables-webapp),
  the [full platform reference](https://wearables.developer.meta.com/llms.txt?full=true),
  and [Wearables MCP](https://mcp.developer.meta.com/wearables).

## Validators

Run after any edit to the manifest or plan, and before packaging:

```sh
uv run $SKILL/scripts/validate_surface_manifest.py
uv run $SKILL/scripts/validate_capability_evidence_plan.py
```

Any failure (counts, roles, anchors, IDs, levels, secret scan) blocks a refresh.

## Workflow

1. **Freeze the snapshot:** platform, target, OS/min SDK, package/artifact
   version, repository revision, Meta AI version, device wording, requested
   capabilities, and intended evidence level.
2. **Resolve wording** through the manifest `terminology_contract`. "Regular
   SDK" is ambiguous, "full SDK" is a composite audit, and "Gen 3" stays an
   unresolved alias.
3. **Select rows.** Filter `api_surface.rows` by journey and platform; carry
   each row's source anchors, status, compile/runtime gate, privacy path,
   fallback, and migration note. Pick the capability-plan entry and its
   `PRE-*` tasks, owning skills, minimum evidence levels, and proof task IDs.
4. **Inventory modules** per the [module inventory](references/audit-details.md#module-inventory),
   then resolve exact iOS products (atlas mode) and Android artifacts before
   comparing concepts across platforms.
5. **Classify each capability** as `current`, `to-verify`, `source-conflict`,
   `unsupported`, or a platform fallback: registration, permissions, device
   selection, session, camera/photo, audio, Display, sensors, health/update,
   MockDevice, debugging, privacy, and release.
6. **Record conflicts.** Search upstream `AGENTS.md`, plugin skills, samples,
   changelogs, API reference, and MCP results for stale versions or conflicting
   symbols. The selected artifact's API reference wins only after the conflict
   and its build gate are recorded.
7. **Label data paths** as glasses-native, phone-local, remote, mixed, or
   unknown, with consent, retention, thermal, and fallback per capability.
8. **Return** the smallest implementation route, missing proof rows, fallback,
   owning skills, and the next source-refresh trigger.

## Fast path

For one symbol, answer with one row: source revision, package/module, symbol,
status, target gate, fallback, and proof. For one feature, return the selected
rows plus the lanes explicitly not selected. Traverse the full surface only for
a genuine full-SDK or parity request.

## Required output

1. Source, package/artifact snapshot and date; manifest and plan IDs with revisions.
2. Terminology term, resolution status, and canonical route candidates for the
   user's device/SDK wording.
3. Module and capability matrix with platform-specific symbols, each marked
   `source`, `compile`, or `to-verify`, and the API row IDs used.
4. Selected capability-plan entries: owning skills, route, privacy path,
   fallback, evidence levels, `PRE-*` and proof task IDs.
5. Stale or conflicting source ledger with migration actions.
6. Product label, SDK identity, and runtime capability kept separate, with Gen 2
   mapping and Gen 3 `to-verify` unless official evidence closes it.
7. Target, account, permission, privacy, firmware, and release gates, plus the
   mock/browser/connected/physical evidence plan.
8. Unresolved gaps. For full audits, add the [full-audit checklist](references/audit-details.md#full-audit-checklist).
   Never return "full SDK" as an unqualified conclusion.

## Hard boundaries

- Never count an upstream plugin role, `llms.txt` entry, MCP search result, or
  repo sample as a compiled module or hardware capability.
- Never invent a module import from a broad platform index; verify package
  products and generated symbols in the selected release.
- Never treat the Android sample's phone `AudioRecord` as a glasses microphone,
  a phone `AVAudioSession` route as HFP glasses proof, or the iOS HFP route as
  an Android DAT audio API.
- Never conflate native DAT with the Web Apps DOM and hosted-URL runtime.
