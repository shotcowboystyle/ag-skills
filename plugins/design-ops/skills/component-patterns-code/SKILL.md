---
name: component-patterns-code
description: Production UI component code in React/TypeScript, Vue 3, Svelte 5, SwiftUI and modern CSS, with full state matrices, ARIA, keyboard handling and design tokens. Use when building or reviewing a component, designing a component API or composition pattern, or choosing a styling approach such as Tailwind, CSS Modules or CSS-in-JS.
allowed-tools: Read, Grep, Glob
---

# Component Patterns & Code

A component is a state machine with a visual output. Ship it only when every
state looks right, every interaction works by pointer, touch and keyboard, and
assistive technology can read its purpose and state.

## Component State Matrix Methodology

Before writing code, enumerate every visual and behavioral state the component can occupy.

### The Universal State Set

1. **Default** — the resting state, no user interaction, content loaded normally
2. **Hover** — pointer device is over the component, visual feedback indicates interactivity
3. **Focus** — the component has keyboard focus, visible focus ring is mandatory (WCAG 2.4.7)
4. **Active/Pressed** — the component is being activated (mousedown, touch start)
5. **Disabled** — the component is non-interactive, visually muted, removed from tab order
6. **Loading** — the component or its content is being fetched, skeleton or spinner is shown
7. **Error** — something went wrong, the error is communicated visually and to screen readers
8. **Success** — an operation completed successfully, confirmation feedback is shown
9. **Skeleton** — content has not yet loaded, a placeholder shape indicates the forthcoming layout
10. **Empty** — no data to display, guidance or action is offered to the user
11. **Read-only** — content is visible but not editable, visually distinct from disabled
12. **Selected** — the component is chosen within a selection group (checkbox checked, row highlighted)
13. **Dragging** — the component is being repositioned, visual affordance communicates movability
14. **Overflow** — content exceeds bounds, truncation or scroll behavior activates

### Compound States

States combine (focused + error, loading + disabled, selected + hovered). Model each dimension independently instead of a union of every combination:

- **Interaction state:** default, hover, focus, active (mutually exclusive for pointer, but focus persists alongside hover)
- **Validation state:** none, error, warning, success (one at a time)
- **Content state:** loaded, loading, skeleton, empty, error (one at a time)
- **Selection state:** selected, unselected
- **Availability state:** enabled, disabled, read-only

### State Matrix Audit Checklist

Before any component ships:

- Are all 14 universal states accounted for in design and code?
- Do compound states resolve without visual conflicts?
- Is every state transition animated appropriately (not jarring, not distracting)?
- Does every state have a screen reader equivalent (aria-busy, aria-invalid, aria-disabled, aria-selected)?
- Has every state been tested on mobile (touch) and desktop (pointer + keyboard)?

## Core Rules

- **Tokens, not raw values.** Never hardcode hex colors, pixel values or font stacks. Component tokens alias global tokens (`--button-bg: var(--color-primary)`), state variants reference the token system (`--button-bg-hover: var(--color-primary-hover)`), and dark mode is a token swap, not a component rewrite.
- **Semantic HTML first, ARIA second.** Use `<button>`, `<input>`, `<dialog>`, `<nav>`; follow the WAI-ARIA Authoring Practices keyboard pattern for custom widgets (arrows in menus/tabs/radios, Enter/Space to activate, Escape to dismiss); trap focus only in modals; focus indicator at 3:1 contrast.
- **Announce state changes.** Update `aria-expanded`/`-selected`/`-checked`/`-busy`/`-invalid`; link errors with `aria-describedby`; toasts use `role="status"`; icon-only buttons need `aria-label`.
- **Container queries over media queries** for reusable components, `clamp()` for fluid type and spacing, and touch targets of at least 24x24 CSS px (WCAG 2.5.8 AA), 44pt on iOS, 48dp on Android.
- **API shape.** Semantic prop names, sensible defaults, composition via `children`/slots instead of prop explosion, `className` override, support controlled and uncontrolled use, forward refs.
- **Styling approach.** Prefer zero-runtime styling (Tailwind + CVA, CSS Modules, Vanilla Extract); runtime CSS-in-JS does not work in React Server Components.

## Routing

| Question | Read |
| --- | --- |
| React component code (Button, TextInput, Select, Dialog, Toast, Card, DataTable, Form...) with CVA + Tailwind + Radix, every state and ARIA | `references/react-component-cookbook.md` |
| Component API design, compound components, render props, polymorphic `as`, controlled/uncontrolled, slots, imperative refs | `references/component-api-and-composition.md` |
| Vue 3 (slots, provide/inject composables) or Svelte 5 (runes, snippets) | `references/vue-svelte-patterns.md` |
| Choosing or using Tailwind, CSS Modules, styled-components, Emotion, Vanilla Extract; SSR style extraction | `references/css-styling-approaches.md` |
| Library-free modal, dropdown, combobox, form field, skip links, live regions, focus-trap hooks | `references/accessibility-patterns.md` |
| SwiftUI theme system and components (PrimaryButton, ValidatedTextField, AdaptiveSheet...), haptics | `references/swiftui-component-cookbook.md` |
| Modern CSS: container queries, `:has()`, anchor positioning, `@starting-style`, view transitions, subgrid, `@layer`, popover | `references/css-modern-patterns.md` |
| Component taxonomy (action, input, feedback, navigation, content, data), token categories, full keyboard/ARIA/responsive baselines | `references/component-taxonomy-and-baselines.md` |

## Cross-References

- **Cognitive psychology foundations** — `cognitive-psychology-ux` covers Fitts's Law (touch target sizing), Hick's Law (choice overload in selects and menus), Miller's Law (chunking in tables and forms), and gestalt grouping.
- **Accessibility compliance** — `accessibility-inclusive-design` provides the full WCAG 2.2 checklist, ARIA widget specs and assistive technology testing.
- **Design token architecture** — `visual-design-mastery` details token naming, scale generation and semantic mapping that components consume.
- **Animation and interaction** — `interaction-motion-design` covers easing curves, duration scales, reduced-motion handling and spring physics.
- **Design-to-code workflow** — `figma-design-tool-workflows` maps Figma auto-layout to flexbox, variants to props, and token export.
- **System governance** — `design-systems-architecture` explains how components are documented, versioned, tested and distributed.

## Key Sources

- WAI-ARIA Authoring Practices 1.2 — W3C component keyboard and ARIA patterns
- Inclusive Components — Heydon Pickering (component accessibility patterns)
- Material Design 3 Component Guidelines — Google
- Apple Human Interface Guidelines — Components
- React Aria (Adobe) — accessible React component primitives
- Radix UI — unstyled, accessible component primitives
- Open UI — web platform component standards research
