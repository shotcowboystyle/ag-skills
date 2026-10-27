---
name: ambient-calm-zero-ui
description: Calm technology principles, zero-UI and screenless patterns, ambient displays, proactive intelligence, and peripheral attention design. Use when designing smart home, automotive, wearable, or background-intelligence experiences, or reducing notification and attention load.
allowed-tools: Read, Grep, Glob
---

# Ambient Computing & Calm Technology — Designing the Invisible Interface

## Purpose

Design technology that attends to people instead of demanding their attention: move information from the center of attention to the periphery and the background. As Weiser and Brown put it, "The most profound technologies are those that disappear." Use this skill to judge whether a system is calm, design ambient and screenless interactions, audit attention cost, and handle the privacy obligations of always-on sensing.

## Core rules

- **Minimum attention.** Deliver value with the least focal attention possible. Complexity is acceptable (a cockpit is complex but built for peripheral scanning); unnecessary demand on focal attention is not.
- **Place information on the attention spectrum.** Background (automated, zero attention) → periphery (status, trends, binary states) → center (only for conscious decisions). Escalate one zone at a time and only on anomaly or when the user must act. Design the transitions as carefully as the states.
- **Pick the channel by context.** Proactive notifications (timely, actionable, infrequent), ambient displays (light, e-ink, physical change), voice (about three options before working memory fails), gesture (solve discoverability and false positives), haptics (few distinguishable patterns, but private).
- **Context sets the constraint.** Smart home: multi-user conflicts, guest mode, offline degradation. Office: personalization vs. shared space and employer monitoring. Automotive: nothing that takes eyes off the road; touchscreens for driving functions are an anti-pattern. Wearables: under two seconds to glance. Public space: no training, no account, accessibility is the baseline.
- **Resolve the discoverability paradox.** Invisible by default, transparent on demand ("why did you do that?"), configurable when desired.
- **Privacy is architectural.** Hardware listening/camera indicators that software cannot override, physical shutters, real opt-out, local processing, data minimization, raw sensor data discarded. Design for the most privacy-sensitive person in the household; conservative defaults, expanded capability opt-in; never infer consent from convenience.
- **Fail gracefully.** The system must still work, or degrade safely, when it or the network fails.
- **Measure attention, not clicks.** Use the Calm Technology Scorecard (eight principles, violates → exemplifies), the Attention Budget Audit (sum focal/peripheral/background demand per day), and ambient adaptations of Nielsen's heuristics.

## Routing

| Question | Read |
| --- | --- |
| Full prose on the attention spectrum, zero-UI patterns, ambient contexts, discoverability, privacy, evaluation | `references/ambient-overview.md` |
| Amber Case's eight principles with modern examples | `references/calm-technology-principles.md` §1 |
| Ambient display patterns (always-on, e-ink, LED, light, soundscapes) | `references/calm-technology-principles.md` §2 |
| Proactive intelligence, anticipatory design | `references/calm-technology-principles.md` §3 |
| Smart home, office, automotive, retail, healthcare | `references/calm-technology-principles.md` §4 |
| Privacy patterns, transparency indicators | `references/calm-technology-principles.md` §5 |
| Glanceability and status-at-a-glance | `references/calm-technology-principles.md` §6 |
| Scorecard, attention budget audit, ambient heuristics | `references/calm-technology-principles.md` §7 |
| Anti-patterns (surveillance, over-automation, the creepy line) | `references/calm-technology-principles.md` §8 |

## Cross-References to Other Skills

- **spatial-voice-ux**: Voice interaction is a primary modality for zero-UI systems. Spatial audio is a key ambient communication channel.
- **interaction-motion-design**: Motion and animation serve as peripheral communication channels. Micro-interactions provide feedback in ambient displays. Gesture design is fundamental to screenless interaction.
- **accessibility-inclusive-design**: Ambient interfaces must serve users with visual, auditory, motor, and cognitive differences. Multi-sensory communication (visual + auditory + haptic) is both an ambient design principle and an accessibility requirement. Universal design and calm design share the same goal: technology that works for everyone without demanding special effort.
- **agentic-ai-generative-ux**: AI agents that act autonomously face the same discoverability and trust challenges as ambient systems. Transparency patterns, approval gates, and progressive autonomy models apply to both domains.
- **cognitive-psychology-ux**: The attention spectrum, working memory limitations, peripheral perception, and the science of interruption all provide the cognitive foundation for calm technology design.
- Ethics of data collection and consent: `ux-ethics-content-strategy`
