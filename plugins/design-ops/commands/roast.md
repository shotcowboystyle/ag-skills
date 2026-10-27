---
description: Quick brutal design critique — 10 dimensions scored, letter grade, top fixes, one-line verdict. Fast and opinionated.
argument-hint: "[design, screenshot, or file to critique]"
---

# Roast — Quick Design Critique

## Before running

This command needs a design, screenshot, or file to critique.

If the user invoked it with nothing and no target is evident from the conversation or open files, ask for it in one plain-language question and stop. Do not invent a target and do not produce generic output in place of the real work — output about something imaginary reads as authoritative and is worthless.

If a target is evident from context, use it and say which one you picked.


Fast, opinionated, actionable design critique. Not comprehensive (that is `/audit`). This is the "show me your design and I will tell you what is wrong in 60 seconds" command.

**Accepts**: Code, screenshot description, URL description, or Figma reference.

---

## Critique Protocol

### Step 0: Establish Context

Quick context grab — do not block on missing information:

1. **What is it**: Component, screen, flow, or product
2. **Who is it for**: Target users and their context
3. **What stage**: Exploration, refinement, or final review
4. **Against what**: If `.design-ops/refs/board.json` exists, roast against the wall. Look at the best reference's screenshots and name where the build falls short, citing the reference by name
4. **Designer's questions**: Does the designer have specific concerns? Address those first

### Step 1: Statements of Meaning

Before critiquing, identify what WORKS. This is not flattery — it identifies what to protect during iteration. Following the Liz Lerman Critical Response Process.

List 3-5 genuine strengths with specific reasoning:
- What stands out positively and WHY
- What design decisions show clear intentionality
- What would be lost if this were redesigned carelessly

### Step 1.5: Questions Before Opinions (CRP Steps 2-3)

Liz Lerman's process does not go from strengths straight to judgment. Two question rounds sit in between, and they are the part that keeps a critique from becoming an opinion dump. Run both, briefly.

**Designer's questions.** Ask what the designer wants examined. If no designer is present — the usual case when the target is code or a screenshot — infer the two or three decisions that were clearly deliberate and state what they appear to be optimising for. Naming an intention before judging it is what separates a critique from a reaction.

**Neutral questions.** Ask about the design without smuggling an opinion into the question. A neutral question has no preferred answer.

- Neutral: "What decides which of these two actions is primary?"
- Not neutral: "Why is the primary action so hard to find?"

The second sentence is an opinion wearing a question mark. If a question can only be answered by agreeing with you, rewrite it or move it to the findings where it belongs. Where a neutral question exposes a decision with no answer, that is a finding — usually a good one.

### Step 2: Score 10 Dimensions

Score the 10 dimensions in `visual-design-mastery/references/visual-scoring-framework.md`, 1-10 each, using its per-score descriptors. It is the one Design Ops rubric, shared with `/grade` and the critic. Be honest — most production designs score 4-7. An 8+ is genuinely impressive. A 3 or below means fundamental problems.

Clarity, interaction feedback and accessibility are not separate dimensions here. Raise problems with them as must-fix items (Step 4), and send deep accessibility work to `/a11y`.

### Step 2.5: AI Slop Detection

Scan the design for telltale AI-generated UI patterns. Check each item that applies:

**THE PURPLE GRADIENT SYNDROME**:
- [ ] Uses default Tailwind indigo/violet/purple as primary color (bg-indigo-500, bg-purple-600, bg-violet-500)
- [ ] Purple/indigo gradient backgrounds (from-indigo-500 to-purple-600)
- [ ] White or near-white background with purple accents — the #1 AI-generated look
- [ ] Uses Tailwind's default color palette with zero customization

**THE FONT MONOTONY**:
- [ ] Inter as the only font (or Roboto, system-ui with no intentional pairing)
- [ ] No font pairing — heading and body use same font/weight
- [ ] Generic font-sans with no typographic hierarchy
- [ ] Missing type scale — sizes feel random rather than systematic

**THE LAYOUT LOTTERY**:
- [ ] 3-column equal-width grid for everything (the default AI layout)
- [ ] Every section has the same padding/spacing
- [ ] Hero section with centered text + generic gradient background
- [ ] Features grid: 3 cards with icon + title + paragraph (the AI cliche)
- [ ] No visual rhythm variation — every section same height/weight

**THE COMPONENT COPY-PASTE**:
- [ ] Buttons with bg-blue-500 or bg-indigo-600 and no hover state defined
- [ ] Cards with rounded-lg shadow-md (the AI default card)
- [ ] Missing states: no loading, error, empty, disabled
- [ ] No micro-interactions or transitions
- [ ] Generic placeholder content ("Lorem ipsum" or "Description goes here")

**THE ACCESSIBILITY VOID**:
- [ ] No ARIA labels on interactive elements
- [ ] Color as the only meaning indicator
- [ ] No focus-visible styles
- [ ] No skip navigation
- [ ] Images without alt text

**Slop Scoring**:
Count the number of checks that apply:
- **0-2**: Clean — this doesn't look AI-generated
- **3-5**: Mild slop — some AI defaults slipped through
- **6-8**: Moderate slop — needs a Design Ops `/fix` pass
- **9+**: Full slop — this is raw AI output, run `/fix` immediately

Add a **Slop Score** to the final output alongside the letter grade. Format: `Slop Score: X/23 ([Severity]) — run /fix to transform this into visual cuisine`

### Step 3: Calculate DQS

**Total**: DQS — the framework's weighted overall × 10, rounded (0-100). The same number `/grade` reports.

**Letter Grade**:
- **A** (90-100): Exceptional. Ship it and submit to Awwwards
- **A-** (85-89): Excellent. Minor polish away from world-class
- **B+** (80-84): Very good. Competitive with top products
- **B** (75-79): Good. Solid professional work with room to grow
- **B-** (70-74): Above average. Some clear weaknesses to address
- **C+** (65-69): Decent. Functional but unimpressive
- **C** (60-64): Average. Needs meaningful improvement
- **C-** (55-59): Below average. Multiple areas need work
- **D** (45-54): Poor. Significant problems across dimensions
- **F** (0-44): Failing. Fundamental redesign needed

### Step 4: Top 3 Must-Fix Items

For each must-fix, provide:

1. **What is wrong**: Specific observation with exact location
2. **Why it matters**: UX principle or cognitive science grounding (one line)
3. **How to fix it**: Specific actionable fix
4. **Code fix** (if code was provided): Exact corrected code snippet

These are the three changes that will have the highest impact on the overall score. Prioritize by (severity * breadth of impact).

**Classify every finding, not just the top three.** Three must-fixes is the right ceiling for what leads the output, but findings below that line still need a home, and the class you assign tells the reader what to do with each one:

| Class | Meaning | What the reader does |
|---|---|---|
| **Must-fix** | Breaks the experience, blocks a task, or fails accessibility. Max 3. | Fix before shipping |
| **Should-fix** | Real cost to quality or conversion, but the design works without it | Fix this cycle |
| **Could-improve** | Craft and polish. Defensible to leave as-is | Fix when touching that area |
| **Explore** | A genuine open question the critique cannot settle | Route to research, do not argue |

**Explore** is the class most critiques lack. When a disagreement rests on an assumption about users rather than a design principle, saying so is more honest than picking a side with confidence you have not earned. Send it to `/research` and say what would resolve it.

### Step 5: Top 3 Strengths to Keep

For each strength:

1. **What is working**: Specific observation
2. **Why it works**: UX principle that makes this effective
3. **Protect it**: What would accidentally break this during iteration

These are the three things that would hurt the design most if lost.

### Step 6: One-Line Verdict

A single sentence that captures the essence of this design's quality. Be direct. Be memorable. Examples:

- "A solid foundation buried under visual noise — strip it back and you have something good."
- "All the right components, none of the right hierarchy — this design whispers when it should shout."
- "Ship-ready craft with one fatal flaw: users cannot find the primary action."
- "This is what happens when a developer designs without a type scale — functional but forgettable."
- "Genuinely impressive interaction design held back by a color palette that fights itself."

---

## Output Format

```
## Roast: [Design Name]

### Context
- **Artifact**: [type]
- **Stage**: [exploration / refinement / final]
- **Users**: [who]

---

### Strengths (Protect These)
1. **[Strength]**: [Why it works — principle grounding]
2. **[Strength]**: [Why it works]
3. **[Strength]**: [Why it works]

---

### Dimension Scores

| # | Dimension | Score | Observation |
|---|-----------|-------|-------------|
| 1 | Typography | X/10 | [one-line observation] |
| 2 | Color | X/10 | [one-line observation] |
| 3 | Spacing | X/10 | [one-line observation] |
| 4 | Composition | X/10 | [one-line observation] |
| 5 | Imagery | X/10 | [one-line observation] |
| 6 | Iconography | X/10 | [one-line observation] |
| 7 | Motion | X/10 | [one-line observation] |
| 8 | Polish | X/10 | [one-line observation] |
| 9 | Coherence | X/10 | [one-line observation] |
| 10 | Craft | X/10 | [one-line observation] |

**DQS: [X/100] — Grade: [Letter]**
**Slop Score: [X/23] ([Clean/Mild/Moderate/Full]) — run `/fix` to transform this into visual cuisine**

---

### AI Slop Detection

| Category | Flags Hit | Details |
|----------|-----------|---------|
| Purple Gradient Syndrome | X/4 | [specifics] |
| Font Monotony | X/4 | [specifics] |
| Layout Lottery | X/5 | [specifics] |
| Component Copy-Paste | X/5 | [specifics] |
| Accessibility Void | X/5 | [specifics] |

**Slop Score: [X/23] ([Clean/Mild/Moderate/Full])**

---

### Must-Fix (Top 3)

#### 1. [Issue Title]
- **What**: [specific observation + location]
- **Why**: [principle — one line]
- **Fix**: [specific action]
- **Code**: [corrected snippet if applicable]

#### 2. [Issue Title]
[same format]

#### 3. [Issue Title]
[same format]

---

### Keep (Top 3)

1. **[Strength]** — [what would break it during iteration]
2. **[Strength]** — [what would break it]
3. **[Strength]** — [what would break it]

---

### Verdict
> [One-line verdict]

---

### Next Steps
- `/audit` — Deep comprehensive audit (all lenses)
- `/grade` — Visual quality scoring (Awwwards-calibrated)
- `/a11y` — Accessibility deep-dive
- `/remix` — Fix the issues found
```

---

## Quality Gates

The output MUST include:
- [ ] 3-5 genuine strengths identified before any criticism (Liz Lerman process)
- [ ] All 10 dimensions scored with one-line observation per dimension
- [ ] DQS calculated correctly (weighted overall × 10, per the framework)
- [ ] Letter grade assigned correctly from the scale
- [ ] Top 3 must-fix items with specific location, principle grounding, and actionable fix
- [ ] Top 3 strengths with what would break them during iteration
- [ ] One-line verdict that is specific to THIS design (not generic)
- [ ] Code fixes included when code input was provided
- [ ] AI Slop Detection checklist completed with per-category flags and total Slop Score

The output MUST NOT include:
- Vague criticism ("could be improved") — every finding must cite what specifically and where
- Inflated scores — most designs score 4-7 per dimension. Justify any 8+ or 3-
- Generic verdict that could apply to any design — make it specific
- More than 3 must-fix items — this is a quick critique, not a comprehensive audit
- Unsupported opinions — every criticism must cite a UX principle or cognitive science basis

---

## Cross-References

When critiquing, draw evaluation criteria from:
- `design-critique-case-studies` — Liz Lerman critique methodology, case study benchmarks
- `nng-ux-heuristics` — Heuristic violation identification
- `cognitive-psychology-ux` — Cognitive load and bias analysis
- `accessibility-inclusive-design` — Accessibility scoring
- `ux-ethics-content-strategy` — Ethical design evaluation
- `ui-visual-design-system` — Visual design quality assessment
- `visual-design-mastery` — Visual scoring calibration
- `sector-style-intelligence` — Sector-appropriate expectations

---

## Next Steps

After `/roast`:
- `/audit` — Comprehensive audit (the deep version of this)
- `/grade` — Visual quality scoring
- `/a11y` — Accessibility audit
- `/remix` — Fix the issues found
- `/component` — Rebuild weak components
