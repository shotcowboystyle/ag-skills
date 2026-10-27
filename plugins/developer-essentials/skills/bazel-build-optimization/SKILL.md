---
name: bazel-build-optimization
description: Optimize Bazel builds for large-scale monorepos using Bzlmod (MODULE.bazel). Use when configuring Bazel, migrating off WORKSPACE, setting up remote caching or execution, or speeding up builds.
last_verified: 2026-10-27
---

# Bazel Build Optimization

Patterns for Bazel 8 and 9 (9.3 at last check) in large monorepos.

## When to Use This Skill

- Setting up Bazel for a monorepo
- Migrating from `WORKSPACE` to `MODULE.bazel`
- Configuring remote caching or execution
- Profiling and speeding up builds
- Writing custom rules

## WORKSPACE Is Gone

Bzlmod (`MODULE.bazel`) is the default since Bazel 7, `WORKSPACE` is off by
default in Bazel 8, and Bazel 9 removes it. Declare external dependencies with
`bazel_dep` from the [Bazel Central Registry](https://registry.bazel.build) and
configure them through module extensions. Rules that used to ship with Bazel
(`cc_*`, `java_*`, `py_*`, `proto_*`) must be loaded from their `rules_*`
modules. To migrate an old repo, run
[`migrate_to_bzlmod.py`](https://bazel.build/external/migration) and move one
dependency at a time.

## Layout

```
repo/
├── MODULE.bazel          # Module name, bazel_dep, extensions
├── MODULE.bazel.lock     # Resolved deps; commit it
├── .bazelrc              # Flags and named configs
├── .bazelversion         # Pins Bazel via Bazelisk
├── BUILD.bazel
├── apps/web/BUILD.bazel
└── libs/utils/BUILD.bazel
```

## Key Concepts

| Concept       | Description                                       |
| ------------- | ------------------------------------------------- |
| **Module**    | Unit of versioning, declared in `MODULE.bazel`    |
| **Extension** | Generates repos (npm, pip) from lockfiles         |
| **Target**    | Buildable unit (library, binary, test)            |
| **Package**   | Directory with a `BUILD.bazel` file               |
| **Label**     | Target identifier, `//path/to:target`             |
| **Rule**      | Defines how to build a target                     |

## Templates

`references/details.md` has the templates: `MODULE.bazel` for JS/TS and
Python, `.bazelrc`, TypeScript and Python `BUILD` files, a custom rule,
queries, remote execution platforms and profiling.

## Best Practices

### Do's

- **Pin Bazel** in `.bazelversion` and run it through Bazelisk
- **Commit `MODULE.bazel.lock`** for reproducible resolution
- **Use fine-grained targets** so changes invalidate less
- **Put every `load()` at the top** of a BUILD file
- **Use visibility** to enforce architecture
- **Use a remote cache** shared by CI and developers; let only CI write

### Don'ts

- **Don't add a `WORKSPACE` file** to a new repo
- **Don't glob across packages** or use globs for deps
- **Don't commit `bazel-*` symlinks**; add them to `.gitignore`
- **Don't ignore build warnings**
