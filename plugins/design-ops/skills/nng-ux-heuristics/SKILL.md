---
name: nng-ux-heuristics
description: Jakob Nielsen's 10 usability heuristics with modern interpretation, evaluation protocol, and 0-4 severity rating scale. Use when running a heuristic evaluation or usability review, rating the severity of a finding, or grounding UX feedback in established principles.
allowed-tools: Read, Grep, Glob
---

# NNG UX Heuristics

Jakob Nielsen's 10 heuristics (1994, refined by NNG since) apply across GUIs, AI-native, voice, and spatial interfaces. Every element must earn its place by serving user goals.

## The 10 Heuristics

| # | Heuristic | Modern check | Severity tier when violated |
|---|---|---|---|
| H1 | Visibility of system status | Progress that says *what* is happening; AI processing/uncertainty states; presence in collaboration; skeletons | High |
| H2 | Match between system and real world | Audience-appropriate language; AI confidence in human terms; spatial/voice conventions | Medium-High |
| H3 | User control and freedom | Confirm destructive actions with consequences; multi-level undo; editable/rejectable AI output; autosave with history | Critical |
| H4 | Consistency and standards | Platform conventions (HIG, Material 3, Fluent); internal suite consistency; tokens enforce it | Medium |
| H5 | Error prevention | Inline validation while typing; smart defaults; constrained inputs; friction on dangerous zones | High |
| H6 | Recognition rather than recall | Recents and favorites; command palette (Cmd+K); breadcrumbs; autocomplete | Medium |
| H7 | Flexibility and efficiency of use | Discoverable shortcuts; customizable workflows; progressive disclosure; bulk operations | Low-Medium (High for pro tools) |
| H8 | Aesthetic and minimalist design | Content over chrome; density matched to expertise; AI shows results first, process second | Medium |
| H9 | Recognize, diagnose, recover from errors | What happened, why, how to fix; inline near the source; retry with offline fallback | High |
| H10 | Help and documentation | Contextual help over portals; teach by doing; task-oriented, searchable | Low (High for complex tools) |

## Evaluation Protocol

1. **Prepare** — scope the flows; pick 3-5 evaluators with diverse expertise; prepare personas and task scenarios; agree on the severity scale.
2. **Evaluate independently** — each evaluator walks every task against all 10 heuristics, captures evidence, maps each violation to heuristic(s), and rates it.
3. **Report** — consolidate across evaluators, deduplicate, prioritize by severity x frequency x user impact, write actionable recommendations, track remediation.

## Severity Scale (0-4)

- **0 — Not a usability problem:** no user impact
- **1 — Cosmetic:** fix when convenient
- **2 — Minor:** slight delays; moderate priority
- **3 — Major:** significant difficulty; high priority
- **4 — Catastrophe:** prevents task completion; fix before release

## Routing

| Question | Read |
|---|---|
| Running an evaluation end to end: protocol, writing a finding, severity calibration examples, prioritization matrix, reports per audience, pitfalls, benchmarking | `references/heuristic-evaluation-guide.md` |
| What a heuristic means on a modern interface, heuristic conflicts, industry and cultural applications, famous violations, per-heuristic quick reference, the cognitive science behind H5, H6, H8 | `references/modern-heuristic-applications.md` |

## Cross-Referencing

- Visual design evaluation criteria: `visual-design-mastery`
- Accessibility-specific evaluation: `accessibility-inclusive-design`
- Mobile-specific heuristic application: `mobile-ux-design`
- AI interface evaluation: `agentic-ai-generative-ux`
- Why heuristics work (memory, cognitive load, mental models): `cognitive-psychology-ux`
- Running evaluations as team critique: `design-critique-case-studies`
- Code that implements compliant loading, undo, validation, command palettes: `component-patterns-code`

## Key Sources

- Nielsen, J. (1994). "10 Usability Heuristics for User Interface Design" — updated 2024
- Norman, D. (2013). "The Design of Everyday Things" — revised edition
- NNG Group research articles and studies (2020-2025)
- Rams, D. "Ten Principles for Good Design"
