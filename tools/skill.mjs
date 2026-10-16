// Parse and validate a skill directory against the Agent Skills spec
// (https://agentskills.io/specification). Pure functions, no I/O side effects.
import { readFileSync, existsSync, readdirSync, statSync } from "node:fs";
import { join, basename, dirname, resolve } from "node:path";
import YAML from "yaml";

const NAME_RE = /^[a-z0-9]+(-[a-z0-9]+)*$/;
const KNOWN_KEYS = new Set(["name", "description", "license", "compatibility", "metadata", "allowed-tools"]);
const MAX_BODY_LINES = 500;

export function parseSkillMd(text) {
  const m = text.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n?([\s\S]*)$/);
  if (!m) return { frontmatter: null, body: text };
  let frontmatter;
  try {
    frontmatter = YAML.parse(m[1]);
  } catch (e) {
    return { frontmatter: null, body: m[2], parseError: e.message };
  }
  return { frontmatter, body: m[2] };
}

/** @returns {{errors: string[], warnings: string[]}} */
export function validateSkill(dir) {
  const errors = [];
  const warnings = [];
  const skillPath = join(dir, "SKILL.md");
  if (!existsSync(skillPath)) return { errors: ["missing SKILL.md"], warnings };

  const { frontmatter: fm, body, parseError } = parseSkillMd(readFileSync(skillPath, "utf8"));
  if (parseError) return { errors: [`frontmatter is not valid YAML: ${parseError}`], warnings };
  if (!fm || typeof fm !== "object") return { errors: ["missing YAML frontmatter"], warnings };

  const dirName = basename(resolve(dir));
  if (typeof fm.name !== "string" || !fm.name) errors.push("name is required");
  else {
    if (!NAME_RE.test(fm.name)) errors.push(`name "${fm.name}" must be lowercase letters, digits, hyphens`);
    if (fm.name.length > 64) errors.push("name exceeds 64 characters");
    if (fm.name !== dirName) errors.push(`name "${fm.name}" does not match directory "${dirName}"`);
  }

  if (typeof fm.description !== "string" || !fm.description.trim()) errors.push("description is required");
  else if (fm.description.length > 1024) errors.push("description exceeds 1024 characters");

  if (fm.compatibility !== undefined) {
    if (typeof fm.compatibility !== "string") errors.push("compatibility must be a string");
    else if (fm.compatibility.length > 500) errors.push("compatibility exceeds 500 characters");
  }
  if (fm.license !== undefined && typeof fm.license !== "string") errors.push("license must be a string");
  if (fm["allowed-tools"] !== undefined && typeof fm["allowed-tools"] !== "string") errors.push("allowed-tools must be a string");
  if (fm.metadata !== undefined) {
    if (!fm.metadata || typeof fm.metadata !== "object" || Array.isArray(fm.metadata)) errors.push("metadata must be a map");
    else for (const [k, v] of Object.entries(fm.metadata)) if (typeof v !== "string") errors.push(`metadata.${k} must be a string`);
  }
  for (const k of Object.keys(fm)) if (!KNOWN_KEYS.has(k)) warnings.push(`unknown frontmatter key "${k}"`);

  if (!body.trim()) errors.push("SKILL.md body is empty");
  const lines = body.split("\n").length;
  if (lines > MAX_BODY_LINES) warnings.push(`body is ${lines} lines; keep under ${MAX_BODY_LINES}, move detail to references/`);

  // Relative links in the body must resolve to real files.
  for (const [, target] of body.matchAll(/\]\(([^)\s]+)\)/g)) {
    if (/^(https?:|mailto:|#)/.test(target)) continue;
    if (!existsSync(join(dir, target.split("#")[0]))) errors.push(`broken link: ${target}`);
  }

  const scripts = join(dir, "scripts");
  if (existsSync(scripts)) {
    for (const f of readdirSync(scripts)) {
      const st = statSync(join(scripts, f));
      if (st.isFile() && !(st.mode & 0o111)) warnings.push(`scripts/${f} is not executable`);
    }
  }

  return { errors, warnings };
}

export function listSkillDirs(root) {
  if (!existsSync(root)) return [];
  return readdirSync(root)
    .map((n) => join(root, n))
    .filter((p) => statSync(p).isDirectory())
    .sort();
}

export const repoRoot = resolve(dirname(new URL(import.meta.url).pathname), "..");
