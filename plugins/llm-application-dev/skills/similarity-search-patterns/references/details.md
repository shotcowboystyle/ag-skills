# similarity-search-patterns — templates and worked examples

Client templates for the four common vector stores. Verified against pinecone 10.2,
qdrant-client 1.20, asyncpg 0.32 and weaviate-client 4.24 (2026-10-27).

Not covered here: index parameters and quantization
([vector-index-tuning](../../vector-index-tuning/SKILL.md)), hybrid search, fusion and
reranking ([hybrid-search-implementation](../../hybrid-search-implementation/SKILL.md)),
chunking ([embedding-strategies](../../embedding-strategies/SKILL.md)).

## Templates

### Template 1: Pinecone (serverless)

```python
from pinecone import Pinecone, ServerlessSpec

class PineconeVectorStore:
    def __init__(
        self,
        api_key: str,
        index_name: str,
        dimension: int,
        metric: str = "cosine",
    ):
        self.pc = Pinecone(api_key=api_key)
        if not self.pc.has_index(index_name):
            self.pc.create_index(
                name=index_name,
                dimension=dimension,
                metric=metric,
                spec=ServerlessSpec(cloud="aws", region="us-east-1"),
            )
        self.index = self.pc.Index(index_name)

    def upsert(self, vectors: list[dict], namespace: str = "", batch_size: int = 100) -> int:
        """vectors: [{"id": str, "values": list[float], "metadata": dict}]"""
        for i in range(0, len(vectors), batch_size):
            self.index.upsert(vectors=vectors[i:i + batch_size], namespace=namespace)
        return len(vectors)

    def search(
        self,
        query_vector: list[float],
        top_k: int = 10,
        namespace: str = "",
        filter: dict | None = None,
    ) -> list[dict]:
        results = self.index.query(
            vector=query_vector,
            top_k=top_k,
            namespace=namespace,
            filter=filter,  # e.g. {"source": {"$eq": "handbook"}}
            include_metadata=True,
        )
        return [{"id": m.id, "score": m.score, "metadata": m.metadata} for m in results.matches]

    def delete(self, ids: list[str], namespace: str = ""):
        self.index.delete(ids=ids, namespace=namespace)
```

### Template 2: Qdrant

`client.search` was removed from qdrant-client; use `query_points`.

```python
from qdrant_client import QdrantClient, models

class QdrantVectorStore:
    def __init__(
        self,
        client: QdrantClient,  # QdrantClient(url="http://localhost:6333") or QdrantClient(":memory:")
        collection_name: str,
        vector_size: int,
    ):
        self.client = client
        self.collection_name = collection_name
        if not client.collection_exists(collection_name):
            client.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(
                    size=vector_size, distance=models.Distance.COSINE
                ),
                # HNSW and quantization settings: see vector-index-tuning
            )

    def upsert(self, points: list[dict]) -> int:
        """points: [{"id": int | uuid-str, "vector": list[float], "payload": dict}]"""
        self.client.upsert(
            collection_name=self.collection_name,
            points=[
                models.PointStruct(id=p["id"], vector=p["vector"], payload=p.get("payload", {}))
                for p in points
            ],
        )
        return len(points)

    def search(
        self,
        query_vector: list[float],
        limit: int = 10,
        must: dict | None = None,  # {"payload_key": value, ...}, all must match
        score_threshold: float | None = None,
    ) -> list[dict]:
        query_filter = None
        if must:
            query_filter = models.Filter(must=[
                models.FieldCondition(key=k, match=models.MatchValue(value=v))
                for k, v in must.items()
            ])
        response = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            query_filter=query_filter,
            limit=limit,
            score_threshold=score_threshold,
            with_payload=True,
        )
        return [{"id": p.id, "score": p.score, "payload": p.payload} for p in response.points]


if __name__ == "__main__":
    store = QdrantVectorStore(QdrantClient(":memory:"), "docs", vector_size=3)
    store.upsert([
        {"id": 1, "vector": [1.0, 0.0, 0.0], "payload": {"lang": "en"}},
        {"id": 2, "vector": [0.0, 1.0, 0.0], "payload": {"lang": "de"}},
    ])
    assert store.search([0.9, 0.1, 0.0], limit=1)[0]["id"] == 1
    assert store.search([0.9, 0.1, 0.0], must={"lang": "de"})[0]["id"] == 2
```

### Template 3: pgvector with PostgreSQL

Metadata keys and values both go in as bind parameters. Never format a caller-supplied key
into the SQL string.

```python
import json
import asyncpg

class PgVectorStore:
    def __init__(self, pool: asyncpg.Pool, dimension: int):
        self.pool = pool
        self.dimension = int(dimension)

    async def init(self):
        async with self.pool.acquire() as conn:
            await conn.execute("CREATE EXTENSION IF NOT EXISTS vector")
            await conn.execute(f"""
                CREATE TABLE IF NOT EXISTS documents (
                    id TEXT PRIMARY KEY,
                    content TEXT NOT NULL,
                    metadata JSONB NOT NULL DEFAULT '{{}}',
                    embedding vector({self.dimension})
                )
            """)
            # Index choice and m / ef_construction: see vector-index-tuning
            await conn.execute("""
                CREATE INDEX IF NOT EXISTS documents_embedding_idx
                ON documents USING hnsw (embedding vector_cosine_ops)
            """)

    async def upsert(self, documents: list[dict]):
        """documents: [{"id", "content", "embedding": list[float], "metadata": dict}]"""
        async with self.pool.acquire() as conn:
            await conn.executemany(
                """
                INSERT INTO documents (id, content, metadata, embedding)
                VALUES ($1, $2, $3::jsonb, $4::vector)
                ON CONFLICT (id) DO UPDATE SET
                    content = EXCLUDED.content,
                    metadata = EXCLUDED.metadata,
                    embedding = EXCLUDED.embedding
                """,
                [
                    (d["id"], d["content"], json.dumps(d.get("metadata", {})), str(d["embedding"]))
                    for d in documents
                ],
            )

    async def search(
        self,
        query_embedding: list[float],
        limit: int = 10,
        filter_metadata: dict[str, str] | None = None,
    ) -> list[dict]:
        params: list = [str(query_embedding), limit]
        where = []
        for key, value in (filter_metadata or {}).items():
            params += [key, value]
            where.append(f"metadata->>${len(params) - 1} = ${len(params)}")
        sql = f"""
            SELECT id, content, metadata, 1 - (embedding <=> $1::vector) AS similarity
            FROM documents
            {"WHERE " + " AND ".join(where) if where else ""}
            ORDER BY embedding <=> $1::vector
            LIMIT $2
        """
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(sql, *params)
        return [
            {"id": r["id"], "content": r["content"],
             "metadata": json.loads(r["metadata"]), "score": r["similarity"]}
            for r in rows
        ]
```

`str(list_of_floats)` gives `[0.1, 0.2]`, which pgvector accepts as text input. To pass
numpy arrays directly, register the codec from the `pgvector` package
(`pgvector.asyncpg.register_vector`) on each connection instead.

### Template 4: Weaviate (client v4)

The v3 `weaviate.Client` and its `.query.get(...).with_near_vector(...)` builder were removed
in client v4.

```python
import weaviate
from weaviate.classes.config import Configure, DataType, Property
from weaviate.classes.query import Filter, MetadataQuery
from weaviate.util import generate_uuid5

class WeaviateVectorStore:
    def __init__(self, client: weaviate.WeaviateClient, collection_name: str = "Document"):
        # client = weaviate.connect_to_local()  (close it with client.close())
        if not client.collections.exists(collection_name):
            client.collections.create(
                collection_name,
                vector_config=Configure.Vectors.self_provided(),  # we supply vectors
                properties=[
                    Property(name="content", data_type=DataType.TEXT),
                    Property(name="source", data_type=DataType.TEXT),
                    Property(name="chunk_id", data_type=DataType.INT),
                ],
            )
        self.collection = client.collections.get(collection_name)

    def upsert(self, documents: list[dict]):
        """documents: [{"id", "content", "embedding", "source"?, "chunk_id"?}]"""
        with self.collection.batch.fixed_size(batch_size=100) as batch:
            for doc in documents:
                batch.add_object(
                    properties={
                        "content": doc["content"],
                        "source": doc.get("source", ""),
                        "chunk_id": doc.get("chunk_id", 0),
                    },
                    uuid=generate_uuid5(doc["id"]),
                    vector=doc["embedding"],
                )
        if self.collection.batch.failed_objects:
            raise RuntimeError(f"{len(self.collection.batch.failed_objects)} objects failed")

    def search(
        self,
        query_vector: list[float],
        limit: int = 10,
        source: str | None = None,
    ) -> list[dict]:
        response = self.collection.query.near_vector(
            near_vector=query_vector,
            limit=limit,
            filters=Filter.by_property("source").equal(source) if source else None,
            return_metadata=MetadataQuery(distance=True),
        )
        return [
            {"id": str(o.uuid), **o.properties, "score": 1 - o.metadata.distance}
            for o in response.objects
        ]
```

For Weaviate's built-in BM25 + vector fusion (`collection.query.hybrid(query=..., vector=...,
alpha=...)`), see [hybrid-search-implementation](../../hybrid-search-implementation/SKILL.md).
