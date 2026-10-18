# Agent Reference

Reference for 172 local AI agents organized by category. The model column lists aliases in the shared Claude Code source format. Adapters provide agent formats and model mappings for other tools. See the [capability matrix](./harnesses.md) for setup and tool-specific limits.

## Agent Categories

### Architecture & System Design

#### Core Architecture

| Agent                                                                                         | Model   | Description                                                            |
| --------------------------------------------------------------------------------------------- | ------- | ---------------------------------------------------------------------- |
| [backend-architect](../plugins/backend-development/agents/backend-architect.md)               | inherit | RESTful API design, microservice boundaries, database schemas          |
| [frontend-developer](../plugins/multi-platform-apps/agents/frontend-developer.md)             | inherit | React components, responsive layouts, client-side state management     |
| [graphql-architect](../plugins/backend-development/agents/graphql-architect.md)               | opus    | GraphQL schemas, resolvers, federation architecture                    |
| [architect-review](../plugins/comprehensive-review/agents/architect-review.md)                | opus    | Architectural consistency analysis and pattern validation              |
| [cloud-architect](../plugins/cloud-infrastructure/agents/cloud-architect.md)                  | opus    | AWS/Azure/GCP infrastructure design and cost optimization              |
| [hybrid-cloud-architect](../plugins/cloud-infrastructure/agents/hybrid-cloud-architect.md)    | opus    | Multi-cloud strategies across cloud and on-premises environments       |
| [kubernetes-architect](../plugins/kubernetes-operations/agents/kubernetes-architect.md)       | opus    | Cloud-native infrastructure with Kubernetes and GitOps                 |
| [service-mesh-expert](../plugins/cloud-infrastructure/agents/service-mesh-expert.md)          | opus    | Istio/Linkerd service mesh architecture, mTLS, and traffic management  |
| [event-sourcing-architect](../plugins/backend-development/agents/event-sourcing-architect.md) | inherit | Event sourcing, CQRS patterns, event stores, and saga orchestration    |
| [monorepo-architect](../plugins/developer-essentials/agents/monorepo-architect.md)            | opus    | Monorepo tooling with Nx, Turborepo, Bazel, and workspace optimization |

#### UI/UX & Mobile

| Agent                                                                                    | Model   | Description                                             |
| ---------------------------------------------------------------------------------------- | ------- | ------------------------------------------------------- |
| [ui-designer](../plugins/ui-design/agents/ui-designer.md)                                | inherit | UI/UX design for mobile and web with modern patterns    |
| [accessibility-expert](../plugins/ui-design/agents/accessibility-expert.md)              | inherit | WCAG compliance, accessibility audits, inclusive design |
| [design-system-architect](../plugins/ui-design/agents/design-system-architect.md)        | inherit | Design tokens, component libraries, theming systems     |
| [ui-ux-designer](../plugins/multi-platform-apps/agents/ui-ux-designer.md)                | sonnet  | Interface design, wireframes, design systems            |
| [ui-visual-validator](../plugins/accessibility-compliance/agents/ui-visual-validator.md) | sonnet  | Visual regression testing and UI verification           |
| [mobile-developer](../plugins/multi-platform-apps/agents/mobile-developer.md)            | inherit | React Native and Flutter application development        |
| [ios-developer](../plugins/multi-platform-apps/agents/ios-developer.md)                  | inherit | Native iOS development with Swift/SwiftUI               |
| [flutter-expert](../plugins/multi-platform-apps/agents/flutter-expert.md)                | inherit | Advanced Flutter development with state management      |

### Programming Languages

#### Systems & Low-Level

| Agent                                                             | Model | Description                                                 |
| ----------------------------------------------------------------- | ----- | ----------------------------------------------------------- |
| [c-pro](../plugins/systems-programming/agents/c-pro.md)           | opus  | System programming with memory management and OS interfaces |
| [cpp-pro](../plugins/systems-programming/agents/cpp-pro.md)       | opus  | Modern C++ with RAII, smart pointers, STL algorithms        |
| [rust-pro](../plugins/systems-programming/agents/rust-pro.md)     | opus  | Memory-safe systems programming with ownership patterns     |
| [golang-pro](../plugins/systems-programming/agents/golang-pro.md) | opus  | Concurrent programming with goroutines and channels         |

#### Web & Application

| Agent                                                                               | Model   | Description                                                                       |
| ----------------------------------------------------------------------------------- | ------- | --------------------------------------------------------------------------------- |
| [javascript-pro](../plugins/javascript-typescript/agents/javascript-pro.md)         | inherit | Modern JavaScript with ES6+, async patterns, Node.js                              |
| [typescript-pro](../plugins/javascript-typescript/agents/typescript-pro.md)         | opus    | Advanced TypeScript with type systems and generics                                |
| [python-pro](../plugins/python-development/agents/python-pro.md)                    | opus    | Python development with advanced features and optimization                        |
| [temporal-python-pro](../plugins/backend-development/agents/temporal-python-pro.md) | inherit | Temporal workflow orchestration with Python SDK, durable workflows, saga patterns |

#### Shell Scripting

| Agent                                                                   | Model  | Description                                                         |
| ----------------------------------------------------------------------- | ------ | ------------------------------------------------------------------- |
| [bash-pro](../plugins/shell-scripting/agents/bash-pro.md)               | sonnet | Defensive Bash scripting for production automation and CI/CD        |
| [posix-shell-pro](../plugins/shell-scripting/agents/posix-shell-pro.md) | sonnet | Strict POSIX sh scripts portable across dash, ash, and bash --posix |

#### Specialized Platforms

| Agent                                                                              | Model   | Description                                   |
| ---------------------------------------------------------------------------------- | ------- | --------------------------------------------- |
| [django-pro](../plugins/api-scaffolding/agents/django-pro.md)                      | opus    | Django development with ORM and async views   |
| [fastapi-pro](../plugins/api-scaffolding/agents/fastapi-pro.md)                    | opus    | FastAPI with async patterns and Pydantic      |
| [unity-developer](../plugins/game-development/agents/unity-developer.md)           | opus    | Unity game development and optimization       |
| [minecraft-bukkit-pro](../plugins/game-development/agents/minecraft-bukkit-pro.md) | opus    | Minecraft server plugin development           |
| [sql-pro](../plugins/database-design/agents/sql-pro.md)                            | inherit | Complex SQL queries and database optimization |

### Infrastructure & Operations

#### DevOps & Deployment

| Agent                                                                                  | Model  | Description                                                        |
| -------------------------------------------------------------------------------------- | ------ | ------------------------------------------------------------------ |
| [devops-troubleshooter](../plugins/incident-response/agents/devops-troubleshooter.md)  | sonnet | Production debugging, log analysis, deployment troubleshooting     |
| [deployment-engineer](../plugins/cloud-infrastructure/agents/deployment-engineer.md)   | haiku  | CI/CD pipelines, containerization, cloud deployments               |
| [terraform-specialist](../plugins/cloud-infrastructure/agents/terraform-specialist.md) | opus   | Infrastructure as Code with Terraform modules and state management |
| [dx-optimizer](../plugins/team-collaboration/agents/dx-optimizer.md)                   | sonnet | Developer experience optimization and tooling improvements         |

#### Database Management

| Agent                                                                                  | Model   | Description                                                         |
| -------------------------------------------------------------------------------------- | ------- | ------------------------------------------------------------------- |
| [database-optimizer](../plugins/observability-monitoring/agents/database-optimizer.md) | inherit | Query optimization, index design, migration strategies              |
| [database-admin](../plugins/database-migrations/agents/database-admin.md)              | sonnet  | Database operations, backup, replication, monitoring                |
| [database-architect](../plugins/database-design/agents/database-architect.md)          | opus    | Database design from scratch, technology selection, schema modeling |

#### Incident Response & Network

| Agent                                                                              | Model  | Description                                         |
| ---------------------------------------------------------------------------------- | ------ | --------------------------------------------------- |
| [incident-responder](../plugins/incident-response/agents/incident-responder.md)    | sonnet | Production incident management and resolution       |
| [network-engineer](../plugins/observability-monitoring/agents/network-engineer.md) | sonnet | Network debugging, load balancing, traffic analysis |

#### Project Management

| Agent                                                                     | Model | Description                                                                          |
| ------------------------------------------------------------------------- | ----- | ------------------------------------------------------------------------------------ |
| [conductor-validator](../plugins/conductor/agents/conductor-validator.md) | opus  | Validates Conductor project artifacts for completeness, consistency, and correctness |

### Quality Assurance & Security

#### Code Quality & Review

| Agent                                                                                            | Model  | Description                                                     |
| ------------------------------------------------------------------------------------------------ | ------ | --------------------------------------------------------------- |
| [code-reviewer](../plugins/comprehensive-review/agents/code-reviewer.md)                         | opus   | Code review with security focus and production reliability      |
| [security-auditor](../plugins/comprehensive-review/agents/security-auditor.md)                   | opus   | Vulnerability assessment and OWASP compliance                   |
| [backend-security-coder](../plugins/backend-api-security/agents/backend-security-coder.md)       | sonnet | Secure backend coding practices, API security implementation    |
| [frontend-security-coder](../plugins/frontend-mobile-security/agents/frontend-security-coder.md) | sonnet | XSS prevention, CSP implementation, client-side security        |
| [mobile-security-coder](../plugins/frontend-mobile-security/agents/mobile-security-coder.md)     | sonnet | Mobile security patterns, WebView security, biometric auth      |
| [threat-modeling-expert](../plugins/security-scanning/agents/threat-modeling-expert.md)          | opus   | STRIDE threat modeling, attack trees, and security requirements |

#### Reverse Engineering & Policy

| Agent                                                                                     | Model  | Description                                                               |
| ----------------------------------------------------------------------------------------- | ------ | ------------------------------------------------------------------------- |
| [reverse-engineer](../plugins/reverse-engineering/agents/reverse-engineer.md)             | opus   | Binary analysis, disassembly, and decompilation with IDA, Ghidra, radare2 |
| [malware-analyst](../plugins/reverse-engineering/agents/malware-analyst.md)               | opus   | Defensive malware research, sandbox and behavioral analysis               |
| [firmware-analyst](../plugins/reverse-engineering/agents/firmware-analyst.md)             | opus   | Embedded and IoT firmware extraction and vulnerability research           |
| [policy-enforcer](../plugins/protect-mcp/agents/policy-enforcer.md)                       | opus   | Cedar policies that govern Claude Code tool calls                         |
| [receipt-verifier](../plugins/protect-mcp/agents/receipt-verifier.md)                     | sonnet | Ed25519 signed-receipt verification and tamper detection                  |
| [review-policy-author](../plugins/review-agent-governance/agents/review-policy-author.md) | sonnet | Cedar policies that gate agent review actions behind human approval       |

#### Testing & Debugging

| Agent                                                                         | Model  | Description                                                |
| ----------------------------------------------------------------------------- | ------ | ---------------------------------------------------------- |
| [test-automator](../plugins/codebase-cleanup/agents/test-automator.md)        | sonnet | Comprehensive test suite creation (unit, integration, e2e) |
| [tdd-orchestrator](../plugins/backend-development/agents/tdd-orchestrator.md) | opus   | Test-Driven Development methodology guidance               |
| [debugger](../plugins/error-debugging/agents/debugger.md)                     | sonnet | Error resolution and test failure analysis                 |
| [error-detective](../plugins/error-debugging/agents/error-detective.md)       | sonnet | Log analysis and error pattern recognition                 |

#### Performance & Observability

| Agent                                                                                          | Model   | Description                                                    |
| ---------------------------------------------------------------------------------------------- | ------- | -------------------------------------------------------------- |
| [performance-engineer](../plugins/observability-monitoring/agents/performance-engineer.md)     | inherit | Application profiling and optimization                         |
| [observability-engineer](../plugins/observability-monitoring/agents/observability-engineer.md) | inherit | Production monitoring, distributed tracing, SLI/SLO management |

### Data & AI

#### Data Engineering & Analytics

| Agent                                                                      | Model   | Description                                             |
| -------------------------------------------------------------------------- | ------- | ------------------------------------------------------- |
| [data-scientist](../plugins/machine-learning-ops/agents/data-scientist.md) | inherit | Data analysis, SQL queries, BigQuery operations         |
| [data-engineer](../plugins/data-engineering/agents/data-engineer.md)       | opus    | ETL pipelines, data warehouses, streaming architectures |

#### Machine Learning & AI

| Agent                                                                                                    | Model   | Description                                                           |
| -------------------------------------------------------------------------------------------------------- | ------- | --------------------------------------------------------------------- |
| [ai-engineer](../plugins/llm-application-dev/agents/ai-engineer.md)                                      | inherit | LLM applications, RAG systems, prompt pipelines                       |
| [ml-engineer](../plugins/machine-learning-ops/agents/ml-engineer.md)                                     | inherit | ML pipelines, model serving, feature engineering                      |
| [mlops-engineer](../plugins/machine-learning-ops/agents/mlops-engineer.md)                               | inherit | ML infrastructure, experiment tracking, model registries              |
| [prompt-engineer](../plugins/llm-application-dev/agents/prompt-engineer.md)                              | inherit | LLM prompt optimization and engineering                               |
| [vector-database-engineer](../plugins/llm-application-dev/agents/vector-database-engineer.md)            | inherit | Vector databases, embeddings, similarity search, and hybrid retrieval |
| [llm-finetuning-architect](../plugins/llm-finetuning/agents/llm-finetuning-architect.md)                 | opus    | Fine-tuning strategy, method/model selection, eval-gate ownership     |
| [llm-finetuning-training-engineer](../plugins/llm-finetuning/agents/llm-finetuning-training-engineer.md) | sonnet  | Dataset prep, Unsloth training runs, artifact export                  |
| [llm-finetuning-eval-engineer](../plugins/llm-finetuning/agents/llm-finetuning-eval-engineer.md)         | sonnet  | Golden sets, judge calibration, checkpoint promotion verdicts         |
| [dgx-spark-ops-engineer](../plugins/dgx-spark-ops/agents/dgx-spark-ops-engineer.md)                      | sonnet  | DGX Spark (GB10/aarch64/CUDA 13) environment setup and diagnostics    |

### Documentation & Technical Writing

| Agent                                                                                | Model  | Description                                                           |
| ------------------------------------------------------------------------------------ | ------ | --------------------------------------------------------------------- |
| [docs-architect](../plugins/code-documentation/agents/docs-architect.md)             | sonnet | Comprehensive technical documentation generation                      |
| [api-documenter](../plugins/api-testing-observability/agents/api-documenter.md)      | sonnet | OpenAPI/Swagger specifications and developer docs                     |
| [reference-builder](../plugins/documentation-generation/agents/reference-builder.md) | haiku  | Technical references and API documentation                            |
| [tutorial-engineer](../plugins/code-documentation/agents/tutorial-engineer.md)       | sonnet | Step-by-step tutorials and educational content                        |
| [mermaid-expert](../plugins/documentation-generation/agents/mermaid-expert.md)       | haiku  | Diagram creation (flowcharts, sequences, ERDs)                        |
| [c4-code](../plugins/c4-architecture/agents/c4-code.md)                              | haiku  | C4 Code-level documentation with function signatures and dependencies |
| [c4-component](../plugins/c4-architecture/agents/c4-component.md)                    | sonnet | C4 Component-level architecture synthesis and documentation           |
| [c4-container](../plugins/c4-architecture/agents/c4-container.md)                    | sonnet | C4 Container-level architecture with API documentation                |
| [c4-context](../plugins/c4-architecture/agents/c4-context.md)                        | sonnet | C4 Context-level system documentation with personas and user journeys |

### Business & Operations

#### Business Analysis & Finance

| Agent                                                                            | Model   | Description                                                              |
| -------------------------------------------------------------------------------- | ------- | ------------------------------------------------------------------------ |
| [business-analyst](../plugins/business-analytics/agents/business-analyst.md)     | sonnet  | Metrics analysis, reporting, KPI tracking                                |
| [startup-analyst](../plugins/startup-business-analyst/agents/startup-analyst.md) | inherit | Market sizing, financial modeling, and competitive analysis for startups |

#### Marketing & Sales

| Agent                                                                                             | Model | Description                                           |
| ------------------------------------------------------------------------------------------------- | ----- | ----------------------------------------------------- |
| [social-publishing-publisher](../plugins/social-publishing/agents/social-publishing-publisher.md) | haiku | Multi-platform social media publishing via SocialClaw |

#### Support & Legal

| Agent                                                                   | Model  | Description                                             |
| ----------------------------------------------------------------------- | ------ | ------------------------------------------------------- |
| [hr-pro](../plugins/hr-legal-compliance/agents/hr-pro.md)               | sonnet | HR operations, policies, employee relations             |
| [legal-advisor](../plugins/hr-legal-compliance/agents/legal-advisor.md) | sonnet | Privacy policies, terms of service, legal documentation |

### SEO & Content Optimization

| Agent                                                                                                     | Model  | Description                                          |
| --------------------------------------------------------------------------------------------------------- | ------ | ---------------------------------------------------- |
| [seo-content-auditor](../plugins/seo-content-creation/agents/seo-content-auditor.md)                      | sonnet | Content quality analysis, E-E-A-T signals assessment |
| [seo-meta-optimizer](../plugins/seo-technical-optimization/agents/seo-meta-optimizer.md)                  | haiku  | Meta title and description optimization              |
| [seo-keyword-strategist](../plugins/seo-technical-optimization/agents/seo-keyword-strategist.md)          | haiku  | Keyword analysis and semantic variations             |
| [seo-structure-architect](../plugins/seo-technical-optimization/agents/seo-structure-architect.md)        | haiku  | Content structure and schema markup                  |
| [seo-snippet-hunter](../plugins/seo-technical-optimization/agents/seo-snippet-hunter.md)                  | haiku  | Featured snippet formatting                          |
| [seo-content-refresher](../plugins/seo-analysis-monitoring/agents/seo-content-refresher.md)               | haiku  | Content freshness analysis                           |
| [seo-cannibalization-detector](../plugins/seo-analysis-monitoring/agents/seo-cannibalization-detector.md) | haiku  | Keyword overlap detection                            |
| [seo-authority-builder](../plugins/seo-analysis-monitoring/agents/seo-authority-builder.md)               | sonnet | E-E-A-T signal analysis                              |
| [seo-content-writer](../plugins/seo-content-creation/agents/seo-content-writer.md)                        | sonnet | SEO-optimized content creation                       |
| [seo-content-planner](../plugins/seo-content-creation/agents/seo-content-planner.md)                      | haiku  | Content planning and topic clusters                  |

### Teams, Workflows & Evaluation

| Agent                                                                                   | Model   | Description                                                                                  |
| --------------------------------------------------------------------------------------- | ------- | -------------------------------------------------------------------------------------------- |
| [team-lead](../plugins/agent-teams/agents/team-lead.md)                                 | fable   | Decomposes work into parallel tasks with file ownership and synthesizes results              |
| [team-implementer](../plugins/agent-teams/agents/team-implementer.md)                   | opus    | Parallel feature builder within strict file ownership boundaries                             |
| [team-reviewer](../plugins/agent-teams/agents/team-reviewer.md)                         | opus    | Reviews one assigned dimension (security, performance, architecture, testing, accessibility) |
| [team-debugger](../plugins/agent-teams/agents/team-debugger.md)                         | opus    | Confirms or falsifies one debugging hypothesis with file:line evidence                       |
| [orchestrate](../plugins/ship-mate/agents/orchestrate.md)                               | sonnet  | Turns a story file into an unambiguous spec through clarifying questions                     |
| [architect](../plugins/ship-mate/agents/architect.md)                                   | inherit | Produces a numbered implementation plan and pauses for approval                              |
| [implement](../plugins/ship-mate/agents/implement.md)                                   | sonnet  | Implements the architect plan step by step with tests                                        |
| [review](../plugins/ship-mate/agents/review.md)                                         | inherit | PR review with a three-tier severity taxonomy                                                |
| [qa](../plugins/ship-mate/agents/qa.md)                                                 | sonnet  | Tests acceptance criteria and edge cases, writes a QA report                                 |
| [playwright](../plugins/ship-mate/agents/playwright.md)                                 | sonnet  | Verifies frontend acceptance criteria in a real browser                                      |
| [session-start](../plugins/operating-kit/agents/session-start.md)                       | haiku   | Reads the state doc, verifies live state, and prints a session briefing                      |
| [session-end](../plugins/operating-kit/agents/session-end.md)                           | haiku   | Records lessons, open issues, and next steps at session end                                  |
| [code-review-preshipment](../plugins/operating-kit/agents/code-review-preshipment.md)   | sonnet  | Pre-ship review of all changes since the last deploy                                         |
| [deploy-with-verification](../plugins/operating-kit/agents/deploy-with-verification.md) | sonnet  | Tests, builds, deploys, and verifies the live revision                                       |
| [prod-logs-health-check](../plugins/operating-kit/agents/prod-logs-health-check.md)     | haiku   | Scans recent production logs for errors and anomalies                                        |
| [eval-orchestrator](../plugins/plugin-eval/agents/eval-orchestrator.md)                 | opus    | Orchestrates plugin quality evaluation and certification                                     |
| [eval-judge](../plugins/plugin-eval/agents/eval-judge.md)                               | sonnet  | LLM judge that scores skills with anchored rubrics                                           |

### Specialized Domains

| Agent                                                                              | Model   | Description                                    |
| ---------------------------------------------------------------------------------- | ------- | ---------------------------------------------- |
| [payment-integration](../plugins/payment-processing/agents/payment-integration.md) | sonnet  | Payment processor integration (Stripe, PayPal) |
| [context-manager](../plugins/agent-orchestration/agents/context-manager.md)        | inherit | Multi-agent context management                 |

## Model Configuration

Source agents specify Claude Code model aliases. Other tools use the [adapter model mappings](../tools/adapters/capabilities.py), including fixed defaults for some `inherit` entries. The distribution below counts source assignments.

### Model Distribution Summary

| Model   | Agent Count | Use Case                                                        |
| ------- | ----------- | --------------------------------------------------------------- |
| Fable   | 1           | Longest-horizon autonomous work (tier above Opus; see criteria) |
| Opus    | 49          | Critical architecture, security, code review, production coding |
| Sonnet  | 62          | Complex tasks, support with intelligence                        |
| Haiku   | 18          | Fast operational tasks                                          |
| Inherit | 42          | Complex tasks where the user chooses the model at runtime       |

### Model Selection Criteria

#### Haiku - Fast Execution & Deterministic Tasks

**Use when:**

- Generating code from well-defined specifications
- Creating tests following established patterns
- Writing documentation with clear templates
- Executing infrastructure operations
- Performing database query optimization
- Handling customer support responses
- Processing SEO optimization tasks
- Managing deployment pipelines

#### Sonnet - Complex Reasoning & Architecture

**Use when:**

- Designing system architecture
- Making technology selection decisions
- Performing security audits
- Reviewing code for architectural patterns
- Creating complex AI/ML pipelines
- Providing language-specific expertise
- Orchestrating multi-agent workflows
- Handling business-critical legal/HR matters

#### Fable - Longest-Horizon Autonomous Work

Claude Fable 5 (`model: fable`) is the tier above Opus. It is opt-in in Claude Code
(v2.1.170+, never the default) and carries roughly 2.6× the effective cost of Opus
($10/$50 per MTok plus a ~30% heavier tokenizer), so reserve it for agents where Opus
demonstrably needs multiple attempts.

**Use when:**

- Running multi-hour autonomous sessions (large codebase migrations, overnight refactors)
- Executing end-to-end work from a single well-specified goal
- Coordinating long-lived parallel sub-agent workstreams

**Avoid for:**

- Security-analysis agents — Fable 5's cyber/bio safety classifiers fall back to
  Opus 4.8 on that content anyway
- Anything Sonnet or Opus already completes in one pass

Other harnesses map `fable` to their top available model (see
[authoring.md](authoring.md#model-aliases)). Fable-tier agent bodies should state goals
and constraints rather than step-by-step scaffolding, and must not ask the model to echo
its internal reasoning.

### Hybrid Orchestration Patterns

The plugin ecosystem leverages Sonnet + Haiku orchestration for optimal performance and cost efficiency:

#### Pattern 1: Planning → Execution

```
Sonnet: backend-architect (design API architecture)
  ↓
Haiku: Generate API endpoints following spec
  ↓
Haiku: test-automator (generate comprehensive tests)
  ↓
Sonnet: code-reviewer (architectural review)
```

#### Pattern 2: Reasoning → Action (Incident Response)

```
Sonnet: incident-responder (diagnose issue, create strategy)
  ↓
Haiku: devops-troubleshooter (execute fixes)
  ↓
Haiku: deployment-engineer (deploy hotfix)
  ↓
Haiku: Implement monitoring alerts
```

#### Pattern 3: Complex → Simple (Database Design)

```
Sonnet: database-architect (schema design, technology selection)
  ↓
Haiku: sql-pro (generate migration scripts)
  ↓
Haiku: database-admin (execute migrations)
  ↓
Haiku: database-optimizer (tune query performance)
```

#### Pattern 4: Multi-Agent Workflows

```
Full-Stack Feature Development:
Sonnet: backend-architect + frontend-developer (design components)
  ↓
Haiku: Generate code following designs
  ↓
Haiku: test-automator (unit + integration tests)
  ↓
Sonnet: security-auditor (security review)
  ↓
Haiku: deployment-engineer (CI/CD setup)
  ↓
Haiku: Setup observability stack
```

## Agent Invocation

The examples below use Claude Code. Agent names and invocation methods vary by tool. See the [setup guide](./harnesses.md) for generated agent formats and installation routes.

### Natural Language

The following natural-language examples ask Claude Code to choose a specialist:

```
"Use backend-architect to design the authentication API"
"Have security-auditor scan for OWASP vulnerabilities"
"Get performance-engineer to optimize this database query"
```

### Slash Commands

Claude Code plugin slash commands invoke workflows that can delegate to agents:

```bash
/backend-development:feature-development user authentication
/security-scanning:security-sast
/incident-response:smart-fix "memory leak in payment service"
```

## Contributing

To add a new agent:

1. Create `plugins/{plugin-name}/agents/{agent-name}.md`
2. Add frontmatter with name, description, and model assignment
3. Write comprehensive system prompt
4. No marketplace change needed: agents are auto-discovered from `agents/`

See [Contributing Guide](../CONTRIBUTING.md) for details.
