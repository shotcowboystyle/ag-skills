#!/usr/bin/env node
// Usage: node tools/new-skill.mjs <skill-name> ["one-line description"]
import { mkdirSync, writeFileSync, existsSync } from "node:fs";
import { join } from "node:path";
import { repoRoot } from "./skill.mjs";

const [name, description = "TODO: what this skill does and when the agent should use it."] = process.argv.slice(2);
if (!name || !/^[a-z0-9]+(-[a-z0-9]+)*$/.test(name)) {
  console.error("usage: pnpm new <kebab-case-name> [description]");
  process.exit(1);
}
const dir = join(repoRoot, "skills", name);
if (existsSync(dir)) {
  console.error(`${dir} already exists`);
  process.exit(1);
}
mkdirSync(join(dir, "tests"), { recursive: true });
writeFileSync(
  join(dir, "SKILL.md"),
  `---
name: ${name}
description: ${description}
---

# ${name}

## When to use

TODO

## Steps

1. TODO
`,
);
writeFileSync(
  join(dir, "tests", `${name}.test.mjs`),
  `import { test } from "node:test";
import assert from "node:assert/strict";
import { validateSkill } from "../../../tools/skill.mjs";

const dir = new URL("..", import.meta.url).pathname;

test("${name} passes spec validation", () => {
  assert.deepEqual(validateSkill(dir).errors, []);
});
`,
);
console.log(`created skills/${name}`);
