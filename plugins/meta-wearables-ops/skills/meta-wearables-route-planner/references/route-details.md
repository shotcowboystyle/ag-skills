# Meta Wearables route planner — details

## Read when the request mentions…

| Wording in the request | Read |
| --- | --- |
| Gen 2, Gen 3, Meta Glasses, Display, an SDK alias | [Device-generation and runtime-support matrix](../../meta-wearables-knowledge-base/references/70-meta-wearables/16-device-generation-and-runtime-support-matrix.md) |
| firmware, companion or DAT-app version, support matrix, compatibility failure | [Version-dependency and device-compatibility evidence](../../meta-wearables-knowledge-base/references/70-meta-wearables/26-version-dependency-and-device-compatibility-evidence.md) |
| "full", "regular SDK", "all capabilities", parity | [Full SDK capability and source-conflict matrix](../../meta-wearables-knowledge-base/references/70-meta-wearables/15-full-sdk-capability-and-source-conflict-matrix.md), then hand off to [SDK audit](../../meta-wearables-sdk-audit/SKILL.md) |
| Android, Kotlin/Java symbols, Maven coordinates, 0.9 migration | [DAT Android API surface atlas](../../meta-wearables-knowledge-base/references/70-meta-wearables/20-dat-android-api-surface-atlas.md) |
| account, team, project identity, testers, versions, release channels, telemetry | [Developer Center project and release operations](../../meta-wearables-knowledge-base/references/70-meta-wearables/21-developer-center-project-and-release-operations.md) |
| Bluetooth, Wi-Fi/local network, HFP/A2DP, latency, backpressure, thermal, link recovery | [Transport, audio, and runtime reliability](../../meta-wearables-knowledge-base/references/70-meta-wearables/22-transport-audio-and-runtime-reliability.md) |
| "on-device", local-first, private, offline, low-latency, where processing runs | [On-device compliance and runtime contract](../../meta-wearables-knowledge-base/references/70-meta-wearables/17-on-device-compliance-and-runtime-contract.md) |
| Developer Mode, update-required or device-unavailable errors, recovery | [Operational readiness and recovery](../../meta-wearables-knowledge-base/references/70-meta-wearables/18-operational-readiness-and-recovery.md) |
| Display actions, D-pad/captouch, Neural Band/EMG, temple gestures, motion, location, browser sensors | [Input, sensors, and physical interaction](../../meta-wearables-knowledge-base/references/70-meta-wearables/24-input-sensors-and-physical-interaction.md) |
| bundle/package identity, Meta AI callbacks, attestation, credentials, Web App origin, App Store gates | [Security, attestation, and credential boundaries](../../meta-wearables-knowledge-base/references/70-meta-wearables/25-security-attestation-and-credential-boundaries.md) |
| an existing target that needs intake before work | [Existing-target intake and preflight](../../meta-wearables-knowledge-base/references/70-meta-wearables/33-existing-target-intake-and-preflight.md) |
| no target yet | [Project bootstrap and target intake](../../meta-wearables-knowledge-base/references/70-meta-wearables/31-project-bootstrap-and-target-intake.md) and the [bootstrap packet](project-bootstrap-packet.md) |

## Reject routes that assume

- product-generation names map one-to-one to SDK enums;
- every Ray-Ban Meta or Oakley Meta model has a Display, camera, audio, or Wi-Fi capability;
- Web Apps can call native DAT APIs directly;
- a simulator, browser, or phone camera proves glasses behavior;
- Meta AI voice commands are part of the current public DAT preview;
- an undocumented "regular SDK" is interchangeable with DAT;
- a public API, model, entitlement, background behavior, or voice feature that
  the current sources do not establish.

## Sources

- [Meta Wearables DAT iOS repository](https://github.com/facebook/meta-wearables-dat-ios)
- [Meta Wearables DAT Android repository](https://github.com/facebook/meta-wearables-dat-android)
- [DAT iOS changelog](https://github.com/facebook/meta-wearables-dat-ios/blob/main/CHANGELOG.md)
- [DAT Android changelog](https://github.com/facebook/meta-wearables-dat-android/blob/main/CHANGELOG.md)
- [Introducing Meta Wearables Device Access Toolkit](https://developers.meta.com/blog/introducing-meta-wearables-device-access-toolkit/)
- [Wearables Developer Center](https://wearables.developer.meta.com/docs/develop/)
- [Meta Wearables Web Apps](https://wearables.developer.meta.com/docs/develop/webapps)
- [Web Apps toolkit](https://github.com/facebook/meta-wearables-webapp)
- [DAT-filtered full reference](https://wearables.developer.meta.com/llms.txt?full=true&product=dat)
- [Ray-Ban Meta Gen 2 announcement](https://about.fb.com/news/2025/09/ray-ban-meta-gen-2-better-battery-life-video-capture/)
- [Meta Glasses announcement](https://about.fb.com/news/2026/06/meta-essilorluxottica-partner-launch-meta-glasses/)
