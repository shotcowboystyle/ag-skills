---
name: visual-design-mastery
description: "Designer-grade visual craft: type scales, color science (OKLCH, HCT), spacing systems, grids, visual hierarchy, elevation, iconography, 70 canonical rules and 10-dimension scoring. Use when setting type and color, building spacing or hierarchy, scoring visual quality, or when work looks cheap but you cannot say why."
allowed-tools: Read, Grep, Glob
---

# Visual Design Mastery

Visual craft is a finite set of learnable rules: typographic hierarchy, color harmony, spatial
rhythm, compositional balance and detail polish. This skill owns those rules and the single
visual scoring rubric. Load the reference that matches the question; don't answer from memory
when a reference has the exact values.

## Principles

- **Form follows function.** Every visual choice serves a purpose. If removing an element breaks nothing, remove it.
- **Less, but better.** Fewer colors, fewer typefaces, fewer competing elements. Senior designers subtract.
- **Attention is currency.** One focal point per screen, at most three levels of importance. If everything is bold, nothing is.
- **The interface should disappear.** Perfect type reads effortlessly, harmonious color feels calm, rhythmic spacing scans naturally.

## Core rules (apply on every load)

**Type**
- Two typeface families maximum; one family at several weights is often enough. Pair by contrast of classification, not similarity.
- Use a modular scale (1.125 dense UI, 1.2–1.25 product UI, 1.333+ marketing/editorial). Name steps semantically (display, heading, title, body, label, caption). Limit the app to 6–8 distinct text styles.
- Body 16–18px (never below 12px); line-height 1.4–1.6 body, 1.05–1.3 headings; measure 45–75ch.
- Tighten tracking on large type (-0.01 to -0.03em), loosen small caps/labels (+0.01 to +0.05em). Fluid sizes via `clamp()`, never raw `vw`.

**Color**
- Build palettes in OKLCH (or HCT for Material); one hero brand color, tinted neutrals, semantic colors (red error, green success, amber warning, blue info).
- 60-30-10 distribution; chromatic color on 10–20% of surface area.
- Contrast: WCAG 2.2 AA (4.5:1 text, 3:1 large text and UI), check critical text with APCA. Never use color as the only signal.
- Semantic tokens (`--color-text-secondary`), not value names (`--gray-500`). Dark mode is a parallel system: no pure black/white, lower chroma, elevation by lighter surfaces.

**Space and layout**
- 8px base unit with a 4px sub-grid; a fixed spacing scale (4, 8, 12, 16, 24, 32, 48, 64, 96, 128). No arbitrary values.
- Proximity communicates relationship: tight within groups, loose between groups. All whitespace is intentional.
- Align everything to something; establish a grid, then break it once, deliberately, for emphasis.
- Layouts reflow at breakpoints, they don't shrink.

**Hierarchy and depth**
- Hierarchy levers in order: size, weight, color/contrast, position, isolation, depth, motion. Verify with squint, blur and grayscale tests.
- One elevation scale, used consistently: persistent UI low, transient UI high. Tinted shadows; in dark mode, lighter surfaces instead.

**Detail**
- One radius system (max two values), one icon style (stroke, fill, grid, corner) across the product.
- Every interactive element has default, hover, active, focus, disabled and loading states. Touch targets ≥ 44×44pt / 48×48dp.
- Optical alignment beats mathematical alignment (play icons, all-caps sizing, round vs flat shapes).

## Scoring

Design Ops has one scoring rubric: `references/visual-scoring-framework.md`. It defines 10
dimensions (Typography, Color, Spacing, Composition, Imagery, Iconography, Motion, Polish,
Coherence, Craft), their weights, per-score descriptors and the weighted formula. `/grade`
and the critic agent both use it, and DQS is its weighted total × 10. Don't score against
any other dimension list.

## Routing

| Question | Read |
|---|---|
| Type classification, variable fonts, scales, pairing, line-height, rendering, i18n type, OpenType, vertical rhythm | `references/typography-mastery.md` |
| Color spaces (OKLCH, HCT, P3), palette generation, APCA/WCAG, dark mode, dynamic color, semantic tokens, data-viz and cultural color, `color-mix()` and relative color | `references/color-mastery.md` |
| Grids, 8px baseline, golden ratio, visual weight, whitespace, density, responsive patterns, hierarchy, scanning, asymmetry, bento and broken grids | `references/composition-mastery.md` |
| Pixel and optical alignment, subpixel rendering, baseline elevation scale, icon rules | `references/craft-details.md` |
| The 70 canonical rules with sources, violations and fixes (plus a one-line digest) | `references/canonical-design-rules.md` |
| Designer and team style DNA, "make it feel like X", 2025–2026 visual trends | `references/designer-pattern-library.md` |
| Scoring visual quality, award calibration | `references/visual-scoring-framework.md` |

## Cross-references

- Pattern-level analysis: `ui-pattern-intelligence`
- Sector visual norms: `sector-style-intelligence`
- Token architecture and multi-brand theming: `design-systems-architecture`
- Component code and modern CSS (container queries, `:has()`, subgrid, `@layer`): `component-patterns-code` (its `css-modern-patterns.md` reference)
- Figma variables and token export: `figma-design-tool-workflows`
- Perception science: `cognitive-psychology-ux`
- Motion: `interaction-motion-design`
- Accessibility: `accessibility-inclusive-design`
- Ready-made palettes: `color-palette-library`
- Tested font pairings: `typography-pairing-recipes`
- Full shadow and elevation systems: `shadow-elevation-density`
- Icon and illustration systems: `icon-illustration-systems`
- Platform materials (iOS 26 Liquid Glass, Material 3 Expressive): `platform-visual-standards`

## Commands that use this skill

`/grade` (visual scoring and design direction), `/roast` (rules and dimensions in critique),
`/style` (designer DNA for direction and inspiration), `/tokens` (color and type values),
`/component` (composition quality), `/qa` (detail checks).
