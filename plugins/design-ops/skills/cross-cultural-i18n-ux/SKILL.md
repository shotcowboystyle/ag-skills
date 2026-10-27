---
name: cross-cultural-i18n-ux
description: "Internationalization and localization: RTL layouts with CSS logical properties, CJK typography, text expansion, locale-aware formatting, cultural color semantics, and Hofstede's dimensions applied to interfaces. Use when shipping to new markets, adding Arabic or Hebrew support, or pseudo-localization testing."
allowed-tools: Read, Grep, Glob
---

# Cross-Cultural & Internationalization UX

Internationalization (i18n) is a structural design decision, not a post-design string-extraction phase: a fixed-width button or a red-only error state is already an i18n decision. Localization (l10n) adapts content, visuals, and workflows to a locale. Retrofitting either into a monolingual design is expensive rework.

## Core Rules

- **Layout:** use CSS logical properties (`margin-inline-start`, not `margin-left`) and flexible containers; no fixed-width or fixed-height text boxes.
- **RTL is not a blind mirror:** mirror navigation and directional icons (back/forward, undo/redo); do not mirror numbers, phone numbers, media playback controls, or universal icons (search, home, settings). Isolate embedded LTR text with `<bdi>`.
- **Text expansion:** German +30-35%, French +15-20%; design short strings (under 20 characters) for up to 200%. Run pseudo-localized builds in CI.
- **Formatting:** always use locale-aware formatters (JS `Intl`, Swift Foundation). Hardcoded date formats, separators, or currency symbols are bugs. Mind lakh/crore grouping, 10,000-based counting, imperial vs metric.
- **Names and addresses:** prefer one "Full name" field, or "Given name(s)" / "Family name(s)"; address formats vary by country.
- **Culture:** Hofstede dimensions are hypotheses to validate with cross-cultural testing, not stereotypes. Color and gestures carry different meanings by culture, so never let color be the sole carrier of meaning.

## Routing

- **Implementation** — global-design scope, CSS logical properties, RTL patterns and bidi text, react-intl vs i18next, iOS i18n, text expansion, multi-script fonts, locale-aware formatting code (dates, numbers, units, names, addresses), testing and automation: read `references/internationalization-patterns.md`.
- **Culture** — Hofstede's six dimensions mapped to UI, cross-cultural usability testing, case studies, payment diversity, trust signals, color and imagery semantics: read `references/cultural-ux-dimensions.md`.

## Cross-Referencing

- Mobile text expansion, RTL gestures, CJK input: `mobile-ux-design`
- `lang` attributes, bidi screen-reader output, non-color-only meaning: `accessibility-inclusive-design`
- Translation quality ethics, culture-exploiting dark patterns: `ux-ethics-content-strategy`
- Logical-property tokens, RTL icon variants, CJK line-height: `visual-design-mastery`
- Locale-aware component APIs, system-level RTL, string management: `design-systems-architecture`

## When to Invest in i18n

Not every product needs full internationalization from day one. The decision of when and how deeply to invest depends on the product's market strategy and growth trajectory. However, certain foundational decisions are nearly free at the start and extremely expensive to retrofit later.

**Always do from the start**, regardless of market plans: use CSS logical properties, use locale-aware formatters for dates and numbers, externalize all user-facing strings into translation-ready files, use flexible layout containers, and set the `lang` attribute on the HTML element.

**Do when entering a new script family**: RTL layout testing and remediation, multi-script font stack configuration, bidirectional text handling, and input method testing for the target script.

**Do when entering a culturally distinct market**: cultural usability research, payment method integration, trust signal adaptation, color and imagery audit, content tone review, and locale-specific formatting validation.

**Do when scaling to many markets simultaneously**: design system locale tokens, automated pseudo-localization testing in CI, translation management system integration, and cross-cultural analytics segmentation.

The key insight is that the foundational technical decisions (logical properties, formatters, string externalization) cost almost nothing when done from the start but can require weeks of refactoring when added later. Teams that treat these as defaults rather than i18n-specific features gain optionality at no meaningful cost.
