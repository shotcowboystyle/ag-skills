---
name: turborepo-caching
description: Configure Turborepo 2 for efficient monorepo builds with local and remote caching. Use when setting up Turborepo, writing turbo.json tasks, debugging cache misses, or wiring a remote cache into CI.
last_verified: 2026-10-27
---

# Turborepo Caching

Patterns for Turborepo 2.x (`turbo` 2.11 at last check). Monorepo layout and
pnpm workspaces are covered by the `monorepo-management` skill.

## When to Use This Skill

- Writing or migrating `turbo.json`
- Enabling remote caching locally and in CI
- Running only affected packages in CI
- Debugging cache misses

## Turborepo 1.x → 2.x

Turborepo 2 renamed the top-level `pipeline` key to `tasks` and rejects a
`turbo.json` that still uses `pipeline`. Environment variables run in strict
mode by default: a task only sees variables listed in `env`, `globalEnv` or
`passThroughEnv`. Upgrade a 1.x repo with:

```bash
npx @turbo/codemod migrate
```

## Task Options

| Option           | Meaning                                                        |
| ---------------- | -------------------------------------------------------------- |
| `dependsOn`      | `^build` = build dependencies first; `build` = same package    |
| `outputs`        | Files to cache. Omit for tasks that only produce logs          |
| `inputs`         | Files that affect the hash. `$TURBO_DEFAULT$` = git-tracked    |
| `env`            | Env vars that affect the hash and are passed to the task       |
| `cache`          | `false` for tasks with side effects (deploy, db push)          |
| `persistent`     | Long-running task (dev server); nothing can depend on it       |

## Root turbo.json

```json
{
  "$schema": "https://turborepo.dev/schema.json",
  "globalDependencies": [".env"],
  "globalEnv": ["NODE_ENV"],
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "inputs": ["$TURBO_DEFAULT$", "!**/*.md", "!**/*.test.*"],
      "outputs": ["dist/**", ".next/**", "!.next/cache/**"],
      "env": ["API_URL", "NEXT_PUBLIC_*"]
    },
    "test": {
      "dependsOn": ["^build"],
      "outputs": ["coverage/**"],
      "env": ["CI"]
    },
    "lint": {},
    "typecheck": {
      "dependsOn": ["^build"]
    },
    "db:generate": {
      "cache": false
    },
    "@repo/web#build": {
      "dependsOn": ["^build", "@repo/db#db:generate"]
    },
    "deploy": {
      "dependsOn": ["build", "test", "lint"],
      "cache": false
    },
    "dev": {
      "cache": false,
      "persistent": true
    }
  }
}
```

## Package Configuration

A `turbo.json` inside a package overrides the root for that package only.
`extends` must start with `"//"` (the root).

```json
{
  "$schema": "https://turborepo.dev/schema.json",
  "extends": ["//"],
  "tasks": {
    "build": {
      "outputs": [".next/**", "!.next/cache/**"],
      "env": ["NEXT_PUBLIC_API_URL"]
    }
  }
}
```

## Remote Caching

### Vercel Remote Cache

```bash
npx turbo login
npx turbo link
```

In CI, set `TURBO_TOKEN` (secret) and `TURBO_TEAM` (team slug). Control cache
sources with `--cache` (default `local:rw,remote:rw`); `--remote-only` is
deprecated.

```bash
# CI that reads the remote cache but never writes it (e.g. fork PRs)
turbo run build --cache=local:rw,remote:r

# Skip the local cache, use only the remote cache
turbo run build --cache=remote:rw
```

### Self-hosted Remote Cache

Turborepo talks to any server that implements its Remote Cache HTTP API. Run a
maintained implementation (for example `ducktors/turborepo-remote-cache`) rather
than writing one: a cache server stores executable build output, so it needs
authentication, path validation and access control. Point Turborepo at it:

```bash
export TURBO_API="https://turbo-cache.internal.example.com"
export TURBO_TOKEN="$CACHE_TOKEN"   # bearer token the server checks
export TURBO_TEAM="my-team"
turbo run build
```

Or set `remoteCache.apiUrl` in `turbo.json`. Enable artifact signing so
corrupted or partial uploads are rejected:

```json
{
  "remoteCache": { "signature": true }
}
```

With `signature: true`, Turborepo signs uploads with HMAC-SHA256 using
`TURBO_REMOTE_CACHE_SIGNATURE_KEY` (use at least 32 bytes) and rejects artifacts
with a missing or bad signature. This checks integrity; it does not replace
server authentication.

## CI (GitHub Actions)

```yaml
name: CI
on:
  push:
    branches: [main]
  pull_request:

env:
  TURBO_TOKEN: ${{ secrets.TURBO_TOKEN }}
  TURBO_TEAM: ${{ vars.TURBO_TEAM }}

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
        with:
          fetch-depth: 0 # --affected needs history back to the base branch
      - uses: pnpm/action-setup@v6
      - uses: actions/setup-node@v7
        with:
          node-version: 22
          cache: pnpm
      - run: pnpm install --frozen-lockfile
      - run: pnpm turbo run build test lint --affected
```

`--affected` equals `--filter=...[main...HEAD]`. Override the base with
`TURBO_SCM_BASE`. A shallow checkout makes every package look changed.

## Filtering

```bash
turbo run build --filter=@repo/web        # one package
turbo run build --filter=@repo/web...     # package and its dependencies
turbo run build --filter=...@repo/ui      # package and its dependents
turbo run build --filter='./apps/*'       # by directory
turbo run build --filter='!@repo/docs'    # exclude
turbo run build --filter='...[HEAD^1]'    # changed since a commit, plus dependents
```

## Debugging Cache Misses

```bash
turbo run build --dry=json        # hashes and inputs without running
turbo run build --summarize       # writes .turbo/runs/<id>.json; diff two runs
turbo run build --graph=graph.svg # task graph (svg, html, mermaid, dot)
turbo run build --force           # ignore cache reads
turbo run build -vv               # debug logging
```

Common causes: an env var missing from `env` (strict mode hides it and it
doesn't affect the hash), a generated file inside `inputs`, `outputs` that
don't match where the tool writes, and lockfile changes (which affect every
package that depends on the changed entries).

## Best Practices

- Declare every env var a task reads in `env` or `globalEnv`.
- Give tasks that write nothing no `outputs`; give side-effect tasks `cache: false`.
- Use `workspace:*` for internal dependencies so the graph is correct.
- Read-only remote cache for untrusted PRs; write from trusted branches only.
- Never commit `TURBO_TOKEN` or the signature key.
