# Diagnostic evidence contract

Use this reference when creating or reviewing a DAT troubleshooting handoff.
It keeps app-visible diagnosis, physical-device proof, and release evidence
separate.

## Baseline sequence

```text
debug server connection (if any)
  -> SDK readiness
  -> DAT registration
  -> DAT/companion permission
  -> eligible device and compatibility
  -> device link
  -> session
  -> camera / audio / Display capability
  -> stream or payload
  -> recovery or fallback
```

The first transition that fails owns the initial diagnosis. Later failures can
be consequences; record them without replacing the first blocker.

## Required observation row

| Field | Value |
| --- | --- |
| `evidence_id` | `DBG-*` row identifier |
| `plane` | `source`, `config`, `compile`, `mock`, `browser-sim`, `connected`, `physical`, `signed`, or `release-channel` |
| `platform` | `iOS`, `Android`, or `Web App` |
| `operation` | One bounded action, such as registration, session start, camera start, Display send, or audio route check |
| `sdk_revision` | Package/artifact version plus commit/tag when known |
| `app_build` | Redacted build identifier |
| `target_tuple` | Phone OS, Meta AI version, firmware, product label, runtime device type, mode/channel |
| `baseline` | Connection, SDK readiness, registration, permission, device, link, and compatibility state |
| `first_failure` | Exact first failing state or `not-run`/`to-verify` |
| `evidence` | Narrow event/error digest, counters, or observed state transition; no raw media |
| `action` | One next diagnostic or recovery action |
| `result` | `observed`, `attempted`, `not-run`, `to-verify`, or `blocked` |
| `redaction` | What was removed or why no bundle was exported |

## Observation sources

Collect the baseline in this order, from whichever source is available.

**Live-debugging MCP server connected.** Discover its tools at run time; tool
names change between SDK releases, so do not assume them. Use only read-only
tools: connection status, SDK/DAT readiness, companion-boundary and permission
state, device path and properties, a narrow event wait, an error digest, and a
diagnostic-bundle export. Never call a tool that registers, unregisters,
changes permissions, or resets state without separate user authorization.

**No MCP server connected.** Say so, then use:

1. Platform logs for one reproduction. iOS: the Xcode debug console, or
   Console.app with the iPhone selected, filtered to the app's process and its
   `os_log` subsystem. Android:
   `adb logcat --pid=$(adb shell pidof <application.id>)`.
2. The app's own DAT observations: log each registration-state, device,
   link-state, session-state, and typed error transition with a timestamp. If the
   app does not log them yet, add one temporary redacted log line per transition.
3. MockDevice reproduction of the same operation, to split app/config faults
   (fail under mock) from device, companion, or transport faults (pass under
   mock, fail connected).
4. A hand-built redacted bundle: target tuple, the ordered transitions, the
   first error, and counters. Use the handoff template below.

Without an MCP server the same `DBG-*` rows still apply; only `DBG-CONN-01`
becomes `not-run`.

## Evidence rows

| ID | What it proves | What it does not prove |
| --- | --- | --- |
| `DBG-SOURCE-01` | Official debugging/MCP procedure exists at the recorded revision | The target app is configured or connected |
| `DBG-CONN-01` | A local debug server accepted a connection | DAT readiness or glasses connectivity |
| `DBG-READINESS-01` | App-visible SDK/DAT readiness state | Companion internals or physical capability |
| `DBG-BOUNDARY-01` | App-visible companion/permission/configuration diagnosis | Permission mutation or successful recovery |
| `DBG-PATH-01` | Observed path through registration, device selection/link, session, and capability | A different device or build |
| `DBG-EVENT-01` | Narrow event/error sequence for one reproduction | A generalized product defect |
| `DBG-BUNDLE-01` | A redacted diagnostic bundle was exported | Raw-data safety unless redaction was inspected |
| `DBG-REDACTION-01` | Sensitive payloads were removed or identifiers pseudonymized | Privacy/legal approval |
| `DBG-PHYSICAL-01` | Named hardware run produced the stated audio/display/input/camera result | Public release eligibility |
| `DBG-RELEASE-01` | Signed/release-channel operation produced the stated result | General production availability |

## Diagnosis handoff template

```text
Evidence plane: <plane>
Operation: <one action>
Compatibility tuple: <platform, SDK/artifact, app build, phone OS, companion,
firmware, product label/runtime type, mode/channel>
Baseline: <connection -> readiness -> registration -> permission -> device ->
link -> session -> capability>
First failure: <exact state/error>
Observed evidence: <narrow digest; no raw media or credentials>
Owner hypothesis: <app/config | companion boundary | device/firmware | link/
transport | audio | thermal/power | release>
Next action: <one bounded step>
Fallback: <phone/display-safe/manual path>
Proof still missing: <compile, connected, physical, signed, channel, or other>
Redaction: <bundle handling>
```

## Sources

- [Official DAT iOS debugging skill](https://github.com/facebook/meta-wearables-dat-ios/blob/main/plugins/mwdat-ios/skills/debugging/SKILL.md)
- [Official DAT iOS live-debugging MCP skill](https://github.com/facebook/meta-wearables-dat-ios/blob/main/plugins/mwdat-ios/skills/live-debugging-mcp/SKILL.md)
- [Official DAT Android debugging skill](https://github.com/facebook/meta-wearables-dat-android/blob/main/plugins/mwdat-android/skills/debugging/SKILL.md)
- [Official DAT Android live-debugging MCP skill](https://github.com/facebook/meta-wearables-dat-android/blob/main/plugins/mwdat-android/skills/live-debugging-mcp/SKILL.md)
- [Wearables MCP](https://mcp.developer.meta.com/wearables)
- [Meta Wearables device and release evidence packet](../../meta-wearables-knowledge-base/references/70-meta-wearables/12-device-and-release-evidence-packet.md)
