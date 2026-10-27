---
name: desktop-app-design
description: "Desktop and enterprise application chrome: windows and multi-pane layouts, menus and context menus, toolbars, sidebars and panels, keyboard shortcuts and command palettes, drag and drop, master-detail, complex forms and wizards, and OS conventions. Use when designing an admin panel or professional desktop tool. For dashboards, charts and data tables, use data-visualization-mastery."
allowed-tools: Read, Grep, Glob
---

# Desktop App Design — Professional & Enterprise Excellence

## Desktop Design Philosophy

Desktop applications serve users who invest hours of focused attention in professional workflows. Unlike mobile's brief, task-focused interactions, desktop design must optimize for sustained productivity, information density, and expert efficiency. The challenge is supporting both first-day learnability and thousandth-day mastery within the same interface.

### Core Principles (Edward Tufte + Jony Ive)

1. **Information density with clarity** — show more data without increasing cognitive load (Tufte: "maximize data-ink ratio")
2. **Invisible design** — the interface should disappear, leaving only the work (Ive: "true simplicity is derived from so much more than just the absence of clutter")
3. **Keyboard-first, mouse-enhanced** — power users live on the keyboard; mouse interaction is the fallback
4. **Progressive complexity** — simple surface, deep capability accessible through exploration
5. **Spatial memory** — consistent layouts allow users to develop muscle memory over months of use

## Core Rules

- **Dashboards, charts and data tables** are owned by `data-visualization-mastery`; this skill covers the desktop chrome around them.
- **Workflows and forms:** visible progress, non-linear step navigation, save draft every step, review step before submit; auto-save with a quiet "Saved"; validation summary linking to fields.
- **Master-detail** is the default productivity layout: resizable split, arrow keys traverse, Enter opens, Escape returns.
- **Keyboard-first:** Cmd/Ctrl+K command palette, shortcut overlay (? or Ctrl+/), visible focus rings, Escape always cancels, platform-standard shortcuts, never override browser shortcuts.
- **Panels:** collapsible sidebar, right inspector, resizable bottom panel, detachable floating panels; persist layout, last view, and filters across sessions.
- **Menus and drag-drop:** context menus group actions (primary, transfer, modify, destructive last), show shortcuts, and open with Shift+F10 or the Menu key; every drag-and-drop action has a keyboard or menu alternative.
- **Enterprise:** hide what a role cannot use (tooltip-explain the disabled items that give context); audit trails on sensitive actions; toasts for confirmations, modals only for critical decisions; errors persist until addressed.

## Routing

| Question | Read |
|----------|------|
| Master-detail, complex forms, wizards, command palette, shortcut systems, multi-window and docking, drag and drop, context menus, tree views, split panes, notification center, bulk ops, infinite canvas, undo/redo, permission-aware enterprise UI | `references/desktop-interaction-patterns.md` |
| Dashboards, charts, KPI cards, data tables (sort, filter, density, inline editing, grid vs. table) | `data-visualization-mastery` skill |
| Industry conventions: healthcare, financial services, e-commerce, SaaS/B2B, education, real-time collaboration | `references/industry-vertical-patterns.md` |

## Cross-Referencing

- For design token systems, reference `design-systems-architecture`
- For interaction and transition design, reference `interaction-motion-design`
- For UX evaluation, reference `nng-ux-heuristics`
- For web/macOS/Windows visual standards, reference `platform-visual-standards`
- Production desktop components (data tables, command palette, resizable panels, tree views): `component-patterns-code`
- Figma variables, auto-layout, and design-to-code handoff: `figma-design-tool-workflows`

## Key Sources

- Tufte, E. (2001). "The Visual Display of Quantitative Information"
- Cooper, A. (2014). "About Face: The Essentials of Interaction Design"
- Microsoft Fluent Design System guidelines
- Apple macOS Human Interface Guidelines
- NNG Group enterprise UX research
