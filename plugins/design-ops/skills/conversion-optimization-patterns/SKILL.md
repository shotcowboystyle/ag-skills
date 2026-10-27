---
name: conversion-optimization-patterns
description: "Evidence-based conversion patterns: CTA design, pricing page psychology, form and checkout friction, trust signals, social proof placement, urgency, and funnel analysis. Use when asking why people are not finishing a flow, or optimizing signup, cart, or pricing for completion."
allowed-tools: Read, Grep, Glob
---

# Conversion Optimization Patterns

## Purpose

Apply behavioral psychology and cognitive science to help users complete actions they already want to take. Ethical optimization removes friction from desired behavior; dark patterns manufacture behavior the user never intended. Where evidence is ambiguous or context-dependent, say so.

## Core rules

- **Diagnose with B = MAP (Fogg).** Behavior happens when Motivation, Ability and a Prompt converge. Clear CTA but low conversion: look at motivation or ability, not the prompt. Users start but don't finish: ability drops mid-flow. Users finish but don't return: motivation was inflated by urgency.
- **Value first (MECLABS: C = 4M + 3V + 2(I − F) − 2A).** No CTA test fixes a weak value proposition. Friction reduction has diminishing returns; anxiety reduction (trust signals, guarantees, security) is as important and often overlooked.
- **Choice architecture is unavoidable.** Defaults should match what an informed user would choose. Prefer 3-4 pricing tiers with a recommended option. Anchors must be real.
- **Use biases honestly.** Loss aversion, endowment, social proof (specific, recent, similar), scarcity (only if real), commitment (easy asks first), the IKEA effect, and peak-end (invest in success and error moments).
- **Track micro- and macro-conversions.** Where they diverge, you find the problem: pricing visits without signups suggests pricing or trust; signups without activation suggests onboarding; activation without payment suggests value demonstration.
- **Never optimize the aggregate.** Segment by source, device, new vs. returning, geography, intent, and persona. Watch RPV, LTV:CAC, activation and time-to-value as well as conversion rate.
- **Test properly.** For how to run and analyze a test (sample size, MDE, peeking, significance), use `ux-metrics-measurement`.
- **Follow the loop:** quantitative analysis → qualitative research → hypothesis ("Because we observed [data], we believe [change] will cause [outcome], measured by [metric]") → ICE/PIE prioritization → test → iterate. Record losing tests too.

## Ethics: the bright line

Help users do what they already want; never manufacture actions. Hidden costs, pre-checked opt-outs, fake countdown timers, roach-motel cancellation, confirmshaming, disguised ads, forced continuity and misdirection are out, and regulators (FTC, EU DSA, CCPA) increasingly enforce against them. Before shipping any pattern, ask:

1. Would the user thank me for this if they understood exactly what it does?
2. Would I be comfortable if a journalist described this pattern in a news article about my product?
3. Does this pattern work equally well for the user and the business, or only for the business?
4. Would removing this pattern cause users to make different decisions — and would those different decisions actually be better for them?

If any answer gives you pause, redesign the pattern.

## Routing

| Question | Read |
| --- | --- |
| Cialdini, Fogg, MECLABS, choice architecture, anchoring, cognitive biases in depth | `references/conversion-psychology.md` |
| Micro/macro conversions, metrics, segmentation, the six-step process (hypothesis, ICE/PIE), ethics examples | `references/measurement-and-testing.md` |
| CTAs: copy psychology, conversion CTA lists, color/size/placement, sticky bars, personalization, A/B case studies | `references/cta-optimization.md` |
| Pricing pages: anchoring, decoys, tier design, feature matrices, freemium, layouts | `references/pricing-page-psychology.md` |
| Forms as the drop-off point: field reduction, progressive disclosure, multi-step, validation, mobile | `references/form-conversion.md` |
| The funnel: AIDA/AARRR, landing pages, checkout, cart abandonment, retention, attribution | `references/funnel-optimization.md` |
| Trust: signal taxonomy, testimonials, ratings and reviews, security, guarantees | `references/trust-persuasion-patterns.md` |

For general button labels and error/success message copy, use `micro-copy-intelligence`.

Every figure in these files is unverified. Conversion
statistics are the most-copied and least-sourced numbers in the industry, and
this skill's output influences revenue decisions. Use the patterns; do not quote
the numbers to a client until they are checked.

## Cross-References

- **cognitive-psychology-ux**: Deep coverage of Laws of UX, cognitive biases, and mental models that underpin conversion behavior
- **ux-metrics-measurement**: owner of experiment statistics and methodology (sample size, significance, peeking, Bayesian vs frequentist); this skill decides what to test
- **ui-pattern-intelligence**: 190+ UI patterns including form, pricing, and checkout component patterns with implementation guidance
- **screen-flow-patterns**: User flow design including signup, onboarding, and checkout flow architecture
- **ux-ethics-content-strategy**: Detailed coverage of dark pattern taxonomy and ethical design frameworks
- **ux-research-methods**: User research methods for qualitative conversion research (usability testing, surveys, interviews)
- **performance-states-patterns**: Loading states, skeleton screens, and performance optimization that directly impacts conversion rates
- **accessibility-inclusive-design**: Accessible conversion flows reach the roughly 16% of people worldwide living with significant disability (WHO, 2023)
- **form-design-encyclopedia**: Detailed form patterns, input types, and validation strategies
- **micro-copy-intelligence**: owner of button-label templates and error/success message copy; use it for UI copy, and this skill's CTA lists only for conversion-specific contexts
- **layout-block-intelligence**: CTA, pricing, and testimonial block patterns
