---
name: icon-illustration-systems
description: "Icon and illustration systems: grid and sizing scales, library selection (Lucide, Heroicons, Phosphor, SF Symbols, Material Symbols), illustration style guides, SVG optimization, and accessible iconography. Use when choosing an icon set, sizing icons, or establishing an illustration style."
allowed-tools: Read, Grep, Glob
---

# Icon and Illustration Systems

## Mental model

An icon is a compression of meaning, and compression only works when the reader
already has the key. Most icon failures are the designer assuming a metaphor is
universal when it is learned.

- **Universal metaphors are a short list.** Home, search, close, play, plus,
  trash, settings, back. Everything else is learned, and learned means a label.
- **If you have to debate whether an icon is self-explanatory, add a label.**
  The debate is the evidence. Icon-only navigation measurably reduces
  discoverability; icon-plus-label costs a few pixels and removes the problem.
- **Optical alignment beats mathematical alignment.** A triangle centred by
  bounding box looks off-centre. Centre by visual mass, which for a play glyph
  means nudging right.
- **One grid, one stroke weight, one corner radius.** Mixing icon sets is the
  fastest way to make an interface look assembled rather than designed.
- **Decorative icons are invisible to screen readers, meaningful ones are not.**
  That distinction is a decision you make per icon, not a default.

## Procedure

1. **Decide labels first.** For each icon, ask whether the metaphor is on the
   universal list. If not, it ships with a visible label.
2. **Pick one set.** Choose a single library by style, weight range, coverage
   and licence (see Routing). Do not mix sets in one interface.
3. **Set the size scale.** Use the tokens below, and draw or pick dedicated
   small variants for 16px and 12px instead of scaling down.
4. **Mark every icon** as meaningful or decorative and wire it as shown under
   Accessibility.
5. **Wire states and colour** through `currentColor` and the state tokens in
   `references/icon-implementation-recipes.md`.
6. **Optimize** each SVG with the SVGO config in the same file before it lands.

## Constants

Every recipe in the reference files emits these size tokens.

| Token | Size | Line Height | Use Cases | Touch Target |
|-------|------|-------------|-----------|--------------|
| `icon-xs` | 12px | 12px | Status dots, inline indicators, badge counts, color swatches | N/A (not interactive) |
| `icon-sm` | 16px | 16px | Inline with small text (12-13px), table row icons, tag icons, breadcrumb separators | 24x24px min |
| `icon-md` | 20px | 20px | Default size — nav items, buttons, form field icons, list item icons, dropdown arrows | 32x32px min |
| `icon-lg` | 24px | 24px | Prominent actions, card header icons, section markers, tab bar icons (mobile) | 44x44px min (mobile) |
| `icon-xl` | 32px | 32px | Feature icons, section headers, sidebar category icons, dialog icons | 44x44px min |
| `icon-2xl` | 40px | 40px | Hero feature icons, onboarding step icons, empty state accents | N/A (usually decorative) |
| `icon-3xl` | 48px | 48px | Large empty state illustrations, marketing feature blocks, landing page icons | N/A (usually decorative) |

### Sizing Rules
- Icons below 16px should use simplified glyphs (fewer details, thicker relative strokes)
- Icons at 12px may need to be redesigned as filled shapes rather than stroked outlines
- At 32px+, icons can support more detail (inner strokes, secondary elements)
- Never scale a 24px icon down to 12px by setting width/height — use a dedicated small variant
- Design at 24px, then create size-specific variants for 16px and 12px

## Accessibility

### Meaningful vs Decorative Icons
Every icon is either **meaningful** (conveys information) or **decorative** (visual embellishment). The treatment differs completely:

**Meaningful icons** (icon is the only way to understand the action):
```html
<!-- Method 1: aria-label on the button -->
<button aria-label="Search">
  <svg aria-hidden="true"><!-- icon --></svg>
</button>

<!-- Method 2: title element inside SVG -->
<svg role="img" aria-labelledby="search-title">
  <title id="search-title">Search</title>
  <!-- icon paths -->
</svg>

<!-- Method 3: Visually hidden text -->
<button>
  <svg aria-hidden="true"><!-- icon --></svg>
  <span class="sr-only">Search</span>
</button>
```

**Decorative icons** (icon accompanies visible text):
```html
<button>
  <svg aria-hidden="true" focusable="false"><!-- icon --></svg>
  <span>Search</span>
</button>
```

### Accessibility Rules
1. **Every icon** must have either `aria-hidden="true"` (decorative) or an accessible name (meaningful)
2. `focusable="false"` on inline SVGs only matters for legacy IE/Edge tab stops; it is harmless elsewhere
3. Use `role="img"` when the SVG is meaningful and uses `<title>` for its label
4. Toggle icons must announce their state: `aria-pressed="true/false"` or `aria-expanded`
5. Icon-only buttons need a 24x24px target at minimum (WCAG 2.5.8, AA); aim for 44x44px on touch (2.5.5, AAA)
6. Color alone must not be the only indicator — pair colored icons with shape changes (e.g., filled vs outline for selected)
7. Animated icons must respect `prefers-reduced-motion` (WCAG 2.3.3)

## Routing

For **choosing an icon set** -- style, weights, coverage, licence, import
pattern, and the SF Symbols and Material Symbols platform conventions: read
`references/icon-library-catalog.md`.

For **getting icons into the codebase** -- the React component, inline vs sprite
vs font, state transitions, animated icons, and SVG optimization: read
`references/icon-implementation-recipes.md`.

For **illustration** -- sixteen styles with the brands that use them, plus
empty-state and spot illustration practice: read
`references/illustration-systems.md`.

For **drawing icons** -- the 24x24 grid, pixel alignment, keyline shapes, safe
zones, and how icons take colour across themes: read
`references/icon-geometry-and-color.md`.

## Cross-References

- `ui-visual-design-system` -- where iconography sits in the visual language
- `platform-visual-standards` -- SF Symbols and Material Symbols in their native context
- `animation-recipe-library` -- the easing tokens animated icons use
- `accessibility-inclusive-design` -- the full decorative-vs-meaningful story
- `design-systems-architecture` -- icon size tokens in the three-tier model
