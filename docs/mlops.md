# MLOps Lab Pipeline

This document covers the end-to-end MLOps pipeline for the Major 7 lab:
experiment tracking on W&B, model/dataset storage on Hugging Face, and the
GitHub Actions glue that ties them together.

## Environment

The lab runs on a DGX Spark. GPU training and fine-tuning run locally;
W&B receives all metrics and artifacts; Hugging Face is the durable model
and dataset store; GitHub Actions handles CPU-side CI (lint, test, eval,
model release).

| Service        | Entity / namespace                                       | Notes                                              |
| -------------- | -------------------------------------------------------- | -------------------------------------------------- |
| W&B            | `shotcowboystyle` (team under org `shotcowboystyle-org`) | Project: `shotcowboystyle-lab`                     |
| Hugging Face   | `shotcowboystyle` org                                    | Token has `write` role; admin on `shotcowboystyle` |
| GitHub Actions | `shotcowboystyle/ag-skills` repo                         | CPU-side only; no GPU runners                      |

### Shell environment

The following variables are exported in `~/.bashrc`:

```bash
export WANDB_API_KEY='wandb_v1_…'
export WANDB_ENTITY='shotcowboystyle'
export WANDB_PROJECT='shotcowboystyle-lab'
export HUGGING_FACE_HUB_TOKEN='hf_…'
export HF_TOKEN=$HUGGING_FACE_HUB_TOKEN
export HF_HUB_ENABLE_HF_TRANSFER='1'
```

`HF_HUB_ENABLE_HF_TRANSFER` requires the `hf_transfer` package, which is
installed in the `unsloth` conda environment.

### Python environment

ML workloads use the `unsloth` conda environment:

```bash
source ~/miniconda3/bin/activate unsloth
```

The `unsloth` env has `wandb`, `torch`, and `hf_transfer` installed.

## Training a Model (local GPU)

```python
import wandb
from transformers import Trainer, TrainingArguments, AutoModelForSequenceClassification, AutoTokenizer

wandb.init(project="shotcowboystyle-lab", entity="shotcowboystyle", tags=["fine-tune"])

model = AutoModelForSequenceClassification.from_pretrained("shotcowboystyle/my-base-model")
tokenizer = AutoTokenizer.from_pretrained("shotcowboystyle/my-base-model")

trainer = Trainer(
    model=model,
    args=TrainingArguments(
        output_dir="./checkpoints",
        report_to="wandb",
        run_name="my-finetune-run",
        logging_steps=50,
        save_steps=500,
        save_total_limit=3,
    ),
)
trainer.train()
wandb.finish()
```

Checkpoints are saved locally under `./checkpoints`. Push the best one to
Hugging Face after training:

```python
from huggingface_hub import HfApi
api = HfApi()
api.upload_folder(
    folder_path="./checkpoints/best",
    repo_id="shotcowboystyle/my-model",
    repo_type="model",
    commit_message="finetune: epoch 3, val acc 0.94",
)
```

## Running Plugin Eval with W&B Logging

The `eval-report.yml` workflow supports a `log_wandb` dispatch input that
pushes per-plugin scores to W&B. To run it manually from the GitHub Actions
UI, set `log_wandb = true`.

Or run the same static sweep locally. The script runs the static layer
only, so it doesn't need a GPU or a model:

```bash
cd plugins/plugin-eval
uv run python scripts/eval_all.py --output-dir /tmp/eval-reports
```

The W&B logging step reads `eval-reports/summary.json` and logs a table plus
aggregate metrics to the `shotcowboystyle-lab` project.

## Releasing a Model via GitHub Actions

Tag a commit with a `model/*` prefix to trigger the release job in
`mlops.yml`:

```bash
git tag model/my-model-v1
git push origin model/my-model-v1
```

This pushes the directory `my-model-v1/` (relative to the repo root) to
Hugging Face as `shotcowboystyle/my-model-v1`.

For a manual dispatch, set `kind = release`, `hf_target = shotcowboystyle/my-model`,
and `model_path = path/to/local/model/dir`.

## W&B Project Layout

All runs land under `wandb.ai/shotcowboystyle/shotcowboystyle-lab`. Use tags to organize:

| Tag              | Meaning                        |
| ---------------- | ------------------------------ |
| `fine-tune`      | Fine-tuning runs               |
| `plugin-eval`    | Plugin quality eval runs       |
| `dgx-spark`      | Runs executed on the DGX Spark |
| `github-actions` | Runs triggered from CI         |

Group related runs with `group=` in `wandb.init()` so they collapse into a
single row in the project table.

## Offline Mode

If the network is unstable, set `WANDB_MODE=offline` before starting a run.
Runs sync later with:

```bash
wandb sync ./wandb/offline-run-<timestamp>-<id>
```

## Troubleshooting

| Symptom                                              | Fix                                                                                        |
| ---------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| `you may not log runs directly to your organization` | Use the team entity (`shotcowboystyle`), not the org entity (`shotcowboystyle-org`)        |
| W&B run stuck in "syncing"                           | Check network; run `wandb sync <run-dir>` manually                                         |
| `hf_transfer` errors on upload                       | Set `HF_HUB_ENABLE_HF_TRANSFER=0` and retry; fall back to standard HTTP                    |
| GitHub Actions HF push fails with 403                | Verify `HF_TOKEN` secret has `write` role and covers the `shotcowboystyle` org             |
| `import torch` hangs on the DGX                      | Use a lighter probe or run inside the activated `unsloth` env; first CUDA init can be slow |
