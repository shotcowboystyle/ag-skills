---
name: interaction-motion-design
description: Micro-interactions, animation timing and easing curves, spring physics, transition choreography, haptic feedback vocabularies, and emotional design. Use when adding or reviewing animation, tuning motion duration, designing haptics, or supporting prefers-reduced-motion.
allowed-tools: Read, Grep, Glob
---

# Interaction & Motion Design — Purposeful Animation Framework

Motion connects interface states, communicates causality, and creates emotional resonance. Every animation must earn its milliseconds — gratuitous motion is worse than no motion at all.

## Core Principles (Disney's 12 Principles, Adapted for UI)

1. **Purpose over polish** — every animation must serve a functional role: guide attention, show relationships, confirm actions, or create continuity
2. **Physics-based movement** — natural motion follows physical laws (acceleration, deceleration, spring, gravity)
3. **Performance is non-negotiable** — animations must run at 60fps; a janky animation is worse than no animation
4. **Respect user preference** — honor `prefers-reduced-motion` unconditionally; motion sensitivity is real and common
5. **Subtlety scales** — small animations compound; individually subtle, collectively they define the interface's personality

## Base Motion Scale (owned here)

This skill owns the base motion tokens for design-ops. `animation-recipe-library` and `design-token-presets` use these names; the full spec with rationale is in `references/animation-timing-curves.md`.

| Token | Value | Use |
|---|---|---|
| `--ease-out` | `cubic-bezier(0.16, 1, 0.3, 1)` | Entrances |
| `--ease-in` | `cubic-bezier(0.55, 0.055, 0.675, 0.19)` | Exits |
| `--ease-in-out` | `cubic-bezier(0.87, 0, 0.13, 1)` | On-screen state changes |
| `--ease-spring` | `cubic-bezier(0.34, 1.56, 0.64, 1)` | Single overshoot (CSS stand-in for a spring) |
| `--duration-instant` | 50ms | Hover color, cursor |
| `--duration-fast` | 150ms | Press, toggle, focus, tooltip |
| `--duration-normal` | 250ms | Dropdown, dialog, card expand |
| `--duration-moderate` | 300ms | Panel slide, toast, view change |
| `--duration-slow` | 400ms | Modal with backdrop, page transition |
| `--duration-slower` | 600ms | Complex reflow, onboarding, celebration (rare) |

| Spring preset | Stiffness / damping / mass | Use |
|---|---|---|
| `spring-snappy` | 400 / 30 / 1 | Toggles, switches, presses |
| `spring-default` | 300 / 25 / 1 | General UI, panels, drag release |
| `spring-gentle` | 200 / 25 / 1 | Large surfaces, sheets, layout morphs |
| `spring-bouncy` | 300 / 10 / 1 | Celebrations, playful confirmations |

Platform springs (M3 Expressive, iOS 26 Liquid Glass): `platform-visual-standards`.

## Timing Rules

- Interface responses under 100ms feel instantaneous — do not animate these.
- User-initiated actions: 150-300ms (responsive, not sluggish).
- System-initiated changes: 200-500ms (smooth, noticeable enough to orient).
- Exits run 20-40% faster than the matching entrance.
- Never exceed 1000ms for any single transition in regular workflows.
- Mobile animations should be approximately 30% shorter than desktop equivalents for a faster feel.
- Never use linear easing for UI motion. The only exceptions are infinite progress indicators and color transitions.
- Prefer a spring for anything the user directly manipulates; prefer a bezier when timing must be predictable.

## Haptic Rules

- Pair haptics with visual feedback — never rely on haptics alone.
- Keep haptic patterns short (under 100ms) for UI feedback.
- Match haptic intensity to action significance.
- Disable haptics when user has reduced motion preferences.

## Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

**Preferred approach:** Replace motion with non-motion alternatives rather than removing all animation.

- Replace slide transitions with instant state changes or opacity fades.
- Replace bouncing/spinning with static state indicators.
- Keep essential functional animations (progress bars) but simplify them.
- Remove parallax, auto-playing video backgrounds, and decorative animations entirely.

## Routing

For **timing and easing** — the base motion scale, CSS animation fundamentals, the cubic-bezier deep dive, Material/Apple/brand curves, spring physics, duration calculation, stagger patterns, performance, the `@keyframes` pattern library, and the View Transitions API: read `references/animation-timing-curves.md`.

For **concrete UI patterns** — button, toggle, form and toast micro-interactions, page/modal/tab transitions, shared-element transitions, skeletons, progress, optimistic UI: read `references/ui-motion-patterns.md`.

For **why motion makes people feel something** — Norman's three levels, Saffer's micro-interaction anatomy, the micro-interaction catalog, sound design, brand personality and emotional vocabulary through motion, and the line between delight and annoyance: read `references/emotional-design-patterns.md`.

For **the haptic feedback system** — iOS Core Haptics, Android haptics, Apple Watch Taptic Engine, brand haptic vocabulary, haptic accessibility: read `references/haptic-feedback-design-system.md`.

## Cross-Referencing

- For copy-paste motion code built on the base scale, reference `animation-recipe-library`.
- For performance impact on mobile, reference `mobile-ux-design`.
- For accessibility requirements, reference `accessibility-inclusive-design`.
- For visual design integration, reference `visual-design-mastery`.
- For spatial and XR motion, reference `spatial-voice-ux`.

## Key Sources

- Thomas, F. & Johnston, O. "The Illusion of Life" (Disney animation principles)
- Norman, D. (2004). "Emotional Design"
- Material Design motion guidelines
- Apple Human Interface Guidelines — Motion
- Google Web Vitals animation performance guidance
