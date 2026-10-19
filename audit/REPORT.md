# Agent & Skill Quality Audit — 2026-10-18

Scope: every agent (`plugins/*/agents/*.md`, 183 files / 133 unique bodies) and every skill (`plugins/*/skills/*/SKILL.md` + bundled `references/`, `scripts/`, `assets/`, 322 skills) across 80 local plugins. Commands were reviewed only where they wire to agents/skills.
Branch: `shotcowboystyle/full-audit` @ `7b8d94b`. **Report only — no source files were changed.**

Detail per item (grade, severity, line refs, fix) lives in `audit/findings-group{0..7}.md`. This file holds the cross-cutting picture and the prioritized fix list.

## Method

1. **Mechanical sweep** (script over all frontmatter and bodies): name/description shape, model tier, `tools:` presence, body size, dead links, missing/orphaned bundled files, byte-level duplicate detection, Codex 8 KB cap, splitter damage (odd code fences, orphan headings).
2. **Existing gates**: `make garden` → clean (9 checks); `check_agent_name_collisions.py` → clean; `evals/static-score-snapshot.json` (skills only) → 12 gold / 136 silver / 149 bronze / 25 no badge. Weakest sub-scores: `structural_completeness` 0.42, `progressive_disclosure` 0.52.
3. **Qualitative review**: 8 parallel reviewers, ~57 items each, against an 8-point rubric (single responsibility, trigger quality, actionability, correctness/currency, progressive disclosure, frontmatter/tier/tools, safety, portability).
4. **Verification**: I re-checked a sample of high-severity claims against the source. Confirmed: data-quality-frameworks corruption, `cat >` over settings.json in block-no-verify-hook, ml-pipeline-workflow (only SKILL.md exists), bash-pro BASH_VERSINFO logic, policy-enforcer "all permit rules must match", paypal-integration `paypalrestsdk`, k8s-security-policies PodSecurityPolicy, ai-video-producer `pipelines/<name>.md` vs agent layout, and hardcoded "Daniel" in pipeline-repo-setup. Unchecked claims are marked as reviewer findings in the group files. Items flagged "needs measurement" or "probably" have not been verified.

## Scorecard

| Grade | Count | Meaning |
|---|---|---|
| A | 40 | Ship as is |
| B | 184 | Minor fixes |
| C | 173 | Needs rework: generic, overlapping, or stale |
| D | 54 | Wrong, unsafe, or a kitchen-sink persona |
| F | 2 | Broken: `data-quality-frameworks`, `ml-pipeline-workflow` |

About 453 graded items in total; the counts were self-reported by the reviewers.

**Strongest plugins (use them as the house style):** operating-kit, review-agent-governance, signed-audit-trails, llm-finetuning, dgx-spark-ops, email-deliverability (`email-dns-setup` A), matter-ops, evidence-ops (good decomposition, gaps in the wiring between skills), avoid-ai-writing, file-conversion.

**Weakest clusters:** generic "expert" agents in the wshobson style (backend, cloud, cicd, python, systems, SEO, data, ML), design-ops (size and overlap), meta-wearables-ops and ios-ops (overlap and knowledge-base bloat), ai-video-producer (path contract), payment-processing, the shell-scripting stubs.

---

## Systemic findings (fix once, many items improve)

### S1. Duplicate agent copies: 50 redundant files
183 agent files have only 133 unique bodies. 27 basenames are copied byte-for-byte across 2–6 plugins: backend-architect ×6, code-reviewer ×6, test-automator ×6, performance-engineer ×5, cloud-architect/deployment-engineer/frontend-developer/security-auditor/debugger ×4, and others. Only the frontmatter `name` differs. As a result, every fix has to land N times, and the copies are already drifting: `code-reviewer`, `debugger`, `security-auditor`, `test-automator` and `performance-engineer` each have a divergent variant. Several copies are also orphaned or in the wrong plugin: nothing in `database-cloud-optimization` calls its DB agents, `distributed-debugging` never calls error-detective, `code-documentation/code-reviewer` is unused, and frontend-developer sits in application-performance.
**Fix:** give each agent one canonical home. Plugins that need it should declare a dependency, or have the generator materialize the copies from one source; add a CI check that fails on byte-identical bodies. Delete the orphaned copies.

### S2. Personas with capability lists instead of procedures
Most agents inherited from the wshobson collection use the "Capabilities / Behavioral Traits / Knowledge Base / Response Approach" template: 150–300 lines of bullets with no decision rules, no stop conditions and no output contract. 130 of 183 agents carry a "Use PROACTIVELY" trigger, so broad agents (ai-engineer, python-pro, cloud-architect, mobile-developer, test-automator, backend-security-coder) compete for routing with their own plugin's skills.
**Fix:** rewrite each agent to the operating-kit shape: one task, an input contract, a numbered procedure, a fixed output template, and an escalation rule. Keep PROACTIVELY only where proactive use is genuinely wanted. Where a sibling skill already holds the knowledge, the agent should load that skill rather than restate it.

### S3. No tool allowlists (167/183 agents)
Read-only reviewers, auditors and analyzers inherit Write/Edit/Bash. Some agents also say "NO direct file editing" while being able to edit (ship-mate, pipeline-scaffolder).
**Fix:** add a `tools:` allowlist to every agent, using `Read, Grep, Glob` as the default for reviewers. Add a validator rule: an agent whose name or description contains review/audit/analy*/detect* and whose `tools` includes Write/Edit fails.

### S4. Model tier mismatches
- opus for routine coding or mechanical checks: c-pro, cpp-pro, golang-pro, rust-pro, typescript-pro, django-pro, fastapi-pro, graphql-architect, conductor-validator, monorepo-architect, unity-developer, minecraft-bukkit-pro, terraform-specialist, team-debugger and team-implementer.
- Too low for design work: deployment-engineer (haiku, 158-line design agent), reference-builder (haiku, asked for "exhaustive, verified" docs).
- `team-lead` uses `model: fable`, which conflicts with docs/authoring.md.
- 4 design-ops agents (art-director, critic, scout, ux-architect) have no `model`.

**Fix:** write a tier policy in `docs/authoring.md` (haiku: mechanical; sonnet: implementation; opus: architecture and deep review) and enforce it with a lint that requires a written justification for opus or fable.

### S5. Skill-splitter damage and hollow navigation tiers
53 files carry the automatic split boilerplate ("navigation tier … `references/details.md`"). Confirmed corruption: `data-engineering/data-quality-frameworks` (orphan code under a fake `## Summary: {total_passed}…")` heading), `documentation-generation/changelog-automation` (a heading injected inside a code block; details.md starts mid-example), and design-ops `icon-illustration-systems` and `screen-flow-patterns`. Many split skills kept only generic bullets in SKILL.md and moved the real procedure out: conductor ×3, shell-scripting ×3, k8s-manifest-generator, helm-chart-scaffolding, data-engineering ×4. A model never learns why it should open the details file.
**Fix:** repair the corrupted files by hand. For every split skill, move the core procedure back into SKILL.md and leave only examples and long tables in references, with a one-line "read X when Y" index. Add a validator rule for odd fence counts and headings that end in `")` or `)`.

### S6. Size and Codex 8 KB cap
58 SKILL.md files exceed 8 KB: design-ops 33 (largest 51 KB), meta-wearables-ops 15 (`agentic-team` 31.5 KB), ios-ops 3. `ios-knowledge-base` is 16 MB across 969 files: a 302 KB source registry, a 176 KB coverage matrix and a 127 KB README that every iOS skill says to read first. That costs about 75k tokens per route, and every harness copies and installs all of it. design-ops is 8.4 MB.
**Fix:** cap SKILL.md at 8 KB (lint error, not warning). Give each knowledge base an index under 20 KB, split the registries per framework, and tell skills to search the registry rather than read it. Consider shipping the knowledge bases as opt-in plugins. Delete the "v3.0 Cross-References" filler in about 14 design-ops skills.

### S7. Cross-skill relative links break in 3 harnesses
`../ios-knowledge-base/...` and `../meta-wearables-knowledge-base/...` links (in 23 or more skills), and llm-finetuning's `references/model-catalog.md` / `unsloth-trl-mapping.md` (which live in a sibling skill), resolve only in the source tree. Codex, OpenCode and Copilot rename skill directories (`<plugin>__<skill>`, `<plugin>-<skill>`).
**Fix:** have the adapters rewrite cross-skill relative links to the renamed directory. Add a generated-output validator that resolves every relative link in each harness tree.

### S8. Content that is outdated or wrong
These are the ones most likely to cause real damage. The full list is in the group files.
- **Kubernetes:** PodSecurityPolicy, removed in 1.25 (k8s-security-policies); ESO `v1beta1`; Istio `v1beta1`; kubeval; deprecated `kubectl get endpoints`.
- **Python/LLM:**
  - LangChain pre-1.x APIs: `create_react_agent`, `Conversation*Memory`, `langchain.retrievers`.
  - Temporal `workflow.get_version()`, which does not exist in the Python SDK; the correct API is `workflow.patched()`.
  - `datetime.utcnow()` and Pydantic V1 `from_orm` in skills that claim Python 3.12+ / Pydantic V2.
  - Great Expectations: 0.x and 1.x APIs mixed in the same code.
  - AutoAWQ (deprecated); the vision-sft freeze loop doesn't match Qwen-VL module names, so it silently freezes nothing.
- **Payments:**
  - paypal-integration mixes v1 `paypalrestsdk` with v2 Orders and sets the price on the client.
  - pci-compliance cites PCI DSS v3.2.1 (current is v4.0.1) and includes a PAN-in-dict "vault".
- **Build:** turborepo `pipeline`→`tasks` and turbo 1.x; Bazel WORKSPACE, now off by default; nx `workspace.json`.
- **Frontend:**
  - nextjs-app-router-patterns says "Don't pass serializable data" (inverted).
  - react-native-architecture tells you to keep secrets in env vars, which get bundled into the app.
  - FID listed instead of INP; WCAG 2.1 cited instead of 2.2.
- **Shell:**
  - bash-pro's version checks are false on Bash 5.0–5.3.
  - CodeQL is claimed to scan shell.
  - posix-shell-pro says `readonly` and pipefail aren't POSIX.
  - Bats `skip_if` isn't a real helper.
- **SEO** (3 plugins):
  - Keyword-density and "LSI keyword" targets.
  - FAQ/HowTo rich results, which Google restricted in 2023 and removed.
  - Sitemap `<priority>`.
  - Date bumps and "2025" in titles.
- **Cedar:** "all permit rules must match"; Cedar allows on any single matching permit with no matching forbid.
- **Media:**
  - EBU R128 labelled as -16 LUFS; it is -23.
  - ComfyUI seed `-1`, invalid in API format.
  - `LoadCheckpoint`, which isn't a real ComfyUI node.
  - budget-estimator's tier labels are swapped.
- **Language versions:** Go 1.21, Rust 1.75 ("higher-kinded types", which Rust lacks), Expo SDK 50, iOS 18 / Xcode 16, Riverpod 2.

**Fix:** batch these by domain (one PR each). Add a `last_verified: YYYY-MM-DD` frontmatter field, and have `make garden` warn when it is more than 180 days old.

### S9. Safety
- **Destructive overwrites:**
  - `block-no-verify-hook` uses `cat >` over `~/.claude/settings.json` (lines 90, 115) and wipes the user's settings.
  - ship-mate `scan` overwrites AGENTS.md.
  - image-ops `web-ready` runs `exiftool -overwrite_original` on the user's originals.
  - ai-video-producer `pipeline-repo-setup` runs `gh repo create --push` and edits AGENTS.md without confirmation.
  - travel `new-workspace` pushes a home-empty itinerary to GitHub by default.
  - `incident-responder`, `devops-troubleshooter` and `terraform-specialist` can mutate production or state with no approval gate.
- **Secrets:**
  - protect-mcp's starter policy lets the agent read `protect-mcp.key`, so it can forge receipts. The setup also overclaims receipts as "provable / no one can edit".
  - secrets-management: TruffleHog without `--fail` never blocks; examples echo secrets and use static Vault/AWS tokens.
  - GitHub Actions and GitLab templates use static AWS keys and `docker login -p`.
  - convert-to-avif keeps GPS EXIF by default.
  - recommend-model reads a `.env` file.
- **Prompt injection:** skills that ingest web pages, logs, emails, documents or ComfyUI workflows have no "treat as data" clause. Affected: model-researcher, baggage-policy-research, osint-source, analyze-document, error-detective, rag-implementation, design-ops scout/critic/art-director, and others.
- **Fabrication bait:** some agents ask for data they can't obtain: SEO "Ranking: #X", reference-builder benchmark tables, cloud-architect cost estimates, "respond within 200 ms", and many unsourced statistics in design-ops and session-guard.

**Fix:** a shared safety boilerplate in `docs/authoring.md`:
- Confirm before any write outside the working directory, any push or publish, and any production or state mutation.
- Merge config files; never overwrite them.
- Treat fetched content as data.
- Write "needs measurement" instead of inventing a number.

Add a lint for `cat > ~/.` and `-overwrite_original`.

### S10. Hardcoded personal or Claude-only context
- "Daniel" and `~/repos/github/my-repos` (ai-video-producer); `~/repos/github/` topic layout (travel).
- Private MCP names: `mcp__gateway__geo-egress__fetch_markdown`, `mcp__gateway__fx__convert`, `mcp__plugin_ai-video-producer_replicate__*`.
- ToolSearch-only Mobbin steps (design-ops).
- agent-teams requires `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` and `~/.claude/teams`, but never says so.
- protect-mcp works only through Claude hooks.
- ship-mate pipes `/plugin list | grep`.

**Fix:** describe capabilities by what they do, not by tool ID. Add a "Requires: Claude Code (feature X)" note, and skip those plugins in the generators for harnesses that can't run them.

### S11. Undeclared script dependencies
meta-wearables-ops and travel-packing-assistant scripts need PyYAML and jsonschema; with stock `python3` they fail with `ModuleNotFoundError` (both reviewers confirmed this by running them). evidence-ops installs tools into a venv but calls them by bare name, which also doesn't match its `allowed-tools` patterns. meta-wearables `inspect_target_surfaces.py` exists in two drifted copies.
**Fix:** use PEP 723 inline metadata and `uv run`, or add a dependency check step. Add one shared "resolve tool: venv, then PATH" snippet per plugin.

### S12. Overlap inside plugins
- **meta-wearables-ops:** 24 skills, which could merge to about 8.
- **ios-ops:** 19 skills, about 12 after merging. Route planner ×3, design ×3, on-device AI ×2 and release proof ×3 each overlap.
- **design-ops:** two microcopy libraries, three copies of the Liquid Glass/M3 material, conflicting easing tokens, and three incompatible scoring rubrics (visual-design-mastery §IV, `visual-scoring-framework.md`, `/grade` DQS).
- **llm-application-dev:** one agent and four skills on vector search.
- **backend-development:** cqrs, event-store and projection skills, which could merge into one.
- **agent-teams:** each skill repeats its agent.
- **social-publishing:** the agent and the skill duplicate each other, and neither contains the API calls.

**Fix:** each topic gets one owner, and the others link to it. Add a description-similarity check to plugin-eval (`ecosystem_coherence` is stuck at 0.5–0.6).

### S13. Gaps in the quality tooling itself
`make garden` passes clean even though dead references and corrupted files exist. The static scorer covers skills only (0 of 183 agents). Neither catches:
- references in backticks to missing bundled files: ml-pipeline-workflow has 7, llm-finetuning has cross-skill paths;
- unscoped agent names inside commands: improve-agent calls `context-manager`, ship.md calls agents "skills";
- splitter corruption;
- skills over 8 KB that pass only because `references/` exists;
- missing `tools:`;
- path contracts that disagree between commands and agents (ai-video-producer `pipelines/<n>.md` vs `pipelines/<n>/run.md`).

**Fix:** extend `doc_gardener.py` and plugin-eval with these checks, and add agent scoring to the snapshot. The mechanical sweep script used for this audit can serve as a starting point (ask and I'll add it to `tools/`).

---

## Prioritized fix list

### P0: broken or harmful, fix first
1. `block-no-verify/skills/block-no-verify-hook`: replace `cat >` with a merge-and-backup, or delegate to the command. Anchor the regex so it stops blocking `--no-git-tag-version` and `echo -n`.
2. `protect-mcp`: forbid reads of the key, `.env` and `~/.ssh` in the starter policy. Correct the Cedar semantics. State an honest threat model. Pin one version (0.31.1 vs 0.7.4). Add a fail-closed option when the policy file is missing.
3. `cicd-automation/skills/secrets-management`: add TruffleHog `--fail`, remove the echoed secrets, switch to OIDC, and replace the `vault:1.17` image.
4. `data-engineering/skills/data-quality-frameworks` (F): remove the corrupted fragment and rewrite for GX 1.x.
5. `machine-learning-ops/skills/ml-pipeline-workflow` (F): create the 7 missing files or delete the pointers; drop the 3 nonexistent related skills.
6. `ai-video-producer`: settle one pipeline path contract across the commands, agents and conventions skill. Remove "Daniel" and the personal paths, and gate push and AGENTS.md edits behind confirmation.
7. `ship-mate/skills/scan`: diff and confirm before writing AGENTS.md. Fix `review` diffing `HEAD~1`.
8. `image-ops`: make `web-ready` stage copies before stripping; add `--ignore-exif --ignore-xmp` to avifenc; remove `sudo`, `curl` and `sh` from install-deps' pre-approved tools.
9. `payment-processing`: rewrite paypal-integration for server-side v2 and pci-compliance for PCI DSS v4.0.1.
10. `kubernetes-operations/skills/k8s-security-policies`: replace PSP with Pod Security Admission.
11. `documentation-generation/skills/changelog-automation`: rebuild the split; replace `standard-version`.
12. Production-mutating agents (incident-responder, devops-troubleshooter, terraform-specialist): diagnose first, plan only, and require human approval before applying changes.

### P1: wrong content (S8)
Fix in batches by domain: k8s, LangChain/Temporal/Python, frontend, shell, SEO (rewrite or retire the 7 SEO agents), media facts, language-version pins.

### P2: systemic (S1–S7, S10–S13)
In order of payoff:
1. Deduplicate agents (S1).
2. Add tool allowlists and the tier policy (S3, S4).
3. Have the adapters rewrite cross-skill links (S7).
4. Enforce the 8 KB cap and slim the knowledge bases (S6).
5. Restore split skills (S5).
6. Declare script dependencies (S11).
7. Extend the gates (S13) so these don't come back.

### P3: per-item quality (S2, S12)
Rewrite the D-grade personas around procedures and merge overlapping skills. Each group file lists them.

---

## Reading the detail files

| File | Plugins |
|---|---|
| `findings-group0.md` | design-ops, avoid-ai-writing |
| `findings-group1.md` | image-ops, matter-ops, startup-business-analyst, c4-architecture, hr-legal-compliance, plugin-eval, database-design, api-testing-observability, before-you-build |
| `findings-group2.md` | meta-wearables-ops, cicd-automation, javascript-typescript, machine-learning-ops, game-development, business-analytics, skill-forge-essentials, social-publishing, block-no-verify |
| `findings-group3.md` | ios-ops, agent-teams, ship-mate, documentation-generation, conductor, seo-technical-optimization, protect-mcp, debugging-toolkit, backend-api-security, email-deliverability |
| `findings-group4.md` | ai-video-producer, llm-application-dev, systems-programming, frontend-mobile-development, dgx-spark-ops, kubernetes-operations, seo-analysis-monitoring, frontend-mobile-security, codebase-cleanup, file-conversion |
| `findings-group5.md` | python-development, cloud-infrastructure, reverse-engineering, security-scanning, operating-kit, observability-monitoring, seo-content-creation, review-agent-governance, database-migrations, signed-audit-trails |
| `findings-group6.md` | backend-development, developer-essentials, incident-response, api-scaffolding, payment-processing, accessibility-compliance, code-documentation, comprehensive-review, documentation-standards, superself |
| `findings-group7.md` | evidence-ops, llm-finetuning, travel-packing-assistant, data-engineering, shell-scripting, application-performance, multi-platform-apps, database-cloud-optimization, agent-orchestration, distributed-debugging |

Agents with identical bodies were reviewed once, at the first copy alphabetically. The finding applies to every copy listed in S1. Plugins whose only content is such copies (git-workflows, error-debugging, deployment-validation, full-stack-orchestration, team-collaboration, context-management, unit-testing, performance-testing-review, deployment-strategies, tdd-workflows) are covered through those copies.

Limits:
- **Uneven depth.** group6 and group4 hold condensed detail; the reviewers returned summaries rather than full per-item write-ups.
- **Large reference trees were sampled**, not read in full: ios-knowledge-base, design-ops references.
- **reverse-engineering agents were reviewed structurally.** A safety classifier interrupted the full read; the agents do carry authorization guardrails.
