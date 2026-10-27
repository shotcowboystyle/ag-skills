# CSS Styling Approaches Reference

How to choose and apply a styling approach for a component library. CVA +
Tailwind + `cn()` (tailwind-merge) are covered with full components in
`react-component-cookbook.md`; native CSS features (container queries, `:has()`,
`@layer`) are in `css-modern-patterns.md`.

## Choosing an Approach

| Solution              | Approach               | Best For                          |
| --------------------- | ---------------------- | --------------------------------- |
| **Tailwind CSS**      | Utility classes        | Rapid prototyping, design systems |
| **CSS Modules**       | Scoped CSS files       | Existing CSS, gradual adoption    |
| **styled-components** | Template literals      | React, dynamic styling            |
| **Emotion**           | Object/template styles | Flexible, SSR-friendly            |
| **Vanilla Extract**   | Zero-runtime           | Performance-critical apps         |

Runtime CSS-in-JS (styled-components, Emotion) needs a client runtime and does
not work in React Server Components; styled-components is in maintenance mode.
Prefer a zero-runtime option (CSS Modules, Tailwind, Vanilla Extract) for new
React Server Components / App Router code.

## Comparison Matrix

| Approach          | Runtime | Bundle Size    | Learning Curve | Dynamic Styles | SSR   |
| ----------------- | ------- | -------------- | -------------- | -------------- | ----- |
| CSS Modules       | None    | Minimal        | Low            | Limited        | Yes   |
| Tailwind          | None    | Small (purged) | Medium         | Via classes    | Yes   |
| styled-components | Yes     | Medium         | Medium         | Full           | Yes\* |
| Emotion           | Yes     | Medium         | Medium         | Full           | Yes   |
| Vanilla Extract   | None    | Minimal        | High           | Limited        | Yes   |

## CSS Modules

Scoped CSS with zero runtime overhead.

### Setup

```tsx
// Button.module.css
.button {
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  font-weight: 500;
  transition: background-color 0.2s;
}

.primary {
  background-color: #2563eb;
  color: white;
}

.primary:hover {
  background-color: #1d4ed8;
}

.secondary {
  background-color: #f3f4f6;
  color: #1f2937;
}

.secondary:hover {
  background-color: #e5e7eb;
}

.small {
  padding: 0.25rem 0.5rem;
  font-size: 0.875rem;
}

.large {
  padding: 0.75rem 1.5rem;
  font-size: 1.125rem;
}
```

```tsx
// Button.tsx
import styles from "./Button.module.css";
import { clsx } from "clsx";

interface ButtonProps {
  variant?: "primary" | "secondary";
  size?: "small" | "medium" | "large";
  children: React.ReactNode;
  onClick?: () => void;
}

export function Button({
  variant = "primary",
  size = "medium",
  children,
  onClick,
}: ButtonProps) {
  return (
    <button
      className={clsx(
        styles.button,
        styles[variant],
        size !== "medium" && styles[size],
      )}
      onClick={onClick}
    >
      {children}
    </button>
  );
}
```

### Composition

```css
/* base.module.css */
.visuallyHidden {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  border: 0;
}

/* Button.module.css */
.srOnly {
  composes: visuallyHidden from "./base.module.css";
}
```

## Tailwind CSS

Utility-first CSS with design system constraints. For CVA variants and the
`cn()` merge helper, see `react-component-cookbook.md` (Shared Utility and
Button sections).

### Custom Plugin

Tailwind v3 config shown. In Tailwind v4, define simple utilities in CSS with
`@utility`, and load a JS plugin like this one with `@plugin "./plugin.js";`.

```js
// tailwind.config.js
const plugin = require("tailwindcss/plugin");

module.exports = {
  plugins: [
    plugin(function ({ addUtilities, addComponents, theme }) {
      // Add utilities
      addUtilities({
        ".text-balance": {
          "text-wrap": "balance",
        },
        ".scrollbar-hide": {
          "-ms-overflow-style": "none",
          "scrollbar-width": "none",
          "&::-webkit-scrollbar": {
            display: "none",
          },
        },
      });

      // Add components
      addComponents({
        ".card": {
          backgroundColor: theme("colors.white"),
          borderRadius: theme("borderRadius.lg"),
          padding: theme("spacing.6"),
          boxShadow: theme("boxShadow.md"),
        },
      });
    }),
  ],
};
```

## styled-components

CSS-in-JS with template literals.

```tsx
import styled, { css, keyframes } from "styled-components";

// Keyframes
const fadeIn = keyframes`
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
`;

// Base button with variants
interface ButtonProps {
  $variant?: "primary" | "secondary" | "ghost";
  $size?: "sm" | "md" | "lg";
  $isLoading?: boolean;
}

const sizeStyles = {
  sm: css`
    padding: 0.25rem 0.75rem;
    font-size: 0.875rem;
  `,
  md: css`
    padding: 0.5rem 1rem;
    font-size: 1rem;
  `,
  lg: css`
    padding: 0.75rem 1.5rem;
    font-size: 1.125rem;
  `,
};

const variantStyles = {
  primary: css`
    background-color: ${({ theme }) => theme.colors.primary};
    color: white;
    &:hover:not(:disabled) {
      background-color: ${({ theme }) => theme.colors.primaryHover};
    }
  `,
  secondary: css`
    background-color: ${({ theme }) => theme.colors.secondary};
    color: ${({ theme }) => theme.colors.text};
    &:hover:not(:disabled) {
      background-color: ${({ theme }) => theme.colors.secondaryHover};
    }
  `,
  ghost: css`
    background-color: transparent;
    color: ${({ theme }) => theme.colors.text};
    &:hover:not(:disabled) {
      background-color: ${({ theme }) => theme.colors.ghost};
    }
  `,
};

const Button = styled.button<ButtonProps>`
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border: none;
  border-radius: 0.375rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  animation: ${fadeIn} 0.3s ease;

  ${({ $size = "md" }) => sizeStyles[$size]}
  ${({ $variant = "primary" }) => variantStyles[$variant]}

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  ${({ $isLoading }) =>
    $isLoading &&
    css`
      pointer-events: none;
      opacity: 0.7;
    `}
`;

// Extending components
const IconButton = styled(Button)`
  padding: 0.5rem;
  aspect-ratio: 1;
`;

// Theme provider
const theme = {
  colors: {
    primary: "#2563eb",
    primaryHover: "#1d4ed8",
    secondary: "#f3f4f6",
    secondaryHover: "#e5e7eb",
    ghost: "rgba(0, 0, 0, 0.05)",
    text: "#1f2937",
  },
};

// Usage
<ThemeProvider theme={theme}>
  <Button $variant="primary" $size="lg">
    Click me
  </Button>
</ThemeProvider>;
```

## Emotion

Flexible CSS-in-JS with object and template syntax.

```tsx
/** @jsxImportSource @emotion/react */
import { css, Theme, ThemeProvider, useTheme } from "@emotion/react";
import styled from "@emotion/styled";

// Theme typing
declare module "@emotion/react" {
  export interface Theme {
    colors: {
      primary: string;
      background: string;
      text: string;
    };
    spacing: (factor: number) => string;
  }
}

const theme: Theme = {
  colors: {
    primary: "#2563eb",
    background: "#ffffff",
    text: "#1f2937",
  },
  spacing: (factor: number) => `${factor * 0.25}rem`,
};

// Object syntax
const cardStyles = (theme: Theme) =>
  css({
    backgroundColor: theme.colors.background,
    padding: theme.spacing(4),
    borderRadius: "0.5rem",
    boxShadow: "0 1px 3px rgba(0, 0, 0, 0.1)",
  });

// Template literal syntax
const buttonStyles = css`
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  font-weight: 500;

  &:hover {
    opacity: 0.9;
  }
`;

// Styled component with theme
const Card = styled.div`
  background-color: ${({ theme }) => theme.colors.background};
  padding: ${({ theme }) => theme.spacing(4)};
  border-radius: 0.5rem;
`;

// Component with css prop
function Alert({ children }: { children: React.ReactNode }) {
  const theme = useTheme();

  return (
    <div
      css={css`
        padding: ${theme.spacing(3)};
        background-color: ${theme.colors.primary}10;
        border-left: 4px solid ${theme.colors.primary};
      `}
    >
      {children}
    </div>
  );
}

// Usage
<ThemeProvider theme={theme}>
  <Card>
    <Alert>Important message</Alert>
  </Card>
</ThemeProvider>;
```

## Vanilla Extract

Zero-runtime CSS-in-JS with full type safety.

```tsx
// styles.css.ts
import { style, styleVariants, createTheme } from "@vanilla-extract/css";
import { recipe, type RecipeVariants } from "@vanilla-extract/recipes";

// Theme contract
export const [themeClass, vars] = createTheme({
  color: {
    primary: "#2563eb",
    secondary: "#64748b",
    background: "#ffffff",
    text: "#1f2937",
  },
  space: {
    small: "0.5rem",
    medium: "1rem",
    large: "1.5rem",
  },
  radius: {
    small: "0.25rem",
    medium: "0.375rem",
    large: "0.5rem",
  },
});

// Simple style
export const container = style({
  padding: vars.space.medium,
  backgroundColor: vars.color.background,
});

// Style variants
export const text = styleVariants({
  primary: { color: vars.color.text },
  secondary: { color: vars.color.secondary },
  accent: { color: vars.color.primary },
});

// Recipe (like CVA)
export const button = recipe({
  base: {
    display: "inline-flex",
    alignItems: "center",
    justifyContent: "center",
    fontWeight: 500,
    borderRadius: vars.radius.medium,
    transition: "background-color 0.2s",
    cursor: "pointer",
    border: "none",
    ":disabled": {
      opacity: 0.5,
      cursor: "not-allowed",
    },
  },
  variants: {
    variant: {
      primary: {
        backgroundColor: vars.color.primary,
        color: "white",
        ":hover": {
          backgroundColor: "#1d4ed8",
        },
      },
      secondary: {
        backgroundColor: "#f3f4f6",
        color: vars.color.text,
        ":hover": {
          backgroundColor: "#e5e7eb",
        },
      },
    },
    size: {
      small: {
        padding: "0.25rem 0.75rem",
        fontSize: "0.875rem",
      },
      medium: {
        padding: "0.5rem 1rem",
        fontSize: "1rem",
      },
      large: {
        padding: "0.75rem 1.5rem",
        fontSize: "1.125rem",
      },
    },
  },
  defaultVariants: {
    variant: "primary",
    size: "medium",
  },
});

export type ButtonVariants = RecipeVariants<typeof button>;
```

```tsx
// Button.tsx
import { button, type ButtonVariants, themeClass } from "./styles.css";

interface ButtonProps extends ButtonVariants {
  children: React.ReactNode;
  onClick?: () => void;
}

export function Button({ variant, size, children, onClick }: ButtonProps) {
  return (
    <button className={button({ variant, size })} onClick={onClick}>
      {children}
    </button>
  );
}

// App.tsx - wrap with theme
function App() {
  return (
    <div className={themeClass}>
      <Button variant="primary" size="large">
        Click me
      </Button>
    </div>
  );
}
```

## Performance Considerations

### Critical CSS Extraction

```tsx
// Next.js with styled-components
// pages/_document.tsx
import Document, { DocumentContext } from "next/document";
import { ServerStyleSheet } from "styled-components";

export default class MyDocument extends Document {
  static async getInitialProps(ctx: DocumentContext) {
    const sheet = new ServerStyleSheet();
    const originalRenderPage = ctx.renderPage;

    try {
      ctx.renderPage = () =>
        originalRenderPage({
          enhanceApp: (App) => (props) =>
            sheet.collectStyles(<App {...props} />),
        });

      const initialProps = await Document.getInitialProps(ctx);
      return {
        ...initialProps,
        styles: [initialProps.styles, sheet.getStyleElement()],
      };
    } finally {
      sheet.seal();
    }
  }
}
```

### Code Splitting Styles

```tsx
// Dynamically import heavy styled components
import dynamic from "next/dynamic";

const HeavyChart = dynamic(() => import("./HeavyChart"), {
  loading: () => <Skeleton height={400} />,
  ssr: false,
});
```
