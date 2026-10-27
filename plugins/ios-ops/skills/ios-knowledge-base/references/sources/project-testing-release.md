# Official sources: Project, testing, privacy, and release

Checked against Apple documentation on **2026-08-19** (iOS 26 / Xcode 26 SDK cycle). Apple documentation changes; re-open the page before relying on a version-sensitive API.

## Design and SwiftUI

| Topic | Official source |
| --- | --- |
| Xcode previews | [Previews in Xcode](https://developer.apple.com/documentation/swiftui/previews-in-xcode) |

## Availability, capabilities, and proof

| Topic | Official source |
| --- | --- |
| Release-environment testing | [Testing a release build](https://developer.apple.com/documentation/xcode/testing-a-release-build) |

## Swift Package Manager, macros, plugins, and Xcode composition

| Topic | Official source |
| --- | --- |
| Swift package model | [PackageDescription](https://docs.swift.org/swiftpm/documentation/packagedescription/), [Package](https://docs.swift.org/swiftpm/documentation/packagedescription/package/), and [Introducing Packages](https://docs.swift.org/swiftpm/documentation/packagemanagerdocs/introducingpackages/) |
| Targets, products, dependencies, and resources | [Target](https://docs.swift.org/swiftpm/documentation/packagedescription/target/), [Target dependencies](https://docs.swift.org/swiftpm/documentation/packagedescription/target/dependencies/), [Target type](https://docs.swift.org/swiftpm/documentation/packagedescription/target/targettype/), and [Adding package dependencies](https://docs.swift.org/swiftpm/documentation/packagemanagerdocs/addingdependencies/) |
| Xcode package integration | [Swift packages in Xcode](https://developer.apple.com/documentation/xcode/swift-packages), [Adding package dependencies to your app](https://developer.apple.com/documentation/xcode/adding-package-dependencies-to-your-app), and [Creating a standalone Swift package with Xcode](https://developer.apple.com/documentation/xcode/creating-a-standalone-swift-package-with-xcode) |
| Dependency resolution and binary trust | [Identifying binary dependencies](https://developer.apple.com/documentation/xcode/identifying-binary-dependencies) and [Swift package dependencies](https://developer.apple.com/documentation/xcode/swift-packages) |
| Swift macros | [The Swift Programming Language: Macros](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/macros/) and [PackageDescription macro targets](https://docs.swift.org/swiftpm/documentation/packagedescription/target/targettype/) |
| Build-tool and command plugins | [PackagePlugin](https://docs.swift.org/swiftpm/documentation/packageplugin/), [Plugins](https://docs.swift.org/swiftpm/documentation/packagemanagerdocs/plugins/), [Writing a build tool plugin](https://docs.swift.org/swiftpm/documentation/packagemanagerdocs/writingbuildtoolplugin/), and [Writing a command plugin](https://docs.swift.org/swiftpm/documentation/packagemanagerdocs/writingcommandplugin/) |
| Plugin enablement and commands | [Enable a build tool plugin](https://docs.swift.org/swiftpm/documentation/packagemanagerdocs/enablebuildplugin/), [Enable a command plugin](https://docs.swift.org/swiftpm/documentation/packagemanagerdocs/enablecommandplugin/), and [Swift package commands](https://docs.swift.org/swiftpm/documentation/packagemanagerdocs/swiftpackagecommands/) |
| Liquid Glass composition | [Liquid Glass technology overview](https://developer.apple.com/documentation/TechnologyOverviews/liquid-glass) and [Applying Liquid Glass to custom views](https://developer.apple.com/documentation/swiftui/applying-liquid-glass-to-custom-views) |
| On-device AI module boundary | [AI and machine learning](https://developer.apple.com/documentation/TechnologyOverviews/ai-machine-learning) and [Foundation Models](https://developer.apple.com/documentation/foundationmodels/) |
| Accessibility and release evidence | [Accessibility fundamentals](https://developer.apple.com/documentation/swiftui/accessibility-fundamentals), [Testing system accessibility features](https://developer.apple.com/documentation/accessibility/testing-system-accessibility-features-in-your-app), and [Testing a release build](https://developer.apple.com/documentation/xcode/testing-a-release-build) |

## Swift Testing, XCTest, UI automation, performance, and AI evaluation

| Topic | Official source |
| --- | --- |
| Swift Testing framework | [Swift Testing](https://developer.apple.com/documentation/testing), [Defining test functions](https://developer.apple.com/documentation/Testing/DefiningTests), and [Organizing test functions with suite types](https://developer.apple.com/documentation/Testing/OrganizingTests) |
| Async, parameterized, and parallel tests | [Testing asynchronous code](https://developer.apple.com/documentation/testing/testing-asynchronous-code), [Implementing parameterized tests](https://developer.apple.com/documentation/Testing/ParameterizedTesting), [Running tests serially or in parallel](https://developer.apple.com/documentation/Testing/Parallelization), and [Expectations and confirmations](https://developer.apple.com/documentation/Testing/Expectations) |
| Xcode testing and test targets | [Xcode testing](https://developer.apple.com/documentation/xcode/testing), [Adding tests to your Xcode project](https://developer.apple.com/documentation/xcode/adding-tests-to-your-xcode-project), and [Running tests and interpreting results](https://developer.apple.com/documentation/xcode/running-tests-and-interpreting-results) |
| Test plans | [Improving code assessment by organizing tests into test plans](https://developer.apple.com/documentation/xcode/organizing-tests-to-improve-feedback) |
| UI automation | [XCUIApplication](https://developer.apple.com/documentation/xcuiautomation/xcuiapplication), [XCUIElement](https://developer.apple.com/documentation/xcuiautomation/xcuielement), and [XCUIElementAttributes](https://developer.apple.com/documentation/xcuiautomation/xcuielementattributes) |
| Performance metrics | [Performance Tests](https://developer.apple.com/documentation/xctest/performance-tests), [XCTHitchMetric](https://developer.apple.com/documentation/xctest/xcthitchmetric), and [Improving your app’s performance](https://developer.apple.com/documentation/xcode/improving-your-app-s-performance) |
| Accessibility task testing | [Accessibility fundamentals](https://developer.apple.com/documentation/swiftui/accessibility-fundamentals) and [Testing system accessibility features](https://developer.apple.com/documentation/accessibility/testing-system-accessibility-features-in-your-app) |
| Release evidence | [Testing a release build](https://developer.apple.com/documentation/xcode/testing-a-release-build) |

## Xcode archive, signing, TestFlight, and release evidence

| Topic | Official source |
| --- | --- |
| Release archive and distribution | [Distributing your app for beta testing and releases](https://developer.apple.com/documentation/xcode/distributing-your-app-for-beta-testing-and-releases) |
| Release configuration | [Testing a release build](https://developer.apple.com/documentation/xcode/testing-a-release-build) and [Build settings reference](https://developer.apple.com/documentation/xcode/build-settings-reference) |
| Privacy manifests | [Privacy manifest files](https://developer.apple.com/documentation/bundleresources/privacy-manifest-files), [Adding a privacy manifest to your app or third-party SDK](https://developer.apple.com/documentation/bundleresources/adding-a-privacy-manifest-to-your-app-or-third-party-sdk), and [Describing use of required reason API](https://developer.apple.com/documentation/bundleresources/describing-use-of-required-reason-api) |
| Upload and process a build | [Upload builds](https://developer.apple.com/help/app-store-connect/manage-builds/upload-builds) |
| TestFlight beta testing | [TestFlight overview](https://developer.apple.com/help/app-store-connect/test-a-beta-version/testflight-overview) |
| Select a processed build | [Choose a build to submit](https://developer.apple.com/help/app-store-connect/manage-builds/choose-a-build-to-submit) |
| Submit an app | [Submit an app](https://developer.apple.com/help/app-store-connect/manage-submissions-to-app-review/submit-an-app/) |
| Publish an app | [Overview of publishing your app on the App Store](https://developer.apple.com/help/app-store-connect/manage-your-apps-availability/overview-of-publishing-your-app-on-the-app-store/) |
| Review requirements | [App Store Review Guidelines](https://developer.apple.com/app-store/review/guidelines/) |

## Xcode Cloud CI/CD and release automation

| Topic | Official source |
| --- | --- |
| Xcode Cloud overview | [Xcode Cloud](https://developer.apple.com/documentation/xcode/xcode-cloud) |
| Onboarding | [Getting started with Xcode Cloud](https://developer.apple.com/documentation/xcode/getting-started-with-xcode-cloud) and [Setting up your project to use Xcode Cloud](https://developer.apple.com/documentation/xcode/setting-up-your-project-to-use-xcode-cloud) |
| First workflow | [Configuring your first Xcode Cloud workflow](https://developer.apple.com/documentation/xcode/configuring-your-first-xcode-cloud-workflow) |
| Workflow strategy | [Developing a workflow strategy for Xcode Cloud](https://developer.apple.com/documentation/xcode/developing-a-workflow-strategy-for-xcode-cloud) and [Xcode Cloud workflow reference](https://developer.apple.com/documentation/xcode/xcode-cloud-workflow-reference) |
| Start conditions and actions | [Configuring start conditions](https://developer.apple.com/documentation/xcode/configuring-start-conditions) and [Configuring your Xcode Cloud workflow’s actions](https://developer.apple.com/documentation/xcode/configuring-your-xcode-cloud-workflow-s-actions) |
| Distribution workflow | [Creating a workflow that builds your app for distribution](https://developer.apple.com/documentation/xcode/creating-a-workflow-that-builds-your-app-for-distribution) and [Distributing your Xcode Cloud builds through TestFlight](https://developer.apple.com/documentation/xcode/distributing-your-xcode-cloud-builds-through-testflight) |
| Scripts and variables | [Writing custom build scripts](https://developer.apple.com/documentation/xcode/writing-custom-build-scripts), [Environment variable reference](https://developer.apple.com/documentation/xcode/environment-variable-reference), and [Sharing environment variables across Xcode Cloud workflows](https://developer.apple.com/documentation/xcode/sharing-environment-variables-across-xcode-cloud-workflows) |
| Pull-request protection | [Configuring requirements for merging a pull request](https://developer.apple.com/documentation/xcode/configuring-requirements-for-merging-a-pull-request) |
| Artifact retention and diagnosis | [Configuring your first Xcode Cloud workflow](https://developer.apple.com/documentation/xcode/configuring-your-first-xcode-cloud-workflow) and [Resolving common configuration and build issues](https://developer.apple.com/documentation/xcode/resolving-common-configuration-and-build-issues) |
| Infrastructure validation | [Understanding Xcode Cloud infrastructure validation builds](https://developer.apple.com/documentation/xcode/understanding-infrastructure-validation-builds) |
| Webhooks | [Configuring webhooks in Xcode Cloud](https://developer.apple.com/documentation/xcode/configuring-webhooks-in-xcode-cloud) |
| App Store Connect API | [Xcode Cloud Workflows and Builds](https://developer.apple.com/documentation/appstoreconnectapi/xcode-cloud-workflows-and-builds) |
| TestFlight notes | [Including notes for testers with a beta release](https://developer.apple.com/documentation/xcode/including-notes-for-testers-with-a-beta-release-of-your-app) |

## SwiftUI animation, motion, transitions, and feedback

| Topic | Official source |
| --- | --- |
| Motion performance and hitches | [Understanding hitches in your app](https://developer.apple.com/documentation/xcode/understanding-hitches-in-your-app), [Improving app responsiveness](https://developer.apple.com/documentation/xcode/improving-app-responsiveness), [Performance Tests](https://developer.apple.com/documentation/xctest/performance-tests), and [XCTHitchMetric](https://developer.apple.com/documentation/xctest/xcthitchmetric) |

## SwiftUI accessibility and alternate input

| Topic | Official source |
| --- | --- |
| Accessibility task testing | [Performing accessibility testing for your app](https://developer.apple.com/documentation/accessibility/performing-accessibility-testing-for-your-app), [Accessibility Inspector](https://developer.apple.com/documentation/accessibility/accessibility-inspector), [Inspecting the accessibility of the screens in your app](https://developer.apple.com/documentation/accessibility/inspecting-the-accessibility-of-screens), [Testing system accessibility features in your app](https://developer.apple.com/documentation/accessibility/testing-system-accessibility-features-in-your-app), and [VoiceOver](https://developer.apple.com/documentation/accessibility/voiceover) |

## SwiftUI collections, scrolling, and adaptive layout

| Topic | Official source |
| --- | --- |
| Collection proof and performance | [Accessibility fundamentals](https://developer.apple.com/documentation/swiftui/accessibility-fundamentals), [Performing accessibility testing for your app](https://developer.apple.com/documentation/accessibility/performing-accessibility-testing-for-your-app), [Improving your app’s performance](https://developer.apple.com/documentation/xcode/improving-your-app-s-performance/), [Performance Tests](https://developer.apple.com/documentation/xctest/performance-tests), and [Testing a release build](https://developer.apple.com/documentation/xcode/testing-a-release-build) |

## SwiftUI interoperability, previews, and adaptive platforms

| Topic | Official source |
| --- | --- |
| Xcode previews, traits, and parameterized fixtures | [Previewing your app’s interface in Xcode](https://developer.apple.com/documentation/xcode/previewing-your-apps-interface-in-xcode), [Previews in Xcode](https://developer.apple.com/documentation/swiftui/previews-in-xcode), and [SwiftUI](https://developer.apple.com/documentation/swiftui) |

## Privacy manifests and App Store privacy

| Topic | Official source |
| --- | --- |
| Privacy manifest overview | [Privacy manifest files](https://developer.apple.com/documentation/bundleresources/privacy-manifest-files) |
| Add a privacy manifest | [Adding a privacy manifest to your app or third-party SDK](https://developer.apple.com/documentation/bundleresources/adding-a-privacy-manifest-to-your-app-or-third-party-sdk) |
| Required-reason API declarations | [Describing use of required reason API](https://developer.apple.com/documentation/bundleresources/describing-use-of-required-reason-api) |
| Required-reason API implementation note | [TN3183: Adding required reason API entries to your privacy manifest](https://developer.apple.com/documentation/technotes/tn3183-adding-required-reason-api-entries-to-your-privacy-manifest) |
| Collected-data declarations | [Describing data use in privacy manifests](https://developer.apple.com/documentation/bundleresources/describing-data-use-in-privacy-manifests) |
| App privacy details | [App privacy details on the App Store](https://developer.apple.com/app-store/app-privacy-details/) |
| App Store Connect privacy workflow | [Manage app privacy](https://developer.apple.com/help/app-store-connect/manage-app-information/manage-app-privacy) |
| App privacy reference | [App privacy](https://developer.apple.com/help/app-store-connect/reference/app-privacy/) |

## Testing, logging, performance, and diagnostics

| Topic | Official source |
| --- | --- |
| Swift Testing framework | [Swift Testing](https://developer.apple.com/documentation/testing) |
| Add test targets | [Adding tests to your Xcode project](https://developer.apple.com/documentation/xcode/adding-tests-to-your-xcode-project) |
| Test plans | [Improving code assessment by organizing tests into test plans](https://developer.apple.com/documentation/xcode/organizing-tests-to-improve-feedback) |
| Run and interpret tests | [Running tests and interpreting results](https://developer.apple.com/documentation/xcode/running-tests-and-interpreting-results) |
| Xcode testing strategy | [Testing](https://developer.apple.com/documentation/xcode/testing) |
| Unified logging | [Logging](https://developer.apple.com/documentation/os/logging/) |
| Swift log messages | [Generating log messages from your code](https://developer.apple.com/documentation/os/generating-log-messages-from-your-code) |
| Signpost intervals | [Recording Performance Data](https://developer.apple.com/documentation/os/recording-performance-data) |
| Historical log access | [OSLog](https://developer.apple.com/documentation/oslog) |
| Daily real-device reports | [MetricKit](https://developer.apple.com/documentation/metrickit) |
| MetricKit reporting model | [Monitoring app performance with MetricKit](https://developer.apple.com/documentation/metrickit/monitoring-app-performance-with-metrickit) |
| Legacy iOS 26-compatible MetricKit route | [MXMetricManager](https://developer.apple.com/documentation/metrickit/mxmetricmanager) |
| Newer Swift-first MetricKit route | [MetricManager](https://developer.apple.com/documentation/metrickit/metricmanager) |
| MetricKit API changes | [MetricKit updates](https://developer.apple.com/documentation/updates/metrickit) |
| XCTest performance metrics | [Performance Tests](https://developer.apple.com/documentation/xctest/performance-tests) |
| Hitch measurement | [XCTHitchMetric](https://developer.apple.com/documentation/xctest/xcthitchmetric) |

## Distribution, release, and App Store Connect

| Topic | Official source |
| --- | --- |
| Prepare for distribution | [Preparing your app for distribution](https://developer.apple.com/documentation/xcode/preparing-your-app-for-distribution) |
| Archive and distribute | [Distributing your app for beta testing and releases](https://developer.apple.com/documentation/xcode/distributing-your-app-for-beta-testing-and-releases/) |
| Test a Release configuration | [Testing a release build](https://developer.apple.com/documentation/xcode/testing-a-release-build) |
| TestFlight workflow | [TestFlight overview](https://developer.apple.com/help/app-store-connect/test-a-beta-version/testflight-overview) |
| Upload builds | [Upload builds](https://developer.apple.com/help/app-store-connect/manage-builds/upload-builds) |
| App information and metadata | [App information](https://developer.apple.com/help/app-store-connect/reference/app-information/app-information) |
| Review policy | [App Store Review Guidelines](https://developer.apple.com/app-store/review/guidelines/) |
