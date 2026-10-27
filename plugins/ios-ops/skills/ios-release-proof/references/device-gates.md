# Device and system proof gates

## Device verification workflow

1. Convert the requested claim into an observable operation: “camera frame delivered,” “Foundation Models response generated,” “HealthKit query authorized,” “Widget refreshed,” “Watch event applied,” “VoIP call reported,” “StoreKit entitlement verified,” or “signed build launched.”
2. Map the operation to required usage descriptions, capabilities, entitlements, accounts, server/APNs configuration, model/language assets, paired hardware, region, and deployment target.
3. Inspect the target artifact and source to ensure the intended bundle ID/version/build/device family and configuration are present. Treat secrets/credentials as opaque; never print them.
4. Run the smallest deterministic unit/compile/preview fixture. Capture logs/artifacts without private user data.
5. Run the real operation on the physical target; for Watch/CarPlay/communications, test every counterpart/system surface. Reset permission/account/state between cases when needed.
6. Test negative states: denied, restricted, unavailable, stale, offline, canceled, interrupted, low power, locked device, app/extension termination, server timeout, duplicate event, and migration.
7. If distributing, verify signed entitlements, provisioning, App Store/TestFlight metadata, privacy declarations, capabilities, version/build, and the release environment. Do not substitute a local archive for a submitted/reviewed/live result.
8. Report evidence and gaps in a compact matrix; do not promote an inference to proof.

## Route-specific gates

- SwiftUI/Liquid Glass: Dynamic Type, localization, VoiceOver/focus/actions, reduced motion/transparency, hit regions, contrast/legibility, adaptive layouts, and real device ergonomics.
- On-device AI: model/language availability, privacy/offline behavior, typed-output validation, prompt/tool side-effect boundaries, latency/memory/thermal measurement, fallback, and reviewable output.
- Camera/sensors/radio/GPU: usage description, capability/support check, session lifecycle, queue/backpressure/teardown, frame or sample budgets, battery/thermal, actual hardware.
- Files/photos/WebKit/PDF/extensions: user intent, security scope/bookmarks, coordinated access, data redaction, host/extension process, cancellation, provider state, and cleanup.
- Widgets/Live Activities/background: shared projection, refresh budget, stale/end state, foreground start/push environment, expiration/cancellation, no scheduling guarantee.
- Watch/CarPlay/App Clips: paired/active/reachable state, scene/category entitlement, invocation URL/AASA/App Store configuration, full-app handoff, two-device/vehicle physical testing.
- StoreKit/Apple Pay/Wallet/identity: verified transaction/server state, merchant/pass signing, nonce/state/revocation, Keychain policy, physical system UI, sandbox/TestFlight/release environment.
- CallKit/PushKit/LiveCommunicationKit: specialized push purpose, current token/APNs environment, server call reconciliation, fast system report, action fulfillment, audio/session, region/role entitlement.



## Related routes

- [Framework availability and device-proof matrix](../../ios-knowledge-base/references/40-framework-routes/08-framework-availability-and-device-matrix.md)
- [Build/device/release checklist](../../ios-knowledge-base/references/60-verification/01-build-device-and-release-checklist.md)
- [Accessibility checklist](../../ios-knowledge-base/references/60-verification/02-accessibility-and-adaptability-checklist.md)
- [AI evaluation and safety checklist](../../ios-knowledge-base/references/60-verification/03-ai-evaluation-and-safety-checklist.md)
- [Permission/entitlement/privacy checklist](../../ios-knowledge-base/references/60-verification/04-permission-entitlement-and-privacy-checklist.md)
- [System-surface checklist](../../ios-knowledge-base/references/60-verification/05-system-surface-checklist.md)
- [Availability and fallback deep dive](../../ios-knowledge-base/references/30-on-device-ai/06-privacy-availability-and-fallback.md)


## Sources

- [Running your app on simulated or physical devices](https://developer.apple.com/documentation/xcode/running-your-app-on-simulated-or-physical-devices)
- [Adding capabilities to your app](https://developer.apple.com/documentation/xcode/adding-capabilities-to-your-app)
- [Configuring app groups](https://developer.apple.com/documentation/xcode/configuring-app-groups)
- [Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/)
- [SwiftUI accessibility fundamentals](https://developer.apple.com/documentation/swiftui/accessibility-fundamentals)
- [Foundation Models](https://developer.apple.com/documentation/foundationmodels/)
- [AVFoundation](https://developer.apple.com/documentation/avfoundation/)
- [ARKit](https://developer.apple.com/documentation/arkit)
- [Watch Connectivity](https://developer.apple.com/documentation/watchconnectivity)
- [CarPlay](https://developer.apple.com/documentation/carplay)
- [App Clips](https://developer.apple.com/documentation/appclip)
- [Background Tasks](https://developer.apple.com/documentation/backgroundtasks)
- [ActivityKit](https://developer.apple.com/documentation/activitykit)
- [StoreKit](https://developer.apple.com/documentation/storekit)
- [CallKit](https://developer.apple.com/documentation/callkit)
- [PushKit](https://developer.apple.com/documentation/pushkit)
- [LiveCommunicationKit](https://developer.apple.com/documentation/livecommunicationkit)
