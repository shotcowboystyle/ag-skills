# Meta Wearables route planner — details

## Planning workflow

1. Rewrite the request as an outcome, not a device label: capture, show, notify, navigate, control, or configure.
2. Identify the delivery surface: iOS companion, native glasses Display, Ray-Ban Display Web App, or phone fallback.
3. Record the exact device wording and map it to the runtime `DeviceType` only when an official source or observed device proves the mapping.
4. Identify the capability: registration, camera, audio, Display, button/input, Wi-Fi, or another named API. Mark undocumented behavior `to-verify`.
5. Define the permission, consent, privacy, session, disconnect, cancellation, and unavailable states.
6. Freeze the operational tuple when the route depends on companion, firmware,
   on-glasses DAT-app provisioning, release-channel, thermal, or transport state.
7. Select the shared domain/coordinator and platform adapter boundaries before
   assigning implementation files; keep Web Apps and native DAT separate.
8. Select the smallest specialist team and write a handoff with sources, version, and evidence requirements.
9. Reject routes that depend on a public API, model, entitlement, background behavior, or voice feature that the current sources do not establish.


## Compatibility language

Use these labels in plans and code reviews:

- **Documented** — present in the cited official API or product documentation.
- **Build-proven** — the exact target compiles or tests against the cited package/version.
- **Mock-proven** — the SDK mock or simulator exercises the path.
- **Connected-device proven** — a paired device completed the path, with model/firmware recorded.
- **Physical Display proven** — the actual glasses rendered and accepted the interaction.
- **To verify** — an open question; never write it as a supported feature.


## Required output

Return:

- route and rejected alternatives;
- exact SDK/repository/tag or commit;
- device/model/capability table;
- phone and wearable state machine;
- permissions/privacy and data-flow questions;
- firmware/companion/provisioning/release-channel and recovery questions;
- implementation owners and evidence ladder;
- explicit `Gen 3` and “regular SDK” resolution status.
- the manifest terminology status and the exact canonical route selected from it.


## Hard boundaries

- product-generation names map one-to-one to SDK enums;
- every Ray-Ban Meta or Oakley Meta model has a Display, camera, audio, or Wi-Fi capability;
- Web Apps can use native DAT APIs directly;
- a simulator, browser, or phone camera proves glasses behavior;
- Meta AI voice commands are part of the current public DAT preview;
- an undocumented “regular SDK” is interchangeable with DAT.


## Related routes

- [Meta Wearables agentic team](../../meta-wearables-agentic-team/SKILL.md)
- [DAT iOS integration](../../meta-dat-ios-integration/SKILL.md)
- [DAT camera and audio](../../meta-dat-camera-audio/SKILL.md)
- [Transport and runtime reliability](../../meta-wearables-transport-reliability/SKILL.md)
- [DAT Display](../../meta-dat-display/SKILL.md)
- [Input and sensors](../../meta-wearables-input-sensors/SKILL.md)
- [Web Apps](../../meta-wearables-web-apps/SKILL.md)
- [device proof](../../meta-wearables-device-proof/SKILL.md)
- [on-device compliance](../../meta-wearables-on-device-compliance/SKILL.md)
- [operational readiness](../../meta-wearables-operational-readiness/SKILL.md)
- [application architecture](../../meta-wearables-app-architecture/SKILL.md)
- [security and attestation](../../meta-wearables-security-attestation/SKILL.md)


## Sources

- [Meta Wearables DAT iOS repository](https://github.com/facebook/meta-wearables-dat-ios)
- [Meta Wearables DAT Android repository](https://github.com/facebook/meta-wearables-dat-android)
- [DAT Android API surface atlas](../../meta-wearables-knowledge-base/references/70-meta-wearables/20-dat-android-api-surface-atlas.md)
- [Developer Center operations](../../meta-wearables-knowledge-base/references/70-meta-wearables/21-developer-center-project-and-release-operations.md)
- [Security, attestation, and credential-boundaries route](../../meta-wearables-knowledge-base/references/70-meta-wearables/25-security-attestation-and-credential-boundaries.md)
- [DAT iOS changelog](https://github.com/facebook/meta-wearables-dat-ios/blob/main/CHANGELOG.md)
- [Introducing Meta Wearables Device Access Toolkit](https://developers.meta.com/blog/introducing-meta-wearables-device-access-toolkit/)
- [Wearables Developer Center](https://wearables.developer.meta.com/docs/develop/)
- [Meta Wearables Web Apps](https://wearables.developer.meta.com/docs/develop/webapps)
- [Ray-Ban Meta Gen 2 announcement](https://about.fb.com/news/2025/09/ray-ban-meta-gen-2-better-battery-life-video-capture/)
- [Meta Glasses announcement](https://about.fb.com/news/2026/06/meta-essilorluxottica-partner-launch-meta-glasses/)
