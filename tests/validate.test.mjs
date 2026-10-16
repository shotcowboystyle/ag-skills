import { test } from "node:test";
import assert from "node:assert/strict";
import { join } from "node:path";
import { validateSkill, parseSkillMd } from "../tools/skill.mjs";

const fx = (n) => join(new URL("./fixtures", import.meta.url).pathname, n);

test("valid skill has no errors or warnings", () => {
  assert.deepEqual(validateSkill(fx("good-skill")), { errors: [], warnings: [] });
});

test("rejects bad name and dir mismatch", () => {
  const { errors } = validateSkill(fx("bad-name"));
  assert.ok(errors.some((e) => e.includes("lowercase")));
  assert.ok(errors.some((e) => e.includes("does not match directory")));
});

test("requires description, warns on unknown keys", () => {
  const { errors, warnings } = validateSkill(fx("no-description"));
  assert.deepEqual(errors, ["description is required"]);
  assert.deepEqual(warnings, ['unknown frontmatter key "extra"']);
});

test("flags broken relative links, ignores http", () => {
  const { errors } = validateSkill(fx("broken-link"));
  assert.deepEqual(errors, ["broken link: references/missing.md"]);
});

test("missing SKILL.md", () => {
  assert.deepEqual(validateSkill(fx("does-not-exist")).errors, ["missing SKILL.md"]);
});

test("parseSkillMd splits frontmatter and body", () => {
  const { frontmatter, body } = parseSkillMd("---\nname: x\n---\nhello");
  assert.equal(frontmatter.name, "x");
  assert.equal(body, "hello");
  assert.equal(parseSkillMd("no frontmatter").frontmatter, null);
});
