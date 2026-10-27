---
name: llm-evaluation
description: Implement comprehensive evaluation strategies for LLM applications using automated metrics, human feedback, and benchmarking. Use when testing LLM performance, measuring AI application quality, or establishing evaluation frameworks.
last_verified: 2026-10-27
---

# LLM Evaluation

Master comprehensive evaluation strategies for LLM applications, from automated metrics to human evaluation and A/B testing.

## When to Use This Skill

- Measuring LLM application performance systematically
- Comparing different models or prompts
- Detecting performance regressions before deployment
- Validating improvements from prompt changes
- Building confidence in production systems
- Establishing baselines and tracking progress over time
- Debugging unexpected model behavior

## Core Evaluation Types

### 1. Automated Metrics

Fast, repeatable, scalable evaluation using computed scores.

**Text Generation:**

- **BLEU**: N-gram overlap (translation)
- **ROUGE**: Recall-oriented (summarization)
- **METEOR**: Semantic similarity
- **BERTScore**: Embedding-based similarity
- **Perplexity**: Language model confidence

**Classification:**

- **Accuracy**: Percentage correct
- **Precision/Recall/F1**: Class-specific performance
- **Confusion Matrix**: Error patterns
- **AUC-ROC**: Ranking quality

**Retrieval (RAG):**

- **MRR**: Mean Reciprocal Rank
- **NDCG**: Normalized Discounted Cumulative Gain
- **Precision@K**: Relevant in top K
- **Recall@K**: Coverage in top K

### 2. Human Evaluation

Manual assessment for quality aspects difficult to automate.

**Dimensions:**

- **Accuracy**: Factual correctness
- **Coherence**: Logical flow
- **Relevance**: Answers the question
- **Fluency**: Natural language quality
- **Safety**: No harmful content
- **Helpfulness**: Useful to the user

### 3. LLM-as-Judge

Use stronger LLMs to evaluate weaker model outputs.

**Approaches:**

- **Pointwise**: Score individual responses
- **Pairwise**: Compare two responses
- **Reference-based**: Compare to gold standard
- **Reference-free**: Judge without ground truth

## Quick Start

A self-contained harness: plain metric functions with one signature, an async model
callable, and mean scores per metric. Swap `fake_model` for your chain
(`lambda q: chain.ainvoke(q)`) and add metrics from `references/details.md`.

```python
import asyncio
import re
from collections import Counter
from statistics import mean
from typing import Awaitable, Callable

# Every metric: (prediction, reference, context) -> score in [0, 1]
Metric = Callable[[str, str | None, str | None], float]


def _tokens(text: str) -> list[str]:
    return re.findall(r"\w+", text.lower())


def exact_match(prediction, reference, context=None) -> float:
    return float(_tokens(prediction) == _tokens(reference or ""))


def token_f1(prediction, reference, context=None) -> float:
    pred, ref = _tokens(prediction), _tokens(reference or "")
    common = sum((Counter(pred) & Counter(ref)).values())
    if not common:
        return 0.0
    precision, recall = common / len(pred), common / len(ref)
    return 2 * precision * recall / (precision + recall)


def context_overlap(prediction, reference=None, context=None) -> float:
    """Cheap groundedness proxy: share of answer tokens found in the context.
    Use an NLI model or LLM judge (references/details.md) for real faithfulness."""
    pred = _tokens(prediction)
    return sum(t in set(_tokens(context or "")) for t in pred) / len(pred) if pred else 0.0


async def evaluate(
    model: Callable[[str], Awaitable[str]],
    test_cases: list[dict],
    metrics: dict[str, Metric],
) -> dict:
    predictions = await asyncio.gather(*(model(t["input"]) for t in test_cases))
    raw = {
        name: [fn(p, t.get("expected"), t.get("context")) for p, t in zip(predictions, test_cases)]
        for name, fn in metrics.items()
    }
    return {"metrics": {name: mean(scores) for name, scores in raw.items()}, "raw": raw}


async def fake_model(question: str) -> str:  # replace with your application
    return "Paris"


test_cases = [
    {
        "input": "What is the capital of France?",
        "expected": "Paris",
        "context": "France is a country in Europe. Paris is its capital.",
    },
]

results = asyncio.run(
    evaluate(
        fake_model,
        test_cases,
        {"exact_match": exact_match, "token_f1": token_f1, "grounded": context_overlap},
    )
)
print(results["metrics"])  # {'exact_match': 1.0, 'token_f1': 1.0, 'grounded': 1.0}
```

## Detailed patterns and worked examples

Detailed pattern documentation lives in `references/details.md`. Read that file when the navigation tier above is insufficient.

