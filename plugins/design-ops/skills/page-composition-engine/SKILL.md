---
name: page-composition-engine
description: Full-page recipes giving exact block order, spacing rhythm, visual pacing, and content hierarchy for landing pages, dashboards, e-commerce, auth, settings, and profiles. Use when composing a whole page. For a single section in isolation, use layout-block-intelligence.
allowed-tools: Read, Grep, Glob
---

# Page Composition Engine

## The Art of Page Composition

A page is not a collection of random sections — it's a narrative. Every page tells a story through the deliberate sequencing of layout blocks. The composition engine provides complete recipes: which blocks to use, in what order, with what spacing rhythm, to achieve a specific goal.

"Every page is a conversation. The hero opens with a promise. The features deliver evidence. The testimonials provide social validation. The CTA asks for commitment." — This is not decoration; it's persuasion architecture.

## Page Archetypes

### Marketing Pages (External-Facing)
Pages designed to attract, inform, and convert visitors.
- Landing pages, product pages, pricing pages, about pages, case study pages

### Product Pages (Internal App)
Pages within the authenticated product experience.
- Dashboards, settings, profiles, lists, detail pages, create/edit pages

### Transactional Pages (Flow Steps)
Pages that are part of a multi-step process.
- Auth pages, checkout, onboarding, wizards

### Content Pages (Information)
Pages primarily delivering content.
- Blog posts, documentation, help center, changelog

## Procedure

1. **Name the archetype** (marketing, product, transactional, content) and the
   one action the page exists to get.
2. **Start from the nearest recipe** in the references (see Routing). For a
   login, signup or onboarding page, use the auth recipes below.
3. **Order blocks along the narrative arc** below; drop any stage the page does
   not need rather than padding it.
4. **Specify each block** from `layout-block-intelligence`, which holds the
   variants, anatomy and code for every block type a recipe names.
5. **Set rhythm**: alternate dense and light blocks and backgrounds, and apply
   the spacing scale.
6. **Check the first viewport** for what, why, how and trust, then apply the
   responsive rules.

## Composition Theory

### The Block Stacking Model

Every page follows a **narrative arc** through its blocks:

```
┌─────────────────────────┐
│   HOOK                  │  ← Hero: Capture attention
├─────────────────────────┤
│   CREDIBILITY           │  ← Logos/Social proof: Establish trust
├─────────────────────────┤
│   VALUE                 │  ← Features: Explain the offering
├─────────────────────────┤
│   EVIDENCE              │  ← Testimonials/Case studies: Prove it
├─────────────────────────┤
│   CONVERSION            │  ← Pricing/CTA: Ask for action
├─────────────────────────┤
│   OBJECTION HANDLING    │  ← FAQ: Remove doubts
├─────────────────────────┤
│   CLOSE                 │  ← Footer: Navigation + trust
└─────────────────────────┘
```

### Visual Rhythm

**Alternating density** prevents scroll fatigue:
- Dense block (feature grid) → Light block (CTA banner) → Dense block (testimonials) → Light block (stats)

**Background alternation** creates section separation:
- White → Gray-50 → White → Primary-950 (dark CTA) → White → Gray-50

### Spacing Between Blocks

| Context | Desktop | Mobile |
|---------|---------|--------|
| Default between blocks | 96-120px | 48-64px |
| Tight (related blocks) | 48-64px | 32-40px |
| Breathing room (after dense block) | 120-160px | 64-80px |
| Zero (blocks that visually connect) | 0px | 0px |

### Above-the-Fold Strategy

The first viewport (above the fold) must accomplish:
1. **What** — Clear heading explaining the product
2. **Why** — Subheading with the key benefit
3. **How** — Primary CTA button
4. **Trust** — Social proof element (logos, rating, user count)

Most visitors do scroll, but only if the first viewport gives them a reason to.

### Content-to-Chrome Ratio

- Marketing pages: 90% content, 10% chrome (nav + footer)
- App pages: 75-85% content, 15-25% chrome (nav + sidebar + toolbars)
- Dashboards: 70-80% content, 20-30% chrome

## Auth Page Recipes

### AUTH-01: Login Page
```
1. Two-column layout:
   Left: Brand panel (logo + tagline + illustration)
   Right: Login form (email + password + social login + forgot password link)
```

### AUTH-02: Signup Page
```
1. Two-column layout:
   Left: Brand panel (logo + value props + social proof)
   Right: Signup form (name + email + password + terms checkbox)
```

### AUTH-03: Onboarding Flow (3-step)
```
Step 1: Profile setup (avatar + name + role)
Step 2: Preferences (team size + use case + integrations)
Step 3: Workspace setup (invite team + import data)
Each step: progress indicator + back/next buttons
```

## Responsive Composition Rules

### Desktop → Tablet
- 3-column grids → 2-column grids
- Sidebar nav → collapsible sidebar or top nav
- Side-by-side sections → stacked
- Section padding: reduce by 25%

### Tablet → Mobile
- 2-column grids → single column
- Horizontal nav → hamburger menu
- Side images → stacked above text
- Pricing tables → horizontal scroll or accordion
- Section padding: reduce by 50% from desktop
- Font sizes: reduce by 1-2 scale steps

### Block Reordering on Mobile
Some blocks reorder on mobile for thumb-reach and visual hierarchy:
- CTA button moves from inline to sticky bottom bar
- Social proof moves closer to hero (trust first)
- Navigation images/illustrations hide (content first)

## Routing

For **marketing pages** — seven complete recipes (SaaS landing, mobile app
landing, startup launch, enterprise B2B, e-commerce product, agency portfolio,
event) each with block order and rationale: read
`references/marketing-page-recipes.md`.

For **product pages** — nine recipes (dashboard home, settings, profile,
list/feed, detail, editor/canvas, chat, calendar, analytics): read
`references/app-page-recipes.md`.

For **the spacing that holds a page together** — the section spacing scale,
stacking rhythm rules, visual rhythm patterns, the responsive reduction formula,
container width strategy, grid systems, Z- and F-pattern layouts, and the rhythm
diagnostics for when a page feels wrong but you cannot say why: read
`references/spacing-rhythm-system.md`.

## Cross-References

- **layout-block-intelligence** — Individual block specs and variants
- **responsive-block-patterns** — Detailed breakpoint transformations
- **conversion-optimization-patterns** — Which compositions convert best
- **screen-flow-patterns** — Screen types that use these compositions
- **sector-style-intelligence** — Industry-specific page templates
