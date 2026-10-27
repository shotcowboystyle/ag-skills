# Model Catalog

Last verified: 2026-10-27
Refresh checklist: (1) check Unsloth's model catalog and supported-models pages, (2) check the current open-weights leaderboards for each size class, (3) update rows + bump this date. This file is the ONLY place base models are named in the llm-finetuning and dgx-spark-ops plugins.

**Staleness rule:** the catalog is stale once the date above is more than 90 days old. A stale catalog is refreshed before any row is used to name a model. If a refresh is not possible in the current session (no web access), recommend a size class only, and say the catalog is stale and needs a refresh. Never name a model from a stale row.

## How to Read This Table

Pick the row matching the target parameter count, then read across: a text recommendation, a vision (VLM) recommendation for the same size class, what that class can do on a single DGX Spark, and any notes that change the recommendation. Check the date above against the staleness rule before trusting a row.

## Catalog (2026-10)

| Size class | Text recommendation | Vision recommendation | Spark feasibility | Notes |
|---|---|---|---|---|
| ≤4B | Qwen3.5 4B, Gemma 4 E4B | The same checkpoints (both take image input); SmolVLM for the smallest footprint | Full fine-tune feasible | Smallest class where full FT is still *feasible* by default — a hardware/size-class note, not a method recommendation. Method choice (LoRA vs. full FT) is `lora-qlora-recipes`'s LoRA vs QLoRA vs Full FT table, routed by task shape (demonstrations vs. dense knowledge injection); that table governs over this feasibility note whenever the two appear to disagree. |
| 7–9B | Qwen3.5 9B, Llama-class 8B | Qwen3.5 9B; Qwen3-VL-8B when a dedicated VL checkpoint is required | Full fine-tune ceiling | Above this class, full FT stops being the default on Spark — see 12–32B row. |
| 12–32B | Qwen3.8 27B, Gemma 4 31B | The same checkpoints (both take image input); Qwen3-VL-32B as the dedicated VL option | LoRA-only; 27B is the verified LoRA ceiling at pack≤1024 | 27B is the largest dense model measured to fit a LoRA run on a single Spark. Gemma 4 31B sits above that measurement — needs measurement before committing a run to it. |
| Small-active MoE (≤35B total) | Qwen3.6 35B-A3B, Gemma 4 26B-A4B | Gemma 4 26B-A4B | Not yet measured on Spark | Training memory scales with *total* parameters, not active ones — size these as 26–35B models in `references/memory-math.md`, not as 3–4B ones. |
| 70B+ | Llama 3.3 70B class | Use the 12–32B vision class instead — no 70B+ VLM recommendation at this size | QLoRA-only, ≈40GB, 30–48h for 3 epochs | bf16 is not feasible at this class on a single Spark; QLoRA is the only path in. |
| 100B+ MoE | gpt-oss-120b class | Use the 12–32B vision class instead — no 100B+ MoE VLM recommendation at this size | NVFP4-native LoRA via community recipe (`nvfp4-lora-spark`), experimental | Not the default assumption for other 100B+ MoE models (Qwen3.5-122B-A10B, Nemotron 3 Super 120B-A12B) — verify per-model before relying on this row. |

## Vision Model Notes

- **Current Qwen and Gemma releases are natively multimodal.** Qwen3.5, Qwen3.8 27B and every Gemma 4 size take image input in the base checkpoint, so the text and vision columns can name the same model. Qwen3-VL is the last separate Qwen VL line; pick it only when a dedicated VL checkpoint is needed.
- **Qwen2.5-VL and LLaVA are legacy.** Do not recommend them for new work; they are listed here only so a stale recommendation can be recognized as such.
- **Module names differ across these families.** `vision-sft` scopes LoRA by module path for that reason — never assume one family's vision-tower names carry over to another.
