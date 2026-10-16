// Every skill under skills/ must pass spec validation.
import { test } from "node:test";
import assert from "node:assert/strict";
import { join, basename } from "node:path";
import { validateSkill, listSkillDirs, repoRoot } from "../tools/skill.mjs";

for (const dir of listSkillDirs(join(repoRoot, "skills"))) {
  test(`skills/${basename(dir)} is valid`, () => {
    assert.deepEqual(validateSkill(dir).errors, []);
  });
}
