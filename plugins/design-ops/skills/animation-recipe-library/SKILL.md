---
name: animation-recipe-library
description: "200+ copy-paste animation recipes in CSS, Framer Motion, and GSAP: entrances, micro-interactions, page transitions, scroll-driven effects, spring physics, and cursor and text effects, each with timing, easing, and a reduced-motion fallback. Use when you need working motion code rather than motion principles."
allowed-tools: Read, Grep, Glob
---

# Animation Recipe Library

## Mental model

Motion is a sentence about causality: this happened *because* that happened.
Animation that does not explain a relationship is decoration, and decoration is
the first thing that reads as amateur.

- **Duration follows distance and size.** A 200px slide is not a 20px nudge.
  150-200ms for small state changes, 250-350ms for entrances, 400-500ms for
  anything crossing the viewport. Over 500ms and the interface feels slow no
  matter how pretty the curve.
- **Ease out for entrances, ease in for exits.** Things arriving decelerate;
  things leaving accelerate away. Linear is for progress bars and nothing else.
- **Animate transform and opacity.** They are composited. Width, height, top,
  left and box-shadow are painted, and animating them drops frames on the
  devices least able to afford it.
- **Reduced motion is not optional.** WCAG 2.1 SC 2.3.3, and a vestibular
  trigger for real people. Every recipe here ships a fallback.

Spring physics beats a bezier when the motion should feel physical -- drags,
sheets, anything the user is directly manipulating. Bezier beats spring when
timing must be predictable.

## Constants

Every recipe in every reference file writes against these. Without them in
context the references are unusable. They are the base motion scale owned by
`interaction-motion-design` (`animation-timing-curves.md`); same
names, same values. The extended curve catalog is in
`references/easing-and-spring-catalog.md`.

```css
:root {
  /* === Base easings === */
  --ease-out:    cubic-bezier(0.16, 1, 0.3, 1);          /* Decelerate — entrances */
  --ease-in:     cubic-bezier(0.55, 0.055, 0.675, 0.19); /* Accelerate — exits */
  --ease-in-out: cubic-bezier(0.87, 0, 0.13, 1);         /* Symmetric — movement */
  --ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1);      /* Single overshoot ≈ spring-default */

  /* === Base durations === */
  --duration-instant: 50ms;  --duration-fast: 150ms;     --duration-normal: 250ms;
  --duration-moderate: 300ms; --duration-slow: 400ms;    --duration-slower: 600ms;

  /* === CSS approximations of the named spring presets === */
  --spring-snappy: cubic-bezier(0.25, 1.5, 0.5, 1);       /* ≈ spring-snappy 400/30 */
  --spring-gentle: cubic-bezier(0.34, 1.3, 0.64, 1);      /* ≈ spring-gentle 200/25 */
  --spring-bouncy: cubic-bezier(0.68, -0.55, 0.27, 1.55); /* ≈ spring-bouncy 300/10 */
}
```

### Framer Motion Spring Presets

```tsx
// Snappy — toggles, switches, presses, small controls
const springSnappy  = { type: "spring", stiffness: 400, damping: 30, mass: 1 };

// Default — general UI, panels, drag release, modals
const springDefault = { type: "spring", stiffness: 300, damping: 25, mass: 1 };

// Gentle — large surfaces, sheets, shared-element and layout morphs
const springGentle  = { type: "spring", stiffness: 200, damping: 25, mass: 1 };

// Bouncy — celebrations, likes, playful confirmations
const springBouncy  = { type: "spring", stiffness: 300, damping: 10, mass: 1 };
```

### When to Use Each Easing

| Easing | Use For | Avoid For |
|--------|---------|-----------|
| ease-out | Entrances, appearing elements | Exits, disappearing elements |
| ease-in | Exits, disappearing elements | Entrances (feels sluggish) |
| ease-in-out | Position changes, slides between states | Quick micro-interactions |
| ease-spring | Playful entrances, bouncing buttons | Serious/enterprise UI |
| spring (gentle) | Modals, sheets, overlays | Rapid repeated actions |
| spring (snappy) | Toggles, switches, small controls | Large page transitions |
| spring (bouncy) | Notifications, celebrations | Data-heavy interfaces |
| linear | Progress bars, continuous rotation only | Everything else |

---

The reduced-motion floor, which every recipe assumes is already in the sheet:

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

## What every reference file contains

1. The recipe name and what it is for in one line
2. Complete, runnable CSS or JSX -- no placeholders
3. Exact duration and easing, using the tokens above
4. The reduced-motion fallback for that specific recipe
5. What it costs: composited, painted, or layout-triggering
6. When to reach for a different recipe instead

## Performance

Composited properties are `transform`, `opacity`, and `filter`. Everything else
repaints. `will-change` is a promise you pay for whether or not you keep it --
set it immediately before the animation and remove it after, never in a
stylesheet at rest. Sixty frames per second is 16.7ms per frame including
everything else on the page.

## Routing

For **CSS entrances, exits and loading states**: read
`references/css-animation-recipes.md`.

For **the small responses that make an interface feel alive** -- presses,
toggles, hovers, focus, drag affordances: read
`references/micro-interaction-recipes.md`.

For **moving between screens** -- route changes, shared-element morphs, list
reordering: read `references/page-transition-recipes.md`.

For **scroll and touch** -- reveal, parallax, sticky progress, swipe, drag,
pull-to-refresh: read `references/scroll-gesture-recipes.md`.

For **Framer Motion** -- variants, the layout prop, stagger and orchestration:
read `references/framer-motion-recipes.md`.

For **GSAP** -- pin and scrub, horizontal scroll, SplitText, Lenis smooth
scroll: read `references/gsap-scrolltrigger-recipes.md`.

For **the showy stuff** -- custom cursors, magnetic buttons, text effects,
React Three Fiber, particles: read `references/cursor-text-3d-effects.md`.

For **anything with more than two visual states**: read
`references/animation-state-machines.md`.

For **extended easing curves** (quad/cubic/quart/circ/back variants,
elastic, emphasis, platform approximations) and extra springs: read
`references/easing-and-spring-catalog.md`.

For **why a motion should exist at all** -- Disney's twelve principles
translated into interface terms: read `references/motion-principles.md`.

## Cross-References

- `interaction-motion-design` -- the principles behind these recipes; read that
  when deciding *whether* to animate, this when deciding *how*
- `performance-states-patterns` -- loading and skeleton states as UX, not motion
- `accessibility-inclusive-design` -- the full reduced-motion and vestibular story
- `shadow-elevation-density` -- animating elevation specifically
- `platform-visual-standards` -- native iOS / Material 3 Expressive springs
