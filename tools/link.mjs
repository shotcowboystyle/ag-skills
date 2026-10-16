#!/usr/bin/env node
// Symlink a skill into an agent's skills directory so edits here are live there.
// Usage: node tools/link.mjs <skill-name> [--to <dir>]   (default: ~/.claude/skills)
import { symlinkSync, mkdirSync, existsSync, lstatSync, readlinkSync } from "node:fs";
import { join } from "node:path";
import { homedir } from "node:os";
import { repoRoot } from "./skill.mjs";

const args = process.argv.slice(2);
const name = args[0];
const toIdx = args.indexOf("--to");
const target = toIdx > -1 ? args[toIdx + 1] : join(homedir(), ".claude", "skills");
if (!name) {
  console.error("usage: pnpm install-skill <skill-name> [--to <dir>]");
  process.exit(1);
}
const src = join(repoRoot, "skills", name);
if (!existsSync(join(src, "SKILL.md"))) {
  console.error(`no skill at ${src}`);
  process.exit(1);
}
mkdirSync(target, { recursive: true });
const dest = join(target, name);
if (existsSync(dest) || (() => { try { lstatSync(dest); return true; } catch { return false; } })()) {
  const current = lstatSync(dest).isSymbolicLink() ? readlinkSync(dest) : "(not a symlink)";
  console.error(`${dest} already exists -> ${current}; remove it first`);
  process.exit(1);
}
symlinkSync(src, dest, "dir");
console.log(`${dest} -> ${src}`);
