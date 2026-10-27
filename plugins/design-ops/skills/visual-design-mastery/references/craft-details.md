# Craft Details

> Micro-craft (alignment, subpixel rendering, optical adjustments), a baseline elevation scale, and iconography rules.

---

## Micro-Craft Details

### Pixel-Perfect Alignment

The difference between good and great lives at the subpixel level.
- Align all text baselines across columns. If two columns of text are side by side, their baselines should match.
- Icon optical centering: geometric center is not always visual center. A play button triangle needs to shift ~10% right to appear centered.
- Button text: vertically center text using line-height matching the button height, not padding. Padding-based centering causes text to shift with font metrics.
- Border alignment: use box-sizing: border-box universally. A 1px border should not shift element dimensions.

### Subpixel Rendering Awareness

- Render thin lines (1px) on full pixel boundaries to avoid blurring on 1x displays.
- Use transform: translateZ(0) to force GPU rendering for smoother animations.
- Test designs on both 1x and 2x displays. Details visible on Retina may disappear on standard screens.
- Use -webkit-font-smoothing: antialiased on macOS for consistent text rendering (lighter text weight).

### Optical Adjustments

Mathematical precision does not always equal visual precision. Common optical corrections:
- Round shapes (circles, os) need to extend slightly beyond flat shapes (squares, Hs) to appear the same size.
- Pointed shapes (triangles, As) need to extend even further.
- Horizontal lines appear heavier than vertical lines at the same width — compensate.
- Text in ALL CAPS appears smaller than mixed case at the same font-size — increase size by ~5%.
- Dark elements on light backgrounds appear to bleed/expand — reduce size slightly. Light elements on dark backgrounds appear to shrink — increase size slightly (irradiation illusion).

---

## Elevation and Depth

### Elevation System

Baseline scale only. The full shadow and elevation system lives in `shadow-elevation-density`.

```
Level 0: Flat surface (0px shadow) — background, canvas
Level 1: Low (0 1px 3px rgba(0,0,0,0.12)) — cards, tiles
Level 2: Medium (0 4px 6px rgba(0,0,0,0.12)) — dropdowns, popovers
Level 3: High (0 8px 16px rgba(0,0,0,0.12)) — modals, dialogs
Level 4: Highest (0 16px 32px rgba(0,0,0,0.16)) — toasts, floating elements
```

- Higher elevation = closer to user = more important/temporary
- Use elevation consistently: persistent UI at level 0-1, transient UI at level 2-4
- Dark mode: use surface tint (lighter background) instead of shadow for elevation

---

## Iconography

### Icon Design Rules

Icon sets, grids and illustration systems live in `icon-illustration-systems`.

- Consistent style: outline OR filled, not mixed (pick one system-wide)
- Minimum touch target: 44x44pt even if icon is visually 24x24
- Always pair icons with text labels in navigation — icons alone are ambiguous
- Standard sizes: 16px (inline), 20px (buttons), 24px (navigation), 32px (feature)
- Consistent stroke width across all icons (typically 1.5-2px at 24px size)
