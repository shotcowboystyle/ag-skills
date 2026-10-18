# iOS Privacy, Performance, and Release Proof — details

## Workflow

### 1. Convert the claim into an operation

Write the observable operation first: create a privacy report, resolve an App Entity, render a widget after reload, complete a VoiceOver task, measure a scroll hitch, receive a MetricKit report, archive a Release build, install a TestFlight build, or submit an App Store package. Identify what success and failure look like.

### 2. Map configuration and data boundaries

- Record the deployment target, SDK, device family, target membership, extension membership, capabilities, entitlements, usage descriptions, privacy resources, package/SDK versions, account state, server/APNs environment, model/language assets, and supported regions.
- Decide whether `PrivacyInfo.xcprivacy` belongs to the app, framework, static/dynamic SDK, widget, or extension target. Add it to the owning bundle resources and inspect the built artifact.
- Trace actual data collection, retention, tracking, linkage, remote processing, and third-party SDK behavior. Reconcile `NSPrivacyCollectedDataTypes`, `NSPrivacyAccessedAPITypes`, App Store Connect App Privacy, privacy-policy URLs, permission copy, and observed network behavior.
- For every required-reason API category, use only Apple’s current approved `NSPrivacyAccessedAPITypeReasons` values. Do not use a manifest to authorize tracking, and do not make the app manifest stand in for an SDK’s own manifest.

### 3. Choose the test route

- Use Swift Testing for deterministic unit/integration behavior with suites, traits, and parameterized inputs; use XCTest/XCUIAutomation for UI, system interaction, accessibility audits, and performance tests.
- Inspect the active `.xctestplan`: targets, included/excluded tags, configurations, diagnostics policy, destinations, and command. Create separate focused-development and pre-submission plans when their coverage or runtime differs.
- Include negative states: denied/restricted, unavailable, stale/missing record, locked device, offline, canceled, interrupted, terminated process, extension expiration, model-not-ready, language asset missing, duplicate event, and migration failure.
- Inspect the result bundle and identify skipped/excluded tests; a green plan proves only the tests and configurations it actually ran.

### 4. Measure without leaking data

- Use `Logger` with reverse-DNS subsystem/category names for actionable diagnostics. Redact prompts, model output, images, audio, health/contact data, credentials, tokens, and unnecessary identifiers.
- Use `OSSignposter` intervals/events with stable names and per-operation IDs for Instruments timelines. Record the workload, warm/cold state, device, OS, build, and measurement tool.
- Use XCTest performance metrics for controlled regressions, including hitch, clock, memory, and signpost measurements where relevant. Define a baseline and an acceptable change; never turn one run into a universal guarantee.
- Use MetricKit for system-collected reports from real devices. For an iOS 26 deployment target, verify the SDK/API availability before selecting the route: Apple documents `MXMetricManager` for iOS 13+, while current documentation describes the Swift-first `MetricManager` async-sequence API for iOS 27 and later. Add availability/fallback handling rather than compiling a future-only symbol unconditionally.
- Treat debug Instruments traces, XCTest baselines, real-device daily MetricKit payloads, and product-wide performance claims as different evidence classes.

### 5. Run accessibility and system-surface tasks

- Create a task matrix for launch, empty, success, edit, error, destructive, settings, deep link, notification, and recovery flows.
- Test VoiceOver, Voice Control, Switch Control, Assistive Access, Dynamic Type, increased contrast, reduced transparency, Reduce Motion, captions/transcripts, localization/RTL, keyboard, pointer, and controller input as supported by the target. Use physical devices for assistive technologies Apple documents as unavailable in Simulator.
- Test widgets, controls, App Intents, Shortcuts, Spotlight, Live Activities, notifications, extensions, Watch, CarPlay, App Clips, and share/file destinations from the real system or host surface. Include terminated, locked/restricted, stale, offline, and permission-revoked states.
- Treat accessibility audits, previews, system discovery, and a rendered system surface as diagnostic/layout evidence; they do not prove task completion, action side effects, or release delivery.

### 6. Verify the signed release path

1. Build and test the intended Release configuration.
2. Inspect the archive’s bundle IDs, version/build, entitlements, embedded extensions, privacy manifests, usage descriptions, symbols, and device-family metadata.
3. Generate/review the archive privacy report and reconcile App Store Connect App Privacy, metadata, claims, accessibility declarations, and privacy-policy URLs.
4. Validate/distribute through the intended TestFlight/App Store path and record processing/upload results.
5. Exercise the actual signed build on representative physical devices and real system surfaces.
6. Record APNs/server/account/storefront/capability state separately from local evidence.
7. Report what remains unproven: App Review, production rollout, all devices, all locales, or future OS behavior.


## Sources

- [Privacy manifest files](https://developer.apple.com/documentation/bundleresources/privacy-manifest-files)
- [Adding a privacy manifest to your app or third-party SDK](https://developer.apple.com/documentation/bundleresources/adding-a-privacy-manifest-to-your-app-or-third-party-sdk)
- [Describing use of required reason API](https://developer.apple.com/documentation/bundleresources/describing-use-of-required-reason-api)
- [Describing data use in privacy manifests](https://developer.apple.com/documentation/bundleresources/describing-data-use-in-privacy-manifests)
- [App privacy details on the App Store](https://developer.apple.com/app-store/app-privacy-details/)
- [Swift Testing](https://developer.apple.com/documentation/testing)
- [Adding tests to your Xcode project](https://developer.apple.com/documentation/xcode/adding-tests-to-your-xcode-project)
- [Improving code assessment by organizing tests into test plans](https://developer.apple.com/documentation/xcode/organizing-tests-to-improve-feedback)
- [Running tests and interpreting results](https://developer.apple.com/documentation/xcode/running-tests-and-interpreting-results)
- [Testing](https://developer.apple.com/documentation/xcode/testing)
- [Logging](https://developer.apple.com/documentation/os/logging/)
- [Generating log messages from your code](https://developer.apple.com/documentation/os/generating-log-messages-from-your-code)
- [Recording Performance Data](https://developer.apple.com/documentation/os/recording-performance-data)
- [MetricKit](https://developer.apple.com/documentation/metrickit)
- [Monitoring app performance with MetricKit](https://developer.apple.com/documentation/metrickit/monitoring-app-performance-with-metrickit)
- [MXMetricManager](https://developer.apple.com/documentation/metrickit/mxmetricmanager)
- [MetricManager](https://developer.apple.com/documentation/metrickit/metricmanager)
- [MetricKit updates](https://developer.apple.com/documentation/updates/metrickit)
- [Performing accessibility testing for your app](https://developer.apple.com/documentation/accessibility/performing-accessibility-testing-for-your-app)
- [VoiceOver](https://developer.apple.com/documentation/accessibility/voiceover)
- [Optimizing your app for Assistive Access](https://developer.apple.com/documentation/accessibility/optimizing-your-app-for-assistive-access)
- [App Intents](https://developer.apple.com/documentation/appintents/)
- [WidgetKit](https://developer.apple.com/documentation/widgetkit/)
- [ActivityKit](https://developer.apple.com/documentation/activitykit/)
- [Running your app on simulated or physical devices](https://developer.apple.com/documentation/xcode/running-your-app-on-simulated-or-physical-devices)
- [Preparing your app for distribution](https://developer.apple.com/documentation/xcode/preparing-your-app-for-distribution)
- [Distributing your app for beta testing and releases](https://developer.apple.com/documentation/xcode/distributing-your-app-for-beta-testing-and-releases/)
- [Testing a release build](https://developer.apple.com/documentation/xcode/testing-a-release-build)
- [TestFlight overview](https://developer.apple.com/help/app-store-connect/test-a-beta-version/testflight-overview)
- [Upload builds](https://developer.apple.com/help/app-store-connect/manage-builds/upload-builds)
- [App Store Review Guidelines](https://developer.apple.com/app-store/review/guidelines/)
