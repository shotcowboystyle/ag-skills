"""Minimal train-evaluate-promote pipeline as an Airflow 3 DAG.

ingest >> validate_data >> train >> evaluate >> promotion_gate >> promote

Run it once without a scheduler (from the directory holding this file):

    pip install "apache-airflow>=3.0" scikit-learn
    export AIRFLOW__CORE__DAGS_FOLDER="$PWD" AIRFLOW__CORE__LOAD_EXAMPLES=False
    airflow db migrate
    airflow dags test ml_pipeline

Or drop the file in your dags/ folder. Tasks pass file paths through XCom, never
data. Swap ingest() and train() for your own source and model; keep the gate.
"""

import json
import os
import shutil
from pathlib import Path

import joblib
import numpy as np
from airflow.sdk import dag, task

HOME = Path(os.environ.get("ML_PIPELINE_HOME", "/tmp/ml_pipeline"))
CHAMPION = HOME / "champion"

# Data gate: fail the run before training on bad input.
MIN_ROWS = 500
MAX_MINORITY_SHARE_DROP = 0.5  # minority class must keep >= 50% of its expected share
EXPECTED_MINORITY_SHARE = 0.37

# Promotion gate: every check must pass, or the champion stays.
MIN_ROC_AUC = 0.95  # absolute floor
MIN_RECALL = 0.90  # recall of the positive class
MAX_AUC_DROP = 0.005  # candidate may trail the champion by at most this much


@dag(schedule=None, catchup=False, tags=["ml"])
def ml_pipeline():
    @task
    def ingest(run_id=None) -> str:
        from sklearn.datasets import load_breast_cancer
        from sklearn.model_selection import train_test_split

        X, y = load_breast_cancer(return_X_y=True)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.25, stratify=y, random_state=42
        )
        run_dir = HOME / "runs" / run_id.replace(":", "_")
        run_dir.mkdir(parents=True, exist_ok=True)
        path = run_dir / "data.npz"
        np.savez(path, X_train=X_train, X_test=X_test, y_train=y_train, y_test=y_test)
        return str(path)

    @task
    def validate_data(path: str) -> str:
        d = np.load(path)
        X, y = d["X_train"], d["y_train"]
        rows = len(X) + len(d["X_test"])
        if rows < MIN_ROWS:
            raise ValueError(f"{rows} rows < MIN_ROWS={MIN_ROWS}")
        if np.isnan(X).any():
            raise ValueError("NaN in training features")
        minority = min(np.bincount(y)) / len(y)
        if minority < EXPECTED_MINORITY_SHARE * MAX_MINORITY_SHARE_DROP:
            raise ValueError(f"minority share {minority:.3f} collapsed")
        return path

    @task
    def train(path: str) -> str:
        from sklearn.linear_model import LogisticRegression
        from sklearn.pipeline import make_pipeline
        from sklearn.preprocessing import StandardScaler

        d = np.load(path)
        model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))
        model.fit(d["X_train"], d["y_train"])
        model_path = Path(path).with_name("model.joblib")
        joblib.dump(model, model_path)
        return str(model_path)

    @task
    def evaluate(model_path: str, path: str) -> dict:
        from sklearn.metrics import recall_score, roc_auc_score

        d = np.load(path)
        model = joblib.load(model_path)
        scores = model.predict_proba(d["X_test"])[:, 1]
        metrics = {
            "roc_auc": float(roc_auc_score(d["y_test"], scores)),
            "recall": float(recall_score(d["y_test"], scores >= 0.5)),
            # The run that produced this model, so you can roll back by re-promoting it.
            "run": Path(model_path).parent.name,
        }
        Path(model_path).with_name("metrics.json").write_text(json.dumps(metrics))
        return {"model_path": model_path, **metrics}

    @task.short_circuit
    def promotion_gate(candidate: dict) -> bool:
        champion_file = CHAMPION / "metrics.json"
        champion = (
            json.loads(champion_file.read_text()) if champion_file.exists() else None
        )
        failures = []
        if candidate["roc_auc"] < MIN_ROC_AUC:
            failures.append(f"roc_auc {candidate['roc_auc']:.4f} < {MIN_ROC_AUC}")
        if candidate["recall"] < MIN_RECALL:
            failures.append(f"recall {candidate['recall']:.4f} < {MIN_RECALL}")
        if champion and candidate["roc_auc"] < champion["roc_auc"] - MAX_AUC_DROP:
            failures.append(
                f"roc_auc {candidate['roc_auc']:.4f} trails champion "
                f"{champion['roc_auc']:.4f} by more than {MAX_AUC_DROP}"
            )
        print("gate:", "PASS" if not failures else "REJECT " + "; ".join(failures))
        return not failures

    @task
    def promote(candidate: dict) -> None:
        # Copy into a staging dir, then swap it in, so a failed copy never leaves a half-written champion.
        staging = HOME / "champion.staging"
        shutil.rmtree(staging, ignore_errors=True)
        staging.mkdir(parents=True)
        src = Path(candidate["model_path"])
        shutil.copy2(src, staging / "model.joblib")
        shutil.copy2(src.with_name("metrics.json"), staging / "metrics.json")
        shutil.rmtree(CHAMPION, ignore_errors=True)
        staging.rename(CHAMPION)

    data = validate_data(ingest())
    candidate = evaluate(train(data), data)
    promotion_gate(candidate) >> promote(candidate)


ml_pipeline()
