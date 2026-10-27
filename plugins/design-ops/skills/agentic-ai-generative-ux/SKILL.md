---
name: agentic-ai-generative-ux
description: "Design patterns for agentic AI: multi-agent orchestration UX, generative UI, RAG interfaces, LLM hallucination guardrails, confidence indicators, and trust calibration. Use when designing AI copilots or autonomous agents, adding verification affordances, or auditing an AI feature for safety, control, and consent."
allowed-tools: Read, Grep, Glob
---

# Agentic AI & Generative UX

## The Paradigm Shift: Tools to Agents

Agentic AI acts on the user's behalf: it infers goals, executes multi-step plans, and reports results. The user shifts from operator to supervisor, delegator, and collaborator.

### Three Interface Eras

1. **Tool Era (pre-2023):** User drives every action. Software responds to explicit commands. Interfaces optimized for direct manipulation.
2. **Copilot Era (2023-2025):** AI assists within existing workflows. User remains in control. AI suggests, user accepts or rejects. Chat sidebars, inline completions, smart suggestions.
3. **Agent Era (2025+):** AI executes entire workflows autonomously. User sets goals, defines constraints, and monitors outcomes. Interfaces optimized for delegation, oversight, and trust calibration.

The three eras coexist. Not every task needs an agent. The designer's job is to match the right interaction model to the right task and user context.

## Intent Modeling UX

Agentic systems must infer user goals rather than waiting for explicit commands. This creates a new design challenge: intent resolution.

### Intent Signals

- **Explicit intent:** User types a goal in natural language ("Book me a flight to Tokyo next week under $800").
- **Contextual intent:** System infers from behavior, history, calendar, and environment (user opens travel app on Friday → likely planning weekend trip).
- **Ambient intent:** Background signals from connected systems (calendar shows conference in Tokyo → proactively suggest flights).

### Design Principles for Intent

- Always confirm inferred intent before acting on high-stakes tasks. "It looks like you're planning a trip to Tokyo. Want me to find flights?" is safer than silently booking.
- Display the interpreted intent visibly so users can correct misunderstanding. Show "I understood: round-trip flight, Tokyo, March 15-22, under $800" before execution.
- Provide progressive autonomy — start with confirmation-required mode, let users opt into higher autonomy as trust builds.
- Support intent refinement through conversation. The first statement rarely captures the full goal. Design for iterative clarification without friction.

## Constraint and Policy Design

What an agent cannot do is as important as what it can do. Constraint design is a first-class UX discipline for agentic systems.

### Constraint Taxonomy

- **Hard constraints (non-negotiable):** Security boundaries, legal compliance, data access limits. The agent cannot override these regardless of user request.
- **Soft constraints (user-configurable):** Budget limits, time preferences, quality thresholds, communication style. Users set and adjust these.
- **Contextual constraints (system-inferred):** Derived from user role, organization policies, or current task context. May be overridden with appropriate authorization.

### Constraint UX Patterns

- Present constraints as "guardrails" that protect the user, not limitations that restrict them. Frame positively: "I'll keep your spending under $200" not "I cannot exceed $200."
- Make constraint boundaries visible before the agent encounters them. Show the operating envelope upfront.
- When the agent hits a constraint, explain clearly: what it tried to do, which constraint blocked it, and how the user can adjust if they want to.
- Provide a constraint dashboard where power users can view and configure all agent boundaries in one place.

## AI Safety UX and Guardrail Design

### Trust Calibration

Trust is the central design challenge for AI interfaces. The goal is calibrated trust — users trust the AI exactly as much as its actual reliability warrants. Over-trust leads to unverified acceptance of errors. Under-trust leads to wasted verification effort and eventual abandonment.

### Guardrail Tiers

- **Tier 1 — Informational:** Agent acts autonomously, logs actions for optional review. For low-risk, reversible actions.
- **Tier 2 — Advisory:** Agent proposes action and explains reasoning, user approves or modifies. For medium-risk actions.
- **Tier 3 — Mandatory:** Agent cannot proceed without explicit user approval. For high-risk, irreversible, or financially significant actions.

Map every agent capability to a guardrail tier based on risk and reversibility.

## AI UX Anti-Patterns

Avoid AI fatigue: no AI where a deterministic workflow or direct manipulation is faster, and no "AI-powered" badges as marketing.

### When NOT to Use AI

AI is not always the answer. Prefer direct manipulation for: binary choices, simple CRUD operations, well-defined form fills, single-click actions, and tasks where user preference is clear. AI adds value for: ambiguous goals, complex multi-step workflows, pattern recognition at scale, personalization, and creative assistance.

## Routing

- **Trust and safety** — trust calibration, confidence visualization, uncertainty display, explainable AI, guardrail framework, risk-tiered approval, guardrail configuration UI, AI literacy, progressive autonomy levels, limitations disclosure, opt-out: `references/ai-safety-trust-guardrails.md`.
- **Multi-agent systems** — background task patterns, monitoring dashboards, coordination, agent identity and handoff, agent memory UX, platform copilot guidelines, task delegation, supervised/autonomous modes: `references/agentic-multi-agent-patterns.md`.
- **Generative UI and RAG** — the three UI paradigms, outcome-oriented design, design-system integration, citation design, knowledge freshness, image-generation UX, multimodal output, intent-generated forms and dashboards: `references/generative-ui-rag-patterns.md`.
- **Interface archetypes** and AI fatigue; copilot patterns (inline suggestions, AI sidebar, command palette, form extraction): `references/ai-interface-archetypes.md`.
- **Hallucination guardrails** — taxonomy, confidence indicators, verification UX, quality gates: `references/llm-hallucination-design-guardrails.md`.
- **Conversational dialogue** — state machines, turn-taking, streaming UX, context drawer, persona selection, model/quota status, memory transparency, prompt augmentation: `references/conversational-ai-dialogue-patterns.md`.

## Cross-Referencing

- Voice interaction mechanics, spatial and multimodal AI surfaces: `ai-spatial-voice-ux`.
- For AI content quality and ethics, reference `ux-ethics-content-strategy`.
- For AI feature accessibility, reference `accessibility-inclusive-design`.
- For AI metrics and measurement, reference `ux-metrics-measurement`.
- For design system integration with generative UI, reference `design-systems-architecture`.
- Proactive AI in ambient, screenless contexts: `ambient-calm-zero-ui`

## Key Sources

- Gartner Top Strategic Technology Trends 2025 (Agentic AI)
- NNG Group: Generative UI, Outcome-Oriented Design, State of UX 2026, AI Literacy
- Microsoft Design: UX Design for Agents, Copilot Framework
- Google A2UI: Agent-to-UI Interoperability Format
- OpenAI Apps SDK Design System
- World Economic Forum: Multi-Agent AI UX
- Arxiv: Agentic AI Design Workflows, Survey of GenAI UI Design
- ACM CHI 2025: Designing UIs with AI Workshop
