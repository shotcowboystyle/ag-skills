import { test } from "node:test";
import assert from "node:assert/strict";
import { validateSkill } from "../../../tools/skill.mjs";

const dir = new URL("..", import.meta.url).pathname;

test("skill-authoring passes spec validation", () => {
  assert.deepEqual(validateSkill(dir).errors, []);
});
