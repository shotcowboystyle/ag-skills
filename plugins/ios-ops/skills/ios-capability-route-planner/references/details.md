# iOS Capability Route Planner — details

## Capability decision table

| Need | Start route | Do not assume |
| --- | --- | --- |
| Native screen/navigation/design | SwiftUI, UIKit bridge where necessary, HIG, Liquid Glass system adoption | A custom replica is more native than a standard control. |
| Local records/files | SwiftData, Core Data, FileDocument, DocumentGroup, security-scoped URLs | CloudKit, an account, or a server is required. |
| Text generation/typed proposal | Foundation Models with availability, guided output, validation, review | Model availability, correctness, or domain truth. |
| Image/video observation | Vision/VisionKit/Core ML/AVFoundation | Confidence is truth or a simulator is camera proof. |
| Speech/translation/audio | SpeechAnalyzer/SpeechTranscriber, TranslationSession, Natural Language, Sound Analysis, AVAudioSession | All Speech APIs are on-device or every locale has the same assets/quality. |
| Map/location/weather | MapKit, Core Location, CoreLocationUI, WeatherKit | A map requires location permission or a forecast is current/guaranteed. |
| Health/personal data | HealthKit, Contacts, EventKit, UserNotifications | Authorization is permanent, complete, or medical validation. |
| Commerce/identity/security | StoreKit 2, PassKit, AuthenticationServices, Keychain, LocalAuthentication, CryptoKit, DeviceCheck/App Attest | Local state proves payment, identity, entitlement, or integrity. |
| System discoverability | App Intents, AppEntity, EntityQuery, Spotlight, WidgetKit, ActivityKit | An in-app action proves Siri/Spotlight/widget/control delivery. |
| Physical/accessory/companion | HomeKit, Core Bluetooth, Nearby Interaction, NFC, WatchConnectivity, CarPlay, CallKit/LiveCommunicationKit | Discovery is trust, pairing is compatibility, or one device proves a two-device route. |
| Documents/background/extensions | FileProvider, sharing, WebKit/PDFKit, App Groups, BackgroundTasks, App Clips | Background execution is scheduled on demand or an extension shares in-memory app state. |
| Spatial/graphics/games | ARKit, RealityKit, Metal, SpriteKit, GameplayKit, GameKit | Static assets, simulator, or a debug frame rate proves physical tracking/performance. |


## Evidence rules

- Treat Apple documentation as source evidence, not compile or runtime proof.
- Treat a preview as visual/state evidence, not accessibility, hardware, model, entitlement, or release evidence.
- Treat a simulator as UI/system-flow evidence only where the simulated route is documented; it does not prove camera, microphone, sensors, haptics, radio, GPU/thermal, Apple Intelligence, Watch, CarPlay, App Clip, protected data, or production behavior.
- Treat a physical-device run as proof only for the device/build/configuration and task actually tested.
- Treat a system-surface invocation as proof of that invocation, not all devices, all languages, all users, or production delivery.
- Treat a signed archive/TestFlight/App Store build as a separate release boundary; do not claim App Review approval or production behavior from an archive.


## Refuse to assume

- Do not add a backend, account, analytics, paid service, cloud sync, health access, background mode, or production credential without a stated product need and authorization.
- Do not copy Apple-owned screens, branding, icons, wording, or proprietary visual identity; use native conventions with original hierarchy and copy.
- Do not call a generated proposal, observation, transcript, translation, location, weather value, health sample, transaction, or system entity domain truth without the relevant deterministic validation and review policy.
- Do not make permission, entitlement, device, language, model, service, accessibility, performance, privacy, or release claims from a framework name or code snippet.


## Related routes

- [Capability-first Apple SDK atlas](../../ios-knowledge-base/references/40-framework-routes/10-capability-first-apple-sdk-atlas.md)
- [Cross-framework feature lifecycle](../../ios-knowledge-base/references/41-framework-deep-dives/06-cross-framework-feature-lifecycle.md)
- [System-surface and extension composition](../../ios-knowledge-base/references/43-system-framework-deep-dives/06-system-surface-and-extension-composition.md)
- [Device and companion capability contracts](../../ios-knowledge-base/references/42-framework-deep-dives/08-device-and-companion-capability-contracts.md)
- [Apple-native design and Liquid Glass verification](../../ios-native-design-verification/SKILL.md)
- [On-device intelligence evaluation](../../ios-on-device-intelligence-evaluation/SKILL.md)
- [System surfaces and background](../../ios-system-surfaces-and-background/SKILL.md)
- [Companion and communications](../../ios-companion-communications/SKILL.md)
- [Device and release proof](../../ios-device-release-proof/SKILL.md)


## Sources

- [Apple Developer Documentation](https://developer.apple.com/documentation/)
- [SwiftUI](https://developer.apple.com/documentation/swiftui/)
- [Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/)
- [Adopting Liquid Glass](https://developer.apple.com/documentation/TechnologyOverviews/adopting-liquid-glass)
- [Foundation Models](https://developer.apple.com/documentation/foundationmodels/)
- [Vision](https://developer.apple.com/documentation/vision/)
- [Speech](https://developer.apple.com/documentation/speech/)
- [Translation](https://developer.apple.com/documentation/translation)
- [App Intents](https://developer.apple.com/documentation/appintents/)
- [SwiftData](https://developer.apple.com/documentation/swiftdata/)
- [AVFoundation](https://developer.apple.com/documentation/avfoundation/)
- [MapKit](https://developer.apple.com/documentation/mapkit)
- [Core Location](https://developer.apple.com/documentation/corelocation)
- [HealthKit](https://developer.apple.com/documentation/healthkit/)
- [StoreKit](https://developer.apple.com/documentation/storekit)
- [BackgroundTasks](https://developer.apple.com/documentation/backgroundtasks/)
- [WatchConnectivity](https://developer.apple.com/documentation/watchconnectivity/)
- [CarPlay](https://developer.apple.com/documentation/carplay)
- [RealityKit](https://developer.apple.com/documentation/realitykit/)
- [Metal](https://developer.apple.com/documentation/metal/)
