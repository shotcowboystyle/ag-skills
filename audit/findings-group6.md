# Audit findings — group 6

Plugins: backend-development, developer-essentials, incident-response, api-scaffolding, payment-processing, accessibility-compliance, code-documentation, comprehensive-review, documentation-standards, superself

Paths relative to plugins/. Grades A–F per item; severity high/med/low; each issue carries a recommended fix.

**Grade counts (57 items):** A 1 · B 20 · C 30 · D 6 · F 0

**Top 10 fixes**
1. **paypal-integration (D):** the browser creates a v2 Orders order but the backend uses the deprecated v1 `paypalrestsdk`, so it can't work. It also sets the price and captures in the browser. Make create/capture server-side v2 and verify webhooks instead of IPN.
2. **pci-compliance (D):** update PCI DSS v3.2.1 to v4.0.1. Delete the PAN-in-a-dict `TokenVault`, the encryption example whose key changes every run, and the legacy `createToken`/`Charge.create` calls.
3. **turborepo-caching (D):** move `pipeline` to `tasks` and turbo ^1.10 to 2.x, replace `--remote-only`. Fix or remove the self-hosted cache server (`fs` is never imported; `teamId` allows path traversal). Split it under the 8 KB Codex cap.
4. **Temporal (agent and two skills):** `workflow.get_version()` isn't a Python SDK API; use `workflow.patched()`. Remove the false rule that async code in workflows is a violation. Fix the async fixture in the testing quick-start.
5. **bazel-build-optimization (D):** rewrite for `MODULE.bazel` (Bzlmod). WORKSPACE is off by default in Bazel 8 and removed in Bazel 9.
6. **incident-responder:** require human approval before any production rollback, scaling or throttling. Cut it to a first-hour procedure with an output format.
7. **Duplicates:** code-documentation/code-reviewer copies comprehensive-review's and is unused. backend-architect and graphql-architect each exist in both backend-development and api-scaffolding.
8. **tdd-orchestrator (D):** replace the 183-line opus catalog with a concrete red-green-refactor loop on sonnet.
9. **All agents:** none has a `tools:` allowlist, so read-only reviewers get Write/Edit/Bash. 4 incident-response agents have no trigger phrase, and most define no output format. Both security-auditors cite old OWASP lists (2017 and 2021, not 2025).
10. **Stale facts:**
    - `pg_stat_statements` columns were renamed in PG13, and the OR and subquery claims are wrong.
    - nx still uses `workspace.json` and `tasksRunnerOptions`.
    - The monorepo `exports` map lists `types` after `import`.
    - superself is pinned to 0.6.1 while 0.13.1 is installed, and the documented `work block --on` flag no longer exists.

Only connectivity-triage got an A.

**Per-plugin detail**

**backend-development**
- *event-sourcing-architect, C:* a generic list with no "when not to event-source" rule and no output format. It doesn't point to its four sibling skills. Name isn't plugin-scoped; `model: inherit`.
- *performance-engineer, B:* steps say "measure or estimate", which invites made-up numbers. Severity is latency-only.
- *security-auditor, B:* lists the 2017 OWASP categories (XXE, insecure deserialization). No read-only allowlist.
- *tdd-orchestrator, D:* see fix 8. It claims multi-agent coordination but names no agents and no command uses it.
- *temporal-python-pro, C:* `get_version` at L134. 349 lines that repeat the skills. Missing `@workflow.update`, the sandbox, and `workflow.random()`.
- *test-automator, B:* "one test file per source file" conflicts with "follow project conventions". It never requires actually running the tests.
- *api-design-principles, C:* four bundled files are never referenced (`rest-best-practices.md`, `graphql-schema-design.md`, `api-design-checklist.md`, `rest-api-template.py`). The body is a primer with no decision rules.
- *architecture-patterns, B:* two overlapping references with no rule for which to read.
- *cqrs-implementation, event-store-design, projection-patterns, all C:* thin overlapping stubs; merge into one event-sourcing skill. EventStoreDB is now KurrentDB. "Don't query in commands" is wrong as stated.
- *microservices-patterns, C:* buzzword bullets with no decision rules.
- *saga-orchestration, B:* says "see Template 3 above", but the templates moved to references. Two empty "Moved to" stub sections.
- *temporal-python-testing, C:* `get_version` at L365 and L409 of `resources/replay-testing.md`. An async fixture uses plain `@pytest.fixture`. Its "≥80% coverage" figure is wrongly credited to Temporal's docs.
- *workflow-orchestration-patterns, C:* the async error at L56 and `get_version` in its reference. Its lists repeat the agent's verbatim.

**developer-essentials**
- *monorepo-architect, C:* opus for a 50-line checklist, no output format.
- *auth-implementation-patterns, B:* `jwt.verify` is called without an `algorithms` option.
- *code-review-excellence, C:* written for humans (time boxes, emoji, "offer to pair"). It overlaps three code-reviewer agents that use different severity scales.
- *debugging-strategies, C:* generic advice ("rubber duck", "take breaks", comment out half the code).
- *e2e-testing-patterns, B:* shell commands sit inside a TypeScript code block.
- *error-handling-patterns, C:* its "good" example breaks its own pitfalls (`except Exception`, log-and-rethrow).
- *git-advanced-workflows, B:* relies on `git rebase -i`, which needs an interactive editor most agent tools lack.
- *monorepo-management, C:* repeats the Turborepo skill. `exports` has `types` after `import`. Old pnpm 8 and tsup 7 pins.
- *nx-workspace-patterns, C:* see fix 10.
- *sql-optimization-patterns, C:* see fix 10. Also shows `VACUUM FULL` and `REINDEX TABLE` with no lock warning.

**incident-response**
- Severity scales disagree: SEV1 ack <15 min with <1 h resolution in incident-responder, vs SEV1 15 min / SEV2 30 min in the runbook skill.
- *code-reviewer, debugger, error-detective, test-automator, all C:* no trigger phrase and no output format, though the commands depend on "structured findings".
  - error-detective reads untrusted logs with no rule to treat their text as data.
  - debugger's git bisect can check out commits in the user's working tree.
- *incident-responder, C:* see fix 6. Its principles contradict each other ("accuracy matters more" vs "fix first"). Lists Opsgenie, which Atlassian stopped selling.
- *runbook-templates, B:* the idle-session filter uses `query_start` where it should use `state_change`.
- *on-call-handoff-patterns, B:* human-process content only.
- *postmortem-writing, B:* templates split between SKILL.md and the reference.

**api-scaffolding**
- *backend-architect, C:* a 309-line catalog. It refers to database-architect and cloud-architect, which aren't in this plugin.
- *django-pro, C:* opus, a catalog with no playbooks.
- *fastapi-pro, C:* recommends `python-jose` (unmaintained, has CVEs) and Motor (deprecated). opus.
- *graphql-architect, C:* a duplicate, opus.
- *fastapi-templates, B:* should use `async_sessionmaker` and `StaticPool` for the SQLite test DB.

**payment-processing**
- *payment-integration, B:* its "respond within 200 ms" is an invented figure.
- *billing-automation, C:* the quick start imports a library that doesn't exist (`from billing import BillingEngine`). No build-vs-buy guidance.
- *stripe-integration, B:* the test confirms a PaymentIntent with no `return_url`. Stripe rejects that unless `allow_redirects: 'never'` is set.

**accessibility-compliance**
- *ui-visual-validator, C:* no way to capture screenshots. It claims to measure contrast from screenshots, which isn't reliable.
- *screen-reader-testing, C:* code bugs: focusing an h2 with no tabindex, an undefined `modal` variable, an accessible-name helper that returns an ID string. An agent can't drive a screen reader and no automated path is given.
- *wcag-audit-patterns, B:* covers only one of the WCAG 2.2 additions (2.4.11).

**code-documentation**
- *code-reviewer, D:* see fix 7. Also lists dead tools (Codiga), uses opus, and has no output format.
- *docs-architect, B:* targets "10-100+ pages" with no output location or check that examples work.
- *tutorial-engineer, B:* relies on the learning-styles myth and has no step to run the tutorial code.

**comprehensive-review**
- *architect-review, C:* a catalog with no review checklist or output format.
- *security-auditor, C:* cites OWASP 2021. As a reviewer it is also told to "implement controls" and "provide training".

**documentation-standards and superself**
- *grounded-vault, B:* the commit gate runs `scripts/check_vault.py`, but that script exists only inline in `references/details.md`.
- *hads, B:* Claude-specific wording. Its required BUG fields are stated two different ways.
- *superself, B:* the version drift in fix 10. Its install line could lead an agent to `npm install -g` without asking.