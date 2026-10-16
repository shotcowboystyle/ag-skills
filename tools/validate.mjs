#!/usr/bin/env node
// Usage: node tools/validate.mjs [dir ...]   (defaults to every dir under skills/)
import { join, relative } from "node:path";
import { validateSkill, listSkillDirs, repoRoot } from "./skill.mjs";

const dirs = process.argv.slice(2).length ? process.argv.slice(2) : listSkillDirs(join(repoRoot, "skills"));
let failed = 0;
for (const dir of dirs) {
  const { errors, warnings } = validateSkill(dir);
  const label = relative(process.cwd(), dir) || dir;
  if (errors.length) {
    failed++;
    console.log(`✗ ${label}`);
    for (const e of errors) console.log(`    error: ${e}`);
  } else console.log(`✓ ${label}`);
  for (const w of warnings) console.log(`    warn:  ${w}`);
}
console.log(`\n${dirs.length - failed}/${dirs.length} skills valid`);
process.exit(failed ? 1 : 0);
