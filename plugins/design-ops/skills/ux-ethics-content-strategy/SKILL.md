---
name: ux-ethics-content-strategy
description: Dark pattern detection and avoidance, persuasive vs. manipulative design, privacy UX, the regulatory landscape, sustainable/green UX, and UX writing principles, readability, and inclusive language. Use when auditing a flow for manipulation, designing consent or privacy UX, or setting content strategy; for interface strings use micro-copy-intelligence.
allowed-tools: Read, Grep, Glob
---

# UX Ethics & Content Strategy — Designing with Integrity

"Design is a political act. Every thing we design goes on to design us back." — Anne-Marie Willis

## Core Ethical Principles

1. **Respect autonomy** — users must make informed, uncoerced decisions
2. **Transparent by default** — never hide information that affects user decisions
3. **Benefit over extraction** — design for user value, not just engagement metrics
4. **Inclusive representation** — content, imagery, and language must reflect human diversity
5. **Privacy as a right** — treat user data as if it were your own; collect minimum, protect maximum

## Dark Patterns

Dark (deceptive) patterns trick users into doing things they did not intend, exploiting cognitive biases for business gain at user expense (term coined by Harry Brignull). The taxonomy in `references/dark-pattern-avoidance.md` covers 16: trick questions, sneak into basket, roach motel, privacy zuckering, misdirection, hidden costs, bait and switch, confirmshaming, forced continuity, disguised ads, friend spam, nagging, urgency, scarcity, social proof manipulation, obstruction. The default ethical alternatives:

- Affirmative, plain opt-in language; never double negatives or pre-checked boxes
- Exit as easy as entry: self-service cancellation, deletion, unsubscribe
- Equal visual weight for "Accept all" and "Reject all"
- Show the total cost, including fees, as early as possible
- Neutral decline copy ("No thanks", "Maybe later"), never guilt
- Warn before a trial converts; require explicit opt-in to paid
- Label all ads and sponsored content

### Dark Pattern Detection Checklist

When reviewing any interface, verify:
- [ ] Can the user complete their goal without unintended side effects?
- [ ] Are all costs, commitments, and consequences visible before action?
- [ ] Is the "undo" or "opt-out" path as easy as the "do" or "opt-in" path?
- [ ] Are default selections in the user's interest, not the business's?
- [ ] Is the visual hierarchy honest (primary action = user's most likely intent)?
- [ ] Would the design be embarrassing if explained transparently to users?

## Privacy UX

Default to maximum privacy. Ask for data only in context and say why; make consent granular, unbundled, and as easy to withdraw as to give; let users see, export, and truly delete their data. Privacy by Design principles and the full pattern list: `references/privacy-ux.md`.

## UX Writing Principles

1. **Clear over clever** — functional text must be immediately understood
2. **Concise** — use the minimum words needed; every word must earn its place
3. **Conversational** — write like a knowledgeable friend, not a legal document
4. **Consistent** — same terms for same concepts across the entire product
5. **Actionable** — tell users what to do, not just what happened

Target an 8th-grade reading level (Flesch-Kincaid) for consumer products and front-load key information. Microcopy templates and per-component strings (buttons, errors, empty states, confirmations, tooltips, loading, permissions) are owned by `micro-copy-intelligence`.

## Routing

| Question | Read |
| --- | --- |
| Auditing for manipulation: the 16-pattern taxonomy, audit methodology, flow checklists, cookie consent, subscription and cancellation ethics, e-commerce, FTC/GDPR/CCPA/DSA/AI Act and the 2025-2026 regulatory landscape | `references/dark-pattern-avoidance.md` |
| Privacy by Design principles; data collection, consent, and data transparency patterns | `references/privacy-ux.md` |
| UX writing system (voice chart, style guide, terminology, governance), readability, number and date formatting, legal copy, content accessibility, content strategy and IA, inclusive language, content operations, AI content design | `references/content-writing-readability.md` |
| Environmental impact: sustainable UI principles, performance as sustainability, energy-efficient patterns, green hosting, carbon measurement, sustainable color | `references/sustainable-green-ux.md` |
| Interface strings and templates | `micro-copy-intelligence` skill |

## Cross-Referencing

- Microcopy templates and strings: `micro-copy-intelligence`
- Visual design of content: `visual-design-mastery`
- Accessibility requirements: `accessibility-inclusive-design`
- Heuristic evaluation of content: `nng-ux-heuristics`
- AI content generation ethics: `agentic-ai-generative-ux`
- Cross-cultural ethics, localization, regional privacy norms: `cross-cultural-i18n-ux`
- Cognitive biases that dark patterns exploit: `cognitive-psychology-ux` (its cognitive-biases reference)

## Key Sources

- Brignull, H. "Deceptive Patterns" (deceptivedesign.net)
- Cavoukian, A. "Privacy by Design" framework
- Krug, S. (2014). "Don't Make Me Think"
- Podmajersky, T. (2019). "Strategic Writing for UX"
- NNG Group content strategy and UX writing articles
