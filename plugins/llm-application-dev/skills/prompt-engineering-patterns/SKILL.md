---
name: prompt-engineering-patterns
description: >-
  This skill should be used when the user asks to "optimize a prompt", "improve prompt
  performance", "design a prompt template", "write better prompts", "debug prompt issues", "use
  chain-of-thought", "structured prompting", "few-shot prompting", or wants to apply advanced
  prompt engineering patterns for production LLM applications.
last_verified: 2026-10-27
---

# Prompt Engineering Patterns

Master advanced prompt engineering techniques to maximize LLM performance, reliability, and controllability.

## When to Use This Skill

- Designing complex prompts for production LLM applications
- Optimizing prompt performance and consistency
- Implementing structured reasoning patterns (chain-of-thought, tree-of-thought)
- Building few-shot learning systems with dynamic example selection
- Creating reusable prompt templates with variable interpolation
- Debugging and refining prompts that produce inconsistent outputs
- Implementing system prompts for specialized AI assistants
- Using structured outputs (JSON mode) for reliable parsing

## Core Capabilities

### 1. Few-Shot Learning

- Example selection strategies (semantic similarity, diversity sampling)
- Balancing example count with context window constraints
- Constructing effective demonstrations with input-output pairs
- Dynamic example retrieval from knowledge bases
- Handling edge cases through strategic example selection

### 2. Chain-of-Thought Prompting

- Step-by-step reasoning elicitation
- Zero-shot CoT with "Let's think step by step"
- Few-shot CoT with reasoning traces
- Self-consistency techniques (sampling multiple reasoning paths)
- Verification and validation steps

### 3. Structured Outputs

- JSON mode for reliable parsing
- Pydantic schema enforcement
- Type-safe response handling
- Error handling for malformed outputs

### 4. Prompt Optimization

- Iterative refinement workflows
- A/B testing prompt variations
- Measuring prompt performance metrics (accuracy, consistency, latency)
- Reducing token usage while maintaining quality
- Handling edge cases and failure modes

### 5. Template Systems

- Variable interpolation and formatting
- Conditional prompt sections
- Multi-turn conversation templates
- Role-based prompt composition
- Modular prompt components

### 6. System Prompt Design

- Setting model behavior and constraints
- Defining output formats and structure
- Establishing role and expertise
- Safety guidelines and content policies
- Context setting and background information

## Quick Start

```python
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

# Define structured output schema
class SQLQuery(BaseModel):
    query: str = Field(description="The SQL query")
    explanation: str = Field(description="Brief explanation of what the query does")
    tables_used: list[str] = Field(description="List of tables referenced")

# Initialize model with structured output
llm = ChatAnthropic(model="claude-sonnet-5-5")  # as of 2026-10
structured_llm = llm.with_structured_output(SQLQuery)

# Create prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an expert SQL developer. Generate efficient, secure SQL queries.
    Always use parameterized queries to prevent SQL injection.
    Explain your reasoning briefly."""),
    ("user", "Convert this to SQL: {query}")
])

# Create chain
chain = prompt | structured_llm

# Use
result = await chain.ainvoke({
    "query": "Find all users who registered in the last 30 days"
})
print(result.query)
print(result.explanation)
```

## Bundled references

Read only the file the task needs:

- `references/details.md`: structured output, dynamic few-shot selection, progressive disclosure, error recovery, RAG and caching patterns. Read when building a prompt into code.
- `references/few-shot-learning.md`: example selection (similarity, diversity, difficulty, error-based) and token budgets. Read when choosing or trimming examples.
- `references/chain-of-thought.md`: zero/few-shot CoT, self-consistency, least-to-most, tree-of-thought, verification. Read when the task needs multi-step reasoning.
- `references/prompt-templates.md`: conditional, modular, inherited and multi-turn templates with variable validation. Read when building a template system.
- `references/system-prompts.md`: system prompt structure and role patterns. Read when writing a system prompt.
- `references/prompt-optimization.md`: baselines, A/B tests, failure analysis, versioning. Read when measuring or iterating on a prompt.
- `assets/prompt-template-library.md`: copy-ready templates for classification, extraction, generation, transformation, analysis and QA.
- `assets/few-shot-examples.json`: sample example sets by task.
- `scripts/optimize-prompt.py`: runnable A/B and iterative optimization harness. Pass your own client with a `complete(prompt) -> str` method; `python scripts/optimize-prompt.py` runs a mock demo.

## Best Practices

1. **Be Specific**: Vague prompts produce inconsistent results
2. **Show, Don't Tell**: Examples are more effective than descriptions
3. **Use Structured Outputs**: Enforce schemas with Pydantic for reliability
4. **Test Extensively**: Evaluate on diverse, representative inputs
5. **Iterate Rapidly**: Small changes can have large impacts
6. **Monitor Performance**: Track metrics in production
7. **Version Control**: Treat prompts as code with proper versioning
8. **Document Intent**: Explain why prompts are structured as they are

## Common Pitfalls

- **Over-engineering**: Starting with complex prompts before trying simple ones
- **Example pollution**: Using examples that don't match the target task
- **Context overflow**: Exceeding token limits with excessive examples
- **Ambiguous instructions**: Leaving room for multiple interpretations
- **Ignoring edge cases**: Not testing on unusual or boundary inputs
- **No error handling**: Assuming outputs will always be well-formed
- **Hardcoded values**: Not parameterizing prompts for reuse

## Success Metrics

Track these KPIs for your prompts:

- **Accuracy**: Correctness of outputs
- **Consistency**: Reproducibility across similar inputs
- **Latency**: Response time (P50, P95, P99)
- **Token Usage**: Average tokens per request
- **Success Rate**: Percentage of valid, parseable outputs
- **User Satisfaction**: Ratings and feedback
