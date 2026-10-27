# monorepo-management — detailed patterns and worked examples

## pnpm Workspaces

### Setup

```yaml
# pnpm-workspace.yaml
packages:
  - "apps/*"
  - "packages/*"
  - "tools/*"

# One version per dependency, referenced as "catalog:" in package.json
catalog:
  react: ^19.3.0
  typescript: ^7.0.0

# pnpm settings live here (camelCase), not in .npmrc
autoInstallPeers: true
strictPeerDependencies: true
```

```json
// packages/ui/package.json (excerpt)
{
  "peerDependencies": { "react": "catalog:" },
  "devDependencies": { "typescript": "catalog:" }
}
```

Keep `.npmrc` for registry auth only, and keep tokens out of the repository.
Avoid `shamefullyHoist`: it hides phantom dependencies that pnpm's strict
`node_modules` layout exists to catch.

### Dependency Management

```bash
# Install dependency in specific package
pnpm add react --filter @repo/ui
pnpm add -D typescript --filter @repo/ui

# Install workspace dependency
pnpm add @repo/ui@workspace:* --filter web

# Install at the workspace root
pnpm add -Dw eslint

# Update all dependencies
pnpm update -r

# Remove dependency
pnpm remove react --filter @repo/ui
```

### Scripts

```bash
# Run script in specific package
pnpm --filter web dev
pnpm --filter @repo/ui build

# Run in all packages (topological order)
pnpm -r build
pnpm -r test

# Run in parallel
pnpm -r --parallel dev

# Filter by pattern
pnpm --filter "@repo/*" build
pnpm --filter "web..." build  # web and its dependencies
pnpm --filter "...web" build  # web and its dependents
```

## Nx and Turborepo

Task configuration, caching and affected runs are covered by the
`nx-workspace-patterns` and `turborepo-caching` skills. To add Nx to an
existing pnpm workspace, run `npx nx@latest init`.

## Shared Configurations

### TypeScript Configuration

```json
// packages/tsconfig/base.json
{
  "compilerOptions": {
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "module": "ESNext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "incremental": true,
    "declaration": true
  },
  "exclude": ["node_modules"]
}

// packages/tsconfig/react.json
{
  "extends": "./base.json",
  "compilerOptions": {
    "jsx": "react-jsx",
    "lib": ["ES2022", "DOM", "DOM.Iterable"]
  }
}

// apps/web/tsconfig.json
{
  "extends": "@repo/tsconfig/react.json",
  "compilerOptions": {
    "outDir": "dist",
    "rootDir": "src"
  },
  "include": ["src"],
  "exclude": ["node_modules", "dist"]
}
```

### ESLint Configuration

```javascript
// packages/eslint-config/index.js
import js from "@eslint/js";
import { defineConfig } from "eslint/config";
import tseslint from "typescript-eslint";
import reactHooks from "eslint-plugin-react-hooks";
import prettier from "eslint-config-prettier";

export default defineConfig([
  js.configs.recommended,
  tseslint.configs.recommended,
  reactHooks.configs.flat.recommended,
  prettier,
]);

// apps/web/eslint.config.js
import { defineConfig } from "eslint/config";
import base from "@repo/eslint-config";

export default defineConfig([
  base,
  {
    rules: {
      // App-specific rules
    },
  },
]);
```

## Code Sharing Patterns

### Pattern 1: Shared UI Components

```typescript
// packages/ui/src/button.tsx
import * as React from 'react';

export interface ButtonProps {
  variant?: 'primary' | 'secondary';
  children: React.ReactNode;
  onClick?: () => void;
}

export function Button({ variant = 'primary', children, onClick }: ButtonProps) {
  return (
    <button
      className={`btn btn-${variant}`}
      onClick={onClick}
    >
      {children}
    </button>
  );
}

// packages/ui/src/index.ts
export { Button, type ButtonProps } from './button';
export { Input, type InputProps } from './input';

// apps/web/src/app.tsx
import { Button } from '@repo/ui';

export function App() {
  return <Button variant="primary">Click me</Button>;
}
```

### Pattern 2: Shared Utilities

```typescript
// packages/utils/src/string.ts
export function capitalize(str: string): string {
  return str.charAt(0).toUpperCase() + str.slice(1);
}

export function truncate(str: string, length: number): string {
  return str.length > length ? str.slice(0, length) + "..." : str;
}

// packages/utils/src/index.ts
export * from "./string";
export * from "./array";
export * from "./date";

// Usage in apps
import { capitalize, truncate } from "@repo/utils";
```

### Pattern 3: Shared Types

```typescript
// packages/types/src/user.ts
export interface User {
  id: string;
  email: string;
  name: string;
  role: "admin" | "user";
}

export interface CreateUserInput {
  email: string;
  name: string;
  password: string;
}

// Used in both frontend and backend
import type { User, CreateUserInput } from "@repo/types";
```

## CI/CD for Monorepos

### GitHub Actions

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v7
        with:
          fetch-depth: 0 # --affected needs history back to the base branch

      - uses: pnpm/action-setup@v6 # reads "packageManager" from package.json

      - uses: actions/setup-node@v7
        with:
          node-version: 22
          cache: "pnpm"

      - name: Install dependencies
        run: pnpm install --frozen-lockfile

      - name: Build, test, lint and type-check affected packages
        run: pnpm turbo run build test lint typecheck --affected
```

### Deploy Affected Only

Give `deploy` `"cache": false` and `"dependsOn": ["build"]` in `turbo.json`,
and a `deploy` script in each deployable app. Then `--affected` runs it only
for apps the branch changed:

```yaml
- name: Deploy affected apps
  if: github.ref == 'refs/heads/main'
  env:
    TURBO_SCM_BASE: ${{ github.event.before }} # compare with the previous main commit
  run: pnpm turbo run deploy --affected --filter='./apps/*'
```
