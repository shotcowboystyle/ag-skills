# Cross-Platform Design Harmony

## The Multi-Platform Challenge

Modern products must work across 9 form factors: phone, tablet, desktop, TV, watch, spatial (XR), automotive, kiosk, and e-ink. Each has different screen sizes, input methods, viewing distances, and platform conventions. The challenge is maintaining brand coherence and design system consistency while respecting each platform's native idioms.

The answer is NOT "one design for all platforms." The answer is one design SYSTEM that adapts intelligently to each platform.

---

## The 9 Form Factors

| Form Factor | Screen Size | Distance | Input | Key Constraint |
|-------------|------------|----------|-------|----------------|
| Phone | 5.5-6.9" | 10-14" | Touch | One-handed reach |
| Tablet | 8.3-13" | 14-20" | Touch + Pencil | Two orientations |
| Desktop | 13-34" | 18-30" | Mouse + keyboard | Precision pointer |
| TV | 40-85" | 8-12 ft | D-pad remote | No precision input |
| Watch | 1.5-2" | 8-14" | Crown + tap | Glanceability |
| Spatial (XR) | FOV-based | 1-10 ft | Eye + hand | Depth axis |
| Automotive | 6.5-15" | 18-30" | Touch + voice | Safety (< 2s glance) |
| Kiosk | 15-55" | 12-24" | Touch | Public use, linear flow |
| E-Ink | 6-13" | 10-18" | Touch + pen | No animation |

---

## Token Architecture for Multi-Platform

Design tokens are the bridge between a unified design system and platform-specific implementations. A well-structured token architecture has three layers.

### Layer 1: Global Tokens (Platform-Agnostic)

These represent the brand's design decisions independent of any platform:

```json
{
  "color": {
    "brand-primary": { "value": "oklch(0.55 0.20 250)" },
    "brand-secondary": { "value": "oklch(0.65 0.15 145)" },
    "neutral-10": { "value": "oklch(0.10 0.01 250)" },
    "neutral-90": { "value": "oklch(0.90 0.01 250)" },
    "semantic-error": { "value": "oklch(0.55 0.22 25)" },
    "semantic-success": { "value": "oklch(0.55 0.18 145)" }
  },
  "font": {
    "family-primary": { "value": "Inter Variable" },
    "family-mono": { "value": "JetBrains Mono" },
    "weight-regular": { "value": 400 },
    "weight-medium": { "value": 500 },
    "weight-bold": { "value": 700 }
  },
  "spacing": {
    "unit": { "value": 4 },
    "xs": { "value": 4 },
    "sm": { "value": 8 },
    "md": { "value": 16 },
    "lg": { "value": 24 },
    "xl": { "value": 32 },
    "2xl": { "value": 48 }
  },
  "radius": {
    "sm": { "value": 4 },
    "md": { "value": 8 },
    "lg": { "value": 16 },
    "full": { "value": 9999 }
  }
}
```

### Layer 2: Semantic Tokens (Context-Aware)

Map global tokens to semantic roles:

```json
{
  "color": {
    "surface-primary": { "value": "{color.neutral-90}" },
    "surface-elevated": { "value": "{color.neutral-90}" },
    "text-primary": { "value": "{color.neutral-10}" },
    "text-secondary": { "value": "{color.neutral-10}", "alpha": 0.7 },
    "interactive-primary": { "value": "{color.brand-primary}" },
    "interactive-hover": { "value": "{color.brand-primary}", "lighten": 10 },
    "feedback-error": { "value": "{color.semantic-error}" },
    "feedback-success": { "value": "{color.semantic-success}" }
  },
  "size": {
    "touch-target-min": { "value": "{spacing.2xl}" },
    "icon-sm": { "value": 16 },
    "icon-md": { "value": 24 },
    "icon-lg": { "value": 32 }
  }
}
```

### Layer 3: Platform-Specific Overrides

Each platform overrides semantic tokens where its conventions differ.

> The `motion.curve` values below are **platform-native springs** (SwiftUI `spring(response:dampingFraction:)` on iOS; the Material 3 Expressive default spatial spring, stiffness 380 / damping ratio 0.8, on Android). They are not the product's base motion scale; for base durations and easings see `interaction-motion-design` (its `animation-timing-curves.md` reference).

```json
{
  "ios": {
    "font.family-primary": "SF Pro",
    "radius.md": 10,
    "radius.lg": 20,
    "size.touch-target-min": 44,
    "spacing.margin-screen": 16,
    "motion.curve": "spring(response: 0.35, dampingFraction: 0.85)"
  },
  "android": {
    "font.family-primary": "Roboto",
    "radius.md": 12,
    "radius.lg": 16,
    "size.touch-target-min": 48,
    "spacing.margin-screen": 16,
    "motion.curve": "spring(stiffness: 380, dampingRatio: 0.8)"
  },
  "web": {
    "font.family-primary": "Inter Variable, system-ui, sans-serif",
    "radius.md": 8,
    "radius.lg": 16,
    "size.touch-target-min": 44,
    "spacing.margin-screen": "clamp(16px, 4vw, 64px)"
  },
  "tv": {
    "font.family-primary": "system-ui",
    "font.weight-regular": 500,
    "size.touch-target-min": 60,
    "size.text-body": 28,
    "spacing.margin-screen": "5%"
  },
  "watch": {
    "font.family-primary": "SF Compact",
    "size.text-body": 17,
    "size.touch-target-min": 44,
    "spacing.margin-screen": 8,
    "color.surface-primary": "#000000"
  },
  "automotive": {
    "font.family-primary": "SF Pro",
    "size.touch-target-min": 76,
    "size.text-body": 24,
    "spacing.gap-interactive": 23,
    "color.surface-primary": "#121212"
  }
}
```

### Token Build Pipeline

```
Global Tokens (JSON/YAML)
    │
    ├── Style Dictionary / Tokens Studio
    │
    ├──► iOS: Swift Color/Font extensions
    ├──► Android: Compose Theme / XML resources
    ├──► Web: CSS custom properties
    ├──► TV: platform-specific theme
    ├──► Watch: compact theme overrides
    └──► Figma: synced variables
```

Tools: Style Dictionary (Amazon), Tokens Studio (Figma plugin), Specify, Supernova — all can transform a single token source into multi-platform outputs.

---

## Platform Adaptation Patterns

### Pattern 1: Component Morphing

The same logical component takes different visual forms per platform:

**Button**
- iOS: rounded rectangle, SF Pro medium, system tint
- Android: pill shape (M3), Roboto medium, primary container color
- Web: 8px radius, Inter, brand primary
- TV: large rectangle, focused state with scale + glow
- Watch: full-width, tappable row
- Automotive: extra-large touch target, high contrast

The button's purpose is identical. Its appearance adapts to where the user encounters it.

### Pattern 2: Navigation Transformation

Navigation must fundamentally change across form factors:

| Form Factor | Primary Navigation |
|-------------|-------------------|
| Phone | Bottom tab bar (4-5 items) |
| Tablet (portrait) | Bottom tab bar or side rail |
| Tablet (landscape) | Side navigation rail |
| Desktop | Side navigation drawer or top nav bar |
| TV | Top tab bar or side rail (focus-driven) |
| Watch | List menu or page-based swipe |
| Spatial | Ornament toolbar or tabbed window |
| Automotive | Template-enforced tabs (limited) |
| Kiosk | Step-based wizard (no persistent nav) |

### Pattern 3: Information Density Scaling

Content density must scale with screen size and viewing distance:

| Form Factor | Density | Example |
|-------------|---------|---------|
| Watch | Ultra-low | 1 data point per screen |
| Phone | Low | 5-8 list items visible |
| Tablet | Medium | 10-15 list items or 2-column grid |
| Desktop | High | Dense tables, multi-pane layouts |
| TV | Low | 3-5 large cards per row |
| Spatial | Low-Medium | 1 window of focused content |
| Automotive | Ultra-low | 1 data point + 1 action |
| E-Ink | Low | Page-based, print-like density |

### Pattern 4: Input Adaptation

Design for the primary input method, accommodate secondary methods:

| Form Factor | Primary Input | Secondary Input | Design Implication |
|-------------|--------------|-----------------|-------------------|
| Phone | Touch (thumb) | Voice | Bottom-weighted layout, thumb zones |
| Tablet | Touch (fingers) | Pencil, keyboard | Larger targets, hover support |
| Desktop | Mouse + keyboard | Touch (2-in-1) | Hover states, keyboard shortcuts |
| TV | D-pad remote | Voice | Focus system, no hover |
| Watch | Crown + tap | Voice, double-tap | Minimal interaction per task |
| Spatial | Eye + pinch | Voice, keyboard | 60pt targets, hover on gaze |
| Automotive | Voice | Touch | Voice-first, huge touch targets |
| Kiosk | Touch | Accessibility switch | Large targets, ADA height |
| E-Ink | Touch | Pen, buttons | Page turns, not scrolling |

### Pattern 5: Motion Adaptation

Animation behavior must change across platforms:

| Form Factor | Motion Approach |
|-------------|----------------|
| Phone | Spring-based, gesture-driven, 60fps |
| Tablet | Same as phone, wider canvas |
| Desktop | Subtle, duration-based (200-300ms), cursor-driven |
| TV | Scale and fade on focus, parallax layers |
| Watch | Minimal, quick transitions |
| Spatial | Spring-based, depth transitions, 90fps minimum |
| Automotive | None or minimal (< 2s glance = no time for animation) |
| Kiosk | Directional slides between steps |
| E-Ink | None — instant page transitions only |

---

## When to Diverge vs. Converge

### CONVERGE (Keep Consistent Across Platforms)

- **Brand colors**: same palette everywhere (with accessibility adjustments per platform)
- **Brand typeface**: same family (swap to platform system font for chrome, keep brand font for content)
- **Iconography style**: same icon set (adapt size and weight per platform)
- **Illustration style**: same visual language for illustrations
- **Terminology**: same labels, same copy, same microcopy
- **Content hierarchy**: same information architecture (adapted layout, same structure)
- **Accessibility standards**: WCAG AA minimum everywhere
- **Animation easing feel**: same "personality" (bouncy, snappy, smooth) even if technical implementation differs

### DIVERGE (Adapt to Platform Conventions)

- **Navigation pattern**: tab bar (phone) vs. rail (tablet) vs. drawer (desktop) vs. focus grid (TV)
- **System font for chrome**: SF Pro (iOS), Roboto (Android), system-ui (web)
- **Touch target sizes**: 44pt (iOS), 48dp (Android), 60pt (visionOS), 76dp (automotive)
- **Corner radius values**: continuous/squircle (iOS), circular (Android), CSS (web)
- **Motion curves**: platform-native spring specs differ between iOS (response + damping fraction) and Android (stiffness + damping ratio); see `ios-26-liquid-glass.md` and `material-3-expressive.md`
- **Color system integration**: Dynamic Color (Android), system accent (iOS), CSS custom properties (web)
- **Sheet/modal behavior**: iOS half-sheet vs. Android bottom sheet vs. web dialog
- **Back navigation**: swipe-back (iOS), predictive back (Android), browser back (web)
- **Dark mode implementation**: system materials (iOS), surface tints (Android), prefers-color-scheme (web)

---

## Cross-Platform Design System Checklist

### Foundation

- [ ] Single source of truth for design tokens (JSON/YAML)
- [ ] Token build pipeline producing platform-specific outputs
- [ ] Figma library with platform variants for components
- [ ] Shared icon set with platform-specific sizing
- [ ] Brand guidelines that specify what converges and what diverges

### Per-Platform Validation

- [ ] iOS: follows HIG, uses system materials, supports Dynamic Type
- [ ] Android: follows Material 3, supports Dynamic Color, uses canonical layouts
- [ ] Web: uses semantic HTML, supports keyboard navigation, responsive without breakpoint-only design
- [ ] TV: 10-foot UI validated, focus navigation tested, safe zones respected
- [ ] Watch: glanceability validated (< 3 seconds), complication designed
- [ ] Spatial: 60pt targets, depth hierarchy limited, hover states visible
- [ ] Automotive: NHTSA compliance (< 2s glance, < 12s task), voice-first validated
- [ ] Kiosk: ADA height range, linear workflow (< 5 steps), timeout handling
- [ ] E-Ink: no animations, pure black/white text, page-based layout

### Governance

- [ ] Component API parity: same logical components exist on every supported platform
- [ ] Platform delta documentation: what differs and why
- [ ] Cross-platform QA matrix: test matrix covering platform x feature x device
- [ ] Deprecation policy: how platform-specific patterns are retired
- [ ] Update cadence: token refresh schedule aligned with OS releases (WWDC, I/O, etc.)

---

## Implementation Frameworks

### React Native / Expo

- Single JavaScript/TypeScript codebase
- Platform-specific code via `Platform.OS` checks or `.ios.tsx` / `.android.tsx` files
- Paper (old) vs. Fabric (new) architecture
- Expo provides managed workflow with OTA updates
- Good for: phone + tablet, some desktop (Windows/macOS via react-native-windows/macos)
- Not suitable for: TV, watch, automotive, spatial, e-ink

### Flutter

- Single Dart codebase
- Material 3 default, Cupertino widgets for iOS feel
- Platform-adaptive widgets: `Switch.adaptive()`, `Slider.adaptive()`
- Good for: phone, tablet, desktop, web
- Experimental: TV (community), embedded (kiosk)
- Not suitable for: watch (limited), automotive, spatial

### Kotlin Multiplatform (KMP)

- Shared business logic in Kotlin
- Platform-native UI: SwiftUI (iOS), Compose (Android), Compose Multiplatform (desktop/web)
- Best platform fidelity — each UI is truly native
- Good for: phone, tablet, desktop, web, Wear OS
- Not suitable for: TV (separate Leanback), automotive (separate AAOS)

### SwiftUI (Apple Ecosystem)

- Single framework across iOS, iPadOS, macOS, watchOS, tvOS, visionOS
- Same code with conditional compilation: `#if os(watchOS)`
- Platform-specific modifiers: `.navigationBarTitleDisplayMode()` (iOS) vs. `.navigationSubtitle()` (macOS)
- Perfect for: all Apple platforms
- Not available for: Android, web, automotive (non-CarPlay)

### Web (PWA + Responsive)

- HTML/CSS/JavaScript
- Single codebase for all screen sizes via responsive design
- PWA for installability on phone, tablet, desktop
- WebXR for spatial experiences
- Good for: any device with a browser
- Limitations: no watch (too small), limited automotive, no native platform feel

---

## Decision Matrix: Which Platforms to Support

When deciding which form factors to prioritize, score each on these axes:

| Axis | Question |
|------|----------|
| **User need** | Do your users actually use this form factor for this task? |
| **Task fit** | Does the task fit the form factor's constraints? |
| **Business value** | Does supporting this platform drive revenue, retention, or reach? |
| **Technical cost** | What is the engineering and maintenance cost? |
| **Platform maturity** | Is the platform's design system stable or rapidly changing? |

### Common Platform Strategies

**Mobile-First**
Phone → Tablet → Web → Desktop
Best for: consumer apps, social, commerce, media

**Desktop-First**
Desktop → Web → Tablet → Phone
Best for: productivity, enterprise, developer tools

**Screen-Agnostic**
Web (responsive) → PWA → native where needed
Best for: content platforms, SaaS, dashboards

**Ecosystem-Locked**
iOS full stack (iPhone + iPad + Mac + Watch + TV + Vision Pro)
Best for: premium consumer apps, Apple ecosystem plays

**Everywhere**
Phone + Tablet + Desktop + TV + Watch + Auto + Spatial
Best for: platform companies (Google, Apple, Spotify, Google Maps)

---

## Anti-Patterns in Cross-Platform Design

### The Pixel-Perfect Trap
Trying to make every platform look identical. Users expect platform-native conventions. A Material app on iOS or an iOS-styled app on Android both feel wrong.

### The Lowest Common Denominator
Designing for the most constrained platform and using that design everywhere. A watch-appropriate interface is useless on desktop. Design for each platform's strengths.

### Ignoring Platform Updates
Apple and Google update their design systems annually (WWDC, Google I/O). A design system that does not track these updates falls behind quickly. Budget for annual platform alignment.

### Over-Abstracting Components
Making components so abstract they lose platform meaning. A "dialog" component that looks the same on iOS, Android, and web feels native nowhere. Allow platform-specific rendering within shared APIs.

### Single-Breakpoint Responsive
Using only phone and desktop breakpoints. Tablet, foldable, and large-screen phone experiences are distinct — they need dedicated attention, not just a scaled-up phone layout.

---

## Quick Specifications: Device Matrix and Tokens

### Device Matrix

| Device | Screen Range | Input | Viewing Distance | Primary Context |
|--------|-------------|-------|-------------------|----------------|
| Phone | 320-430pt width | Touch | 30cm (handheld) | Mobile, one-handed |
| Tablet | 744-1024pt width | Touch + Pencil | 40-50cm (lap/table) | Lean-back, productivity |
| Desktop | 1024-2560pt width | Mouse + keyboard | 50-70cm (desk) | Focused work |
| Watch | 162-205px width | Crown + tap | 25-30cm (wrist) | Glanceable |
| TV | 1920-3840px width | D-pad + voice | 2-4 meters (couch) | Lean-back entertainment |
| Car | 800-1920px width | Touch + voice | 50-70cm (dash) | Distracted, safety-critical |
| XR Headset | Virtual canvas | Eye + hand | 1-3m (virtual) | Immersive |
| Foldable | 320-886pt width | Touch | 30-40cm (handheld) | Dual-mode |
| E-Ink | 758-1872px width | Touch (slow) | 30cm (handheld) | Reading, low-power |

### Shared Design Tokens

A cross-platform design system defines tokens at three levels:

1. **Global tokens** — Platform-agnostic values: brand colors (oklch), font scale ratios, spacing multipliers, border-radius scale
2. **Alias tokens** — Semantic mappings: `color-surface`, `color-on-surface`, `spacing-md`, `radius-card`. Same name everywhere, different values per platform.
3. **Component tokens** — Platform-specific overrides: `button-height` is 44pt on iOS, 48dp on Android, 36px on web, 72px on TV.

### Platform-Specific Adaptations

| Pattern | iOS | Android | Web | Watch | TV |
|---------|-----|---------|-----|-------|-----|
| Primary nav | Bottom tab bar (floating) | Bottom nav bar | Top nav or sidebar | Page-based scroll | Top rail + sidebar |
| Back navigation | Swipe from left edge | System back button/gesture | Browser back or breadcrumb | Swipe right | Back button on remote |
| Selection | Checkmark | Checkbox | Checkbox | Tap highlight | Focus + select |
| Destructive action | Swipe-to-delete | Long-press menu | Button with confirmation | Force Touch menu | Focus + hold |
| Search | Pull-down search bar | Top app bar search | Search field in header | Scribble or voice | Voice or on-screen keyboard |

### Responsive Breakpoints by Device

| Breakpoint | Width | Target |
|-----------|-------|--------|
| xs | 0-319pt | Small watch |
| sm | 320-430pt | Phone |
| md | 431-743pt | Large phone / foldable inner |
| lg | 744-1023pt | Tablet |
| xl | 1024-1365pt | Small desktop / tablet landscape |
| 2xl | 1366-1920pt | Standard desktop |
| 3xl | 1921pt+ | Large desktop / TV |

### Foldable-Specific Considerations

- **Outer screen** — Treat as phone (320-430pt). Show condensed single-column layout.
- **Inner screen (unfolded)** — Treat as small tablet (744-886pt). Show two-pane layout.
- **Fold-aware layout** — Content should not cross the fold hinge. Place the layout seam on the hinge, creating a natural two-pane boundary.
- **Continuity** — When the user unfolds the device, the app must seamlessly transition from the outer layout to the inner layout without losing state or scroll position.

### E-Ink Considerations

- **No animation** — E-ink refresh is 200-500ms. Animations appear as ghostly smears. Use instant state changes.
- **High contrast** — E-ink displays have lower contrast ratios than LCD/OLED. Use pure black on pure white. Avoid grays below #333333 or above #CCCCCC.
- **No color dependency** — Most e-ink displays are grayscale. Never encode meaning in color alone.
- **Large text** — Minimum 14pt body text. E-ink pixel density is typically 212-300 PPI (lower than phones at 400-600 PPI).
- **Minimal chrome** — Every pixel of UI chrome is a pixel not showing content. On a reading device, content is everything.

---

## Platform Detection Patterns

### When to Adapt vs When to Unify

**Adapt to the platform** when:
- The OS provides a native control that users expect (e.g., iOS date picker, Android bottom sheet)
- Navigation patterns differ fundamentally (tab bar vs navigation drawer)
- System gestures conflict with custom gestures (iOS swipe-back, Android system back)
- Accessibility APIs differ (VoiceOver vs TalkBack rotor patterns)
- Legal requirements differ by platform (NHTSA for automotive, WCAG for web)

**Unify across platforms** when:
- Brand identity requires visual consistency (color palette, typography, iconography)
- The interaction is domain-specific and has no platform equivalent (e.g., a custom chart interaction)
- Users frequently switch between platforms and expect continuity (e.g., Figma on web vs desktop app)
- The cost of maintaining platform-specific implementations exceeds the UX benefit

### User Expectations Per Platform

| Platform | Users Expect | Users Reject |
|----------|-------------|-------------|
| iOS | Smooth 60fps, system gestures respected, Liquid Glass materials, SF Symbols | Android-style hamburger menus, Material FABs, system font overrides |
| Android | Material components, Dynamic Color, predictable back behavior | iOS-style non-standard back navigation, tab bars without labels |
| Web | Fast load times, keyboard accessibility, URL-based state, responsive | Native app idioms forced onto web (e.g., mobile tab bar on desktop) |
| Watch | Instant information, minimal interaction, complications | Full-screen forms, long text, complex navigation hierarchies |
| TV | Focus-visible at all times, large text, card grids | Tiny text, hover-dependent interactions, touch assumptions |
| Car | Voice-first, huge touch targets, zero cognitive load | Text-heavy displays, small buttons, multi-step flows |
| XR | Spatial depth, gaze responsiveness, comfortable ergonomics | Flat 2D panels with no spatial awareness, tiny targets |

---

## Design Token Mapping Across Platforms

### CSS Custom Properties to SwiftUI Environment to Compose Theme

| Semantic Role | CSS Custom Property | SwiftUI | Compose (M3) |
|--------------|--------------------|---------|----|
| Primary color | `--color-primary` | `Color.accentColor` | `MaterialTheme.colorScheme.primary` |
| Surface | `--color-surface` | `Color(.systemBackground)` | `MaterialTheme.colorScheme.surface` |
| On-surface text | `--color-on-surface` | `Color(.label)` | `MaterialTheme.colorScheme.onSurface` |
| Error | `--color-error` | `Color(.systemRed)` | `MaterialTheme.colorScheme.error` |
| Border radius (sm) | `--radius-sm: 8px` | `.clipShape(RoundedRectangle(cornerRadius: 8))` | `shape = RoundedCornerShape(8.dp)` |
| Border radius (lg) | `--radius-lg: 16px` | `.clipShape(RoundedRectangle(cornerRadius: 16))` | `shape = RoundedCornerShape(16.dp)` |
| Spacing unit | `--space-md: 16px` | `.padding(16)` | `Modifier.padding(16.dp)` |
| Elevation (low) | `box-shadow: 0 1px 3px` | `.shadow(radius: 2)` | `tonalElevation = 1.dp` |
| Elevation (high) | `box-shadow: 0 8px 24px` | `.shadow(radius: 8)` | `tonalElevation = 4.dp` |
| Body font | `font-family: var(--font-body)` | `.font(.body)` | `MaterialTheme.typography.bodyLarge` |
| Title font | `font-family: var(--font-title)` | `.font(.title)` | `MaterialTheme.typography.titleLarge` |
| Caption font | `font-family: var(--font-caption)` | `.font(.caption)` | `MaterialTheme.typography.labelSmall` |

### Token Translation Strategy

1. **Define once in a neutral format** — Use JSON or YAML as the source of truth (e.g., Style Dictionary, Tokens Studio)
2. **Transform per platform** — Generate CSS custom properties, SwiftUI extensions, and Compose theme objects from the same source
3. **Override at the platform layer** — iOS gets `thinMaterial` for surface, Android gets tonal elevation, web gets `backdrop-filter: blur()`
4. **Test with a visual diff** — Render the same screen on all three platforms and compare. Token mapping is correct when the screens feel like siblings, not clones.

### Token File Structure

```
tokens/
  global/
    color.json        # oklch values, brand palette
    spacing.json      # 4px base unit scale
    typography.json    # font scale ratios
    radius.json       # border-radius scale
  platform/
    ios.json          # SwiftUI overrides, Liquid Glass materials
    android.json      # M3 overrides, Dynamic Color hooks
    web.json          # CSS custom property names, rem conversions
    watch.json        # Compact sizing overrides
    tv.json           # 10-foot UI sizing overrides
    car.json          # Large touch target overrides
    xr.json           # Spatial depth tokens
```
