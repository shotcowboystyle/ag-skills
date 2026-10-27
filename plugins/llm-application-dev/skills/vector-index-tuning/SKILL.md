---
name: vector-index-tuning
description: Optimize vector index performance for latency, recall, and memory. Use when tuning HNSW parameters, selecting quantization strategies, or scaling vector search infrastructure.
last_verified: 2026-10-27
---

# Vector Index Tuning

Guide to optimizing vector indexes for production performance.

This skill owns index type selection, HNSW parameters, quantization and store-level index
configuration (for example Qdrant `hnsw_config` / `quantization_config`). Client code lives
in [similarity-search-patterns](../similarity-search-patterns/SKILL.md); hybrid search in
[hybrid-search-implementation](../hybrid-search-implementation/SKILL.md).

## When to Use This Skill

- Tuning HNSW parameters
- Implementing quantization
- Optimizing memory usage
- Reducing search latency
- Balancing recall vs speed
- Scaling to billions of vectors

## Core Concepts

### 1. Index Type Selection

Rough starting points by corpus size; your recall/latency/memory budget decides.

```
Data Size           Starting point
────────────────────────────────────────
< 10K vectors  →    Flat (exact search)
10K - 1M       →    HNSW
1M - 100M      →    HNSW + Quantization
> 100M         →    IVF + PQ or DiskANN
```

### 2. HNSW Parameters

Defaults differ by engine (hnswlib, pgvector, Qdrant, FAISS); check yours.

| Parameter          | Typical | Effect                                               |
| ------------------ | ------- | ---------------------------------------------------- |
| **M**              | 16      | Connections per node, ↑ = better recall, more memory |
| **efConstruction** | 100     | Build quality, ↑ = better index, slower build        |
| **efSearch**       | 50      | Search quality, ↑ = better recall, slower search     |

### 3. Quantization Types

```
Full Precision (FP32): 4 bytes × dimensions
Half Precision (FP16): 2 bytes × dimensions
INT8 Scalar:           1 byte × dimensions
Product Quantization:  ~32-64 bytes total
Binary:                dimensions/8 bytes
```

## Procedure

1. Build exact (brute-force) top-k ground truth for a sample of real queries.
2. Start from engine defaults; measure recall@k, p50/p99 latency and memory.
3. Raise `efSearch` (query time) first; it needs no rebuild. Raise `M` / `efConstruction`
   only if recall plateaus below target.
4. Add quantization when memory is the constraint, with rescoring on full-precision
   vectors; re-measure recall.
5. Record the chosen parameters with the measured numbers. Write "needs measurement"
   rather than quoting numbers you did not measure.

## Templates

[references/details.md](references/details.md) has: an hnswlib parameter sweep with a
runnable recall check, int8 / product / binary quantization, a memory estimator, Qdrant
collection and search-parameter presets with a runnable in-memory recall check, and a
latency/recall monitor.

## Best Practices

### Do's

- **Benchmark with real queries** - Synthetic may not represent production
- **Monitor recall continuously** - Can degrade with data drift
- **Start with defaults** - Tune only when needed
- **Use quantization** - Significant memory savings
- **Consider tiered storage** - Hot/cold data separation

### Don'ts

- **Don't over-optimize early** - Profile first
- **Don't ignore build time** - Index updates have cost
- **Don't forget reindexing** - Plan for maintenance
- **Don't skip warming** - Cold indexes are slow
