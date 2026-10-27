---
name: checkpoint-promotion
description: Gate fine-tuned checkpoints with drift budgets, paired comparison, and forgetting checks before promotion. Use after a training run produces a checkpoint, when deciding whether a tuned model ships, or when a promoted model needs re-gating against updated goldens.
---

# Checkpoint Promotion

The Phase 5 gate for the whole plugin: a checkpoint that trains cleanly and beats its task metric still doesn't ship without clearing all four stages below. `eval-harness-first` built the suite re-run here — this skill is where that suite's baseline decides something.

**Input:** a trained checkpoint, `eval/baseline-<model>.json` and its per-item `eval/baseline-<model>-results.json` from `eval-harness-first`, and the frozen `eval/drift-suite.yaml`.
**Output format:** `runs/<date>-<slug>/promotion-report.md` — the four-stage evidence plus a terminal `PROMOTE` or `REJECT` verdict that `/finetune` Phase 5 and `/promote-checkpoint` consume directly.

## The Four-Stage Gate

Each stage gates the next — a failure at stage 2 means stage 3 doesn't run. On a **deterministic** arena, stages 2 and 3 may share one inference pass and apply gate order at verdict time; a judge-based arena waits for stage 2 first.

1. **Data-quality gate.** Before any eval touches the checkpoint: dedup the training set, check for eval-goldens leakage (the exact failure `trace-to-training-data`'s Hygiene section exists to prevent), and scan for label noise. A checkpoint trained on leaked goldens invalidates every later stage.
2. **Held-out + frozen capability-drift suite.** Re-run `eval-harness-first`'s `eval/drift-suite.yaml` — MMLU/GSM8K/IFEval plus 200–500 domain-adjacent items — against the checkpoint, pair each item with the base model's verdict on the same item, and score every benchmark against the Drift Budget below.
3. **Paired arena vs. base.** Position-randomized judge, checkpoint vs. base model, same prompts — or the deterministic paired-comparison variant in `references/gate-templates.md` when every grader in the harness is deterministic (no LLM-judge; position randomization N/A there). **A holdout win that loses the live arena does not ship** — stage-2 numbers and stage-3 judgments must agree; a win on frozen goldens and a loss in paired comparison is a real signal, not a discrepancy to explain away.
4. **Canary.** 5–10% stratified rollout with auto-rollback for any checkpoint reaching production traffic. **Local-only users stop at stage 3** — skipping stage 4 for a local deployment is the correct stopping point, not a shortcut.

### Drift Budget

Drift `d` is baseline accuracy minus checkpoint accuracy, in percentage points, per benchmark (positive = regression). The bands are contiguous — every value of `d` lands in exactly one row:

| Drift `d` (pts) | Verdict |
|---|---|
| d ≤ 1 | Noise — proceed |
| 1 < d ≤ 5 | Rerun with seed variation before deciding |
| d > 5 | **HARD FAIL** — no exception for task gains |

The >5pt row governs regardless of the others: a checkpoint that gained 8 points on the target task and lost 6 points of general capability still fails here — task improvement never buys back a drift-budget breach.

**Measure drift as a paired difference, not two independent scores.** Base and checkpoint answer the same items, so the uncertainty that matters is in the items whose verdict *flipped*, not in each score on its own. With `b` items the base passed and the checkpoint failed, `c` the reverse, and `n` items total:

```
d  = (b − c) / n
SE = sqrt(b + c − (b − c)² / n) / n
95% CI upper bound: hi = d + 1.96 · SE
```

**A noise-band result passes only when `hi ≤ 5pt`** — the CI has to rule out a hard-fail breach. When `d ≤ 1` but `hi > 5`, the stage verdict is `REJECT (uncertain)`: resolve it with a larger suite, never by rounding to the more convenient verdict. A `d > 5` is a HARD FAIL whatever its CI says.

**n=200 is the floor, and PROMOTE is reachable there.** At `d ≈ 0`, `hi ≤ 5pt` holds whenever no more than ~13% of items (26 of 200) flip verdict between base and checkpoint; at `d = 1pt` the limit is ~8%. Two unpaired scores could not get there (each alone carries ±6pt at n=200, p≈0.7). When flips run higher, size the suite with `n ≥ 1.96² · r / (0.05 − d)²` (`r` = flip fraction). Full math, the report table, and a 5-run cautionary example: `references/gate-templates.md`.

**RERUN is not a verdict.** A `1 < d ≤ 5` result only ever produces `PROMOTE` or `REJECT` after the seed-variation rerun completes. Score the rerun the same way, on the pooled items: `PROMOTE` requires `d ≤ 1` and `hi ≤ 5`; anything else resolves stage 2 to `REJECT`. No report may reach the Verdict section with stage 2 still showing `RERUN`.

## Catastrophic Forgetting

Unmanaged LoRA fine-tuning loses real general capability, and stage 2 is what catches it:

- **~43% knowledge loss unmanaged** — no replay, no regularization.
- **~10% with basic management** — some replay or a conservative LR.
- **~3% with replay + EWC** — the disciplined case.
- **10–30% general-data replay mix is the standard mitigation** — blend general-domain data into training rather than target-task data alone.

If a checkpoint hits the >5pt hard fail in stage 2, work this escalation ladder in order — the one canonical order this skill and `references/gate-templates.md` both point to:

1. **Adjust the replay-mix fraction — swap rows, don't add them** (adding confounds fraction with total optimizer steps). Dose is not monotonic at small-run scale (<~100 steps) — re-check drift after any swap.
2. **Lower the learning rate.**
3. **Fewer epochs.**
4. **A smaller LoRA rank** — the same rank/LR levers `lora-qlora-recipes` and `preference-optimization` tune for the training run, applied here in reverse.

This order is a default, not a law: **remediation guidance from a single before/after run pair is a hypothesis** — label it low-confidence once any lever produces a reversal, and prefer a seed-variation repeat over trusting the next rung blindly. A lever that clears the breach but drops a success metric below target is a tradeoff for a human, not a reason to keep descending. Full reasoning and the 5-run trajectory behind both caveats: `references/gate-templates.md`.

**Disclose drift-suite instruction reuse.** A replay row that copies the drift harness's exact instruction phrasing makes that benchmark's post-replay score an upper bound — flag it, or re-probe with a paraphrase, before trusting a near-budget pass.

## The Verdict

`promotion-report.md` covers all four stages as sections and **must end with a terminal verdict: `PROMOTE` or `REJECT`**, the evidence that produced it, and exactly one top remediation when the verdict is `REJECT`. Template: `references/gate-templates.md`. The terminal contract other skills parse:

```
## Verdict

REJECT

Evidence: domain-adjacent drift suite dropped 6.2pt (threshold: >5pt hard fail) despite +8pt on the target task.

Top remediation: swap the replay-mix fraction from 10% toward 20%, holding step count constant.
```

- **REJECT is a result, not an error.** A checkpoint that fails stage 2 or stage 3 shows the gate working; don't rerun this skill to get a different answer.
- **One remediation, not a menu.** Evidence sections may list everything observed; the verdict section names the single highest-leverage fix per the escalation ladder above. A report that hedges across three possible fixes hasn't done the prioritization this skill exists to do.
- **No auto-retraining.** This skill produces a verdict and a report, not a re-triggered training run. A `REJECT` hands the remediation back to a human decision at `finetuning-method-selection` or the relevant training skill.

## Related Skills

- `eval-harness-first` — owns the drift suite and baseline this skill re-runs and diffs against; no `baseline-<model>.json` means nothing to gate against.
- `quantized-export` — the only valid next step after a `PROMOTE` verdict.
- `preference-optimization` and `lora-qlora-recipes` — own the LR and rank levers in the Catastrophic Forgetting escalation path; this skill diagnoses the breach, those skills own the config that caused it.
- `dataset-curation` — owns the replay-mix construction recipe the escalation ladder's first rung applies.
