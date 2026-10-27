# Color Mastery

> Deep color science for UI design: perceptually uniform color spaces, palette generation, accessibility, dark mode, dynamic color, and semantic systems.

---

## Color Spaces for UI

### sRGB — The Legacy Default

sRGB (standard Red Green Blue) is the default web color space. Every hex value (#3B82F6), rgb(), and hsl() function operates in sRGB.

**Limitations**:
- **Perceptually non-uniform**: hsl(60, 100%, 50%) (yellow) appears far brighter than hsl(240, 100%, 50%) (blue) despite equal lightness values. You cannot rotate hue and maintain perceived brightness.
- **Gamut limits**: sRGB covers only ~35% of visible colors. Modern displays (P3) can show 25% more.
- **Gradient interpolation**: Gradients between distant hues pass through desaturated muddy midpoints (blue→yellow = gray/green sludge).

**When to use**: Legacy browser support. Fallback values in CSS.

### oklch() — The Modern Standard

oklch(Lightness Chroma Hue) is a perceptually uniform cylindrical color space, native to CSS since 2023.

```css
/* oklch(L C H / alpha) */
/* L: 0-1 (0 = black, 1 = white) */
/* C: 0-0.4 (0 = gray, higher = more saturated) */
/* H: 0-360 (hue angle: 0=pink, 70=yellow, 150=green, 250=blue, 330=magenta) */

--primary: oklch(0.55 0.25 250);       /* Vivid blue */
--primary-light: oklch(0.75 0.15 250);  /* Same hue, lighter, less saturated */
--primary-dark: oklch(0.40 0.20 250);   /* Same hue, darker */
```

**Advantages**:
- **Perceptually uniform L**: oklch(0.7 0.15 70) and oklch(0.7 0.15 250) actually appear equally bright.
- **Hue-stable lightness adjustment**: Changing L doesn't shift the perceived hue.
- **Better gradients**: Interpolation in oklch avoids muddy midpoints.
- **CSS-native**: Supported in Chrome 111+, Safari 16.4+, Firefox 113+.

**When to use**: All new color work. Palette generation. Gradient definitions. Tonal scales.

### LCH — oklch's Predecessor

LCH (Lightness, Chroma, Hue) uses the CIE LAB color space. Similar to oklch but with a slightly different lightness model (CIE L* vs Oklab L).

**Key difference from oklch**: LCH has slight hue shifts when adjusting lightness (e.g., blue shifts toward purple at high lightness). oklch corrects this.

**When to use**: If oklch is not available. Otherwise, prefer oklch.

### HCT — Material 3's Color Space

HCT (Hue, Chroma, Tone) is Google's custom color space for Material Design 3. It combines CAM16 hue and chroma with CIE L* tone.

```
HCT(hue: 0-360, chroma: 0-~120, tone: 0-100)
```

**Key properties**:
- **Tone** = CIE L* lightness (0-100), which maps well to contrast calculations.
- **Perceptually accurate** hue and chroma from CAM16.
- **Designed for** generating tonal palettes where every step has predictable contrast.

**When to use**: Material 3 design systems. Android Dynamic Color. When you need precise contrast math (tone difference of 40+ ≈ WCAG AA).

### Display P3 — Wide Gamut

P3 is a color gamut 25% larger than sRGB, standard on Apple devices since 2016 and increasingly on Android/Windows.

```css
/* P3 color with sRGB fallback */
.button {
  background-color: #3B82F6;                          /* sRGB fallback */
  background-color: color(display-p3 0.23 0.51 0.96); /* P3 — more vivid */
}

/* Feature detection */
@media (color-gamut: p3) {
  :root {
    --primary: oklch(0.55 0.25 250);  /* oklch can express P3 colors */
  }
}
```

**When to use**: When brand colors benefit from increased vibrancy. Gradients. Hero sections. Use with sRGB fallback.

---

## Palette Generation Algorithms

### Harmony Types

All hue calculations are in oklch hue degrees (0-360):

| Harmony | Formula | Character | Use Case |
|---|---|---|---|
| **Complementary** | base_hue + 180 | High contrast, energetic | CTA on opposite-color background, data viz with 2 categories |
| **Analogous** | base_hue ± 30 | Harmonious, calm | Multi-section apps, related features |
| **Triadic** | base_hue ± 120 | Balanced variety | Data visualization with 3 categories, multi-brand |
| **Split-complementary** | base_hue + 150, base_hue + 210 | Contrast with less tension | Accent colors that complement without clashing |
| **Tetradic** | base_hue + 90, + 180, + 270 | Maximum variety | Complex dashboards, many categories |

### Tonal Palette Generation (Material 3 Style)

Generate 13 tones from a single source color for systematic UI use:

```
Source color: oklch(0.55 0.20 250) /* Blue */

Tones (L values in oklch, C adjusted for gamut):
  tone-0:   oklch(0.00 0.00 250)  /* Black */
  tone-5:   oklch(0.15 0.04 250)
  tone-10:  oklch(0.22 0.07 250)
  tone-15:  oklch(0.28 0.10 250)
  tone-20:  oklch(0.33 0.12 250)
  tone-30:  oklch(0.42 0.16 250)
  tone-40:  oklch(0.50 0.20 250)
  tone-50:  oklch(0.58 0.22 250)  /* Close to source */
  tone-60:  oklch(0.65 0.18 250)
  tone-70:  oklch(0.72 0.14 250)
  tone-80:  oklch(0.80 0.10 250)
  tone-90:  oklch(0.88 0.06 250)
  tone-95:  oklch(0.93 0.03 250)
  tone-99:  oklch(0.98 0.01 250)
  tone-100: oklch(1.00 0.00 250)  /* White */
```

**Key rule**: As lightness increases, chroma must decrease (high-lightness, high-chroma colors are out of gamut for sRGB). Scale chroma proportionally: max chroma at L=0.50, decreasing toward both extremes.

### oklch-Based Palette Generation

Generate a full UI palette from a single brand color:

```css
:root {
  /* Source brand color */
  --brand-h: 250;  /* Hue */
  --brand-c: 0.20; /* Max chroma */

  /* Primary scale */
  --primary-50:  oklch(0.97 0.01 var(--brand-h));
  --primary-100: oklch(0.93 0.03 var(--brand-h));
  --primary-200: oklch(0.87 0.07 var(--brand-h));
  --primary-300: oklch(0.78 0.11 var(--brand-h));
  --primary-400: oklch(0.68 0.16 var(--brand-h));
  --primary-500: oklch(0.58 0.20 var(--brand-h));  /* Source */
  --primary-600: oklch(0.50 0.20 var(--brand-h));
  --primary-700: oklch(0.42 0.18 var(--brand-h));
  --primary-800: oklch(0.35 0.14 var(--brand-h));
  --primary-900: oklch(0.27 0.10 var(--brand-h));
  --primary-950: oklch(0.20 0.07 var(--brand-h));
}
```

### Brand Color Expansion Method

Given a single brand hex color (e.g., #3B82F6):

1. **Convert** to oklch: oklch(0.55 0.22 252)
2. **Extract** H (252) and C (0.22) as base values
3. **Generate primary scale**: 11 steps from L=0.97 to L=0.20, adjusting C
4. **Generate neutral scale**: same H, C reduced to 0.01-0.02 (tinted neutrals)
5. **Generate semantic colors**: rotate H for success (H+130≈green), warning (H-180≈amber), error (H-220≈red)
6. **Test all pairs** for APCA contrast

### Accessible Palette Generation

Ensure every color pair meets APCA standards:

```
APCA Lc (Lightness Contrast) thresholds:
  Lc 90+:  Preferred for body text (16px regular)
  Lc 75+:  Minimum for body text (16px regular)
  Lc 60+:  Minimum for large text (24px+ or 18px bold)
  Lc 45+:  Minimum for non-text elements (icons, borders)
  Lc 30+:  Minimum for large non-text (decorative elements)
  Lc 15+:  Minimally distinguishable (subtle dividers, disabled states)
```

**APCA vs WCAG 2.x**: APCA is polarity-aware — dark text on light background has different thresholds than light text on dark background. APCA better predicts real-world readability and is the successor standard (WCAG 3.0 draft).

---

## Contrast & Accessibility

### WCAG 2.x Contrast Ratios

| Level | Normal text (<24px, <18.5px bold) | Large text (≥24px or ≥18.5px bold) | Non-text UI |
|---|---|---|---|
| **AA** | 4.5:1 | 3:1 | 3:1 |
| **AAA** | 7:1 | 4.5:1 | N/A |

**Calculating in CSS**: No native calculation. Use dev tools or build-time tools (axe, Pa11y).

### APCA (Advanced Perceptual Contrast Algorithm)

APCA replaces the simplistic WCAG 2.x ratio with perceptually accurate Lightness Contrast (Lc):

```
Lc value  Recommended use
Lc 90+    Preferred body text (14-16px)
Lc 75     Minimum body text (16px)
Lc 60     Large bold text (24px+), or 18px body at reduced importance
Lc 45     Sub-text, placeholders, large icons
Lc 30     Large decorative text, non-essential borders
Lc 15     Subtle disabled states, decorative dividers
```

**Polarity**: APCA accounts for the fact that white text on black is perceived differently from black text on white. The same color pair has different Lc values depending on polarity.

**Checking in oklch**: Two colors with an oklch L difference of 0.45+ generally pass APCA Lc 60+. L difference of 0.55+ generally passes Lc 75+. But always verify with APCA calculator because chroma and hue affect perception.

### Contrast Checking Tools

- **APCA calculator**: myndex.com/APCA
- **oklch.com**: Live oklch color picker with contrast preview
- **Chrome DevTools**: Contrast ratio shown in color picker tooltip
- **Figma plugins**: Stark, A11y - Color Contrast Checker

---

## Dark Mode

### Core Principles

Dark mode is NOT "invert the colors." It is a complete re-mapping of the color system:

1. **Reduce contrast slightly**: Pure white (#FFF) text on pure black (#000) causes halation (white text bleeds on OLED). Use off-white (#E5E7EB) on near-black (#111827).
2. **Increase lightness of accent colors**: Light-mode primary (oklch 0.55) becomes dark-mode primary (oklch 0.75) — lighter and less saturated.
3. **Use surface tinting**: Elevated surfaces are tinted with the primary color, not just lighter gray.
4. **Flip elevation model**: In light mode, higher = lighter + more shadow. In dark mode, higher = lighter surface (no visible shadow on dark).

### Dark Mode Surface Elevation

Using Material 3's surface tinting approach:

```css
:root[data-theme="dark"] {
  --surface-base: oklch(0.15 0.01 var(--brand-h));

  /* Elevation via primary color tint */
  --surface-0: var(--surface-base);
  --surface-1: color-mix(in oklch, var(--surface-base) 95%, var(--primary) 5%);
  --surface-2: color-mix(in oklch, var(--surface-base) 92%, var(--primary) 8%);
  --surface-3: color-mix(in oklch, var(--surface-base) 89%, var(--primary) 11%);
  --surface-4: color-mix(in oklch, var(--surface-base) 85%, var(--primary) 15%);
  --surface-5: color-mix(in oklch, var(--surface-base) 80%, var(--primary) 20%);
}
```

### Light-to-Dark Color Mapping

| Token | Light Mode | Dark Mode | Rule |
|---|---|---|---|
| --color-bg-primary | oklch(1.0 0 0) white | oklch(0.15 0.01 H) near-black | Flip lightness extremes |
| --color-bg-surface | oklch(0.97 0.005 H) off-white | oklch(0.20 0.015 H) dark gray | Slight tint |
| --color-bg-elevated | oklch(1.0 0 0) white | oklch(0.25 0.02 H) lighter dark | Elevate = lighten in dark |
| --color-text-primary | oklch(0.15 0.01 H) near-black | oklch(0.90 0.01 H) off-white | High contrast text |
| --color-text-secondary | oklch(0.45 0.02 H) mid-gray | oklch(0.65 0.02 H) light gray | Moderate contrast |
| --color-text-tertiary | oklch(0.60 0.02 H) light gray | oklch(0.50 0.02 H) mid-gray | Low contrast |
| --color-interactive | oklch(0.55 0.25 H) vivid | oklch(0.75 0.15 H) lighter, less sat | Increase L, decrease C |
| --color-border | oklch(0.85 0.01 H) light border | oklch(0.30 0.015 H) subtle border | Adjusted for surface |

### Common Dark Mode Failures

1. **Saturated colors on dark backgrounds**: Creates visual vibration. Fix: reduce chroma by 30-40% in dark mode.
2. **Pure black backgrounds (#000000)**: Works on OLED (saves battery) but feels harsh on LCD. Fix: use #111827 or oklch(0.15 0.01 H) unless targeting OLED specifically.
3. **Same shadows in dark mode**: box-shadow is invisible on dark backgrounds. Fix: use border (1px solid rgba(255,255,255,0.06)) or surface color difference instead.
4. **White images/illustrations on dark background**: Blinding. Fix: add dark-mode variants or apply filter: brightness(0.85) to images.
5. **Insufficient elevation distinction**: All dark surfaces look the same. Fix: use the tinting system above with clearly different levels.

---

## Dynamic Color

### Material You: Wallpaper-Based Color Extraction

Material You (Android 12+) extracts a palette from the user's wallpaper:

**Algorithm**:
1. **Sample** the wallpaper image for dominant colors using a k-means clustering variant
2. **Select** the most chromatic, well-distributed seed color
3. **Convert** to HCT color space
4. **Generate** 5 tonal palettes:
   - Primary: from seed hue
   - Secondary: seed hue, lower chroma
   - Tertiary: seed hue + 60 degrees
   - Neutral: seed hue, very low chroma (tinted gray)
   - Neutral variant: seed hue, slightly more chroma than neutral
5. **Each palette**: 13 tones (0, 5, 10, 15, 20, 25, 30, 35, 40, 50, 60, 70, 80, 90, 95, 99, 100)
6. **Map** tones to color roles (primary-container = primary tone 90 in light, tone 30 in dark)

### iOS 26 Tinted System Colors

iOS 26 introduces system-wide tinting based on wallpaper and app icon:

- System colors (blue, red, green, etc.) shift hue slightly to match the dominant wallpaper tone
- App-specific tint color can be set via the asset catalog
- Liquid Glass material tinting: see `platform-visual-standards` (its `ios-26-liquid-glass.md` reference)

### Implementing Dynamic Color in CSS

```css
/* Basic approach: CSS custom properties + user preference */
:root {
  --user-hue: 250; /* Default blue, overridden by user/system */
}

/* Generate full palette from user hue */
:root {
  --primary: oklch(0.55 0.20 var(--user-hue));
  --primary-container: oklch(0.90 0.06 var(--user-hue));
  --surface: oklch(0.98 0.005 var(--user-hue));
  --on-surface: oklch(0.15 0.02 var(--user-hue));
}

/* For Android WebView: read Material You colors */
@media (prefers-color-scheme: light) {
  :root {
    --primary: var(--md-sys-color-primary, oklch(0.55 0.20 250));
  }
}
```

---

## Semantic Color Systems

### Role-Based Color Architecture

```
Tier 1: Reference Colors (raw values, never used directly)
  --ref-blue-500: oklch(0.55 0.22 250)
  --ref-green-500: oklch(0.60 0.18 155)
  --ref-amber-500: oklch(0.75 0.16 80)
  --ref-red-500: oklch(0.55 0.22 25)
  --ref-gray-500: oklch(0.55 0.02 250)

Tier 2: Semantic Colors (mapped to roles)
  Brand:
    --color-primary: var(--ref-blue-500)
    --color-primary-hover: oklch(0.48 0.22 250)
    --color-primary-active: oklch(0.42 0.20 250)
    --color-on-primary: oklch(1.0 0 0)       /* Text on primary */
    --color-primary-container: oklch(0.92 0.04 250)
    --color-on-primary-container: oklch(0.20 0.10 250)

  Semantic:
    --color-success: var(--ref-green-500)
    --color-success-container: oklch(0.93 0.04 155)
    --color-warning: var(--ref-amber-500)
    --color-warning-container: oklch(0.95 0.04 80)
    --color-error: var(--ref-red-500)
    --color-error-container: oklch(0.93 0.04 25)
    --color-info: var(--ref-blue-500)

  Surface:
    --color-bg: oklch(1.0 0 0)
    --color-surface: oklch(0.98 0.005 250)
    --color-surface-elevated: oklch(1.0 0 0)
    --color-surface-overlay: oklch(0 0 0 / 0.5)

  Content:
    --color-text-primary: oklch(0.15 0.02 250)
    --color-text-secondary: oklch(0.45 0.015 250)
    --color-text-tertiary: oklch(0.60 0.01 250)
    --color-text-disabled: oklch(0.70 0.005 250)
    --color-text-on-primary: oklch(1.0 0 0)
    --color-text-link: var(--color-primary)

  Border:
    --color-border-default: oklch(0.85 0.01 250)
    --color-border-strong: oklch(0.70 0.015 250)
    --color-border-focus: var(--color-primary)

  State:
    --color-hover: oklch(0 0 0 / 0.04)
    --color-active: oklch(0 0 0 / 0.08)
    --color-selected: oklch(0.92 0.04 250)
    --color-disabled-bg: oklch(0.95 0.005 250)
    --color-disabled-text: oklch(0.70 0.005 250)
```

### Design Token Format (W3C DTCG)

```json
{
  "color": {
    "primary": {
      "$value": "oklch(0.55 0.22 250)",
      "$type": "color",
      "$description": "Primary brand color. Used for CTAs, interactive elements, active states."
    },
    "surface": {
      "base": {
        "$value": "oklch(0.98 0.005 250)",
        "$type": "color",
        "$description": "Default page/card background. Slightly warm-tinted."
      }
    }
  }
}
```

---

## Color Psychology by Sector

Brief reference — see `sector-style-intelligence` for full sector analysis.

| Sector | Primary Colors | Psychology | Notes |
|---|---|---|---|
| **Fintech** | Blue (#0052FF Coinbase), Green (#00C805 Robinhood) | Trust, growth, stability | Avoid red (loss), warm colors (impulsive) |
| **Healthcare** | White, light blue (#0077C8), teal | Clinical, clean, trustworthy | High contrast for accessibility. Calm, not exciting. |
| **Social/Consumer** | Vibrant, warm (Instagram gradient, Snapchat yellow) | Energy, connection, fun | Bold, saturated, memorable. Icon color IS brand. |
| **SaaS/Dev Tools** | Dark themes, blue/purple accents (Vercel, Linear) | Focus, productivity, technical | Dark mode default. Muted accents. Monochrome + 1 color. |
| **E-commerce** | Orange (#FF9900 Amazon), green (buy/add to cart) | Action, urgency, value | High-contrast CTAs. Price in large, bold type. |
| **Education** | Friendly blues, greens, warm accents | Approachable, supportive, clear | Avoid harsh colors. Warm, inclusive palette. |
| **Luxury** | Black, gold (#C5A572), white | Exclusivity, quality, timelessness | Restrained palette. Color through photography, not UI chrome. |
| **Climate/Sustainability** | Greens, earth tones, natural hues | Nature, responsibility, growth | Desaturated, natural feeling. Avoid artificial-looking colors. |

---

## Practical Color Workflows

### Starting a New Palette

1. **Choose one brand color** in oklch: oklch(L C H)
2. **Generate tonal scale**: 11 steps from L=0.97 to L=0.20
3. **Generate tinted neutrals**: same H, C=0.01-0.02, 11 lightness steps
4. **Add semantic colors**: rotate H for green (+130), amber (-170), red (-225)
5. **Generate dark mode**: increase L by 0.20, decrease C by 0.08 for accents
6. **Test contrast**: every text/background pair at APCA Lc 75+ for body
7. **Test colorblind**: simulate protanopia, deuteranopia, tritanopia
8. **Document**: assign semantic names, export as tokens

### Auditing an Existing Palette

1. **Collect** every color value in the codebase (grep for hex, rgb, hsl, oklch)
2. **Count** unique values (target: <30 for a mature product)
3. **Check** contrast for all text/background pairs
4. **Identify** unnamed/one-off colors (each should map to a token)
5. **Test** dark mode (screenshot comparison)
6. **Score** using the Color dimension of the Visual Scoring Framework

---

## Brand Color Systems and Dark Mode Strategy

### Brand Color Systems

A complete brand color system includes: primary (hero + scale), secondary (complementary + scale), accent (for moments of delight), neutrals (warm or cool tinted), semantic (success, warning, error, info), surface (layered backgrounds for elevation), and interactive (hover, active, focus, disabled modifications of primary).

### Dark Mode Color Strategy

Dark mode is a parallel color system, not an inversion. Key principles:
- Background: not pure black (#000). Use dark gray (oklch 0.15-0.20 with brand hue tint).
- Surfaces: each elevation layer gets +2-3% lightness. Background < Card < Modal < Tooltip.
- Text: not pure white. Use off-white (oklch 0.93-0.95) for body, slightly brighter (0.97) for headings.
- Colors: reduce chroma by 15-25% from light mode values. Saturated colors vibrate on dark backgrounds.
- Shadows: nearly invisible in dark mode. Replace with subtle borders or increased background lightness for elevation.

## Palette Refinement

**Algorithmic Approaches**

1. **Lightness ramp method**: Fix hue and chroma, vary lightness in equal OKLCH steps. Produces consistent tonal scales.
2. **Chroma curve method**: Increase chroma toward mid-tones, decrease at extremes (lights and darks). Mimics natural color behavior and prevents neon artifacts at mid-range.
3. **Hue rotation method**: Apply slight hue shifts across the lightness ramp (e.g., blue shifts toward purple in dark tones, toward cyan in light tones). Creates richer, more natural-feeling palettes.

**Hand-Tuning**

After algorithmic generation, adjust by eye:

- Ensure the darkest step (900) works as text on white and the lightest step (100) works as a background.
- Verify mid-range steps (400-600) meet WCAG AA contrast against both white and dark surfaces.
- Check that adjacent steps are distinguishable from each other; merge any steps that appear identical.

Generate 9-11 steps per color for maximum flexibility. At minimum, produce 5 steps: lightest background, light, mid, dark, darkest text.

**Brand color integrity**: Never modify the exact brand color value for primary usage (logos, brand marks). Adjust derived UI colors (hover states, backgrounds, borders) freely within the generated scale.

## Color for Data Visualization

**Sequential Palettes**

Use a single-hue lightness ramp for ordered data (low-to-high). Ensure at least 3:1 contrast ratio between adjacent stops when the palette encodes fewer than 7 values.

**Diverging Palettes**

Use two hues (one warm, one cool) diverging from a neutral midpoint. Ensure the two endpoints are distinguishable under all forms of color vision deficiency — pair blue-orange or purple-green rather than red-green.

**Categorical Palettes**

Assign colors that are maximally distinguishable in hue and lightness. Limit categorical palettes to 8-10 colors maximum; beyond that, use patterns, shapes, or labels.

- Test categorical palettes with a color blindness simulator (Sim Daltonism, Coblis).
- Ensure every category is identifiable by a non-color cue (shape, pattern, label, position).

## Cultural Color Associations

Color meaning varies by culture. Account for this in products serving international audiences.

| Color | Western | East Asian | Middle Eastern | South Asian |
|-------|---------|------------|----------------|-------------|
| Red | Danger, passion, urgency | Luck, prosperity, celebration | Danger, caution | Purity (in marriage), fertility |
| White | Purity, cleanliness | Mourning, death | Purity, peace | Mourning (in some contexts) |
| Green | Nature, growth, money | Youth, fertility | Islam, paradise, prosperity | Fertility, happiness |
| Yellow | Caution, warmth | Royalty, sacred | Happiness, prosperity | Sacred, auspicious |
| Black | Elegance, mourning | Power, mystery | Mourning, evil | Evil, negativity |

Do not rely on color alone to convey meaning. Always pair color with text labels, icons, or patterns so the message persists regardless of cultural interpretation.

## Dark Mode Elevation by Lightness

An alternative to surface tinting: step OKLCH lightness per elevation level.

| Elevation | OKLCH Lightness | Use |
|-----------|----------------|-----|
| Base (dp 0) | 0.15 | App background |
| Surface (dp 1) | 0.18 | Cards, sheets |
| Raised (dp 4) | 0.21 | App bars, menus |
| Overlay (dp 8) | 0.24 | Dialogs, modals |
| Top (dp 16) | 0.27 | Popovers, tooltips |

**Brand Color in Dark Contexts**

If the brand color is dark (low lightness), use a lighter tint (300-400 step) as the primary interactive color in dark mode. Never place a dark brand color on a dark surface where contrast falls below 3:1.

## CSS Color Functions

**`color-mix()`**

Blend two colors in any color space:

```css
/* 30% white mixed into the brand color in OKLCH space */
--brand-light: color-mix(in oklch, var(--brand) 70%, white);

/* 50/50 blend for a hover midpoint */
--hover: color-mix(in oklch, var(--primary), var(--secondary));
```

Always specify `in oklch` for perceptually uniform mixing.

**`oklch()` Function**

```css
--color: oklch(0.65 0.2 250);
--color-alpha: oklch(0.65 0.2 250 / 0.5);
```

**Relative Color Syntax**

Derive new colors from existing ones by modifying individual channels:

```css
--primary: oklch(0.55 0.2 250);
/* Lighten by adding 0.2 to lightness */
--primary-light: oklch(from var(--primary) calc(l + 0.2) c h);
/* Desaturate by halving chroma */
--primary-muted: oklch(from var(--primary) l calc(c / 2) h);
/* Shift hue by 30 degrees */
--secondary: oklch(from var(--primary) l c calc(h + 30));
```

Relative color syntax eliminates the need for pre-generated palette steps in many cases, enabling dynamic theme generation with minimal tokens.

## Typography and Color as One System

### Hierarchy Through Combined Systems

Build visual hierarchy using both type scale and color simultaneously:

- **Primary content**: Largest appropriate type step + highest contrast text color (`text.primary`).
- **Secondary content**: One step smaller + reduced contrast (`text.secondary` or reduced opacity).
- **Tertiary/metadata**: Smallest type step + lowest contrast (`text.tertiary`), minimum 4.5:1 against background.

### Testing Typography and Color as a System

- Generate a type specimen page showing every heading level, body variant, and caption with the full color palette applied.
- Test the specimen page under simulated color vision deficiency.
- Validate every text-on-background combination against WCAG AA at minimum.
- Review the specimen on macOS, Windows, iOS, and Android for rendering consistency.
- Print the specimen (or view in grayscale) to verify hierarchy is maintained without color.

Treat typography and color as interdependent systems. Changes to one always affect the other. Audit both simultaneously during design reviews and accessibility testing.
