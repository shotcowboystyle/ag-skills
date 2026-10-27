---
name: ui-pattern-intelligence
description: 190+ UI patterns across 10 categories, benchmark DNA from 25+ world-class products, sector pattern matrices, a matcher for code and screenshots, and a 43-entry anti-pattern encyclopedia. Use when detecting AI slop, judging whether a pattern is standard, or matching how a known product feels.
allowed-tools: Read, Grep, Glob
---

# UI Pattern Intelligence

## Mental model

Most interface problems are solved problems. The skill is recognising which
solved problem you have, and noticing when what you have built is a known
mistake wearing a new coat of paint.

- **Convention is a budget.** Jakob's Law says people spend most of their time
  on other products. Every deviation from convention spends some of the goodwill
  you need for the deviation that actually matters. Spend it once, deliberately.
- **AI-generated UI has a signature.** Purple-to-blue gradients, uniform 8px
  radius on everything, a single font weight, no hover states, no empty states,
  perfectly even spacing with no hierarchy. Recognising the signature is faster
  than evaluating the design.
- **An anti-pattern is a pattern that tested well once.** Carousels, hamburger
  menus on desktop, and infinite scroll on a shopping grid all had a reason.
  Know the reason before you deploy the fix.
- **Match the paradigm, not the pixels.** Copying Linear's colours gets you
  nothing. Copying its commitment to sub-50ms response gets you Linear.

## Index

| Need                                                 | Reference                        |
| ---------------------------------------------------- | -------------------------------- |
| Find a pattern by category                           | `pattern-quick-lookup.md`        |
| Choose between candidate patterns                    | `pattern-decision-engine.md`     |
| The full taxonomy, 190+ patterns                     | `pattern-taxonomy-complete.md`   |
| Detect AI slop in code or a screenshot               | `anti-pattern-encyclopedia.md`   |
| 43 anti-patterns with the fix                         | `anti-pattern-encyclopedia.md`   |
| Match how Linear, Stripe, Notion feel                | `world-class-pattern-dna.md`     |
| What is arriving: AI-native, spatial, voice, ambient | `emerging-patterns-2025-2026.md` |
| What died recently and why                           | `pattern-evolution-2024-2026.md` |
| Score an existing UI against known patterns          | `pattern-matching-engine.md`     |
| Which patterns a sector expects                      | `sector-pattern-matrix.md`       |
| Benchmark DNA by product tier                        | `designer-benchmark-dna.md`      |

`references/pattern-quick-lookup.md` (~2,500 lines) is the largest file in the plugin. Read a section, not
the file.

## What every reference file contains

1. The pattern's name, and the other names it goes by
2. When it applies and the condition that rules it out
3. What a correct implementation includes
4. The failure mode, and the anti-pattern it degrades into
5. Products that do it well, named

## Routing

For **finding a pattern fast** — the complete indexed lookup across navigation,
content display, data entry, feedback and social patterns: read
`references/pattern-quick-lookup.md`.

For **choosing between candidates** — decision trees for lists, navigation
systems, and the other recurring "which of these five" questions: read
`references/pattern-decision-engine.md`.

For **matching a product's feel** — Linear, Stripe, Notion and the rest
deconstructed into the paradigm each is built on: read
`references/world-class-pattern-dna.md`.

For **what is arriving** — AI-native, spatial/AR, voice and multimodal,
collaborative and ambient patterns: read `references/emerging-patterns-2025-2026.md`.

For **the full taxonomy and the anti-patterns**: read
`references/pattern-taxonomy-complete.md` and
`references/anti-pattern-encyclopedia.md`.

For **auditing an existing interface** — the three-stage identify, benchmark and
sector-fit process that turns a screenshot or a codebase into scored findings:
read `references/pattern-matching-engine.md`, with
`references/sector-pattern-matrix.md` for what the sector expects and
`references/designer-benchmark-dna.md` for the tier the product is aiming at.

## Cross-References

- **`sector-style-intelligence`** — Provides visual direction (colors, typography, tone) per sector. This skill provides pattern direction per sector. Together they define what a product in sector X should look like AND how it should work.
- **`screen-flow-patterns`** — Provides screen type and flow catalogs. This skill provides the broader pattern taxonomy that screen types are composed of.
- **`component-patterns-code`** — Provides React, SwiftUI, and CSS code for individual components. This skill identifies which components are needed; component-patterns-code provides the implementation.
- **`cognitive-psychology-ux`** — Provides the cognitive science (Fitts, Hick, Miller, Gestalt) that explains why patterns work or fail. This skill applies those principles to pattern evaluation.
- **`nng-ux-heuristics`** — Provides Nielsen's 10 heuristics for evaluation. This skill uses heuristics to score pattern execution.
- **`accessibility-inclusive-design`** — Provides WCAG compliance details. This skill flags accessibility gaps in pattern execution.
- **`design-systems-architecture`** — Provides token architecture. This skill assesses whether patterns consume tokens consistently (coherence).
- **`design-critique-case-studies`** — Provides deep product case studies. This skill provides broader pattern-level benchmarking.
- **`interaction-motion-design`** — Provides animation and motion patterns. This skill assesses whether patterns have appropriate motion.
- **`performance-states-patterns`** — Provides loading, error, and empty state patterns. This skill flags missing states as pattern gaps.

## Commands Powered by This Skill

| Command      | How This Skill Is Used                                                                |
| ------------ | ------------------------------------------------------------------------------------- |
| `/audit`     | Primary command — full analysis pipeline; pattern quality in heuristic evaluation     |
| `/component` | Consumes pattern taxonomy for component building, benchmark DNA for quality targeting |
| `/screen`    | Consumes screen patterns from taxonomy, sector expectations from matrix               |
| `/benchmark` | Uses designer benchmark DNA for competitive comparison                                |
| `/style`     | Uses pattern taxonomy and benchmark DNA for inspiration references                    |
| `/roast`     | References anti-pattern encyclopedia during design critique                           |
| `/remix`     | Uses prescriptions from pattern analysis to drive redesign                            |
| `/grade`     | Pattern quality contributes to overall design score                                   |
