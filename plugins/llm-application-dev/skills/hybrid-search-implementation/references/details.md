# hybrid-search-implementation — templates and worked examples

Verified against asyncpg 0.32, elasticsearch-py 9.5, qdrant-client 1.20 and
weaviate-client 4.24 (2026-10-27). Store client setup (connections, collections, upserts)
lives in [similarity-search-patterns](../../similarity-search-patterns/references/details.md).

## Templates

### Template 1: Fusion functions (pure Python, runnable)

```python
from collections import defaultdict


def reciprocal_rank_fusion(
    result_lists: list[list[str]],
    k: int = 60,
    weights: list[float] | None = None,
) -> list[tuple[str, float]]:
    """RRF: score(d) = sum_i w_i / (k + rank_i(d)), rank is 1-based.

    result_lists: one ranked list of doc IDs per retriever, best first.
    Documents missing from a list contribute nothing for that list.
    """
    weights = weights or [1.0] * len(result_lists)
    scores: dict[str, float] = defaultdict(float)
    for ranked, weight in zip(result_lists, weights, strict=True):
        for rank, doc_id in enumerate(ranked, start=1):
            scores[doc_id] += weight / (k + rank)
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)


def linear_combination(
    vector_results: list[tuple[str, float]],
    keyword_results: list[tuple[str, float]],
    alpha: float = 0.5,
) -> list[tuple[str, float]]:
    """alpha * norm(vector) + (1 - alpha) * norm(keyword), min-max normalized per list."""

    def normalize(results):
        if not results:
            return {}
        scores = [s for _, s in results]
        lo, hi = min(scores), max(scores)
        span = (hi - lo) or 1.0
        return {doc_id: (s - lo) / span for doc_id, s in results}

    v, kw = normalize(vector_results), normalize(keyword_results)
    combined = {
        d: alpha * v.get(d, 0.0) + (1 - alpha) * kw.get(d, 0.0) for d in v.keys() | kw.keys()
    }
    return sorted(combined.items(), key=lambda x: x[1], reverse=True)


if __name__ == "__main__":
    fused = reciprocal_rank_fusion([["a", "b", "c"], ["b", "c", "d"]])
    # b: 1/62 + 1/61 beats a: 1/61 alone
    assert [d for d, _ in fused] == ["b", "c", "a", "d"]
    assert abs(dict(fused)["a"] - 1 / 61) < 1e-12
    assert reciprocal_rank_fusion([[], []]) == []
    lin = linear_combination([("a", 0.9), ("b", 0.1)], [("b", 12.0), ("c", 3.0)], alpha=0.5)
    assert lin[0][0] == "b"
```

### Template 2: PostgreSQL (pgvector + full-text) with RRF in SQL

Bind parameter positions are fixed (`$1`–`$5`); filter parameters are appended after them,
so adding a filter never shifts `$4` or `$5`. The candidate count per retriever is its own
parameter, so no integer division can shrink the final `LIMIT` to 0.

```python
import asyncpg


class PostgresHybridSearch:
    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool

    async def setup_schema(self, dimension: int):
        async with self.pool.acquire() as conn:
            await conn.execute(f"""
                CREATE EXTENSION IF NOT EXISTS vector;

                CREATE TABLE IF NOT EXISTS documents (
                    id TEXT PRIMARY KEY,
                    content TEXT NOT NULL,
                    embedding vector({int(dimension)}),
                    metadata JSONB NOT NULL DEFAULT '{{}}',
                    ts_content tsvector GENERATED ALWAYS AS (
                        to_tsvector('english', content)
                    ) STORED
                );

                CREATE INDEX IF NOT EXISTS documents_embedding_idx
                ON documents USING hnsw (embedding vector_cosine_ops);

                CREATE INDEX IF NOT EXISTS documents_fts_idx
                ON documents USING gin (ts_content);
            """)

    async def hybrid_search(
        self,
        query: str,
        query_embedding: list[float],
        limit: int = 10,
        candidates: int = 50,  # per retriever, >= limit
        vector_weight: float = 0.5,
        filter_metadata: dict[str, str] | None = None,
    ) -> list[dict]:
        params: list = [str(query_embedding), query, max(candidates, limit), vector_weight, limit]
        where = ["TRUE"]
        for key, value in (filter_metadata or {}).items():
            params += [key, value]
            where.append(f"metadata->>${len(params) - 1} = ${len(params)}")
        where_sql = " AND ".join(where)

        sql = f"""
            WITH vector_search AS (
                SELECT id, ROW_NUMBER() OVER (ORDER BY embedding <=> $1::vector) AS rnk
                FROM documents
                WHERE {where_sql}
                ORDER BY embedding <=> $1::vector
                LIMIT $3
            ),
            keyword_search AS (
                SELECT id, ROW_NUMBER() OVER (
                    ORDER BY ts_rank(ts_content, websearch_to_tsquery('english', $2)) DESC
                ) AS rnk
                FROM documents
                WHERE ts_content @@ websearch_to_tsquery('english', $2) AND {where_sql}
                ORDER BY ts_rank(ts_content, websearch_to_tsquery('english', $2)) DESC
                LIMIT $3
            ),
            fused AS (
                SELECT COALESCE(v.id, k.id) AS id,
                       v.rnk AS vector_rank,
                       k.rnk AS keyword_rank,
                       COALESCE($4::float8 / (60 + v.rnk), 0)
                     + COALESCE((1 - $4::float8) / (60 + k.rnk), 0) AS rrf_score
                FROM vector_search v
                FULL OUTER JOIN keyword_search k ON v.id = k.id
            )
            SELECT d.id, d.content, d.metadata, f.vector_rank, f.keyword_rank, f.rrf_score
            FROM fused f JOIN documents d USING (id)
            ORDER BY f.rrf_score DESC
            LIMIT $5
        """
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(sql, *params)
        return [dict(r) for r in rows]
```

To rerank, call `hybrid_search(..., limit=candidates)` and pass the rows to a cross-encoder
(Template 5).

### Template 3: Elasticsearch retrievers (8.16+, 9.x)

The `rrf` retriever replaces the older `sub_searches` + `rank.rrf` request body. Whether RRF
needs a paid license tier depends on the Elasticsearch version; check your deployment.

```python
from elasticsearch import Elasticsearch


class ElasticsearchHybridSearch:
    def __init__(self, es: Elasticsearch, index_name: str = "documents"):
        self.es = es
        self.index_name = index_name

    def create_index(self, vector_dims: int):
        if self.es.indices.exists(index=self.index_name):
            return
        self.es.indices.create(
            index=self.index_name,
            mappings={
                "properties": {
                    "content": {"type": "text", "analyzer": "english"},
                    "embedding": {
                        "type": "dense_vector",
                        "dims": vector_dims,
                        "index": True,
                        "similarity": "cosine",
                    },
                    "metadata": {"type": "object"},
                }
            },
        )

    def hybrid_search_rrf(
        self,
        query: str,
        query_embedding: list[float],
        limit: int = 10,
        rank_window_size: int = 100,
        filter: list[dict] | None = None,  # e.g. [{"term": {"metadata.source": "kb"}}]
    ) -> list[dict]:
        response = self.es.search(
            index=self.index_name,
            size=limit,
            retriever={
                "rrf": {
                    "retrievers": [
                        {"standard": {"query": {"bool": {
                            "must": {"match": {"content": query}},
                            "filter": filter or [],
                        }}}},
                        {"knn": {
                            "field": "embedding",
                            "query_vector": query_embedding,
                            "k": rank_window_size,
                            "num_candidates": rank_window_size * 2,
                            "filter": filter or [],
                        }},
                    ],
                    "rank_window_size": rank_window_size,
                    "rank_constant": 60,
                }
            },
        )
        return [
            {"id": h["_id"], "content": h["_source"]["content"], "score": h["_score"]}
            for h in response["hits"]["hits"]
        ]
```

### Template 4: Native fusion in Qdrant and Weaviate

```python
from qdrant_client import QdrantClient, models

# Collection needs a named dense vector and a named sparse vector:
#   vectors_config={"dense": models.VectorParams(size=DIM, distance=models.Distance.COSINE)},
#   sparse_vectors_config={"sparse": models.SparseVectorParams()}
def qdrant_hybrid(
    client: QdrantClient,
    collection: str,
    dense: list[float],
    sparse: models.SparseVector,  # e.g. from a BM25 / SPLADE encoder
    limit: int = 10,
    candidates: int = 50,
):
    return client.query_points(
        collection_name=collection,
        prefetch=[
            models.Prefetch(query=dense, using="dense", limit=candidates),
            models.Prefetch(query=sparse, using="sparse", limit=candidates),
        ],
        query=models.FusionQuery(fusion=models.Fusion.RRF),
        limit=limit,
    ).points
```

```python
import weaviate
from weaviate.classes.query import HybridFusion, MetadataQuery


def weaviate_hybrid(
    client: weaviate.WeaviateClient,
    collection: str,
    query: str,
    query_vector: list[float],
    alpha: float = 0.5,  # 0 = pure BM25, 1 = pure vector
    limit: int = 10,
):
    response = client.collections.get(collection).query.hybrid(
        query=query,
        vector=query_vector,
        alpha=alpha,
        fusion_type=HybridFusion.RANKED,  # RRF-style; RELATIVE_SCORE = normalized linear
        limit=limit,
        return_metadata=MetadataQuery(score=True),
    )
    return [{"id": str(o.uuid), **o.properties, "score": o.metadata.score}
            for o in response.objects]
```

Each engine scales its fused scores differently. Compare ranks across engines, not raw
scores.

### Template 5: Hybrid RAG pipeline with optional reranking

Retriever objects are duck-typed: each needs an async `search(query_or_vector, limit,
filter) -> list[dict]` returning dicts with `id` and `content`. The reranker is anything with
`predict(list[tuple[str, str]]) -> list[float]`, for example
`sentence_transformers.CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")` loaded once at
startup.

```python
import asyncio
from dataclasses import dataclass, field

# reciprocal_rank_fusion from Template 1


@dataclass
class SearchResult:
    id: str
    content: str
    score: float
    metadata: dict = field(default_factory=dict)


class HybridRAGPipeline:
    def __init__(self, vector_store, keyword_store, embedder, reranker=None):
        self.vector_store = vector_store
        self.keyword_store = keyword_store
        self.embedder = embedder
        self.reranker = reranker

    async def search(self, query: str, top_k: int = 10, filter: dict | None = None,
                     candidates: int = 50) -> list[SearchResult]:
        query_embedding = await self.embedder.aembed_query(query)
        vector_hits, keyword_hits = await asyncio.gather(
            self.vector_store.search(query_embedding, candidates, filter),
            self.keyword_store.search(query, candidates, filter),
        )
        by_id = {h["id"]: h for h in keyword_hits} | {h["id"]: h for h in vector_hits}
        fused = reciprocal_rank_fusion(
            [[h["id"] for h in vector_hits], [h["id"] for h in keyword_hits]]
        )
        results = [
            SearchResult(id=d, content=by_id[d]["content"], score=s,
                         metadata=by_id[d].get("metadata", {}))
            for d, s in fused
        ]
        if self.reranker and results:
            pool = results[: max(top_k * 2, top_k)]
            scores = await asyncio.to_thread(
                self.reranker.predict, [(query, r.content) for r in pool]
            )
            for r, s in zip(pool, scores):
                r.score = float(s)
            results = sorted(pool, key=lambda r: r.score, reverse=True)
        return results[:top_k]
```
