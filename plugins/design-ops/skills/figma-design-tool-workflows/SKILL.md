---
name: figma-design-tool-workflows
description: "Figma mastery and design-to-code: Auto Layout, component architecture, variable modes, Dev Mode handoff, Figma MCP server integration, Code Connect, and token pipelines. Use when working in Figma, converting designs to code, or setting up a design-to-code flywheel."
allowed-tools: Read, Grep, Glob
---

# Figma Design Tool Workflows

Treat Figma as the design system of record: every layer name, component property, and variable is data that flows into code generation, token pipelines, accessibility audits, and visual regression. A sloppy file produces sloppy code.

## Component Architecture

- **Property types map to code props:** boolean → optional boolean prop (conditional render); text → `label`/`children`; instance swap → slot prop (`icon?: ReactNode`); preferred values curate the swap picker.
- **Variants** for visually distinct states that change several properties at once (`variant` x `size`). **Component properties** for independent toggles (an icon on/off) so the variant count does not double. **Separate components** when there is no shared structure.
- **Nested sub-components** (`CardHeader`, `CardBody`, `CardFooter`) via instance swap slots mirror React compound components.
- **Naming:** `Category/Type/State` (`Button/Primary/Hover`, `Input/Text/Error`), matching code directory structure.

## Variable Modes

Three collections: **primitive** (raw values, one mode), **semantic** (light/dark/high-contrast modes), **component** (bindings; modes for density or brand). Switching a frame's mode previews every permutation without duplicate frames. Variable names must match CSS custom property or token names in code.

## Auto Layout Rules

- Every component uses Auto Layout; if it can't, rethink the design.
- Bind padding and gap to spacing variables so density modes work.
- Fill container = `flex: 1`; Hug contents = `width: auto`.
- Absolute positioning only for overlays such as avatar badges and FABs (`position: absolute` in a relative parent).

## Dev Mode

Developers see props, CSS values, variable names instead of raw values, annotations, snippets, and measurements. Output quality depends entirely on naming, variable binding, and Auto Layout.

## Figma MCP and the Flywheel

The Figma MCP server lets an agent read file structure, component properties and variants, variables and modes, Auto Layout specs, styles, and prototype flows. The flywheel: **Design** with proper architecture → **Read** via MCP → **Generate** typed component, token-based styles, Storybook stories, tests → **Validate** with visual regression (Chromatic, Percy) and axe-core → **Iterate** on Figma changes → **Ship** through CI and the token pipeline. Later passes are cheaper than the first; measure the saving on your own components before quoting a number.

## Routing

| Question | Read |
|---|---|
| Auto Layout in depth, component architecture, variable modes, prototyping, Dev Mode, library management, naming and file organization, plugins, shortcuts, canvas-to-code mapping summary | `references/figma-mastery-workflows.md` |
| Pipeline architecture, Style Dictionary config, token transforms, CI/CD, visual regression, Storybook, multi-brand, accessibility in the pipeline | `references/design-to-code-pipeline.md` |
| MCP server setup and tools, the flywheel, Card walkthrough, Code Connect, token extraction, prompt templates, quality gates, ROI | `references/figma-mcp-ai-flywheel.md` |

## Cross-References

- Component code patterns MCP output should follow: `component-patterns-code`
- Token hierarchy, versioning, contribution and change management: `design-systems-architecture`
- Color, type scale, spacing, and elevation behind variable collections: `visual-design-mastery`
- Accessibility plugins, contrast, focus order and screen reader annotations: `accessibility-inclusive-design`
- Prototyping, smart animate, motion tokens: `interaction-motion-design`

## Key Sources

- Figma official documentation: Components, Variables, Auto Layout, Dev Mode, Code Connect
- Figma MCP server documentation and API reference
- Style Dictionary documentation for multi-platform token transformation
- Tokens Studio (Figma plugin) documentation for token management
- Chromatic documentation for visual regression testing with Storybook
- W3C Design Tokens Community Group specification for token format
