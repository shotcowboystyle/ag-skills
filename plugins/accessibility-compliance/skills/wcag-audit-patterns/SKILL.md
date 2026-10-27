---
name: wcag-audit-patterns
description: Conduct WCAG 2.2 accessibility audits with automated testing, manual verification, and remediation guidance. Use when auditing websites for accessibility, fixing WCAG violations, or implementing accessible design patterns.
last_verified: 2026-10-27
---

# WCAG Audit Patterns

Comprehensive guide to auditing web content against WCAG 2.2 guidelines with actionable remediation strategies.

## When to Use This Skill

- Conducting accessibility audits
- Fixing WCAG violations
- Implementing accessible components
- Preparing for accessibility lawsuits
- Meeting ADA/Section 508 requirements
- Achieving VPAT compliance

## Core Concepts

### 1. WCAG Conformance Levels

| Level   | Description            | Required For      |
| ------- | ---------------------- | ----------------- |
| **A**   | Minimum accessibility  | Legal baseline    |
| **AA**  | Standard conformance   | Most regulations  |
| **AAA** | Enhanced accessibility | Specialized needs |

### 2. POUR Principles

```
Perceivable:  Can users perceive the content?
Operable:     Can users operate the interface?
Understandable: Can users understand the content?
Robust:       Does it work with assistive tech?
```

### 3. Common Violations by Impact

```
Critical (Blockers):
├── Missing alt text for functional images
├── No keyboard access to interactive elements
├── Missing form labels
└── Auto-playing media without controls

Serious:
├── Insufficient color contrast
├── Missing skip links
├── Inaccessible custom widgets
└── Missing page titles

Moderate:
├── Missing language attribute
├── Unclear link text
├── Missing landmarks
└── Improper heading hierarchy
```

### 4. What WCAG 2.2 Changed

WCAG 2.2 (W3C Recommendation, October 2023) adds nine success criteria and removes 4.1.1 Parsing. Audit every one explicitly; automated tools catch little of this list.

| SC     | Name                                 | Level | Audit check                                                                        |
| ------ | ------------------------------------ | ----- | ---------------------------------------------------------------------------------- |
| 2.4.11 | Focus Not Obscured (Minimum)         | AA    | Focused element never fully hidden by sticky headers, banners or chat widgets      |
| 2.4.12 | Focus Not Obscured (Enhanced)        | AAA   | No part of the focused element is hidden                                           |
| 2.4.13 | Focus Appearance                     | AAA   | Focus indicator ≥ 2 CSS px perimeter area with 3:1 change in contrast              |
| 2.5.7  | Dragging Movements                   | AA    | Every drag (sliders, reorder, maps) has a single-pointer alternative               |
| 2.5.8  | Target Size (Minimum)                | AA    | Pointer targets ≥ 24×24 CSS px, or spaced so a 24 px circle doesn't overlap        |
| 3.2.6  | Consistent Help                      | A     | Help/contact mechanisms appear in the same relative order across pages             |
| 3.3.7  | Redundant Entry                      | A     | Data already entered in the same process is auto-filled or selectable              |
| 3.3.8  | Accessible Authentication (Minimum)  | AA    | No cognitive test to log in unless paste, password managers or an alternative work |
| 3.3.9  | Accessible Authentication (Enhanced) | AAA   | As 3.3.8, with no object- or personal-content-recognition exception                |
| 4.1.1  | Parsing                              | —     | Removed; duplicate IDs only fail when they break 1.3.1 or 4.1.2                    |

Worked checks and code for each are in `references/details.md` under "WCAG 2.2 Additions".

## Detailed patterns and worked examples

Detailed pattern documentation lives in `references/details.md`. Read that file when the navigation tier above is insufficient.

## Best Practices

### Do's

- **Start early** - Accessibility from design phase
- **Test with real users** - Disabled users provide best feedback
- **Automate what you can** - 30-50% issues detectable
- **Use semantic HTML** - Reduces ARIA needs
- **Document patterns** - Build accessible component library

### Don'ts

- **Don't rely only on automated testing** - Manual testing required
- **Don't use ARIA as first solution** - Native HTML first
- **Don't hide focus outlines** - Keyboard users need them
- **Don't disable zoom** - Users need to resize
- **Don't use color alone** - Multiple indicators needed
