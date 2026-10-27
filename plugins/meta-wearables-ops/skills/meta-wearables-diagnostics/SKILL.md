---
name: meta-wearables-diagnostics
description: Diagnose and recover Meta Wearables DAT iOS/Android, native Display, and Display Web App failures, and resolve device and version compatibility — first failing state across registration, permissions, link, session, camera/audio/Display, transport, firmware, and companion, with a redacted diagnostic bundle and a validated compatibility packet. Use when a DAT app cannot reach the glasses, registration or a session fails, an update-required or device-unavailable error appears, firmware or Meta AI versions drift, or someone asks whether a named product such as Gen 2 or Gen 3 supports a capability.
allowed-tools: Read, Grep, Glob, Bash(uv run *)
last_verified: 2026-08-22
---

# Meta Wearables diagnostics

Find the first failing state, apply the least invasive documented recovery, and
decide compatibility from an observed version tuple, never from a product label.
Diagnosis is observation: it is not permission to change the Meta AI app, the
glasses, the account, registration, or a release channel.

Apply the [shared rules](../meta-wearables-knowledge-base/references/shared-rules.md) — evidence ladder, device labels, secrets, claims.

## Read before acting

- First failure: the [diagnostic contract](references/diagnostic-contract.md) and the
  [debugging and observability route](../meta-wearables-knowledge-base/references/70-meta-wearables/23-debugging-observability-and-diagnostic-evidence.md).
- Recovery and readiness: the [recovery contract](references/recovery-contract.md) and the
  [operational readiness route](../meta-wearables-knowledge-base/references/70-meta-wearables/18-operational-readiness-and-recovery.md).
- Compatibility: the [compatibility contract](references/compatibility-contract.md), the
  [version-dependency route](../meta-wearables-knowledge-base/references/70-meta-wearables/26-version-dependency-and-device-compatibility-evidence.md), and the
  [device-generation matrix](../meta-wearables-knowledge-base/references/70-meta-wearables/16-device-generation-and-runtime-support-matrix.md).
- Transport, audio, or thermal faults: [transport and runtime reliability](../meta-wearables-knowledge-base/references/70-meta-wearables/22-transport-audio-and-runtime-reliability.md).
- Refresh the [DAT iOS changelog](https://github.com/facebook/meta-wearables-dat-ios/blob/main/CHANGELOG.md),
  [DAT Android changelog](https://github.com/facebook/meta-wearables-dat-android/blob/main/CHANGELOG.md),
  [version dependencies](https://wearables.developer.meta.com/docs/develop/dat/version-dependencies/), and
  [known issues](https://wearables.developer.meta.com/docs/knownissues) before a version-sensitive call.
  A login-gated table stays `access-gated` until the account view is observed.

## Workflow

1. **Freeze the tuple.** Platform, app build, SDK package or artifact and tag,
   phone OS, Meta AI version, glasses firmware, on-glasses DAT app version,
   product label, runtime device type, account mode (Developer Mode or release
   channel), and the one operation being attempted. Mark gaps `to-verify`.
2. **Collect the baseline.** If a DAT live-debugging MCP server is connected,
   discover its tools and use them read-only. If none is connected, fall back to
   platform logs (the Xcode console or Console.app filtered to the app's `os_log`
   subsystem; `adb logcat --pid=$(adb shell pidof <application.id>)`), the app's
   own logged DAT registration, device, link, session, and typed-error
   transitions, a MockDevice reproduction of the same operation, and a
   hand-built redacted diagnostic bundle. The
   [diagnostic contract](references/diagnostic-contract.md#observation-sources) lists the steps.
3. **Walk the path in order:** initialization and configuration -> callback ->
   registration -> permission -> device eligibility and compatibility -> link ->
   session -> camera/audio/Display -> transport -> thermal/power. The first
   transition that fails owns the diagnosis; record later failures as symptoms.
   Use the platform's own typed errors; never translate iOS and Android symbols.
4. **Reproduce once, narrowly.** One operation, one run ID; stop at the earliest
   actionable boundary.
5. **Recover with the least invasive documented step,** then re-run the same
   operation under a new run ID. Never auto-retry through thermal emergency,
   critical battery, power shutdown, doff/hinge closure, or an unknown protocol
   error. A firmware update, DAT-app update, or re-pair counts as successful only
   when the post-action state is reported and the original operation completes.
6. **Resolve compatibility per capability.** Compare each tuple member with the
   official version-dependency surface and label it `source`, `observed`,
   `access-gated`, `conflict`, or `unknown`. Exercise each requested capability
   on its own, including a negative path, and give a fallback for every
   unresolved one.
7. **Validate the packet.** Fill the
   [compatibility packet template](references/compatibility-evidence-packet.yaml)
   and run the validator below before handing off.

## Running the validator

`$SKILL` below is this skill's directory — the folder holding this SKILL.md.
Find it by name in your tool's skills folder (some tools prefix it, e.g.
`meta-wearables-ops__meta-wearables-diagnostics`).

```bash
uv run $SKILL/scripts/validate_compatibility_packet.py <packet.yaml>
```

A `completed` packet needs connected-tuple, physical-capability, and release
evidence rows. A Gen 3 packet cannot close without `COMP-GEN3-01` physical and
release evidence.

## Hard boundaries

- Do not register, unregister, change permissions, re-pair, update firmware, or
  switch a channel during diagnosis unless the user authorizes that operation.
- Do not diagnose from a generic "not connected" message when the first failing
  state can be observed.
- A debug-server or log result is app-visible evidence through the DAT
  boundary, not introspection of the Meta AI companion.
- A GitHub issue or forum report is a troubleshooting signal, never a
  compatibility guarantee. Label it separately.
- Developer Mode success is not release-channel evidence. Re-test with the
  signed build, tester account, and exact firmware before calling a route ready.

## Required output

1. Frozen tuple with each field labeled `source`, `observed`, `access-gated`,
   or `to-verify`, plus the evidence level reached.
2. Baseline source used (MCP server, or the named fallback steps) and the
   ordered event trace with the exact first failing state.
3. Likely owner: app, SDK/config, Meta AI boundary, device/firmware, transport,
   audio, thermal/power, or release channel.
4. Recovery attempted, post-action state, and whether the original operation
   then completed.
5. Capability-by-capability status (`current`, `to-verify`, `device-gated`,
   `source-conflict`, `unsupported`) with a fallback for each gap, and explicit
   Gen 2 / Gen 3 treatment.
6. Evidence rows (`DBG-*`, `OPS-*`, `COMP-*`) with redaction status and the
   validator receipt.
7. Verdict — `ready`, `ready-for-device`, `blocked`, `source-conflict`, or
   `to-verify` — with the proof still missing and the next refresh trigger.

## Related skills

- [Route planner](../meta-wearables-route-planner/SKILL.md) — pick the surface first.
- [DAT integration](../meta-wearables-dat-integration/SKILL.md) — fix an app or SDK/config defect.
- [Device capabilities](../meta-wearables-device-capabilities/SKILL.md) — camera, audio, Display, input, transport.
- [Device proof](../meta-wearables-device-proof/SKILL.md) — physical and signed evidence.
- [Trust and release](../meta-wearables-trust-and-release/SKILL.md) — identity, callback, attestation, channel failures.

