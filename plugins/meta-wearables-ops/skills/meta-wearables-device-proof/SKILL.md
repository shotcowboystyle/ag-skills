---
name: meta-wearables-device-proof
description: Plan and audit reproducible target preflight and evidence for Meta Wearables apps across source inspection, iOS/Android/Web App inventory, unit/build checks, DAT MockDevice, browser simulator, connected-device tests, and physical Ray-Ban/Oakley/Meta glasses. Use whenever a result could be mistaken for hardware, model, camera, audio, Display, input, or release proof.
last_verified: 2026-08-22
allowed-tools: Bash(uv run *), Read, Grep, Glob
---

# Meta Wearables device proof

Keep simulated, connected, and physical observations separate. This skill stops a passing build or mock from turning into an unsupported product claim.

Apply the [shared rules](../meta-wearables-knowledge-base/references/shared-rules.md) — evidence ladder, device labels, secrets, claims.

## Read before acting

- Inspect the actual target, SDK tag/commit, test scheme, mock/simulator setup, and available hardware/account access.
- Load the selected entry from the [capability/evidence plan](../meta-wearables-sdk-audit/references/capability-evidence-plan.yaml); carry its required evidence levels and proof task IDs into the run instead of inventing a task list.
- Read the [target-preflight reference](references/target-preflight.md) before `BUILD-01`, `REL-01`, `PRE-*`, connected, physical, or release work.
- Read the [execution packet](references/execution-packet.md) for the portable task, artifact, and redaction contract.
- Read the [proof workflow detail](references/proof-workflow.md) for the full step list, the physical script minimum, and which knowledge-base route to read for each claim (generation, firmware, compliance, input, transport, diagnostics, security).

## Scripts

`$SKILL` below is this skill's directory — the folder holding this SKILL.md. Find it by name in your tool's skills folder (some tools prefix it, e.g. `meta-wearables-ops__meta-wearables-device-proof`).

1. Inspect the target workspace first. `TARGETS_PRESENT` permits target-specific preflight; `TARGETS_PARTIAL` and `NO_TARGET` require the project bootstrap packet.

   ```bash
   uv run $SKILL/scripts/inspect_target_surfaces.py <app-root>
   ```

2. For an iOS `TARGETS_PRESENT` target, emit a redacted receipt. Add `--test --destination <dest>` only for an intentional build/test observation; the JSON holds safe settings and package-lock facts, never raw xcodebuild output or credentials.

   ```bash
   uv run $SKILL/scripts/run_ios_target_preflight.py <app-root> --project <App.xcodeproj> --scheme <Scheme> --json
   ```

3. For an Android `TARGETS_PRESENT` target, inventory the build graph, DAT coordinates, manifest keys, migration markers, toolchain, and credential presence without printing values or resolving dependencies. A static pass is not a compile or device result.

   ```bash
   uv run $SKILL/scripts/run_android_target_preflight.py <gradle-root> --module app --variant debug --json
   ```

4. After editing the target-preflight reference, run `uv run $SKILL/scripts/validate_target_preflight.py`.

## Workflow

1. Freeze the source snapshot (SDK version, repo tag, docs date, target commit, build config) and the device tuple (`DeviceType`, model, firmware, phone OS, app build, access condition).
2. Run the target inspector, then only the lowest unmet `PRE-*` prerequisite for the named claim.
3. Run static/config checks, then deterministic unit/MockDevice tests, then the browser simulator for Web Apps.
4. Run connected-device tests, then the physical script on the exact target, capturing only sanitized evidence.
5. On failure, keep the first failing state, apply one documented recovery, and record `recovery-attempted` versus `recovery-observed`.
6. Promote one ladder level at a time. Mark every unrun step `not run` or `to-verify`; stop at a missing gate instead of rerunning downstream steps.

## Required output

1. Target-surface inspector receipt.
2. `PRE-*` preflight summary, reported before any build or device claim.
3. Selected capability/evidence-plan entry and its proof task IDs.
4. Evidence matrix — one row per feature: exact target, source, ladder level, observed result, artifact pointer, remaining gate.
5. Recovery actions and post-action state for any failure.
6. Open gates blocking release readiness.

## Hard boundaries

- Do not generalize a result from Ray-Ban to Oakley or from one generation to another.
- Do not announce release readiness while a required physical, privacy, access, or publishing gate is open.
- Do not call a Web App toolkit feature supported because it works in a desktop simulator; close the Developer Center/toolkit conflict on the exact firmware or keep the fallback.

## Related skills

- [Route planner](../meta-wearables-route-planner/SKILL.md)
- [DAT integration](../meta-wearables-dat-integration/SKILL.md)
- [Web Apps](../meta-wearables-web-apps/SKILL.md)
- [Device capabilities](../meta-wearables-device-capabilities/SKILL.md) — transport, input, sensors
- [Diagnostics](../meta-wearables-diagnostics/SKILL.md) — debugging and observability
- [Trust and release](../meta-wearables-trust-and-release/SKILL.md)
- [iOS release proof](https://github.com/shotcowboystyle/ag-skills/blob/main/plugins/ios-ops/skills/ios-release-proof/SKILL.md)

## Sources

- [DAT iOS MockDevice testing skill](https://github.com/facebook/meta-wearables-dat-ios/tree/main/plugins/mwdat-ios/skills/mockdevice-testing)
- [Meta Mock Device Kit](https://wearables.developer.meta.com/docs/mock-device-kit)
- [Testing with the Mock Device Kit on iOS](https://wearables.developer.meta.com/docs/testing-mdk-ios)
- [Apple target build settings](https://developer.apple.com/documentation/xcode/configuring-the-build-settings-of-a-target/)
- [Gradle dependencyInsight](https://docs.gradle.org/current/userguide/command_line_interface.html)
