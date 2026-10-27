---
name: spatial-voice-ux
description: Spatial computing (AR/VR/MR), voice interaction, and multimodal input design. Use when designing headset or mixed-reality UI, a voice-first or voice-assistant flow, or combining speech, gaze, gesture, and touch input.
allowed-tools: Read, Grep, Glob
---

# Spatial, Voice & Multimodal UX

AI chat, LLM dialogue, AI output, copilots, agents, and generative UI live in `agentic-ai-generative-ux`. This skill owns spatial, voice, and multimodal interaction mechanics; for an AI voice assistant, design the voice mechanics here and the conversational/LLM dialogue there.

## Spatial Computing UX (AR/VR/MR)

### Spatial Design Principles

1. **Respect physical space** — digital elements must coexist naturally with the physical environment
2. **Spatial hierarchy** — distance from user communicates importance (near = primary, far = peripheral)
3. **Comfort first** — never cause disorientation, nausea, or visual strain
4. **Body-aware interaction** — design for natural human posture, reach, and movement
5. **Environment-adaptive** — interfaces must respond to lighting, surfaces, and obstacles

Key numbers: AR text 1.5-2x screen sizes; VR text at least 1.5 degrees of visual angle; primary VR content 1-2 m away, slightly below eye level; comfortable eye sweep +/-30 degrees horizontal, +20 to -40 degrees vertical; never tilt the horizon; offer teleportation and FOV tunneling for movement.

## Voice Interface Design

### Voice UX Principles

1. **Be conversational** — match natural speech patterns, not command-line syntax
2. **Keep it brief** — voice responses must be shorter than visual text equivalents
3. **Confirm ambiguity** — repeat back unclear inputs for confirmation
4. **Provide escape hatches** — "cancel", "go back", "start over" must always work
5. **Progressive disclosure via voice** — offer summaries with option to hear details

Key rules: at most 3 options per voice menu; show a listening indicator; support barge-in; never answer with silence; after 2-3 recognition failures, offer another input method or a human.

## Multimodal Interaction Design

### The Multimodal Stack (2025-2030)
- **Touch + Voice:** Common on phones and smart displays
- **Gaze + Hand + Voice:** Spatial computing (Vision Pro, Quest)
- **Keyboard + Mouse + AI:** Desktop productivity
- **Gesture + Voice + Touch:** Automotive and kiosk interfaces
- **Brain-Computer Interface (emerging):** Assistive tech, early consumer exploration

### Multimodal Design Rules
- Each modality should be self-sufficient for critical tasks — never require a specific modality
- Complement modalities: voice for command, visual for confirmation, haptic for feedback
- Resolve conflicts between simultaneous inputs gracefully (voice says "blue" while touching "red")
- Adapt interface emphasis based on active modality (larger touch targets when touch is primary)

## Design Patterns for Emerging Tech

### Ambient Computing
- Interfaces that appear when needed and disappear when not
- Context-aware: adapt based on time, location, activity, and user state
- Proactive suggestions without being intrusive — the design challenge of the decade
- Respect boundaries: ambient does not mean always-on surveillance

## Routing

- **Spatial, voice, and multimodal depth** — Apple Vision Pro and Meta Quest patterns, AR and VR interface patterns, spatial layout, voice interaction patterns and the voice deep dive, multimodal design, emerging paradigms through 2030: read `references/spatial-voice-multimodal.md`.

## Cross-Referencing

- For interaction and motion patterns, reference `interaction-motion-design`
- For accessibility in emerging platforms, reference `accessibility-inclusive-design`
- For design system adaptation to spatial platforms, reference `design-systems-architecture`
- AI chat, LLM dialogue, AI output, copilots, agents, generative UI: `agentic-ai-generative-ux`
- Calm technology and zero-UI ambient patterns: `ambient-calm-zero-ui`
- Working-memory limits on voice menus, split attention in multimodal input: `cognitive-psychology-ux`

## Key Sources

- Apple Vision Pro Human Interface Guidelines (2024)
- Meta Quest Design Guidelines
- Google Conversational Design Guidelines
