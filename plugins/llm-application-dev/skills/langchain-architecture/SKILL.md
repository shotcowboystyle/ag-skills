---
name: langchain-architecture
description: Design LLM applications using LangChain 1.x and LangGraph for agents, memory, and tool integration. Use when building LangChain applications, implementing AI agents, or creating complex LLM workflows.
last_verified: 2026-10-27
---

# LangChain & LangGraph Architecture

Build LLM applications with LangChain 1.x agents and LangGraph workflows: state, memory, tools, and tests.

## When to Use This Skill

- Building AI agents with tool access
- Implementing multi-step LLM workflows
- Managing conversation memory and state
- Writing offline tests for agents

## Package Structure (verified 2026-10-27)

```
langchain (1.4.x)          # create_agent, middleware, init_chat_model
langchain-core (1.7.x)     # messages, prompts, tools, runnables
langgraph (1.2.x)          # StateGraph, checkpointers, stores
langchain-classic (1.0.x)  # legacy chains, retrievers, memory (migration only)
langchain-anthropic / langchain-openai / langchain-voyageai / langchain-<vectorstore>
```

`langchain.retrievers`, `langchain.chains` and `langchain.memory` are gone from `langchain` 1.x. Import them from `langchain_classic` only while migrating old code.

## Core Concepts

### 1. Choose the right abstraction

| Need | Use |
| ---- | --- |
| Model + tools loop | `langchain.agents.create_agent` |
| Fixed steps, branching, loops | `langgraph.graph.StateGraph` |
| Cross-cutting behaviour (summaries, retries, HITL, PII) | `create_agent(middleware=[...])` |

`langgraph.prebuilt.create_react_agent` is superseded by `create_agent`; don't use it in new code.

### 2. Memory

- **Short-term (per conversation)**: pass a checkpointer (`InMemorySaver` in dev, `PostgresSaver` in prod) and a `thread_id` in config. History is stored per thread.
- **Long history**: add `SummarizationMiddleware` to compress old messages before they overflow context.
- **Long-term (across threads)**: pass a LangGraph `store=` (`InMemoryStore`, `PostgresStore`) and read/write it from tools.

The old `ConversationBufferMemory` / `ConversationSummaryMemory` classes are legacy (`langchain_classic.memory`); don't use them with agents.

### 3. Models (as of 2026-10)

Anthropic: `claude-opus-5-5`, `claude-sonnet-5-5`, `claude-haiku-5-5`. OpenAI: `gpt-5.5`. Model IDs change often; check the provider docs before pinning one.

### 4. Tracing

Set `LANGSMITH_TRACING=true` and `LANGSMITH_API_KEY` to trace every LangChain/LangGraph call.

## Quick Start

```python
from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware
from langchain_core.tools import tool
from langgraph.checkpoint.memory import InMemorySaver


@tool
def search_database(query: str) -> str:
    """Search internal database for information."""
    return f"Results for: {query}"  # your search logic


agent = create_agent(
    "anthropic:claude-sonnet-5-5",
    tools=[search_database],
    system_prompt="You are a helpful research assistant.",
    checkpointer=InMemorySaver(),
    middleware=[
        SummarizationMiddleware(
            model="anthropic:claude-haiku-5-5",
            trigger=("tokens", 4000),
            keep=("messages", 20),
        )
    ],
)

config = {"configurable": {"thread_id": "user-123"}}
result = await agent.ainvoke(
    {"messages": [("user", "Search for Python tutorials")]}, config
)
print(result["messages"][-1].content)
```

## Testing Agents Offline

Script the model's replies with a fake chat model so tests run without an API key. Assert on what the tools received and on the checkpointed history, not on model wording.

```python
import pytest
from langchain.agents import create_agent
from langchain_core.language_models.fake_chat_models import GenericFakeChatModel
from langchain_core.messages import AIMessage, ToolMessage
from langchain_core.tools import tool
from langgraph.checkpoint.memory import InMemorySaver


class FakeToolModel(GenericFakeChatModel):
    """Replays scripted AIMessages; create_agent needs bind_tools."""

    def bind_tools(self, tools, **kwargs):
        return self


calls: list[str] = []


@tool
def search_database(query: str) -> str:
    """Search internal database for information."""
    calls.append(query)
    return f"Results for: {query}"


def make_agent(script: list[AIMessage]):
    model = FakeToolModel(messages=iter(script))
    return create_agent(model, [search_database], checkpointer=InMemorySaver())


@pytest.mark.asyncio
async def test_agent_calls_tool():
    calls.clear()
    agent = make_agent([
        AIMessage(content="", tool_calls=[
            {"name": "search_database", "args": {"query": "python"}, "id": "call_1"}
        ]),
        AIMessage(content="Found Python results."),
    ])
    result = await agent.ainvoke(
        {"messages": [("user", "search for python")]},
        {"configurable": {"thread_id": "t1"}},
    )
    assert calls == ["python"]
    tool_msgs = [m for m in result["messages"] if isinstance(m, ToolMessage)]
    assert tool_msgs[0].content == "Results for: python"
    assert result["messages"][-1].content == "Found Python results."


@pytest.mark.asyncio
async def test_memory_is_per_thread():
    agent = make_agent([AIMessage(content="Noted."), AIMessage(content="12345"),
                        AIMessage(content="Hi.")])
    a = {"configurable": {"thread_id": "a"}}
    await agent.ainvoke({"messages": [("user", "Remember: the code is 12345")]}, a)
    await agent.ainvoke({"messages": [("user", "What was the code?")]}, a)
    await agent.ainvoke({"messages": [("user", "Hello")]},
                        {"configurable": {"thread_id": "b"}})

    history_a = (await agent.aget_state(a)).values["messages"]
    assert [m.content for m in history_a] == [
        "Remember: the code is 12345", "Noted.", "What was the code?", "12345"]
    history_b = (await agent.aget_state({"configurable": {"thread_id": "b"}})).values["messages"]
    assert len(history_b) == 2
```

Requires `pytest-asyncio`. Run real-model evaluations separately (see the `llm-evaluation` skill).

## Detailed patterns and worked examples

`references/details.md` covers: RAG as a StateGraph, structured tools, multi-step workflows, supervisor multi-agent routing, production checkpointers and long-term stores, callbacks, streaming, and caching. Read it when the quick start above is not enough.
