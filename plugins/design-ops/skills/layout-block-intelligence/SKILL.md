---
name: layout-block-intelligence
description: ~300 individual section patterns — heroes, feature grids, pricing tables, testimonials, CTAs, footers, FAQs, stats, timelines — each with specs, spacing, and code. Use when choosing or building one section. For ordering sections into a whole page, use page-composition-engine.
allowed-tools: Read, Grep, Glob
---

# Layout Block Intelligence — ~300 Production Section Patterns

## Mental model

A page is a sequence of blocks, and each block has exactly one job. When a page
feels wrong it is usually not the styling — it is two blocks doing the same job,
or a block doing none.

- **One block, one argument.** A hero makes a claim. Social proof supports it. A
  feature grid explains it. Pricing converts it. If you cannot name a block's
  argument, delete it.
- **Alternate density.** Dense, then open, then dense. Uniform density reads as
  a wall regardless of how good the individual blocks are.
- **Every block needs a mobile form**, and it is rarely "the same but narrower".
  A four-column feature grid becomes a two-by-two, not a four-high stack.
- **Spacing carries the grouping.** Space *between* blocks must exceed space
  *within* them, or the eye cannot find the seams.

For ordering blocks into a whole page, that is `page-composition-engine`. This
skill is the blocks themselves: marketing and content page sections.

## Index

| Block | Variants | Reference |
|---|---|---|
| Hero | centered, split, full-bleed, video, gradient | `hero-section-patterns.md` |
| Feature grid | 3-col, 4-col, alternating, icon-led | `content-section-patterns.md` |
| Content section | prose, media-left, media-right, stat row | `content-section-patterns.md` |
| CTA banner | simple, email capture, split, full-bleed | `cta-pricing-patterns.md` |
| Pricing table | 2-tier, 3-tier, comparison matrix, toggle | `cta-pricing-patterns.md` |
| Testimonials | card grid, carousel, single quote, video | `social-proof-patterns.md` |
| Logo wall, ratings, review display | — | `social-proof-patterns.md` |
| Top nav as a page block | standard, mega, transparent-over-hero | `navigation-footer-patterns.md` |
| Footer | minimal, sitemap, newsletter, mega | `navigation-footer-patterns.md` |

## Reference architecture

| File | Covers | Lines |
|---|---|---|
| `references/hero-section-patterns.md` | hero anatomy, breakpoints, variants | 926 |
| `references/content-section-patterns.md` | feature and content blocks | 810 |
| `references/navigation-footer-patterns.md` | nav and footer blocks | 638 |
| `references/cta-pricing-patterns.md` | conversion blocks | 635 |
| `references/social-proof-patterns.md` | testimonials, logos, ratings | 616 |

## What every reference file contains

1. The block's job in one sentence
2. Universal anatomy — the parts every variant shares
3. Breakpoint specifications, not just a mobile note
4. Each variant with the condition that selects it
5. Production HTML/CSS or TSX
6. The anti-pattern that variant invites

## Routing

For **heroes** — anatomy, breakpoint specs, and variants from centered and split
to full-bleed: read `references/hero-section-patterns.md`.

For **content sections** — universal block specs plus the 3-column, 4-column and
alternating feature-grid variants: read `references/content-section-patterns.md`.

For **conversion blocks** — CTA banners, email-capture CTAs, and pricing tables
with the psychology behind each: read `references/cta-pricing-patterns.md`.

For **social proof** — testimonial grids and carousels, logo walls, and review
displays: read `references/social-proof-patterns.md`.

For **navigation and footers** as page blocks — standard top nav, mega menu,
transparent-over-hero, and footer variants: read
`references/navigation-footer-patterns.md`.

Dashboards (shells, KPI cards, charts, data tables) are not page sections:
use `data-visualization-mastery`. App blocks such as kanban boards, calendars
and activity feeds belong to `ui-pattern-intelligence`.

## Cross-References

- **component-patterns-code** — Individual component implementation (buttons, inputs, modals, cards)
- **screen-flow-patterns** — Full page types and navigation flows between pages
- **ui-pattern-intelligence** — 190+ UI interaction patterns with benchmarks
- **visual-design-mastery** — Color, typography, and composition scoring
- **platform-visual-standards** — Platform-specific adaptations (iOS 26, Material 3, CSS)
- **performance-states-patterns** — Loading, error, skeleton states for every block
- **accessibility-inclusive-design** — WCAG requirements per block type
- **sector-style-intelligence** — Industry-specific block styling and sequencing
- **interaction-motion-design** — Animation and transition patterns for blocks
- **page-composition-engine** — How to stack blocks into complete pages
- **responsive-block-patterns** — Detailed breakpoint transformations for every block
- **conversion-optimization-patterns** — Which blocks convert best and where to place them

---

## Production Code Patterns

Section wrapper, section header and the CSS custom properties: read `references/section-scaffolding.md`.

## Block Quality Checklist

- [ ] Content flexibility: handles short AND long content without breaking?
- [ ] Responsive at 5 breakpoints (1440, 1024, 768, 480, 320)?
- [ ] Empty state: what renders with 0 items?
- [ ] Overflow state: what happens with 50+ items?
- [ ] Heading hierarchy: H2 section, H3 items, no skipping?
- [ ] ARIA landmarks: section + aria-labelledby?
- [ ] Keyboard navigation: all elements reachable?
- [ ] Images lazy-loaded below fold?
- [ ] prefers-reduced-motion respected?
- [ ] Consistent spacing, no magic numbers?
- [ ] Type scale followed, no orphaned heading words?
- [ ] Color contrast WCAG AA (4.5:1 text, 3:1 UI)?
- [ ] Visible focus indicators on interactive elements?
- [ ] Skeleton loading state for async content?
- [ ] Print styles render reasonably?
- [ ] RTL language support considered?
