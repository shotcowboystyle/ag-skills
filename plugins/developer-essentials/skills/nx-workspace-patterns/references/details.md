# nx-workspace-patterns — templates and worked examples

## Templates

### Template 1: nx.json Configuration

```json
{
  "$schema": "./node_modules/nx/schemas/nx-schema.json",
  "defaultBase": "main",
  "parallel": 3,
  "plugins": [
    {
      "plugin": "@nx/vite/plugin",
      "options": {
        "buildTargetName": "build",
        "serveTargetName": "serve",
        "typecheckTargetName": "typecheck"
      }
    },
    {
      "plugin": "@nx/jest/plugin",
      "options": { "targetName": "test" }
    },
    {
      "plugin": "@nx/eslint/plugin",
      "options": { "targetName": "lint" }
    }
  ],
  "targetDefaults": {
    "build": {
      "dependsOn": ["^build"],
      "inputs": ["production", "^production"],
      "cache": true
    },
    "test": {
      "inputs": ["default", "^production", "{workspaceRoot}/jest.preset.js"],
      "cache": true
    },
    "lint": {
      "inputs": ["default", "{workspaceRoot}/eslint.config.mjs"],
      "cache": true
    },
    "e2e": {
      "inputs": ["default", "^production"],
      "cache": true
    }
  },
  "namedInputs": {
    "default": ["{projectRoot}/**/*", "sharedGlobals"],
    "production": [
      "default",
      "!{projectRoot}/**/?(*.)+(spec|test).[jt]s?(x)?(.snap)",
      "!{projectRoot}/tsconfig.spec.json",
      "!{projectRoot}/jest.config.[jt]s",
      "!{projectRoot}/eslint.config.mjs"
    ],
    "sharedGlobals": ["{workspaceRoot}/tsconfig.base.json"]
  },
  "generators": {
    "@nx/react": {
      "library": { "style": "css", "linter": "eslint", "unitTestRunner": "jest" }
    }
  }
}
```

Plugins listed under `plugins` infer targets from tool config files
(`vite.config.ts`, `jest.config.ts`, `eslint.config.mjs`), so projects don't
need hand-written targets for them. Run `nx show project web` to see the
targets Nx inferred.

### Template 2: Project Configuration

```json
// apps/web/project.json
{
  "name": "web",
  "$schema": "../../node_modules/nx/schemas/project-schema.json",
  "sourceRoot": "apps/web/src",
  "projectType": "application",
  "tags": ["type:app", "scope:web"],
  "targets": {
    "build": {
      "outputs": ["{projectRoot}/dist"]
    },
    "deploy": {
      "executor": "nx:run-commands",
      "dependsOn": ["build"],
      "options": {
        "command": "./scripts/deploy.sh apps/web/dist"
      }
    }
  }
}
```

`build`, `serve`, `test` and `lint` come from the plugins; entries here only
override or add to them. A project can use `package.json` instead, with the
same fields under an `"nx"` key.

### Template 3: Module Boundary Rules

```javascript
// eslint.config.mjs
import nx from "@nx/eslint-plugin";

export default [
  ...nx.configs["flat/base"],
  ...nx.configs["flat/typescript"],
  ...nx.configs["flat/javascript"],
  {
    files: ["**/*.ts", "**/*.tsx", "**/*.js", "**/*.jsx"],
    rules: {
      "@nx/enforce-module-boundaries": [
        "error",
        {
          enforceBuildableLibDependency: true,
          allow: [],
          depConstraints: [
            {
              sourceTag: "type:app",
              onlyDependOnLibsWithTags: ["type:feature", "type:ui", "type:data-access", "type:util"],
            },
            {
              sourceTag: "type:feature",
              onlyDependOnLibsWithTags: ["type:ui", "type:data-access", "type:util"],
            },
            { sourceTag: "type:ui", onlyDependOnLibsWithTags: ["type:ui", "type:util"] },
            {
              sourceTag: "type:data-access",
              onlyDependOnLibsWithTags: ["type:data-access", "type:util"],
            },
            { sourceTag: "type:util", onlyDependOnLibsWithTags: ["type:util"] },
            { sourceTag: "scope:web", onlyDependOnLibsWithTags: ["scope:web", "scope:shared"] },
            { sourceTag: "scope:api", onlyDependOnLibsWithTags: ["scope:api", "scope:shared"] },
            { sourceTag: "scope:shared", onlyDependOnLibsWithTags: ["scope:shared"] },
          ],
        },
      ],
    },
  },
];
```

### Template 4: Local Generator

Scaffold the plugin and generator first:

```bash
nx add @nx/plugin
nx g @nx/plugin:plugin tools/workspace-plugin
nx g @nx/plugin:generator tools/workspace-plugin/src/generators/feature-lib
```

```typescript
// tools/workspace-plugin/src/generators/feature-lib/generator.ts
import {
  Tree,
  formatFiles,
  generateFiles,
  joinPathFragments,
  names,
  readProjectConfiguration,
} from "@nx/devkit";
import { libraryGenerator } from "@nx/react";

interface FeatureLibGeneratorSchema {
  name: string;
  scope: string;
}

export default async function featureLibGenerator(
  tree: Tree,
  options: FeatureLibGeneratorSchema,
) {
  const { name, scope } = options;
  const projectName = `${scope}-feature-${name}`;

  // `directory` is required; `name` sets the project name as given
  await libraryGenerator(tree, {
    directory: `libs/${scope}/feature-${name}`,
    name: projectName,
    tags: `type:feature,scope:${scope}`,
    style: "css",
    linter: "eslint",
    unitTestRunner: "jest",
    skipFormat: true,
  });

  const project = readProjectConfiguration(tree, projectName);

  generateFiles(
    tree,
    joinPathFragments(__dirname, "files"),
    project.sourceRoot ?? project.root,
    { ...names(name), scope, tmpl: "" },
  );

  await formatFiles(tree);
}
```

Run it with `nx g @myorg/workspace-plugin:feature-lib auth --scope=web`.

### Template 5: CI Configuration with Affected

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:
  NX_CLOUD_ACCESS_TOKEN: ${{ secrets.NX_CLOUD_ACCESS_TOKEN }}

jobs:
  main:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
        with:
          fetch-depth: 0

      - uses: actions/setup-node@v7
        with:
          node-version: 22
          cache: "npm"

      - run: npm ci

      - name: Derive SHAs for affected commands
        uses: nrwl/nx-set-shas@v5

      - run: npx nx affected -t lint test build
      - run: npx nx affected -t e2e --parallel=1
```

`nx affected` runs only tasks whose inputs a change reaches. Set
`"affected": { "legacy": true }` in `nx.json` to run every task of every
affected project instead.

### Template 6: Remote Caching

Nx Cloud:

```bash
npx nx connect   # writes "nxCloudId" to nx.json
```

```json
// nx.json
{
  "nxCloudId": "SOMEID"
}
```

In CI, give the job a read-write access token through `NX_CLOUD_ACCESS_TOKEN`
and give untrusted pull requests a read-only token. Don't put tokens in
`nx.json`.

Self-hosted: custom tasks runners such as `nx-aws-cache` no longer work. Run a
server that implements Nx's remote cache OpenAPI spec (see "Self-hosted remote
cache" in the Nx docs) and point Nx at it:

```bash
export NX_SELF_HOSTED_REMOTE_CACHE_SERVER="https://nx-cache.internal.example.com"
export NX_SELF_HOSTED_REMOTE_CACHE_ACCESS_TOKEN="$CACHE_TOKEN"
npx nx affected -t build
```

Use `--skipRemoteCache` to skip the remote cache for one command.

## Common Commands

```bash
# Generate a library (the directory is the positional argument)
nx g @nx/react:lib libs/web/feature-auth --tags=type:feature,scope:web

# Run affected tests
nx affected -t test --base=main

# Run a target for many projects
nx run-many -t build --projects=tag:scope:web

# Inspect a project's resolved targets
nx show project web

# View dependency graph
nx graph

# Run a specific project and configuration
nx build web --configuration=production

# Reset cache and daemon
nx reset

# Upgrade Nx and run migrations
nx migrate latest
nx migrate --run-migrations
```
