# iOS Project, Target, and Module Architect — details

## Target selection matrix

| Requirement | First route to evaluate | Boundary to record |
| --- | --- | --- |
| iPhone/iPad app UI | App target with SwiftUI/UIKit as needed | Device family, deployment target, navigation, resources, entitlements |
| Reusable feature/domain | Swift package or framework target | Public API, product dependency, resources, platform conditions |
| Widget or control | WidgetKit extension target | Timeline/control lifecycle, App Group or intent data, widget-family proof |
| Live status | ActivityKit-enabled app/extension route | Activity attributes/content state, start/update/end ownership, device proof |
| Siri/Shortcuts/Spotlight action | App Intents types plus app target | `AppIntent`, entities/queries, authentication, donation/shortcut/system proof |
| Share or file workflow | Share/File Provider extension | Host contract, security-scoped data, extension timeout/process proof |
| App Clip | App Clip target | Associated domain, invocation, limited data/auth route, signed artifact proof |
| Watch or companion | watchOS target plus WatchConnectivity when needed | Reachability, transfer semantics, paired-device proof |
| CarPlay or vehicle UI | CarPlay scene/extension route | Entitlement, template ownership, connected-vehicle proof |
| macOS/Catalyst/visionOS | Separate target or explicit multiplatform target | API availability, conditional code, input/layout, destination proof |
| Background work | BackgroundTasks or system-owned scheduling | Registration, permitted task type, cancellation/expiration, scheduled-run proof |
| Protected data or accessory | Main target plus owning framework/capability | Authorization, usage text, hardware, pairing, privacy, physical proof |


## Module-boundary rules

- Make shared code describe product truth and deterministic behavior, not a particular scene, extension host, or device process.
- Inject persistence, networking, clock, model, location, media, and system clients behind protocols where tests need deterministic fixtures.
- Keep target-specific adapters responsible for OS availability, authorization, lifecycle, and conversion into shared values or proposals.
- Keep side effects behind explicit use cases. Require validation, authorization, confirmation, idempotency, and conflict handling before a target invokes a consequential operation.
- Prefer one-way dependencies. A package should not import an app target; an extension should not reach into in-memory app state; a shared module should not own an entitlement.
- Treat an App Group as a deliberate shared-container contract, not proof that two processes share memory. Define schema, migration, coordination, retention, and failure behavior.
- Use `#if os(...)` and availability checks where required, but keep platform-specific behavior observable through tests or target-specific verification rather than scattering conditions through domain code.


## Handoff format

Return these artifacts in the project or knowledge base:

1. A target graph with owners, processes, products, dependencies, and system/extension boundaries.
2. A module graph with public interfaces, platform adapters, resource ownership, and rejected dependencies.
3. A target configuration ledger for capabilities, entitlements, privacy, App Groups, schemes, configurations, and test plans.
4. A feature scaffold mapping input to normalized evidence, deterministic validation, domain use case, persistence/side effect, and target-specific presentation.
5. A verification ledger that names the next smallest compile, test, simulator, physical-device, system, or artifact check.


## Refuse to assume

- Do not add an account, backend, cloud sync, analytics, paid service, credential, background mode, protected-data capability, or new target without a product need and authorization.
- Do not copy Apple-owned screens, branding, icons, wording, or proprietary visual identity; use documented native behavior with original product hierarchy and copy.
- Do not claim that a target exists, a package product links, an entitlement is active, an extension is invoked, a system surface is delivered, or a release is ready from source text alone.
- Do not use a preview or simulator as proof of camera, microphone, sensors, haptics, radio, GPU/thermal behavior, Apple Intelligence, Watch, CarPlay, App Clip, protected data, or production delivery.


## Workspace routes

- [Knowledge-base map](../../ios-knowledge-base/references/README.md)
- [Project and target route matrix](../../ios-knowledge-base/references/40-framework-routes/11-project-target-and-extension-route-matrix.md)
- [Xcode target/module plan](../../ios-knowledge-base/references/90-templates/xcode-target-and-module-plan.md)
- [Target-aware feature scaffold](../../ios-knowledge-base/references/90-templates/target-aware-feature-scaffold.md)
- [Target configuration and artifact checklist](../../ios-knowledge-base/references/60-verification/06-target-configuration-and-artifact-checklist.md)
- [iOS route planner](../../ios-route-planner/SKILL.md)


## Sources

- [Configuring a new target](https://developer.apple.com/documentation/xcode/configuring-a-new-target-in-your-project)
- [Build system](https://developer.apple.com/documentation/xcode/build-system)
- [Building and running an app](https://developer.apple.com/documentation/xcode/building-and-running-an-app)
- [Customizing build schemes](https://developer.apple.com/documentation/xcode/customizing-the-build-schemes-for-a-project)
- [Adding a build configuration file](https://developer.apple.com/documentation/xcode/adding-a-build-configuration-file-to-your-project)
- [Build settings reference](https://developer.apple.com/documentation/xcode/build-settings-reference)
- [Adding package dependencies](https://developer.apple.com/documentation/xcode/adding-package-dependencies-to-your-app)
- [Swift packages in Xcode](https://developer.apple.com/documentation/xcode/swift-packages)
- [Identifying binary dependencies](https://developer.apple.com/documentation/xcode/identifying-binary-dependencies)
- [PackageDescription](https://docs.swift.org/swiftpm/documentation/packagedescription/)
- [Swift Package Manager targets](https://docs.swift.org/swiftpm/documentation/packagedescription/target/)
- [ExtensionKit](https://developer.apple.com/documentation/extensionkit)
- [Including extension-based UI](https://developer.apple.com/documentation/extensionkit/including-extension-based-ui-in-your-interface)
- [App Groups entitlement](https://developer.apple.com/documentation/bundleresources/entitlements/com.apple.security.application-groups)
- [Security entitlements](https://developer.apple.com/documentation/bundleresources/security-entitlements)
- [Privacy manifest files](https://developer.apple.com/documentation/bundleresources/privacy-manifest-files)
- [Adding tests to an Xcode project](https://developer.apple.com/documentation/xcode/adding-tests-to-your-xcode-project)
- [Organizing tests with test plans](https://developer.apple.com/documentation/xcode/organizing-tests-to-improve-feedback)
- [WidgetKit](https://developer.apple.com/documentation/widgetkit/)
- [ActivityKit](https://developer.apple.com/documentation/activitykit/)
- [App Intents](https://developer.apple.com/documentation/appintents/)
- [App Clips](https://developer.apple.com/documentation/appclip)
- [WatchConnectivity](https://developer.apple.com/documentation/watchconnectivity/)
- [CarPlay](https://developer.apple.com/documentation/carplay)
