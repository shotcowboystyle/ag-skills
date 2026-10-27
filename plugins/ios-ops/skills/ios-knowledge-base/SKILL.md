---
name: ios-knowledge-base
description: Source-checked Apple-platform reference library (iOS 26 / Xcode 26, checked August 2026) that the other ios-ops skills cite — SwiftUI, Liquid Glass, on-device AI, framework routes and deep dives, capability and code recipes, verification proof matrices, and official source registries. Use when an ios-ops skill links into it, or when you need the source-backed reference for an Apple framework, API, or proof requirement.
allowed-tools: Read, Grep, Glob
last_verified: 2026-08-19
---

# iOS knowledge base

Shared reference library for the ios-ops skills. Every document lives under
`references/` in this skill's directory. Other ios-ops skills link here with
`../ios-knowledge-base/references/<path>`; if your tool installs skills under
prefixed directory names, find this skill by name and resolve the same
`references/<path>` inside it.

## How to use it

1. Grep, don't browse. The tree has ~970 documents; search `references/` for the
   framework, symbol, or capability name and open only the matches.
2. Open `references/README.md` (a short index) when you need the layout or a
   starting document for a domain.
3. Before calling any claim current, open the matching file in
   `references/sources/` and re-check the official page. The corpus was
   source-checked against iOS 26 / Xcode 26 on 2026-08-19; newer SDKs may differ.

## Layout

| Directory | Contents |
|---|---|
| `00-foundations/` | Scope, mental model, SDK versioning, evidence vocabulary |
| `10-swiftui/` | State, layout, navigation, accessibility, interop |
| `20-liquid-glass/`, `21-design-deep-dives/` | Liquid Glass adoption and design recipes |
| `30-on-device-ai/`, `31-on-device-ai-recipes/`, `32-apple-intelligence-surfaces/` | Foundation Models, Core ML, Apple Intelligence surfaces |
| `40-framework-routes/` to `44-system-services/` | Framework routing and deep dives |
| `50-capability-recipes/`, `70-code-recipes/` | Capability and code recipes |
| `60-verification/` | Checklists and device-backed proof matrices |
| `90-templates/` | Briefs and target plans |
| `sources/` | Official source registry, one file per domain |

Keep the distinction the documents draw between *verified on a device* and
*only written down*.
