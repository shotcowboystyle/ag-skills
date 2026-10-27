# Native DAT Display — details

Design the glasses surface as a small, stateful system surface. The phone stays
the configuration, consent, recovery, and detailed-content surface unless the
product has a proven reason to move that work onto the Display.

This covers native DAT Display only. A 600×600 Ray-Ban Display Web App has a
different API, deployment, and proof route; use
[Web Apps](../../meta-wearables-web-apps/SKILL.md) for it.

## Read

- [Display access and glasses UI](../../meta-wearables-knowledge-base/references/70-meta-wearables/04-display-access-and-glasses-ui.md)
- [Device models and capability matrix](../../meta-wearables-knowledge-base/references/70-meta-wearables/05-device-models-and-capability-matrix.md)
- [DAT iOS API surface atlas](../../meta-wearables-knowledge-base/references/70-meta-wearables/10-dat-ios-api-surface-atlas.md) for the Display module, capability, ButtonGroup, video, and teardown map
- [On-device compliance](../../meta-wearables-knowledge-base/references/70-meta-wearables/17-on-device-compliance-and-runtime-contract.md) for sanitized payloads, stale data, and fallback
- [Operational readiness](../../meta-wearables-knowledge-base/references/70-meta-wearables/18-operational-readiness-and-recovery.md) for firmware, on-glasses DAT-app provisioning, and Display update-required errors
- Official [DAT iOS Display skill](https://github.com/facebook/meta-wearables-dat-ios/tree/main/plugins/mwdat-ios/skills/display-access), [DAT Android Display skill](https://github.com/facebook/meta-wearables-dat-android/blob/main/plugins/mwdat-android/skills/display-access/SKILL.md), and [Display documentation](https://wearables.developer.meta.com/docs/develop/)

Starters: [iOS Display](../../meta-wearables-implementation-recipes/assets/meta-wearables-ios-display-starter/MetaWearablesDisplayStarter.swift),
[Android Display](../../meta-wearables-implementation-recipes/assets/meta-wearables-android-display-starter/MetaWearablesAndroidDisplayStarter.kt).

## Workflow

1. Ask the runtime device whether it supports Display, using the selected release's capability API (for example `DeviceType.supportsDisplay()`). Do not infer capability from a product name.
2. Define a compact state machine: `hidden`, `presenting`, `focused`, `actionAvailable`, `dismissed`, `timedOut`, `disconnected`, `unsupported`.
3. Build one clear root view per feature, legible at a glance. Prefer one primary status or action over a miniature phone screen.
4. Use the current input contract (`ButtonGroup`, `Button`, `FlexBox.onTap` where exposed). Model focus, selection, previous/next, dismiss, timeout, and accidental input.
5. Keep the source of truth in the phone domain layer. Project a small, sanitized snapshot and define behavior when it is stale.
6. Clear or replace the Display on completion, cancellation, disconnect, and route change (for example `Display.clearDisplay()` where available).
7. Test supported and unsupported models, no connection, long text, dynamic state, low confidence, and a lost phone session.

## Interaction and visual contract

- One glance explains what changed and what action is possible.
- High contrast, short labels, stable focus, predictable action order.
- No private content, sensitive transcription, or raw media unless designed and disclosed.
- Every glasses action has a phone fallback and a recoverable error state.
- No assumptions about color, brightness, input, or resolution beyond current official device documentation.

## Proof limits

- `supportsDisplay()` is a gate, not proof that a product-generation label is supported.
- A mock Display or screenshot proves layout logic only, not brightness, focus, button behavior, latency, or comfort.

## Sources

- [Meta DAT iOS changelog](https://github.com/facebook/meta-wearables-dat-ios/blob/main/CHANGELOG.md)
- [Full Wearables platform reference](https://wearables.developer.meta.com/llms.txt?full=true)
- [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/)
- [Apple accessibility fundamentals](https://developer.apple.com/documentation/swiftui/accessibility-fundamentals)
