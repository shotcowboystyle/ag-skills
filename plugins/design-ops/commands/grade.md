---
description: Visual quality scoring — Awwwards-calibrated 10-dimension assessment, designer DNA match, canonical rule compliance, production quality verdict.
argument-hint: "[design, screenshot, or file to score]"
---

# Grade — Visual Design Quality Score

## Before running

This command needs a design, screenshot, or file to score.

If the user invoked it with nothing and no target is evident from the conversation or open files, ask for it in one plain-language question and stop. Do not invent a target and do not produce generic output in place of the real work — output about something imaginary reads as authoritative and is worthless.

If a target is evident from context, use it and say which one you picked.

Score any UI's visual design quality across 10 weighted dimensions, calibrated to Awwwards and international design award standards. Every score is justified with specific observations, benchmarked against world-class products, and paired with actionable prescriptions that include exact values.

**Accepts**: Screenshot, code files, URL description, or Figma reference. Code + screenshot together gives highest-fidelity scoring. Do NOT score hypothetically without visual evidence.

---

## Scoring Protocol

### Step 0: Gather Context

1. **Input**: What was provided (screenshot, code, URL, Figma)
2. **What the app does**: Product description, purpose, target users
3. **Sector**: Auto-detect from content/code, or ask. Sector determines what "good" looks like — fintech and a children's game have different benchmarks
4. **Platform**: Web, iOS, Android, or cross-platform
5. **Prior Design Ops outputs**: Consume `/style`, `/tokens`, `/palette`, `/type` if available. Score against the intended direction
6. **Reference Board**: If `.design-ops/refs/board.json` exists, grade side by side with the references per `reference-intelligence/references/comparison-protocol.md`: report `Build | Best ref | Δ` and a verdict (clears the wall / below the wall / clone risk). No board → say the grade is uncalibrated

### Step 1: Visual Inventory

Catalog every visual element present:

**Colors**: List every distinct color observed. Note palette structure (or lack thereof). Count unique colors. Identify primary, secondary, semantic usage.

**Typography**: List every font observed (or inferred from code). Note size variations, weight usage, hierarchy levels. Count distinct type styles.

**Spacing**: Note spacing consistency or inconsistency. Identify apparent base unit (or lack of one). Note density.

**Shapes**: Border radii observed, shape consistency across components, icon style.

**Imagery**: Photos, illustrations, decorative elements — quality, treatment consistency.

**Icons**: Style (outlined/filled/mixed), consistency, grid adherence.

**Motion** (if code available): Transitions, animations, easing curves, durations.

**Elevation**: Shadow usage, depth layering, consistency.

**Visual language assessment**: Is there a coherent visual language? Intentional or ad hoc?

### Step 2: 10-Dimension Scoring

Score each dimension 1-10. Be honest — most production apps score 5-7. Scores of 8+ are rare and reserved for genuinely exceptional work. Scores below 4 indicate fundamental problems.

For EACH dimension, provide ALL of the following:

1. **Score** (1-10): Whole numbers only
2. **What's working**: Minimum 2 specific positive observations
3. **What's failing**: Minimum 2 specific negative observations (unless score is 9+)
4. **Benchmark**: Named product that scores 9/10 in this dimension + what they do that this UI does not
5. **Priority fix**: Single most impactful improvement with specific values

**The 10 dimensions**: use the dimensions, weights and per-score descriptors in `visual-design-mastery/references/visual-scoring-framework.md`. It is the single Design Ops rubric, shared with the critic agent. Don't restate, rename or reweight dimensions here.

### Step 3: Weighted Overall Score and DQS

Compute the overall score with the framework's weighted formula and read the tier from its **Score Interpretation** table.

**DQS** (Design Quality Score) = overall × 10, rounded to a whole number (0–100). It is the same score on a 100-point scale, not a separate rubric. The critic reports the same number.

**Awwwards equivalent**: Map to Awwwards 4-criteria system (Design, Usability, Creativity, Content — each 1-10). Estimate total score. Note: Awwwards skews toward marketing sites; adjust for product/app context.

### Step 4: Designer DNA Match

Identify which famous designer, studio, or design team this most resembles in approach and aesthetic:

- **Primary match**: [Designer/Studio name] — [Why: specific visual qualities that match]
- **Secondary match**: [Designer/Studio name] — [Why]
- **Aspirational match**: If this design were elevated to its full potential, which designer's work would it resemble?

Draw from the `designer-pattern-library.md` reference. Examples: Dieter Rams (functional minimalism), Jony Ive (material honesty), Tobias van Schneider (bold monochrome + accent), Stripe design team (engineering precision + warmth), Linear design team (dark mode craft + motion).

### Step 5: Canonical Rule Compliance

Check against the 70 canonical design rules from `canonical-design-rules.md`. Flag the top rules being violated and the top rules being followed well:

**Rules followed** (top 5):

| Rule # | Rule Name   | Evidence                     |
| ------ | ----------- | ---------------------------- |
| [N]    | [Rule name] | [How this design follows it] |

**Rules violated** (top 5):

| Rule # | Rule Name   | Violation       | Fix                        |
| ------ | ----------- | --------------- | -------------------------- |
| [N]    | [Rule name] | [What is wrong] | [Specific fix with values] |

### Step 6: Issue Priority Ranking

Rank ALL visual issues by impact * effort:

**P0 — Critical** (makes the design look amateur):

- Issues that immediately signal "not designed by a designer"
- These destroy credibility on first impression

**P1 — High Impact** (prevents professional quality):

- Issues that cap the design at "competent" level
- Fixing these moves the score from 5-6 range to 7-8 range

**P2 — Polish** (prevents world-class quality):

- Issues that separate good from great
- Fixing these moves the score from 7-8 range to 8.5+ range

**P3 — Delight** (opportunities for exceptional craft):

- Not problems but opportunities
- Micro-interactions, Easter eggs, exceptional empty states, crafted transitions

### Step 7: Visual Upgrade Roadmap

For each P0-P2 issue, provide ALL of the following:

1. **What's wrong**: Specific observation with exact location/component
2. **What world-class looks like**: Named product that does this exceptionally
3. **How to fix**: Specific values — exact colors (hex/oklch), exact sizes (px/rem), exact spacing, exact timing (ms). Not "make it bigger" but "increase to 18px with 28px line-height"
4. **Canonical rule**: Citation from `canonical-design-rules.md`
5. **Designer reference**: Who would solve this differently (from `designer-pattern-library.md`)
6. **Effort estimate**: Quick win (<1hr) | Medium (1-4hr) | Large (4hr+) | Strategic (days)
7. **Design Ops command**: Which `/command` addresses this issue

### Step 8: Score Projection

If all P0 fixes applied: **[X.X/10]** (from [current])
If all P0 + P1 fixes applied: **[X.X/10]**
If all P0 + P1 + P2 fixes applied: **[X.X/10]**

### Step 9: Before/After Comparison (if redesigning)

If the user is comparing a redesign against an original, provide:

| Dimension  | Before | After | Delta | Assessment                     |
| ---------- | ------ | ----- | ----- | ------------------------------ |
| Typography | X/10   | X/10  | +/-N  | [improved/regressed/unchanged] |
| ...        | ...    | ...   | ...   | ...                            |

**Overall**: [Before X.X] -> [After X.X] — Net change: [+/-X.X]

Highlight:

- Dimensions that improved
- Dimensions that regressed (this is critical — redesigns can lose qualities)
- Trade-offs made (e.g., gained polish but lost personality)

---

## Output Format

```
## Visual Grade: [App/Design Name]

### Overview
- **App**: [name/description]
- **Sector**: [detected/specified]
- **Platform**: [platform]
- **Input analyzed**: [what was examined]
- **Prior Design Ops context**: [consumed or "none"]

---

### Visual Inventory
**Colors**: [N] unique — [key colors with hex]
**Typography**: [N] type styles — [fonts, sizes]
**Spacing**: [base unit or "inconsistent"] — [density]
**Shapes**: [radii] — [consistency]
**Imagery**: [type and quality]
**Icons**: [style, consistency]
**Motion**: [present/absent, quality]
**Elevation**: [shadow usage]
**Visual Language**: [coherent/fragmented]

---

### 10-Dimension Scores

| # | Dimension | Weight | Score | Tier | Top Issue |
|---|-----------|--------|-------|------|-----------|
| 1 | Typography | 15% | X/10 | [tier] | [top issue] |
| 2 | Color | 12% | X/10 | [tier] | [top issue] |
| 3 | Spacing | 12% | X/10 | [tier] | [top issue] |
| 4 | Composition | 12% | X/10 | [tier] | [top issue] |
| 5 | Imagery | 8% | X/10 | [tier] | [top issue] |
| 6 | Iconography | 8% | X/10 | [tier] | [top issue] |
| 7 | Motion | 8% | X/10 | [tier] | [top issue] |
| 8 | Polish | 10% | X/10 | [tier] | [top issue] |
| 9 | Coherence | 8% | X/10 | [tier] | [top issue] |
| 10 | Craft | 7% | X/10 | [tier] | [top issue] |

**Overall Visual Score: [X.X/10] — [Quality Tier]** (DQS [NN])
**Awwwards Equivalent: ~[X.X]/10**

---

### Dimension Deep-Dives

#### 1. Typography — [X/10]
**Working**: [specific positives]
**Failing**: [specific negatives]
**Benchmark**: [Product] scores 9/10 because [reason]
**Priority fix**: [single most impactful improvement with exact values]

#### 2. Color — [X/10]
[same structure for all 10 dimensions]

---

### Designer DNA
- **Primary match**: [Designer/Studio] — [why]
- **Secondary match**: [Designer/Studio] — [why]
- **Aspirational**: [Designer/Studio] — [what this design could become]

---

### Canonical Rule Compliance

**Rules followed well**:
| Rule # | Rule | Evidence |
|--------|------|----------|

**Rules violated**:
| Rule # | Rule | Violation | Fix |
|--------|------|-----------|-----|

---

### Visual Issues by Priority

#### P0 — Critical
[Issues with location, observation, and fix with exact values]

#### P1 — High Impact
[Issues]

#### P2 — Polish
[Issues]

#### P3 — Delight Opportunities
[Opportunities]

---

### Upgrade Roadmap

| # | Priority | Dimension | Issue | Fix (with values) | Rule | Designer Ref | Effort | Command |
|---|----------|-----------|-------|--------------------|------|-------------|--------|---------|

---

### Score Projection
- P0 fixes applied: **[X.X/10]**
- P0 + P1 fixes: **[X.X/10]**
- P0 + P1 + P2 fixes: **[X.X/10]**

---

### Next Steps
1. [Highest-impact fix — specific]
2. [Second fix — specific]
3. [Third fix — specific]

**Recommended command sequence**:
-> `/style` — Generate/update visual direction
-> `/tokens` — Formalize tokens to fix coherence
-> `/component [name]` — Rebuild weakest-scoring components
-> `/grade` — Re-run to measure improvement
```

---

## Quality Gates

The output MUST include:

- [ ] All 10 dimensions scored with specific observations (minimum 2 working + 2 failing per dimension)
- [ ] Named benchmark product for every dimension
- [ ] Weighted overall score computed correctly using the formula
- [ ] Quality tier label applied correctly
- [ ] Awwwards equivalent estimated
- [ ] Designer DNA match with primary, secondary, and aspirational
- [ ] Canonical rule compliance (top 5 followed, top 5 violated)
- [ ] Priority-ranked issues across P0-P3 levels
- [ ] Every prescription includes specific values (hex, px, ms — not "make it better")
- [ ] Canonical design rule citation for every P0 and P1 prescription
- [ ] Designer reference for P0 prescriptions
- [ ] Effort estimate for every prescription
- [ ] Design Ops command for every prescription
- [ ] Upgrade roadmap table sorted by priority
- [ ] Score projection showing expected score after each priority tier

The output MUST NOT include:

- Vague feedback ("could be better", "needs work") — every finding must be specific
- Scores without justification — every score must cite what is present and what is missing
- Recommendations without benchmarks — every upgrade must reference a product that does it well
- Inflated scores — most production apps score 5-7. Be honest
- Prescriptions without specific values — "increase contrast" is not acceptable; "change text from #999 to #555 on #fff (ratio: 7.0:1)" is
- Hypothetical scoring — require visual evidence (code, screenshot, or URL description)

---

## Cross-References

When scoring visual design, draw knowledge from:

- `visual-design-mastery` -> `visual-scoring-framework.md` — Scoring rubric and dimension definitions
- `visual-design-mastery` -> `designer-pattern-library.md` — Designer references and benchmark comparisons
- `visual-design-mastery` -> `canonical-design-rules.md` — Rule citations for prescriptions
- `visual-design-mastery` -> `color-mastery.md` — Color harmony evaluation, contrast verification
- `visual-design-mastery` -> `typography-mastery.md` — Type scale evaluation, readability assessment
- `visual-design-mastery` -> `composition-mastery.md` — Layout and spacing evaluation
- `color-palette-library` — Palette quality benchmarks
- `typography-pairing-recipes` — Type pairing quality assessment
- `shadow-elevation-density` — Elevation and density assessment
- `ui-pattern-intelligence` — Pattern quality and benchmark products
- `sector-style-intelligence` — Sector-specific visual expectations
- `accessibility-inclusive-design` — WCAG contrast and motion requirements
- `interaction-motion-design` — Motion quality evaluation
- `cognitive-psychology-ux` — Perception science grounding

---

## Next Steps

After `/grade`:

- `/style` — Generate or revise visual direction based on findings
- `/tokens` — Formalize design tokens to fix coherence issues
- `/palette` — Fix color issues with a proper palette
- `/type` — Fix typography issues with a proper type system
- `/component [name]` — Rebuild lowest-scoring components
- `/audit` — Full comprehensive audit (heuristic + cognitive + flow + fortification)
- `/roast` — Quick opinionated critique

---

## Badge

Offer a badge only when DQS is 70+ (Professional or World-class) and no dimension scores below 5:

```markdown
![Design Quality Score](https://img.shields.io/badge/DQS-[SCORE]-[COLOR]?style=flat-square&label=Design%20Ops)
```

`[COLOR]` is `22C55E` for 85+ and `EAB308` for 70–84. Below 70, suggest `/fix` instead.

---

### Comparison Mode

When run with a reference (`/grade vs stripe` or `/grade vs linear`), score the user's design against a reference product:

| Dimension   | Your App | [Reference] | Gap    |
| ----------- | -------- | ----------- | ------ |
| Typography  | [X]      | [X]         | [+/-N] |
| Color       | [X]      | [X]         | [+/-N] |
| Spacing     | [X]      | [X]         | [+/-N] |
| Composition | [X]      | [X]         | [+/-N] |
| Imagery     | [X]      | [X]         | [+/-N] |
| Iconography | [X]      | [X]         | [+/-N] |
| Motion      | [X]      | [X]         | [+/-N] |
| Polish      | [X]      | [X]         | [+/-N] |
| Coherence   | [X]      | [X]         | [+/-N] |
| Craft       | [X]      | [X]         | [+/-N] |
| **DQS**     | **[X]**  | **[X]**     | **[+/-N]** |

Dimensions come from the framework above. When `.design-ops/refs/board.json` exists, grade against the board instead (Step 0).

Then generate specific recommendations to close the gap, prioritized by impact:

1. **Largest gap first**: Address the dimension with the biggest negative gap
2. **Quick wins**: Identify gaps that can be closed with minimal effort
3. **Strategic investments**: Identify gaps that require significant work but yield the highest quality improvement
4. **Irrelevant gaps**: Note dimensions where the gap is expected due to different product contexts (e.g., a B2B tool vs a consumer marketing site)

**Available reference products**: Stripe, Linear, Vercel, Notion, Figma, Apple, Airbnb, Shopify, GitHub, Raycast, Arc, Craft, Things 3, Bear, Mercury, Ramp, Loom, Pitch. Reference scores are based on public product analysis and the `designer-pattern-library.md` benchmarks.

**Usage**:

- `/grade vs stripe` — Compare against Stripe's design quality
- `/grade vs linear` — Compare against Linear's design quality
- `/grade vs [product]` — Compare against any well-known product
