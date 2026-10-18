# iOS Native Design and Liquid Glass Verification — details

## Verification matrix

| Surface | Check | Evidence boundary |
| --- | --- | --- |
| Hierarchy/navigation | Primary action, back behavior, sheet/toolbar semantics, loading/error/empty routes | A screenshot cannot prove state ownership or a complete navigation path. |
| Liquid Glass | System bars retained, custom glass justified, grouping/identity stable, content legible behind material | Preview/simulator cannot prove all physical contrast, performance, or OS-version behavior. |
| Adaptation | Dynamic Type, localization, split view, orientation, keyboard, long content, compact width | One device size or one language is not coverage. |
| Accessibility | VoiceOver labels/actions/focus, contrast, hit targets, captions, non-color/non-gesture alternatives, Reduce Motion/Effects | Static visual review cannot prove assistive technology behavior. |
| Interaction | Scroll, gesture cancellation, focus, keyboard/controller, haptic availability, transition interruption | A successful tap in a preview is not physical ergonomics or completion proof. |
| Release | Actual SDK availability, performance, system surface, signing, and supported device matrix | Documentation guidance does not prove the app compiles, passes review, or works in production. |


## Hard boundaries

- Never call a screenshot, preview, or simulator result proof of accessibility, physical ergonomics, performance, or release behavior.
- Never replace a semantic system control with a decorative imitation when the system control meets the product need.
- Never hide a missing state, contrast failure, reduced-effects path, or localization failure behind visual polish.


## Related routes and recipes

- [SwiftUI native design package](../../swiftui-native-design/SKILL.md)
- [Liquid Glass design package](../../liquid-glass-design/SKILL.md)
- [Apple-native design deep dives](../../ios-knowledge-base/references/21-design-deep-dives/README.md)
- [SwiftUI and Liquid Glass recipes](../../ios-knowledge-base/references/70-code-recipes/00-swiftui-and-liquid-glass-recipes.md)
- [Accessibility, adaptation, and native design recipes](../../ios-knowledge-base/references/70-code-recipes/12-accessibility-adaptive-and-native-design-recipes.md)
- [Interaction and transition recipes](../../ios-knowledge-base/references/70-code-recipes/07-interaction-and-transition-recipes.md)
- [Accessibility and adaptability checklist](../../ios-knowledge-base/references/60-verification/02-accessibility-and-adaptability-checklist.md)
- [Build, device, and release checklist](../../ios-knowledge-base/references/60-verification/01-build-device-and-release-checklist.md)


## Sources

- [SwiftUI](https://developer.apple.com/documentation/swiftui/)
- [Managing user interface state](https://developer.apple.com/documentation/swiftui/managing-user-interface-state)
- [Navigation](https://developer.apple.com/documentation/swiftui/navigation)
- [Accessibility fundamentals](https://developer.apple.com/documentation/swiftui/accessibility-fundamentals)
- [Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/)
- [Liquid Glass](https://developer.apple.com/documentation/TechnologyOverviews/liquid-glass)
- [Adopting Liquid Glass](https://developer.apple.com/documentation/TechnologyOverviews/adopting-liquid-glass)
- [Applying Liquid Glass to custom views](https://developer.apple.com/documentation/swiftui/applying-liquid-glass-to-custom-views)
- [GlassEffectContainer](https://developer.apple.com/documentation/swiftui/glasseffectcontainer)
- [Glass](https://developer.apple.com/documentation/swiftui/glass)
- [Accessibility modifiers](https://developer.apple.com/documentation/swiftui/view-accessibility)
- [DynamicTypeSize](https://developer.apple.com/documentation/swiftui/dynamictypesize)
- [Sensory feedback](https://developer.apple.com/documentation/swiftui/sensoryfeedback)
