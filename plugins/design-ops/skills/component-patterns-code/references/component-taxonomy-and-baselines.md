# Component Taxonomy, Tokens, and Baseline Rules

Detail behind the rules in SKILL.md: the foundational component set, the token categories components consume, and the accessibility and responsive baselines.

## Component Taxonomy

Organizing components into functional categories creates a shared vocabulary for the team and ensures coverage. The taxonomy below covers the foundational set that virtually every product needs.

### Action Components

Components that trigger operations. The user clicks, taps, or activates them to cause something to happen.

- **Button** — the primary action trigger; variants include primary, secondary, ghost, danger, icon-only
- **IconButton** — a button with only an icon and an accessible label; used where space is constrained
- **FAB (Floating Action Button)** — a persistent action button layered over content, common on mobile
- **SegmentedControl** — a group of buttons where exactly one is selected, acting as a toggle between views

### Input Components

Components that accept user data.

- **TextField** — single-line text entry with optional label, helper text, validation, and character count
- **TextArea** — multi-line text entry with auto-resize and character limit
- **Select** — a dropdown menu for choosing one option from a predefined list
- **Combobox** — a searchable select that combines text input with option filtering
- **Checkbox** — a binary or indeterminate toggle for non-exclusive options
- **RadioGroup** — a set of mutually exclusive options
- **Toggle/Switch** — an on/off binary control with immediate effect
- **Slider** — a draggable track for selecting a numeric value within a range
- **DatePicker** — a calendar-based date selection with keyboard support

### Feedback Components

Components that communicate status, results, or system state to the user.

- **Toast/Snackbar** — a temporary, non-blocking notification that auto-dismisses
- **Banner** — a persistent message pinned to a region of the interface
- **Dialog/Modal** — a focused overlay requiring user attention and response
- **ProgressBar** — a visual indicator of completion percentage for a known-duration operation
- **Skeleton** — a placeholder shape indicating content is loading

### Navigation Components

Components that move the user between views, sections, or pages.

- **Tabs** — horizontal or vertical tab strips for switching between panels of content
- **Breadcrumb** — a hierarchical trail showing the user's location within a navigation structure
- **Sidebar/Drawer** — a vertical navigation panel, collapsible on smaller screens
- **Pagination** — page controls for navigating multi-page data sets
- **BottomNav** — a mobile navigation bar anchored to the screen bottom

### Content Components

Components that present or contain information.

- **Card** — a bounded container for a cohesive unit of content and related actions
- **Avatar** — a circular or rounded image representing a user, entity, or placeholder
- **Badge** — a small indicator attached to another element showing count or status
- **Chip/Tag** — a compact element representing an attribute, filter, or selection
- **Tooltip** — a small overlay providing supplementary text on hover or focus
- **Accordion** — a vertically stacked set of collapsible sections

### Data Components

Components optimized for displaying structured datasets.

- **Table** — a two-dimensional grid of rows and columns with sortable headers, pagination, and row selection
- **List** — a vertical sequence of related items with optional actions
- **Grid** — a responsive multi-column layout of repeated content items
- **Chart** — a visual representation of data (bar, line, pie, scatter)

## Design Token Integration

Every component must consume design tokens rather than hardcoded values. Tokens are the contract between design and code. They ensure that when the design system changes a color, spacing value, or font, every component updates automatically.

### Token Categories in Components

- **Color tokens:** `--color-primary`, `--color-surface`, `--color-on-surface`, `--color-error`, `--color-border`
- **Spacing tokens:** `--space-xs`, `--space-sm`, `--space-md`, `--space-lg`, `--space-xl`
- **Typography tokens:** `--font-family-body`, `--font-size-sm`, `--line-height-normal`, `--font-weight-medium`
- **Radius tokens:** `--radius-sm`, `--radius-md`, `--radius-lg`, `--radius-full`
- **Shadow tokens:** `--shadow-sm`, `--shadow-md`, `--shadow-lg`
- **Motion tokens:** `--duration-fast`, `--duration-normal`, `--easing-standard`, `--easing-decelerate`
- **Size tokens:** `--size-touch-target` (44px minimum), `--size-icon-sm`, `--size-icon-md`

## Accessibility-First Component Engineering

Accessibility is not an enhancement. It is a baseline requirement. Components built with accessibility from the start are cheaper to maintain, more robust, and usable by everyone.

### Keyboard Navigation

- Every interactive component must be reachable via Tab key.
- Custom widgets must implement the expected keyboard pattern from WAI-ARIA Authoring Practices: arrow keys for menus, tabs, and radio groups; Enter/Space for activation; Escape for dismissal.
- Focus order must match the visual order. If CSS reorders elements visually, ensure `tabindex` or DOM order reflects the intended sequence.
- Focus must never become trapped (except intentionally in modals, where a focus trap is required).
- The visible focus indicator must meet 3:1 contrast and should not rely solely on browser defaults.

### ARIA Roles and States

- Use semantic HTML first (`<button>`, `<input>`, `<dialog>`, `<nav>`). ARIA is a supplement, not a replacement.
- Dynamic state changes require ARIA state updates: `aria-expanded`, `aria-selected`, `aria-checked`, `aria-busy`, `aria-invalid`, `aria-disabled`.
- Live regions (`aria-live="polite"` or `aria-live="assertive"`) announce dynamic content changes (toast notifications, form validation messages, loading completions).
- Every icon-only button requires `aria-label`. Every image requires `alt` text or `aria-hidden="true"` if decorative.

### Screen Reader Announcements

- Toast notifications must use `role="status"` or `aria-live="polite"` so screen readers announce them without interrupting the current task.
- Error messages should be linked to their inputs via `aria-describedby`.
- Loading states should use `aria-busy="true"` on the loading region.
- Route changes in SPAs should announce the new page title via a live region or focus management.

## Responsive Component Patterns

Container query code is in `css-modern-patterns.md` (section 1).

### Fluid Sizing

Use `clamp()` for typography and spacing that scales smoothly between breakpoints without abrupt jumps:

```css
font-size: clamp(1rem, 0.5rem + 1.5vw, 1.5rem);
padding: clamp(0.75rem, 2vw, 2rem);
```

### Touch Target Minimums

Per WCAG 2.5.8 (Target Size), interactive elements must be at least 24x24 CSS pixels (AA), or have enough spacing; 44x44 CSS pixels is 2.5.5 Target Size (Enhanced), Level AAA. Apple HIG specifies 44pt minimum. Material Design specifies 48dp. Always err on the side of larger targets on touch devices.

This is directly informed by Fitts's Law (see `cognitive-psychology-ux`): the time to reach a target is a function of distance and target size. Smaller targets increase error rates and frustration, especially under mobile conditions (one-handed use, walking, glare).

