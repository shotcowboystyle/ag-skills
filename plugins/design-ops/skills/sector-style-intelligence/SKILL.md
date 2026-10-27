---
name: sector-style-intelligence
description: "Visual direction by industry for 20+ sectors: color psychology, typography norms, component conventions, spacing philosophy, motion personality, trust signals, and sector anti-patterns. Use when a design must read as credible for fintech, healthcare, SaaS, e-commerce, or education."
allowed-tools: Read, Grep, Glob
---

# Sector Style Intelligence — Visual Direction by Industry

## Purpose

Every sector conditions users to read certain visual choices as credible. Fintech earns trust with precision typography, muted palettes and clinical spacing; wellness expects warmth and breathing room; dashboards are dense, editorial layouts are generous. Motion carries meaning too: precise and instant for a payment confirmation, slow and calming for meditation.

Know the baseline before you break it. Stripe borrowed editorial elegance from publishing and Duolingo imported gaming mechanics, and both worked because the departure was deliberate. Use this skill to get the sector baseline, then choose any deviation on purpose.

## Sector Coverage

| Sector | Style Archetype | Key Reference Apps |
| --- | --- | --- |
| **Fintech & Banking** | Precision trust, clean data density | Stripe, Cash App, Robinhood, Wise, Revolut, Mercury |
| **Healthcare (Clinical)** | Accessible precision, HIPAA-conscious | One Medical, Epic MyChart, Zocdoc, Teladoc |
| **Wellness & Fitness** | Warm organic, breathing space | Headspace, Calm, Peloton, MyFitnessPal, Apple Health |
| **Social Media** | Content-first, viral loops, dark mode | TikTok, Threads, Discord, BeReal, Mastodon |
| **Creator Tools** | Canvas-centric, minimal chrome | Notion, Figma, Arc, Framer, Obsidian |
| **SaaS & Productivity** | Keyboard-first, information density | Linear, Superhuman, Slack, Raycast, Cron |
| **Enterprise SaaS** | Professional calm, role-based density | Salesforce, Workday, ServiceNow, Datadog |
| **E-Commerce** | High-quality imagery, conversion-optimized | Shopify, Nike SNKRS, StockX, Etsy, SSENSE |
| **Marketplace** | Trust badges, two-sided design | Airbnb, DoorDash, Uber, TaskRabbit |
| **Education** | Gamification, progress, celebration | Duolingo, Khan Academy, Coursera, Brilliant |
| **Entertainment & Media** | Immersive, content-forward, minimal UI | Spotify, Netflix, Apple TV+, YouTube Music |
| **Gaming** | High contrast, achievement systems | Roblox, Steam, Xbox, PlayStation |
| **Travel & Hospitality** | Aspirational imagery, date-driven flows | Airbnb, Booking.com, Hopper, Google Travel |
| **Real Estate** | Map-first, listing cards, filter-heavy | Zillow, Redfin, Trulia, Compass |
| **Food & Beverage** | Appetite appeal, quick ordering flows | DoorDash, Uber Eats, Starbucks, Sweetgreen |
| **Automotive** | Configurator UX, premium materials | Tesla, Rivian, BMW, Porsche |
| **Legal & Compliance** | Document-centric, formal hierarchy | Clio, LegalZoom, DocuSign |
| **Developer Tools** | Terminal aesthetic, code-first, monospace | GitHub, Vercel, Railway, Supabase |
| **AI & ML Products** | Conversational UI, generative patterns | ChatGPT, Claude, Midjourney, Runway |
| **Luxury & Fashion** | Editorial, serif typography, negative space | SSENSE, Mr Porter, Net-a-Porter, Hermes |
| **Non-Profit & Civic** | Accessible, mission-forward, warm | charity: water, ACLU, Code.org |

## Reference Architecture

| File | Sectors Covered |
| --- | --- |
| `references/fintech-banking-style.md` | Fintech, Banking, Payments, Crypto |
| `references/health-wellness-style.md` | Healthcare (Clinical), Wellness, Fitness |
| `references/creator-social-style.md` | Social Media, Creator Tools, Community |
| `references/saas-productivity-style.md` | SaaS, Productivity, Developer Tools |
| `references/ecommerce-marketplace-style.md` | E-Commerce, Marketplace, Luxury |
| `references/education-entertainment-style.md` | Education, Entertainment, Gaming |

### Page Template Reference Files

Complete page-level templates with block sequences, typography maps, color application, spacing rhythm, component selection, responsive behavior, and React/TSX skeletons:

| File | Pages Covered |
| --- | --- |
| `references/saas-page-templates.md` | 10 SaaS pages (landing, pricing, onboarding, dashboard, settings, team, billing, integrations, changelog, docs) with 3 style variants each (Minimal/Warm/Bold) |
| `references/fintech-page-templates.md` | 10 Fintech pages (dashboard, transactions, transfer, portfolio, card, bills, loan, budget, insights, KYC) with 2 style variants (Clean Modern/Bold Fintech) + compliance and security patterns |
| `references/ecommerce-page-templates.md` | 10 E-Commerce pages (listing, detail, cart, checkout, confirmation, tracking, account, wishlist, returns, reviews) with 2 style variants (Premium/Marketplace) + conversion optimization |
| `references/healthcare-education-templates.md` | 5 Healthcare pages (portal, booking, records, telemedicine, medications) + 5 Education pages (catalog, detail, dashboard, lesson, quiz) with accessibility and engagement patterns |
| `references/creative-developer-templates.md` | 5 Creative/Portfolio pages (landing, case study, about, contact, blog) + 5 Developer pages (docs, API reference, CLI landing, changelog, status) |

### Each Style Reference File Includes

Color psychology (palettes with hex values), typography norms, component conventions (radius, elevation, density, in px), spacing philosophy, motion personality (timing, easing), trust signals, sector anti-patterns, 6+ reference apps with lessons, a W3C design token starter kit (JSON), and Mobbin/Screenlane inspiration filters.

## Cross-References

- **visual-design-mastery** — For foundational color theory, typography scales, and spacing systems that underpin all sector-specific guidance
- **design-systems-architecture** — For token architecture and multi-brand/multi-sector design system strategies
- **interaction-motion-design** — For detailed motion design principles that sector-specific motion personalities build upon
- **desktop-app-design** — For desktop-specific patterns in SaaS, productivity, and enterprise sectors
- **component-patterns-code** — For implementation-ready component code (React, SwiftUI, CSS) that can be styled with sector tokens
- **accessibility-inclusive-design** — For WCAG compliance requirements that apply across all sectors but have heightened importance in healthcare, education, and civic tech
- **cognitive-psychology-ux** — For the psychological principles behind sector-specific trust signals and engagement patterns
- **cross-cultural-i18n-ux** — For adapting sector styles across cultural contexts and markets

## How to Use This Skill

### With the `/style` Command

```
/style fintech — Get complete style direction for a fintech app
/style healthcare clinical — Get clinical healthcare style direction
/style e-commerce luxury — Get luxury e-commerce style direction
```

### With the `/benchmark` Command

```
/benchmark my-app against stripe — Compare your app's visual language against Stripe
/benchmark my-app fintech — Compare against the fintech sector baseline
```

### Direct Reference

Read the sector's style file, then its page-template file if you are building a specific page. Apply the conventions, or deviate from them deliberately based on the product's positioning.
