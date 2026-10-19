# Audit findings — group 2

Plugins: meta-wearables-ops, cicd-automation, javascript-typescript, machine-learning-ops, game-development, business-analytics, skill-forge-essentials, social-publishing, block-no-verify

Paths relative to plugins/. Grades A–F per item; severity high/med/low; each issue carries a recommended fix.

# Audit findings, group 2

Paths are relative to `plugins/`. Line numbers refer to the file under each heading.

## meta-wearables-ops

- **Overlap:** 24 skills for one SDK family. Every skill restates the same evidence-ladder, "never map Gen 3" and no-secrets rules ("Gen 3" appears 47 times). Merge candidates:
  - {meta-dat-api-atlas, meta-dat-android-api-atlas, meta-wearables-full-sdk-audit}
  - {debugging-observability, operational-readiness, device-compatibility}
  - {on-device-compliance, privacy-publishing, security-attestation}
  - {android-integration, android-api-atlas}
- **Size:** 15 of 24 SKILL.md files are over the Codex 8 KB cap (agentic-team 31.5 KB, full-sdk-audit 16.9 KB, security-attestation 14.7 KB, device-proof 14.3 KB, implementation-recipes 13.0 KB, the rest 8.3–11.2 KB). They pass the lint only because a `references/` folder exists, so Codex still truncates them. Most of the bulk is "Read before acting" lists with 6–40 links each.
- **Scripts:** they `import yaml` but don't declare PyYAML, so `python3 scripts/validate_team_manifest.py` fails with `ModuleNotFoundError`. It passes under `uv run --with pyyaml`. The skills say to run `python3 scripts/...` "in the workspace", which only works from the skill directory. `inspect_target_surfaces.py` has two drifted copies (agentic-team and device-proof). The README "## Commands" section is empty.

### meta-dat-android-api-atlas — Grade C
- [med] Overlaps android-integration: duplicate 0.9 migration lists (L61-77 vs L54-67), the same artifacts and boundaries, and the same triggers. Fix: merge, or narrow the description to symbol and artifact lookup only.
- [med] 10.3 KB. Fix: move "Capability lanes" and the migration list to references.
- [low] L52 asks to resolve `Session`/`DeviceSession` from the artifact, but `allowed-tools: Read, Grep, Glob` pre-approves no Gradle command. Fix: add `Bash(./gradlew *)`, or say the user runs the compile.
- [low] 5 knowledge-base docs and 6 URLs must be read even on the fast path. Fix: let the fast path skip them.

### meta-dat-android-integration — Grade C
- [med] Duplicates the atlas (see above). Fix: merge.
- [med] 9.9 KB with 13 "Read" bullets (L16-33). Fix: keep 3 conditional links.
- [low] L64-66 "current examples contain 0.8.0 coordinates" is an undated claim. Fix: date it, or move it to the source log.

### meta-dat-api-atlas — Grade B
- [med] The name hides that it is iOS-only and collides with the Android atlas and full-sdk-audit ("broader SDK coverage"). Fix: rename to `meta-dat-ios-api-atlas` and narrow the trigger.
- [low] L35 "Read the relevant local Apple route" points to nothing. Fix: link a real file or delete the line.

### meta-dat-camera-audio — Grade B
- [low] The description is framed for iOS/AVFoundation, but the body links Android starters and has no Android audio route. Fix: state the scope or add the route.
- [low] L22 has 0.9.0 symbols inline. Fix: keep version-specific symbols only in references.

### meta-dat-display — Grade B
- [low] L72 links an external repo (`ios-ops-plugin`) that isn't in this marketplace. Fix: remove it or mark it optional.
- [low] Overlaps input-sensors on ButtonGroup. Fix: point input handling there.

### meta-dat-ios-integration — Grade B
- [med] L23 hardcodes commit SHAs and the "2026-08-22 refresh". Fix: move them to the knowledge-base sources registry.
- [low] It writes code but pre-approves no xcodebuild or swift commands. Fix: add them, or drop `allowed-tools`.

### meta-wearables-agentic-team — Grade D
- [high] 31.5 KB: about 40 Read/Load/Run bullets (L21-61), a 22-role list and an 18-section required output (L122-141). Codex keeps about a quarter of it, and it costs roughly 8k tokens before any work starts. Fix: make it a ≤150-line router, move roles and receipts to references, and require 4–5 output sections.
- [high] The four scripts it requires need PyYAML and only resolve from the skill directory. Fix: declare the dependency, use skill-relative paths, and give a no-script fallback.
- [med] Kitchen-sink lead role (22 local roles plus 32 upstream). Fix: limit it to routing and final reconciliation.
- [low] The `Bash(python3 *)` syntax is Claude-only. Fix: also give the command in prose.

### meta-wearables-app-architecture — Grade C
- [med] Overlaps agentic-team (playbook selection, step 10), implementation-recipes and full-sdk-audit. Fix: limit it to domain/adapter boundary design.
- [med] 10 KB with an 11-item output. Fix: trim to diagram, interfaces, state machine and fallback.

### meta-wearables-debugging-observability — Grade B
- [med] L38-57 hardcodes MCP tool names (`get_dat_readiness`, `export_diagnostic_bundle` and others) with no source and no fallback when the server is missing. Fix: cite the source and add a logs/state-stream branch.
- [med] Its trigger collides with operational-readiness. Fix: merge, or split into live diagnosis vs release readiness.
- [low] 10 KB. Fix: move the anchors and redaction rules to references.

### meta-wearables-developer-operations — Grade B
- [low] Its identity map duplicates security-attestation's. Fix: keep a single map in the knowledge base.
- [low] The mutation guard appears twice (L149, L228). Fix: keep one.

### meta-wearables-device-compatibility — Grade B
- [med] The tuple-freezing step overlaps device-proof and operational-readiness. Fix: make this the single owner.
- [low] Its validator needs PyYAML. Fix: declare it.

### meta-wearables-device-proof — Grade C
- [med] 14.3 KB, and it ships the drifted duplicate inspector. Fix: keep one copy here.
- [med] The 375-line preflight runners have no example invocation. Fix: add usage lines.
- [low] L372-374 has a dated source-conflict note. Fix: move it to the knowledge base.

### meta-wearables-full-sdk-audit — Grade D
- [high] 16.9 KB with about 30 required-output items (L90-127). Its trigger overlaps 5 siblings. Fix: produce one coverage matrix with 6–8 fields.
- [med] Steps 8-10 restate the compliance, readiness and architecture skills. Fix: replace them with links.
- [med] Its scripts need PyYAML. Fix: declare it.

### meta-wearables-implementation-recipes — Grade C
- [med] 13 KB, with an 11-starter catalogue in the read list. Fix: move it into a table in references.
- [med] It writes and compiles code but pre-approves only python3 and Read. Fix: add the tools or drop the field.
- [low] Requiring a validated YAML handoff before any code is heavy for small changes. Fix: make it optional on the fast path.

### meta-wearables-input-sensors — Grade C
- [med] Overlaps display (ButtonGroup) and web-apps (D-pad). Fix: keep only the signal routing and event model.
- [low] 10.2 KB, and the README description is missing the "Use when" sentence. Fix: trim and regenerate the README.

### meta-wearables-knowledge-base — Grade B
- [med] The description lists every domain, so it can win routing over the skill that should do the work. Fix: describe it as "Reference library; not a task skill" and make it non-user-invocable.
- [low] L10-12 says "find this skill by name" under prefixed installs. That breaks the `../meta-wearables-knowledge-base/...` links in 23 skills. Fix: have the adapter rewrite the links.

### meta-wearables-on-device-compliance — Grade C
- [med] Overlaps privacy-publishing and security-attestation (L707-709). Fix: merge with privacy-publishing.
- [low] 9.3 KB. Fix: move the claim-vocabulary table to references.

### meta-wearables-operational-readiness — Grade C
- [med] Same trigger as debugging, and the same tuple as compatibility. Fix: merge, or narrow to the Developer Mode → release-channel transition.
- [low] 11.2 KB. Fix: move detail to `recovery-contract.md`.

### meta-wearables-privacy-publishing — Grade B
- [med] Overlaps compliance and security. Fix: merge.
- [low] L22 mentions an "App Store warning" without quoting it. Fix: quote or link it.

### meta-wearables-route-planner — Grade B
- [med] It and agentic-team both claim to be the entry point "before implementation". Fix: make route-planner the only entry trigger.
- [low] Its reads aren't needed when the inline route map (L38-46) already answers. Fix: make them conditional.

### meta-wearables-security-attestation — Grade C
- [med] 14.7 KB, and it duplicates developer-operations and knowledge-base file 25. Fix: keep the callback and credential controls, link the rest.
- [low] 22 "Never" lines, mostly repeated in siblings. Fix: centralize the shared rules.

### meta-wearables-source-refresh — Grade B
- [med] Its script uses `git ls-remote` and urllib and needs PyYAML, and none of that is documented. Fix: document network access and dependencies.
- [low] Versions are embedded in 23 skill bodies, so each refresh is wide. Fix: centralize them in the registry.

### meta-wearables-transport-reliability — Grade B
- [low] Overlaps camera-audio on HFP and backpressure. Fix: have camera-audio defer to it.
- [low] 8.4 KB. Fix: trim.

### meta-wearables-web-apps — Grade B
- [low] 10.6 KB, with a time-sensitive conflict section (L44-61). Fix: move it to references.
- [low] The README description is missing the "Use when" trigger. Fix: regenerate the README.

## cicd-automation

- All 5 agents match `cloud-infrastructure/agents/` except for the frontmatter name (2 lines differ). devops-troubleshooter is also triplicated in incident-response and distributed-debugging, and the others appear 3–4 times. Every agent is a capability list (Capabilities, Traits, Knowledge, Examples) with no procedure, no output format, no `tools:` allowlist, and no guard before mutations.
- `commands/workflow-automate.md` is 1,372 lines of embedded Python and isn't wired to any agent or skill.

### agents/cloud-architect — Grade D
- [high] Kitchen sink, including "Quantum computing" (L82) and 5G. Fix: one ADR/cost-estimate task with a fixed template.
- [med] Duplicated in 4 plugins. Fix: deduplicate.
- [med] L113 "Include cost estimates" gives no data source. Fix: require cited pricing pages, or say "needs measurement".
- [low] opus with all tools for an advisory role. Fix: `tools: Read, Grep, Glob, WebFetch`.

### agents/deployment-engineer — Grade D
- [high] haiku for a 158-line design agent. Fix: sonnet, or narrow it to mechanical work.
- [med] L114 "no manual deployment steps or human intervention" conflicts with production approval gates. Fix: require explicit production gates.
- [med] A 12-section capability list that overlaps the pipeline skill and the k8s architect. Fix: limit it to implementing the CI/CD pipeline files for a repo.
- [low] Exists in 4 plugins. Fix: deduplicate.

### agents/devops-troubleshooter — Grade D
- [high] "Use PROACTIVELY" for production outages, with all tools and no read-only-first rule. Fix: diagnose-first, with confirmation before restart, scale, rollback or delete.
- [med] No triage steps and no report template. Fix: scope → timeline → hypotheses → test → mitigation proposal.
- [med] Triplicated across plugins. Fix: keep one copy.

### agents/kubernetes-architect — Grade D
- [med] Overlaps deployment-engineer and cloud-architect. Fix: limit it to cluster/platform ADRs.
- [med] Exists in 3 plugins. Fix: deduplicate (ml-pipeline already uses the kubernetes-operations copy).
- [low] opus with all tools. Fix: restrict tools.

### agents/terraform-specialist — Grade D
- [high] Can run apply or state surgery (L104) with no confirmation rule. Fix: plan only; require approval before apply, `state rm/mv`, import or destroy; back up state first.
- [med] No review checklist and no output format. Fix: add pins, locking, `moved`/`check` blocks, policy and drift checks.
- [low] Exists in 3 plugins, and opus is a heavy tier for writing HCL. Fix: deduplicate and use sonnet.

### skills/deployment-pipeline-design — Grade B
- [low] L50 refers to a "Health Checks section above" that has moved to references. Fix: link `references/details.md`.
- [low] The two reference files aren't indexed. Fix: add one line per file.

### skills/github-actions-templates — Grade C
- [high] Uses static AWS keys (L136-141). Fix: OIDC with `id-token: write` and `role-to-assume`.
- [med] Outdated: Node 18 (end of life April 2025), Python 3.9 (end of life October 2025), slack-github-action v1, build-push v5, codecov v4. Fix: update.
- [med] Recommends tag pins, which is weak against supply-chain attacks, and sets no default `permissions:`. Fix: pin third-party actions to SHAs and set `contents: read`.
- [low] Pattern 3 deploys to production on every push with no `environment:` protection. Fix: add it.

### skills/gitlab-ci-patterns — Grade C
- [high] The `hashicorp/terraform` image's entrypoint makes `script:` fail, and the global `before_script: cd` leaks into every job. Fix: `entrypoint: [""]` and per-job `before_script`.
- [med] `docker login -p` (L85) puts the password on the command line, and the image is built twice instead of tagged. Fix: `--password-stdin` and `docker tag`.
- [med] Uses deprecated `only:`. `bitnami/kubectl:1.31` is affected by Bitnami's 2025 catalog removals, and Terraform 1.6.0 is old. Fix: `rules:`, a maintained image, current Terraform.
- [low] `--exit-code 1` together with `allow_failure: true` makes the gate meaningless. Fix: pick one.

### skills/secrets-management — Grade D
- [high] TruffleHog v3 exits 0 unless `--fail` is set, so the pre-commit hook (L318-331) and the CI job never block. Fix: `--fail --results=verified`, scanning in git mode.
- [high] Insecure patterns: static `VAULT_TOKEN` (L88, L107), static AWS keys, `echo "Deploying with $API_KEY"` and `echo $DATABASE_URL` (L204-205), and a password passed on the CLI. Fix: JWT/OIDC auth; remove the echoes.
- [med] The `vault:1.17` image doesn't exist (use `hashicorp/vault`), ESO `v1beta1` is deprecated (use `v1`), and the Terraform example puts the password in state. Fix: `manage_master_user_password` or ephemeral resources.
- [med] The rotation Lambda ignores the 4-step rotation contract, and `generate_strong_password` is undefined. Fix: show the step-dispatch skeleton.
- [low] The tools section is feature bullets. Fix: a decision table.

## javascript-typescript

- The two agents overlap, and neither name is plugin-scoped. modern-javascript-patterns and nodejs-backend-patterns have only a listicle in their SKILL.md.

### agents/javascript-pro — Grade C
- [med] Generic, with no procedure, and a broad trigger that overlaps typescript-pro. Fix: one task (async/race debugging) with steps and an output format.
- [low] "Jest tests" and "polyfill strategy" are dated. Fix: use the project's own test runner.
- [low] Name not plugin-scoped. Fix: rename.

### agents/typescript-pro — Grade C
- [med] opus is too high a tier for type authoring. Fix: sonnet or inherit.
- [med] Pushes class-heavy "enterprise" patterns and doesn't distinguish decorator modes. Fix: favour discriminated unions and Result types, and note the decorator mode.
- [low] No output contract, and the name isn't scoped. Fix: add one and rename.

### skills/javascript-testing-patterns — Grade C
- [med] 537 lines / 14.6 KB. Fix: move the pattern code to references.
- [med] Claims E2E and BDD coverage, but has none. Fix: add an E2E section or drop the claim.
- [low] Mixes a ts-jest setup with Vitest examples, and keeps the "one assertion per test" rule. Fix: lead with Vitest and drop the rule.

### skills/modern-javascript-patterns — Grade C
- [med] 15 platitudes, some wrong for ES modules or hot code paths ("use strict mode", "prefer arrow functions", "array methods over loops"). Fix: a decision table plus a reference index.
- [low] Vague trigger. Fix: narrow it to migrating callback/ES5 code.

### skills/nodejs-backend-patterns — Grade C
- [med] No framework decision (Express 5, Fastify, Hono) and no index of the two 1,000-line references. Fix: add both.
- [low] References use a 10 MB body limit and scatter `process.env` secrets. Fix: small limits, a central config, and token rotation.

### skills/typescript-advanced-types — Grade B
- [low] The type-test helpers (L283-299) are fragile with `any`, and `ExpectError` causes a real compile error. Fix: `expectTypeOf`, `tsd` or `@ts-expect-error`.
- [low] Performance tips are vague. Fix: `--extendedDiagnostics` and `--generateTrace`.

## machine-learning-ops

- The three agents overlap (feature stores, orchestration and versioning are repeated), and their names aren't scoped. `commands/ml-pipeline.md` relies on agents from 4 other plugins without declaring that.

### agents/data-scientist — Grade D
- [med] Kitchen sink that overlaps ml-engineer and business-analyst. Fix: EDA and inference with an output template.
- [med] No statistical-rigour checklist. Fix: add assumption, multiple-comparison and leakage checks.
- [low] 10 KB with all tools. Fix: trim and set tools.

### agents/ml-engineer — Grade D
- [med] Overlaps mlops-engineer. Fix: split into model code vs platform.
- [low] Recommends TorchServe, which is no longer actively developed. Fix: vLLM, Triton or KServe.

### agents/mlops-engineer — Grade D
- [med] 11 KB of per-cloud catalogues (L48-93) and no procedure. Fix: a procedure and output format.
- [low] Pachyderm and "AWS Feature Store" are listed uncritically. Fix: trim.

### skills/ml-pipeline-workflow — Grade F
- [high] 7 referenced files under `references/` and `assets/` don't exist (L59-72, L90, L190, L207, L215). The directory holds only SKILL.md. Fix: create them or remove the pointers.
- [high] The related skills hyperparameter-tuning, experiment-tracking-setup and model-deployment-patterns don't exist. Fix: remove them.
- [med] Code blocks are comment-only placeholders, and the rest is buzzword bullets. Fix: a runnable minimal DAG with gate thresholds.
- [low] Overlaps the `/ml-pipeline` command. Fix: have the command load this skill.

### skills/recsys-pipeline-architect — Grade B
- [med] "The scaffold must run", but no templates are bundled and the references live in an external repo. Fix: bundle stubs.
- [low] L90 suggests promises without `await`, which risks unhandled rejections. Fix: add `.catch` or use a queue.
- [low] It is application architecture placed in the ML plugin. Fix: acceptable, or move it.

## game-development

### agents/minecraft-bukkit-pro — Grade C
- [med] Hardcodes the WebSearch and WebFetch tool names (L49, L115). Fix: describe the action instead.
- [med] No Paper-vs-Spigot or `paper-plugin.yml` decision, and it leans on NMS. Fix: add a target-selection step and prefer the API.
- [low] opus, plus Docker/Kubernetes scope creep. Fix: sonnet and trim.

### agents/unity-developer — Grade D
- [med] A 228-line, 16-section list. Fix: one task with a profile-first procedure.
- [med] Uses the old names Unity Collaborate and Cloud Build. Fix: Unity Version Control and Build Automation.
- [low] opus, and overlaps the ECS skill. Fix: sonnet and defer DOTS to the skill.

### skills/godot-gdscript-patterns — Grade B
- [low] No index of the reference files, and advanced-patterns.md isn't mentioned. Fix: add an index.
- [low] advanced-patterns L213 says "Pattern 4 in the main skill", which doesn't exist. Fix: point to details.md.

### skills/unity-ecs-patterns — Grade C
- [med] L54 says "Use Aspects", and details.md Pattern 5 uses IAspect. Aspects are deprecated as of Entities 1.3. Fix: use `SystemAPI.Query` with component tuples.
- [low] No Entities version pinned. Fix: state 1.3+ / Unity 6.

## business-analytics

### agents/business-analyst — Grade D
- [med] Buzzword kitchen sink with a broad "strategic analysis" trigger. Fix: one question-to-recommendation task with a template.
- [low] Name not scoped, no tool restriction. Fix: rename and restrict.

### skills/data-storytelling — Grade B
- [low] No output template. Fix: add a one-page brief or slide outline.
- [low] Generic advice ("rule of three"). Fix: concrete checks.

### skills/kpi-dashboard-design — Grade B
- [med] L66 "Red=bad, green=good" doesn't work for colour-blind readers. Fix: add icons and labels, and use a palette safe for colour-vision deficiency.
- [low] The cohort note, snapshot `ON CONFLICT` and MRR `CASE` (no `ELSE`) examples contradict themselves. Fix: correct the snippets.

## skill-forge-essentials (no README)

### ai-debt-detector — Grade B
- [low] No findings-table output format. Fix: add one.
- [low] L71 has an unsourced statistic. Fix: remove it.

### session-guard — Grade C
- [med] Unverifiable claims: issues "#19471, #9796, #64171", "5K token cap", "#1 unsolved problem in 2026". Fix: remove them.
- [med] The trigger fires on any complex task, the model can't count its own tool calls, and "STOP" at 60 calls halts real work. Fix: trigger on drift signals and checkpoint to a file instead of stopping.
- [low] `/compact` and CLAUDE.md are Claude-specific. Fix: neutral wording.

### visual-edit-precision — Grade B
- [low] L44 encourages concurrent edits to one file. Fix: edit sequentially.
- [low] The VERIFY step has no method. Fix: screenshot and diff the target element.

## social-publishing (agent and skill duplicate each other; neither contains the API surface)

### agents/social-publishing-publisher — Grade C
- [med] No endpoints or commands, and it relies on an unpinned third-party `npx skills add`. Fix: document the API and pin the version.
- [med] Says 13 platforms but lists 11. Fix: correct the count.
- [low] Write tool not needed, and publishing is irreversible but the confirm step is soft. Fix: drop Write and make confirmation a hard rule.

### skills/social-publishing — Grade C
- [med] Same gaps, and it duplicates the agent. Fix: put the API here and make the agent a thin wrapper.
- [low] "Claude generates" wording, and `export KEY=` leaves the key in shell history. Fix: neutral wording and a secrets store.

## block-no-verify

### skills/block-no-verify-hook — Grade D
- [high] L113-132 runs `cat > ~/.claude/settings.json`, overwriting all global settings; the per-project snippet does the same. The `/block-no-verify` command already merges correctly. Fix: merge with a backup, or delegate to the command.
- [med] False positives I confirmed: it blocks `npm version patch --no-git-tag-version` and `git commit -m x && echo -n`. Fix: anchor the pattern to git subcommands and `\b` flag boundaries.
- [low] Claude Code-only, with no fallback for other harnesses. Fix: mention a git pre-commit hook plus branch protection.