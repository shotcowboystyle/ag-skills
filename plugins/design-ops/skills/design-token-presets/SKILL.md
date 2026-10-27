---
name: design-token-presets
description: 15 ready-to-deploy token systems by industry vertical, each in W3C DTCG JSON, CSS custom properties, and Tailwind v4 @theme, with Style Dictionary config and Figma Variables mapping. Use when you want a vetted starting token set. For architecting your own, use design-systems-architecture.
allowed-tools: Read, Grep, Glob
---

# Design Token Presets — 15 Ready-to-Deploy Token Systems

Complete token systems to deploy now and customize later. Each preset is opinionated by design — opinionated defaults ship faster than blank canvases.

## Token Architecture (3-Tier)

Every preset follows the W3C Design Tokens Community Group (DTCG) standard:

### Tier 1: Primitive Tokens (Raw Values)
The foundational palette — colors, sizes, raw numbers.
```json
{ "color": { "blue": { "500": { "$value": "oklch(0.55 0.2 260)", "$type": "color" } } } }
```

### Tier 2: Semantic Tokens (Meaning)
Map primitives to purpose — what the color MEANS.
```json
{ "color": { "primary": { "$value": "{color.blue.500}", "$type": "color" } } }
```

### Tier 3: Component Tokens (Context)
Map semantics to specific components — where the color IS USED.
```json
{ "button": { "primary": { "background": { "$value": "{color.primary}", "$type": "color" } } } }
```

## Token Categories in Every Preset

| Category | Tokens | Description |
|----------|--------|-------------|
| Color | 80-120 tokens | 10-step scales per hue, semantic mapping, dark mode |
| Typography | 20-30 tokens | Font family, size scale, weight, line-height, letter-spacing |
| Spacing | 16-20 tokens | Base-4 scale from 0 to 96 |
| Border Radius | 6-8 tokens | none through full |
| Shadow | 5-6 tokens | sm through 2xl |
| Motion | 8-10 tokens | Duration + easing |

**Motion:** sector presets tune durations (and some curve values) on top of the base motion scale owned by `interaction-motion-design` (`animation-timing-curves.md`), using the same names: `--duration-{instant,fast,normal,moderate,slow,slower}` and `--ease-{out,in,in-out,spring}`. `--ease-spring` is each preset's accent curve; restrained sectors set it to a non-overshoot curve. Sector-only extras (`--ease-dramatic`, `--ease-playful`, `--ease-gentle`, `--duration-cinematic`) are additions, never renames.
| Breakpoint | 5-7 tokens | xs through 2xl |
| Z-index | 8-10 tokens | Layer scale |
| Opacity | 5-6 tokens | Transparency scale |

## Color Generation Methodology

All colors use **oklch** color space for perceptual uniformity:
1. Choose a hue (0-360)
2. Set chroma (saturation intensity)
3. Generate 10 lightness steps: 50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950
4. Validate APCA contrast for all text/background combinations
5. Map to semantic roles: background, surface, text, primary, secondary, success, warning, error, info

## Available Presets

### SaaS / Productivity (5 presets)
1. **"Linear"** — Minimal, monochromatic, violet accent. For precision tools
2. **"Notion"** — Warm neutrals, readable, content-first. For knowledge tools
3. **"Stripe"** — Premium blue-to-purple gradient, high-trust. For financial tools
4. **"Slack"** — Colorful, friendly, communication-focused. For social tools
5. **"Figma"** — Purple-accent, dense, productive. For creative tools

### Fintech / Healthcare (4 presets)
6. **"Mercury"** — Navy + clean accent, high trust. For banking
7. **"Robinhood"** — Black + green, action-oriented. For trading
8. **"Calm Health"** — Soft blues/greens, accessible. For patient-facing health
9. **"Clinical"** — High contrast, data-dense. For medical professionals

### E-commerce / Social (4 presets)
10. **"Shopify"** — Merchant-friendly green, versatile. For commerce
11. **"Premium Commerce"** — Elegant type, minimal color. For luxury retail
12. **"Social Warm"** — Warm gradients, engaging. For social platforms
13. **"Community"** — Dark-first, vibrant accents. For forums/communities

### Creative / Luxury / Dev (4 presets)
14. **"Studio"** — Bold type, minimal palette. For portfolios
15. **"Luxury"** — Serif type, gold/black, elegant. For premium brands
16. **"Playful"** — Bright colors, rounded, fun. For consumer apps
17. **"Developer"** — Mono-forward, syntax colors, dark-first. For dev tools

## Preset Structure

Each preset is one CSS `:root {}` block (primitives, semantic light/dark, typography, spacing, radius, shadow, motion, breakpoints) plus a Tailwind v4 `@theme` block. The complete worked example is the Linear preset, section 1 of `references/saas-fintech-presets.md`.

## Customization Guide

### Changing the Primary Color
1. Choose your brand hue in oklch (e.g., hue 200 for teal)
2. Generate 10 lightness steps maintaining chroma
3. Replace `--color-primary` semantic mapping
4. Validate APCA contrast ratios

### Making a Preset Warmer
- Shift gray hue from 280 (cool) toward 40-60 (warm)
- Increase chroma slightly on grays (0.005 → 0.015)
- Choose warmer accent hues (amber, coral, warm violet)

### Making a Preset Darker
- Set default mode to dark
- Reduce surface lightness
- Increase text lightness for contrast

## Routing

Detailed presets are available in the `references/` directory:
- `saas-fintech-presets.md` — Linear, Stripe, Notion, Slack, Figma, Mercury, Robinhood presets (CSS `:root` + Tailwind v4 `@theme`)
- `ecommerce-social-presets.md` — Shopify, Premium Commerce, Social Warm, Community presets (CSS `:root` + Tailwind v4 `@theme`)
- `creative-dev-health-presets.md` — Studio, Luxury, Playful, Developer, Calm Health, Clinical presets (CSS `:root` + Tailwind v4 `@theme`)
- `dtcg-json-presets.md` — W3C DTCG JSON format for 6 flagship presets (Linear SaaS, Stripe Fintech, Shopify E-commerce, Discord Social, Creative Agency, Healthcare). 3-tier structure (primitive/semantic/component). Style Dictionary 4.x config. Figma Variables mapping.

## Cross-References

- **design-systems-architecture** — Token architecture deep-dive
- **sector-style-intelligence** — Industry visual direction
- **color-palette-library** — 180+ color palettes
- **visual-design-mastery** — Typography and spacing theory, complete visual scoring
- **interaction-motion-design** — Base motion scale (easing, duration, springs)
