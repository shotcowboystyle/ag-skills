---
name: monorepo-management
description: Master monorepo management with pnpm workspaces, Turborepo, and Nx to build efficient, scalable multi-package repositories with shared dependencies, shared configs, and package publishing. Use when setting up monorepos, structuring packages, or managing shared dependencies.
last_verified: 2026-10-27
---

# Monorepo Management

Build monorepos that share code, tooling and atomic changes across packages and
applications. This skill covers layout, workspaces, internal packages and
publishing. For task configuration and caching, use the `turborepo-caching`,
`nx-workspace-patterns` or `bazel-build-optimization` skill.

## When to Use This Skill

- Setting up new monorepo projects
- Migrating from multi-repo to monorepo
- Managing shared dependencies
- Implementing code sharing strategies
- Setting up CI/CD for monorepos
- Versioning and publishing packages

## Core Concepts

### 1. Why Monorepos?

**Advantages:** shared code and dependencies, atomic commits across projects,
consistent tooling, easier refactoring, better code visibility.

**Challenges:** build performance at scale, CI complexity, access control,
large Git history.

### 2. Monorepo Tools

**Package managers** (workspaces): pnpm (recommended), npm, Yarn Berry.

**Task runners and build systems:**

- Turborepo — simple task graph and caching on top of package scripts
- Nx — task graph plus generators, inferred tasks and module boundaries
- Bazel — hermetic, multi-language builds for very large repos
- Lerna — now maintained by the Nx team; use it only for its publishing commands

## Setup

```bash
npx create-turbo@latest my-monorepo --package-manager pnpm
# or: npx create-nx-workspace@latest my-org
```

```
apps/
  web/          # Next.js app
  docs/         # Documentation site
packages/
  ui/           # Shared UI components
  tsconfig/     # Shared TypeScript configs
  eslint-config/
pnpm-workspace.yaml
turbo.json      # or nx.json
package.json
```

```json
// package.json (root)
{
  "name": "my-monorepo",
  "private": true,
  "scripts": {
    "build": "turbo run build",
    "dev": "turbo run dev",
    "test": "turbo run test",
    "lint": "turbo run lint",
    "format": "prettier --write \"**/*.{ts,tsx,md}\""
  },
  "devDependencies": {
    "prettier": "^3.6.0",
    "turbo": "^2.11.0",
    "typescript": "^7.0.0"
  },
  "packageManager": "pnpm@12.15.0"
}
```

pnpm reads workspace packages and pnpm settings only from
`pnpm-workspace.yaml` (see `references/details.md`); `.npmrc` holds registry
auth only.

### Internal Package

```json
// packages/ui/package.json
{
  "name": "@repo/ui",
  "version": "0.0.0",
  "private": true,
  "type": "module",
  "exports": {
    ".": {
      "types": "./dist/index.d.ts",
      "default": "./dist/index.js"
    },
    "./button": {
      "types": "./dist/button.d.ts",
      "default": "./dist/button.js"
    }
  },
  "scripts": {
    "build": "tsc -p tsconfig.build.json",
    "dev": "tsc -p tsconfig.build.json --watch",
    "lint": "eslint src/",
    "typecheck": "tsc --noEmit"
  },
  "devDependencies": {
    "@repo/tsconfig": "workspace:*",
    "typescript": "^7.0.0"
  },
  "peerDependencies": {
    "react": "^19.0.0"
  }
}
```

`types` must come first in each `exports` entry: TypeScript takes the first
condition that matches, so a `types` entry after `import` or `default` is never
read. `tsc` emits one `.js` and one `.d.ts` per source file, so the paths
above are exact. To bundle or ship ESM and CJS together, use `tsdown`; `tsup`
is no longer maintained.

## Detailed patterns and worked examples

`references/details.md` covers pnpm workspace settings and commands, shared
TypeScript and ESLint configs, code-sharing patterns and CI.

## Best Practices

1. **Consistent versions**: one version per dependency, via pnpm catalogs
2. **Shared configs**: centralize ESLint, TypeScript and Prettier configs
3. **Acyclic graph**: no circular dependencies between packages
4. **Correct cache inputs**: declare inputs, outputs and env vars per task
5. **Shared types**: one package for types used by frontend and backend
6. **Testing**: unit tests in packages, end-to-end tests in apps
7. **Documentation**: a README in each package
8. **Releases**: changesets for versioning and changelogs

## Common Pitfalls

- **Circular dependencies**: A depends on B, B depends on A
- **Phantom dependencies**: importing a package not in your `package.json`
- **Wrong cache inputs**: missing files or env vars in task inputs
- **Over-sharing**: sharing code that should stay separate
- **Under-sharing**: duplicating code across packages

## Publishing Packages

```bash
pnpm add -Dw @changesets/cli
pnpm changeset init
pnpm changeset          # describe a change
pnpm changeset version  # bump versions and changelogs (exits 1 if none pending)
pnpm changeset publish
```

Changesets 3 needs Node 22.11+ and no longer versions private packages unless
`privatePackages` is set in `.changeset/config.json`.

```yaml
# .github/workflows/release.yml (step)
- name: Create Release Pull Request or Publish
  uses: changesets/action@v2
  with:
    publish: pnpm changeset publish
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
```
