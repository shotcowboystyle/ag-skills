---
name: ux-research-methods
description: "UX research methodology: usability testing protocols, user interviews, contextual inquiry, surveys, card sorting, and diary studies, plus synthesis frameworks including JTBD, journey mapping, and affinity diagramming. Use when planning a study, writing a discussion guide, or analyzing research data."
allowed-tools: Read, Grep, Glob
---

# UX Research Methods

## Research Philosophy

Great design is grounded in evidence, not assumption. UX research exists to reduce the risk of building the wrong thing and to illuminate the gap between designer intent and user reality. Every design decision should trace back to user evidence — whether from direct observation, behavioral data, or validated heuristics.

### The Research Hierarchy (adapted from NNG Group)

1. **Behavioral data** (what users do) > **Attitudinal data** (what users say)
2. **Qualitative research** (why) informs **quantitative research** (how much)
3. **Generative research** (discover opportunities) precedes **evaluative research** (validate solutions)
4. **Continuous discovery** (ongoing) outperforms **project-based research** (periodic)

## Method Selection

| Question type | Method | Typical sample |
|---|---|---|
| Workflows, workarounds, unarticulated needs | Contextual inquiry | 4-8 |
| Motivations, mental models | Semi-structured interviews | 5-8 per segment |
| Behavior over time | Diary study | 10-15 (dropout) |
| Information architecture | Card sorting / tree testing | 15-30 / 50+ |
| Can users complete the task? | Moderated usability test | 5 finds ~85% of issues |
| Scaled task evidence | Unmoderated remote test | 10-20 |
| Expert review, no users | Heuristic evaluation (3-5 evaluators) or cognitive walkthrough | n/a |
| How many, how much | Surveys / analytics | 100+ (400+ for segments) |
| Which variant performs better | A/B test | traffic for significance, define MDE first, 1-2 weeks min |

## Research Operations

### Planning a Research Study
1. Define research questions (3-5 focused questions per study)
2. Select appropriate method(s) based on questions and constraints
3. Write a 1-page research plan: goals, method, participants, timeline, deliverables
4. Recruit representative participants — screen rigorously for target criteria
5. Prepare materials: discussion guide, task scenarios, consent forms
6. Pilot test the protocol with 1-2 internal participants

### Participant Recruitment
- Screen for behavioral criteria, not just demographics
- Include users with disabilities (minimum 1 per study for inclusive insights)
- Offer fair compensation respecting participants' time and expertise
- Maintain a participant panel for longitudinal research
- Avoid "professional testers" — seek real target users

### Ethical Research Practice
- Obtain informed consent with clear explanation of data usage
- Allow participants to withdraw at any time without consequence
- Protect participant privacy and anonymize data
- Never manipulate or deceive participants
- Share findings back with participants when possible

## AI-Assisted Analysis Rules

Treat LLM themes and codes as a first pass only: review 100% of AI output for the first three studies, then spot-check 30-50%; trace every insight to a participant quote; the researcher authors the report; anonymize transcripts and get consent before any upload; disclose AI assistance.

## Routing

- **Choosing and running a study** — the full method selection matrix (discovery, evaluative, quantitative), moderator scripts, interview guides, contextual inquiry, diary studies, card sorting and tree testing, A/B protocols, survey design, screener and consent templates, research ops: read `references/research-protocols.md`.
- **Making sense of what you collected** — affinity diagramming, thematic coding, Jobs-to-Be-Done, journey maps, personas, SUS and significance tests, mixed methods, repositories, atomic research, AI-assisted synthesis with prompts and ethics: read `references/analysis-frameworks.md`.

## Cross-Referencing

- For heuristic evaluation methodology, reference `nng-ux-heuristics`.
- For accessibility research requirements, reference `accessibility-inclusive-design`.
- For mobile-specific testing considerations, reference `mobile-ux-design`.
- For design system validation, reference `design-systems-architecture`.
- For UX metrics and measurement frameworks, reference `ux-metrics-measurement`.
- For AI-specific research methods, reference `agentic-ai-generative-ux`.
- Turning findings into design direction with structured critique: `design-critique-case-studies`

## Key Sources

- NNG Group: "Which UX Research Methods" and research methodology articles
- Portigal, S. (2013). "Interviewing Users"
- Krug, S. (2014). "Rocket Surgery Made Easy"
- Sauro, J. & Lewis, J. (2016). "Quantifying the User Experience"
- Arxiv: GenAI for UX Research (Dec 2025)
- Arxiv: EvAlignUX — Evaluating AI Alignment in UX Research (Sep 2024)
