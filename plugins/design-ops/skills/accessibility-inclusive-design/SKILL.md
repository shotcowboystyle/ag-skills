---
name: accessibility-inclusive-design
description: WCAG 2.2 compliance, ARIA authoring patterns, screen reader and keyboard navigation, color contrast, and cognitive/neurodiversity accommodations. Use when auditing accessibility, fixing a11y violations, choosing ARIA roles, checking contrast ratios, or designing for ADHD, dyslexia, autism, or motor impairment.
allowed-tools: Read, Grep, Glob
---

# Accessibility & Inclusive Design

Accessibility is a design constraint from the first wireframe, not a final-pass feature. Disability spans permanent, temporary, and situational cases, so designing for it helps everyone. Target WCAG 2.2 Level AA as the compliance baseline.

## WCAG 2.2 Compliance Framework

Every criterion maps to POUR: **Perceivable** (text alternatives, captions, contrast), **Operable** (keyboard, time, no seizures, navigation, input modalities), **Understandable** (readable, predictable, error help), **Robust** (semantic HTML, programmatic name/role/value).

### WCAG Conformance Levels

- **Level A:** Minimum accessibility — baseline legal requirement.
- **Level AA:** Standard target — required by most laws (ADA, EN 301 549, EAA).
- **Level AAA:** Enhanced accessibility — aspirational, target for critical public services.

### Key WCAG 2.2 Success Criteria

**New in 2.2:**
- **2.4.11 Focus Not Obscured (Minimum):** Focused element not fully hidden by other content.
- **2.4.12 Focus Not Obscured (Enhanced):** Focused element fully visible.
- **2.4.13 Focus Appearance:** Focus indicators are sufficiently visible (size and contrast).
- **2.5.7 Dragging Movements:** Provide a single-pointer alternative for drag operations.
- **2.5.8 Target Size (Minimum):** 24×24 CSS pixels minimum for interactive elements.
- **3.2.6 Consistent Help:** Place help mechanisms in consistent locations across pages.
- **3.3.7 Redundant Entry:** Do not ask users to re-enter previously provided information.
- **3.3.8 Accessible Authentication (Minimum):** No cognitive function tests for login.
- **3.3.9 Accessible Authentication (Enhanced):** No object/image recognition for login.

## Semantic HTML Foundation

### Critical Semantic Elements

- Use `<nav>` for navigation regions, `<main>` for primary content, `<aside>` for complementary content.
- Use heading hierarchy (`<h1>`–`<h6>`) that reflects document structure — never skip levels.
- Use `<button>` for actions and `<a>` for navigation — never use `<div>` for interactive elements.
- Use `<table>` with proper `<thead>`, `<th>`, and `scope` attributes for data tables.
- Use `<form>`, `<fieldset>`, `<legend>`, and `<label>` for form structure.
- Use `<ul>`/`<ol>` for lists — screen readers announce list length and position.
- Use landmark roles implicitly through semantic HTML (preferred) or explicitly via ARIA.

### ARIA Patterns (When HTML Is Not Enough)

**Core ARIA Rules:**
1. If native HTML can achieve the behavior, use it instead of ARIA.
2. Do not change native semantics unless absolutely necessary.
3. All interactive ARIA controls must be keyboard operable.
4. Do not use `role="presentation"` or `aria-hidden="true"` on focusable elements.
5. All interactive elements must have an accessible name.

**Common ARIA Widget Patterns:**
- **Tabs:** `role="tablist"`, `role="tab"`, `role="tabpanel"` with arrow key navigation.
- **Modal dialog:** `role="dialog"`, `aria-modal="true"`, trap focus within dialog.
- **Combobox/Autocomplete:** `role="combobox"`, `aria-expanded`, `aria-activedescendant`.
- **Menu:** `role="menu"`, `role="menuitem"` with arrow key navigation.
- **Tree view:** `role="tree"`, `role="treeitem"` with expand/collapse and arrow keys.
- **Live regions:** `aria-live="polite"` for non-urgent updates, `"assertive"` for critical alerts.

## Motor and Cognitive Accommodations

### Motor Accessibility

- Touch targets: minimum 44x44pt (iOS), 48x48dp (Android), 24x24 CSS px (WCAG 2.2 minimum).
- Provide alternatives to complex gestures (drag-and-drop, multi-finger).
- Support system-level accessibility features (sticky keys, switch access, voice control).
- Avoid time-limited interactions or provide ability to extend time limits.

### Cognitive Accessibility

- Use clear, simple language at the appropriate reading level.
- Provide consistent navigation and layout across the application.
- Break complex tasks into smaller, manageable steps.
- Avoid unexpected changes in context (auto-playing media, unexpected navigation).
- Provide clear error messages with specific correction instructions.
- Support pause, stop, or hide for any auto-updating content.

## Neurodiversity Accommodations

- **Reduced motion:** Respect `prefers-reduced-motion` media query — disable animations or substitute with opacity/instant transitions.
- **High contrast:** Support `forced-colors` / `prefers-contrast: more` for users who need maximum contrast.
- **Reading preferences:** Allow font size adjustment, line spacing customization, and typeface choice where possible.
- **Attention considerations:** Minimize distracting animations, auto-playing content, and notification frequency.
- **Predictability:** Maintain consistent behavior, clear labeling, and reduced cognitive surprises to support ADHD and autism spectrum users.

## Routing

- **Conformance work** — WCAG 2.2 checklist by POUR, ARIA roles and states, widget patterns, keyboard navigation and focus indicators, screen reader content and dynamic updates, SPA focus management, skip links and landmarks, live regions, forms, image alt-text decision tree, testing tools and methodology, and the WCAG 3.0 preview: read `references/wcag-aria-patterns.md`.
- **Cognitive and neurodivergent accommodation** — the inclusive design spectrum, ADHD, autism, dyslexia, learning disabilities, anxiety, memory impairment, motor load, and the preference media queries that implement them: read `references/neurodiversity-accommodations.md`.

## Cross-Referencing

- For color contrast and visual design, reference `visual-design-mastery`.
- For mobile accessibility specifics, reference `mobile-ux-design`.
- For motion and reduced-motion handling, reference `interaction-motion-design`.
- For ethical considerations, reference `ux-ethics-content-strategy`.
- For AI feature accessibility, reference `agentic-ai-generative-ux`.
- For measuring accessibility outcomes, reference `ux-metrics-measurement`.
- Accessible React/SwiftUI component implementations: `component-patterns-code`
- Cognitive science behind cognitive accessibility: `cognitive-psychology-ux`
- RTL, CJK, and localized accessibility: `cross-cultural-i18n-ux`

## Key Sources

- W3C WCAG 2.2 Specification
- W3C WCAG 3.0 Working Draft (September 2025; superseded by the March 2026 draft -- verify current
  status at w3.org/TR/wcag-3.0/ before citing specifics)
- WAI-ARIA Authoring Practices Guide 1.2
- WebAIM articles and testing tools
- Microsoft Inclusive Design Toolkit
- NNG Group accessibility research
- Deque: WCAG 3.0 analysis (174 outcomes)
