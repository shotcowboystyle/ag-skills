---
name: embedding-strategies
description: Choose an embedding model and a chunking strategy for semantic search and RAG. Use when choosing embedding models, splitting documents into chunks, reducing embedding dimensions, or evaluating embedding quality on a specific domain.
last_verified: 2026-10-27
---

# Embedding Strategies

Choosing embedding models and chunking documents for vector search.

This skill owns embedding model choice and chunking. Related topics:

| Topic | Owner |
| --- | --- |
| Vector store clients, distance metrics | [similarity-search-patterns](../similarity-search-patterns/SKILL.md) |
| Hybrid search, RRF, reranking | [hybrid-search-implementation](../hybrid-search-implementation/SKILL.md) |
| Index parameters, quantization | [vector-index-tuning](../vector-index-tuning/SKILL.md) |

## When to Use This Skill

- Choosing an embedding model for RAG or semantic search
- Choosing chunk size, overlap and split boundaries
- Reducing embedding dimensions (Matryoshka truncation)
- Handling code, multilingual or domain-specific content
- Comparing embedding models on your own queries

## Embedding Models (as of 2026-10)

Model lineups change often. Dimensions, context limits and prices are configurable or
change between releases: check the provider's docs before you size an index.

| Model family | Provider | Notes |
| --- | --- | --- |
| `voyage-4-large`, `voyage-4`, `voyage-4-lite` | Voyage AI | General text; Anthropic's docs point to Voyage for embeddings with Claude |
| `voyage-code-4` | Voyage AI | Code search |
| `voyage-context-4` | Voyage AI | Contextualized chunk embeddings (chunk encoded with its document context) |
| `voyage-finance-2`, `voyage-law-2` | Voyage AI | Finance and legal domains |
| `text-embedding-3-large`, `text-embedding-3-small` | OpenAI | Supports `dimensions` to truncate output |
| `BAAI/bge-*`, `intfloat/multilingual-e5-*`, `sentence-transformers/all-MiniLM-L6-v2` | Open source | Run locally; check each model card for query/passage prefixes and token limit |

Pick by measured retrieval quality on your own labeled queries (Template 6 in the
references), not by leaderboard rank alone.

## Chunking

| Strategy | Use when |
| --- | --- |
| Recursive character/token splitting (`RecursiveCharacterTextSplitter`) | Default for prose |
| Header-aware (`MarkdownHeaderTextSplitter`, then size-limit) | Markdown, docs sites; keeps the header path as metadata |
| Sentence packing | Short-form text where sentence boundaries matter |
| Syntax-aware (tree-sitter functions/classes) | Source code |
| Fixed token windows with overlap | Uniform inputs, or when you need exact token budgets |

Rules:

- Size chunks in **tokens of the embedding model's tokenizer**, and stay under its input
  limit. Truncation silently drops text.
- Overlap must be smaller than the chunk size. Start around 10–20% and measure.
- Keep `document_id`, `chunk_index` and the section/header path as metadata on every chunk.
- Re-chunking or switching models means re-embedding the whole corpus. Vectors from
  different models are not comparable.

## Pipeline

```
Document → Clean → Chunk → Embed (batched) → Store with metadata
                     ↑
       size + overlap in model tokens
```

## Templates

[references/details.md](references/details.md) has: Voyage and OpenAI embedding clients,
local sentence-transformers (BGE / E5 prefixes), chunkers with runnable self-checks,
domain and code (tree-sitter) pipelines, and a retrieval-quality evaluator (precision,
recall, MRR, nDCG).

## Best Practices

### Do's

- **Match model to content**: code vs prose vs multilingual
- **Use the model's query/document modes**: `embed_query` vs `embed_documents`, or the
  model's documented prefixes (E5 `query:` / `passage:`)
- **Normalize embeddings** when the store uses dot product
- **Batch requests and cache** embeddings for unchanged content

### Don'ts

- **Don't ignore token limits**: truncation loses information
- **Don't mix embedding models** in one collection
- **Don't strip meaningful characters** in preprocessing (code symbols, units, IDs)
- **Don't forget metadata**: needed for filtering, citations and debugging
