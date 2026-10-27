---
name: design-critique-case-studies
description: Structured design critique using the Liz Lerman Critical Response Process, plus deep-dives on Stripe, Linear, Notion, Airbnb, Figma, and Arc, and post-mortems of redesign failures like Snapchat 2018 and Sonos 2024. Use when running a critique session, giving design feedback, or learning from a shipped product.
allowed-tools: Read, Grep, Glob
---

# Design Critique & Case Studies

Critique is the cheapest quality intervention in the lifecycle: a flaw caught in wireframes costs hours, the same flaw after launch costs months. It also raises the team's quality floor, builds shared vocabulary, and spreads senior judgment.

## Critique Types

- **Studio** — scheduled, 4-8 people, 45-60 minutes; roles: presenter, facilitator, critics, note-taker. For major milestones.
- **Desk** — informal 1:1, frequent; still anchor feedback to a principle or user scenario.
- **Async** — Figma comments or a 3-5 minute recorded walkthrough; tag every comment [Question], [Concern], [Suggestion], or [Praise].
- **Self** — checklist before group critique: empty/loading/error states, hierarchy clear in 3 seconds, strongest affordance on the primary action, user language, WCAG AA contrast and target size.

## Liz Lerman's Critical Response Process

Four steps, in strict order:

1. **Statements of Meaning** — critics name what works and why (specific, not "looks nice"), so the presenter knows what to protect.
2. **Artist's Questions** — the presenter asks about what they are unsure of, steering feedback to real concerns.
3. **Neutral Questions** — critics ask non-leading questions to surface intent ("What was your rationale for...", not "Don't you think...").
4. **Opinion Time** — opinions only with the presenter's permission, and grounded in a principle or evidence.

## Critique by Fidelity (30/60/90)

| Stage | Focus | Out of scope |
|---|---|---|
| 30% concept | Right problem, information architecture, core flows, mental model | Color, type, pixels |
| 60% mid-fi | Interaction patterns, content hierarchy, edge cases (empty, error, overflow, truncation), systematic heuristic pass | Visual polish |
| 90% pre-handoff | Token consistency, micro-interactions, WCAG AA, responsive behavior, implementation ambiguity | Foundational architecture |

## Anti-Patterns

- **Design by committee** — name one decision-maker before the session; everyone is heard, one person decides.
- **HiPPO** — the most senior person speaks last, or run an anonymous written first round.
- **Vague feedback** ("make it pop") — every comment must cite a heuristic, principle, or user scenario.
- **Preference vs. evidence** — separate them; when evidence is missing, flag the question for user testing.
- **Bike-shedding** — time-box by decision impact; the facilitator redirects to higher-impact topics.

Always ground feedback in principles, heuristics, or evidence. When principles conflict, name the tradeoff and recommend how to resolve it: user testing, business priority, or design principle hierarchy.

## Routing

| Question | Read |
|---|---|
| Running a session: facilitator guide, formats, feedback frameworks (I Like/I Wish/What If, Rose-Thorn-Bud, Feldman, Six Thinking Hats), async protocols, the 10-dimension scoring rubric, receiving critique, critique types, full Lerman steps | `references/critique-methodology.md` |
| Why a product's design works: Stripe, Linear, Notion, Airbnb, Figma, Arc, Duolingo, Vercel, Apple Health, Discord, plus condensed analyses (Raycast, Supabase, Superhuman, Cal.com, Framer, Obsidian, Loom, and more) | `references/product-deep-dives.md` |
| Redesign post-mortems: Snapchat, Windows 8, Digg, Twitter/X, Google Plus, Sonos, Healthcare.gov, Reddit API, YouTube dislikes, Skype; redesign safety checklist | `references/redesign-failure-analysis.md` |

## Cross-References

- Grounding comments in a heuristic, especially at 60%: `nng-ux-heuristics`
- Biases in the critique room (anchoring, confirmation, groupthink): `cognitive-psychology-ux`
- Settling disagreements with a usability test: `ux-research-methods`
- Design system component use at 90%: `component-patterns-code`
- Quantitative evidence for feedback: `ux-metrics-measurement`
- Dark patterns and manipulative content: `ux-ethics-content-strategy`
