---
name: design-process-methods
description: "Design process methodology: NNG's six phases, Double Diamond, Google Design Sprint, IDEO, Lean UX, and the bridge from AI-assisted building to evidence-based UX. Use when framing how the work should run, planning a sprint, or grounding a build in Empathize, Define, Ideate, Prototype, Test."
allowed-tools: Read, Grep, Glob
---

# UX Process Workflow — From Process to Product

## Purpose

Ground every AI-assisted build in established UX process. Prompting can produce polished UI quickly; process decides whether it solves the right problem. The vibe-coding shortcut is:

```
Traditional:  Empathize → Define → Ideate → Prototype → Test → Implement
Vibe coding:  Prompt → Ship → Hope
```

The result is UI that solves the wrong problem, looks like every other AI-generated interface, and erodes the builder's own design judgment (arXiv:2509.10652).

## The process in three lines

```
BEFORE you prompt: "Who is this for, and what problem does it solve?"
WHILE it generates:  "Does this match the user's reality, or the AI's patterns?"
AFTER it generates:  Run /audit + /a11y. Fix severity 3-4. Ship.
```

## Core rules

- **Use NNG's six phases in three stages.** Understand (Empathize, Define) → Explore (Ideate, Prototype) → Materialize (Test, Implement). Design Ops is iterative, so loop back as needed. NNG provides the thinking; Design Ops commands provide the doing.
- **Empathize before prompting.** Name a specific user, the task (verb + noun), their current workaround, what frustrates them, and their environment (device, context, accessibility needs).
- **Define in one sentence:** "Users who [X] need [Y] because [Z]." If you can't fill it in, go back to Empathize. Add measurable success criteria.
- **Diverge before converging.** List three approaches before generating one. The first idea is rarely the best.
- **Prototypes are questions.** Generate 2-3 variations and evaluate them; don't treat the first output as production code.
- **Testing is learning, not validation.** Heuristic review, cognitive walkthrough, accessibility audit, and 5-user think-aloud tests find problems; they don't prove the design works.
- **Watch for the three risks** of skipping process: pseudo-productivity (more screens, fewer solved problems), homogenization (every AI UI looks the same), and skill erosion (losing the ability to critique).
- **Check every generated screen** for the persona, the information hierarchy, and all seven states: empty, loading, populated, error, partial, offline, updating.

## Choosing a methodology

| Context | Methodology |
| --- | --- |
| Solo developer, vibe coding | Lean UX + Vercel/Figma design-engineer workflow |
| Small team (2-5) | Google Design Sprint (compressed) or Double Diamond |
| Large organization | IBM Enterprise Design Thinking |
| Accessibility-first | Microsoft Inclusive Design |
| Complex, ambiguous problem | IDEO Human-Centered Design |
| Continuous iteration | Spotify squad model + Lean UX |

## The Builder's Cheat Sheet

### I have 2 minutes

Run `/brief` on whatever you're about to build. Just the problem statement. That's it.

### I have 10 minutes

`/design-ops` → `/brief` → then build with the constraint stack pasted into your prompt.

### I have 30 minutes

`/brief` → `/style` → `/tokens` → then build. You now have a defined problem, visual direction, and token system.

### I have 2 hours

Full Phase 0→5 journey. `/design-ops` → `/brief` → `/style` → `/style` → `/tokens` → `/screen` → `/component` → `/audit` → `/a11y` → `/roast`. This is what real design teams do.

### I have a real product to ship

Follow the full 22-step journey via `/design-ops`. Run every audit. Loop `/roast` → `/remix` → `/roast` until all scores are 7+. This is how Stripe, Linear, and Notion work.

### The one non-negotiable

Whatever your time budget: **run `/audit` + `/a11y` before shipping**. 5 minutes. Zero excuses.

## Routing

| Question | Read |
| --- | --- |
| Each NNG phase: goals, methods, terminal workflow, command mapping; full process-to-command map | `references/nng-six-phases.md` |
| IDEO, Double Diamond, Design Sprint, IBM, Lean UX, Spotify, Microsoft, Vercel/Figma in depth; summary table; decision matrix | `references/company-ux-methodologies.md` |
| Before/while/after checklists, 15-minute UX check, anti-patterns, process recipes, maturity, constraint stack | `references/vibe-coder-ux-bridge.md` |
| ISO 9241-210, Norman's seven principles, cognitive laws | `references/academic-foundations.md` |

## Cross-References

- `nng-ux-heuristics` — The 10 heuristics used in the Test phase
- `ux-research-methods` — Research methodologies for the Empathize phase
- `cognitive-psychology-ux` — Cognitive laws that justify process rigor
- `agentic-ai-generative-ux` — AI-assisted design patterns and risks
- `ux-ethics-content-strategy` — Ethical frameworks for the Define phase
- `ux-metrics-measurement` — Measurement frameworks for success criteria
- `design-systems-architecture` — System thinking for the Implement phase
- `design-critique-case-studies` — Case studies showing process impact (Stripe, Linear: process-heavy; Sonos 2024, Healthcare.gov: process-light failures)
