# Shared rules for every meta-wearables-ops skill

Every meta-wearables-ops skill applies these rules. Skills link here instead of
restating them.

## Evidence ladder

Report each result at the level it actually reached. A lower level never stands
in for a higher one.

| Level | What it proves | What it does not prove |
| --- | --- | --- |
| `source` | An official page, repository, or changelog at a pinned revision says it | That the target app compiles or that a device behaves that way |
| `static` | The target's configuration, identity, permissions, and wiring are present | That it builds, registers, or runs |
| `build` | The exact target builds and its tests pass against the resolved package or artifact | Any wearable behavior |
| `mock` | DAT MockDevice drives registration, lifecycle, and media fixtures | Radio, optics, audio routing, firmware, or thermal behavior |
| `browser-sim` | The Web App renders and handles focus in the browser simulator | Physical Display rendering, input, or performance |
| `connected` | A named phone and companion reach a named device | Sustained behavior on physical glasses in the field |
| `physical` | The feature works on named glasses, firmware, and companion versions | Signed distribution or release eligibility |
| `signed` | A signed build passes the same physical run | Release-channel access or store approval |
| `release-channel` | Testers on the named channel can install and use it | Production availability |
| `production` | It ships to users | Nothing further |

The machine-readable form lives in the `evidence_levels` list of
[the capability/evidence plan](../../meta-wearables-sdk-audit/references/capability-evidence-plan.yaml).
An unrun level leaves its row empty. Never invent a result.

## Device labels

- Never map "Gen 3" to `DeviceType`, `.metaGlasses`, `.rayBanMeta`, `META_GLASSES`,
  `RAYBAN_META`, Display, or any other enum from user wording, a product
  announcement, or a neighboring model. As of the 2026-08-22 source snapshot no
  public Gen 3 mapping exists. Mark the claim `to-verify` and carry it until an
  official mapping and a named physical run exist.
- "Gen 2", a product name, or a marketing page is not a runtime capability.
  Capability comes from the runtime device type, firmware, companion version, and
  the capability response on that device.
- "Regular SDK" means native DAT (iOS or Android) or Web Apps once the surface is
  identified. There is no third SDK.

## Secrets and personal data

Never print, commit, log, paste into fixtures, screenshot, or archive:
GitHub Packages tokens, client tokens, application IDs paired with secrets,
signing material, callback payloads, tester emails or account IDs, device serials
or identifiers, raw camera frames, audio, or transcripts. Redact them in
diagnostic bundles and evidence packets.

## Claims

- Cite a knowledge-base document or an official upstream page for each
  substantive claim. Mark anything uncited as unverified.
- A compile, mock, browser-simulator, or phone-only result is never hardware
  proof.
- A callback receipt, Developer Mode registration, app attestation, or
  release-channel membership does not prove permissions, physical capability,
  local processing, or store approval.
- Do not infer Kotlin/Gradle/Manifest behavior from Swift examples, or the
  reverse. Platform parity needs both artifacts and both target builds.
- Native DAT and Web Apps are separate surfaces with separate packages,
  lifecycle, deployment, and evidence gates.
- Keep the phone app useful when the wearable is absent, unregistered,
  unsupported, disconnected, denied, or out of range.
