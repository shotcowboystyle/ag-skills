---
name: data-visualization-mastery
description: 50+ chart types with selection criteria, dashboard composition, data tables, KPI cards, sparklines, heatmaps, and accessible data presentation, with React code (Recharts, D3, Nivo) and data-viz tokens. Use when designing charts, dashboards, or any data-dense screen.
allowed-tools: Read, Grep, Glob
---

# Data Visualization Mastery

## Purpose

Encode data so people see patterns, outliers and trends faster than they could by reading numbers, and never mislead them. The skill applies Tufte, Few, Bertin/Cleveland-McGill and Munzner to charts, dashboards and data tables that are honest, readable and accessible.

## Core rules

- **Truthful encoding.** Keep the lie factor between 0.95 and 1.05. Start bar charts at 0. Avoid dual Y-axes, 3D, rainbow scales and decorative gradients.
- **Maximize data-ink (aim above 0.8).** Remove chartjunk: heavy gridlines (use opacity 0.1-0.15), redundant legends (label directly), borders, excess decimals. Use small multiples instead of crowded charts.
- **Use the most accurate channel for the most important dimension.** Position, then length, angle, area, saturation, hue. A bar chart beats a pie; use pies only for part-to-whole with 2-5 slices.
- **Choose the chart by purpose:** compare → bar/dot; trend → line/area/sparkline; part-to-whole → 100% stacked bar, treemap, donut (2-5); distribution → histogram/box/violin; relationship → scatter/bubble; flow → Sankey/funnel; geography → choropleth; hierarchy → treemap/sunburst. Match density to the audience: executives see 5-7 data points, analysts get interaction.
- **Color.** Sequential for ordered data, diverging around a meaningful midpoint, categorical capped at 8 (group the rest as "Other"). Never rely on red/green alone; add lightness, pattern or labels. Keep series colors the same across charts. Gray for context, saturated color for focus.
- **Numbers.** Use tabular figures (`font-variant-numeric: tabular-nums`) and right-align them. Abbreviate large values ($1.2M) and show deltas with sign, color and arrow.
- **This skill owns dashboards and data tables.** `desktop-app-design` covers desktop chrome (windows, menus, panels, shortcuts); `layout-block-intelligence` covers marketing page sections; `ui-pattern-intelligence` covers app blocks such as kanban, calendars and activity feeds.
- **Dashboards (Few).** Fit the primary view on one screen, put the most important information top-left, give every number context (target, previous period, benchmark), use 5-7 charts at most, summary first and detail on demand.
- **KPI cards.** One hero number, always with context, semantic delta color (an increase can be bad, e.g. churn), an optional sparkline, 3-5 per row.
- **Animate only data changes.** Data stays readable within 500ms and animations respect `prefers-reduced-motion`.
- **Every chart has loading, empty, error and partial-data states**, resizes rather than scales, has 44×44px touch targets, and has alt text stating the insight plus a data-table alternative.

## Routing

| Question | Read |
| --- | --- |
| Tufte/Bertin/Few/Munzner detail; selection by purpose, data shape and audience; palettes with hex values; type scale; grid and spacing; animation and interaction; KPI anatomy; density; anti-patterns; responsive behavior; dataviz tokens and dark mode; print CSS; the full review checklist | `references/dataviz-foundations.md` |
| Picking or specifying a particular chart (50+ types: when to use, data shape, max points, design specs) | `references/chart-type-encyclopedia.md` |
| Dashboard layouts: KPI rows, chart grids, filters, executive/operational/analytical, responsive collapse | `references/dashboard-layout-patterns.md` |
| Data tables: column types, sort, filter, pagination, selection, editing, density, accessibility, React code | `references/data-table-mastery.md` |
| Dashboard IA and metric tiers, card anatomy, page shells, interaction (zoom, brush, linked views, drill), real-time refresh and streaming, loading and stale data, alerts and thresholds, personalization, export, embedding, performance; advanced tables (grouped rows, tree tables, frozen columns, virtual scrolling, inline and bulk editing, grid vs. table) | `references/dashboards-and-tables.md` |
| Accessibility: alt-text patterns, colorblind-safe palettes, pattern fills, screen readers, keyboard, sonification | `references/dataviz-accessibility.md` |
| Recharts code: chart wrapper with states, tooltip, legend, responsive container, 20 chart types, KPI card, print | `references/dataviz-code-patterns.md` |

### Common requests

- **"I need a chart for this data":** ask for the analytical purpose and the data shape (dimensions, measures, cardinality), pick the chart from the encyclopedia, then give its design specs and code from `dataviz-code-patterns.md`.
- **"Design a dashboard":** identify the type (executive, operational, analytical), pick the layout from `dashboard-layout-patterns.md`, choose a chart per panel, and apply the KPI-card and responsive rules in `dataviz-foundations.md`.
- **"Make this chart accessible":** write alt text using the chart type's pattern, add a data table alternative, check the palette with a colorblind simulation, and add keyboard navigation if the chart is interactive.
- **"Build a data table":** decide column types, sorting and filtering, pick a responsive strategy, and use a native `<table>` with `aria-sort` on the sorted `<th>` (`role="grid"` only for an interactive grid with arrow-key cell navigation), using `data-table-mastery.md`; for grouping, trees, inline editing or spreadsheet-style entry, see `dashboards-and-tables.md`.

## Cross-References

- **`visual-design-mastery`** -- Color science (oklch, palette generation) applies directly to dataviz color palettes. Typography mastery (tabular figures, alignment) is critical for number-heavy UIs.
- **`ui-pattern-intelligence`** -- Dashboard and table patterns at the component level. This skill provides the deeper dataviz-specific design intelligence.
- **`accessibility-inclusive-design`** -- WCAG foundation. This skill extends it with dataviz-specific accessibility patterns.
- **`component-patterns-code`** -- Component architecture. This skill provides dataviz-specific component patterns and code.
- **`design-systems-architecture`** -- Token architecture. This skill defines dataviz-specific tokens (chart colors, gridlines, axes).
- **`performance-states-patterns`** -- Loading, error, and empty states apply to every chart and table component.
- **`cognitive-psychology-ux`** -- Perceptual principles (pre-attentive processing, Gestalt grouping) underpin all visual encoding decisions.
