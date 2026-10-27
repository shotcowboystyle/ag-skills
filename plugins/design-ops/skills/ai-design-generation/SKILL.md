---
name: ai-design-generation
description: Produce visual assets from AI image and UI models through MCP — Stitch screens, Fal.ai (Imagen, FLUX, Veo), Recraft V3 vectors, GPT-Image and Figma file access — with prompt patterns and quality scoring. Use when rendering mockups, icons, illustrations or video. Not for interface copy; not for agent UX.
allowed-tools: Read, Grep, Glob
---

# AI Design Generation

## Purpose

Turn a design brief into AI-generated screens, icons, illustrations, photos and video, then curate them to production quality. The tools have no understanding of users, goals or brand; the agent supplies the brief, constraints, quality bar and iteration direction. MCP servers are optional: without them, produce detailed specs and prompts the user can run in any tool.

## Core rules

- **Run the curation loop.** Specify → generate 3-6 candidates → evaluate against brand, usability and aesthetics → select → refine the prompt → repeat. 2-4 rounds usually reach production quality. Never ship a first-generation output unreviewed.
- **Write prompts like briefs.** Be specific ("16px Inter Medium, #1A1A2E on white, 8px radius card", not "modern and clean"). Name real products ("Stripe dashboard density"). State what the design must NOT do. Layer the prompt: style, layout, content, details. Inject design tokens, sector and platform (for iOS 26 Liquid Glass or Material 3 Expressive conventions, see `platform-visual-standards`).
- **Pick the tool by asset:** UI screens → Stitch; SVG icons and vectors → Recraft V3; hero photos → FLUX Pro or Imagen 4; editorial illustration → Midjourney (manual) or FLUX; concepts and patterns → FLUX Schnell; video → Veo 3.1 via fal. OpenAI image models have no official MCP server, so call the Images API or hand the user the prompt.
- **Go from breadth to depth.** Use cheap, fast models at low resolution for 10-20 concepts, premium models for 4-6 variations of the chosen directions, then refine, and upscale only the selected outputs.
- **Keep sets consistent.** Generate an anchor (the most complex icon or the hero illustration) first, batch the rest against it in groups of about 6, review the set as a whole, and regenerate outliers.
- **Quality gate.** Check for garbled text (replace it with real copy), spacing drift, phantom UI, style drift, anatomical errors, brand contamination and soft edges. Score brand compliance on 7 dimensions (0-10). Production needs a 7+ average. Color-correct to brand values and re-check WCAG contrast.
- **Hand off.** Rebuild generated screens with Figma Auto Layout and real tokens, or map them to existing components and code via `component-patterns-code`, then compare the rendered output against the mockup.
- **Ethics.** Prompt explicitly for demographic and cultural diversity. Audit accessibility, since generated designs rarely meet WCAG. Verify commercial-use licenses. Tell clients when shipped or presented work is AI-generated.

## Routing

| Question | Read |
| --- | --- |
| Which MCP server; configuration; Stitch, fal, Recraft, Midjourney, DALL-E, Veo, Runway, Pika capabilities and prompt patterns | `references/mcp-design-tools.md` |
| Prompt anatomy per tool, token injection, sector/platform prompting, negative prompts, UI/icon/illustration/landing-page templates | `references/prompt-engineering-visual.md` |
| Multi-step and batch pipelines, design-system asset generation, Figma import, code from mockups, when to hand-craft | `references/generation-pipelines.md` |
| Scoring output, artifact detection, consistency checklist, brand-compliance rubric, iteration fixes | `references/quality-control-generation.md` |
| Icons, illustrations, photos, video, patterns; upscaling, background removal, SVG tracing, color correction; ethics; cost per model and asset | `references/asset-generation-guide.md` |

## Cross-References

- **`visual-design-mastery`** — Provides the design intelligence that makes generation prompts effective and quality scoring meaningful.
- **`platform-visual-standards`** — Provides platform-specific constraints for generation prompts.
- **`ui-pattern-intelligence`** — Identifies which patterns to generate and their quality benchmarks.
- **`sector-style-intelligence`** — Provides sector-specific visual direction for generation prompts.
- **`design-systems-architecture`** — Ensures generated designs consume design tokens consistently.
- **`figma-design-tool-workflows`** — Integration with Figma for design-to-code pipelines.
- **`icon-illustration-systems`** — Detailed icon and illustration design guidance that informs generation prompts.
- **`color-palette-library`** — Curated palettes for color-accurate generation prompts.
- **`typography-pairing-recipes`** — Type system knowledge for typography-aware generation.
- **`animation-recipe-library`** — Motion design knowledge for video generation prompts.
- **`scroll-experience-direction`** — Kie AI stills, image-to-video shots and background removal for scroll sites (`kie-ai.md`).

## Commands Powered by This Skill

| Command      | How This Skill Is Used                                            |
| ------------ | ----------------------------------------------------------------- |
| `/generate`  | Primary command — screen and asset generation (icons, illustrations, photos, video) via MCP tools |
| `/grade`     | Can generate mood board visualizations using image generation     |
| `/screen`    | Can use Stitch to generate screen mockups before coding           |
| `/component` | Can reference generated designs as implementation targets         |
