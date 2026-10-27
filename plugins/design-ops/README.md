# Design Ops Plugin

**Version:** 1.5.0

UX/UI design ops for coding agents: briefs, research, information architecture, visual
identity, design tokens, components, screens and pages, accessibility, and builds graded
against live Awwwards and Mobbin references.

A private customization of [Sumi](https://phazurlabs.com) 4.2.0 by Phazur Labs LLC. See
[Attribution](#attribution).

Version 1.3.0 absorbs the former `ui-design` plugin. Its Android/Compose, React Native,
and web-component skills and its three agents moved here; its accessibility, token,
responsive, interaction, visual-foundation and iOS skills, and its four commands, were
dropped in favour of the deeper equivalents below (`/a11y`, `/tokens`, `/component`,
`/audit`, and `ios-ops` for SwiftUI).

Version 1.5.0 gives each topic one owner. `ui-visual-design-system` merged into
`visual-design-mastery`, `web-component-design` into `component-patterns-code`,
microcopy lives in `micro-copy-intelligence`, Liquid Glass and Material 3 Expressive
in `platform-visual-standards`, the base motion tokens in `interaction-motion-design`,
experiment statistics in `ux-metrics-measurement`, AI chat and generative UI in
`agentic-ai-generative-ux`, and dashboards and data tables in `data-visualization-mastery`.

## Installation

Part of the [ag-skills](../../README.md) marketplace. In Claude Code:

```bash
/plugin marketplace add shotcowboystyle/ag-skills
/plugin install design-ops@claude-code-workflows
```

For Codex CLI, Cursor, OpenCode, Antigravity CLI, GitHub Copilot, and Pi, see
[docs/harnesses.md](../../docs/harnesses.md).

## Commands

- `/design-ops:a11y [file, component, or screen to audit]` — Accessibility audit — WCAG 2.2 AA full checklist, ARIA audit, keyboard navigation, color contrast (APCA), focus management, screen reader, cognitive a11y, with code fixes.
- `/design-ops:ai-audit [AI feature, file, or description]` — Audit AI-powered features against agentic, trust, safety, and interaction best practices with scoring and specific fix recommendations.
- `/design-ops:animate [element or interaction to animate]` — Generate production animations — CSS keyframes, Framer Motion, scroll-driven, micro-interactions, with reduced motion fallbacks.
- `/design-ops:audit [product, screen, or codebase] [optional: section]` — Comprehensive design audit — heuristic, cognitive, flow, fortification, cognitive load analysis, and summary scoring in one command. Run all lenses or pick specific sections.
- `/design-ops:before-after [file or component to compare]` — Before/after comparison — show exactly how AI-generated slop transforms into production-quality UI. Visual proof of every design improvement.
- `/design-ops:benchmark [product or competitor set]` — Competitive analysis — 10-dimension scorecard, gap analysis, improvement roadmap, and differentiation strategy.
- `/design-ops:brief [product or feature to define]` — Problem definition — persona, How Might We questions, constraints, success criteria, and a ready-to-paste Constraint Stack.
- `/design-ops:component [component name and requirements]` — Production component builder — generate complete, runnable UI components (30+ types) with 10 states, full accessibility, design tokens, animation, tests, and platform code (React/SwiftUI/CSS).
- `/design-ops:dark [existing palette or token file]` — Generate a complete dark mode system — oklch luminance mapping, surface elevation, accent adjustments, shadows, toggle component, and dark tokens.
- `/design-ops:design-ops [optional: command or topic]` — Command map and quick start — see all 39 commands, starter recipes, Design Quality Score, anti-slop engine, and tips for best results. Start with /start if you are new.
- `/design-ops:figma [Figma URL or design spec] [target platform]` — Generate production code from a Figma design specification using the MCP-powered design-to-code flywheel. Extracts tokens, components, and layout to produce platform-ready code.
- `/design-ops:fix [file, component, or directory to fix]` — Anti-slop engine — takes AI-generated UI code and transforms it into production-quality design. Fixes typography, color, spacing, accessibility, and design consistency in one pass.
- `/design-ops:form [form purpose and fields]` — Generate production forms — validation, error states, multi-step wizards, accessibility, complete React + Zod code.
- `/design-ops:generate [asset type and description]` — AI design generation — mockups, icons, illustrations, images via Stitch MCP, Fal.ai, Recraft V3, Veo 3.1
- `/design-ops:grade [design, screenshot, or file to score]` — Visual quality scoring — Awwwards-calibrated 10-dimension assessment, designer DNA match, canonical rule compliance, production quality verdict.
- `/design-ops:icon [icon set or product context]` — Generate an icon system — library selection, sizing tokens, React wrapper component, animated recipes, SVG optimization, and accessibility.
- `/design-ops:inspo [brief, flow, or URLs — e.g. "fintech landing, dark, editorial"]` — Source REAL references — live Awwwards winners, Mobbin screens and flows, MotionSites motion recipes — capture the sites, measure their design DNA, and build a Reference Board in .design-ops/refs/ that later commands design and grade against.
- `/design-ops:layout [page or section to lay out]` — Generate responsive page layouts — CSS Grid, Flexbox, container queries, spacing rhythm, breakpoint transformations.
- `/design-ops:map [product or content to structure]` — Information architecture — sitemap, navigation model, content hierarchy, cross-linking map, URL structure, and search strategy.
- `/design-ops:measure [product or feature to measure]` — Metrics plan — HEART framework, OKRs, experimentation strategy, dashboards, and baseline measurement.
- `/design-ops:nav [product and navigation type]` — Generate responsive navigation systems — top bar, sidebar, bottom tabs, command palette, mega menu, with ARIA and dark mode.
- `/design-ops:next [optional: current focus]` — Context-aware suggestion of what to do next based on what you've generated so far.
- `/design-ops:onboard [product and first-run goal]` — Generate a complete onboarding flow — step sequence, progressive disclosure, permission timing, empty states, activation metrics, and production React code.
- `/design-ops:page [page type and purpose]` — Full page builder — generate complete, runnable marketing and product pages with ordered block stacking, SEO, Open Graph, scroll animations, lazy loading, and responsive composition.
- `/design-ops:palette [brand, mood, or existing colors]` — Generate a deep color system — oklch palettes, APCA contrast scores, dark mode, data-viz colors, gradients, and CSS custom properties.
- `/design-ops:preflight [product or release to check]` — Pre-launch checklist and post-launch plan — SEO, performance, analytics, legal, security, monitoring, feedback loops, iteration strategy.
- `/design-ops:qa [implementation and design spec to compare]` — Design QA — verify implementation matches design spec. Token compliance, state coverage, responsive fidelity, accessibility, pixel-level issues.
- `/design-ops:remix [file, component, or screen to redesign]` — Redesign existing UI — fix top problems with UX reasoning for every change
- `/design-ops:research [research question or product area]` — User research and usability testing — interview guides, survey design, test plans, recruitment, and analysis frameworks.
- `/design-ops:responsive [screen, block, or component]` — Generate responsive behavior for any screen or component — breakpoints, container queries, fluid scaling, block transformations, and touch targets.
- `/design-ops:roast [design, screenshot, or file to critique]` — Quick brutal design critique — 10 dimensions scored, letter grade, top fixes, one-line verdict. Fast and opinionated.
- `/design-ops:screen [screen type and requirements]` — Production screen builder — generate complete, runnable React/TypeScript + Tailwind screens for 30+ screen types with all states, accessibility, responsive breakpoints, dark mode, and token consumption.
- `/design-ops:scroll [subject — product, brand, or place] [--continue | --stage N | --you-decide]` — Cinematic scroll site — interview, brand truth, live references, depth-plane plan, Kie AI assets, GSAP build, and frame-verified delivery graded against the board.
- `/design-ops:start [optional: describe what you are working on]` — Start here. Figures out what you need and routes you to the right Design Ops skills — no prior knowledge of the plugin required.
- `/design-ops:status [optional: project path]` — Progress dashboard — see what you've generated, what's available, and suggested next moves.
- `/design-ops:style [product, sector, or mood]` — Generate a complete visual identity — colors, typography, spacing, motion, tone, tokens, and reference apps for any sector or mood.
- `/design-ops:tokens [brand requirements or existing palette]` — Generate a complete W3C DTCG design token system — primitives, semantics, component tokens, multi-theme, with CSS/Tailwind/Style Dictionary output.
- `/design-ops:type [brand voice or existing fonts]` — Generate a complete typography system — font pairing, modular type scale with fluid clamp() values, line-height, letter-spacing, and platform stacks.
- `/design-ops:wireframe [screen or flow to wireframe]` — Generate low-fidelity ASCII wireframes with layout alternatives and interaction notes

## Skills

- **accessibility-inclusive-design** — WCAG 2.2 compliance, ARIA authoring patterns, screen reader and keyboard navigation, color contrast, and cognitive/neurodiversity accommodations. Use when auditing accessibility, fixing a11y violations, choosing ARIA roles, checking contrast ratios, or designing for ADHD, dyslexia, autism, or motor impairment.
- **agentic-ai-generative-ux** — Design patterns for agentic AI: multi-agent orchestration UX, generative UI, RAG interfaces, LLM hallucination guardrails, confidence indicators, and trust calibration. Use when designing AI copilots or autonomous agents, adding verification affordances, or auditing an AI feature for safety, control, and consent.
- **ai-design-generation** — Produce visual assets from AI image and UI models through MCP — Stitch screens, Fal.ai (Imagen, FLUX, Veo), Recraft V3 vectors, GPT-Image and Figma file access — with prompt patterns and quality scoring. Use when rendering mockups, icons, illustrations or video. Not for interface copy; not for agent UX.
- **ai-spatial-voice-ux** — Spatial computing (AR/VR/MR), voice interaction, and multimodal input design. Use when designing headset or mixed-reality UI, a voice-first or voice-assistant flow, or combining speech, gaze, gesture, and touch input.
- **ambient-calm-zero-ui** — Calm technology principles, zero-UI and screenless patterns, ambient displays, proactive intelligence, and peripheral attention design. Use when designing smart home, automotive, wearable, or background-intelligence experiences, or reducing notification and attention load.
- **animation-recipe-library** — 200+ copy-paste animation recipes in CSS, Framer Motion, and GSAP: entrances, micro-interactions, page transitions, scroll-driven effects, spring physics, and cursor and text effects, each with timing, easing, and a reduced-motion fallback. Use when you need working motion code rather than motion principles.
- **business-design-templates** — Client-facing design deliverables: proposals, SOWs, case studies, pitch decks, pricing calculators, project briefs, and handoff documentation. Use when packaging design work for a client, an executive, or a portfolio — the artifact that leaves the team, not the interface itself.
- **cognitive-psychology-ux** — Laws of UX (Fitts, Hick, Miller, Jakob, Peak-End, Doherty), Gestalt principles, cognitive biases, mental models, attention, and memory constraints. Use when auditing cognitive load, sizing tap targets, reducing choice overload, fixing decision fatigue, or grounding a design decision in research.
- **color-palette-library** — 180+ ready-made color palettes with contrast scores, plus OKLCH palette generation, dark-mode luminance mapping, semantic color architecture, and data-viz scales. Use when picking or generating a specific palette. For color theory and hierarchy craft, use visual-design-mastery.
- **component-patterns-code** — Production UI component code in React/TypeScript, Vue 3, Svelte 5, SwiftUI and modern CSS, with full state matrices, ARIA, keyboard handling and design tokens. Use when building or reviewing a component, designing a component API or composition pattern, or choosing a styling approach such as Tailwind, CSS Modules or CSS-in-JS.
- **conversion-optimization-patterns** — Evidence-based conversion patterns: CTA design, pricing page psychology, form and checkout friction, trust signals, social proof placement, urgency, and funnel analysis. Use when asking why people are not finishing a flow, or optimizing signup, cart, or pricing for completion.
- **cross-cultural-i18n-ux** — Internationalization and localization: RTL layouts with CSS logical properties, CJK typography, text expansion, locale-aware formatting, cultural color semantics, and Hofstede's dimensions applied to interfaces. Use when shipping to new markets, adding Arabic or Hebrew support, or pseudo-localization testing.
- **data-visualization-mastery** — 50+ chart types with selection criteria, dashboard composition, data tables, KPI cards, sparklines, heatmaps, and accessible data presentation, with React code (Recharts, D3, Nivo) and data-viz tokens. Use when designing charts, dashboards, or any data-dense screen.
- **design-critique-case-studies** — Structured design critique using the Liz Lerman Critical Response Process, plus deep-dives on Stripe, Linear, Notion, Airbnb, Figma, and Arc, and post-mortems of redesign failures like Snapchat 2018 and Sonos 2024. Use when running a critique session, giving design feedback, or learning from a shipped product.
- **design-memory** — The .design-ops/ design memory contract — which files exist, the canonical style.json schema, which command owns which subtree, read order, and merge rules. Use whenever a command reads or writes .design-ops/, or when design decisions from an earlier command must survive into a later one.
- **design-ops-orchestrator** — Routes any UX/UI request to the right Design Ops skills in the right order, with stage gates and handoffs. Use when the user asks where to start, what comes next, what the process is, or wants a full design engagement run end to end — and whenever a request is broad enough to need more than one skill (redesign, launch, audit, new product, design system).
- **design-process-methods** — Design process methodology: NNG's six phases, Double Diamond, Google Design Sprint, IDEO, Lean UX, and the bridge from AI-assisted building to evidence-based UX. Use when framing how the work should run, planning a sprint, or grounding a build in Empathize, Define, Ideate, Prototype, Test.
- **design-systems-architecture** — Design system architecture: W3C design tokens, Style Dictionary pipelines, component library structure, theming, multi-brand token tiers, governance, versioning, and maturity models. Use when starting or scaling a design system, generating tokens, or setting up design-to-code distribution.
- **design-token-presets** — 15 ready-to-deploy token systems by industry vertical, each in W3C DTCG JSON, CSS custom properties, and Tailwind v4 @theme, with Style Dictionary config and Figma Variables mapping. Use when you want a vetted starting token set. For architecting your own, use design-systems-architecture.
- **desktop-app-design** — Desktop and enterprise application chrome: windows and multi-pane layouts, menus and context menus, toolbars, sidebars and panels, keyboard shortcuts and command palettes, drag and drop, master-detail, complex forms and wizards, and OS conventions. Use when designing an admin panel or professional desktop tool. For dashboards, charts and data tables, use data-visualization-mastery.
- **figma-design-tool-workflows** — Figma mastery and design-to-code: Auto Layout, component architecture, variable modes, Dev Mode handoff, Figma MCP server integration, Code Connect, and token pipelines. Use when working in Figma, converting designs to code, or setting up a design-to-code flywheel.
- **form-design-encyclopedia** — Form patterns covering 50+ input types, 30+ layouts, validation strategies, multi-step wizards, and error states, with production React and CSS, accessibility requirements, and mobile optimization. Use when building or fixing a form, choosing a validation approach, or reducing abandonment on signup and checkout.
- **icon-illustration-systems** — Icon and illustration systems: grid and sizing scales, library selection (Lucide, Heroicons, Phosphor, SF Symbols, Material Symbols), illustration style guides, SVG optimization, and accessible iconography. Use when choosing an icon set, sizing icons, or establishing an illustration style.
- **image-media-patterns** — Image, video, and media UI patterns: hero and product imagery, galleries, carousels, video and audio players, avatars, thumbnails, aspect ratios, cropping, lazy loading, responsive images, and media accessibility. Use when placing media on a page or building a gallery or player.
- **interaction-motion-design** — Micro-interactions, animation timing and easing curves, spring physics, transition choreography, haptic feedback vocabularies, and emotional design. Use when adding or reviewing animation, tuning motion duration, designing haptics, or supporting prefers-reduced-motion.
- **layout-block-intelligence** — ~300 individual section patterns — heroes, feature grids, pricing tables, testimonials, CTAs, footers, FAQs, stats, timelines — each with specs, spacing, and code. Use when choosing or building one section. For ordering sections into a whole page, use page-composition-engine.
- **micro-copy-intelligence** — 1000+ microcopy and UX-writing templates by component, tone and sector: button labels, every error message and failure state, empty states, tooltips, confirmations, permission requests and notifications. Use when writing any interface string — robotic copy is the loudest slop tell.
- **mobile-android-design** — Master Material Design 3 and Jetpack Compose patterns for building native Android apps. Use when designing Android interfaces, implementing Compose UI, or following Google's Material Design guidelines.
- **mobile-ux-design** — Mobile-first design: touch targets, gesture systems, thumb zones, responsive layout, mobile forms and navigation, iOS 26 Liquid Glass, Material 3 Expressive, and wearable/IoT patterns. Use when designing or auditing an iOS, Android, or responsive mobile experience.
- **navigation-pattern-encyclopedia** — Every navigation pattern with specs, trade-offs, and production code: top bars, sidebars, bottom tabs, mega menus, breadcrumbs, command palettes, and contextual and mobile navigation. Use when choosing a nav model, fixing discoverability, or structuring information architecture.
- **nng-ux-heuristics** — Jakob Nielsen's 10 usability heuristics with modern interpretation, evaluation protocol, and 0-4 severity rating scale. Use when running a heuristic evaluation or usability review, rating the severity of a finding, or grounding UX feedback in established principles.
- **page-composition-engine** — Full-page recipes giving exact block order, spacing rhythm, visual pacing, and content hierarchy for landing pages, dashboards, e-commerce, auth, settings, and profiles. Use when composing a whole page. For a single section in isolation, use layout-block-intelligence.
- **performance-states-patterns** — Perceived performance and state design: skeleton screens, optimistic UI, progressive loading, notification architecture (toast, banner, badge, push), and empty, error, offline, and onboarding states. Use when a UI feels slow, or when specifying what a screen shows before, during, and after data arrives.
- **platform-visual-standards** — Current platform visual standards: iOS 26 Liquid Glass and SF Symbols 7, Material 3 Expressive (HCT, Dynamic Color, spring physics), web CSS 2025-2026 (container queries, view transitions, anchor positioning), plus watchOS, tvOS, and automotive. Use when a design must feel native to its platform.
- **react-native-design** — Master React Native styling, navigation, and Reanimated animations for cross-platform mobile development. Use when building React Native apps, implementing navigation patterns, or creating performant animations.
- **reference-intelligence** — Sources REAL design references instead of recalling them — award-winning live sites from Awwwards, app screens and flows from Mobbin (MCP), motion recipes from MotionSites (MCP) — captures them, measures their design DNA (type, color, spacing, grid, radius, motion stack), and synthesizes a Reference Board in .design-ops/refs/ that every MAKE and REVIEW command builds and grades against. Use when the user mentions: inspiration, inspo, references, reference sites, moodboard, Awwwards, SOTD, site of the day, Mobbin, MotionSites, 'make it look like', 'sites like', 'award-winning', 'best in class', examples of, what are the best sites for, reference board, steal like an artist, benchmark against real sites.
- **responsive-block-patterns** — How every block and component transforms across breakpoints: container queries, fluid scaling, breakpoint transformation catalogs, responsive grids, and mobile-first CSS with production code. Use when a layout must survive small screens, or when specifying responsive behavior for handoff.
- **screen-flow-patterns** — Taxonomy of 25+ screen types, 15+ user flows, and 25+ UI element deep-dives with layout patterns, component hierarchies, state matrices, and best-in-class references. Use when deciding which screens a product needs and what connects them, before any visual design starts.
- **scroll-experience-direction** — Art-directs cinematic scroll sites around one subject: interview, verified brand assets and facts, live references, depth planes with contact anchors, opening/midpoint/exit states, photographic compositing or real 3D, Kie AI imagery, separate phone direction, a uniqueness gate against past builds, and frame-checked packaging. Use when building premium launch, product or brand storytelling sites.
- **sector-style-intelligence** — Visual direction by industry for 20+ sectors: color psychology, typography norms, component conventions, spacing philosophy, motion personality, trust signals, and sector anti-patterns. Use when a design must read as credible for fintech, healthcare, SaaS, e-commerce, or education.
- **shadow-elevation-density** — Elevation, shadow, depth, and density systems: shadow scales, elevation hierarchy, glassmorphism, blur effects, border-radius systems, and compact, comfortable, and spacious density modes with production CSS. Use when surfaces look flat or float wrongly, or when tuning information density.
- **typography-pairing-recipes** — 100+ font pairing recipes and type scale systems covering Google Fonts, system stacks, variable fonts, fluid clamp() scales, and platform-native type, each with display, body, and mono picks at exact weights and line-heights. Use when choosing fonts or building a type scale.
- **ui-pattern-intelligence** — 190+ UI patterns across 10 categories, benchmark DNA from 25+ world-class products, sector pattern matrices, a matcher for code and screenshots, and a 43-entry anti-pattern encyclopedia. Use when detecting AI slop, judging whether a pattern is standard, or matching how a known product feels.
- **ux-ethics-content-strategy** — Dark pattern detection and avoidance, persuasive vs. manipulative design, privacy UX, the regulatory landscape, sustainable/green UX, and UX writing principles, readability, and inclusive language. Use when auditing a flow for manipulation, designing consent or privacy UX, or setting content strategy; for interface strings use micro-copy-intelligence.
- **ux-metrics-measurement** — UX measurement: HEART framework, SUS, UEQ, SUPR-Q, task success and time-on-task metrics, A/B testing statistics, AI-specific metrics, and design system ROI. Use when defining UX KPIs, building a measurement plan, interpreting a usability score, or proving UX impact.
- **ux-research-methods** — UX research methodology: usability testing protocols, user interviews, contextual inquiry, surveys, card sorting, and diary studies, plus synthesis frameworks including JTBD, journey mapping, and affinity diagramming. Use when planning a study, writing a discussion guide, or analyzing research data.
- **visual-design-mastery** — Designer-grade visual craft: type scales, color science (OKLCH, HCT), spacing systems, grids, visual hierarchy, elevation, iconography, 70 canonical rules and 10-dimension scoring. Use when setting type and color, building spacing or hierarchy, scoring visual quality, or when work looks cheap but you cannot say why.

## Agents

- **design-ops-art-director** — Design Ops art director. Turns captured references (.design-ops/refs/*/dna.json + screenshots) into a Reference Board, which is a tokenized direction with one stolen trait per reference, a category-norm list, an avoid list and a rejected list, written to .design-ops/refs/board.md + board.json for /style to turn into tokens. Also receives the critic's below-the-wall fixes and revises direction. Use after /inspo captures, or when a build keeps failing the same dimension.
- **design-ops-critic** — Design Ops critic. Grades a built page or screen SIDE BY SIDE against the Reference Board. It captures the build with the same scripts/capture.mjs, diffs its measured DNA against board.json, scores the build and the best reference on the same 10 dimensions, and returns a DQS, per-dimension deltas and a routed fix list. Use after /page, /screen or /remix produce something runnable, before shipping, or whenever someone asks "is this good enough?"
- **design-ops-scout** — Design Ops reference scout. Sources REAL design references for a brief (Awwwards award winners via scripts/awwwards.mjs, Mobbin screens and flows via the Mobbin MCP, MotionSites motion recipes), captures the live sites with scripts/capture.mjs in one call, and returns a shortlist with measured DNA. Use when a design task needs references, inspiration, "sites like X", or a refreshed .design-ops/refs/ board. Never recalls references from memory.
- **design-ops-ux-architect** — Design Ops UX architect. Designs flows, screen inventory, IA and states from REAL app patterns sourced through the Mobbin MCP (plus screen-flow-patterns taxonomy), and records them in .design-ops/refs/mobbin.json. Use for onboarding, checkout, signup, paywall, settings, dashboards, or any multi-screen product flow, and before /wireframe or /screen on app UI.

## Dependencies

- **Python 3.10+** for `design_ops_corpus.py`.
- **Node 18+** for `awwwards.mjs` and `capture.mjs`, bundled in the `reference-intelligence`
  skill's `scripts/` directory. Commands locate it as `$DESIGN_OPS`.
- **puppeteer-core** for capture. It is not bundled. Install it in the project you are
  designing (`npm i -D puppeteer-core`), or point `DESIGN_OPS_PUPPETEER_DIR` at a folder
  that has it. Set `DESIGN_OPS_CHROME` if Chrome is not found automatically.
- **Optional MCP servers**: Mobbin (screens and flows), Figma (design to code),
  Stitch and Fal (generation). Each is configured by the user and unlocks the commands
  that name it.

## Conventions

- Design decisions persist in the target project's `.design-ops/` directory. The
  `design-memory` skill defines which command owns which file.
- References are sourced live and captured, never recalled.
- WCAG 2.2 AA is the floor for everything built.

## Attribution

Design Ops is derived from Sumi 4.2.0, Copyright 2026 Phazur Labs LLC, licensed under the
Apache License, Version 2.0. It has been renamed, restructured as a portable multi-tool
plugin, and modified. See `NOTICE` and `LICENSE`. "Sumi" and "Phazur Labs" are trademarks
of Phazur Labs LLC. This project is not affiliated with or endorsed by them.

## Author

**Curtis Blanton**

- Website: [shotcowboystyle.com](https://shotcowboystyle.com)
- Email: public@shotcowboystyle.com
- GitHub: [@shotcowboystyle](https://github.com/shotcowboystyle)

## License

Apache-2.0. See `LICENSE` and `NOTICE`.
