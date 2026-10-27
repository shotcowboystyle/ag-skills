# Starter assets

Pick one starter for the selected playbook. Every starter is a scaffold: none
proves that the user's target compiles, registers, or runs on glasses. Paths
are relative to this skill's `assets/` folder.

| Starter | Use | What it proves, and its gate |
| --- | --- | --- |
| [Shared domain](../assets/meta-wearables-domain-starter) | Typed product state, epoch handling, teardown ordering, phone fallback. No DAT/Android/Web SDK imports. | Passing `swift test` proves shared reducer behavior only, never SDK compilation or hardware support. |
| [iOS camera](../assets/meta-wearables-ios-camera-starter/MetaWearablesCameraStarter.swift) | DAT 0.9 camera/photo work. Keeps raw frames inside the adapter; makes photo handoff, permission, stream, and child-before-parent teardown explicit. | Type-checks against the selected `MWDATCore`/`MWDATCamera` simulator frameworks. |
| [Android camera](../assets/meta-wearables-android-camera-starter/MetaWearablesAndroidCameraStarter.kt) | DAT 0.9 Android camera/photo work, following the official `CameraAccess` `DatResult`/`Flow` shape. | Android target compile gate until the selected Maven artifacts resolve. |
| [iOS MockDevice](../assets/meta-wearables-ios-mockdevice-starter/MetaWearablesMockDeviceStarter.swift) | Deterministic iOS DAT fixtures; keeps mock lifecycle, permission, media, and captouch controls outside shared state. | Type-checks against DAT 0.9.0 `MWDATCore`/`MWDATMockDevice`. |
| [iOS MockDevice test client](../assets/meta-wearables-ios-mockdevice-test-client-starter/MetaWearablesMockDeviceTestClientStarter.swift) | XCUITest control of the app process's MockDevice test server; keeps the app/server versus UI-test process boundary explicit. | Type-checks against the test-only `MWDATMockDeviceTestClient` product. |
| [Android MockDevice](../assets/meta-wearables-android-mockdevice-starter/MetaWearablesAndroidMockDeviceStarter.kt) | Deterministic Android DAT instrumentation fixtures, following the official 0.9.0 `MockDeviceKit` sample. | Android target compile gate until the Maven artifacts resolve. |
| [iOS native Display](../assets/meta-wearables-ios-display-starter/MetaWearablesDisplayStarter.swift) | Native DAT Display: `supportsDisplay()`, `DeviceSession` state/error streams, `session.addDisplay()`, `Display.statePublisher`, `Display.send(FlexBox)`, child-before-parent teardown. | Type-check against the selected SPM product first. Not proof of registration, physical rendering, or input. |
| [Android native Display](../assets/meta-wearables-android-display-starter/MetaWearablesAndroidDisplayStarter.kt) | Native DAT Android Display: `SpecificDeviceSelector`, `Wearables.createSession(...).fold`, `DeviceSession` `Flow` collection, `addDisplay()`, `Display.state`, `sendContent`, `buttonGroup`, `removeDisplay()`, parent-session stop. | Compile in the selected Android target; the uncompiled asset is not target or hardware proof. |
| [Android target](../assets/meta-wearables-android-target-starter/README.md) | New sibling Gradle project when Android is selected but no target exists. Pins the 0.9.0 full-artifact DAT graph and GitHub Packages route; keeps Developer Center values out of the archive; stops at a target-owned `Wearables.initialize(context)` bootstrap. | A build-graph seed, not a DAT compile receipt. Credentials stay in ignored local properties or environment variables. |
| [Web App](../assets/meta-wearables-web-starter) | Ray-Ban Display Web App reducer. Run `node --test test/display-state.test.mjs` in the starter folder. | Proves bounded 600×600 state/input/fallback behavior only; toolkit contract, browser simulator, hosted URL, and physical Display stay separate gates. |

## Workflow detail

- Resolve the selected release's generated API before writing imports or
  method signatures. Label any source-index-only or moving-reference name
  `to-verify`; use a clearly marked placeholder instead of inventing syntax.
- Keep shared product state free of MWDAT types, Kotlin classes, browser
  events, raw frames, raw audio, tokens, and device identifiers.
- If Android has no target, instantiate the target starter in a sibling folder,
  configure private values through ignored local properties or environment
  variables, and record the resulting `PRE-*` target receipt before adding
  capability code.
