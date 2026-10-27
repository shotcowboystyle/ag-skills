# Dashboards and Tables: Behavior, Operations, and Advanced Tables

Companion to `dashboard-layout-patterns.md` (grids, KPI rows, dashboard types) and `data-table-mastery.md` (column types, sort, filter, pagination, density, accessibility). This file covers what those two do not: dashboard information architecture, interaction, real-time data, filters and drill paths, personalization, alerts, loading, export, performance, and advanced table behavior (grouping, trees, inline editing, grid vs. table).

Tables default to native `<table>` semantics; use `role="grid"` only for an interactive grid that implements arrow-key cell navigation (see `data-table-mastery.md` section 15).

---

## Dashboard Information Architecture

### Organizing the Information Hierarchy

Structure every enterprise dashboard around a clear information hierarchy that maps to how decision-makers consume data. Place the most critical metrics at the top of the visual hierarchy and allow progressive disclosure into supporting detail.

**The Inverted Pyramid Model.** Borrow from journalism: lead with the headline number (revenue, uptime, pipeline value), follow with supporting context (trend, comparison, breakdown), and provide access to the raw detail on demand. Never force users to scroll or click to reach the single most important number on the dashboard.

**Metric Taxonomy.** Organize metrics into three tiers:

- **Tier 1 -- North Star metrics.** The 3-5 numbers the business lives and dies by. Display these as large-format KPI cards at the top of the viewport. Examples: monthly recurring revenue, system uptime, customer satisfaction score.
- **Tier 2 -- Diagnostic metrics.** The 8-15 numbers that explain why Tier 1 metrics moved. Present these as charts and medium-format cards in the body of the dashboard. Examples: churn rate by segment, error rate by service, conversion funnel by channel.
- **Tier 3 -- Operational detail.** The hundreds of data points that support investigation. Expose these through drill-down, expandable sections, or linked detail views. Examples: individual transaction logs, per-user activity, raw event data.

**Grouping Strategy.** Group metrics by business domain (Sales, Engineering, Support), by workflow stage (Acquire, Activate, Retain), or by entity (Product A, Product B). Never group by chart type -- placing all bar charts together provides no semantic value. Each group deserves a visible section header with optional collapse.

**Reading Order.** Respect the F-pattern for left-to-right reading cultures. Place the primary KPI summary row across the top, the most critical diagnostic chart in the upper-left quadrant, and secondary views below and to the right. Conduct eye-tracking studies or heatmap analysis to validate placement for high-stakes dashboards.

---

## Widget and Card Design System

### Anatomy of a Dashboard Card

Every dashboard card is a self-contained unit of insight. Standardize the anatomy across the entire dashboard to reduce cognitive switching cost.

**Required elements of a KPI card:**

1. **Metric label.** A concise, unambiguous name. Use business terminology the audience already knows. Avoid acronyms without context. Place the label at the top-left of the card in secondary-weight typography (14-16px).
2. **Primary value.** The headline number displayed in large, high-contrast type (24-48px depending on card size). Apply appropriate formatting: currency symbols, percentage signs, decimal precision, thousand separators. Never display raw integers for financial data.
3. **Trend indicator.** An arrow or directional icon combined with a percentage or absolute delta. Color-code the trend: green for favorable movement, red for unfavorable, neutral gray for negligible change. Always clarify the comparison basis (vs. last week, vs. target, vs. same period last year).
4. **Sparkline or micro-chart.** A small, unadorned line chart showing the last 7-30 data points. Remove axes, labels, and gridlines from sparklines -- they exist solely to communicate shape and direction. Place the sparkline below or beside the primary value.
5. **Contextual footer.** A single line of secondary information: the time range, data freshness timestamp, sample size, or comparison benchmark. Display in muted text (12-13px) at the bottom of the card.

**Card sizing standards on a 12-column grid:**

- **Small card (3 columns).** Single KPI with trend and sparkline. Ideal for Tier 1 summary rows.
- **Medium card (4-6 columns).** KPI with an accompanying chart or breakdown table. Ideal for Tier 2 diagnostics.
- **Large card (6-12 columns).** Full chart with filters, legend, and interactive controls. Ideal for analytical exploration.

**Card interaction patterns.** Support hover to reveal secondary actions (expand, export, configure). Support click-through to a detail view or drill-down. Provide a kebab menu (three-dot icon) at the top-right corner for card-level actions: edit, remove, duplicate, export, set alert.

**Card states** (from the dashboard block specs):
- **Loading**: Skeleton pulse animation (gray-200 bg, rounded shapes matching content)
- **Error**: Card with error icon + "Failed to load" + retry link
- **Empty**: Show $0 or 0 — never hide the card
- **Stale data**: Show last-updated timestamp, slightly dimmed

**Screen readers**: KPI cards should have aria-label summarizing the metric ("Revenue: $45,230, up 12% from last month").

---

## Page Shells for Dashboards

### Full-Width Dashboard
- Top: KPI card row (full width)
- Middle: primary chart (full width or 2/3) + secondary widget (1/3)
- Bottom: data table (full width)
- Sidebar: navigation (fixed left)

### Two-Panel Dashboard
- Left panel (60-70%): charts and primary data
- Right panel (30-40%): activity feed, notifications, quick actions
- Top: KPI cards spanning full width

### Grid Dashboard
- 2x2 or 3x2 grid of equal-sized chart/widget blocks
- Each block: self-contained visualization with title
- Drag-and-drop reordering (advanced)
- Responsive: 2 cols at lg, 1 col at md

### Sidebar + Main Content
- Fixed sidebar (240-280px): navigation + filters
- Main area: scrollable dashboard content
- Top bar: fixed header with search + user menu
- Content padding: 24-32px

---

## Interactive Patterns

Static charts inform; interactive charts enable exploration. Each interaction pattern below serves a distinct analytical task.

### Tooltip Design

Tooltips are the most common chart interaction. They answer "what exactly is this data point?"

- **Trigger**: Hover on desktop, tap on touch. Use a 200ms delay to prevent flicker on mousemove.
- **Content hierarchy**: Primary value (bold, larger), secondary context (category, date), optional tertiary (percentage, rank).
- **Positioning**: Prefer top-right of the cursor. Flip when near viewport edges. Never obscure the data point being inspected.
- **Formatting**: Use locale-aware number formatting. Abbreviate large numbers (1.2M, not 1,200,000). Include units.
- **Multi-series tooltips**: When multiple lines share an x-axis, show a vertical crosshair and list all series values in a single tooltip, sorted by value descending.

### Zoom and Pan

Zoom and pan enable focus on dense regions without losing global context.

- **Semantic zoom**: Change the level of detail as users zoom in — show aggregated values at zoom-out, individual data points at zoom-in. This is more valuable than geometric zoom alone.
- **Axis zoom**: Allow zooming on a single axis (e.g., zoom the x-axis time range without changing the y-axis scale). Scroll-wheel on the axis area is a natural mapping.
- **Reset control**: Always provide a visible "Reset zoom" button. Users who zoom in frequently lose their bearings.
- **Minimap**: For large datasets, show a small overview with a viewport rectangle indicating the current zoom region.

### Drill-Down

Drill-down moves from aggregate to detail, revealing the data behind a summary.

- **Visual cue**: Use a pointer cursor and subtle underline or highlight to indicate that a bar, slice, or cell is clickable.
- **Breadcrumb trail**: Show the drill path (All > Region > Country > City) so users can navigate back to any level.
- **Animation**: Animate the transition — bars splitting into sub-bars, a map zooming into a region. This preserves spatial context and reduces disorientation.
- **Data-level indicator**: Show a small indicator (e.g., a "+" icon or chevron) on aggregated elements that have children.

### Brush Selection

Brushing selects a subset of data by dragging across a range.

- **1D brush**: Drag along the x-axis to select a time range. Show the selected range with a highlighted overlay and handles for resizing.
- **2D brush**: Drag a rectangle on a scatterplot to select a cluster. Show the selected region with a semi-transparent overlay.
- **Snap behavior**: For categorical axes, snap the brush to category boundaries. For continuous axes, allow free positioning.
- **Selection count**: Display the number of selected data points and aggregate statistics (mean, sum) for the selection.

### Linked Views (Coordinated Multiple Views)

Linked views connect multiple charts so that interaction in one updates all others.

- **Highlight linking**: Hovering a category in one chart highlights the same category across all linked charts. Use consistent color encoding.
- **Filter linking**: Brushing a range in one chart filters the data shown in all linked charts. This is the most powerful exploration pattern for multivariate data.
- **Detail linking**: Clicking a data point in an overview chart updates a detail panel showing the individual record or a zoomed sub-chart.
- **Implementation**: Use a shared state store (React context, Zustand, or Observable reactive variables) to synchronize selection state across components.

### Detail-on-Demand

Shneiderman's information-seeking mantra: "Overview first, zoom and filter, then details on demand."

- **Progressive disclosure**: Start with the highest-level summary. Let users drill, filter, and hover to reach granular data.
- **Side panel**: Clicking a data point opens a detail panel (not a modal) showing the full record, related records, and contextual actions.
- **Data table toggle**: Provide a "View as table" toggle that shows the underlying data in a sortable, searchable table. Analysts trust the raw numbers.

---

## Filter and Drill-Down Patterns

### Global Filters

Place global filters (date range, business unit, region, product) in a persistent filter bar at the top of the dashboard, immediately below the header. Global filters affect every card and chart simultaneously.

**Filter bar design:**

- Display active filter values as dismissible chips or pills.
- Provide a "Reset all filters" action.
- Use appropriate filter controls: date picker for time ranges, multi-select dropdown for categorical dimensions, search-ahead for high-cardinality fields.
- Persist filter state in the URL (query parameters or hash) so filtered views can be bookmarked and shared.

### Cross-Filtering

Implement cross-filtering so that selecting a segment in one chart filters all other charts on the dashboard. For example, clicking a bar in a "Revenue by Region" chart filters the trend line, table, and map to show only that region.

Visually dim (reduce opacity to 30-40%) the unselected data rather than removing it entirely, so users retain context of the whole while focusing on the part. Display a visible indicator that cross-filtering is active and provide a one-click clear action. Provide both per-chart reset (click to clear this filter) and global reset (clear all filters). Show active filter count.

### Drill-Down and Drill-Through

**Drill-down** navigates deeper within the same card: Country > State > City > Store. Provide breadcrumb navigation within the card to track depth and allow jumping back to any level.

**Drill-through** navigates to a separate detail page or dashboard with the selected dimension as context. Open drill-through targets in the same window with a clear back-navigation path, or in a new tab if the user holds Cmd/Ctrl while clicking.

Debounce filter inputs (300ms) to prevent excessive API calls while typing. When filtering or sorting changes the data, announce the change to screen readers via a live region.

---

## Real-Time Dashboard Patterns

### Auto-Refresh

Implement polling-based auto-refresh for dashboards where latency tolerance is 5 seconds or greater. Display a countdown or timestamp showing next refresh. Allow users to pause auto-refresh during analysis -- nothing is more frustrating than a chart shifting while a user is mid-interpretation.

Refresh intervals by dashboard type:

- **Infrastructure monitoring:** 5-15 seconds.
- **Operational dashboards (call center, logistics):** 15-30 seconds.
- **Sales and marketing dashboards:** 5-15 minutes.
- **Executive dashboards:** 30-60 minutes or manual refresh.

Display a last-updated timestamp in the dashboard header. Use subtle animation (fade or pulse) to indicate refreshed data rather than jarring full-page reloads.

### WebSocket and Server-Sent Events

Use persistent connections for dashboards requiring sub-5-second latency. WebSocket connections support bidirectional communication (useful when users send filter changes that affect the data stream). Server-Sent Events (SSE) are lighter-weight for unidirectional server-to-client updates.

Design for connection resilience: display a connection status indicator (connected, reconnecting, disconnected). Implement exponential backoff on reconnection attempts. Cache the last known state locally so the dashboard remains useful during brief disconnections.

### Streaming Data Visualization

For dashboards displaying streaming data (log viewers, trading terminals, IoT sensor feeds):

- Use a fixed-width time window that slides forward (last 5 minutes, last 1 hour). New data enters from the right; old data exits from the left.
- Buffer incoming data points and render in batches (every 100ms-1s) rather than on every event to prevent rendering thrash.
- Provide a pause/freeze control that stops the visual scroll while continuing to buffer data, allowing users to inspect a moment in time.
- Implement data decimation for historical ranges: when zoomed out, aggregate thousands of points into statistical summaries (min, max, mean, percentiles).
- **Append-only rendering**: For line charts, compute only the new path segment rather than recomputing the entire path. Use `requestAnimationFrame` to schedule updates.

### Animation for Data Changes

Animation in data visualization serves a functional purpose: it helps users track which elements moved and where.

- **Transition duration**: 300-500ms for value updates. Shorter than UI animation because data updates are frequent.
- **Easing**: Use `ease-out` for elements entering (they arrive fast, settle slowly). Use `ease-in-out` for elements moving (smooth acceleration and deceleration).
- **Enter/Exit**: New data points fade in (opacity 0 to 1). Exiting data points fade out (opacity 1 to 0). Do not use movement for enter/exit — it implies the data moved rather than appeared/disappeared.
- **Value changes**: Bars grow or shrink smoothly. Numbers count up or down (use a counter animation). Line chart points interpolate to new positions.
- **Avoid gratuitous animation**: If the chart updates every second, do not animate every update. Show the latest state instantly and reserve animation for significant changes (threshold crossings, anomalies).

### Optimistic Rendering

In dashboards connected to user actions (e.g., a sales team dashboard), render expected changes immediately.

- **Pattern**: When a user marks a deal as "closed," update the revenue chart immediately while the server request is in-flight. If the server rejects, roll back with a subtle flash to indicate the correction.
- **Confidence indicators**: For predictive dashboards, show the predicted value with a dashed line or confidence interval band, and the actual confirmed value with a solid line.

---

## Dashboard Loading Patterns

### Progressive Loading

Load and render Tier 1 KPI cards first (they typically require the simplest queries). Render chart skeletons with correct dimensions while data loads to prevent layout shift. Load Tier 2 and Tier 3 elements in priority order. Use HTTP/2 multiplexing or GraphQL batching to parallelize data fetches.

### Skeleton States

Display skeleton placeholders that match the exact dimensions and layout of the final content. For KPI cards, show a rectangular pulse animation where the number will appear. For charts, show the axes and chart area outline with a shimmer effect. Never use a single full-page spinner -- it provides no spatial information about what is loading.

### Stale Data Indicators

When cached data is displayed while fresh data loads, mark it clearly. Apply a subtle overlay or badge reading "Updating..." or "Data from 5 minutes ago." After the fresh data loads, briefly highlight the changed values with a background flash (200-300ms fade). If a data source fails entirely, display the last known value with a visible error badge and a retry action.

---

## KPI Targets and Comparisons

### Goal Tracking

For KPIs with defined targets, display a progress bar or bullet chart showing actual vs. goal. Use distinct visual treatment when the metric exceeds goal (celebratory green), is on-pace (neutral), or is behind (warning amber or red). Show the numeric gap ("$42K to goal" or "12% above target") alongside the visual indicator.

### Comparative Metrics

Support multiple comparison modes within a single KPI card: absolute value, percentage change, index (normalized to 100). Allow users to toggle between comparison bases: previous period, same period last year, custom baseline, organizational benchmark.

---

## Alert and Threshold Design

### Visual Encoding of States

Define three to five severity levels with consistent visual encoding:

| State | Color | Icon | Behavior |
|---|---|---|---|
| Normal | Green or neutral gray | Checkmark or none | Default display, no special treatment |
| Attention | Blue | Info circle | Informational, no action required |
| Warning | Amber/Yellow | Triangle exclamation | Investigation recommended |
| Critical | Red | Circle exclamation | Immediate action required |
| Emergency | Red with pulse | Filled octagon | System-level alert, often with audible signal |

Apply these encodings to card borders, badge indicators, chart annotation lines, and notification banners consistently.

### Threshold Configuration

Allow administrators to define thresholds per metric: static thresholds (revenue below $1M) or dynamic thresholds (more than 2 standard deviations from the rolling mean). Display threshold lines on charts as dashed horizontal rules with labels. Provide a threshold configuration panel accessible from the card's kebab menu.

### Alert Channels

Connect dashboard thresholds to notification channels: in-app notification center, email digest, Slack/Teams integration, SMS for critical alerts. Allow per-user alert preferences. Implement alert deduplication and cooldown periods to prevent notification fatigue during sustained threshold breaches.

---

## Dashboard Navigation

### Sidebar Navigation

Use a collapsible left sidebar to organize multiple dashboards and dashboard groups. Display icons with labels; collapse to icon-only to reclaim space. Support nested groups (e.g., "Sales > Regional > EMEA"). Highlight the currently active dashboard. Provide search/filter within the sidebar for organizations with dozens of dashboards.

### Tabbed Dashboards

Use horizontal tabs within a single dashboard to separate views that share the same global filters (Overview, Details, Trends, Alerts). Limit to 5-7 tabs. Persist the active tab in the URL for shareability. Lazy-load tab content to improve initial load time.

### Drill-Through Navigation

When a user clicks a chart element to drill through to a detail dashboard, maintain the filter context and provide a clear breadcrumb trail: "Executive Summary > Regional Performance > EMEA > Germany." Support browser back-button navigation through the drill-through chain.

### Breadcrumb Design

Display breadcrumbs below the dashboard header when the user has navigated away from the top-level view. Each breadcrumb segment is clickable. Truncate long breadcrumb chains with an ellipsis menu that expands on click. Ensure breadcrumbs reflect both the dashboard hierarchy and the current filter context.

---

## Dashboard Personalization

### Saving Custom Views

Allow users to save the current state of filters, time range, layout, and visible widgets as a named view. Distinguish between personal views (visible only to the creator) and shared views (visible to the team or organization). Provide a view selector dropdown in the dashboard header.

### Custom Dashboards

In advanced enterprise products, allow users to compose dashboards from a widget catalog. Provide a drag-and-drop dashboard builder with a grid-snapping system. Offer a library of pre-built templates that users can clone and customize. Enforce guardrails: define minimum card sizes, maximum cards per dashboard, and required default views that administrators configure.

### Widget Rearrangement

Support drag-and-drop reordering of dashboard cards. Snap cards to the grid and reflow surrounding cards automatically. Provide resize handles at card edges and corners. Enter an explicit "edit mode" to prevent accidental rearrangement during daily use. Auto-save layout changes or provide explicit save/discard controls.

---

## Responsive Dashboard Layouts

### Breakpoint Behavior

Enterprise dashboards must accommodate monitors from 1280px to 3840px and beyond. Define breakpoints:

- **Compact (1280-1439px).** Collapse sidebar to icon-only. Cards reflow to fewer columns (2-3 instead of 4). Charts reduce padding.
- **Standard (1440-1919px).** Full sidebar with labels. 3-4 column card grid. Comfortable chart sizing.
- **Wide (1920-2559px).** 4-6 column card grid. Charts can display more data points and longer labels.
- **Ultra-wide (2560px+).** Support multi-dashboard side-by-side or use the additional space for a persistent detail panel.

### Card Reflow Strategy

Define a stacking order for cards so that when the viewport narrows, cards reflow predictably. Tier 1 KPI cards remain at the top. Tier 2 diagnostic charts stack vertically in priority order. Tier 3 detail views may collapse into accordion sections or move behind a "Show more" action on narrow viewports.

### Mobile Adaptations

For dashboards accessed on tablets or phones, convert the multi-column grid to a single-column stack. Replace interactive charts with simplified metric cards and sparklines. Provide swipe gestures to navigate between dashboard sections. Prioritize Tier 1 metrics and hide Tier 2/3 behind expandable sections.

### Simplification at Small Sizes

- **Reduce data points**: Downsample a 365-day line chart to weekly or monthly at small breakpoints. Use LTTB (Largest Triangle Three Buckets) algorithm for perceptually faithful downsampling.
- **Remove gridlines**: At small sizes, gridlines create noise. Keep only the baseline and perhaps one reference line.
- **Rotate or truncate labels**: Below 600px, rotate x-axis labels to 45 degrees. Below 400px, show every other label or abbreviate (Jan, Feb, Mar).
- **Collapse legends**: Replace a color legend with direct labels on the lines or bars themselves. Below 400px, use a dropdown selector to toggle series visibility.
- **Touch targets**: Increase interactive target areas to at least 44x44px for touch. This may require spacing out bars or points.

### Data Reduction Techniques

- **Aggregation**: Roll up daily data to weekly or monthly. Group long-tail categories into "Other."
- **Filtering**: Show only the top N categories. Provide a control to adjust N.
- **Sampling**: For scatterplots with millions of points, use reservoir sampling to display a representative subset.
- **Level of detail**: At zoom-out, show county-level data. At zoom-in, show city-level. This mirrors semantic zoom.

---

## Embedded Analytics

### Embedding Dashboards in Other Applications

Support iframe-based embedding with configurable chrome (show/hide header, filters, navigation). Provide a JavaScript SDK for tighter integration: passing authentication tokens, synchronizing filters with the host application, listening for user interaction events.

**Security.** Enforce row-level security so that embedded dashboards respect the host application's user permissions. Use signed tokens or OAuth flows -- never pass credentials in query parameters. Implement content security policy (CSP) headers to control which domains may embed the dashboard.

**Theming.** Allow the embedded dashboard to inherit the host application's theme (colors, typography, border radius) so it appears native. Provide a theming API or CSS custom property passthrough.

**Interaction bridging.** When a user clicks a data point in an embedded chart, emit an event to the host application so it can respond (navigate to a record, open a drawer, apply a filter in its own UI).

---

## Print and Export

### PDF Generation

Provide a "Print / Export PDF" action that renders the current dashboard state (with active filters) to a paginated PDF. Use server-side rendering (headless browser or dedicated PDF engine) for high-fidelity output. Include a header with dashboard title, filter summary, and generation timestamp on every page. Optimize chart rendering for print: remove hover states, increase label sizes, convert interactive elements to static annotations.

### Email Scheduling

Allow users to schedule recurring dashboard snapshots delivered by email. Support daily, weekly, and monthly schedules. Include a PDF attachment and an inline summary of Tier 1 KPIs in the email body. Allow recipients to be configured per schedule. Include an "Open live dashboard" link in every email.

### CSV and Excel Export

Provide per-card export of the underlying data in CSV or Excel format. Include column headers, applied filters as metadata, and a generation timestamp. For charts, export the data series as tabular rows. For Excel, use named sheets and basic formatting (headers bolded, numbers formatted). Respect row-level security in exports -- never export data the user cannot see on screen.

---

## Dashboard Performance Optimization

### Data Pagination and Aggregation

Pre-aggregate data at the backend for common time grains (hourly, daily, weekly, monthly). Serve pre-aggregated results for initial dashboard load; fetch granular data only on drill-down. Implement cursor-based pagination for data tables embedded within dashboards. Cache frequently accessed aggregations with TTL-based invalidation.

### Lazy Chart Rendering

Render only the charts visible in the current viewport. Use Intersection Observer to detect when a card scrolls into view and trigger data fetch and chart render at that moment. Provide skeleton placeholders for off-screen cards. This is especially critical for dashboards with 20+ cards where rendering everything upfront would block the main thread for seconds.

### Caching Strategies

Implement a multi-layer cache:

- **Browser cache.** Cache static assets (chart libraries, fonts, icons) aggressively with immutable hashes.
- **Application cache.** Store the last successful query response in localStorage or IndexedDB. Display cached data immediately while fetching fresh data in the background (stale-while-revalidate pattern).
- **CDN cache.** For dashboards with organization-wide data (not user-specific), serve query results from a CDN with short TTLs (1-5 minutes).
- **Server-side cache.** Use Redis or Memcached to cache expensive query results. Implement cache key strategies that account for filter combinations. Set cache warming jobs for the most-viewed dashboards to precompute results before business hours.

- **Bundle size.** Recharts/D3 are large. Code-split chart libraries. Load only the chart types used.
- **Memoization.** Memoize chart components to prevent re-renders when parent state changes.

---

## Executive vs. Operational vs. Analytical Dashboard Design

### Executive Dashboards

**Audience:** C-suite, VP-level, board members. Infrequent, high-stakes viewing.

**Design principles:**

- Minimize to 5-7 Tier 1 KPIs. Remove all Tier 3 detail.
- Every metric tells a story: "Revenue is up 12% vs. target, driven by EMEA growth."
- Use large typography, generous whitespace, and minimal chart complexity.
- Provide natural language summaries or AI-generated insight callouts ("This is the highest monthly revenue since October 2024").
- Avoid requiring interaction. The story should be clear within 10 seconds of viewing.
- Design for presentation on large screens in boardrooms and for PDF consumption.

### Operational Dashboards

**Audience:** Team leads, shift managers, operations staff. Continuous, real-time monitoring.

**Design principles:**

- Optimize for glanceability. Use traffic-light color coding, large status indicators, and anomaly highlighting.
- Auto-refresh at 5-30 second intervals with clear freshness indicators.
- Display the last N events or alerts in a scrolling feed or timeline.
- Support audio or desktop notification alerts for critical thresholds.
- Design for persistent display on wall-mounted monitors: high contrast, large text, no screensaver, no session timeout.
- Minimize navigation -- everything relevant should be on a single screen or a 2-3 tab rotation.

### Analytical Dashboards

**Audience:** Analysts, data scientists, business intelligence teams. Deep, investigative interaction.

**Design principles:**

- Maximize interactivity: cross-filtering, drill-down, brushing, zooming, panning.
- Support custom date ranges, dynamic segmentation, and ad-hoc groupings.
- Display confidence intervals, sample sizes, and statistical annotations.
- Allow chart type switching (view data as bar chart, table, or pivot table).
- Provide export to notebook (Jupyter, R Markdown) or direct SQL access for further analysis.
- Support saving and sharing analysis configurations as named explorations.
- Accept higher visual density and smaller text -- this audience tolerates complexity.

---

## Anti-Pattern: Misleading Aggregation

Showing only averages hides distribution. A bar chart showing "average response time: 200ms" conceals the fact that 95th percentile is 2,000ms. Always consider what summary statistic serves the analytical question. Show distributions (histograms, box plots) when the spread matters. Show confidence intervals or error bars when uncertainty matters. Annotate with sample sizes when magnitudes differ.

---

## Advanced Table Behavior

### Structural Patterns

Data tables are the backbone of enterprise desktop applications. Move beyond simple flat tables to support the structural and interactive complexity that professional users demand.

**Expandable rows.** Allow rows to expand in-place to reveal nested detail: sub-items, metadata, related records, or inline charts. Indicate expandability with a chevron icon in the first column. Expand a single row at a time to prevent vertical sprawl, or allow multiple expansions depending on use case. Animate the expansion with a brief slide-down (150-200ms) so users perceive spatial continuity. Indent the expanded content and apply a subtle background tint to visually associate it with the parent row.

**Grouped rows.** Group rows by a shared dimension (status, category, date, assignee) with a sticky group header that persists while scrolling through that group. Display an aggregate summary in the group header: count, sum, average. Allow collapsing an entire group to a single summary row. Support re-grouping by different columns through a "Group by" dropdown or drag-and-drop column headers into a grouping zone.

**Tree tables.** For hierarchical data (org charts, file systems, bill of materials), render rows as an expandable tree with indentation levels. Display expand/collapse toggles at each node. Use `role="treegrid"` and support keyboard navigation: Right Arrow expands a node, Left Arrow collapses it, Down Arrow moves to the next visible row. Maintain expansion state across data refreshes and pagination events.

**Frozen columns.** Freeze the first 1-3 identifier columns (name, ID, status) so they remain visible during horizontal scrolling. Apply a subtle shadow or border on the right edge of the frozen zone to indicate the scroll boundary. Allow users to configure which columns freeze. Frozen columns must remain vertically synchronized with the scrollable region -- scroll jank between frozen and scrollable zones is a critical usability defect.

**Virtual scrolling.** For tables with thousands or tens of thousands of rows, implement virtual scrolling (windowed rendering) that only renders the rows visible in the viewport plus a small buffer above and below. Recycle DOM nodes as the user scrolls. Maintain a consistent scrollbar thumb size that accurately reflects total row count. Libraries such as react-window, react-virtualized, or AG Grid provide production-grade implementations.

---

### Inline Editing Patterns

#### Cell Editing

Transform a cell into an editable state on double-click or Enter keypress when the cell has focus. Display an input control appropriate to the data type: text input for strings, number input with stepper for numerics, date picker for dates, dropdown for enumerated values, checkbox for booleans. Highlight the active cell with a prominent border (2px, primary color). Commit the edit on Enter, Tab (which advances to the next cell), or blur. Cancel on Escape, restoring the original value.

Validate immediately on commit. Display inline validation errors as a red border and tooltip on the cell. For server-side validation, show a brief loading indicator within the cell during the round-trip, then confirm with a subtle green flash or display the error.

#### Row Editing

Enter row-level edit mode on an explicit "Edit" action (row action button or keyboard shortcut). Transform all editable cells in the row simultaneously. Display Save and Cancel buttons at the end of the row or in a floating toolbar. Highlight the entire row with a distinct background to signal edit mode. Prevent navigation away from the row with unsaved changes -- display a confirmation dialog or auto-save.

#### Bulk Editing

Allow users to select multiple rows and apply a single value change to a shared field across all selected rows. Open a modal or inline panel listing the affected rows and the field to change. Display a preview of the change: "Set status to 'Approved' for 47 selected items." Require explicit confirmation for bulk edits. Provide undo capability immediately after the bulk operation completes.

#### Validation in Tables

Display validation errors at three levels:

1. **Cell level.** Red border and inline tooltip for the specific field.
2. **Row level.** Error icon in the row status column linking to a summary of all errors in that row.
3. **Table level.** A banner above the table: "3 rows have validation errors. Fix errors before saving." with links to jump to each error row.

Prevent submission of the table or form while validation errors exist. For server-side validation failures returned after a batch save, highlight the specific rows and cells that failed and preserve the user's input.

---

### Data Grid vs. Data Table

#### When to Use Spreadsheet-Style Grids

A data grid is a spreadsheet-like component that supports cell-level editing, formulas, copy-paste, fill-down, and free-form data entry. A data table is a structured list of records with column-based operations.

**Use a data grid when:**

- Users need to enter or edit data across many cells rapidly, resembling spreadsheet workflows (financial modeling, inventory management, scheduling).
- The mental model is a matrix of values rather than a list of entities.
- Copy-paste from external spreadsheets is a core workflow.
- Users expect cell range selection (click-drag across cells), fill handles, and keyboard-driven rapid entry (Tab to advance, Enter to move down).

**Use a data table when:**

- Each row represents a distinct entity (user, order, ticket, device).
- Operations are row-level: view detail, edit record, delete, change status.
- Data arrives from an API as a collection of objects.
- Sorting, filtering, pagination, and search are the primary interactions.
- Rows have action buttons, links, or navigation targets.

**Hybrid patterns.** Some enterprise applications use a data table with inline editable cells that selectively activate grid-like behaviors. This hybrid is common in ERP and CRM systems where records are entities but rapid multi-cell editing is needed for certain workflows (pricing updates, batch status changes).

---

## Sources

- Few, S. (2006). *Information Dashboard Design: The Effective Visual Communication of Data.* Analytics Press.
- Few, S. (2012). *Show Me the Numbers: Designing Tables and Graphs to Enlighten.* Analytics Press.
- Shneiderman, B. (1996). "The Eyes Have It: A Task by Data Type Taxonomy for Information Visualizations."
