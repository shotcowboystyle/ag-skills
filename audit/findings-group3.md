# Audit findings — group 3

Plugins: ios-ops, agent-teams, ship-mate, documentation-generation, conductor, seo-technical-optimization, protect-mcp, debugging-toolkit, backend-api-security, email-deliverability

Paths relative to plugins/. Grades A–F per item; severity high/med/low; each issue carries a recommended fix.

# Full findings (group 3)

Paths are relative to `plugins/`. Line numbers refer to the source file.

## ios-ops
- **Four overlap groups among 19 skills.**
  - Route planning: `apple-sdk-route`, `ios-capability-route-planner`, and the intake and route roles in `ios-agentic-apple-engineering-team`.
  - Design: `swiftui-native-design` and `liquid-glass-design` are subsets of `ios-native-design-verification`, which repeats their text almost word for word.
  - AI: `on-device-ai-feature` and `ios-on-device-intelligence-evaluation` cover the same ground.
  - Release proof: `ios-device-release-proof`, `ios-privacy-performance-release-proof` and `ios-testing-and-release-assurance` each ship a near-identical 7-row evidence ladder and report template.
  - Fix: keep one skill per group (planner, native-design-verification, intelligence-evaluation, testing-and-release-assurance). Keep privacy-performance only for privacy manifests and required-reason APIs. That leaves about 12 skills.
- **Links break in 3 of 7 tools.** Every skill links `../ios-knowledge-base/references/...`, and all of those resolve in the source tree. But Codex copies skills to `ios-ops__<skill>`, OpenCode to `ios-ops-<skill>` and Copilot to `ios-ops__<skill>`, so the relative path no longer points anywhere. The knowledge base's own note (lines 10-12) only helps if the model reads it first. Fix: have the generators rewrite these links to the renamed folder.
- **`allowed-tools: Read, Grep, Glob` on every skill is misleading.** The bodies tell the agent to implement, compile and patch files. In Claude Code this field pre-approves tools rather than restricting them. Fix: remove it, or list the tools the steps actually need.

### ios-ops/skills/apple-sdk-route/SKILL.md — Grade: C
- [sev: high] Duplicates `ios-capability-route-planner`: same deliverable, and the triggers collide (line 3). Fix: delete it and fold its "Refuse to assume" list (lines 42-50) into the planner.
- [sev: med] Lines 17-18 send the agent to the 127 KB README, the 72 KB framework catalog and the 302 KB source registry (about 75k tokens). Fix: point at a small per-framework index, and say to search the registry for the framework name instead of reading it.
- [sev: low] The description repeats itself.

### ios-ops/skills/ios-agentic-apple-engineering-team/SKILL.md — Grade: C
- [sev: high] Tries to cover everything. The description (line 3) claims every lane, so it will win routing over every specialist skill. Fix: limit the trigger to work that spans 3 or more specialist areas.
- [sev: med] Lines 174-192 "Open-source bundle boundary" is maintainer guidance about packaging `.skill` files, a flow this repo doesn't use. Fix: move it to `docs/` or delete it.
- [sev: med] The 10 role descriptions (lines 44-71) restate the specialist skills. Fix: replace them with a table of role, skill and stop condition.
- [sev: low] Lines 106-131 are another copy of the evidence ladder. Fix: link the single shared one.

### ios-ops/skills/ios-capability-route-planner/SKILL.md — Grade: B
- [sev: med] Lines 17-21 send the agent to 5 index files plus the 302 KB registry and the 168 KB availability matrix. Fix: search them for the chosen framework instead.
- [sev: low] The description is over 640 characters. Fix: trim it to pre-implementation planning.

### ios-ops/skills/ios-commerce-identity-and-security/SKILL.md — Grade: B
- [sev: low] Wide trigger: StoreKit, Pay, Wallet, Sign in with Apple, Keychain, LocalAuthentication, CryptoKit and App Attest. Fix: optionally split commerce from identity and secrets.
- [sev: low] No concrete StoreKit 2 names (`Transaction.currentEntitlements`, `Transaction.updates`, `VerificationResult`). Fix: add a short cheat sheet.

### ios-ops/skills/ios-companion-communications/SKILL.md — Grade: B
- [sev: low] Line 33 says to report VoIP calls to CallKit "quickly" without the hard rule: report from inside the PushKit delegate or the app is terminated. Fix: state the rule.
- [sev: low] Inherits the broken-link problem in Codex, OpenCode and Copilot.

### ios-ops/skills/ios-data-and-device-services/SKILL.md — Grade: B
- [sev: med] Covers 10 frameworks (line 3). Fix: split into persistence/sync and protected-data/accessories.
- [sev: low] `ModelActor` (line 38) needs a deployment-target check. Fix: mark it `to-verify`.

### ios-ops/skills/ios-device-release-proof/SKILL.md — Grade: C
- [sev: high] The evidence ladder (lines 23-31) and report (lines 63-76) nearly copy `ios-privacy-performance-release-proof` (lines 15-44). Fix: merge into `ios-testing-and-release-assurance` and keep the route-specific gates (lines 50-59) as a reference file.

### ios-ops/skills/ios-knowledge-base/SKILL.md — Grade: D
- [sev: high] 16 MB in 969 markdown files. The largest are the source registry (302 KB), coverage matrix (176 KB), availability matrix (168 KB) and the README "map" (127 KB). Every tool's generated copy duplicates all of it, and `gh skill install` / `npx skills add` download it on every install. Fix: an index under 20 KB as the entry point, split the registry per framework, and consider an opt-in plugin.
- [sev: med] Leftovers from the build process: 139 internal task IDs (T194, T202, T226…), and coverage-matrix line 200 describes "portable `.skill` archives". Fix: strip them.
- [sev: med] Off-topic content: a Meta Wearables snapshot (registry line 43). Fix: remove it.
- [sev: med] Out of date: skills call "iOS 26" current, while 31 knowledge-base files already mention iOS 27 or WWDC 2026. Fix: say "current SDK, last verified against iOS 26 on <date>".
- [sev: low] It can be auto-picked for general iOS questions. Fix: mark it reference-only (`user-invocable: false`) or give it a narrow trigger.

### ios-ops/skills/ios-media-ml-and-inputs/SKILL.md — Grade: B
- [sev: med] Overlaps the AI evaluation skill on Vision, Core ML and Natural Language. Fix: this skill owns capture, NFC and music; model evaluation goes to the AI skill.

### ios-ops/skills/ios-native-design-verification/SKILL.md — Grade: C
- [sev: high] Covers everything in `swiftui-native-design` and `liquid-glass-design`; lines 19-20 repeat `liquid-glass-design` lines 16-18. Fix: make this the only design skill.
- [sev: low] Lines 15-32 repeat themselves. Fix: shorten.

### ios-ops/skills/ios-on-device-intelligence-evaluation/SKILL.md — Grade: C
- [sev: high] Duplicates `on-device-ai-feature`, and line 13 tells the agent to read it anyway. Fix: merge.
- [sev: low] No concrete Foundation Models names (`SystemLanguageModel.default.availability`, `@Generable`, `LanguageModelSession`). Fix: add them.

### ios-ops/skills/ios-privacy-performance-release-proof/SKILL.md — Grade: C
- [sev: high] Third copy of the evidence ladder. Its unique value, privacy manifests and required-reason APIs, is buried. Fix: narrow it to `PrivacyInfo.xcprivacy`, required-reason APIs and App Store privacy labels.
- [sev: low] Description is about 600 characters.

### ios-ops/skills/ios-project-target-architect/SKILL.md — Grade: B
- [sev: low] Only steps 3-5 of the 12 are specific to this skill. Fix: compress steps 1, 10 and 12.

### ios-ops/skills/ios-source-refresh-and-availability/SKILL.md — Grade: D
- [sev: high] A maintainer skill for the knowledge base, shipped to users ("refresh the `.skill` archive", lines 48 and 76) with a broad trigger. Fix: move it out of the distributed plugin, or rewrite it around this repo's `make validate` and `make garden`.
- [sev: med] Its steps require patching files and type-checking (lines 39-49), but it declares read-only tools (line 4). Fix: make them match.
- [sev: low] Sources list only Swift.org. Fix: add Apple's developer documentation.

### ios-ops/skills/ios-spatial-graphics-and-games/SKILL.md — Grade: B
- [sev: low] Broad but consistent. Fix: optionally split games from spatial.

### ios-ops/skills/ios-system-surfaces-and-background/SKILL.md — Grade: B
- [sev: low] `BGContinuedProcessingTask` (line 28) is iOS 26+. Fix: add an availability check.

### ios-ops/skills/ios-testing-and-release-assurance/SKILL.md — Grade: B
- [sev: med] Make this the main proof skill. Fix: absorb the device-proof gates into `references/release-audit.md`.
- [sev: low] Links to knowledge-base files numbered 144 and 172 show how the reference tree has sprawled.

### ios-ops/skills/liquid-glass-design/SKILL.md — Grade: C
- [sev: high] Subset of `ios-native-design-verification`. Fix: merge.
- [sev: low] Calls iOS 26 current (line 7).

### ios-ops/skills/on-device-ai-feature/SKILL.md — Grade: C
- [sev: high] Duplicate of `ios-on-device-intelligence-evaluation`. Fix: merge.

### ios-ops/skills/swiftui-native-design/SKILL.md — Grade: C
- [sev: high] Subset of `ios-native-design-verification`, and the triggers collide. Fix: merge.

## agent-teams
- **Only works in Claude Code with the experimental Agent Teams feature**, but the skills never say so. It relies on TeamCreate, SendMessage, TaskCreate, `~/.claude/teams` and `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`. Fix: add a requirement note and a fallback (run the passes one after another), or don't generate it for other tools.
- **Agents and skills repeat each other**: `parallel-debugging` repeats `team-debugger`, and `team-reviewer` repeats `review-dimensions.md`. Fix: the agents keep the procedure, the skills keep only the lead's coordination.

### agent-teams/agents/team-debugger.md — Grade: B
- [sev: low] `opus` for one hypothesis, with 3 or more running in parallel. Fix: use `sonnet`.
- [sev: low] Reproduction step with Bash has no limit on side effects. Fix: "read-only commands unless the lead approves".

### agent-teams/agents/team-implementer.md — Grade: B
- [sev: low] `opus` for scoped work. Fix: use `sonnet`.
- [sev: low] Doesn't require reporting the verification commands it ran. Fix: require commands and output in the completion message.

### agent-teams/agents/team-lead.md — Grade: C
- [sev: med] `model: fable` for coordination contradicts `docs/authoring.md` and costs about 2.6× Opus. Fix: use `opus`.
- [sev: med] The lead "owns shared files" (line 64) but has no Write or Edit tool (line 4). Fix: add the tools, or give each shared file to one implementer.
- [sev: low] The capability list (lines 15-57) has no decision rules. Fix: link `team-composition-patterns`.
- [sev: low] "Configure display modes" (line 22) is a user setting. Fix: remove.

### agent-teams/agents/team-reviewer.md — Grade: B
- [sev: med] Cites WCAG 2.1 AA (line 63); 2.2 has been current since October 2023. Fix: update.
- [sev: low] Has Bash without a "no mutating commands" rule.

### agent-teams/skills/multi-reviewer-patterns/SKILL.md — Grade: B
- [sev: low] "Use the higher severity" (line 37) conflicts with its own calibration rules. Fix: re-derive severity from the impact and likelihood table.

### agent-teams/skills/parallel-debugging/SKILL.md — Grade: B
- [sev: low] No rule for how many hypotheses to spawn or when to stop. Fix: add both.

### agent-teams/skills/parallel-feature-development/SKILL.md — Grade: B
- [sev: low] Multi-branch strategy with no worktree advice. Fix: recommend one git worktree per implementer.

### agent-teams/skills/task-coordination-strategies/SKILL.md — Grade: C
- [sev: med] Its decomposition strategies duplicate `parallel-feature-development`, and the triggers collide. Fix: merge.
- [sev: low] Claude-specific TaskCreate/TaskUpdate pseudo-calls (lines 64-69). Fix: describe the actions in prose.

### agent-teams/skills/team-communication-protocols/SKILL.md — Grade: C
- [sev: med] Hard-codes undocumented message formats (`shutdown_request`, `plan_approval_response`) and `~/.claude/teams` paths that will likely change. Fix: keep the communication rules and link the official docs.
- [sev: low] The `request_id` troubleshooting entry (lines 126-127) is a guess. Fix: remove unless verified.

### agent-teams/skills/team-composition-patterns/SKILL.md — Grade: C
- [sev: med] `teammateMode: "iterm2"` (line 78) is probably not a valid value. As I recall the documented values are auto, in-process and tmux, but this needs checking against the docs. The README's default also conflicts. Fix: correct both.
- [sev: low] Names Claude-only built-in agents (`Explore`, `Plan`, `general-purpose`). Fix: add a portability note.

## ship-mate
- **Agent names aren't plugin-scoped** (`architect`, `implement`, `orchestrate`, `playwright`, `qa`, `review`), which breaks the authoring rule. Fix: `ship-mate-<name>`.
- **`ship.md` lines 113-170 say "invoke the X skill"** but these are agents; only `scan` is a skill. The agents also call the `ship` command a skill. Fix: delegate to the named agents.
- **No trigger phrases and no tool allowlists**, while several agents claim "NO direct file editing". Fix: add triggers; give read-only roles Write limited to their own report file.
- **Every task resets the stage to `scan`** (`ship.md` line 179), so each task re-scans the project. Fix: scan once per story.

### ship-mate/agents/orchestrate.md — Grade: C
- [sev: high] Asks the user questions one at a time (line 36) from inside a subagent, which can't hold that conversation. Fix: run this stage in the main session, or return the questions and stop.
- [sev: med] FRONTEND or BACKEND, never both (line 29), so full-stack tasks skip the Playwright stage. Fix: add `FULLSTACK`.
- [sev: low] "25 years of experience" persona. Fix: delete.

### ship-mate/agents/architect.md — Grade: C
- [sev: med] Writes the plan and state files while claiming no file editing, and has no tools field. Fix: allow Write only to `.claude/pipeline/`.
- [sev: med] `model: inherit` for the planning gate, and no trigger. Fix: `opus` and "Use when…".

### ship-mate/agents/implement.md — Grade: C
- [sev: med] "Halt and flag the reviewer" (line 20) has no channel or state flag behind it. Fix: set `flags.security_review_required` and stop.
- [sev: med] "Proceeding with adjustment unless instructed otherwise" (line 39) silently departs from an approved plan. Fix: stop for approval when files or scope change.
- [sev: low] MERN-specific branch (line 48). Fix: leave stack rules to AGENTS.md.

### ship-mate/agents/review.md — Grade: C
- [sev: high] Reviews `git diff HEAD~1` (line 42), but implement never commits, so it reviews the previous commit. Fix: diff the working tree against a base commit recorded in state.
- [sev: med] "Should Fix" items are supposed to go back to the developer, but no loop exists for them. Fix: route them through `stage=implement`.
- [sev: low] Flags vulnerable dependencies without running a scanner. Fix: name `npm audit` or `pip-audit`.

### ship-mate/agents/qa.md — Grade: C
- [sev: med] "Verify no authentication bypass" (lines 57-59) isn't testable as written. Fix: concrete checks (unauthenticated request gets 401/403, another user's ID gets 403).
- [sev: med] Overlaps Playwright on UI acceptance criteria. Fix: QA does unit, integration and API only.
- [sev: low] Coverage percentage with no command to measure it. Fix: run the tool or write "not measured".

### ship-mate/agents/playwright.md — Grade: C
- [sev: med] The sample page object (lines 43-58) won't compile in strict TypeScript: no `Page` import, undeclared fields. Fix: declare `readonly` `Locator` fields and import the types.
- [sev: med] Always waits for `networkidle` (line 83), which Playwright discourages. Fix: use `expect(locator).toBeVisible()`.
- [sev: med] Starts a dev server (line 27) and never stops it. Fix: use `webServer` in `playwright.config.ts`.
- [sev: low] Manual screenshots on failure. Fix: `screenshot: 'only-on-failure'` in the config.

### ship-mate/skills/scan/SKILL.md — Grade: D
- [sev: high] Writes AGENTS.md (line 78) whenever `project-doc.md` is missing (lines 23-25), overwriting an existing or symlinked AGENTS.md. Fix: if it exists, show a diff and require confirmation.
- [sev: med] Checks plugins with `/plugin list | grep` (lines 10-11); you can't pipe a slash command, and other tools have no `/plugin`. Fix: check by name, or use the fallback.
- [sev: med] Says "use `understand-anything`" (line 27) right after calling it optional. Fix: write two explicit branches.
- [sev: med] The delta scan uses `git diff HEAD~1` (line 71), missing uncommitted and older changes. Fix: diff against the last scanned commit.
- [sev: low] Coverage percentage is a guess unless measured.

## documentation-generation
- `reference-builder` overlaps `api-documenter` (not in this group).

### documentation-generation/agents/mermaid-expert.md — Grade: C
- [sev: med] "Test rendering" (line 25) with no tool to do it. Fix: run `npx -y @mermaid-js/mermaid-cli` when a shell is available, otherwise say it wasn't rendered.
- [sev: low] Missing newer diagram types (mindmap, architecture-beta, block, sankey, C4).
- [sev: low] Always produces two versions. Fix: styled version only on request.

### documentation-generation/agents/reference-builder.md — Grade: C
- [sev: med] `haiku` for "exhaustive, verified" reference docs. Fix: `sonnet`.
- [sev: med] Asks for benchmark and rate-limit tables (lines 18 and 78) without measuring anything, which invites invented numbers. Fix: include only sourced or measured values.
- [sev: low] A 180-line list of capabilities. Fix: four steps (inventory, extract, verify, format) and one template.

### documentation-generation/skills/architecture-decision-records/SKILL.md — Grade: B
- [sev: low] The lifecycle diagram shows Accepted → Deprecated → Superseded as one chain (lines 29-33); they're separate branches.
- [sev: low] "2 senior engineers reviewed" (line 96) is team-policy filler.

### documentation-generation/skills/changelog-automation/SKILL.md — Grade: D
- [sev: high] The automatic split inserted a heading inside the Keep a Changelog code block (lines 23-70). The block now holds a release-notes example, and `references/details.md` starts mid-example with stray braces. Fix: rebuild both by hand.
- [sev: med] "Don't manual edit — generated changelogs only" (line 76) contradicts Keep a Changelog's own guidance. Fix: generate a draft, then a person edits it.
- [sev: med] Recommends `standard-version` (details lines 82-160), which is deprecated. Fix: release-please or git-cliff.

### documentation-generation/skills/openapi-spec-generation/SKILL.md — Grade: C
- [sev: med] Says "Don't forget nullable" (line 64) and uses `nullable: true` (details line 231). OpenAPI 3.1 removed `nullable`. Fix: `type: [string, "null"]`.
- [sev: low] Little guidance in SKILL.md itself: no design-first vs code-first rule and no lint command. Fix: add a short workflow with `npx @redocly/cli lint` and link both reference files directly.

## conductor
- **All three skills hold almost nothing.** Each SKILL.md is 36-41 lines of generic bullets, and every step lives in 350-590-line details files. Fix: move the core procedure into each SKILL.md.
- **The validator isn't wired in.** No command calls it. Fix: run it after setup and before implement.

### conductor/agents/conductor-validator.md — Grade: C
- [sev: med] Expects `<type>_<name>_<YYYYMMDD>` track IDs (lines 71 and 170). The real format is `{shortname}_{YYYYMMDD}` (`commands/new-track.md` line 158), so every real track gets flagged. Fix: align it.
- [sev: med] `opus` for a mechanical check. Fix: `haiku` or `sonnet`.
- [sev: low] "Use Glob/Read/Grep" (lines 85-88) is Claude tool wording.
- [sev: low] The sample report's "Backend" section isn't in its own required list.

### conductor/skills/context-driven-development/SKILL.md — Grade: C
- [sev: med] Too little in SKILL.md, and `artifact-templates.md` is only linked from the details file. Fix: add the greenfield/brownfield rule and link the templates.
- [sev: low] Overlaps the `/conductor:setup` command.

### conductor/skills/track-management/SKILL.md — Grade: C
- [sev: med] The ID format and status markers the validator depends on live only in the details file. Fix: put them in SKILL.md.

### conductor/skills/workflow-patterns/SKILL.md — Grade: C
- [sev: med] The TDD and commit loop, including `git notes`, is buried in details. Fix: move it into SKILL.md.
- [sev: low] "Wait for approval" (line 30) isn't defined for tools without a live user.

## seo-technical-optimization
- **Covers only on-page copy and markup** despite "technical" in the name. Fix: rename it, or add a technical-SEO audit agent.
- **No tool allowlists.** Fix: `Read, Grep, Glob`.
- **Some deliverables need data the agents can't fetch** (competitor and position analysis), which invites made-up results. Fix: drop them, or require web tools and cited sources.

### seo-technical-optimization/agents/seo-keyword-strategist.md — Grade: D
- [sev: high] Built on keyword density targets of 0.5-1.5% (line 17) and "20-30 LSI keywords" (lines 41 and 47). Google has said density isn't a ranking factor and that "LSI keywords" don't exist. Fix: rewrite around search intent and topic coverage.
- [sev: low] "Voice search" filler.

### seo-technical-optimization/agents/seo-meta-optimizer.md — Grade: C
- [sev: med] Recommends special characters (✓ ★), emotional triggers and adding the year (lines 25 and 32), which are clickbait tactics. Fix: accurate, page-specific summaries.
- [sev: low] "Helmet" for Next.js is outdated. Fix: the App Router `metadata` API.

### seo-technical-optimization/agents/seo-snippet-hunter.md — Grade: D
- [sev: high] Recommends FAQ and HowTo markup for rich results. Google restricted FAQ results to government and health sites in 2023 and removed HowTo results. Fix: drop or label them.
- [sev: med] Overlaps `seo-structure-architect`. Fix: merge.

### seo-technical-optimization/agents/seo-structure-architect.md — Grade: C
- [sev: med] Recommends sitemap `<priority>` (line 65), which Google ignores, and lists FAQ/HowTo as high-impact (lines 31-32). Fix: remove both.
- [sev: low] No concrete internal-linking rule.

## protect-mcp
- **Two package versions:** the policy check runs `protect-mcp@0.31.1` while signing runs `@0.7.4`. Fix: pin one, or explain why.
- **Claude Code only** (it uses hooks), but the descriptions don't say so.
- **`npx` runs twice on every tool call.** The latency hasn't been measured. Fix: recommend a local install.

### protect-mcp/agents/policy-enforcer.md — Grade: C
- [sev: high] Misstates Cedar's rules: "all permit rules must match" (line 18). Cedar allows a request when any one permit matches and no forbid does. Fix: correct it.
- [sev: high] The example policies allow `cat*` and unrestricted Read, so the agent can read `protect-mcp.key` and forge receipts. Fix: forbid reading the key, `.env` files and `~/.ssh`.
- [sev: med] Allows `terraform apply*` but forbids `-auto-approve` (lines 251 and 268), so apply hangs on an interactive prompt. Fix: allow only `terraform apply <planfile>`.
- [sev: low] No tool allowlist.

### protect-mcp/agents/receipt-verifier.md — Grade: B
- [sev: med] Takes pasted JSON and user-supplied paths with no note that they're data, not instructions. Fix: add that note and quote paths.
- [sev: low] Version mismatch (0.7.4 vs 0.31.1).
- [sev: low] No tool allowlist.

### protect-mcp/skills/protect-mcp-setup/SKILL.md — Grade: C
- [sev: high] Overclaims. Its "provable / no one can edit it" table (lines 185-188) doesn't hold: receipts record only the tool name, with no input or output (`decision: allow`, `policy_digest: none`). They aren't chained, so deleted lines go unnoticed. The key is self-signed and sits in a file the starter policy lets the agent read. Fix: an accurate threat model, plus a forbid on the key file.
- [sev: med] Without a policy file, every call is allowed. Fix: a fail-closed option.
- [sev: med] The install command (line 44) isn't valid. Fix: `/plugin marketplace add shotcowboystyle/ag-skills`, then `/plugin install protect-mcp@claude-code-workflows`.
- [sev: low] Leaving the `/path/to/project/*` placeholder in place silently denies all writes.
- [sev: low] Integration and PR marketing text.

## debugging-toolkit
- `dx-optimizer` doesn't belong in this plugin.

### debugging-toolkit/agents/debugger.md — Grade: C
- [sev: med] Trigger "any issues" collides with every other debugger. Fix: scope it to a single failing test or error.
- [sev: med] Adds debug logging without removing it afterwards. Fix: require cleanup.
- [sev: low] No regression test required. Fix: add one.
- [sev: low] No output format and no tools field.

### debugging-toolkit/agents/dx-optimizer.md — Grade: D
- [sev: med] A generic list with unmeasurable goals ("onboarding under 5 minutes", "developer satisfaction"). Fix: concrete steps — time a clean clone, install and test run, then propose the top 3 cuts.
- [sev: med] Delivers `.claude/commands/`, which only Claude Code reads. Fix: Makefile or package scripts.
- [sev: low] Wrong plugin; the trigger collides with scaffolding agents.

## backend-api-security

### backend-api-security/agents/backend-security-coder.md — Grade: D
- [sev: high] A persona covering everything: about 60 bullets (lines 13-77) and no procedure. Its response steps (lines 100-109) set up MFA on every task. Fix: a backend request-path checklist (authorization on every handler, parameterized queries, input limits, SSRF allowlist, secret handling, error leakage) with findings and a diff.
- [sev: med] Outdated advice: X-Frame-Options instead of CSP `frame-ancestors`, and TLS certificate pinning for backend clients.
- [sev: low] Points to a `security-auditor` that isn't in this plugin.
- [sev: low] No tools field and an overlapping trigger.

## email-deliverability
- Low-severity notes only. `evals/evals.json` contains what look like real personal domains; replace them with `example.*`. On domains with a wildcard DKIM record, the audit script reports every selector it probes as "revoked key"; detect the wildcard once and say so.

### email-deliverability/skills/email-dns-setup/SKILL.md — Grade: A
- No material issues. The script passes `bash -n` and shellcheck, and ran correctly against example.com.

## Group summary
Top 10 fixes and grade counts are at the top of this message.