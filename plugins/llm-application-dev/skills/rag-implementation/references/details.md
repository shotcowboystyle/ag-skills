# rag-implementation — detailed patterns and worked examples

Topics owned elsewhere (link, don't repeat):

- Chunking and text splitters: [embedding-strategies](../../embedding-strategies/SKILL.md)
- Hybrid search, BM25 and Reciprocal Rank Fusion: [hybrid-search-implementation](../../hybrid-search-implementation/SKILL.md)
- Vector store setup (Pinecone, Qdrant, pgvector, Weaviate): [similarity-search-patterns](../../similarity-search-patterns/SKILL.md)
- Retrieval and answer-quality evaluation with LLM judges: [llm-evaluation](../../llm-evaluation/SKILL.md)

Model IDs are as of 2026-10; check the provider docs for current ones. The prebuilt
retrievers below (`MultiQueryRetriever`, `ContextualCompressionRetriever`,
`ParentDocumentRetriever`) live in the `langchain-classic` package since LangChain 1.0;
`langchain.retrievers` no longer exists.

## Setup used by the examples

```python
from langchain_anthropic import ChatAnthropic
from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_voyageai import VoyageAIEmbeddings

llm = ChatAnthropic(model="claude-sonnet-5-5")
embeddings = VoyageAIEmbeddings(model="voyage-4")
documents = [
    Document(id="pricing", page_content="The Pro plan costs $20 per month.",
             metadata={"source": "pricing.md", "category": "billing"}),
    Document(id="limits", page_content="Pro accounts can create 50 projects.",
             metadata={"source": "limits.md", "category": "technical"}),
    Document(id="sso", page_content="SSO is available on the Enterprise plan.",
             metadata={"source": "sso.md", "category": "technical"}),
]
vectorstore = InMemoryVectorStore(embeddings)
vectorstore.add_documents(documents)
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
```

Every example has an async twin (`ainvoke`, `asimilarity_search`, …) for serving code.

## Query rewriting

### Multi-query retrieval

The LLM writes several phrasings of the question; results are merged and de-duplicated.

```python
from langchain_classic.retrievers import MultiQueryRetriever

multi_query_retriever = MultiQueryRetriever.from_llm(
    retriever=vectorstore.as_retriever(search_kwargs={"k": 5}),
    llm=llm,
)
results = multi_query_retriever.invoke("What does Pro cost?")
```

### HyDE (hypothetical document embeddings)

Embed a model-written answer passage instead of the short question. Drop this `retrieve`
into the Quick Start graph in place of the original node.

```python
from langchain_core.prompts import ChatPromptTemplate

hyde_prompt = ChatPromptTemplate.from_template(
    "Write a short passage that would answer this question:\n\n{question}\n\nPassage:"
)

def retrieve(state: dict) -> dict:
    passage = (hyde_prompt | llm).invoke({"question": state["question"]}).text
    return {"context": retriever.invoke(passage)}

retrieve({"question": "What does Pro cost?"})
```

HyDE costs one extra LLM call per query and can drift when the model doesn't know the
domain; measure it against plain retrieval before adopting.

## Shaping what comes back

### Contextual compression

An LLM extracts only the relevant sentences from each retrieved document.

```python
from langchain_classic.retrievers import ContextualCompressionRetriever
from langchain_classic.retrievers.document_compressors import LLMChainExtractor

compression_retriever = ContextualCompressionRetriever(
    base_compressor=LLMChainExtractor.from_llm(llm),
    base_retriever=vectorstore.as_retriever(search_kwargs={"k": 10}),
)
compressed_docs = compression_retriever.invoke("What does Pro cost?")
```

### Parent document retrieval

Search small chunks for precision, return their larger parent for context.

```python
from langchain_classic.retrievers import ParentDocumentRetriever
from langchain_core.stores import InMemoryStore
from langchain_text_splitters import RecursiveCharacterTextSplitter

parent_retriever = ParentDocumentRetriever(
    vectorstore=InMemoryVectorStore(embeddings),  # holds the child chunks
    docstore=InMemoryStore(),                     # holds the parents
    child_splitter=RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=50),
    parent_splitter=RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200),
)
parent_retriever.add_documents(documents)
results = parent_retriever.invoke("project limits")
```

`InMemoryStore` loses parents on restart; use a persistent `BaseStore` in production.

### Metadata filtering

Filter syntax is store-specific. `InMemoryVectorStore` takes a callable; Pinecone, Qdrant,
pgvector and Weaviate take their own filter objects (see similarity-search-patterns).

```python
results = vectorstore.similarity_search(
    "plans",
    k=5,
    filter=lambda doc: doc.metadata.get("category") == "technical",
)
```

### Maximal marginal relevance (MMR)

```python
results = vectorstore.max_marginal_relevance_search(
    "plans",
    k=2,
    fetch_k=20,      # fetch 20 candidates, return the 2 most diverse relevant ones
    lambda_mult=0.5, # 0 = max diversity, 1 = max relevance
)
```

### Reranking with a cross-encoder

Requires `sentence-transformers`. Rerank a wide candidate set down to the few you send
to the model.

```python
from sentence_transformers import CrossEncoder

reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

def retrieve_and_rerank(query: str, k: int = 5) -> list[Document]:
    candidates = vectorstore.similarity_search(query, k=20)
    scores = reranker.predict([(query, doc.page_content) for doc in candidates])
    ranked = sorted(zip(candidates, scores), key=lambda pair: pair[1], reverse=True)
    return [doc for doc, _ in ranked[:k]]
```

Hosted rerankers (Cohere, Voyage) plug into `ContextualCompressionRetriever` as the
`base_compressor` via their LangChain integration packages.

## Structured, grounded output

Ask for the answer and its sources as fields, then check the sources against what you
retrieved. The prompt rules from the Quick Start still apply: documents go inside
delimiters and are treated as data, never as instructions.

```python
from pydantic import BaseModel, Field

class RAGResponse(BaseModel):
    answer: str = Field(description="Answer using only the documents, or \"I don't know.\"")
    sources: list[str] = Field(description="Ids of the documents the answer relies on")

structured_llm = llm.with_structured_output(RAGResponse)

def grounded(response: RAGResponse, context: list[Document]) -> RAGResponse:
    retrieved = {doc.id for doc in context}
    if response.answer != "I don't know." and (
        not response.sources or not set(response.sources) <= retrieved
    ):
        return RAGResponse(answer="I don't know.", sources=[])
    return response
```

## Retrieval evaluation

Score retrieval separately from generation: a bad answer from good context is a prompt
problem, a bad answer from bad context is a retrieval problem. For answer-quality judges
(faithfulness, relevance) see [llm-evaluation](../../llm-evaluation/SKILL.md).

```python
def evaluate_retrieval(retriever, test_cases: list[dict], k: int = 4) -> dict:
    """test_cases: [{"question": str, "relevant_ids": [str, ...]}, ...]"""
    precision, recall, rr = [], [], []
    for case in test_cases:
        retrieved = [doc.id for doc in retriever.invoke(case["question"])][:k]
        relevant = set(case["relevant_ids"])
        hits = [doc_id in relevant for doc_id in retrieved]
        precision.append(sum(hits) / len(retrieved) if retrieved else 0.0)
        recall.append(sum(hits) / len(relevant))
        rr.append(next((1 / (i + 1) for i, hit in enumerate(hits) if hit), 0.0))
    n = len(test_cases)
    return {
        f"precision@{k}": sum(precision) / n,
        f"recall@{k}": sum(recall) / n,
        "mrr": sum(rr) / n,
    }

print(evaluate_retrieval(retriever, [{"question": "Pro price", "relevant_ids": ["pricing"]}]))
```
