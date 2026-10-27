# DAT iOS integration — details

## Source pinning

Pin the official [DAT iOS repository](https://github.com/facebook/meta-wearables-dat-ios)
by tag. On the 2026-08-22 refresh, `main` was
`225f64ff1617e7acc8c407bb8d3ee132f7263d00` and the 0.9.0 tag was
`9b1b83d791dfebff7afd452e924a256819094b64`. Resolve SPM products from the tag
and validate its [changelog](https://github.com/facebook/meta-wearables-dat-ios/blob/main/CHANGELOG.md)
against the actual package graph. Do not copy a product name from another release.

Read the official [iOS integration guide](https://wearables.developer.meta.com/docs/build-integration-ios),
[permissions/registration skill](https://github.com/facebook/meta-wearables-dat-ios/tree/main/plugins/mwdat-ios/skills/permissions-registration),
and [session lifecycle skill](https://github.com/facebook/meta-wearables-dat-ios/tree/main/plugins/mwdat-ios/skills/session-lifecycle)
before writing adapter code. Check exact symbols against the
[iOS surface map](../../meta-wearables-sdk-audit/references/ios-surface-map.md)
and the [DAT iOS API atlas route](../../meta-wearables-knowledge-base/references/70-meta-wearables/10-dat-ios-api-surface-atlas.md).

## Topic routes

| When in scope | Read |
| --- | --- |
| Module or migration-specific symbol | [upstream skill/tooling map](../../meta-wearables-knowledge-base/references/70-meta-wearables/11-upstream-skill-and-tooling-map.md) |
| Firmware, companion, Developer Mode, thermal, recovery | [operational readiness](../../meta-wearables-knowledge-base/references/70-meta-wearables/18-operational-readiness-and-recovery.md) |
| `Info.plist` identity, callbacks, attestation, signing, privacy manifest | [security and credential boundaries](../../meta-wearables-knowledge-base/references/70-meta-wearables/25-security-attestation-and-credential-boundaries.md) |
| Registration, session, stream, or typed-error diagnosis | [debugging and observability](../../meta-wearables-knowledge-base/references/70-meta-wearables/23-debugging-observability-and-diagnostic-evidence.md) |
| Display input or native IMU/gesture claims | [input and sensors](../../meta-wearables-knowledge-base/references/70-meta-wearables/24-input-sensors-and-physical-interaction.md) |

## Starters

- [iOS camera coordinator](../../meta-wearables-implementation-recipes/assets/meta-wearables-ios-camera-starter/MetaWearablesCameraStarter.swift) — after validating SPM products and privacy configuration.
- [iOS MockDevice starter](../../meta-wearables-implementation-recipes/assets/meta-wearables-ios-mockdevice-starter/MetaWearablesMockDeviceStarter.swift) — after linking `MWDATMockDevice`; mock evidence stays separate.
- [iOS MockDevice test client](../../meta-wearables-implementation-recipes/assets/meta-wearables-ios-mockdevice-test-client-starter/MetaWearablesMockDeviceTestClientStarter.swift) — XCUITest-process control with an app-owned test server; keep `MWDATMockDeviceTestClient` test-only.

## 0.9 migration review

When the selected package is 0.9.0 or later, review the changelog for:

- `DeviceSession.addCamera(config:)` and the child `Camera.stream`/`Camera.stop()` lifecycle;
- removal of `addStream(config:)`;
- stream/state/error completion when a session stops;
- `DeviceType.supportsDisplay` and Display button-group changes;
- iOS minimum version, mock-link behavior, and camera sample background handling;
- `ListenerTokenBag` actor and `AnyListenerToken.store(in:)`, synchronous
  `MockCameraKit.setCameraFeed(cameraFacing:)`, doff/`hingesClosed`, terminal
  stream completion;
- crash-reporting and device-access-management configuration changes.

## iOS hard boundaries

- Do not log access tokens, callback URLs containing secrets, raw media, or persistent device identifiers.
- Do not claim a device is supported because the package compiles.
- Do not assume iOS background execution, Meta AI voice commands, or raw glasses audio.

## Related

- [Apple system surfaces](https://github.com/shotcowboystyle/ag-skills/blob/main/plugins/ios-ops/skills/ios-system-surfaces-and-background/SKILL.md)
- [Apple privacy and release proof](https://github.com/shotcowboystyle/ag-skills/blob/main/plugins/ios-ops/skills/ios-release-proof/SKILL.md)

## Sources

- [Meta DAT iOS repository](https://github.com/facebook/meta-wearables-dat-ios)
- [Meta DAT iOS changelog](https://github.com/facebook/meta-wearables-dat-ios/blob/main/CHANGELOG.md)
- [DAT iOS sample-app guide](https://github.com/facebook/meta-wearables-dat-ios/tree/main/plugins/mwdat-ios/skills/sample-app-guide)
- [Build integration for iOS](https://wearables.developer.meta.com/docs/build-integration-ios)
- [Full Wearables platform reference](https://wearables.developer.meta.com/llms.txt?full=true)
- [Apple app life cycle](https://developer.apple.com/documentation/uikit/managing-your-app-s-life-cycle)
- [Apple privacy manifest files](https://developer.apple.com/documentation/bundleresources/privacy-manifest-files)
