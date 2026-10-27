# Component Library, Theming, and Design-to-Code

Component anatomy, the component maturity levels, API design principles, theme structure, multi-brand layering, and Figma-to-code synchronization. For full multi-brand token layering see `maturity-model-multi-brand.md`; for governance see `governance-scaling.md`.

## Component Library Architecture

### Component Anatomy

Every component has a defined structure:

```
Component
├── Props/API (inputs and configuration)
├── Variants (visual and behavioral variations)
├── States (default, hover, active, focused, disabled, loading, error)
├── Slots/Children (composition points for custom content)
├── Tokens (design token bindings)
├── Accessibility (ARIA, keyboard, screen reader behavior)
└── Documentation (usage guidelines, do/don't examples)
```

### Component Maturity Model

**Level 1 — Defined:** Designed in Figma, documented in guidelines
**Level 2 — Implemented:** Coded in component library, props API defined
**Level 3 — Tested:** Unit tests, visual regression tests, accessibility tests pass
**Level 4 — Documented:** Usage guidelines, API docs, examples, do/don't
**Level 5 — Governed:** Change process established, versioning, deprecation path

### Component API Design Principles

- **Predictable props naming:** Use consistent naming conventions across all components (`size`, `variant`, `disabled`, `className`)
- **Enum over boolean:** `variant="primary" | "secondary" | "ghost"` not `isPrimary`, `isSecondary`
- **Composition over configuration:** `<Card><CardHeader /><CardBody /></Card>` not `<Card header={} body={} />`
- **Sensible defaults:** Components work without props; customization is additive
- **Type safety:** Full TypeScript types for all props; no `any` types in public API
- **Forward refs:** All components forward refs for imperative access
- **Polymorphic rendering:** Support `as` prop for semantic HTML flexibility (`<Button as="a" href="..." />`)

## Theming Architecture

### Theme Structure

```json
{
  "theme": {
    "light": {
      "color.bg.primary": "#ffffff",
      "color.bg.secondary": "#f5f5f5",
      "color.text.primary": "#171717",
      "color.text.secondary": "#737373",
      "color.action.primary": "#3b82f6"
    },
    "dark": {
      "color.bg.primary": "#171717",
      "color.bg.secondary": "#262626",
      "color.text.primary": "#f5f5f5",
      "color.text.secondary": "#a3a3a3",
      "color.action.primary": "#60a5fa"
    }
  }
}
```

### Theming Implementation

- Use CSS custom properties (variables) as the runtime theming mechanism
- Apply theme by swapping custom property values at the root level
- Support system preference detection (`prefers-color-scheme`)
- Allow manual override with persistent user preference
- Component tokens reference semantic tokens, which resolve to theme-specific values

### Multi-Brand Architecture

For organizations with multiple brands sharing a system:

- **Shared foundation:** Common component behavior, interaction patterns, accessibility
- **Brand tokens:** Each brand provides its own token set (colors, typography, spacing variations)
- **Component override layer:** Brand-specific component customizations when tokens alone are insufficient
- **Theme matrix:** Brand x Mode (e.g., BrandA-Light, BrandA-Dark, BrandB-Light, BrandB-Dark)

## Design-to-Code Integration

### Figma-to-Code Synchronization

- Figma component naming must match code component naming exactly
- Figma variants map to code component props
- Design tokens sync bidirectionally: Figma to tokens.json to code
- Use Token Studio (Figma plugin) for token management in design
- Automate token export with CI/CD pipeline (Style Dictionary, Token Transformer)

### Code Generation

- Generate CSS/SCSS from design tokens using Style Dictionary
- Platform-specific output: CSS variables, iOS Swift constants, Android XML resources, React Native styles
- Generate TypeScript types from token schema
- Visual regression testing: compare Figma designs with rendered components
