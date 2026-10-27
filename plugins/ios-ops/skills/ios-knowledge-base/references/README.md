# iOS knowledge base

Route-oriented reference for native Apple-platform work. Content was written and
source-checked for **iOS 26 / Xcode 26 as of August 2026**; see
[sources/](sources/README.md) for the official pages behind each route and the
date they were last checked. Treat any "current" API claim as current as of that
date, and re-open the official page before relying on it.

## How to use this library

Start with the outcome, then follow the route:

`idea -> capability -> framework -> state/data -> UI -> system surface -> verification`

Example: "scan a receipt, extract fields, let the user correct them, remind them
later" routes through VisionKit or PhotosUI, Vision OCR, a reviewable domain
model, SwiftUI forms, SwiftData, UserNotifications, and device/permission tests.

**Search, don't read front to back.** The tree has ~970 files. Find the
framework or capability by name, from the `ios-knowledge-base` skill directory:

```bash
grep -ril "LiveActivity" references/        # which documents cover it
grep -il "proof" references/60-verification/*widget*   # its proof matrix
```

The largest files — `40-framework-routes/00-framework-catalog.md` and
`40-framework-routes/08-framework-availability-and-device-matrix.md` — are
tables; grep them for a framework name instead of loading them whole.

## Document conventions

Each document makes these easy to find:

- **Availability** — minimum OS, device, or model-state caveat to verify.
- **Route** — the first framework/API family to investigate.
- **Boundaries** — privacy, permissions, entitlements, or system limits.
- **Proof** — what a preview, simulator, physical device, and release test can each prove.
- **Sources** — the official Apple/Swift pages used.

Keep the distinction the documents draw between *verified on a device* and
*only written down*.

## Foundations (`00-foundations/`)

Scope, mental model, SDK versioning, project shape, concurrency, evidence vocabulary, framework questionnaire.

- [Scope and Source Policy](00-foundations/00-scope-and-source-policy.md)
- [Mental Model for Native iOS](00-foundations/01-mental-model-for-native-ios.md)
- [iOS 26 and SDK Versioning](00-foundations/02-ios-26-and-sdk-versioning.md)
- [Project Shape and Module Boundaries](00-foundations/03-project-shape-and-module-boundaries.md)
- [Concurrency and the Main Actor](00-foundations/04-concurrency-and-main-actor.md)
- [Evidence and Verification Language](00-foundations/05-evidence-and-verification-language.md)
- [Framework Selection Questionnaire](00-foundations/06-framework-selection-questionnaire.md)

## SwiftUI (`10-swiftui/`)

State, layout, navigation, animation, accessibility, interop, scrolling, focus, text.

- [SwiftUI Mental Model](10-swiftui/00-swiftui-mental-model.md)
- [State, Observation, and Data Flow](10-swiftui/01-state-observation-and-data-flow.md)
- [Layout, Typography, and Controls](10-swiftui/02-layout-typography-and-controls.md)
- [Navigation and Routing](10-swiftui/03-navigation-and-routing.md)
- [Animation and Interaction](10-swiftui/04-animation-and-interaction.md)
- [Accessibility and Adaptable UI](10-swiftui/05-accessibility-and-adaptable-ui.md)
- [Previews, Performance, and Interoperability](10-swiftui/06-previews-performance-and-interoperability.md)
- [UIKit Interoperability and Representable Boundaries](10-swiftui/07-uikit-interop-and-representables.md)
- [Platform Adaptation and Conditional Composition](10-swiftui/08-platform-adaptation-and-conditional-routes.md)
- [SwiftUI custom layouts, proposals, and responsive composition](10-swiftui/09-custom-layouts-and-proposals.md)
- [Rich text, attributed content, and custom TextRenderer routes](10-swiftui/10-rich-text-and-text-renderers.md)
- [Scroll geometry, position, visibility, and phase](10-swiftui/11-scroll-geometry-and-scroll-position.md)
- [Focus, keyboard, pointer, and accessibility input](10-swiftui/12-focus-keyboard-pointer-and-accessibility-input.md)

## Liquid Glass (`20-liquid-glass/`)

System-first adoption, custom glass, containers and morphing, screen recipes.

- [Liquid Glass Principles](20-liquid-glass/00-liquid-glass-principles.md)
- [System-First Liquid Glass Adoption](20-liquid-glass/01-system-first-adoption.md)
- [Custom Glass Effects](20-liquid-glass/02-custom-glass-effects.md)
- [Glass Containers, Identity, and Morphing](20-liquid-glass/03-glass-containers-and-morphing.md)
- [Apple-Native Screen Recipes](20-liquid-glass/04-native-screen-recipes.md)
- [Functional Liquid Glass Interactions](20-liquid-glass/05-functional-glass-interactions.md)
- [Liquid Glass State, Morphing, and AI Review Shells](20-liquid-glass/06-ai-review-shell-and-glass-state.md)

## On-device AI (`30-on-device-ai/`)

Route selector, Foundation Models, guided output, tools, Vision, Speech, privacy and fallback, evaluation.

- [On-Device AI Route Selector](30-on-device-ai/00-ai-route-selector.md)
- [Foundation Models Mental Model](30-on-device-ai/01-foundation-models-mental-model.md)
- [Guided Generation and Typed Output](30-on-device-ai/02-guided-generation-and-typed-output.md)
- [Tools, Agents, and Side Effects](30-on-device-ai/03-tools-agents-and-side-effects.md)
- [Vision, OCR, and Camera Intelligence](30-on-device-ai/04-vision-ocr-and-camera.md)
- [Speech, Translation, and Language](30-on-device-ai/05-speech-translation-and-language.md)
- [Privacy, Availability, Safety, and Fallback](30-on-device-ai/06-privacy-availability-and-fallback.md)
- [App Intents and System Routes](30-on-device-ai/07-app-intents-and-system-routes.md)
- [On-Device AI Availability and Proof Matrix](30-on-device-ai/08-on-device-ai-availability-and-proof-matrix.md)
- [AI Feature Lifecycle and Availability](30-on-device-ai/09-ai-feature-lifecycle-and-availability.md)
- [On-Device AI Evaluation and Model-Update Discipline](30-on-device-ai/10-on-device-ai-evaluation-and-model-update-discipline.md)
- [Foundation Models Prompt, Context, and Versioning Engineering](30-on-device-ai/11-foundation-models-prompt-context-and-versioning.md)

## Framework routes (`40-framework-routes/`)

Catalog, per-domain routes, availability and device matrix, SDK atlas, target/extension matrix.

- [Apple SDK Framework Catalog](40-framework-routes/00-framework-catalog.md)
- [Data, Persistence, and Sync](40-framework-routes/01-data-persistence-and-sync.md)
- [Media, Camera, and Sensors](40-framework-routes/02-media-camera-and-sensors.md)
- [Location, Maps, Places, and Weather](40-framework-routes/03-location-maps-and-places.md)
- [System Surfaces, Documents, and Background Work](40-framework-routes/04-system-surfaces-and-background-work.md)
- [Commerce, Identity, and Security](40-framework-routes/05-commerce-identity-and-security.md)
- [Spatial, Graphics, and Games](40-framework-routes/06-spatial-graphics-and-games.md)
- [Networking, Companion Devices, and Communication Surfaces](40-framework-routes/07-networking-and-collaboration.md)
- [Framework Availability and Device-Proof Matrix](40-framework-routes/08-framework-availability-and-device-matrix.md)
- [iOS 26 Edge Routes: Speech, Translation, Transfer, and Continuous Work](40-framework-routes/09-ios-26-edge-routes.md)
- [Capability-First Apple SDK Atlas](40-framework-routes/10-capability-first-apple-sdk-atlas.md)
- [Project, Target, Module, and Extension Route Matrix](40-framework-routes/11-project-target-and-extension-route-matrix.md)
- [Core ML and Vision Model Lifecycle and Device Proof](40-framework-routes/12-core-ml-vision-model-lifecycle-and-device-proof.md)

## Templates (`90-templates/`)

Design brief, AI feature brief, Xcode target and module plan, feature scaffold.

- [On-Device AI Feature Brief](90-templates/ai-feature-brief.md)
- [Native iOS Design Brief](90-templates/design-brief.md)
- [Target-Aware Feature Scaffold Brief](90-templates/target-aware-feature-scaffold.md)
- [Xcode Target and Module Plan](90-templates/xcode-target-and-module-plan.md)

## Larger collections

Each has its own index. Grep inside the directory for the framework name.

- [Native design deep dives (HIG, components, screen composition, per-feature design reviews)](21-design-deep-dives/README.md)
- [On-device AI recipes (sessions, typed output, tools, pipelines, evaluation)](31-on-device-ai-recipes/README.md)
- [Apple Intelligence system surfaces (Visual Intelligence, Writing Tools, Image Playground)](32-apple-intelligence-surfaces/README.md)
- [Framework deep dives (SwiftData, StoreKit, MapKit, App Intents, lifecycle)](41-framework-deep-dives/README.md)
- [Device, media, security, and spatial deep dives, plus SwiftUI-per-framework route reviews](42-framework-deep-dives/README.md)
- [System framework deep dives (Contacts, EventKit, notifications, Watch, CarPlay, App Clips)](43-system-framework-deep-dives/README.md)
- [System-service route cards (CallKit, SharePlay, screen capture, discovery)](44-system-services/README.md)
- [Capability recipes: idea -> route playbooks](50-capability-recipes/README.md)
- [Verification checklists and per-framework proof matrices](60-verification/README.md)
- [Compile-oriented code recipes](70-code-recipes/README.md)
