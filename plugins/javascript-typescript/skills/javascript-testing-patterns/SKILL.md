---
name: javascript-testing-patterns
description: Implement comprehensive testing strategies using Jest, Vitest, and Testing Library for unit tests, integration tests, and end-to-end testing with mocking, fixtures, and test-driven development. Use when writing JavaScript/TypeScript tests, setting up test infrastructure, or implementing TDD/BDD workflows.
---

# JavaScript Testing Patterns

Comprehensive guide for implementing robust testing strategies in JavaScript/TypeScript applications using modern testing frameworks and best practices.

## When to Use This Skill

- Setting up test infrastructure for new projects
- Writing unit tests for functions and classes
- Creating integration tests for APIs and services
- Implementing end-to-end tests for user flows
- Mocking external dependencies and APIs
- Testing React, Vue, or other frontend components
- Implementing test-driven development (TDD)
- Setting up continuous testing in CI/CD pipelines

## Testing Frameworks

### Jest - Full-Featured Testing Framework

**Setup:**

```typescript
// jest.config.ts
import type { Config } from "jest";

const config: Config = {
  preset: "ts-jest",
  testEnvironment: "node",
  roots: ["<rootDir>/src"],
  testMatch: ["**/__tests__/**/*.ts", "**/?(*.)+(spec|test).ts"],
  collectCoverageFrom: [
    "src/**/*.ts",
    "!src/**/*.d.ts",
    "!src/**/*.interface.ts",
  ],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80,
    },
  },
  setupFilesAfterEnv: ["<rootDir>/src/test/setup.ts"],
};

export default config;
```

### Vitest - Fast, Vite-Native Testing

**Setup:**

```typescript
// vitest.config.ts
import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    globals: true,
    environment: "node",
    coverage: {
      provider: "v8",
      reporter: ["text", "json", "html"],
      exclude: ["**/*.d.ts", "**/*.config.ts", "**/dist/**"],
    },
    setupFiles: ["./src/test/setup.ts"],
  },
});
```

## Unit Testing Patterns

### Pattern 1: Testing Pure Functions

```typescript
// utils/calculator.ts
export function add(a: number, b: number): number {
  return a + b;
}

export function divide(a: number, b: number): number {
  if (b === 0) {
    throw new Error("Division by zero");
  }
  return a / b;
}

// utils/calculator.test.ts
import { describe, it, expect } from "vitest";
import { add, divide } from "./calculator";

describe("Calculator", () => {
  describe("add", () => {
    it("should add two positive numbers", () => {
      expect(add(2, 3)).toBe(5);
    });

    it("should add negative numbers", () => {
      expect(add(-2, -3)).toBe(-5);
    });

    it("should handle zero", () => {
      expect(add(0, 5)).toBe(5);
      expect(add(5, 0)).toBe(5);
    });
  });

  describe("divide", () => {
    it("should divide two numbers", () => {
      expect(divide(10, 2)).toBe(5);
    });

    it("should handle decimal results", () => {
      expect(divide(5, 2)).toBe(2.5);
    });

    it("should throw error when dividing by zero", () => {
      expect(() => divide(10, 0)).toThrow("Division by zero");
    });
  });
});
```

### Pattern 2: Testing Classes

Create a fresh instance in `beforeEach` so state never leaks between tests. Cover each public method's success path and its error path (duplicate create, update of a missing record).

### Pattern 3: Testing Async Functions

Stub `global.fetch` with `vi.fn()`, reset it with `vi.clearAllMocks()` in `beforeEach`, and drive each case with `mockResolvedValueOnce`. Assert rejections with `await expect(promise).rejects.toThrow(...)` and check request shape with `expect.objectContaining`.

See `references/unit-and-mocking-examples.md` for the full `UserService` class and `ApiService` async examples.

## Mocking Patterns

### Pattern 1: Mocking Modules

Replace a third-party module with `vi.mock("module", () => ({ ... }))` at the top of the test file, then assert on the mocked calls (for example, `sendMail` on a mocked `nodemailer` transport).

### Pattern 2: Dependency Injection for Testing

Inject collaborators through the constructor behind an interface (`IUserRepository`). Tests pass an object of `vi.fn()` stubs and set per-case results with `vi.mocked(fn).mockResolvedValue(...)`.

### Pattern 3: Spying on Functions

Use `vi.spyOn(obj, "method")` to observe calls on a real object without replacing the module, and call `mockRestore()` in `afterEach`. Assert with `toHaveBeenCalledWith` and `toHaveBeenCalledTimes`.

See `references/unit-and-mocking-examples.md` for the complete email, repository-injection and logger-spy examples.

## Integration Testing

Integration tests verify real database operations and HTTP endpoints using `supertest` and a test database instance. Always truncate tables in `beforeEach` and tear down in `afterAll`.

For full API integration test examples (supertest + PostgreSQL) and database repository integration tests, see [references/advanced-testing-patterns.md](references/advanced-testing-patterns.md).

## Frontend Testing with Testing Library

Test React components by rendering them and querying by role, placeholder, or test ID. Test hooks with `renderHook` + `act`. Prefer semantic queries (`getByRole`, `getByPlaceholderText`) over `data-testid`.

For complete React component test examples (UserForm, hooks with `renderHook`/`act`), see [references/advanced-testing-patterns.md](references/advanced-testing-patterns.md).

## Test Fixtures and Factories

Use `@faker-js/faker` to generate realistic test data factories. Factories accept optional `overrides` so tests can set only the fields they care about:

```typescript
// tests/fixtures/user.fixture.ts
import { faker } from "@faker-js/faker";

export function createUserFixture(overrides?: Partial<User>): User {
  return {
    id: faker.string.uuid(),
    name: faker.person.fullName(),
    email: faker.internet.email(),
    createdAt: faker.date.past(),
    ...overrides,
  };
}
```

For snapshot testing, coverage configuration, test organization patterns, promise testing, and timer mocking, see [references/advanced-testing-patterns.md](references/advanced-testing-patterns.md).

## Best Practices

1. **Follow AAA Pattern**: Arrange, Act, Assert
2. **One assertion per test**: Or logically related assertions
3. **Descriptive test names**: Should describe what is being tested
4. **Use beforeEach/afterEach**: For setup and teardown
5. **Mock external dependencies**: Keep tests isolated
6. **Test edge cases**: Not just happy paths
7. **Avoid implementation details**: Test behavior, not implementation
8. **Use test factories**: For consistent test data
9. **Keep tests fast**: Mock slow operations
10. **Write tests first (TDD)**: When possible
11. **Maintain test coverage**: Aim for 80%+ coverage
12. **Use TypeScript**: For type-safe tests
13. **Test error handling**: Not just success cases
14. **Use data-testid sparingly**: Prefer semantic queries
15. **Clean up after tests**: Prevent test pollution
