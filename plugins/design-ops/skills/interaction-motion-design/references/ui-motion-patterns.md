# UI Motion Patterns — Micro-Interactions, Transitions, Loading

Durations and curves below map to the base scale in `animation-timing-curves.md` (ease-out = `--ease-out`, ease-in = `--ease-in`, ease-in-out = `--ease-in-out`).

## Micro-Interaction Patterns

### Button Interactions

- **Press:** Apply slight scale down (0.97-0.98) plus subtle darkening on press — immediate, under 100ms.
- **Release:** Spring back to 1.0 scale — 150-200ms with ease-out.
- **Loading:** Replace label with inline spinner, maintain button dimensions — prevent layout shift.
- **Success:** Apply brief color transition to success state (green) plus checkmark icon swap — 300ms.
- **Disabled:** Reduce opacity (0.5-0.6), remove hover effects, change cursor.

### Toggle and Switch

- Thumb translation: 200ms ease-in-out.
- Track color transition: 150ms.
- Add slight bounce (overshoot spring) for personality.
- Trigger haptic feedback on state change (mobile).

### Form Interactions

- **Focus:** Transition input border color — 150ms.
- **Validation success:** Apply subtle green border plus checkmark icon fade-in — 200ms.
- **Validation error:** Apply red border plus shake animation (2-3px horizontal, 300ms) plus error text slide-down.
- **Character counter:** Transition color as limit approaches (neutral to warning to error).

### Notification and Toast

- **Enter:** Slide in from edge plus fade — 300ms ease-out.
- **Persist:** 3-5 seconds for success, persistent for errors.
- **Exit:** Fade out plus slight vertical slide — 200ms ease-in.
- **Stack:** Push existing notifications when new ones arrive, with 200ms stagger.

## Transition Design

### Page and View Transitions

**Forward navigation (deeper in hierarchy):**

- Slide new view in from right (LTR) — 300ms ease-out.
- Slide previous view left and slightly scale down (0.95) — 300ms ease-out.
- Maintain visual continuity for shared elements (hero transitions).

**Backward navigation (up in hierarchy):**

- Reverse the forward animation — slide previous view in from left.
- Match gesture velocity for swipe-back (iOS-style).

**Modal/Dialog:**

- Backdrop: fade in black overlay (opacity 0.5) — 200ms.
- Dialog: scale from 0.95 to 1.0 plus fade in — 250ms ease-out.
- Dismiss: reverse with ease-in — 200ms.
- Trap focus on open, restore focus on close.

**Tab/Segment Change:**

- Content crossfade: 150-200ms.
- Slide active indicator to new position — 250ms ease-in-out.
- Avoid sliding content left/right for tabs (it implies hierarchy, not peers).

### Shared Element Transitions (View Transitions API)

```css
/* Modern approach using View Transitions API */
::view-transition-old(hero) {
  animation: fade-out 250ms ease-in;
}
::view-transition-new(hero) {
  animation: fade-in 250ms ease-out;
}
```

- Maintain visual continuity when elements persist across views.
- Anchor transitions to the shared element — the eye follows it naturally.
- Use the View Transitions API for declarative cross-view animation.

## Loading State Choreography

### Skeleton Screens (Preferred)

- Show content structure with animated placeholder shapes before data loads.
- Pulse animation: opacity 0.3 to 0.7 — 1.5s ease-in-out infinite.
- Match skeleton shapes to actual content dimensions.
- Stagger skeleton appearance slightly (50ms between groups) for natural feel.

### Progress Indicators

- **Determinate:** Use when progress percentage is known — smooth bar fill.
- **Indeterminate:** Use when duration is unknown — continuous animation loop.
- **Combined:** Start indeterminate, switch to determinate when progress data arrives.
- Position at the top of the content area being loaded.

### Optimistic UI

- Show the expected result immediately upon user action.
- If the action fails, smoothly revert with clear error notification.
- This eliminates perceived loading time for common operations (like, save, send).
