---
name: meta-wearables-trust-and-release
description: Own the trust and release boundary for Meta Wearables DAT iOS/Android, native Display, and Display Web Apps — on-device and data-flow claims, privacy and consent, privacy manifests and store review, app identity and attestation (MetaAppID, ClientToken, callbacks, package tokens), and Developer Center projects, release channels, testers, and telemetry. Use when a feature captures camera, audio, or sensor data, claims "on-device" or local-first processing, configures Developer Mode or a release build, handles callbacks or credentials, sets up a project or release channel, or is being prepared for testing or publishing.
allowed-tools: Read, Grep, Glob
last_verified: 2026-08-22
---

# Meta Wearables trust and release

Keep four claims separate, and prove each one on its own: where the data goes
(processing, network, storage), what the user agreed to (permissions, consent,
disclosure), who the app is (identity, callback, attestation, credentials), and
who can install it (project, version, channel, testers, store). A pass on one
never stands in for another.

Apply the [shared rules](../meta-wearables-knowledge-base/references/shared-rules.md) — evidence ladder, device labels, secrets, claims.

## Read before acting

- Inspect the actual target first: package/artifact revision, `Info.plist` or
  manifest, entitlements, privacy manifest, permissions, callback scheme,
  network destinations, storage, logs, analytics/crash settings, and signing.
- Data flow and on-device claims: the [compliance contract](references/compliance-contract.md) and
  [on-device compliance route](../meta-wearables-knowledge-base/references/70-meta-wearables/17-on-device-compliance-and-runtime-contract.md).
- Privacy, consent, and publishing: the [privacy and release route](../meta-wearables-knowledge-base/references/70-meta-wearables/08-privacy-publishing-and-release.md) and
  [registration and permissions](../meta-wearables-knowledge-base/references/70-meta-wearables/02-registration-permissions-and-configuration.md).
- Identity, callbacks, and attestation: the [security/attestation contract](references/security-attestation-contract.md) and
  [credential-boundaries route](../meta-wearables-knowledge-base/references/70-meta-wearables/25-security-attestation-and-credential-boundaries.md).
- Projects, channels, testers, telemetry: the [developer operations contract](references/developer-operations-contract.md) and
  [Developer Center route](../meta-wearables-knowledge-base/references/70-meta-wearables/21-developer-center-project-and-release-operations.md).
- Refresh Meta's [terms](https://wearables.developer.meta.com/docs/terms),
  [acceptable use policy](https://wearables.developer.meta.com/docs/acceptable-use-policy),
  [release channels](https://wearables.developer.meta.com/docs/set-up-release-channels/), and Apple's
  [App Store Review Guidelines](https://developer.apple.com/app-store/review/guidelines/).

## Workflow

1. **Freeze the identity tuple.** Platform, bundle ID or Android application ID,
   callback scheme, DAT package/artifact, project and platform app, build
   variant, mode, channel, version, and target device. Record key presence and
   redacted fingerprints, never values.
2. **Draw the data flow** for each data class — camera frames, photos, audio,
   transcripts, sensor readings, Display payloads, identifiers, diagnostics,
   analytics: source -> processing -> network/vendor -> storage/logs -> deletion.
   Label processing `on-device confirmed`, `phone-local`, `local-first`,
   `remote-required`, `source-conflict`, `to-verify`, or `unsupported`
   ([definitions](references/compliance-contract.md#claim-vocabulary)).
3. **Gate every capture.** Each capture or transmission needs capability,
   permission, a user action with notice, and a purpose. Stop or degrade on
   doff/fold, disconnect, denial, background, thermal, battery, or a stale
   session, with a visible phone fallback.
4. **Audit identity and callbacks.** `MetaAppID`, `ClientToken`, Android
   `mwdat_application_id`/`mwdat_client_token`, the bundle or package ID, the
   GitHub Packages token, and the app signature each play a different role.
   Accept only the app-owned callback scheme/host for the current environment;
   reject malformed, replayed, late, or cross-environment callbacks before any
   state change, and log only `callback_rejected`.
5. **Separate Developer Mode from release.** Developer Mode proves a local
   registration path. An attested release-channel build proves project identity
   for that build. Neither proves capability, local processing, or store
   approval. A Web App is a hosted HTTPS origin with no native attestation.
6. **Map distribution.** Managed Meta Account organization (one per company) ->
   Wearables team -> project -> platform app -> version -> release channel
   (one version each) -> tester Meta Account -> Meta AI channel state. Audit
   telemetry and crash opt-out separately from the product privacy program.
7. **Draft review notes** that state hardware requirements, the test account
   path, permissions, and fallback honestly. Recheck the dated DAT App Store
   submission gate (ExternalAccessory/MFi/privacy manifest) against the exact
   package before planning an iOS store release.
8. **Stop before release** if any data path, permission, consent, retention,
   terms, identity, channel, or physical-device gate is open.

## Hard boundaries

- Never call a phone camera, phone microphone, remote transcription, or browser
  API glasses-native; never use "on-device" to mean "uses a phone companion".
- Never capture raw camera, audio, or sensor data silently, or retain it by
  default.
- Never put a credential in a Web App bundle or browser storage; keep private
  credentials server-side.
- Never create, delete, restore, invite, revoke, publish, or switch a Developer
  Center project, version, channel, or tester without explicit authorization
  for that exact live operation and a resolved target.
- Never imply Meta endorsement or App Store/Play approval. Terms review is not
  legal advice; escalate material uncertainty to the product owner or counsel.

## Required output

1. Identity tuple and redacted key-presence matrix per platform, with callback
   validation and debug/release separation.
2. Data-flow table: each data class with processing label, network, storage,
   retention, deletion, consent trigger, and fallback.
3. Permission, usage-description, privacy-manifest, and store-metadata changes
   tied to the code path that needs each one.
4. Organization/team/project/version/channel/tester matrix, with Developer Mode
   versus signed release-channel status and telemetry opt-out state.
5. Evidence rows (`SEC-*`, `DCO-*`, compliance status) at the level actually
   reached; `not-run` or `access-gated` where unobserved.
6. First failure and one bounded recovery, when diagnosing registration, access,
   or channel behavior.
7. Open gates and explicit non-claims: privacy, legal, account, channel, store,
   device, and generation.

## Related skills

- [Diagnostics](../meta-wearables-diagnostics/SKILL.md) — registration, link, version failures.
- [DAT integration](../meta-wearables-dat-integration/SKILL.md) — wire identity and permissions.
- [Device capabilities](../meta-wearables-device-capabilities/SKILL.md) — camera, audio, sensors, Display.
- [Web Apps](../meta-wearables-web-apps/SKILL.md) — hosted Web App origin and deploy.
- [Device proof](../meta-wearables-device-proof/SKILL.md) — physical, signed, channel evidence.
- [iOS release proof](https://github.com/shotcowboystyle/ag-skills/blob/main/plugins/ios-ops/skills/ios-release-proof/SKILL.md) — Apple privacy, signing, and App Store release.
