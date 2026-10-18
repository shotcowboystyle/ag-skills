[Part of the shotcowboystyle marketplace](https://github.com/shotcowboystyle/ai-plugins)

## iOS Ops Plugin

**Version:** 0.2.0

Native iOS and Apple-platform engineering guidance — SwiftUI, Liquid Glass, on-device intelligence, framework routing, and device-backed release verification, grounded in a versioned knowledge base that ships with the plugin.

Pairs with [`meta-wearables-ops`](https://github.com/shotcowboystyle/meta-wearables-ops-plugin), which owns Meta smart-glasses work.
Each works on its own.

## Installation

Part of the [ag-skills](../../README.md) marketplace. In Claude Code:

```bash
/plugin marketplace add shotcowboystyle/ag-skills
/plugin install ios-ops@claude-code-workflows
```

For Codex CLI, Cursor, OpenCode, Antigravity CLI, GitHub Copilot, and Pi, see
[docs/harnesses.md](../../docs/harnesses.md).

## Commands


## Skills

- **apple-sdk-route** — Turn an iOS app idea into an Apple-native framework route, state/data boundary, system-surface plan, permission matrix, and proportional verification plan.
- **ios-agentic-apple-engineering-team** — Orchestrate source-grounded, native Apple app development as a coordinated engineering team across architecture, Swift/SwiftUI implementation, Liquid Glass design, on-device AI, testing, accessibility, security, privacy, performance, system surfaces, physical-device verification, and release auditing. Use when an LLM is planning, building, reviewing, debugging, or hardening an iOS/iPadOS/watchOS/CarPlay/App Clip/spatial app and the work needs precise Apple SDK routing, role-based handoffs, evidence boundaries, or App Store readiness guidance.
- **ios-capability-route-planner** — Turn an iOS app idea or feature request into an Apple-native capability route, framework/symbol choices, SwiftUI and Liquid Glass surface plan, on-device AI boundaries, permission/entitlement/privacy matrix, lifecycle/fallback contract, and proportional verification plan. Use when planning, reviewing, or debugging a native iOS/iPadOS/watchOS/CarPlay/App Clip/spatial feature before implementation or when a project has framework, system-surface, device, or evidence confusion.
- **ios-commerce-identity-and-security** — Route, implement, or review iOS commerce, identity, secrets, local authentication, cryptography, app-integrity, and secure-network features. Use when a feature sells digital goods, accepts Apple Pay, adds Wallet passes, signs users in, protects credentials, gates a local action, or needs server-verified integrity.
- **ios-companion-communications** — Design, route, implement, or review iOS companion and communication features using WatchConnectivity, CarPlay, App Clips, CallKit, LiveCommunicationKit, PushKit, APNs, and UserNotifications. Use when a feature spans iPhone/Watch, a vehicle screen, an App Clip/full app handoff, VoIP/calling, default calling/dialer behavior, or specialized push delivery.
- **ios-data-and-device-services** — Route, implement, or review iOS persistence, CloudKit sync, HealthKit, Contacts, EventKit, WeatherKit, HomeKit, Core Bluetooth, Nearby Interaction, and local-network features. Use when an app stores personal data, syncs across devices, reads protected records, discovers accessories, measures proximity, or connects to a local service.
- **ios-device-release-proof** — Plan and audit evidence for iOS permissions, entitlements, system surfaces, on-device AI, camera/sensors, Watch/CarPlay/App Clips, commerce, networking, accessibility, physical-device behavior, signing, TestFlight, and release claims. Use when deciding whether an iOS feature is actually verified, diagnosing a device-only failure, or preparing a build/release evidence report.
- **ios-media-ml-and-inputs** — Route, implement, or review iOS media, camera, audio, Vision, Core ML, Natural Language, NFC, MusicKit, ShazamKit, and video-processing features. Use when a feature captures or imports media, runs on-device models, reads tags, accesses Apple Music, identifies audio, or needs measured physical-device performance.
- **ios-native-design-verification** — Design, implement, or review Apple-native SwiftUI and iOS 26 Liquid Glass surfaces with adaptive layout, semantic controls, accessibility, purposeful motion, and evidence-bound visual verification. Use when a screen should feel native without copying Apple branding or relying on screenshots alone.
- **ios-on-device-intelligence-evaluation** — Design, implement, evaluate, or review iOS on-device intelligence features using Foundation Models, Vision, Core ML, Speech, Translation, Natural Language, Sound Analysis, and App Intents. Use when a feature generates, extracts, classifies, transcribes, translates, analyzes, or safely acts on user content with Apple intelligence frameworks.
- **ios-privacy-performance-release-proof** — Audit and plan iOS privacy manifests, required-reason APIs, test plans, Swift Testing/XCTest coverage, OSLog/signposts/MetricKit diagnostics, accessibility task evidence, system-surface behavior, archive validation, TestFlight, App Store Connect, and release claims. Use when a feature touches protected data, third-party SDKs, performance-sensitive UI, accessibility, widgets, App Intents, Live Activities, extensions, or any signed/distributed build.
- **ios-project-target-architect** — Architect or audit an Apple-platform project before implementation by choosing the correct Xcode targets, Swift modules and packages, extensions, schemes, configurations, capabilities, privacy resources, test plans, and evidence gates for a feature. Use when an iOS/iPadOS/watchOS/macOS/visionOS/CarPlay/App Clip/widget/Live Activity/companion feature needs a target-aware build route or when project structure and proof are unclear.
- **ios-source-refresh-and-availability** — Refresh an Apple-platform knowledge route or skill bundle when Apple documentation, SDK interfaces, OS availability, entitlements, privacy rules, or release guidance changes. Use to audit source provenance, locate stale claims, update affected Markdown/recipes/packages, and rerun structural, live-link, compile, and packaging validation.
- **ios-spatial-graphics-and-games** — Route, implement, or review iOS and visionOS spatial, AR, 2D game, 3D scene, custom Metal, and Game Center features. Use when a feature uses camera/world tracking, RealityKit entities, RealityView or ImmersiveSpace, SpriteKit, GameplayKit, Metal, controllers, or GameKit multiplayer and needs measured performance and physical-device proof.
- **ios-system-surfaces-and-background** — Route, design, implement, or review iOS files/photos, WebKit/PDF, sharing, widgets, Live Activities, app extensions, File Provider, App Groups, and BackgroundTasks including iOS 26 continuous background work. Use when a feature leaves the main app process, touches user-owned documents/media, needs a system surface, or asks for background execution.
- **ios-testing-and-release-assurance** — Design, implement, review, or audit native Apple app tests and release evidence across Swift Testing, XCTest, XCUIAutomation, accessibility, Liquid Glass, on-device AI evaluation, performance, physical devices, system surfaces, archives, and TestFlight. Use when an LLM or solo developer needs a precise evidence plan or must determine what a green test actually proves.
- **liquid-glass-design** — Create or review native iOS 26 Liquid Glass interfaces using system surfaces first, justified custom effects, adaptable hierarchy, and device-aware verification.
- **on-device-ai-feature** — Design, implement, or audit an Apple on-device intelligence feature with a narrow framework route, explicit availability, reviewable output, privacy boundaries, and device evaluation.
- **swiftui-native-design** — Design, review, or implement native SwiftUI iOS screens and flows with adaptive state, accessibility, previews, and evidence-bound verification.

## Knowledge base

`skills/ios-knowledge-base/references/` ships with the plugin and is what the skills route into. Skills link
into it with relative paths that resolve inside the installed tree. Provenance lives in
`skills/ios-knowledge-base/references/sources/`, which records which upstream documents back the corpus and
when they were last checked.

## Conventions

- **Cite or say you cannot.** Substantive claims trace to a knowledge-base document or to
  upstream documentation. Uncited claims are marked unverified.
- **Written is not verified.** Documentation says one thing; a device shows another. The
  two are never conflated.
- **Never invent a proof.** An unrun verification leaves its row empty.

## Author

Curtis Blanton — [shotcowboystyle.com](https://shotcowboystyle.com)

## License

MIT
