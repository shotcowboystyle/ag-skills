---
name: nx-workspace-patterns
description: Configure and optimize Nx monorepo workspaces. Use when setting up Nx, configuring project boundaries, optimizing build caching, or implementing affected commands.
last_verified: 2026-10-27
---

# Nx Workspace Patterns

Patterns for current Nx (24.x at last check).

## When to Use This Skill

- Setting up new Nx workspaces
- Configuring project boundaries
- Optimizing CI with affected commands
- Implementing remote caching
- Managing dependencies between projects
- Upgrading an older Nx workspace

## Core Concepts

### 1. Nx Architecture

```
workspace/
├── apps/                  # Deployable applications
│   ├── web/project.json
│   └── api/project.json
├── libs/                  # Shared libraries
│   ├── shared/{ui,utils}/
│   └── feature/{auth,dashboard}/
├── tools/                 # Local generators and plugins
├── nx.json                # Workspace-wide defaults and plugins
├── eslint.config.mjs      # Flat config with module boundaries
└── package.json
```

Each project is configured by its own `project.json` or `package.json`.
`workspace.json` was removed; `nx.json` no longer lists projects.

### 2. What Changed From Older Nx

| Old                                         | Current                                          |
| ------------------------------------------- | ------------------------------------------------ |
| `workspace.json`                            | Per-project `project.json` / `package.json`      |
| `tasksRunnerOptions` / `cacheableOperations` | `"cache": true` in `targetDefaults` or targets   |
| `nx-cloud` / custom tasks runners           | `nxCloudId`, or a self-hosted cache server       |
| `npmScope`                                  | Package names in each `package.json`             |
| `affected.defaultBase`                      | Top-level `defaultBase`                          |
| `nx affected:build`                         | `nx affected -t build`                           |
| `.eslintrc.json`                            | `eslint.config.mjs` (flat config)                |
| Hand-written targets for every tool         | Inferred tasks from plugins in `nx.json`         |

Run `nx migrate latest` then `nx migrate --run-migrations` to upgrade; the
migrations rewrite most of these.

### 3. Library Types

| Type            | Purpose                          | Example             |
| --------------- | -------------------------------- | ------------------- |
| **feature**     | Smart components, business logic | `feature-auth`      |
| **ui**          | Presentational components        | `ui-buttons`        |
| **data-access** | API calls, state management      | `data-access-users` |
| **util**        | Pure functions, helpers          | `util-formatting`   |
| **shell**       | App bootstrapping                | `shell-web`         |

## Templates and detailed worked examples

`references/details.md` has `nx.json`, `project.json`, module boundary rules,
a local generator, CI with affected commands, and remote caching.

## Best Practices

### Do's

- **Use tags consistently** - Enforce with module boundaries
- **Enable caching early** - Significant CI savings
- **Keep libs focused** - Single responsibility
- **Use generators** - Ensure consistency
- **Let plugins infer targets** - Less config to drift

### Don'ts

- **Don't create circular deps** - Graph should be acyclic
- **Don't skip affected** - Test only what changed
- **Don't ignore boundaries** - Tech debt accumulates
- **Don't over-granularize** - Balance lib count
- **Don't commit cache tokens** - Use CI secrets
