# NNG Design Thinking — Six Phases and Design Ops Mapping

Moved verbatim from the `design-process-methods` SKILL.md.

## NNG Design Thinking — The 6-Phase Framework

Nielsen Norman Group's design thinking model is the most widely-validated UX process. It organizes into three macro stages:

### Macro Stage 1: UNDERSTAND (Empathize + Define)

The stage most vibe coders skip entirely. You cannot design what you do not understand.

#### Phase 1: Empathize

**Goal**: Understand users' needs, pain points, and context through direct observation and engagement.

**Methods**:

- **Contextual inquiry** — Observe users in their natural environment performing real tasks
- **User interviews** — Semi-structured conversations focusing on behaviors, not opinions
- **Diary studies** — Longitudinal capture of experiences over days or weeks
- **Empathy mapping** — Synthesize what users Say, Think, Do, and Feel
- **Stakeholder interviews** — Understand business constraints, technical limitations, and organizational goals

**Key principle**: Empathy is not sympathy. It's not "feeling sorry for users." It's understanding their mental models, frustrations, and workarounds deeply enough to design for their actual reality.

**In terminal workflow**: Before prompting any AI to generate UI, spend 2 minutes answering:

- Who will use this? (Not "users" — a specific person with a specific job)
- What are they trying to accomplish? (Task, not feature)
- What's their current workaround? (They're solving this somehow today)
- What frustrates them about the current solution?
- What environment are they in? (Mobile on a train? Desktop in an office? Accessibility needs?)

**Design Ops mapping**: `/brief` (0.2) captures this as a structured problem statement.

#### Phase 2: Define

**Goal**: Synthesize empathy findings into a clear, actionable problem statement.

**Methods**:

- **Problem statement** — "Users who [X] need [Y] because [Z]"
- **How Might We questions** — Reframe problems as opportunities ("HMW make checkout feel instant?")
- **Personas** — Behavioral archetypes (not demographic stereotypes)
- **Jobs to Be Done** — Functional, emotional, and social jobs the product fulfills
- **User stories** — "As a [persona], I want [action] so that [outcome]"
- **Success criteria** — Measurable outcomes that define "done" (functional, usability, accessibility, business)

**Key principle**: A well-defined problem is half-solved. Most design failures trace to building the right solution to the wrong problem.

**In terminal workflow**: Write a single sentence: "Users who [X] need [Y] because [Z]." If you can't fill this in, you haven't empathized enough.

**Design Ops mapping**: `/brief` (0.2) generates the problem statement, persona, HMW questions, and success criteria.

### Macro Stage 2: EXPLORE (Ideate + Prototype)

Generate and test multiple solutions before committing.

#### Phase 3: Ideate

**Goal**: Generate a breadth of possible solutions without premature commitment.

**Methods**:

- **Brainstorming** — Quantity over quality, defer judgment, build on others' ideas
- **Crazy 8s** — 8 ideas in 8 minutes, forces divergent thinking
- **How Might We** — Each HMW question generates 3-5 potential solutions
- **Competitive analysis** — Study how others solve the same problem (not to copy — to understand the solution space)
- **Design patterns** — Known solutions to known problems (Design Ops' screen-flow-patterns catalog)
- **Sketching** — Low-fidelity exploration before any code or AI generation

**Key principle**: The first idea is almost never the best idea. Diverge before you converge.

**In terminal workflow**: Before prompting AI to generate a component, list 3 different approaches. Even 30 seconds of divergent thinking improves outcomes.

**Design Ops mapping**: `/style` (1.2) finds patterns; `/benchmark` (1.3) reveals competitive approaches; `/style` (1.1) establishes style direction.

#### Phase 4: Prototype

**Goal**: Build quick, disposable representations to test ideas — not ship-ready code.

**Methods**:

- **Paper prototypes** — Sketch on paper, test with users pointing at elements
- **Wireframes** — Low-fidelity digital layouts showing structure without style
- **Interactive prototypes** — Clickable mockups (Figma, code) testing specific flows
- **Wizard of Oz** — Human simulates AI/backend behavior to test the interface layer
- **A/B prototypes** — Build 2 versions of a critical interaction to test with users

**Key principle**: Prototypes are questions, not answers. Build them to learn, then throw them away.

**In terminal workflow**: Use AI to rapidly generate 2-3 variations of a component or screen. Treat these as prototypes to evaluate, not production code.

**Design Ops mapping**: `/screen` (4.2) and `/component` (4.3) generate prototypes; `/tokens` (4.1) establishes the design foundation.

### Macro Stage 3: MATERIALIZE (Test + Implement)

Validate with real users and ship with confidence.

#### Phase 5: Test

**Goal**: Evaluate prototypes with real users to identify problems before shipping.

**Methods**:

- **Usability testing** — 5 users, think-aloud protocol, task-based scenarios
- **Heuristic evaluation** — Expert review against Nielsen's 10 heuristics
- **Cognitive walkthrough** — Step through tasks from the user's perspective, checking learnability
- **A/B testing** — Statistical comparison of design variants with real traffic
- **Accessibility audit** — WCAG 2.2 compliance, screen reader testing, keyboard navigation
- **Analytics review** — Behavioral data revealing where users struggle

**Key principle**: Testing is not validation — it's learning. The goal is to find problems, not prove your design works.

**In terminal workflow**: After AI generates UI, run Design Ops audits before deploying. Each audit simulates expert evaluation.

**Design Ops mapping**: `/audit` (2.1) heuristic evaluation; `/audit` (2.2) cognitive audit; `/a11y` (2.3) accessibility; `/audit` (2.4) journey audit; `/audit` (3.1) ethics; `/roast` (5.1) critique; `/grade` (5.3) comprehensive review.

#### Phase 6: Implement

**Goal**: Ship the validated design with production quality, accessibility, and performance.

**Methods**:

- **Design system consumption** — Build with tokens, not magic numbers
- **Component library** — Reusable, tested, accessible components
- **Progressive enhancement** — Core functionality works without JavaScript
- **Performance budgets** — Time-to-interactive targets, bundle size limits
- **Monitoring** — Post-launch metrics tracking against success criteria

**Key principle**: Implementation is not "coding the design." It's translating design intent into technical reality while preserving every UX decision.

**In terminal workflow**: Use Design Ops BUILD commands with full context from earlier phases.

**Design Ops mapping**: `/tokens` (4.1) tokens; `/screen` (4.2) screens; `/component` (4.3) components; `/onboard` (4.4) onboarding; `/figma` (4.5) Figma pipeline.

---

## The Understand → Explore → Materialize Framework

NNG's three macro stages create a memorable mental model:

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   UNDERSTAND    │     │     EXPLORE      │     │   MATERIALIZE   │
│                 │     │                  │     │                 │
│  Empathize      │ ──► │  Ideate          │ ──► │  Test           │
│  Define         │     │  Prototype       │     │  Implement      │
│                 │     │                  │     │                 │
│  "Know the      │     │  "Generate       │     │  "Validate and  │
│   problem"      │     │   solutions"     │     │   ship"         │
└─────────────────┘     └─────────────────┘     └─────────────────┘

Design Ops Phase 0: GROUND    Design Ops Phases 1-3         Design Ops Phases 4-5
+ Phase 1: DISCOVER      DISCOVER, DIAGNOSE,     BUILD, LAUNCH
                          FORTIFY
```

### How Design Ops' 6 Phases Map to NNG

| NNG Phase | NNG Stage   | Design Ops Phase                                       | Design Ops Commands                                                              |
| --------- | ----------- | ------------------------------------------------------ | -------------------------------------------------------------------------------- |
| Empathize | Understand  | Phase 0: GROUND                                        | `/design-ops` (0.1), `/brief` (0.2)                                              |
| Define    | Understand  | Phase 0: GROUND                                        | `/brief` (0.2)                                                                   |
| Ideate    | Explore     | Phase 1: DISCOVER                                      | `/style` (1.1), `/style` (1.2), `/benchmark` (1.3), `/research` (1.4)            |
| Prototype | Explore     | Phase 4: BUILD                                         | `/tokens` (4.1), `/screen` (4.2), `/component` (4.3)                             |
| Test      | Materialize | Phase 2: DIAGNOSE + Phase 3: FORTIFY + Phase 5: LAUNCH | `/audit`, `/audit`, `/a11y`, `/audit`, `/audit`, `/ai-audit`, `/roast`, `/grade` |
| Implement | Materialize | Phase 4: BUILD                                         | `/component` (4.3), `/onboard` (4.4), `/figma` (4.5)                             |

Note: Design Ops' phases don't map 1:1 to NNG because Design Ops is iterative — you may prototype (BUILD) before you test (DIAGNOSE), then loop back. The NNG framework provides the _thinking_, Design Ops provides the _doing_.

---

## Process-to-Design-Ops Command Mapping

The mapping from NNG's process phases to the commands that serve them:

```
NNG UNDERSTAND ─────────────────────────────────────────────────
  Empathize        → /brief      Problem, persona, HMW questions
                   → /research   Interviews, surveys, usability tests
  Define           → /brief      Success criteria + constraint stack
                   → /map        Information architecture

NNG EXPLORE ────────────────────────────────────────────────────
  Ideate           → /style      Visual direction for the sector
                   → /benchmark  Competitive scorecard and gaps
                   → /measure    Metrics plan, before anything is built
  Prototype        → /wireframe  Low-fidelity structure
                   → /tokens     Token system
                   → /screen     Screen compositions
                   → /component  Component prototypes

NNG MATERIALIZE ────────────────────────────────────────────────
  Test             → /audit      Heuristics, cognitive load, flow, ethics
                   → /a11y       WCAG 2.2 accessibility audit
                   → /ai-audit   AI trust, control, recovery
                   → /responsive Cross-device behaviour
                   → /roast      Fast critique
                   → /grade      Design Quality Score
  Implement        → /component  Production components
                   → /page       Full page compositions
                   → /onboard    Onboarding flows
                   → /figma      Figma design-to-code pipeline
                   → /remix      Evidence-based redesign
                   → /preflight  Pre-launch and post-launch plan
```

Not every phase needs every command. `/start` routes to the right pipeline
without you choosing from this list.
