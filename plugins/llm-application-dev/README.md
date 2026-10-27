# LLM Application Development Plugin for Claude Code

Build production-ready LLM applications, advanced RAG systems, and intelligent agents with modern AI patterns.

## Version 2.1.0 Highlights

- **LangChain 1.x agents**: `create_agent` with checkpointers and middleware replaces `create_react_agent` and the legacy memory classes
- **One owner per vector topic**: chunking, client setup, hybrid search and index tuning each live in one skill; the others link to it
- **Guarded RAG prompt**: retrieved text is treated as data and answers must cite sources
- **Model IDs are date-qualified**: examples name models "as of 2026-10"; check provider docs for current IDs

## Features

### Core Capabilities

- **RAG Systems**: Production retrieval-augmented generation with hybrid search
- **Vector Search**: Pinecone, Qdrant, Weaviate, Milvus, pgvector optimization
- **Agent Architectures**: LangGraph-based agents with memory and tool use
- **Prompt Engineering**: Advanced prompting techniques with model-specific optimization

### Key Technologies

- LangChain 1.x / LangGraph for agent workflows
- Voyage AI, OpenAI, and open-source embedding models
- HNSW, IVF, and Product Quantization index strategies
- Async patterns with checkpointers for durable execution

## Agents

| Agent                      | Description                                                                |
| -------------------------- | -------------------------------------------------------------------------- |
| `ai-engineer`              | Architecture decision for one LLM feature (call, chain, RAG or agent)      |
| `prompt-engineer`          | Write or revise one production prompt, with test cases                     |
| `vector-database-engineer` | Vector search setup recommendation for a corpus and query workload         |

## Skills

| Skill                          | Description                                                 |
| ------------------------------ | ----------------------------------------------------------- |
| `langchain-architecture`       | LangGraph StateGraph patterns, memory, and tool integration |
| `rag-implementation`           | RAG systems with hybrid search and reranking                |
| `llm-evaluation`               | Evaluation frameworks for LLM applications                  |
| `prompt-engineering-patterns`  | Chain-of-thought, few-shot, and structured outputs          |
| `embedding-strategies`         | Embedding model selection and optimization                  |
| `similarity-search-patterns`   | Vector similarity search implementation                     |
| `vector-index-tuning`          | HNSW, IVF, and quantization optimization                    |
| `hybrid-search-implementation` | Vector + keyword search fusion                              |

## Commands

| Command                                | Description                     |
| -------------------------------------- | ------------------------------- |
| `/llm-application-dev:langchain-agent` | Create LangGraph-based agent    |
| `/llm-application-dev:ai-assistant`    | Build AI assistant application  |
| `/llm-application-dev:prompt-optimize` | Optimize prompts for production |

## Installation

```bash
/plugin install llm-application-dev@claude-code-workflows
```

## Requirements

- LangChain >= 1.0 (examples verified against 1.4.7)
- LangGraph >= 1.0 (examples verified against 1.2.18)
- `langchain-classic` for the legacy retrievers (multi-query, compression, parent-document)
- Python 3.11+

## Changelog

### 2.1.0 (October 2026)

- Agents use `langchain.agents.create_agent`; memory via checkpointers, `SummarizationMiddleware` and stores
- Legacy retrievers import from `langchain_classic.retrievers` (`langchain.retrievers` was removed)
- RAG prompt guards against prompt injection and requires citations
- Qdrant examples use `query_points`; Weaviate examples use the v4 client
- Hybrid search documents the RRF formula and fixes a candidate-limit integer division
- `ai-engineer`, `prompt-engineer` and `vector-database-engineer` rewritten as single-task agents
- Model references updated and date-qualified

### 2.0.0 (January 2026)

- **Breaking**: Migrated from LangChain 0.x to LangChain 1.x/LangGraph
- **Breaking**: Updated model references to Claude 4.6 and GPT-5.4
- Added Voyage AI as primary embedding recommendation for Claude apps
- Added LangGraph StateGraph patterns replacing deprecated `initialize_agent()`
- Added structured outputs with Pydantic
- Added async patterns with checkpointers
- Fixed security issue: replaced unsafe code execution with AST-based safe math evaluation
- Updated hybrid search with modern Pinecone client API

### 1.2.2

- Minor bug fixes and documentation updates

## License

MIT License - See the plugin configuration for details.
