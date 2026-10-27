# embedding-strategies — templates and worked examples

## Templates

### Template 1: Voyage AI Embeddings

Model names as of 2026-10; check Voyage's docs for the current list, dimensions and
context limits.

```python
from langchain_voyageai import VoyageAIEmbeddings
from typing import List

# Reads VOYAGE_API_KEY from the environment
embeddings = VoyageAIEmbeddings(model="voyage-4-large")

def get_embeddings(texts: List[str]) -> List[List[float]]:
    """Get embeddings from Voyage AI."""
    return embeddings.embed_documents(texts)

def get_query_embedding(query: str) -> List[float]:
    """Get single query embedding."""
    return embeddings.embed_query(query)

# Specialized models (as of 2026-10)
code_embeddings = VoyageAIEmbeddings(model="voyage-code-4")
finance_embeddings = VoyageAIEmbeddings(model="voyage-finance-2")
legal_embeddings = VoyageAIEmbeddings(model="voyage-law-2")
```

### Template 2: OpenAI Embeddings

```python
from openai import OpenAI
from typing import List
import numpy as np

client = OpenAI()

def get_embeddings(
    texts: List[str],
    model: str = "text-embedding-3-small",
    dimensions: int = None
) -> List[List[float]]:
    """Get embeddings from OpenAI with optional dimension reduction."""
    # Handle batching for large lists
    batch_size = 100
    all_embeddings = []

    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]

        kwargs = {"input": batch, "model": model}
        if dimensions:
            # Matryoshka dimensionality reduction
            kwargs["dimensions"] = dimensions

        response = client.embeddings.create(**kwargs)
        embeddings = [item.embedding for item in response.data]
        all_embeddings.extend(embeddings)

    return all_embeddings


def get_embedding(text: str, **kwargs) -> List[float]:
    """Get single embedding."""
    return get_embeddings([text], **kwargs)[0]


# Dimension reduction with Matryoshka embeddings
def get_reduced_embedding(text: str, dimensions: int = 512) -> List[float]:
    """Get embedding with reduced dimensions (Matryoshka)."""
    return get_embedding(
        text,
        model="text-embedding-3-small",
        dimensions=dimensions
    )
```

### Template 3: Local Embeddings with Sentence Transformers

```python
from sentence_transformers import SentenceTransformer
from typing import List, Optional
import numpy as np

class LocalEmbedder:
    """Local embedding with sentence-transformers."""

    def __init__(
        self,
        model_name: str = "BAAI/bge-large-en-v1.5",
        device: str = "cuda"
    ):
        self.model = SentenceTransformer(model_name, device=device)
        self.model_name = model_name

    def embed(
        self,
        texts: List[str],
        normalize: bool = True,
        show_progress: bool = False
    ) -> np.ndarray:
        """Embed texts with optional normalization."""
        embeddings = self.model.encode(
            texts,
            normalize_embeddings=normalize,
            show_progress_bar=show_progress,
            convert_to_numpy=True
        )
        return embeddings

    def embed_query(self, query: str) -> np.ndarray:
        """Embed a query with appropriate prefix for retrieval models."""
        # BGE and similar models benefit from query prefix
        if "bge" in self.model_name.lower():
            query = f"Represent this sentence for searching relevant passages: {query}"
        return self.embed([query])[0]

    def embed_documents(self, documents: List[str]) -> np.ndarray:
        """Embed documents for indexing."""
        return self.embed(documents)


# E5 model with instructions
class E5Embedder:
    def __init__(self, model_name: str = "intfloat/multilingual-e5-large"):
        self.model = SentenceTransformer(model_name)

    def embed_query(self, query: str) -> np.ndarray:
        """E5 requires 'query:' prefix for queries."""
        return self.model.encode(f"query: {query}")

    def embed_document(self, document: str) -> np.ndarray:
        """E5 requires 'passage:' prefix for documents."""
        return self.model.encode(f"passage: {document}")
```

### Template 4: Chunking Strategies

Use `langchain-text-splitters` for recursive and header-aware splitting rather than a
hand-rolled splitter. The token chunker below shows the overlap arithmetic.

```python
import re

import tiktoken
from langchain_text_splitters import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
)


def chunk_by_tokens(
    text: str,
    chunk_size: int = 512,
    chunk_overlap: int = 50,
    encoding_name: str = "cl100k_base",
) -> list[str]:
    """Fixed-size token windows with overlap. Count tokens with the tokenizer of the
    embedding model you use; cl100k_base is only an approximation for non-OpenAI models."""
    if not 0 <= chunk_overlap < chunk_size:
        raise ValueError("need 0 <= chunk_overlap < chunk_size")
    enc = tiktoken.get_encoding(encoding_name)
    tokens = enc.encode(text)
    chunks = []
    step = chunk_size - chunk_overlap
    for start in range(0, len(tokens), step):
        chunks.append(enc.decode(tokens[start:start + chunk_size]))
        if start + chunk_size >= len(tokens):
            break
    return chunks


# Recursive split on paragraph -> line -> sentence -> word boundaries
recursive = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    encoding_name="cl100k_base", chunk_size=512, chunk_overlap=50
)

# Markdown: split on headers, keep the header path as metadata, then size-limit
markdown = MarkdownHeaderTextSplitter(
    headers_to_split_on=[("#", "h1"), ("##", "h2"), ("###", "h3")]
)


def chunk_markdown(text: str) -> list[dict]:
    sections = markdown.split_text(text)
    return [
        {"text": doc.page_content, "metadata": doc.metadata}
        for doc in recursive.split_documents(sections)
    ]


def chunk_by_sentences(text: str, max_chars: int = 1000) -> list[str]:
    """Greedy sentence packing. The regex is a cheap splitter; use a real sentence
    segmenter (nltk, spaCy) for abbreviations and non-English text."""
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    chunks, current = [], ""
    for sentence in sentences:
        if current and len(current) + len(sentence) + 1 > max_chars:
            chunks.append(current)
            current = sentence
        else:
            current = f"{current} {sentence}".strip()
    if current:
        chunks.append(current)
    return chunks


if __name__ == "__main__":
    text = " ".join(f"word{i}" for i in range(2000))
    chunks = chunk_by_tokens(text, chunk_size=100, chunk_overlap=20)
    enc = tiktoken.get_encoding("cl100k_base")
    n = len(enc.encode(text))
    assert len(chunks) == -(-(n - 20) // 80)  # no trailing overlap-only chunk
    assert chunk_by_tokens("short", 100, 20) == ["short"]
    md = "# A\nintro\n## B\nbody text"
    assert chunk_markdown(md)[-1]["metadata"] == {"h1": "A", "h2": "B"}
    assert chunk_by_sentences("One. Two. Three.", max_chars=9) == ["One. Two.", "Three."]
```

### Template 5: Domain-Specific Embedding Pipeline

```python
import re
from typing import List, Optional
from dataclasses import dataclass

from langchain_voyageai import VoyageAIEmbeddings
# chunk_by_tokens from Template 4

@dataclass
class EmbeddedDocument:
    id: str
    document_id: str
    chunk_index: int
    text: str
    embedding: List[float]
    metadata: dict

class DomainEmbeddingPipeline:
    """Pipeline for domain-specific embeddings."""

    def __init__(
        self,
        embedding_model: str = "voyage-4-large",
        chunk_size: int = 512,
        chunk_overlap: int = 50,
        preprocessing_fn=None
    ):
        self.embeddings = VoyageAIEmbeddings(model=embedding_model)
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.preprocess = preprocessing_fn or self._default_preprocess

    def _default_preprocess(self, text: str) -> str:
        """Default preprocessing."""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters (customize for your domain)
        text = re.sub(r'[^\w\s.,!?-]', '', text)
        return text.strip()

    async def process_documents(
        self,
        documents: List[dict],
        id_field: str = "id",
        content_field: str = "content",
        metadata_fields: Optional[List[str]] = None
    ) -> List[EmbeddedDocument]:
        """Process documents for vector storage."""
        processed = []

        for doc in documents:
            content = doc[content_field]
            doc_id = doc[id_field]

            # Preprocess
            cleaned = self.preprocess(content)

            # Chunk
            chunks = chunk_by_tokens(
                cleaned,
                self.chunk_size,
                self.chunk_overlap
            )

            # Create embeddings
            embeddings = await self.embeddings.aembed_documents(chunks)

            # Create records
            for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                metadata = {"document_id": doc_id, "chunk_index": i}

                # Add specified metadata fields
                if metadata_fields:
                    for field in metadata_fields:
                        if field in doc:
                            metadata[field] = doc[field]

                processed.append(EmbeddedDocument(
                    id=f"{doc_id}_chunk_{i}",
                    document_id=doc_id,
                    chunk_index=i,
                    text=chunk,
                    embedding=embedding,
                    metadata=metadata
                ))

        return processed


# Code-specific pipeline
class CodeEmbeddingPipeline:
    """Specialized pipeline for code embeddings."""

    def __init__(self):
        # Voyage's code-specific model (as of 2026-10)
        self.embeddings = VoyageAIEmbeddings(model="voyage-code-4")

    def chunk_code(self, code: str, language: str) -> List[dict]:
        """Chunk code by functions/classes using tree-sitter."""
        try:
            # tree-sitter-language-pack replaces the unmaintained tree-sitter-languages
            from tree_sitter_language_pack import get_parser
            parser = get_parser(language)
            tree = parser.parse(bytes(code, "utf8"))

            chunks = []
            # Extract function and class definitions
            self._extract_nodes(tree.root_node, code, chunks)
            return chunks
        except ImportError:
            # Safe to continue: the whole file becomes one chunk when tree-sitter is absent
            return [{"text": code, "type": "module"}]

    def _extract_nodes(self, node, source_code: str, chunks: list):
        """Recursively extract function/class definitions."""
        if node.type in ['function_definition', 'class_definition', 'method_definition']:
            text = source_code[node.start_byte:node.end_byte]
            chunks.append({
                "text": text,
                "type": node.type,
                "name": self._get_name(node),
                "start_line": node.start_point[0],
                "end_line": node.end_point[0]
            })
        for child in node.children:
            self._extract_nodes(child, source_code, chunks)

    def _get_name(self, node) -> str:
        """Extract name from function/class node."""
        for child in node.children:
            if child.type == 'identifier' or child.type == 'name':
                return child.text.decode('utf8')
        return "unknown"

    async def embed_with_context(
        self,
        chunk: str,
        context: str = ""
    ) -> List[float]:
        """Embed code with surrounding context."""
        if context:
            combined = f"Context: {context}\n\nCode:\n{chunk}"
        else:
            combined = chunk
        return await self.embeddings.aembed_query(combined)
```

### Template 6: Embedding Quality Evaluation

```python
import numpy as np
from typing import List, Dict

def evaluate_retrieval_quality(
    queries: List[str],
    relevant_docs: List[List[str]],  # List of relevant doc IDs per query
    retrieved_docs: List[List[str]],  # List of retrieved doc IDs per query
    k: int = 10
) -> Dict[str, float]:
    """Evaluate embedding quality for retrieval."""

    def precision_at_k(relevant: set, retrieved: List[str], k: int) -> float:
        retrieved_k = retrieved[:k]
        relevant_retrieved = len(set(retrieved_k) & relevant)
        return relevant_retrieved / k if k > 0 else 0

    def recall_at_k(relevant: set, retrieved: List[str], k: int) -> float:
        retrieved_k = retrieved[:k]
        relevant_retrieved = len(set(retrieved_k) & relevant)
        return relevant_retrieved / len(relevant) if relevant else 0

    def mrr(relevant: set, retrieved: List[str]) -> float:
        for i, doc in enumerate(retrieved):
            if doc in relevant:
                return 1 / (i + 1)
        return 0

    def ndcg_at_k(relevant: set, retrieved: List[str], k: int) -> float:
        dcg = sum(
            1 / np.log2(i + 2) if doc in relevant else 0
            for i, doc in enumerate(retrieved[:k])
        )
        ideal_dcg = sum(1 / np.log2(i + 2) for i in range(min(len(relevant), k)))
        return dcg / ideal_dcg if ideal_dcg > 0 else 0

    metrics = {
        f"precision@{k}": [],
        f"recall@{k}": [],
        "mrr": [],
        f"ndcg@{k}": []
    }

    for relevant, retrieved in zip(relevant_docs, retrieved_docs):
        relevant_set = set(relevant)
        metrics[f"precision@{k}"].append(precision_at_k(relevant_set, retrieved, k))
        metrics[f"recall@{k}"].append(recall_at_k(relevant_set, retrieved, k))
        metrics["mrr"].append(mrr(relevant_set, retrieved))
        metrics[f"ndcg@{k}"].append(ndcg_at_k(relevant_set, retrieved, k))

    return {name: np.mean(values) for name, values in metrics.items()}


def compute_embedding_similarity(
    embeddings1: np.ndarray,
    embeddings2: np.ndarray,
    metric: str = "cosine"
) -> np.ndarray:
    """Compute similarity matrix between embedding sets."""
    if metric == "cosine":
        # Normalize and compute dot product
        norm1 = embeddings1 / np.linalg.norm(embeddings1, axis=1, keepdims=True)
        norm2 = embeddings2 / np.linalg.norm(embeddings2, axis=1, keepdims=True)
        return norm1 @ norm2.T
    elif metric == "euclidean":
        from scipy.spatial.distance import cdist
        return -cdist(embeddings1, embeddings2, metric='euclidean')
    elif metric == "dot":
        return embeddings1 @ embeddings2.T
    else:
        raise ValueError(f"Unknown metric: {metric}")


def compare_embedding_models(
    texts: List[str],
    models: Dict[str, callable],
    queries: List[str],
    relevant_indices: List[List[int]],
    k: int = 5
) -> Dict[str, Dict[str, float]]:
    """Compare multiple embedding models on retrieval quality."""
    results = {}

    for model_name, embed_fn in models.items():
        # Embed all texts
        doc_embeddings = np.array(embed_fn(texts))

        retrieved_per_query = []
        for query in queries:
            query_embedding = np.array(embed_fn([query])[0])
            # Compute similarities
            similarities = compute_embedding_similarity(
                query_embedding.reshape(1, -1),
                doc_embeddings,
                metric="cosine"
            )[0]
            # Get top-k indices
            top_k_indices = np.argsort(similarities)[::-1][:k]
            retrieved_per_query.append([str(i) for i in top_k_indices])

        # Convert relevant indices to string IDs
        relevant_docs = [[str(i) for i in indices] for indices in relevant_indices]

        results[model_name] = evaluate_retrieval_quality(
            queries, relevant_docs, retrieved_per_query, k
        )

    return results
```
