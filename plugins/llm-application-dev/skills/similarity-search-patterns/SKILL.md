---
name: similarity-search-patterns
description: Implement nearest-neighbor search against a vector database (Pinecone, Qdrant, pgvector, Weaviate) and choose a distance metric. Use when building semantic search, writing vector store client code, or adding metadata filters to vector queries.
last_verified: 2026-10-27
---

# Similarity Search Patterns

Client code and distance metrics for vector databases.

This skill owns vector store clients and distance metrics. Related topics live elsewhere:

| Topic | Owner |
| --- | --- |
| Chunking, embedding model choice | [embedding-strategies](../embedding-strategies/SKILL.md) |
| Hybrid search, RRF, reranking | [hybrid-search-implementation](../hybrid-search-implementation/SKILL.md) |
| Index type, HNSW parameters, quantization | [vector-index-tuning](../vector-index-tuning/SKILL.md) |

## When to Use This Skill

- Writing upsert / query / delete code for a vector store
- Adding metadata filters to vector queries
- Choosing a distance metric for an embedding model

## Distance Metrics

| Metric | Formula | Use when |
| --- | --- | --- |
| **Cosine** | 1 − (A·B) / (‖A‖ ‖B‖) | Default for text embeddings |
| **Dot product** | A·B | Vectors are normalized (same ranking as cosine, cheaper) or magnitude carries meaning |
| **Euclidean (L2)** | √Σ(aᵢ − bᵢ)² | The model was trained with an L2 objective |
| **Manhattan (L1)** | Σ abs(aᵢ − bᵢ) | Rare for embeddings; some sparse features |

Use the metric the embedding model's documentation names. A mismatch quietly degrades
ranking.

## Procedure

1. Pick the metric from the model card; create the collection/index with it and the
   model's exact output dimension.
2. Store the source text (or a pointer to it) and filterable fields as metadata/payload
   next to each vector.
3. Upsert in batches; make IDs deterministic (hash of document ID + chunk index) so
   re-ingestion overwrites instead of duplicating.
4. Query with `top_k` and metadata filters. Prefer the store's native filter over
   post-filtering in Python, which can return fewer than `top_k` results.
5. Measure recall@k against exact (brute-force) search on a sample of real queries before
   tuning anything; see [vector-index-tuning](../vector-index-tuning/SKILL.md).

## Current client APIs (as of 2026-10)

- **Qdrant**: `client.query_points(collection_name, query=vector, ...)`. `client.search`
  was removed.
- **Weaviate**: client v4, `weaviate.connect_to_local()` then
  `client.collections.get(name).query.near_vector(...)`. The v3 `weaviate.Client` is gone.
- **Pinecone**: `Pinecone(api_key=...)`, `pc.has_index(name)`, `pc.Index(name).query(...)`.
- **pgvector**: `embedding <=> $1::vector` (cosine distance), `<->` (L2), `<#>` (negative
  inner product). Bind metadata keys as parameters, never interpolate them into SQL.

## Templates

Full client classes for Pinecone, Qdrant (with a runnable in-memory check), pgvector and
Weaviate v4 live in [references/details.md](references/details.md).

## Best Practices

### Do's

- **Batch upserts** - one request per vector is slow and rate-limited
- **Filter in the database** - native metadata filters keep `top_k` full
- **Keep the embedding model fixed per collection** - vectors from different models are
  not comparable
- **Monitor recall** - measure search quality, not only latency

### Don'ts

- **Don't skip evaluation** - measure before optimizing
- **Don't interpolate filter keys into SQL** - it is an injection path
- **Don't forget costs** - vector storage and read units add up
