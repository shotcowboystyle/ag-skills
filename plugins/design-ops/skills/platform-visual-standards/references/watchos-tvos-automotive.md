# Watch, TV, Automotive, Kiosk, and E-Ink Design Standards

---

## WATCH DESIGN

### Apple Watch (watchOS)

#### Screen Dimensions

| Model | Resolution (px) | Points |
|-------|-----------------|--------|
| Series 10 (42mm) | 374 x 446 | 187 x 223 @2x |
| Series 10 (46mm) | 416 x 496 | 208 x 248 @2x |
| Ultra 3 (49mm) | 422 x 514 | 211 x 257 @2x |

#### Always-On Display

Design for TWO states:
- **Full brightness**: normal interactive state — full color, all details visible
- **Dimmed state**: always-on resting state — reduced brightness, simplified layout, fewer colors
- In dimmed state: hide seconds in clocks, reduce animation to static, drop non-essential elements
- Use `.isLuminanceReduced` environment value to detect dimmed state

#### System Font

- **SF Compact**: default system font, optimized for small screens with wider letter spacing
- **SF Compact Rounded**: used for complications and glanceable data — friendlier appearance
- Minimum readable size: ~17pt system text (below this, legibility degrades significantly)
- Prefer 18-20pt for body text

#### OLED Considerations

- True blacks (#000000) save battery — OLED pixels are physically off for pure black
- Use pure black backgrounds as default
- Colored UI elements pop against black with high contrast
- Avoid large areas of white — they draw significant power
- System backgrounds are black by default

#### Digital Crown Interactions

- **Scroll**: rotate crown to scroll vertically through content
- **Zoom**: rotate crown to zoom in/out on maps, photos
- **Adjust values**: rotate to increment/decrement numeric values (time, volume)
- **Haptic feedback**: the crown provides haptic detents as you scroll
- Design scroll lists with clear item boundaries that align with haptic clicks

#### Double-Tap Gesture (Series 9+)

- Pinch thumb and index finger together to trigger the primary action
- The system assigns this to the most contextually appropriate action
- Typically: answer/end call, pause/play music, dismiss alarm, start/stop timer
- Only ONE action can be the double-tap target at any time
- Use `.handGestureShortcut(.primaryAction)` in SwiftUI

#### Navigation Patterns

**Hierarchical (Push/Pop)**
- NavigationStack: push detail views, swipe back
- Best for apps with clear parent-child content relationships
- Digital Crown scrolls within each view

**Page-Based (Horizontal Swipe)**
- TabView with .tabViewStyle(.page): swipe left/right between pages
- Best for apps with parallel, equally important views
- Maximum 5-7 pages (more becomes tedious to navigate)

#### Complications

Complications display glanceable data on watch faces:

| Type | Shape | Content |
|------|-------|---------|
| Circular | Round | Small icon + short value |
| Rectangular | Wide rectangle | Rich data, small chart |
| Corner | Quarter-circle arc | Gauge-style data |
| Inline | Single text line | Short text string |

- Use WidgetKit (same framework as iOS widgets)
- Refresh cadence: system-managed, typically every 15 minutes minimum
- Data must be meaningful at a glance — no paragraphs, no complex charts
- Tap a complication to launch the app

#### watchOS SwiftUI Patterns

```swift
// Basic watch app structure
NavigationStack {
    List {
        ForEach(items) { item in
            NavigationLink(item.title) {
                DetailView(item: item)
            }
        }
    }
    .navigationTitle("Items")
}

// Date display
Text(Date.now, style: .timer)  // Live-updating timer
Text(Date.now, style: .relative)  // "2 min ago"
```

---

### Wear OS (Material 3 Expressive)

#### Round Screen Challenges

- Round screens have ~22% less usable area than equivalent square screens
- Content at the four corners is clipped — do NOT place important content there
- Center the most critical information
- Use the round shape to your advantage: circular progress indicators, radial menus

#### Screen Size Breakpoint

- **225dp** is the key breakpoint separating smaller and larger Wear OS watches
- Below 225dp: reduce padding, use compact layouts
- Above 225dp: standard padding and spacing

#### Tile Layout (3-Slot)

Wear OS Tiles use a standard 3-slot layout:
1. **Title slot**: top area, brief title text
2. **Main content slot**: center area, primary information or action
3. **Bottom slot**: secondary action or supplementary info

#### Edge-Hugging Buttons

On round screens, buttons placed at the screen edges follow the curve:
- Curved button shapes complement the circular form factor
- Bottom-of-screen buttons curve along the bottom edge
- System-provided curved layouts handle this automatically

#### Typography

- **Variable fonts** recommended for dynamic sizing across screen sizes
- Minimum text: 16px (18-20px preferred for primary content)
- Roboto is the system font
- Avoid more than 2 type sizes per screen

#### Rotating Crown / Bezel

- Similar to Apple's Digital Crown: scroll, adjust values, navigate
- Samsung Galaxy Watch: physical rotating bezel (tactile)
- Haptic feedback on detents
- Scrollable lists should respect crown/bezel rotation

#### Tiles (Swipeable Information Cards)

- Horizontal swipe from the watch face to access tiles
- Each tile: one screen of glanceable information
- Tap tile to launch full app
- Maximum complexity: one primary data point + one action per tile

---

### Watch Design Principles (Cross-Platform)

**Glanceability**
- Information must be readable in 2-3 seconds — the user's wrist is raised, and they will lower it quickly
- If it takes more than 3 seconds to comprehend, redesign it

**Information Density**
- Maximum 3-4 pieces of information visible at any time
- One primary piece of info should dominate the screen
- Supporting data should be visually subordinate

**Full-Screen Pages**
- No split views, ever — the screen is too small
- One page = one purpose
- Vertical scrolling for overflow, but keep it short (3-4 screens maximum)

**Prioritization**
- Ask: what is the ONE thing the user needs right now?
- Surface that one thing prominently
- Everything else is secondary — accessible but not in the way

**Visual Design**
- Bold accent colors on black backgrounds for hierarchy
- High contrast is mandatory — watches are viewed in direct sunlight
- Large, bold numerals for data
- Minimal chrome — every pixel is precious

---

## TV DESIGN (10-FOOT UI)

### General TV Principles

#### Viewing Context

- **Viewing distance**: 8-12 feet (2.4-3.6 meters)
- **Lean-back posture**: relaxed, passive consumption
- **Shared screen**: multiple viewers may watch simultaneously
- **Dim environment**: TVs are typically in dimly lit rooms
- **Limited input**: remote control with D-pad, not a mouse or touch

#### Safe Zones

- **5% margin from all edges** (overscan safe zone)
- Some TVs crop the outer pixels — never place critical content at the very edge
- Title-safe zone: 10% margin for text
- For a 1920x1080 screen: 96px inset on each side (5%), 192px for titles (10%)

#### Visual Design

- **Content-first**: large imagery, hero content — TV is a visual medium
- **Dark themes default**: reduce eye strain in dim rooms, save energy on OLED TVs
- **Avoid pure white (#FFFFFF)**: use off-whites (e.g., #E0E0E0) or work on dark backgrounds — pure white causes bloom on TVs and is uncomfortable
- **Background darkness**: #121212 to #1E1E1E for surfaces (not pure black #000000 on LCD — too flat)
- **On OLED TVs**: pure black is acceptable and saves power

#### Typography

- **Minimum body text**: 24px (at 1080p, viewed from 8-12 feet)
- **Recommended body text**: 28-32px
- **Titles**: 40-60px
- **Bold and medium weights only**: thin/light weights become illegible at distance
- **Small type scale**: 5-6 sizes maximum — keep it simple
- **Line length**: 40-60 characters maximum per line
- **Sans-serif fonts only**: serifs blur at TV resolution and distance

---

### Focus-Based Navigation

#### D-Pad Navigation

TV remotes use directional input: up, down, left, right, select (OK/Enter), back.

**Grid Design for Focus**
- Every screen must be designed as a logical grid for predictable focus movement
- Focus should move in the direction the user presses — no unexpected jumps
- Test: can a user reach every interactive element with only D-pad presses?

**Focus Movement Rules**
- Pressing right from the last item in a row: do NOT wrap to the next row (confusing)
- Pressing down from a row: focus should land on the nearest item in the row below
- Focus memory: when returning to a previously visited row, restore the last focused position

#### Focus Indicators (4 States)

Every interactive element needs four distinct visual states:

| State | Visual Treatment |
|-------|-----------------|
| **Idle** | Default appearance, no emphasis |
| **Focused** | Scale up (1.1x-1.2x), add glow/shadow, brightness shift, or subtle animation |
| **Pressed** | Slight scale down (0.95x), color change, or opacity shift |
| **Loading** | Skeleton or spinner overlay |

- Focus indicators must be visible from 10+ feet away
- Scale is the most universally recognizable focus indicator
- Combine scale with a shadow or glow for added clarity
- No hover states (there is no cursor)

---

### tvOS Specific

#### Parallax Effect

tvOS's signature visual effect:
- Images are composed of 2-5 separate layers
- When an item receives focus, layers shift independently based on remote movement
- Creates a sense of depth and physicality
- Create layered images in the Apple TV Parallax Previewer app
- Use LSR (Layered Source) image format

#### Siri Remote

- Touch surface: swipe for scrolling and browsing, press for selection
- Menu button: back navigation
- TV button: return to TV app / home screen
- Siri button: voice search and commands
- Clickpad: press edges for directional input, center for select

#### Top Shelf

- Premium content showcase area visible from the Apple TV home screen
- Full-width, large imagery
- Two styles: sectioned content (scrollable row) or full-screen poster
- Use this space for the most compelling, current content

#### tvOS Focus Engine

- Automatic focus management — the system determines which element receives focus
- `focusable()` modifier to control focusability
- `@FocusState` for programmatic focus management
- `focusSection()` to group related elements for predictable navigation

---

### Android TV / Google TV

#### Leanback Library

- Android's TV-specific UI framework
- BrowseFragment: the Netflix-style rows of cards pattern
- DetailFragment: hero image + metadata + action buttons
- SearchFragment: voice-activated search results
- PlaybackFragment: media playback controls

#### Layout Pattern

- Horizontal rows of content cards
- Vertical scrolling between rows (categories)
- Each row: a content category with horizontally scrollable items
- Focused card scales up (1.12x) with shadow

#### Predictive Back Gesture

- System back animation shows a preview of the previous screen
- Support `onBackPressedDispatcher` for proper back navigation
- Predictive back provides visual continuity when navigating backward

#### Voice Actions (Google Assistant)

- "Play [content]" — deep link to media playback
- "Show [category]" — navigate to a content section
- "Search for [query]" — launch search results
- Implement MediaSession for voice-controlled playback

---

### Fire TV (Amazon)

#### Design Guidelines

- Overscan safe zone: 5% from all edges (same as general TV)
- Dark theme: #232F3E (Amazon dark blue) or custom dark palette
- Focus ring: 4px solid highlight, high contrast against background
- Card dimensions: 228x128dp (landscape), 138x200dp (portrait)

#### Alexa Voice Integration

- Voice is a primary navigation method
- "Alexa, open [app]" — launch
- "Alexa, play [content]" — media playback
- Implement Alexa voice capabilities for natural interaction

#### Navigation Pattern

- Hub and spoke: main menu (hub) with sub-sections (spokes)
- Left-side navigation rail for top-level categories
- Content area to the right
- Focus starts on the content area, rail accessible by pressing left

---

## AUTOMOTIVE DESIGN

### CarPlay / CarPlay Ultra

#### Screen Sizes and Context

- Screen sizes range from 6.5" to 15"+ (vehicle-dependent, specified by car manufacturer)
- CarPlay Ultra spans the full dashboard including instrument cluster
- Driver is operating a moving vehicle — SAFETY IS THE ABSOLUTE PRIORITY
- All design decisions must minimize distraction

#### Template-Based Design

CarPlay uses predefined templates — custom layouts are extremely limited:
- **List template**: scrollable list of items (messages, contacts, playlists)
- **Grid template**: grid of icons (app launcher style)
- **Information template**: metadata display (now playing)
- **Point of interest template**: map with markers
- **Tab bar template**: tabbed navigation between sections
- Custom drawing is NOT available — you work within Apple's template constraints

#### Visual Rules

- Dark themes are standard (reduce nighttime glare)
- System font only (SF Pro) — no custom typefaces
- Limited color palette — primary tint color + system colors
- Minimal imagery — icons and album art only, no decorative graphics

#### Safety Standards (NHTSA)

- **Glance time**: < 2 seconds per individual glance at the screen
- **Total task time**: < 12 seconds for any complete task
- **Maximum number of steps**: 6 for any task (fewer is better)
- Eyes-off-road time must be minimized

#### Restricted Categories

CarPlay only permits apps in these categories:
- Media (music, podcasts, audiobooks)
- Navigation (maps, directions)
- Messaging (send/receive with Siri)
- Point of Interest (parking, fuel, charging, food)
- IoT (home automation, car accessories)

---

### Android Auto / AAOS (Android Automotive OS)

#### Design Specifications

| Element | Specification |
|---------|--------------|
| Minimum font size | 24sp |
| Minimum touch target | 76 x 76dp |
| Minimum spacing between targets | 23dp |
| Contrast ratio | 4.5:1 minimum for ALL items |
| Maximum list items visible | 6 (scrolling limited) |

#### Why Larger Targets

- Driving vibration reduces touch precision
- The screen is not at a stable distance (arm extended to dashboard)
- Users cannot look at the screen for extended periods
- Width can be sacrificed for increased height (vertical targets are easier to hit while driving)

#### Day/Night Modes

- Automatic switching based on ambient light sensor or headlight status
- Day mode: higher contrast, brighter colors
- Night mode: significantly reduced brightness, limited color palette, no white backgrounds
- Both modes must meet 4.5:1 contrast ratio

#### Voice-First Design

- **Voice is the primary interaction while driving** — touch is secondary
- Design every task to be completable entirely by voice
- Google Assistant integration for commands
- Minimize required screen touches
- Provide voice confirmations for actions

---

### Automotive Design Principles (Cross-Platform)

**Safety FIRST**
- Never, under any circumstance, design an interaction that distracts the driver
- When in doubt, remove the feature or make it voice-only
- The driver's eyes belong on the road

**Glanceable**
- All displayed information must be comprehensible in under 2 seconds
- One primary piece of information per screen (song title, next turn, message sender)
- Icons over text where possible

**Large Touch Targets**
- 76dp minimum (Android Auto) / template-enforced (CarPlay)
- Generous spacing prevents mis-taps
- Physical vibration of the vehicle makes small targets unreachable

**High Contrast**
- Variable ambient lighting: direct sunlight to pitch darkness
- 4.5:1 contrast ratio as absolute minimum
- Test in both bright sunlight and complete darkness

**Voice-First**
- Every task should be completable by voice alone
- Screen interactions should be confirmations, not data entry
- Pre-compose message replies, not free-text input

**Restrict Complexity**
- 4-5 steps maximum per task
- 6 list items maximum visible at once
- No scrolling while driving (systems may lock scrolling when in motion)
- No video playback while driving (blocked by system)

---

## KIOSK DESIGN

### Screen Sizes and Contexts

- **Small kiosks**: 15-22" (self-checkout, check-in, ticketing)
- **Medium kiosks**: 22-32" (wayfinding, information, retail)
- **Large kiosks**: 32-55" (digital signage with touch, interactive displays)

### Interaction Design

**Linear Workflows**
- 4-5 steps maximum from start to completion
- Clear progress indicators (step 1 of 4)
- Always-visible cancel/start-over button
- No dead ends — every screen has a clear next action

**Touch Targets**
- 44px minimum, 1cm x 1cm (10mm) recommended for general public
- 15mm targets for elderly-focused kiosks
- Generous spacing between targets (8mm minimum)
- Large primary action buttons (full-width or prominent placement)

### Accessibility (ADA Compliance)

- **Accessible height**: interactive elements between 15" and 48" from floor
- **Wheelchair reach**: forward reach maximum 48", side reach maximum 54"
- **Voice guidance**: text-to-speech for all screen content
- **Adjustable fonts**: user-selectable text size
- **High contrast mode**: user-activatable
- **Timeout extensions**: allow users to request more time
- **Physical braille**: on hardware buttons if present

### Environmental Considerations

**Outdoor Kiosks**
- Screen brightness: 2,500-5,000 nits (vs ~500 nits for indoor)
- Anti-reflective coatings on screen
- Sunlight-readable designs: high contrast, bold colors
- Weatherproof touch (works with gloves, rain on screen)

**Indoor Kiosks**
- Standard brightness: 300-500 nits
- Consider ambient lighting (retail stores vary widely)
- Glare from overhead lights — angle screen slightly

### Session Management

- **Idle timeout**: 30-60 seconds of inactivity → attract screen
- **Attract screen**: motion graphics or clear "Touch to start" prompt
- **Privacy**: clear all personal data on session end
- **Error recovery**: automatic reset after extended error state
- **Receipt/confirmation**: provide before ending session

---

## E-INK DESIGN

### Display Characteristics

**Monochrome First**
- Standard E Ink: black, white, and 16 levels of gray
- Design primarily for monochrome — it is the most common E Ink type
- Gray levels are visible but lack the precision of LCD grayscale

**Color E Ink (Kaleido 3, Gallery 3)**
- Kaleido: color filter over monochrome — colors appear ~40% less vivid than LCD
- Gallery: native color E Ink — better but still muted
- Never rely on color alone to convey meaning — it may be invisible on monochrome devices
- Desaturated color palettes work best — vivid colors look muddy

### Refresh Behavior

- **Full refresh**: 100-300ms, flashes black before redrawing — best quality, most disruptive
- **Partial refresh**: faster, updates only changed regions — may leave ghosting artifacts
- **Fast/A2 mode**: near-instant updates, lowest quality, significant ghosting
- **Regal waveform**: optimized for mixed content, balances speed and quality

Design implications:
- NO animations — each frame requires a refresh cycle
- Minimize full-screen redraws (they flash the entire screen black/white)
- Design state changes as page transitions, not smooth animations
- Progress indicators: use discrete steps, not smooth bars

### Typography for E-Ink

- Fonts with open counters and healthy x-height reproduce best
- Recommended: Literata, Bookerly, Charter, Georgia
- Pure black (#000000) on pure white (#FFFFFF) for body text — no subtle grays for text
- Minimum body text: 12pt (16pt preferred for extended reading)
- Line spacing: 1.4-1.6x for comfortable reading
- Avoid thin/light weights — they render poorly on E Ink

### Layout Principles

**Page-Based, Not Scroll-Based**
- E Ink devices are optimized for page turns, not smooth scrolling
- Each page should be a complete, self-contained unit of content
- Pagination over infinite scroll

**Minimize Redraws**
- Every pixel change costs energy and time
- Group related updates into single redraws
- Avoid idle animations, blinking cursors, or live clocks with seconds

**Battery Considerations**
- E Ink displays consume power only when changing the image
- A static page consumes zero display power
- This enables weeks of battery life — design to take advantage of it
- Avoid frequent automatic refreshes

**Contrast and Readability**
- Pure black on white for text (no anti-aliased gray text — it looks fuzzy on E Ink)
- Borders and dividers: use solid 1-2px black lines, not subtle grays
- Icons: solid, filled styles work better than outline styles
- Images: convert to high-contrast, dithered versions for best results

### Common E-Ink Devices

| Device | Screen | Color | Interaction |
|--------|--------|-------|-------------|
| Kindle | 6-10.2" | Monochrome | Touch + buttons |
| Kobo | 6-10.3" | Mono / Kaleido | Touch |
| reMarkable | 10.3" | Monochrome | Pen + touch |
| Boox | 6-13.3" | Mono / Kaleido | Pen + touch (Android) |
| Daylight | 10.5" | Monochrome | Touch (backlit) |

### E-Ink Design Checklist

- [ ] All text is pure black on white (no gray text)
- [ ] No animations or smooth transitions
- [ ] Page-based navigation, not scroll-based
- [ ] Icons are solid/filled, not outline
- [ ] Color is not the sole indicator of meaning
- [ ] Large touch targets (E Ink response is slower than LCD)
- [ ] Minimal full-screen redraws
- [ ] Tested at actual E Ink refresh rates
- [ ] Font has open counters and healthy x-height
- [ ] Layout works in both portrait and landscape

---

## Quick Specifications: Watch / Wear OS

### Apple Watch Specifications by Size

| Case Size | Screen Width | Screen Height | Corner Radius | Scale Factor |
|-----------|-------------|---------------|---------------|-------------|
| 42mm (SE) | 176px | 215px | 36px | 2x |
| 44mm (S10) | 198px | 242px | 36px | 2x |
| 46mm (S10) | 208px | 254px | 40px | 2x |
| 49mm (Ultra 3) | 205px | 251px | 40px | 2x |

### Complication Design

Complications are small data displays on the watch face:

- **Circular Small** — 32x32pt. Icon or single metric only.
- **Modular Small** — 52x52pt. Short text or icon with one data point.
- **Modular Large** — Full width (varies). Multi-line content: title + up to 3 lines of body.
- **Rectangular** — 154x68pt (varies by watch size). Rich content: images, gauges, text combinations.
- **Corner** — Curved text along the watch face edge. Maximum 4-5 characters.

Design rules: complications must be readable at arm's length (approximately 30cm). Use SF Compact Rounded for complication text. Minimum font size 13pt. Tint color should be a single accent per complication.

### Glanceable Information Hierarchy

Watch content must be parsed in under 3 seconds:

1. **Primary metric** — The single most important number/status. Largest text, highest contrast.
2. **Context label** — What the metric means. Secondary vibrancy, smaller text.
3. **Trend indicator** — Arrow, spark line, or color shift showing direction.
4. **Action hint** — One obvious tap target or instruction. Maximum one action per screen.

Never show more than 3 information groups on a single watch screen. If content requires scrolling, use a paginated layout (vertical page dots), not a long scroll.

### Crown and Bezel Interactions

- **Digital Crown scroll** — Default scroll behavior for lists. Haptic detents every 4pt of scroll offset.
- **Digital Crown precise input** — Used for pickers (time, date, numeric). Each detent maps to one value step.
- **Bezel rotation (Wear OS)** — Equivalent to Digital Crown. Rotary input events map to scroll or value selection.
- **Double-tap gesture (Apple Watch)** — Primary hand gesture for one-handed interaction. Maps to the "primary action" on the current screen.

### Small Screen Typography

| Role | Font | Size | Weight |
|------|------|------|--------|
| Large Title | SF Compact Rounded | 22pt | Bold |
| Headline | SF Compact Rounded | 17pt | Semibold |
| Body | SF Compact Rounded | 15pt | Regular |
| Caption | SF Compact Rounded | 13pt | Regular |
| Minimum readable | SF Compact Rounded | 11pt | Medium |

Line lengths: maximum 20-25 characters per line on a 44mm watch. Use sentence fragments, not full sentences. Abbreviate aggressively: "Mon" not "Monday", "3h 22m" not "3 hours 22 minutes".

## Quick Specifications: TV / 10-Foot UI

### Focus-Based Navigation

TV interfaces have no cursor or touch. Navigation is entirely focus-based:

- **Focus ring** — A visible highlight (border, scale, or glow) indicating the currently focused element. Minimum 4px visible border or 1.05x scale increase.
- **Focus movement** — D-pad (up/down/left/right) moves focus between elements. Focus movement must be predictable: pressing "right" should move to the element visually to the right.
- **Focus memory** — When a user navigates away from a section and returns, focus should restore to the last-focused element within that section.
- **Focus trapping** — Modals and overlays trap focus within their bounds. D-pad navigation cycles through the modal's focusable elements.

### Overscan Safe Area

Legacy TVs crop the outer edges of the signal. Even modern TVs may overscan slightly:

- **Action safe area** — 5% inset from all edges (where interactive elements must live)
- **Title safe area** — 10% inset from all edges (where text must live)
- **Modern practice** — Most streaming apps use a 48px inset from all edges as a safe margin on 1080p, or 96px on 4K

### Reading Distance Typography

TV viewers sit 2-3 meters from the screen. Typography must be sized accordingly:

| Role | Minimum Size (1080p) | Minimum Size (4K) | Notes |
|------|---------------------|--------------------|-------|
| Hero title | 48px | 72px | Maximum 2 lines |
| Section title | 32px | 48px | Single line preferred |
| Card title | 24px | 36px | Maximum 2 lines |
| Metadata/subtitle | 18px | 28px | Single line |
| Minimum readable | 16px | 24px | Never go below this |

Font weight: use medium to bold weights. Thin and light weights disappear at TV viewing distance. Prefer sans-serif families with open counters and generous x-height.

### D-Pad Navigation Patterns

- **Grid navigation** — Focus moves in a 2D grid. Arrow keys move one cell. Wrap-around is optional but must be consistent (all rows wrap or none do).
- **Rail/carousel navigation** — Horizontal list of cards. Left/right moves between cards. Up/down exits the rail to the rail above/below.
- **Nested focus** — Pressing Select on a card expands it or navigates into a detail view. Back button returns to the previous focus context.
- **Long-press** — Reserved for secondary actions (add to watchlist, info panel). Never required for primary interactions.

### Remote Control UX

- **Minimize button count** — Assume 5 buttons: D-pad (4 directions + select) and Back. Design every flow to be completable with these 5 inputs.
- **Voice search** — Provide voice input as a shortcut for text entry. On-screen keyboards are painful with D-pad navigation.
- **Idle timeout** — If no input for 4+ hours, show a "still watching?" prompt to avoid burning static UI into OLED panels.

### Card-Based Layouts

TV UI is overwhelmingly card-based:

- **Standard card** — 16:9 landscape thumbnail with title below. Focus state scales the card to 1.05x-1.1x with an elevation increase.
- **Wide card** — 2.39:1 cinematic ratio for hero/featured content.
- **Tall card** — 2:3 portrait for book covers, profiles, app icons.
- **Card spacing** — 16-24px gap between cards. Enough to clearly separate but not so much that the screen feels empty.
- **Row labels** — Left-aligned, above each carousel rail. 24-32px font size with 16px gap to the first card.

## Quick Specifications: Automotive / HUD

### Driver Distraction Guidelines

The National Highway Traffic Safety Administration (NHTSA) defines strict limits:

- **Single glance time** — Maximum 2 seconds per glance away from the road
- **Total task time** — Maximum 12 seconds cumulative for any single task (e.g., setting a destination)
- **Total glances** — Maximum 6 glances for a single task
- **Eyes-off-road time** — 85th percentile total eyes-off-road time must not exceed 12 seconds

These are not suggestions. Automotive OEMs certify against these guidelines. Infotainment UI that exceeds these limits can result in regulatory action.

### NHTSA Compliance Checklist

1. No scrolling text or animations that require sustained attention
2. No tasks requiring more than 6 sequential inputs
3. Voice-first for any task exceeding the 12-second glance budget
4. Automatic lockout of complex functions when the vehicle is in motion (above 5 mph)
5. Haptic or audio confirmation for every touch input (driver cannot look to confirm)
6. No video playback on the driver-facing display while in motion

### Glance Time Limits by Content Type

| Content | Max Glance | Interaction |
|---------|-----------|-------------|
| Current song / station | 1s | None (read-only) |
| Navigation next turn | 1s | None (read-only) |
| Temperature adjustment | 1.5s | Single tap or voice |
| Contact selection | 2s | Voice-preferred |
| Destination entry | Voice only | Text entry locked at speed |
| Message reading | Voice only | Read aloud, never displayed |

### Night Mode

Automotive displays must support an aggressive night mode:

- **Background**: Pure black (#000000) to minimize light emission
- **Text**: Amber or red-shifted white (color temperature 2700K-3200K) to preserve scotopic (night) vision
- **Brightness**: Auto-dimming to 1-5 nits in full darkness (phone screens are typically 200-1000 nits)
- **No white surfaces**: Even "light gray" backgrounds can cause glare on the windshield
- **HUD (head-up display)**: Green or white monochrome, 15-25pt text projected at optical infinity (focused at 2-3 meters ahead of the windshield)

### Large Touch Targets

Drivers interact with gloved hands, without looking, while the vehicle vibrates:

- **Minimum touch target**: 18mm x 18mm (approximately 72px at typical automotive DPI)
- **Recommended touch target**: 24mm x 24mm
- **Spacing between targets**: Minimum 8mm gap
- **Physical controls preferred**: Climate, volume, and hazard lights should remain physical knobs/buttons, not touchscreen-only

### Voice-First Interaction

For tasks exceeding a single glance:

- Voice is the primary input, touch is the fallback
- Provide confirmation prompts: "Navigating to 123 Main Street. Is that correct?"
- Wake word should be configurable (users in noisy environments may prefer push-to-talk)
- Visual feedback for voice state: listening, processing, confirming (simple icon states, not text)
