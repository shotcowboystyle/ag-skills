# Audit findings — group 4

Plugins: ai-video-producer, llm-application-dev, systems-programming, frontend-mobile-development, dgx-spark-ops, kubernetes-operations, seo-analysis-monitoring, frontend-mobile-security, codebase-cleanup, file-conversion

Paths relative to plugins/. Grades A–F per item; severity high/med/low; each issue carries a recommended fix.

# Group 4 findings (transcribed from reviewer return)

Grades (57): A 2 · B 20 · C 26 · D 9 · F 0
Cross-cutting: no agent declares `tools:`; wshobson-derived "Capabilities / Behavioral Traits / Knowledge Base" laundry lists with no decision rules.

## ai-video-producer
Plugin: path contract split — commands read `pipelines/<n>.md`, agents write `pipelines/<n>/SPEC.md`+`run.md`; conventions skill omits clips/normalised, clips/converted, budgets, research. model-researcher overlaps recommend-model. Runners live in recommend-model, unreferenced by generation skills.
- agents/aspect-converter.md B — refers to "same detection logic as concatenator" (agents can't see each other) → shared skill or inline; blur-fill missing `-map 0:a?`; no tools.
- agents/concatenator.md B — fixed `/tmp/concat.txt` + `-safe 0` + unescaped quotes → mktemp + escape `'`; ignores clips/normalised/; writes output/ not output/drafts/.
- agents/normalizer.md B — line 16 "-16 LUFS (EBU R128)" wrong, R128 = -23 → label -16 as streaming target; 2nd loudnorm pass missing offset/linear=true; references nonexistent /grade.
- agents/pipeline-builder.md C — [high] writes run.md but /run-pipeline reads <n>.md → fix command; ignores bundled runners; no gitignore of parameters.json.
- agents/pipeline-repo-setup.md D — [high] lines 11,12,40 hardcode "Daniel" + ~/repos/github/my-repos → remove, ask base path; [high] edits AGENTS.md + `gh repo create --push` without confirm → plan + single confirm; no templates → assets/.
- agents/pipeline-scaffolder.md B — "pure planning" but all tools → Read/Write/Glob; unused runs/ folder.
- agents/script-writer.md A.
- skills/ai-media-tools-index B — 64KB refs, md+json duplicated, stale 2026-04 snapshot → JSON + short index + refresh target; add jq example.
- skills/budget-estimator C — [high] line 29 tier labels wrong (Typical/low/high → 1×, mult, mult×1.5) → Low/Typical/High; no pricing sources; no trigger.
- skills/comfyui-export C — [high] line 34 seed `-1` invalid in API format → concrete random int; legacy ControlNetApply; Wan/Hunyuan nodes unnamed.
- skills/comfyui-import C — line 18 sources/sinks reversed; `LoadCheckpoint` not real (`CheckpointLoaderSimple`); `_meta` is API-format not UI; no prompt-injection guard.
- skills/model-researcher C — overlaps recommend-model; Reddit/provider scraping without injection guard; no trigger opener.
- skills/recommend-model C — [high] hardcoded `mcp__plugin_…replicate__*` IDs (lines 26–27) → harness-neutral wording; hosts plugin-wide runners/ → move to plugin-level; reads ~/.config/ai-video-producer/.env → check env vars; stale Kling vs LTX price claim.
- skills/script-to-tts B — ElevenLabs v3 uses audio tags not `<break>`; unsourced 14ms/char → 150 wpm.
- skills/text-to-image-to-video B — no runner call; canonical vs seeded pipelines/*.md unclear.
- skills/text-to-video-direct B — no runner call; unversioned model names.
- skills/upscale-and-interpolate B — "upscale before interpolate" is a tradeoff not a rule; size claim off; overlaps aspect-converter.
- skills/video-workspace-conventions C — [high] line 40 `pipelines/<name>.md` contradicts agents; missing folders; incomplete command list.
- skills/voice-to-lip-sync B — doesn't reuse script-to-tts output; no voice-clone consent check.

## llm-application-dev
Plugin: 1 agent + 4 skills on same vector-search ground; inconsistent model names (Opus 4.8/Sonnet 5 vs "Claude 4.6", "Claude 4 Vision", 200K, Llama 3.3, voyage-3-large); commands/ai-assistant.md 1,253 lines.
- agents/ai-engineer.md D — [high] 158-line everything-AI list w/ PROACTIVE grab-all trigger → scoped procedure; stale models; sibling collision; inherit→sonnet.
- agents/prompt-engineer.md C — 276 lines, ~180 bullets; "Let's think step by step", 200K, Constitutional AI as prompting technique; overlaps skill+command.
- agents/vector-database-engineer.md C — duplicates skills w/o loading them; dated Voyage rec; chunking w/o eval step.
- skills/embedding-strategies C — stale undated "2026" model table; chunking collides with rag-implementation; no decision tree.
- skills/hybrid-search-implementation B — no RRF formula / k default; details.md:177 `LIMIT $3 / 3` int division → 0.
- skills/langchain-architecture D — [high] deprecated create_react_agent + legacy memory classes; fake tests; 8,022B at Codex cap; top-level await.
- skills/llm-evaluation C — Quick Start calls undefined funcs; BLEU/METEOR-first, thin LLM-judge guidance; overlaps prompt-engineering-patterns.
- skills/prompt-engineering-patterns C — 5 refs + assets + script (~2,900 lines) never linked; mock-client script; description not "Use when"; duplicates agent.
- skills/rag-implementation C — [high] details.md:44 imports `langchain.retrievers` (removed 1.x); duplicated tables; RAG prompt lacks injection/citation guard.
- skills/similarity-search-patterns C — lines 24–28 broken Manhattan row; deprecated Qdrant client.search / Weaviate v3; overlaps vector-index-tuning + hybrid-search.
- skills/vector-index-tuning B — overlaps similarity-search; HNSW defaults per engine differ.

## systems-programming
Plugin: all 4 agents opus; C stubs 35 lines vs Go/Rust 171-line lists.
- agents/c-pro.md C — opus; no sanitizers; C99/C11 only (C23 current); kernel/embedded scope unguided.
- agents/cpp-pro.md C — opus; slogans; trigger collides with memory-safety-patterns.
- agents/golang-pro.md D — [high] pinned Go 1.21+, misses 1.22–1.25 idioms; laundry list; opus + PROACTIVE.
- agents/rust-pro.md D — [high] pinned 1.75+, claims "Higher-kinded types" (Rust lacks); no checklist; opus.
- skills/go-concurrency-patterns B — pre-1.22 loop var, no wg.Go; "prefer channels over mutexes" overstated.
- skills/memory-safety-patterns C — 3-language kitchen sink; Go GC "more safe" missing data-race caveat.
- skills/rust-async-patterns B — async-trait default though native async fn in traits stable since 1.75.

## frontend-mobile-development
- agents/mobile-developer.md D — [high] RN+Flutter+native+MAUI+Xamarin+Ionic+ASO in one; Expo SDK 50/RN 0.74/Flipper stale; inherit.
- skills/nextjs-app-router-patterns C — [high] line 110 "Don't pass serializable data" inverted; Next 14 caching model; broken mid-file "use server".
- skills/react-native-architecture C — [high] line 101 env vars for secrets get bundled; template flag stale; StyleSheet perf myth.
- skills/react-state-management B — Zustand example subscribes whole store; recommends Formik.
- skills/tailwind-design-system B — ~130 lines inline CSS, advanced-patterns.md unlinked; wrong v4 date (GA Jan 2025).

## dgx-spark-ops (strongest in group)
- agents/dgx-spark-ops-engineer.md B — no thermal step; no confirm before root drop_caches; UNKNOWN not in output vocabulary.
- skills/spark-environment-setup B — container tag 25.09 vs 25.11; 8,113B at Codex cap.
- skills/spark-memory-thermal-ops B — `echo 3 > drop_caches` fails under sudo (use `sudo tee`); thermal-sample.sh overwrites log.
- skills/spark-training-gotchas B — preflight.sh `G9 UNKNOWN` breaks contract.

## kubernetes-operations
- skills/gitops-workflow C — Argo CD install unpinned, not server-side; ESO v1beta1 removed; 293 inline lines; admin password never rotated.
- skills/helm-chart-scaffolding C — empty nav tier, assets/script unmentioned; `helm install --dry-run` needs cluster.
- skills/k8s-manifest-generator C — ~2,670 ref lines behind one link; kubeval unmaintained (kubeconform); deprecated `kubectl get endpoints`.
- skills/k8s-security-policies D — [high] PodSecurityPolicy (removed 1.25) in description/intro → Pod Security Admission; scope creep 347 lines; Istio v1beta1.

## seo-analysis-monitoring
- agents/seo-authority-builder.md C — X/10 score no rubric; SSL-badge/Knowledge Panel advice; no tools/injection guard.
- agents/seo-cannibalization-detector.md C — [high] demands "Ranking: #X" with no data source → invites fabrication; no similarity% method; canonical misuse.
- agents/seo-content-refresher.md D — [high] date bumps, sitemap priority, "2025" in titles (ignored/spam); hardcoded 2023→2025.

## frontend-mobile-security
- agents/frontend-security-coder.md C — 166-line list; Feature-Policy, JS frame-busting, zoom prevention (WCAG 1.4.4 fail); hands off to ambiguous `security-auditor` (4 copies).
- agents/mobile-security-coder.md C — no MASVS/Play Integrity/App Attest; unconditional cert pinning; Cordova/PhoneGap.

## codebase-cleanup
- agents/test-automator.md D — copied into 4 plugins, off-scope for cleanup; PROACTIVE grab-all.

## file-conversion
- skills/file-conversion A — at 8,184B Codex cap; additions go to references/.
