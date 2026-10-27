---
name: cognitive-psychology-ux
description: Laws of UX (Fitts, Hick, Miller, Jakob, Peak-End, Doherty), Gestalt principles, cognitive biases, mental models, attention, and memory constraints. Use when auditing cognitive load, sizing tap targets, reducing choice overload, fixing decision fatigue, or grounding a design decision in research.
allowed-tools: Read, Grep, Glob
---

# Cognitive Psychology for UX Design

Interfaces fail when they exceed how human cognition works: overloaded working memory, recall where recognition was possible, choice paralysis. Use this skill to predict where load spikes, attention drifts, or a bias nudges behavior, and to ground design decisions in evidence.

## Core Laws of UX

- **Hick's Law:** decision time grows logarithmically with the number of choices. Use progressive disclosure.
- **Fitts's Law:** time to acquire a target depends on distance and size. Make primary actions large and near the user's focus; mobile tap targets at least 44x44 pt.
- **Miller's Law:** working memory holds roughly 7 plus or minus 2 chunks (Cowan: about 4 for novel information). Chunk related items; this is not a rule to group in sevens.
- **Jakob's Law:** users expect your product to work like the ones they already use. Innovate on your core value, not on conventions.
- **Gestalt principles** (proximity, similarity, closure, continuity, common region, figure-ground, uniform connectedness, Pragnanz) decide what users perceive as related before they read anything.
- **Peak-End Rule:** experiences are judged by their most intense moment and their ending. Design peaks and endings deliberately.
- **Doherty Threshold:** responses under 400 ms keep users in flow; above it, attention fragments.

## Working Rules

- **Mental models:** close the gap between the user model and the system model. Use familiar metaphors, immediate feedback, progressive disclosure, and error messages that correct the model. Surface mismatches with first-click tests and think-aloud.
- **Cognitive load (Sweller):** eliminate extraneous load (confusing navigation, inconsistent terms, hidden controls, gratuitous animation), manage intrinsic load by decomposing tasks, and invest in germane load through consistency. Overload shows up as step abandonment, longer time-on-task without accuracy gains, and errors at dense points.
- **Attention:** put critical information inside the task's visual flow (banner blindness, inattentional blindness), protect the primary task from interruptions and autoplay, and chunk long tasks with progress indicators to counter the vigilance decrement.
- **Memory:** prefer recognition over recall (autocomplete, visible options), chunk data (4-4-4-4 card numbers, labeled dashboard groups), and place the most important items first and last (serial position).
- **Decisions:** users satisfice, so curate fewer options unless they are exploring, use smart defaults that serve the user rather than exploit default bias, and put consequential decisions early before decision fatigue sets in.

## Routing

- **Mental models, cognitive load theory, attention modes, memory, decision-making** in full, with research citations: `references/cognitive-foundations.md`.
- **25+ laws** with formulas, code examples, and anti-patterns (including Gestalt, serial position, Zeigarnik, Tesler): `references/laws-of-ux-encyclopedia.md`.
- **Cognitive bias catalog** with ethical and dark-pattern annotations, bias audit framework: `references/cognitive-biases-design-patterns.md`.
- **Visual scanning, eye tracking, attention economics, cognitive load measurement, flow state, emotional design, cognitive budget:** `references/neurodesign-engagement-science.md`.

## Cross-References to Other Skills

- **nng-ux-heuristics**: Nielsen's 10 heuristics are applied cognitive psychology. H6 (Recognition over Recall), H8 (Aesthetic and Minimalist Design reducing extraneous load), and H5 (Error Prevention through mental model alignment) all map directly to concepts in this module.
- **accessibility-inclusive-design**: Cognitive accessibility — designing for ADHD, dyslexia, autism spectrum, and age-related cognitive decline — requires deep understanding of attention, memory, and processing speed variability.
- **interaction-motion-design**: Motion is an attention-direction tool. Easing curves map to expectation (mental models of physics). Animation duration thresholds relate to the Doherty Threshold and perceptual timing.
- **design-systems-architecture**: Consistent design tokens and component APIs create the predictability that supports schema formation (germane load) and reduces learning cost (Jakob's Law).
- **ux-ethics-content-strategy**: Dark patterns are cognitive bias exploits. Understanding the bias is the prerequisite for recognizing and refusing to implement its exploitation.
- **ai-spatial-voice-ux**: Conversational and spatial interfaces introduce novel cognitive challenges — working memory demands of voice, spatial navigation mental models, and attention management in 3D environments.
