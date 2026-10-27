---
name: hybrid-search-implementation
description: Combine vector and keyword (BM25 / full-text) search with Reciprocal Rank Fusion, weighted fusion and reranking. Use when implementing RAG retrieval, when pure vector search misses exact terms (names, codes, IDs), or when tuning how ranked lists are fused.
last_verified: 2026-10-27
---

# Hybrid Search Implementation

Combine vector similarity and keyword search, then fuse and optionally rerank.

This skill owns hybrid search, fusion and reranking. Related topics:

| Topic | Owner |
| --- | --- |
| Vector store clients, distance metrics | [similarity-search-patterns](../similarity-search-patterns/SKILL.md) |
| Chunking, embedding models | [embedding-strategies](../embedding-strategies/SKILL.md) |
| HNSW parameters, quantization | [vector-index-tuning](../vector-index-tuning/SKILL.md) |

## When to Use This Skill

- Queries contain exact terms (product codes, names, error strings) that embeddings blur
- Building RAG retrieval that needs better recall than vector search alone
- Choosing between RRF, weighted score fusion and cross-encoder reranking

## Architecture

```
Query ─┬─► Vector search  ─► top-N ranked IDs ─┐
       │                                        ├─► Fusion ─► (Rerank) ─► top-k
       └─► Keyword search ─► top-N ranked IDs ─┘
```

## Reciprocal Rank Fusion (RRF)

```
RRF(d) = Σ_i  w_i / (k + rank_i(d))
```

- `rank_i(d)` is the **1-based** position of document `d` in retriever `i`'s list. A
  document absent from a list adds nothing for that list.
- `k = 60` is the conventional constant (Cormack et al., 2009). Larger `k` flattens the
  difference between top and lower ranks.
- `w_i` defaults to 1. Weights are optional and should be tuned on labeled queries.
- RRF ignores raw scores, so BM25 and cosine scores never need normalizing.

```python
from collections import defaultdict

def reciprocal_rank_fusion(result_lists, k=60, weights=None):
    weights = weights or [1.0] * len(result_lists)
    scores = defaultdict(float)
    for ranked, w in zip(result_lists, weights, strict=True):
        for rank, doc_id in enumerate(ranked, start=1):
            scores[doc_id] += w / (k + rank)
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)

assert [d for d, _ in reciprocal_rank_fusion([["a", "b"], ["b", "c"]])] == ["b", "a", "c"]
```

## Fusion Methods

| Method | How | Use when |
| --- | --- | --- |
| **RRF** | Sum of 1/(k + rank) | Default; no score calibration needed |
| **Linear** | α·norm(vector) + (1−α)·norm(keyword) | You have labeled queries to tune α |
| **Cross-encoder rerank** | Score (query, passage) pairs with a reranking model | Precision on the final top-k matters more than latency |
| **Native engine fusion** | Qdrant `FusionQuery(RRF)`, Weaviate `query.hybrid`, Elasticsearch `rrf` retriever | The store already holds both representations |

## Procedure

1. Run both retrievers with the same metadata filter and a candidate count `N` per
   retriever (`N` ≥ final `k`, commonly a few times larger).
2. Fuse ranked ID lists with RRF. Keep each retriever's rank on the result for debugging.
3. Optionally rerank the top fused candidates with a cross-encoder, then cut to `k`.
4. Evaluate on labeled queries (recall@k, nDCG@k) against vector-only and keyword-only
   baselines. Keep hybrid only if it measurably wins.

## Pitfalls

- **Limits computed by integer division** (`LIMIT $3 / 3`) can round to 0. Pass the
  candidate count and the final limit as separate parameters.
- **Positional SQL parameters after dynamic filters**: append filter parameters after the
  fixed ones so `$4`/`$5` never shift.
- **Filtering only one retriever** lets the other leak documents the user may not see.
  Apply the same filter to both.
- **Comparing fused scores across engines**: each engine scales them differently.

## Templates

[references/details.md](references/details.md) has: runnable RRF and linear fusion with
self-checks, a PostgreSQL pgvector + full-text query with RRF in SQL, Elasticsearch `rrf`
retriever, native Qdrant and Weaviate hybrid queries, and a hybrid RAG pipeline with
cross-encoder reranking.

## Best Practices

- **Start with RRF** - it works without tuning
- **Log both ranks** - shows which retriever found each result
- **Tune weights on your data** - never copy weights from another corpus
- **Handle empty keyword results** - single-word or stopword-only queries return nothing
  from full-text search; RRF still returns the vector results
