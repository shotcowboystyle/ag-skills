---
name: mobile-ux-design
description: "Mobile-first design: touch targets, gesture systems, thumb zones, responsive layout, mobile forms and navigation, iOS 26 Liquid Glass, Material 3 Expressive, and wearable/IoT patterns. Use when designing or auditing an iOS, Android, or responsive mobile experience."
allowed-tools: Read, Grep, Glob
---

# Mobile UX Design — Platform-Native Excellence

## Mobile-First Philosophy (Luke Wroblewski)

"Mobile forces you to focus. There's simply not enough room for anything extraneous." — Luke Wroblewski

Mobile-first design is not about making desktop designs smaller. It is about starting with the most constrained environment to identify what truly matters, then progressively enhancing for larger screens. This constraint-driven approach produces cleaner, more focused experiences across all platforms.

### Core Principles

1. **Content first, navigation second** — prioritize the user's primary task above all interface chrome
2. **One primary action per screen** — resist the urge to present multiple equal-weight choices
3. **Design for interruption** — mobile users are frequently interrupted; support save, resume, and quick task completion
4. **Respect the thumb** — the most natural interaction zone determines layout hierarchy
5. **Performance is UX** — a 100ms delay feels instant, 1s feels responsive, 3s+ feels broken

## Touch Interaction Design

### Thumb Zone Optimization

Based on Steven Hoober's research on how people hold phones:

- **Primary zone (easy reach):** Bottom-center of screen — place primary actions here
- **Secondary zone (stretch):** Middle and sides — place secondary content and navigation
- **Tertiary zone (hard reach):** Top corners — avoid placing frequent-use controls here
- **Bottom navigation pattern** now dominates both iOS and Android for this reason
- Large phones (6.5"+) make top-left especially difficult — anchor critical UI to bottom

### Touch Target Sizing

- **Minimum:** 44x44pt (iOS) / 48x48dp (Android) — Apple and Google guidelines
- **Recommended:** 48x48pt for primary actions — NNG recommends even larger for critical actions
- **Spacing between targets:** Minimum 8pt gap to prevent mis-taps
- **Edge targets:** Add extra padding near screen edges where grip interferes
- Text links in body copy need generous tap targets — extend the clickable area beyond visible text

### Gesture Design

**Standard gestures (use without instruction):**
- Tap, double-tap, long-press, swipe, pinch-to-zoom, pull-to-refresh

**Discoverable gestures (need visual hints):**
- Swipe to delete/archive (show peek on edge swipe), drag to reorder (use grab handles)

**Avoid:**
- Custom gestures that conflict with system gestures (especially edge swipes on iOS/Android)
- Gestures as the only path to an action — always provide a visible alternative
- Multi-finger gestures beyond pinch-to-zoom on phones

## Platform Conventions (summary)

- **iOS:** tab bar (max 5) + navigation bar with swipe-back on every pushed view; SF Pro with Dynamic Type; 16pt margins; sheets over full-screen modals; respect Dynamic Island and home-indicator safe areas.
- **Android:** bottom navigation bar (3-5) or drawer for more; Material type scale; 16dp margins on a 4dp grid; Dynamic Color-ready palettes; one FAB per screen; predictive back; edge-to-edge with insets.
- Never force one platform's patterns onto the other; React Native and Flutter apps should still feel native. Test on real devices.
- Liquid Glass and Material 3 Expressive specifics are owned by `platform-visual-standards` (its `ios-26-liquid-glass.md` and `material-3-expressive.md` references).

## Routing

| Question | Read |
|----------|------|
| Where iOS and Android differ: navigation, sheets, contextual actions, search, settings, notifications, onboarding, permissions, gestures, widgets, full platform conventions | `references/ios-android-patterns.md` |
| Mobile forms and navigation: field design, keyboards, autofill, wizards, address/payment input, auth flows, tab bars, deep links, quick rules | `references/mobile-form-navigation.md` |
| Responsive breakpoints, reflow patterns, fluid type, Core Web Vitals, skeletons, optimistic UI, offline-first | `references/responsive-performance.md` |
| Beyond the phone: glanceable design, watch, rings, hearables, AR glasses, IoT, connected home, automotive | `references/wearable-iot-patterns.md` |
| iOS 26 Liquid Glass, Material 3 Expressive | `platform-visual-standards` skill |

## Cross-Referencing

- For visual design and typography details, reference `visual-design-mastery`
- For accessibility requirements on mobile, reference `accessibility-inclusive-design`
- For motion and interaction design, reference `interaction-motion-design`
- For design system component patterns, reference `design-systems-architecture`
- For platform materials (Liquid Glass, M3 Expressive), reference `platform-visual-standards`
- Production mobile components (bottom sheets, gesture navigation, platform-adaptive variants): `component-patterns-code`
- Haptic patterns per interaction type: `interaction-motion-design` (its `haptic-feedback-design-system.md` reference)

## Key Sources

- Wroblewski, L. (2011). "Mobile First"
- Hoober, S. (2017). "Design for Fingers, Touch, and People"
- Apple Human Interface Guidelines (2025)
- Google Material Design 3 Guidelines (2025)
- NNG Group mobile usability research
