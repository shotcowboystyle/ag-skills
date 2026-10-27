# Material 3 Expressive Design Standards

## What Changed: M3 to M3 Expressive

Material 3 Expressive is the most significant Material Design update since the Material 2 to Material 3 transition. Announced in 2025, it fundamentally shifts Material Design from a neutral, systematic framework to an emotionally expressive design system that encourages personality and brand differentiation while maintaining usability.

### Core Philosophy

"Emotional expression through systematic design." M3 Expressive recognizes that purely functional design can feel sterile. The update gives designers tools to inject warmth, playfulness, and brand identity without sacrificing accessibility or consistency.

### Three Pillars of Expressiveness

1. **Shape**: 35-shape library replaces fixed corner radii — components can morph between shapes
2. **Motion**: Spring-physics animations replace duration-based transitions — interactions feel physical
3. **Color**: Enhanced HCT color system with more vibrant defaults and richer Dynamic Color

---

## 35-Shape Library

M3 Expressive replaces the simple corner radius system (small, medium, large, extra-large, full) with a library of 35 distinct shapes that can be applied to any component.

### Shape Categories

**Round (Circular Corners)**
- Classic rounded rectangles with varying radii
- Convey approachability and softness
- Default for most components

**Squircle (Continuous Corners)**
- Superellipse curves (like iOS)
- Smoother than circular corners
- Premium, polished feel

**Cut (Chamfered Corners)**
- Straight diagonal cuts at corners
- Convey precision, seriousness, technical
- Good for finance, enterprise, productivity

**Arch**
- Rounded top with flat bottom (or vice versa)
- Architectural, structured
- Good for headers, hero cards

**Pill**
- Full-round ends (stadium shape)
- Strong action signal
- Default for buttons and chips

**Clover**
- Four-lobed organic shape
- Playful, nature-inspired
- Good for wellness, children's apps

**Scallop**
- Wavy, shell-like edges
- Decorative, artisanal
- Good for food, craft, creative apps

**Hexagon**
- Six-sided geometric shape
- Technical, structured, modular
- Good for data visualization, tech, gaming

**Diamond**
- Four-pointed rotated square
- Premium, luxury, distinctive
- Good for fashion, jewelry, premium tiers

**Custom Morphing Shapes**
- Define start and end shapes for transitions
- Components morph between shapes based on state
- Example: FAB morphs from circle to rounded rectangle on scroll

### Shape Tokens

```kotlin
// Shape token scale
MaterialTheme.shapes.extraSmall    // 4dp radius
MaterialTheme.shapes.small         // 8dp radius
MaterialTheme.shapes.medium        // 12dp radius
MaterialTheme.shapes.large         // 16dp radius
MaterialTheme.shapes.extraLarge    // 28dp radius
MaterialTheme.shapes.full          // 50% (pill/circle)
```

| Family | Corner Style | Use Case |
|--------|-------------|----------|
| **Extra Small** | 4dp radius | Chips, small badges |
| **Small** | 8dp radius | Cards, text fields |
| **Medium** | 12dp radius | Dialogs, menus |
| **Large** | 16dp radius | Sheets, FAB |
| **Extra Large** | 28dp radius | Large surfaces, navigation drawer |
| **Full** | 50% radius (circle/pill) | FAB in resting, avatar, pill buttons |

Morph shapes animate between corner families during state transitions. A FAB morphing into a bottom sheet transitions from Full to Extra Large with a spring animation; a FAB starts as Full (circle), morphs to Large when expanded, and returns to Full when collapsed.

### Morphing Shapes in Practice

```kotlin
// FAB that morphs on scroll
val fabShape by animateShapeAsState(
    targetShape = if (isScrolling)
        RoundedCornerShape(16.dp)  // Rounded rectangle
    else
        CircleShape  // Circle
)

FloatingActionButton(
    shape = fabShape,
    onClick = { /* ... */ }
) {
    Icon(Icons.Default.Add, contentDescription = "Add")
}
```

### How Shapes Convey Meaning

| Shape | Emotional Association | Recommended For |
|-------|----------------------|-----------------|
| Round | Friendly, approachable | Consumer apps, social |
| Squircle | Premium, polished | Design tools, premium tiers |
| Cut | Serious, precise | Finance, enterprise |
| Pill | Action, urgency | CTAs, buttons, tags |
| Clover | Playful, organic | Wellness, children |
| Hexagon | Technical, structured | Dev tools, data, gaming |
| Diamond | Luxury, exclusive | Fashion, premium |
| Arch | Architectural, stable | Real estate, institutional |
| Scallop | Artisanal, warm | Food, craft, creative |

---

## Spring-Physics Motion

> These are **Material 3 platform-native spring values** for Android/Compose. They are not the product's base motion scale; for base durations and easings see `interaction-motion-design` (its `animation-timing-curves.md` reference).

M3 Expressive replaces duration-based animations (200ms ease-in-out) with spring physics. Material specifies each spring with two parameters only — **stiffness** and **damping ratio** (mass is fixed). Springs are interruptible: if the target changes mid-flight, the animation redirects from its current velocity with no stutter or restart, which matters during rapid interaction (e.g., quickly switching navigation tabs).

### Why Springs

- **Interruptible**: A spring animation can be redirected mid-flight without jarring stops
- **Natural**: Physical objects don't move with cubic beziers — they accelerate and decelerate organically
- **Responsive**: Springs react to velocity — a fast fling creates a different animation than a slow drag
- **Consistent**: The same spring parameters produce the same feel regardless of distance

### Spring Parameters

- **Stiffness**: How quickly the spring pulls toward the target. Higher stiffness = faster, shorter animation.
- **Damping ratio**: 0 = infinite oscillation, < 1 = underdamped (overshoot/bounce), 1 = critically damped (no bounce), > 1 = overdamped (sluggish)

### Motion Schemes and Spring Tokens

Material defines two **motion schemes** (`MotionScheme.standard()` and `MotionScheme.expressive()` in Compose). Each has six spring tokens: **spatial** springs (position, size, shape/corner radius — may overshoot) and **effects** springs (color, opacity — never bounce), each in **fast / default / slow**.

| Token | Standard scheme (damping ratio / stiffness) | Expressive scheme (damping ratio / stiffness) |
|-------|---------------------------------------------|-----------------------------------------------|
| Fast spatial | 0.9 / 1400 | 0.6 / 800 |
| Default spatial | 0.9 / 700 | 0.8 / 380 |
| Slow spatial | 0.9 / 300 | 0.8 / 200 |
| Fast effects | 1.0 / 3800 | 1.0 / 3800 |
| Default effects | 1.0 / 1600 | 1.0 / 1600 |
| Slow effects | 1.0 / 800 | 1.0 / 800 |

Sources: expressive values from androidx `compose/material3/.../tokens/ExpressiveMotionTokens.kt`; standard values from material-components-android `docs/theming/Motion.md` (`motionSpring*` attributes).

Choosing a speed: **fast** for small component changes (switches, checkboxes, icon buttons), **default** for most component transitions (sheets, nav indicator, FAB morph), **slow** for full-screen transitions. Use the expressive scheme for hero moments and the standard scheme for utilitarian UI.

Guidance (not a Material token): lists and grids can stagger children 20-40ms per item, capped at about 300ms total. Elements moving across the screen can follow arced paths rather than straight lines.

### Compose Implementation

```kotlin
// Spring animation for a float value
val offset by animateFloatAsState(
    targetValue = if (expanded) 200f else 0f,
    animationSpec = spring(
        dampingRatio = Spring.DampingRatioMediumBouncy,
        stiffness = Spring.StiffnessMedium
    )
)

// Expressive default spatial spring (scheme token values, see table above)
val cornerRadius by animateDpAsState(
    targetValue = if (isExpanded) 16.dp else 28.dp,
    animationSpec = spring(dampingRatio = 0.8f, stiffness = 380f)
)

// Generic Compose spring constants (androidx.compose.animation.core.Spring),
// not the M3 scheme tokens above
Spring.DampingRatioNoBouncy        // 1.0
Spring.DampingRatioLowBouncy       // 0.75
Spring.DampingRatioMediumBouncy    // 0.5
Spring.DampingRatioHighBouncy      // 0.2

Spring.StiffnessHigh               // 10000
Spring.StiffnessMedium             // 1500
Spring.StiffnessMediumLow          // 400
Spring.StiffnessLow                // 200
Spring.StiffnessVeryLow            // 50
```

### Container Transforms

Shared element transitions use spring curves for seamless morphing between screens:

```kotlin
// Shared element transition (Compose)
SharedTransitionLayout {
    AnimatedContent(targetState = showDetail) { isDetail ->
        if (isDetail) {
            DetailScreen(
                modifier = Modifier.sharedElement(
                    rememberSharedContentState(key = "card-$id"),
                    animatedVisibilityScope = this
                )
            )
        } else {
            ListScreen(/* ... */)
        }
    }
}
```

---

## HCT Color Space (Hue, Chroma, Tone)

HCT is Google's perceptually accurate color space developed specifically for Material Design. It combines the best attributes of CAM16 (hue, chroma) and L* from CIELAB (tone/lightness).

### HCT Components

**Hue (0-360)**
- The color identity: red, orange, yellow, green, blue, purple
- 0/360 = red, 60 = yellow, 120 = green, 240 = blue
- Mapped from CAM16 for perceptual accuracy

**Chroma (0-~150)**
- Color vividness/saturation
- 0 = completely gray (achromatic)
- Higher values = more vivid
- Maximum chroma varies by hue (yellow can reach ~110, blue can reach ~130)
- Unlike HSL saturation, equal chroma changes look equally vivid across all hues

**Tone (0-100)**
- Lightness on a perceptually uniform scale
- 0 = pure black
- 50 = medium (perceptual midpoint)
- 100 = pure white
- A tone difference of 50+ guarantees 4.5:1 contrast (WCAG AA for normal text); 40+ guarantees 3:1

### Why HCT Over HSL

HSL has severe perceptual non-uniformity: a yellow at 50% lightness looks much lighter than a blue at 50% lightness. HCT corrects this — Tone 50 looks equally light regardless of hue. This makes it possible to generate accessible color palettes algorithmically.

### Tonal Palettes

Each key color generates a 13-tone palette:

| Tone | Use |
|------|-----|
| 0 | Black |
| 10 | Darkest surface in dark mode |
| 20 | Dark mode container fills |
| 30 | Dark mode primary/secondary colors |
| 40 | Light mode primary/secondary colors |
| 50 | Medium contrast elements |
| 60 | Light mode decorative elements |
| 70 | Light secondary containers |
| 80 | Light mode container fills |
| 90 | Light mode surface containers |
| 95 | Lightest surface in light mode |
| 99 | Near-white surface |
| 100 | White |

---

## Dynamic Color (Material You)

### Algorithm

1. **Extract**: Identify dominant colors from the user's wallpaper using quantization (Wu's algorithm or similar)
2. **Map to HCT**: Convert extracted colors to HCT color space
3. **Generate 5 key colors**: Primary, Secondary, Tertiary, Neutral, Neutral Variant
4. **Create tonal palettes**: Generate 13-tone palette for each key color
5. **Assign color roles**: Map tonal palette values to 29 semantic color tokens
6. **Generate schemes**: Create both light and dark theme variants

### 5 Key Colors

| Key Color | Source | Purpose |
|-----------|--------|---------|
| Primary | Dominant wallpaper color | Brand, key actions, active states |
| Secondary | Complementary wallpaper color | Less prominent components |
| Tertiary | Analogous or triadic color | Accent, contrast, visual interest |
| Neutral | Desaturated primary (low chroma) | Surfaces, backgrounds |
| Neutral Variant | Slightly chromatic neutral | Outline, surface variant |

### 29 Color Roles

```
primary, onPrimary, primaryContainer, onPrimaryContainer,
secondary, onSecondary, secondaryContainer, onSecondaryContainer,
tertiary, onTertiary, tertiaryContainer, onTertiaryContainer,
error, onError, errorContainer, onErrorContainer,
background, onBackground,
surface, onSurface, surfaceVariant, onSurfaceVariant,
outline, outlineVariant,
inverseSurface, inverseOnSurface, inversePrimary,
shadow, scrim
```

### Custom Colors (Brand Extension)

```kotlin
// Extend dynamic color with a brand color
val customColor = CustomColor(
    name = "Brand Orange",
    color = Color(0xFFFF6B00),
    harmonize = true  // Blend with dynamic palette
)
```

When `harmonize = true`, the brand color is shifted slightly toward the dynamic palette's primary hue, creating harmony without losing brand identity.

### Compose Implementation

```kotlin
// Dynamic color scheme (Android 12+)
val colorScheme = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
    if (darkTheme) dynamicDarkColorScheme(context)
    else dynamicLightColorScheme(context)
} else {
    if (darkTheme) darkColorScheme() else lightColorScheme()
}

MaterialTheme(
    colorScheme = colorScheme,
    typography = Typography,
    shapes = Shapes
) {
    // App content
}
```

---

## M3 Component Gallery

### Buttons

| Type | Use | Visual |
|------|-----|--------|
| Filled | Primary CTA | Solid primary color, white text |
| Outlined | Secondary action | Border only, no fill |
| Tonal | Medium emphasis | Primary container color fill |
| Elevated | Needs separation from surface | Shadow + surface tint |
| Text | Lowest emphasis | No border, no fill |

All buttons support leading/trailing icons, loading states, and disabled states.

```kotlin
Button(onClick = { }) { Text("Filled") }
OutlinedButton(onClick = { }) { Text("Outlined") }
FilledTonalButton(onClick = { }) { Text("Tonal") }
ElevatedButton(onClick = { }) { Text("Elevated") }
TextButton(onClick = { }) { Text("Text") }
```

### Cards

- **Elevated**: shadow + surface tint — default card style
- **Filled**: surface container fill — grouped content
- **Outlined**: border + no fill — content that needs clear boundary

### Chips

- **Assist**: suggest an action (e.g., "Open in Maps")
- **Filter**: toggle filtering criteria (multi-select)
- **Input**: represent user input (e.g., email recipients)
- **Suggestion**: dynamically generated suggestions

### FAB (Floating Action Button)

- **Regular**: 56dp, primary container color
- **Small**: 40dp, for compact layouts
- **Large**: 96dp, for primary screen actions
- **Extended**: pill with icon + label, for clarity
- **Shape morphing**: FAB can morph shape on scroll/expand

### Navigation

- **Bottom Bar**: 3-5 destinations, active indicator pill, icons + labels
- **Navigation Rail**: vertical strip for medium/expanded screens, 3-7 destinations
- **Navigation Drawer**: full destination list for expanded screens
- **Active indicator**: pill-shaped highlight behind active icon (M3 signature element)

### Text Fields

- **Filled**: bottom border + filled container — default
- **Outlined**: full border — more prominent
- Both support: label, supporting text, error text, leading icon, trailing icon, character counter

### Dialogs

- **Basic**: title + text + actions (2 buttons maximum)
- **Full-screen**: for complex tasks on mobile (takes entire screen, has top app bar)

### Other Components

- **Snackbar**: temporary message at bottom, optional action button
- **Bottom Sheet**: standard (partial) or modal (full with scrim)
- **Date Picker**: docked, modal, or date range
- **Time Picker**: dial or input
- **Menu**: dropdown or exposed dropdown
- **Progress**: linear or circular, determinate or indeterminate
- **Slider**: continuous or discrete, with optional label
- **Switch**: with optional icon inside track
- **Divider**: horizontal separator, full-width or inset

---

## Typography (M3 Type Scale)

### 15 Text Styles

Display is for hero/splash text, Headline for sections, Title for subsections, Body for paragraphs, Label for buttons and chips.

| Role | Font | Size | Weight | Line Height | Tracking |
|------|------|------|--------|-------------|----------|
| Display Large | Brand/Serif | 57sp | 400 | 64sp | -0.25sp |
| Display Medium | Brand/Serif | 45sp | 400 | 52sp | 0sp |
| Display Small | Brand/Serif | 36sp | 400 | 44sp | 0sp |
| Headline Large | Brand/Sans | 32sp | 400 | 40sp | 0sp |
| Headline Medium | Brand/Sans | 28sp | 400 | 36sp | 0sp |
| Headline Small | Brand/Sans | 24sp | 400 | 32sp | 0sp |
| Title Large | Sans | 22sp | 400 | 28sp | 0sp |
| Title Medium | Sans | 16sp | 500 | 24sp | 0.15sp |
| Title Small | Sans | 14sp | 500 | 20sp | 0.1sp |
| Body Large | Sans | 16sp | 400 | 24sp | 0.5sp |
| Body Medium | Sans | 14sp | 400 | 20sp | 0.25sp |
| Body Small | Sans | 12sp | 400 | 16sp | 0.4sp |
| Label Large | Sans | 14sp | 500 | 20sp | 0.1sp |
| Label Medium | Sans | 12sp | 500 | 16sp | 0.5sp |
| Label Small | Sans | 11sp | 500 | 16sp | 0.5sp |

(sp = scaleable pixels)

### Default Typeface

Roboto remains the default. For brand differentiation, use Google Fonts variable fonts. M3 Expressive encourages expressive typeface choices — serif for editorial, rounded sans for playful, geometric for technical.

### Responsive Typography

- **Compact** (<600dp): use Body and Label sizes predominantly
- **Medium** (600-840dp): introduce Headline and Title
- **Expanded** (>840dp): use Display sizes for hero content

---

## Canonical Layouts (Tablet and Foldable)

### Window Size Classes

| Class | Width | Examples |
|-------|-------|---------|
| Compact | < 600dp | Phone portrait, small foldable |
| Medium | 600-840dp | Tablet portrait, large foldable, phone landscape |
| Expanded | > 840dp | Tablet landscape, desktop, foldable open |

### Layout Patterns

**List-Detail**
- Compact: full-screen list, navigate to full-screen detail
- Medium: list pane (1/3) + detail pane (2/3)
- Expanded: list pane (1/3) + detail pane (2/3) with more content

**Supporting Pane**
- Main content area + supporting information panel
- Supporting pane appears alongside on medium/expanded, as bottom sheet on compact

**Feed**
- Full-width content stream
- Compact: single column
- Medium: single column with wider margins
- Expanded: multi-column grid or single column with max-width constraint

### Navigation Adaptation

| Size Class | Primary Navigation |
|------------|-------------------|
| Compact | Bottom navigation bar |
| Medium | Navigation rail (left edge) |
| Expanded | Navigation drawer (persistent) |

```kotlin
// Adaptive navigation in Compose
NavigationSuiteScaffold(
    navigationSuiteItems = {
        items.forEach { item ->
            item(
                selected = item == currentItem,
                onClick = { currentItem = item },
                icon = { Icon(item.icon, contentDescription = null) },
                label = { Text(item.label) }
            )
        }
    }
) {
    // Content area
}
```

---

## Jetpack Compose Quick Reference

### Theme Setup

```kotlin
@Composable
fun AppTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    dynamicColor: Boolean = true,
    content: @Composable () -> Unit
) {
    val colorScheme = when {
        dynamicColor && Build.VERSION.SDK_INT >= Build.VERSION_CODES.S -> {
            val context = LocalContext.current
            if (darkTheme) dynamicDarkColorScheme(context)
            else dynamicLightColorScheme(context)
        }
        darkTheme -> darkColorScheme()
        else -> lightColorScheme()
    }

    MaterialTheme(
        colorScheme = colorScheme,
        typography = Typography,
        shapes = Shapes,
        content = content
    )
}
```

### Scaffold

```kotlin
Scaffold(
    topBar = {
        TopAppBar(title = { Text("Title") })
    },
    bottomBar = {
        NavigationBar { /* navigation items */ }
    },
    floatingActionButton = {
        FloatingActionButton(onClick = { }) {
            Icon(Icons.Default.Add, contentDescription = "Add")
        }
    },
    snackbarHost = { SnackbarHost(snackbarHostState) }
) { innerPadding ->
    Content(modifier = Modifier.padding(innerPadding))
}
```

### Lists

```kotlin
LazyColumn(
    contentPadding = PaddingValues(16.dp),
    verticalArrangement = Arrangement.spacedBy(8.dp)
) {
    items(data) { item ->
        ListItem(
            headlineContent = { Text(item.title) },
            supportingContent = { Text(item.subtitle) },
            leadingContent = { Icon(item.icon, contentDescription = null) }
        )
    }
}
```

### Key Dimensions

| Element | Size |
|---------|------|
| Touch target minimum | 48 x 48 dp |
| Icon size (standard) | 24 x 24 dp |
| Bottom nav bar height | 80 dp |
| Top app bar height | 64 dp |
| FAB size | 56 dp |
| Small FAB | 40 dp |
| Large FAB | 96 dp |
| Standard margin | 16 dp |
| Card elevation | 1-6 dp |
| Bottom sheet peek | 56 dp |

---

## Release Context and Compatibility

M3 Expressive was announced at Google I/O 2025 and ships with Android 16. It is backward-compatible with Material 3: existing M3 apps do not break, and the new components and behaviors are additive. To get the expressive look, apps opt into the new component variants, spring motion specs, and shape tokens.

## Dynamic Color Details

- **Tone stops**: M3 tonal palettes are commonly sampled at 0, 10, 20, 25, 30, 35, 40, 50, 60, 70, 80, 90, 95, 98, 99, 100; the surface and surface-container roles also use intermediate tones (4, 6, 12, 17, 22, 24, 87, 92, 94, 96).
- **Role assignment**: tokens like `colorPrimary`, `colorOnPrimary`, `colorSurface`, `colorOnSurface` map to specific tonal stops. Light theme uses high-tone backgrounds (98-99) with low-tone text (10-20); dark theme inverts: low-tone backgrounds (6-10) with high-tone text (80-90).
- **Color from content**: beyond wallpaper theming, dominant colors can be extracted from in-app content (album art, product images) and applied to nearby UI.
- **Emphasis through tonal weight**: create hierarchy by choosing lighter or darker tones from the same palette rather than lowering opacity, which hurts readability on varied backgrounds.
- **Scheme variants**: `DynamicScheme` generates a full scheme from one seed color; variants include `SchemeTonalSpot` (default), `SchemeExpressive`, `SchemeFruitSalad`, `SchemeRainbow`, `SchemeMonochrome`, each distributing the palette across roles differently.
- **Contrast**: generated schemes enforce WCAG AA for text/background pairs in light and dark themes. Custom overrides can break this — always re-check contrast.

### Elevation with Tonal Surfaces

M3 replaced drop shadows with tonal elevation:

| Elevation Level | Shadow | Tonal Overlay | Use Case |
|----------------|--------|---------------|----------|
| Level 0 | None | None | Flat surfaces |
| Level 1 | None | +3% primary | Cards, list items |
| Level 2 | None | +5% primary | Elevated cards, menus |
| Level 3 | Subtle | +8% primary | Navigation drawer, FAB |
| Level 4 | Medium | +11% primary | App bar (scrolled state) |
| Level 5 | Prominent | +14% primary | Modal bottom sheet |

Tonal overlay means the surface color shifts toward the primary color as elevation increases.

### Material You Personalization

- **Wallpaper-derived color** — Dynamic Color tonal palettes
- **Themed icons** — Home-screen app icons adopt the user's tonal palette as a monochrome tint
- **Widget theming** — Glance widgets consume `DynamicColors` to blend with the home screen
- **Lock screen clock** — Uses Display Large typography with the wallpaper primary color
- **Cross-device sync** — The selected wallpaper color syncs across phone, tablet, Wear OS, and Chromebook via the Google account

### Component Theming

Every M3 component exposes three theming layers: **color scheme** (role tokens from Dynamic Color, never raw colors), **shape scheme** (corner radius and family per size variant), and **typography scheme** (text style per component element). Override at the component level with the `*Defaults` / `*Colors` Compose APIs:

```kotlin
ButtonDefaults.buttonColors(
    containerColor = MaterialTheme.colorScheme.tertiary,
    contentColor = MaterialTheme.colorScheme.onTertiary
)
```

---

## New and Updated Expressive Components

- **FAB / FAB menu** — morphs between shape states (circle idle, rounded rectangle when focused, pill when extended with a label); new large variant.
- **Bottom app bar / floating toolbar** — can expand to reveal more actions; spring-driven, swipe up to expand and down to collapse.
- **Navigation rail** — animated icon transitions; active indicator uses expressive shape tokens.
- **Navigation bar** — the active indicator slides, stretches, and settles between destinations on a spring.
- **Segmented / connected button groups** — the selection indicator stretches to the new item then contracts.
- **Carousel** — first-class component with multi-browse, hero, uncontained, and full-screen layouts; spring-based snap.
- **Date and time pickers** — expressive shapes, spring-animated selection and month transitions.
- **Chips** — spring scale on selection; chip groups reflow with spring layout animation.
- **Progress indicators** — determinate progress springs to the new value; new wavy variants.
- **Search** — expands from a bar into a full-screen search view on a spring.
- **Top app bar** — when scrolling stops mid-collapse, the bar springs to expanded or collapsed instead of snapping.
- **Buttons and icon buttons** — shape "squish" on press (corner radius changes) and spring scale feedback beyond the ripple.
- **Dialogs and bottom sheets** — spring entry/exit; sheets released mid-drag spring to the nearest snap point.

### Compose Examples

```kotlin
@Composable
fun MorphingFAB(isExpanded: Boolean, onClick: () -> Unit, icon: ImageVector, label: String) {
    val spec = spring<Dp>(dampingRatio = 0.8f, stiffness = 380f) // expressive default spatial
    val cornerRadius by animateDpAsState(if (isExpanded) 16.dp else 28.dp, spec)
    FloatingActionButton(
        onClick = onClick,
        shape = RoundedCornerShape(cornerRadius),
        modifier = Modifier.animateContentSize(spring(dampingRatio = 0.8f, stiffness = 380f))
    ) {
        Row(
            modifier = Modifier.padding(horizontal = if (isExpanded) 20.dp else 16.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            Icon(imageVector = icon, contentDescription = null)
            AnimatedVisibility(visible = isExpanded) {
                Text(text = label, style = MaterialTheme.typography.labelLarge)
            }
        }
    }
}

@Composable
fun ExpressiveCarousel(items: List<CarouselItem>, modifier: Modifier = Modifier) {
    HorizontalMultiBrowseCarousel(
        state = rememberCarouselState { items.count() },
        modifier = modifier.height(220.dp),
        preferredItemWidth = 186.dp,
        itemSpacing = 8.dp
    ) { index ->
        val item = items[index]
        Card(shape = RoundedCornerShape(16.dp), modifier = Modifier.fillMaxSize()) {
            AsyncImage(
                model = item.imageUrl,
                contentDescription = item.description,
                contentScale = ContentScale.Crop,
                modifier = Modifier.fillMaxSize()
            )
        }
    }
}
```

---

## Accessibility in M3 Expressive

- **Reduced motion**: when the user turns animations off or reduces them (Android "Remove animations" / animator duration scale), replace springs with instant cuts or a critically damped effects-style spring (damping ratio 1.0, high stiffness) — no bounce.
- **Touch targets**: keep 48 x 48dp minimum in every shape state; shape morphing must not shrink the hit area.
- **Animated icons**: state shown by icon animation must also be exposed through semantics — TalkBack does not see the animation.
- **Dynamic color contrast**: see Dynamic Color Details above.

## iOS 26 vs M3 Expressive

Apple's answer to "make interfaces feel premium" is **material** (glass, refraction, tinting; motion serves the material). Google's answer is **motion** (springs, shape morphing, animated state changes). A glass aesthetic on Android looks out of place and bouncy springs on iOS feel un-Apple. For cross-platform teams:

- **Follow each platform for chrome** (bars, tab bars, toolbars, system controls) — glass on iOS, expressive springs on Android.
- **Unify content areas** — cards, lists, and media can share one brand language inside platform-native chrome.
- **Budget for it** — plan roughly 15-25% extra design/engineering effort (estimate, not measured) to support both languages properly.
- **Use platform-adaptive components** — Flutter `Cupertino`/`Material`, React Native platform components, Compose Multiplatform + SwiftUI.

## Migrating from M3 to M3 Expressive

1. Update the Material 3 Compose BOM to a version with the Expressive components and `MotionScheme`.
2. Wrap the app in `MaterialExpressiveTheme` (or pass `motionScheme = MotionScheme.expressive()`), then replace `tween()` specs in navigation components with scheme springs.
3. Replace custom carousels, FABs, and segmented controls with the M3 Expressive components.
4. Align custom shapes with the M3 shape token scale.
5. Try the expressive `PaletteStyle` / `SchemeExpressive` for dynamic color; re-check contrast in every generated scheme.
6. Audit every spring for reduced-motion handling.

**Testing checklist:**
- Springs are smooth at 60/90/120fps on target devices, with no frame drops on mid-range hardware
- Reduced motion: all springs become critically damped or instant
- Dynamic color: text contrast meets WCAG AA in light, dark, and high-contrast schemes
- Shape morphing: touch targets stay >= 48dp in every state
- Carousel: TalkBack navigation announces position ("item 2 of 5")
- Predictive back works with expanded search, sheet springs, and dialog entry
- Navigation rail expressive icons render and animate on tablets and foldables
