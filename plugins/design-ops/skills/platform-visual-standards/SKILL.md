---
name: platform-visual-standards
description: "Current platform visual standards: iOS 26 Liquid Glass and SF Symbols 7, Material 3 Expressive (HCT, Dynamic Color, spring physics), web CSS 2025-2026 (container queries, view transitions, anchor positioning), plus watchOS, tvOS, and automotive. Use when a design must feel native to its platform."
allowed-tools: Read, Grep, Glob
---

# Platform Visual Standards

Every platform has its own materials, motion, type, spacing, and input idioms. Users carry muscle memory from their OS, so recommendations must be platform-native, not platform-generic. This skill owns iOS 26 Liquid Glass and Material 3 Expressive; other skills point here for both.

## Routing

| Question | Read |
|----------|------|
| iPhone/iPad: Liquid Glass materials, vibrancy, `.glassEffect()`, SF Symbols 7, Dynamic Island, safe areas, Dynamic Type, floating tab bar, Reduce Transparency, migration | `references/ios-26-liquid-glass.md` |
| Android/Wear OS: M3 Expressive shapes, motion schemes and spring tokens, HCT, Dynamic Color, tonal elevation, type scale, components, canonical layouts, Compose | `references/material-3-expressive.md` |
| Web: container queries, `:has()`, view transitions, scroll-driven animation, anchor positioning, nesting, `@scope`, `@layer`, `@property`, oklch/`color-mix()`, `light-dark()`, `@starting-style`, popover/`<dialog>` | `references/web-css-2025-2026.md` |
| Watch, TV (10-foot UI, D-pad focus), automotive (NHTSA glance limits, night mode), kiosk, e-ink | `references/watchos-tvos-automotive.md` |
| visionOS, Meta Quest, WebXR, AR: depth, gaze + pinch, ornaments, passthrough | `references/spatial-xr-design.md` |
| One design system across 9 form factors: device matrix, token layers, breakpoints, adapt vs unify, CSS/SwiftUI/Compose token mapping | `references/cross-platform-harmony.md` |

## Core Rules

**iOS 26 Liquid Glass**
- Glass is for the navigation layer only (tab bars, toolbars, nav bars, sidebars, sheets, floating controls). Never put content — lists, cards in feeds, reading text, data tables — on glass.
- Text on glass uses semantic styles (`.primary`/`.secondary`/`.tertiary`) for vibrancy. Never lower opacity or hardcode white/black.
- Every custom glass view needs an opaque fallback for Reduce Transparency and a visible border when it is tappable.
- System bars adopt glass automatically on the iOS 26 SDK; remove custom bar backgrounds instead of fighting them.

**Material 3 Expressive**
- Motion is spring-based: each spring is stiffness + damping ratio, chosen from the standard or expressive motion scheme (spatial vs effects, fast/default/slow). Effects springs never bounce.
- Color comes from Dynamic Color roles (HCT tonal palettes), never raw hex in components. Tone difference 50+ gives 4.5:1; 40+ gives 3:1.
- Elevation is tonal (surface shifts toward primary), not gray shadows.
- Touch targets stay 48dp in every morphing shape state.

**Web**
- Prefer native CSS (container queries, `:has()`, anchor positioning, view transitions, popover, `<dialog>`) over JavaScript equivalents. Use oklch for perceptually even scales.

**Other form factors**
- Watch: one primary metric per screen, parsable in under 3 seconds, at most 3 information groups.
- TV: focus must always be visible; every flow completable with D-pad + Select + Back; text never below 16px at 1080p (24px at 4K); card titles 24px+.
- Car: 2-second single glance, 12-second total task, voice for anything longer; lock complex input while moving.
- XR: gaze selects, pinch confirms (no dwell activation); 60pt minimum targets; never place UI behind the user.

**Platform-native motion values** in the iOS and M3 references are platform specs, not the product's base motion scale. Base durations and easings live in `interaction-motion-design` (its `animation-timing-curves.md` reference).

## Adapt vs Unify

Adapt to the platform for native controls users expect, navigation structure, system gestures (iOS swipe-back, Android predictive back), accessibility APIs, and legal requirements (NHTSA, WCAG). Unify for brand color, typography, iconography, domain-specific interactions with no platform equivalent, and content areas inside platform-native chrome. Define tokens once (global → alias → component/platform override) and generate CSS, SwiftUI, and Compose from the same source.

| Platform | Users expect | Users reject |
|----------|-------------|-------------|
| iOS | System gestures, Liquid Glass chrome, SF Symbols | Hamburger menus, Material FABs, overridden system font |
| Android | Material components, Dynamic Color, predictable back | Non-standard back, unlabeled tab bars |
| Web | Fast load, keyboard access, URL state, responsive | Mobile tab bar on desktop |
| Watch | Instant info, complications | Forms, long text, deep hierarchy |
| TV | Visible focus, large text, card rails | Hover or touch assumptions |
| Car | Voice-first, huge targets | Text-heavy, multi-step flows |
| XR | Depth, gaze response, comfort | Flat panels, tiny targets |

## Cross-References

- **`visual-design-mastery`** — Visual principles that apply across all platforms. This skill adapts those principles to platform-specific conventions.
- **`mobile-ux-design`** — Mobile UX patterns. This skill provides the current visual standards those patterns render within.
- **`desktop-app-design`** — Desktop patterns. This skill provides web/macOS/Windows visual standards.
- **`component-patterns-code`** — Code implementations. This skill ensures code targets the right platform APIs.
- **`design-systems-architecture`** — Token architecture. This skill defines platform-specific token overrides.
- **`interaction-motion-design`** — Base motion scale and patterns. This skill provides platform-native springs and APIs.
- **`accessibility-inclusive-design`** — Platform-specific accessibility APIs (VoiceOver, TalkBack, ARIA).

## Commands Powered by This Skill

| Command | How This Skill Is Used |
|---------|----------------------|
| `/grade` | Adapts visual direction to target platform conventions |
| `/component` | Generates platform-native component code |
| `/screen` | Uses platform-specific screen patterns and safe areas |
| `/responsive` | Cross-device adaptation using platform breakpoints |
| `/generate` | Informs generation prompts with platform constraints and generates assets at platform-correct sizes |
