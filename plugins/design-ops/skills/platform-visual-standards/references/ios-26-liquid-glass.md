# iOS 26 Liquid Glass Design Standards

## What Is Liquid Glass

Liquid Glass is the defining visual language of iOS 26, iPadOS 26, macOS Tahoe, watchOS 26, and visionOS 26. It gives UI components the optical qualities of physical glass — light refraction, specular highlights, depth-aware translucency, and motion-responsive reflections. Liquid Glass creates a layered spatial hierarchy where navigation chrome floats above content with a distinct material presence.

### The Cardinal Rule

Liquid Glass is ONLY for the navigation layer — tab bars, toolbars, sidebars, and navigation bars that float ABOVE content. NEVER apply Liquid Glass to content itself (lists, tables, cards, media, text areas). Content remains on opaque or subtly tinted surfaces. Violating this rule destroys the spatial hierarchy that makes Liquid Glass work.

### Why Apple Made This Change

iOS 26 represents the largest visual redesign since iOS 7. The motivation is spatial consistency — as Apple's platforms span iPhone, iPad, Mac, Apple Watch, Apple TV, and Vision Pro, a unified material language creates coherence across 2D and 3D contexts. Liquid Glass on a flat screen hints at the same material used in visionOS spatial windows.

---

## Material Tiers

Apple provides four material thickness tiers that control how much background content bleeds through the glass surface. Each tier is designed for specific use cases.

> Note: the SwiftUI `Material` tiers below (`.ultraThinMaterial` ... `.thickMaterial`, plus `.ultraThickMaterial`) are the pre-iOS 26 blur materials and remain available. Liquid Glass itself is applied with `.glassEffect()` (variants `.regular` and `.clear`) and is what system bars use on iOS 26. Use the tiers for custom backgrounds and as the fallback on iOS 25 and earlier.

Approximate rendering values (unverified — not published by Apple; use only as a starting point for mockups):

| Material | Background Blur Radius | Saturation Boost | Use Case |
|----------|----------------------|------------------|----------|
| `ultraThinMaterial` | 8pt | 1.2x | Full-screen ambient overlays |
| `thinMaterial` | 16pt | 1.4x | Popovers, menus |
| `regularMaterial` | 24pt | 1.6x | Sheets, bars on older iOS |
| `thickMaterial` | 40pt | 1.8x | Alerts, critical modals |
| `ultraThickMaterial` | 64pt | 2.0x | Focused input contexts |

### Ultra-Thin Material
- **Blur radius**: Minimal — background is mostly visible
- **Use case**: Full-screen overlays where context must remain visible (e.g., Control Center background)
- **SwiftUI**: `.ultraThinMaterial`
- **Visual effect**: Very subtle frosted appearance, high background legibility

### Thin Material
- **Blur radius**: Light — background is partially visible
- **Use case**: Popovers, menus, and transient UI that benefits from environmental context
- **SwiftUI**: `.thinMaterial`
- **Visual effect**: Noticeable frosting, background shapes recognizable but not readable

### Regular Material
- **Blur radius**: Standard — balanced translucency
- **Use case**: Tab bars, toolbars, navigation bars — the default for persistent chrome
- **SwiftUI**: `.regularMaterial`
- **Visual effect**: Strong frosting, background contributes color tint but details are obscured

### Thick Material
- **Blur radius**: Heavy — background barely visible
- **Use case**: Sidebars, modal backgrounds, elements that need near-opacity without being fully opaque
- **SwiftUI**: `.thickMaterial`
- **Visual effect**: Dense frosting, almost opaque but retains subtle environmental tint

### Choosing a Material Tier

| Context | Recommended Tier |
|---------|-----------------|
| Tab bar | Regular |
| Toolbar | Regular |
| Navigation bar | Regular |
| Sidebar (iPad/Mac) | Thick |
| Popover | Thin |
| Full-screen overlay | Ultra-thin |
| Sheet background | Regular or Thick |

---

## Vibrancy and System Materials

Vibrancy is the system that ensures content placed ON glass materials remains legible. It adjusts text, symbols, and separators to interact correctly with the translucent surface beneath them.

### Vibrancy Levels

- **Primary vibrancy**: Full-strength content (titles, primary labels). Maximum contrast against glass.
- **Secondary vibrancy**: Medium-strength content (subtitles, secondary labels). Slightly reduced prominence.
- **Tertiary vibrancy**: Low-strength content (disabled text, placeholder content). Subtle presence.
- **Quaternary vibrancy**: Separators and structural lines. Minimal visual weight.

### How Vibrancy Works

The system composites vibrant content using a blend mode that brightens in dark mode and darkens in light mode, pulling color from the background to create a natural "etched into glass" appearance. You do not manually set blend modes — use semantic styles and the system handles it.

### SwiftUI Implementation

```swift
Text("Primary Label")
    .foregroundStyle(.primary)  // Full vibrancy

Text("Secondary Label")
    .foregroundStyle(.secondary)  // Reduced vibrancy

Text("Tertiary Label")
    .foregroundStyle(.tertiary)  // Subtle vibrancy
```

---

## Liquid Glass Translucency Behavior

Liquid Glass dynamically adapts its appearance based on the content behind it:

- **Over light content**: Glass appears lighter with subtle shadows along edges
- **Over dark content**: Glass appears darker with brighter specular highlights
- **Over colorful content**: Glass picks up a color tint from the dominant background color
- **Over moving content**: Refraction effects shift subtly, creating a "living" material
- **In motion**: As the user scrolls, the glass refracts content passing beneath it

### SwiftUI Glass Effect

```swift
// Apply Liquid Glass to a toolbar
.toolbar {
    ToolbarItem(placement: .bottomBar) {
        HStack { /* toolbar content */ }
    }
}
.toolbarBackground(.visible, for: .bottomBar)

// Custom glass effect on a view
someView
    .glassEffect()

// Glass effect with specific material
someView
    .background(.regularMaterial)
```

---

## SF Symbols 7

SF Symbols 7 provides over 6,000 symbols, all redesigned to harmonize with Liquid Glass surfaces. Symbols are vector-based, scalable, and automatically adapt to text weight, size, and accessibility settings.

### Four Rendering Modes

**Monochrome**
- Single color applied uniformly
- Default mode — works everywhere
- Respects tint color
- Best for: toolbars, navigation, simple UI

**Hierarchical**
- Single color with automatic opacity layers
- Primary layer at 100%, secondary at ~55%, tertiary at ~25%
- Adds depth without multiple colors
- Best for: complex symbols that need visual hierarchy

**Palette**
- Two or three explicitly assigned colors
- Full control over each layer's color
- Best for: branded UI, category indicators, status badges

**Multicolor**
- Fixed colors defined by Apple (e.g., red heart, yellow star, blue cloud)
- Cannot be overridden — represents real-world color associations
- Best for: weather, health, nature, file types

### SwiftUI Rendering Modes

```swift
Image(systemName: "heart.fill")
    .symbolRenderingMode(.monochrome)

Image(systemName: "heart.fill")
    .symbolRenderingMode(.hierarchical)

Image(systemName: "heart.fill")
    .symbolRenderingMode(.palette)
    .foregroundStyle(.red, .pink)

Image(systemName: "heart.fill")
    .symbolRenderingMode(.multicolor)
```

### Variable Color

Symbols can fill proportionally to represent a value (0.0 to 1.0):

```swift
Image(systemName: "wifi")
    .symbolVariableValue(0.5)  // Half-filled wifi icon

Image(systemName: "speaker.wave.3")
    .symbolVariableValue(volume)  // Fills with volume level
```

Common variable-color symbols: wifi, speaker.wave.3, cellularbars, battery.100percent, chart.bar.fill

### Symbol Animations

```swift
// Bounce — single bounce on trigger
Image(systemName: "star.fill")
    .symbolEffect(.bounce, value: triggerValue)

// Pulse — gentle opacity pulse (repeating)
Image(systemName: "heart.fill")
    .symbolEffect(.pulse)

// Variable color — progressive fill animation (repeating)
Image(systemName: "wifi")
    .symbolEffect(.variableColor.iterative)

// Replace — crossfade to a different symbol
Image(systemName: isPlaying ? "pause.fill" : "play.fill")
    .contentTransition(.symbolEffect(.replace))

// Breathe — slow scale and opacity cycle (iOS 26+)
Image(systemName: "lungs.fill")
    .symbolEffect(.breathe)

// Appear/Disappear — animated entry and exit
Image(systemName: "checkmark.circle.fill")
    .symbolEffect(.appear, isActive: showCheck)
```

### Weight Matching

SF Symbols automatically match the weight of adjacent text. If your label uses `.font(.body)` (which is Regular weight), nearby symbols render at Regular weight. If you use `.bold()`, symbols become Bold. No manual weight selection needed.

### Symbol Sizes

Symbols scale with text styles. For explicit sizing:

```swift
Image(systemName: "gear")
    .font(.system(size: 24))  // Explicit point size

Image(systemName: "gear")
    .imageScale(.large)  // Relative: small, medium, large
```

---

## Dynamic Island

### Dimensions and Layout

- **Compact presentation**: ~126.68 x 37.33 points (hardware pill shape)
- **Minimal presentation**: circular element on the opposite side of the pill (~36.33 x 36.33 points)
- **Expanded presentation**: up to ~371 x 160 points (varies by content)
- **Top safe area**: 62 points from top edge of screen

### Design Guidelines

- Compact: show the single most important piece of info (timer, score, now playing)
- Minimal: a tiny icon or progress indicator — one glanceable element
- Expanded: richer layout with leading, trailing, center, and bottom regions
- Content should complement the app experience, not demand attention
- Animations must be subtle — the Island is persistent, not a notification
- Use system-provided shapes and corner radii (do not fight the pill form)

### Live Activities

Live Activities power the Dynamic Island and Lock Screen:

```swift
// ActivityAttributes define the static and dynamic content
struct DeliveryAttributes: ActivityAttributes {
    struct ContentState: Codable, Hashable {
        var status: String
        var estimatedArrival: Date
    }
    var orderNumber: String
}
```

---

## Safe Areas

### iPhone Safe Area Insets (Pro Max / 16 series)

| Edge | Inset | Notes |
|------|-------|-------|
| Top (portrait) | 62pt | Dynamic Island / status bar |
| Bottom (portrait) | 34pt | Home indicator |
| Left (portrait) | 0pt | Full width |
| Right (portrait) | 0pt | Full width |
| Top (landscape) | 0pt | Status bar hidden |
| Bottom (landscape) | 21pt | Home indicator (reduced) |
| Left (landscape, notch side) | 62pt | Dynamic Island |
| Right (landscape, notch side) | 62pt | Dynamic Island |

### SwiftUI Safe Area Handling

```swift
// Content automatically respects safe areas
ScrollView {
    content
}

// Extend into safe areas intentionally
someView
    .ignoresSafeArea(.all)

// Add custom safe area insets
someView
    .safeAreaInset(edge: .bottom) {
        CustomToolbar()
    }
```

---

## Dynamic Type

### Text Styles (11 Total)

| Style | Default Size | Weight |
|-------|-------------|--------|
| `.largeTitle` | 34pt | Regular |
| `.title` | 28pt | Regular |
| `.title2` | 22pt | Regular |
| `.title3` | 20pt | Regular |
| `.headline` | 17pt | Semibold |
| `.body` | 17pt | Regular |
| `.callout` | 16pt | Regular |
| `.subheadline` | 15pt | Regular |
| `.footnote` | 13pt | Regular |
| `.caption` | 12pt | Regular |
| `.caption2` | 11pt | Regular |

### Accessibility Sizes

Dynamic Type extends to 5 accessibility sizes (AX1 through AX5). At AX5, `.body` text renders at approximately 53pt. Layouts MUST adapt — text truncation is never acceptable for essential content.

```swift
Text("Hello")
    .font(.body)  // Automatically scales with Dynamic Type

// Limit scaling range if needed
Text("Fixed-ish")
    .dynamicTypeSize(.small ... .accessibility3)
```

---

## Dark Mode

### System Color Behavior

System colors (`.label`, `.secondaryLabel`, `.systemBackground`, `.secondarySystemBackground`) automatically adapt between light and dark modes. Do not maintain separate color palettes — use semantic colors.

### Elevated Surfaces in Dark Mode

In dark mode, elevated surfaces use slightly lighter backgrounds to convey hierarchy:
- Base: `systemBackground` (#000000 on OLED)
- Elevated: `secondarySystemBackground` (#1C1C1E)
- Double elevated: `tertiarySystemBackground` (#2C2C2E)

### Glass Materials in Dark Mode

Liquid Glass appears more reflective in dark mode, with brighter specular highlights and more pronounced edge lighting. The tint from background content is more visible against the darker chrome.

---

## Navigation Patterns

### Tab Bar (Primary Navigation)

- Bottom of screen with Liquid Glass material
- 2-5 tabs (5 maximum, use "More" for overflow)
- Each tab: SF Symbol icon + short label
- Active state: filled icon + tint color
- Inactive state: outline icon + secondary label color

```swift
TabView {
    HomeView()
        .tabItem {
            Label("Home", systemImage: "house.fill")
        }
    SearchView()
        .tabItem {
            Label("Search", systemImage: "magnifyingglass")
        }
}
```

### Navigation Stack

```swift
NavigationStack {
    List(items) { item in
        NavigationLink(item.title) {
            DetailView(item: item)
        }
    }
    .navigationTitle("Items")  // Large title by default
    .navigationBarTitleDisplayMode(.large)  // or .inline
}
```

### Sidebar (iPad)

```swift
NavigationSplitView {
    List(sections) { section in
        NavigationLink(section.title) { /* ... */ }
    }
    .navigationTitle("Sidebar")
} detail: {
    DetailView()
}
```

### Modal Sheets

```swift
.sheet(isPresented: $showSheet) {
    SheetContent()
        .presentationDetents([.medium, .large])  // Resizable
        .presentationDragIndicator(.visible)
        .presentationCornerRadius(20)
}
```

---

## Key Design Values

### Touch Targets

- **Minimum tappable area**: 44 x 44 points (Apple HIG requirement)
- **Recommended**: 48 x 48 points for primary actions
- **Visually smaller elements** (e.g., a 24pt icon) must still have a 44pt hit area

### Spacing System

- **Standard margin**: 16pt (leading and trailing)
- **Compact margin**: 8pt (between related elements)
- **Section spacing**: 20pt or 24pt between content groups
- **List row height**: 44pt minimum
- **Minimum spacing between interactive elements**: 8pt

### Corner Radius

- iOS uses continuous corner radius (squircle) — not circular arcs
- System default: ~10-13pt for cards and containers
- Small elements (chips, badges): ~6-8pt
- Large elements (sheets, modals): ~20pt
- Full-round (pills, capsules): height/2

### Animation Curves

> These are **iOS platform-native SwiftUI spring values** (response + damping fraction). They are not the product's base motion scale; for base durations and easings see `interaction-motion-design` (its `animation-timing-curves.md` reference).

iOS 26 uses spring-based animations for interactive elements:

```swift
// Default spring (recommended for most transitions)
withAnimation(.spring(response: 0.35, dampingFraction: 0.85)) {
    // state change
}

// Bouncy spring (for playful interactions)
withAnimation(.spring(response: 0.4, dampingFraction: 0.6)) {
    // state change
}

// Snappy spring (for quick, precise movements)
withAnimation(.spring(response: 0.25, dampingFraction: 0.9)) {
    // state change
}

// Interactive spring (for gesture-driven animations)
withAnimation(.interactiveSpring(response: 0.15, dampingFraction: 0.86)) {
    // state change
}
```

---

## SwiftUI Code Patterns (Quick Reference)

### Color

```swift
// Semantic colors (preferred)
Color.accentColor          // App tint
Color.primary              // Primary label
Color.secondary            // Secondary label

// System colors
Color(.systemBackground)
Color(.secondarySystemBackground)
Color(.systemRed)          // Adaptive red

// Custom with dark mode
Color("BrandPrimary")      // From asset catalog with light/dark variants

// Tint
someView.tint(.blue)
```

### Layout

```swift
// Stacks
VStack(alignment: .leading, spacing: 12) { /* ... */ }
HStack(spacing: 8) { /* ... */ }
ZStack(alignment: .topTrailing) { /* ... */ }

// Grids
LazyVGrid(columns: [GridItem(.adaptive(minimum: 160))], spacing: 16) {
    ForEach(items) { item in CardView(item: item) }
}

// Geometry
GeometryReader { geometry in
    let width = geometry.size.width
    // Responsive layout based on width
}
```

### Lists

```swift
List {
    Section("Recent") {
        ForEach(recentItems) { item in
            ItemRow(item: item)
        }
    }
}
.listStyle(.insetGrouped)  // Default iOS style
.searchable(text: $searchText)  // Built-in search
```

---

## StandBy Mode (iPhone)

StandBy activates when iPhone is on a charger in landscape orientation:

- **Clock face**: large, glanceable time display
- **Widgets**: two side-by-side widget stacks
- **Photos**: full-screen photo display
- **Smart rotation**: widgets rotate based on time, location, habits
- **Night mode**: red tint in dark rooms
- **Always-On (Pro models)**: dimmed StandBy persists on screen

### Design Considerations for StandBy

- Widgets must be legible at arm's length (nightstand distance)
- High contrast, large numerals
- Minimal information density
- Red-compatible colors for night mode

---

## Optical Properties

- **Translucency with refraction** — not just blur: edges refract more than the center, like a curved pane, producing a subtle lens distortion at the periphery.
- **Dynamic tinting** — samples color from the content beneath in real time (cool over blue photos, warm over sunsets), desaturated and biased toward the accent color.
- **Specular highlights** — a simulated light source highlights edges and top surfaces and responds to device motion (gyroscope), giving parallax-like glints.
- **Depth layering** — bars, floating cards, and sheets sit on separate depth planes; deeper layers show stronger effects. This replaces the drop-shadow elevation model.
- **Edge treatment** — thin, semi-transparent luminous borders define where one glass surface ends and another begins.

Design-time approximations used in mockups (unverified, not Apple-published): a 1pt top-edge specular line at white 10-15% opacity (5-8% in Dark Mode, with a faint bottom inner shadow); accent tint at 5-15% of the material, 20-30% for a selected indicator. Custom tint colors must be contrast-checked against both light and dark backgrounds.

## Glass vs Solid

| Context | Recommendation | Reason |
|---------|---------------|--------|
| Chrome (bars, toolbars) | Glass | Users expect to see content continuity |
| Cards in scrollable lists | Solid | Glass-on-glass creates visual noise and rendering cost |
| Full-screen content (video, photo) | Solid or ultra-thin | Content is the focus, glass distracts |
| Modals and sheets | Glass | Maintains spatial context |
| Text-heavy reading views | Solid | Glass behind paragraphs of text reduces readability |
| Data-heavy views (tables, dashboards) | Solid | Glass noise degrades scanability |
| Text input editing area | Solid | The field container can be glass; the editing area needs a stable background |
| Accessibility-critical (medical, financial, emergency) content | Solid | Glass only for non-critical chrome |
| Floating controls over media or maps | Glass with a visible border | Glass alone weakens the tap affordance |

## Floating Tab Bar (iOS 26)

- Floats above content as a capsule rather than an edge-pinned rectangle; 5 items maximum, overflow to "More"
- **Scrolling down** — can minimize to a compact form showing the selected tab (`.tabBarMinimizeBehavior(.onScrollDown)`), reducing content occlusion
- **Scrolling up / tap** — re-expands with a spring
- **Hidden** — dismissed during immersive content (video, full-screen maps)
- Selected state: filled SF Symbol variant + tint; minimum 44pt tap target per item
- SF Symbols on glass: prefer Medium weight and Medium scale for legibility
- Mockup dimensions (unverified, not Apple-published): about 49pt tall compact / 56pt regular, floating about 8pt above the bottom safe area, 24pt icons, 10pt medium labels

### Navigation Bar

- 44pt standard, about 96pt with a large title; large title SF Pro Display 34pt bold, inline title SF Pro Text 17pt semibold
- Large-to-inline title transition is a continuous scroll-driven interpolation, not a snap
- Back button: `chevron.backward` + previous title, 17pt, accent color

SF Symbols effects available on glass: bounce, pulse, variable color, scale, appear, disappear, replace, wiggle, rotate, breathe. Placed on glass, symbols adopt the vibrancy level of their label style automatically.

## System Adoption

Built against the iOS 26 SDK, these adopt Liquid Glass with no code changes: navigation bars (large titles collapse into an inline glass bar on scroll), tab bars, bottom toolbars and keyboard accessories, iPad sidebars, segmented controls (selected segment as a brighter glass pill), search bars in navigation bars, and menus/popovers.

## Liquid Glass APIs

```swift
// Standard glass on a custom view; .clear is the lighter, less-tinted variant
VStack(alignment: .leading, spacing: 8) {
    Text("Now Playing").font(.headline)
    Text("Artist — Track Title").font(.subheadline).foregroundStyle(.secondary)
}
.padding()
.glassEffect(.regular)

// Group neighboring glass shapes so they composite (and morph) together
// instead of stacking blur upon blur
GlassEffectContainer {
    HStack {
        Button("Edit") { }.glassEffect()
        Button("Share") { }.glassEffect()
    }
}
```

UIKit: `UIGlassEffect` is a `UIVisualEffect` used with `UIVisualEffectView`. SwiftUI is the first-class API; UIKit support is the compatibility bridge.

```swift
let glassView = UIVisualEffectView(effect: UIGlassEffect())
glassView.frame = containerView.bounds
containerView.addSubview(glassView)
```

Interactive custom glass elements should carry a visible border to communicate tappability:

```swift
Button(action: action) {
    Text(label).font(.body.weight(.semibold))
        .padding(.horizontal, 20).padding(.vertical, 12)
}
.glassEffect(.regular)
.overlay(RoundedRectangle(cornerRadius: 12).strokeBorder(.white.opacity(0.3), lineWidth: 1))
```

Use semantic foreground styles (`.primary`, `.secondary`, `.tertiary`) for text on glass — they get vibrancy automatically. Hardcoded `Color.white` / `Color.black` / hex values do not adapt and can become unreadable.

### Fallback for iOS 25 and Earlier

```swift
.background {
    if #available(iOS 26, *) {
        Color.clear.glassEffect(.regular)
    } else {
        Rectangle().fill(.ultraThinMaterial)
    }
}
```

```swift
func makeChromeBackground() -> UIView {
    if #available(iOS 26, *) {
        return UIVisualEffectView(effect: UIGlassEffect())
    } else {
        return UIVisualEffectView(effect: UIBlurEffect(style: .systemThinMaterial))
    }
}
```

`.ultraThinMaterial` / `.thinMaterial` are the closest approximation: translucent, but no refraction or dynamic tint.

## Usability Concerns (NNGroup Critique)

Nielsen Norman Group's iOS 26 analysis (nngroup.com) raised evidence-based concerns:

- **Reduced contrast** — glass shifts lightness and hue with the background, so text can drop below WCAG AA (4.5:1 normal, 3:1 large) in cases like light text over a pale sky or dark text over a dark map. Vibrancy mitigates but does not guarantee compliance.
- **Legibility** — even when ratios pass, moving, refracting content under text slows reading and raises cognitive load, especially for older and low-vision users and in bright sunlight.
- **Touch target ambiguity** — soft luminous edges make the clickable area unclear and elements feel decorative rather than interactive.
- **Flattened hierarchy** — when chrome and content are both translucent, users lose the opacity cues that separate controls from content.

## Accessibility

- **Reduce Transparency** — all glass must fall back to opaque. System controls do this automatically; custom glass must check the setting:

```swift
@Environment(\.accessibilityReduceTransparency) var reduceTransparency

var body: some View {
    content.background {
        if reduceTransparency {
            RoundedRectangle(cornerRadius: 12).fill(Color(.systemBackground))
        } else {
            Color.clear.glassEffect(.regular)
        }
    }
}
```

UIKit: `UIAccessibility.isReduceTransparencyEnabled`. Keep the same spatial relationships and hierarchy in the opaque state.

- **Increase Contrast** — glass becomes more opaque, borders more prominent, text heavier. Test with it on.
- **Worst-case contrast testing** — screenshot glass text over the lightest and darkest content that can scroll beneath it and measure; do not assume vibrancy saves you.
- **Borders on interactive glass** — semi-transparent white or system-color strokes on every tappable glass element.
- **VoiceOver** — glass is purely visual; labels, traits, and actions are still required.

## Migrating an Existing App to Liquid Glass

1. Build against the iOS 26 SDK; system bars adopt glass automatically.
2. Remove custom navigation/toolbar backgrounds (`UINavigationBarAppearance` images or colors); use the system default or `.glassEffect()`. Replace `UIBlurEffect` chrome with `UIGlassEffect` where appropriate.
3. Grep for hardcoded text colors on chrome (`UIColor.white`, `Color.black`, `Color(hex:)`) and switch to `.label`, `.secondaryLabel`, `.foregroundStyle(.primary/.secondary)`.
4. Add Reduce Transparency fallbacks to every custom glass view.
5. Test Increase Contrast, the largest Dynamic Type sizes, and landscape.
6. Profile on the oldest supported physical device — glass is composited by the GPU in real time and the Simulator does not reflect performance.

**Testing checklist:**
- Text on glass meets WCAG AA over light, dark, and varied content
- Reduce Transparency: all glass falls back to opaque
- Increase Contrast: borders and text weight increase
- Dynamic Type at all sizes: glass chrome does not clip or obscure text
- Landscape: glass surfaces resize and recomposite correctly
- 60fps scrolling with glass navigation and tab bars on the oldest supported device
- VoiceOver: correct labels, traits, and order on all glass elements
