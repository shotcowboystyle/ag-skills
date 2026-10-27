---
name: design-systems-architecture
description: "Design system architecture: W3C design tokens, Style Dictionary pipelines, component library structure, theming, multi-brand token tiers, governance, versioning, and maturity models. Use when starting or scaling a design system, generating tokens, or setting up design-to-code distribution."
allowed-tools: Read, Grep, Glob
---

# Design Systems Architecture

"A design system is not a project. It is a product serving products." — Nathan Curtis

The system is the single source of truth for how a product family looks, behaves, and communicates: opinionated enough for coherence, flexible enough for diverse products.

## Core Principles

1. **Systematic over stylistic** — define rules and relationships, not just visual recipes
2. **Tokens are the foundation** — design decisions encoded as data, not hardcoded values
3. **Composition over inheritance** — build complex components from simple, composable primitives
4. **Document the why** — every decision needs rationale to prevent future erosion
5. **Adopt, then adapt** — products adopt the system by default, request exceptions with justification

## Token Architecture

Three tiers; each tier references only the tier below:

| Tier | Purpose | Example |
|---|---|---|
| 1 Global / primitive | The full value palette | `color.blue.500 = #3b82f6` |
| 2 Semantic / alias | Design intent | `color.action.primary = {color.blue.500}` |
| 3 Component | Where a value is used | `button.primary.bg = {color.action.primary}` |

Follow the W3C DTCG format: `$value`, `$type` (color, dimension, fontFamily, fontWeight, duration, cubicBezier, shadow), `$description`, `{}` references, `.tokens.json` files. Categories: color, spacing, typography, radius, elevation, duration, easing, sizing, opacity, z-index.

## Components

- **Anatomy:** props/API, variants, states (default, hover, active, focused, disabled, loading, error), slots, token bindings, accessibility, documentation.
- **Maturity:** Defined → Implemented → Tested → Documented → Governed.
- **API rules:** consistent prop names, enums over booleans, composition over configuration, sensible defaults, full TypeScript types, forwarded refs, polymorphic `as`.

## Theming

CSS custom properties are the runtime mechanism: swap values at the root, honor `prefers-color-scheme`, allow a persisted manual override. Component tokens reference semantic tokens, which resolve per theme. Multi-brand: shared behavior and accessibility, per-brand token sets, a component override layer only when tokens are not enough, and a Brand x Mode theme matrix.

## Governance

Hybrid contribution is the default: the core team owns primitives (Button, Input, Card) and governance; domain teams contribute domain components (DataGrid, FileUploader) under core review. Changes go RFC → design, code, and accessibility review → build with tests → document → release. Version with SemVer (MAJOR = breaking API or visual change); keep deprecations for 2 major versions with warnings and migration guidance.

## Design-to-Code

Figma component names match code names exactly, and variants map to props. Tokens flow Figma → `tokens.json` → code through CI (Style Dictionary) into CSS variables, Swift, Android XML, React Native, and TypeScript types. Run visual regression against the Figma source.

## Routing

| Question | Read |
|---|---|
| Three-tier model with JSON examples, DTCG naming, token categories, the 2025 spec update | `references/design-token-architecture.md` |
| DTCG spec detail, full `$type` reference, Style Dictionary config, Token Studio, token CI/CD, the October 2025 stable release | `references/token-specification-guide.md` |
| Aliasing, multi-theme tokens, transformation pipeline, platform outputs, token docs, versioning, testing | `references/design-token-implementation.md` |
| Component anatomy, maturity levels, API principles, theme JSON, multi-brand layering, Figma-to-code sync | `references/component-library-theming.md` |
| Team models, contribution workflow, RFC and proposal templates, lifecycle, versioning, docs, adoption metrics | `references/governance-scaling.md` |
| Five-level maturity model, assessment rubric, multi-brand tokens, white-label, migration, ROI, `$extensions` | `references/maturity-model-multi-brand.md` |

## Cross-Referencing

- Visual design principles: `visual-design-mastery`
- Accessibility component requirements: `accessibility-inclusive-design`
- Motion tokens and animation: `interaction-motion-design`
- Mobile component adaptations: `mobile-ux-design`
- Figma MCP design-to-code flywheel: `figma-design-tool-workflows`
- CSS `@layer` cascade for token architecture: `component-patterns-code`

## Key Sources

- Curtis, N. "Design Systems" and Modular Web Design
- W3C Design Tokens Community Group specification
- Figma design systems documentation
- Material Design component guidelines
- Brad Frost "Atomic Design" methodology
