---
name: ux-metrics-measurement
description: "UX measurement: HEART framework, SUS, UEQ, SUPR-Q, task success and time-on-task metrics, A/B testing statistics, AI-specific metrics, and design system ROI. Use when defining UX KPIs, building a measurement plan, interpreting a usability score, or proving UX impact."
allowed-tools: Read, Grep, Glob
---

# UX Metrics & Measurement

## Measurement Philosophy

Measure what matters, not what is easy. Vanity metrics (page views, downloads, time on site) tell you what happened but not whether the experience was good. Meaningful UX metrics connect user behavior to user satisfaction to business outcomes. Every metric in the system should answer one of three questions: Is it usable? Is it useful? Is it desirable?

### The Measurement Hierarchy

1. **Behavioral metrics** (what users do) are more reliable than **attitudinal metrics** (what users say).
2. **Task-level metrics** (can users accomplish goals?) matter more than **session-level metrics** (how long did users stay?).
3. **Leading indicators** (early signals of success/failure) are more actionable than **lagging indicators** (outcomes measured after the fact).
4. **Benchmarked metrics** (compared to industry or historical baseline) are more meaningful than **absolute metrics** (numbers without context).

## HEART Framework (Google)

Google's HEART framework maps product goals to signals to metrics across five dimensions: **Happiness** (CSAT, NPS, SUS), **Engagement** (DAU/MAU, feature adoption), **Adoption** (activation, time to first value), **Retention** (churn, return rate), and **Task Success** (completion, time on task, errors).

### Goals-Signals-Metrics Process

For each product area, work through three columns:

1. **Goal:** What is the desired user outcome? ("Users can find relevant products quickly")
2. **Signal:** What user behavior indicates progress toward the goal? ("Users complete searches and click results")
3. **Metric:** How do you quantify the signal? ("Search-to-click rate, average time from search to product page view")

This process prevents metric selection from being arbitrary. Every metric traces back to a user goal.

## System Usability Scale (SUS)

The most widely used standardized usability questionnaire. Ten questions on a five-point Likert scale, producing a score from 0-100.

### Scoring and Interpretation

- Raw score calculation: alternate positive/negative items, subtract/add from scale anchors, multiply by 2.5.
- Average SUS score across studies: 68 (this is the 50th percentile, not a passing grade).
- Adjective scale mapping: <50 = Awful, 50-67 = Poor to OK, 68 = Passable, 68-80 = Good, 80-90 = Excellent, 90+ = Best Imaginable.
- Grade scale: <60 = F, 60-69 = D, 70-79 = C, 80-89 = B, 90+ = A.
- Percentile benchmarks: 68 = 50th, 74 = 64th, 80 = 85th, 86 = 96th.

## Choosing an Instrument

- **SUS** (10 items): post-study, baselines, comparisons, longitudinal tracking. Perceived usability only; a thermometer, not a diagnosis.
- **UMUX-Lite** (2 items, r = 0.83 with SUS): in-app pulse checks where survey fatigue matters.
- **UEQ** (26 items, six dimensions): when hedonic qualities matter alongside pragmatic ones.
- **SUPR-Q**: web-only percentile rank against 200+ sites.
- **Task metrics** (success, time on task, errors, lostness) and **behavioral analytics** (funnels, cohorts, retention) for what users do; **A/B or sequential tests** to prove causation.

## AI-Specific UX Metrics

- **Trust calibration score:** How closely does user confidence in AI output match actual AI accuracy?
- **Appropriate reliance rate:** Percentage of times users correctly accept accurate AI outputs and correctly reject inaccurate ones.
- **AI feature adoption:** Opt-in rate, prompt frequency, feature retention over time.
- **Correction frequency:** How often users edit or override AI outputs.
- **Time saved:** Measured difference in task time with AI versus without.

## Routing

- **Choosing and scoring a framework** — HEART in depth, SUS scoring and limitations, UEQ, UMUX-Lite, SUPR-Q, task and behavioral metrics, NPS/CES/CSAT in a UX context, analytics metric design, experimentation (sample size and MDE table, significance, duration, peeking and multiple-comparison errors, Bayesian vs frequentist, sequential testing, guardrails) and benchmarking, UX ROI, design system metrics and ROI, maturity models, dashboards: read `references/metrics-frameworks-compendium.md`.
- **Measuring an AI feature** — AI metric taxonomy, affective metrics, cross-platform measurement, experiments that survive non-determinism, continuous discovery, atomic research, AI experiment pitfalls: read `references/ai-ux-metrics-experimentation.md`.

## Cross-Referencing

- For heuristic evaluation methodology, reference `nng-ux-heuristics`.
- For research methodology, reference `ux-research-methods`.
- For AI-specific metrics detail, reference `ux-metrics-measurement/references/ai-ux-metrics-experimentation`.
- For design system metrics detail, reference `design-systems-architecture/references/governance-scaling`.
- For usability testing protocols that produce metrics, reference `ux-research-methods/references/research-protocols`.
- Design system maturity rubric and adoption thresholds: `design-systems-architecture`
- Hallucination rate and confidence calibration metrics: `agentic-ai-generative-ux`
- Notification effectiveness metrics: `performance-states-patterns`

## Key Sources

- Google HEART Framework (Rodden, Hutchinson, Fu)
- Sauro, J. & Lewis, J.: "Quantifying the User Experience"
- MeasuringU: 48 UX Metrics (2025)
- Brooke, J.: SUS — A Quick and Dirty Usability Scale
- Schrepp, M.: User Experience Questionnaire (UEQ)
- Frontiers in Computer Science: UX Measurement Frameworks
- Sparkbox: Design System ROI Research
- NNG Group: UX Maturity Model, DesignOps 101
