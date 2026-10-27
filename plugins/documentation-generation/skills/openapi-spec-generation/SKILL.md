---
name: openapi-spec-generation
description: Write, generate and lint OpenAPI 3.1 specifications, design-first or from code (FastAPI, tsoa), and generate SDKs from them. Use when creating or fixing an API contract, migrating a 3.0 spec to 3.1, or adding Spectral or Redocly linting to CI.
last_verified: 2026-10-27
---

# OpenAPI Spec Generation

Write OpenAPI 3.1 specifications that lint clean, and keep them in step with the code.

## When to Use This Skill

- Writing an API contract before the code exists (design-first)
- Generating a spec from an existing FastAPI or tsoa codebase (code-first)
- Migrating a 3.0 spec to 3.1
- Adding spec linting to CI, or generating client SDKs

## Procedure

1. **Pick the approach.** Design-first for a new API or a contract other teams consume.
   Code-first when the code exists and is the source of truth: FastAPI emits 3.1 from
   `app.openapi()`, tsoa from its decorators.
2. **Start from the template** in `references/details.md` (Template 1). Set
   `openapi: 3.1.0`, real `servers`, and one `securitySchemes` entry per auth method.
3. **Define each schema once** under `components/schemas` and `$ref` it. Give every
   operation an `operationId`, a `summary`, a `description`, and its 4xx responses.
4. **Write 3.1 schemas, not 3.0 ones.** 3.1 schemas are JSON Schema 2020-12. See the
   table below.
5. **Lint.** Both must pass before the spec is committed:

   ```bash
   npx @redocly/cli@2 lint openapi.yaml
   npx @stoplight/spectral-cli@6 lint openapi.yaml --fail-severity=warn
   ```

   Rulesets for both are in `references/code-first-and-tooling.md` (Template 4). Redocly
   rejects 3.0 keywords such as `nullable` in a 3.1 document.
6. **Add the lint to CI** and fail the build on errors. For code-first, export the spec in
   CI and diff it against the committed one so a code change can't drift silently.

## 3.0 to 3.1 changes

| 3.0 | 3.1 |
| --- | --- |
| `nullable: true` | `type: [string, "null"]`, or `anyOf` with `{type: "null"}` for a `$ref` |
| `example:` inside a schema | `examples:` (a list) inside a schema; media-type `example`/`examples` are unchanged |
| `exclusiveMinimum: true` + `minimum: 0` | `exclusiveMinimum: 0` |
| `type: string, format: binary` for uploads | `contentMediaType: application/octet-stream` |
| `$ref` siblings ignored | `$ref` may have sibling keywords such as `description` |

```yaml
# Nullable scalar
avatar:
  type: [string, "null"]
  format: uri

# Nullable reference
manager:
  anyOf:
    - $ref: "#/components/schemas/User"
    - type: "null"
```

## Design approaches

| Approach         | Description                  | Best For            |
| ---------------- | ---------------------------- | ------------------- |
| **Design-First** | Write spec before code       | New APIs, contracts |
| **Code-First**   | Generate spec from code      | Existing APIs       |
| **Hybrid**       | Annotate code, generate spec | Evolving APIs       |

## References

- `references/details.md`: Template 1, a complete 3.1 spec that passes both linters.
- `references/code-first-and-tooling.md`: FastAPI and tsoa code-first templates, the
  Spectral and Redocly rulesets, and SDK generation.

## Don'ts

- **Don't use 3.0 keywords in a 3.1 spec**: `nullable`, boolean `exclusiveMinimum`.
- **Don't skip security**: every operation is covered by a security requirement or is
  marked public with `security: []`.
- **Don't mix naming styles**: properties and path parameters are camelCase throughout.
- **Don't hardcode environments**: list each one under `servers`, or use server variables.
- **Don't publish numbers you haven't measured**: rate limits and quotas come from the
  gateway config, not from a guess.
