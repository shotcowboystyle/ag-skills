# Audit findings — group 5

Plugins: python-development, cloud-infrastructure, reverse-engineering, security-scanning, operating-kit, observability-monitoring, seo-content-creation, review-agent-governance, database-migrations, signed-audit-trails

Paths relative to plugins/. Grades A–F per item; severity high/med/low; each issue carries a recommended fix.

# Group 5 audit findings

## python-development
- The three `*-pro` agents (python-pro, django-pro, fastapi-pro) and the 16 focused skills substantially overlap; the agents are kitchen-sink personas while the skills do the real single-responsibility work.
- Two orphaned reference files bundled but never linked from any SKILL.md (dead token weight).
- `datetime.utcnow()` and Pydantic V1 `from_orm` appear in several skills that advertise Python 3.12+/Pydantic V2 — both deprecated.

### plugins/python-development/agents/python-pro.md — Grade: D
- [sev: high] Kitchen-sink "expert in everything" persona (lines 59-101: web, data science/ML, DevOps, K8s, all patterns). Collides with django-pro, fastapi-pro, and all 16 python skills. — Fix: narrow to modern core Python (3.12+ language/tooling/async), delegate rest, or drop the agent.
- [sev: med] Pure capability/knowledge-base lists (lines 13-128), no procedure/decision rules/output format. — Fix: replace with a short workflow + output contract.
- [sev: med] `model: opus` unjustified for a generalist advisor. — Fix: sonnet.
- [sev: low] No `tools:` allowlist (gets all tools). — Fix: add allowlist.
- [sev: low] "2024/2025 ecosystem" anchoring (lines 11,132) dates fast. — Fix: drop years.

### plugins/python-development/skills/async-python-patterns/SKILL.md — Grade: B
- [sev: low] "Python 3.7+" (line 86) stale vs 3.12+ stance; TaskGroup/asyncio.timeout only in refs. — Fix: surface them in nav tier.

### plugins/python-development/skills/python-anti-patterns/SKILL.md — Grade: B
- [sev: med] Line 103 `UserResponse.from_orm(user)` is Pydantic V1 (deprecated); V2 is `model_validate`. Self-undermining in an anti-patterns skill. — Fix: use `model_validate`.

### plugins/python-development/skills/python-background-jobs/SKILL.md — Grade: B
- [sev: med] `datetime.utcnow()` (lines 92,210,212 + refs) deprecated in 3.12. — Fix: `datetime.now(timezone.utc)`.

### plugins/python-development/skills/python-code-style/SKILL.md — Grade: B
- [sev: low] Recommends ruff replacing black, but python-packaging lists black. — Fix: align siblings.
- [sev: low] Quick start uses pip while repo standard is uv. — Fix: note uv as preferred.

### plugins/python-development/skills/python-configuration/SKILL.md — Grade: A
- No material issues.

### plugins/python-development/skills/python-design-patterns/SKILL.md — Grade: B
- [sev: low] Very thin body (85 lines, most pushed to refs); near-stub. — Fix: ensure a real one-paragraph decision tree in nav tier.

### plugins/python-development/skills/python-error-handling/SKILL.md — Grade: A
- No material issues.

### plugins/python-development/skills/python-observability/SKILL.md — Grade: A
- No material issues.

### plugins/python-development/skills/python-packaging/SKILL.md — Grade: C
- [sev: med] Orphan reference `references/advanced-patterns.md` (6728 B) not linked from SKILL.md (only details.md is). — Fix: link or remove.
- [sev: low] `requires-python=">=3.8"` and `black` dev dep (lines 81-90) contradict 3.12+/ruff posture. — Fix: bump floor, swap black→ruff.

### plugins/python-development/skills/python-performance-optimization/SKILL.md — Grade: C
- [sev: med] Orphan reference `references/advanced-patterns.md` (10527 B) not linked. — Fix: link or remove.
- [sev: low] Thin body; most substance in refs. — Fix: surface a profiling decision tree in nav tier.

### plugins/python-development/skills/python-project-structure/SKILL.md — Grade: A
- No material issues.

### plugins/python-development/skills/python-resilience/SKILL.md — Grade: A
- No material issues.

### plugins/python-development/skills/python-resource-management/SKILL.md — Grade: A
- No material issues.

### plugins/python-development/skills/python-testing-patterns/SKILL.md — Grade: A
- No material issues.

### plugins/python-development/skills/python-type-safety/SKILL.md — Grade: B
- [sev: low] Shows old `TypeVar`/`Generic[T,E]` but not PEP 695 (3.12 `class Result[T]`, `type` aliases) despite 3.12+ framing. — Fix: mention PEP 695 as modern default.

### plugins/python-development/skills/uv-package-manager/SKILL.md — Grade: B
- [sev: low] `requires-python=">=3.8"` example and `uv lock --no-install` (line 242, not a real flag) — verify flags. — Fix: drop invalid flag, raise floor.

## cloud-infrastructure
- Three agents plus seven siblings overlap; two are opus kitchen-sink personas.
- `network-engineer.md` body is byte-identical to observability-monitoring/agents/network-engineer.md.
- Service-mesh agent domain fully covered by four sibling skills.

### plugins/cloud-infrastructure/agents/hybrid-cloud-architect.md — Grade: D
- [sev: high] Kitchen-sink opus persona (multi-cloud+OpenStack+edge+containers+connectivity+compliance+cost+DR+migration, lines 15-40+). Overlaps multi-cloud-architecture skill and sibling architects. — Fix: narrow or make a thin router.
- [sev: med] Laundry list + generic Response Approach/Example Interactions; no decision rules/output format. — Fix: add workload-placement procedure + deliverable.
- [sev: med] `model: opus` for a generalist. — Fix: sonnet.
- [sev: low] No `tools:` allowlist.

### plugins/cloud-infrastructure/agents/network-engineer.md — Grade: C
- [sev: high] Body identical to observability-monitoring/agents/network-engineer.md (diff confirms). — Fix: keep one canonical copy, remove/redirect the other.
- [sev: med] Long capability list rather than procedure. — Fix: tighten to a troubleshooting workflow.
- [sev: low] No `tools:` allowlist.

### plugins/cloud-infrastructure/agents/service-mesh-expert.md — Grade: C
- [sev: med] Domain fully overlaps four service-mesh skills; agent is thin generic bullets. — Fix: make an explicit router or drop.
- [sev: med] `model: opus` for a 47-line generic persona. — Fix: sonnet.
- [sev: low] No `tools:` allowlist.

### plugins/cloud-infrastructure/skills/cost-optimization/SKILL.md — Grade: B
- [sev: low] 313 lines inline; vendor savings percentages ("72%","90%") stated as fact. — Fix: hedge figures, push provider detail to references.

### plugins/cloud-infrastructure/skills/hybrid-cloud-networking/SKILL.md — Grade: A
- No material issues.

### plugins/cloud-infrastructure/skills/istio-traffic-management/SKILL.md — Grade: B
- [sev: med] All examples use `networking.istio.io/v1beta1`; promoted to `v1` (GA, Istio 1.22+). — Fix: use `v1`.

### plugins/cloud-infrastructure/skills/linkerd-patterns/SKILL.md — Grade: B
- [sev: med] Template 4 uses `split.smi-spec.io/v1alpha1` TrafficSplit (SMI, abandoned); modern Linkerd uses Gateway API HTTPRoute (shown in Template 6). — Fix: mark TrafficSplit legacy, default to HTTPRoute.

### plugins/cloud-infrastructure/skills/mtls-configuration/SKILL.md — Grade: A
- No material issues.

### plugins/cloud-infrastructure/skills/multi-cloud-architecture/SKILL.md — Grade: A
- No material issues.

### plugins/cloud-infrastructure/skills/service-mesh-observability/SKILL.md — Grade: A
- No material issues.

### plugins/cloud-infrastructure/skills/terraform-module-library/SKILL.md — Grade: B
- [sev: low] `references/aws-modules.md` and `oci-modules.md` are tiny bullet stubs (~1.3 KB), low value. — Fix: enrich or fold in.
- [sev: low] Example pins `engine_version="15.3"` — comment as example-only.

## reverse-engineering
- Three defensive-security agents (firmware/malware/reverse) with explicit "Never Assist With"/authorization guardrails — good safety posture; single-domain; opus; command-cheatsheet style.
- None carry a `tools:` allowlist.

### plugins/reverse-engineering/agents/firmware-analyst.md — Grade: B
- [sev: low] Mostly command cheatsheet + phase list; generic Response Approach. Scope coherent. — Fix: optionally gate acquisition behind an explicit authorization step.
- [sev: low] No `tools:` allowlist. — Fix: add one.

### plugins/reverse-engineering/agents/malware-analyst.md — Grade: B
- [sev: low] Strong guardrails, single-domain, reference-heavy. — Fix: none required.
- [sev: low] No `tools:` allowlist.

### plugins/reverse-engineering/agents/reverse-engineer.md — Grade: B
- [sev: low] Overlaps binary-analysis-patterns skill but stays higher-level; ethics section present. — Fix: none required.
- [sev: low] No `tools:` allowlist.

### plugins/reverse-engineering/skills/anti-reversing-techniques/SKILL.md — Grade: B
- [sev: low] 63-line SKILL fronts two large refs (11.4 KB + 10.6 KB); terse nav. — Fix: add a decision tree for which ref.

### plugins/reverse-engineering/skills/binary-analysis-patterns/SKILL.md — Grade: B
- [sev: low] Heading "## Detailed section: Disassembly Fundamentals" (line 18) looks like a mis-generated artifact. — Fix: rename.
- [sev: low] 351 lines mostly inline with thin 2 KB ref. — Fix: acceptable.

### plugins/reverse-engineering/skills/memory-forensics/SKILL.md — Grade: A
- No material issues.

### plugins/reverse-engineering/skills/protocol-reverse-engineering/SKILL.md — Grade: B
- [sev: low] Body jumps into "Traffic Capture" with no When-to-Use section (trigger only in frontmatter). — Fix: add a short nav block.

## security-scanning
- threat-modeling-expert overlaps its five skills as a thin orchestrator.
- Skills use extreme thin-SKILL/huge-references split (66-82 line SKILL vs 597-664 line, 18-23 KB details.md).

### plugins/security-scanning/agents/threat-modeling-expert.md — Grade: C
- [sev: med] 50-line generic capability+workflow+best-practice that restates its skills; `model: opus` for a thin router unjustified. — Fix: sonnet; frame as explicit router.
- [sev: low] No `tools:` allowlist.

### plugins/security-scanning/skills/attack-tree-construction/SKILL.md — Grade: B
- [sev: low] 74-line nav fronts 612-line/19.8 KB details.md; verify not a dumping ground. — Fix: consider splitting.

### plugins/security-scanning/skills/sast-configuration/SKILL.md — Grade: B
- [sev: low] 191 lines inline, no references/ (under 8 KB); tool-list heavy. — Fix: add references/ if it grows.

### plugins/security-scanning/skills/security-requirement-extraction/SKILL.md — Grade: B
- [sev: low] 67-line nav vs 611-line/21.9 KB details.md. — Fix: ensure usable nav decision tree.

### plugins/security-scanning/skills/stride-analysis-patterns/SKILL.md — Grade: B
- [sev: low] 66-line nav vs 597-line/18.5 KB details.md. — Fix: as above.

### plugins/security-scanning/skills/threat-mitigation-mapping/SKILL.md — Grade: B
- [sev: low] 82-line nav vs 664-line/23.6 KB details.md (largest in group). — Fix: split reference by control family.

## operating-kit
- Exemplary: five tightly-scoped agents, correct model tiers (haiku mechanical, sonnet review/deploy), explicit tools allowlists, template placeholders, strong verify-live discipline.

### plugins/operating-kit/agents/code-review-preshipment.md — Grade: A
- No material issues.

### plugins/operating-kit/agents/deploy-with-verification.md — Grade: A
- No material issues.

### plugins/operating-kit/agents/prod-logs-health-check.md — Grade: A
- No material issues.

### plugins/operating-kit/agents/session-end.md — Grade: A
- No material issues.

### plugins/operating-kit/agents/session-start.md — Grade: A
- No material issues.

## observability-monitoring
### plugins/observability-monitoring/skills/distributed-tracing/SKILL.md — Grade: A
- No material issues.

### plugins/observability-monitoring/skills/grafana-dashboards/SKILL.md — Grade: B
- [sev: low] 376 lines inline, no references/ (7986 B — just under Codex 8 KB cap, at risk). — Fix: pre-emptively split panel/JSON detail into references/.

### plugins/observability-monitoring/skills/prometheus-configuration/SKILL.md — Grade: A
- No material issues.

### plugins/observability-monitoring/skills/slo-implementation/SKILL.md — Grade: A
- No material issues.

## seo-content-creation
- Three well-separated roles with clear output contracts and honest scoping.

### plugins/seo-content-creation/agents/seo-content-auditor.md — Grade: B
- [sev: low] sonnet reasonable for scored judgment; clear table output. — Fix: none required.

### plugins/seo-content-creation/agents/seo-content-planner.md — Grade: A
- No material issues (haiku appropriate).

### plugins/seo-content-creation/agents/seo-content-writer.md — Grade: B
- [sev: low] "0.5-1.5% keyword density" (line 68) is outdated SEO guidance. — Fix: replace with intent/entity-coverage guidance.

## review-agent-governance
### plugins/review-agent-governance/agents/review-policy-author.md — Grade: A
- [sev: low] No `tools:` allowlist (plausibly Read/Write/Grep only). — Fix: add narrow allowlist. Otherwise excellent and specific.

### plugins/review-agent-governance/skills/review-agent-setup/SKILL.md — Grade: A
- No material issues (pinned versions, gitignores keys, clear approval/verify flow).

## database-migrations
### plugins/database-migrations/agents/database-admin.md — Grade: D
- [sev: high] Kitchen-sink: all four clouds, every DB engine class, IaC, HA/DR, security, compliance, cost (lines 11-50+). Overlaps database-optimizer sibling. — Fix: decompose or narrow to cloud DB operations/reliability.
- [sev: med] Generic Response Approach/Example Interactions; no runbook/decision rule/output format. — Fix: add procedure + deliverable.
- [sev: med] Breadth suggests decomposition over tuning. — Fix: decompose.
- [sev: low] No `tools:` allowlist.

## signed-audit-trails
### plugins/signed-audit-trails/skills/signed-audit-trails-recipe/SKILL.md — Grade: A
- [sev: low] Claude-Code-specific but explicitly a teaching recipe for that runtime; pinned versions, gitignores private key, controlled tamper demo. — Fix: none required.

## Group summary

Top 10 most important fixes:
1. python-pro.md — dissolve kitchen-sink opus persona (overlaps django/fastapi-pro + 16 skills); narrow or drop, demote to sonnet.
2. database-admin.md — decompose all-clouds/all-engines kitchen-sink agent; add real runbook/output contract.
3. hybrid-cloud-architect.md — narrow scope, add workload-placement decision procedure, opus→sonnet.
4. cloud-infrastructure/network-engineer.md — byte-identical duplicate of observability-monitoring copy; dedupe.
5. service-mesh-expert.md & threat-modeling-expert.md — thin opus personas fully covered by sibling skills; make routers, demote to sonnet.
6. python-packaging & python-performance-optimization — remove/link the two orphan references/advanced-patterns.md files.
7. Deprecated APIs in python skills — datetime.utcnow() (background-jobs) and Pydantic V1 from_orm (anti-patterns, design-patterns refs) → modern equivalents.
8. linkerd-patterns — flag split.smi-spec.io/v1alpha1 TrafficSplit as legacy (SMI abandoned); default to Gateway API HTTPRoute.
9. istio-traffic-management — move examples from networking.istio.io/v1beta1 to v1 (GA since 1.22).
10. Add missing tools: allowlists / demote unjustified opus across generalist agents (python-pro, hybrid-cloud-architect, network-engineer, service-mesh-expert, database-admin, threat-modeling-expert).

Grade counts (58 items):
- A: 24
- B: 22
- C: 5
- D: 4
- F: 0
