# Complete Plugin Reference

Browse all 74 marketplace plugins organized by category: 73 local plugins plus 1 external Claude Code marketplace entry (`hol-guard`). The local source supports seven coding tools through native formats and adapters. Install commands below use Claude Code syntax. See the [tool setup guide](./harnesses.md) for other installation routes.

## Quick Start - Essential Plugins

> 💡 **Getting Started?** Install these popular plugins for immediate productivity gains.

### Development Essentials

**code-documentation** - Documentation and technical writing

```bash
/plugin install code-documentation
```

Automated doc generation, code explanation, and tutorial creation for comprehensive technical documentation.

**debugging-toolkit** - Smart debugging and developer experience

```bash
/plugin install debugging-toolkit
```

Interactive debugging, error analysis, and DX optimization for faster problem resolution.

**git-workflows** - Git automation and PR enhancement

```bash
/plugin install git-workflows
```

Git workflow automation, pull request enhancement, and team onboarding processes.

### Full-Stack Development

**backend-development** - Backend API design and architecture

```bash
/plugin install backend-development
```

RESTful and GraphQL API design with test-driven development and modern backend architecture patterns.

**frontend-mobile-development** - UI and mobile development

```bash
/plugin install frontend-mobile-development
```

React/React Native component development with automated scaffolding and cross-platform implementation.

**full-stack-orchestration** - End-to-end feature development

```bash
/plugin install full-stack-orchestration
```

Multi-agent coordination from backend → frontend → testing → security → deployment.

### Testing & Quality

**unit-testing** - Automated test generation

```bash
/plugin install unit-testing
```

Generate pytest (Python) and Jest (JavaScript) unit tests automatically with comprehensive edge case coverage.

### Infrastructure & Operations

**cloud-infrastructure** - Cloud architecture design

```bash
/plugin install cloud-infrastructure
```

AWS/Azure/GCP architecture, Kubernetes setup, Terraform IaC, and multi-cloud cost optimization.

**incident-response** - Production incident management

```bash
/plugin install incident-response
```

Rapid incident triage, root cause analysis, and automated resolution workflows for production systems.

### Language Support

**python-development** - Python project scaffolding

```bash
/plugin install python-development
```

FastAPI/Django project initialization with modern tooling (uv, ruff) and production-ready architecture.

**javascript-typescript** - JavaScript/TypeScript scaffolding

```bash
/plugin install javascript-typescript
```

Next.js, React + Vite, and Node.js project setup with pnpm and TypeScript best practices.

---

## Complete Plugin Catalog

### 🎨 Development (6 plugins)

| Plugin                          | Description                                                           | Install                                       |
| ------------------------------- | --------------------------------------------------------------------- | --------------------------------------------- |
| **debugging-toolkit**           | Interactive debugging and DX optimization                             | `/plugin install debugging-toolkit`           |
| **backend-development**         | Backend API design with GraphQL and TDD                               | `/plugin install backend-development`         |
| **frontend-mobile-development** | Frontend UI and mobile development                                    | `/plugin install frontend-mobile-development` |
| **ui-design**                   | UI/UX design for mobile (iOS, Android, React Native) and web          | `/plugin install ui-design`                   |
| **multi-platform-apps**         | Cross-platform app coordination (web/iOS/Android)                     | `/plugin install multi-platform-apps`         |
| **developer-essentials**        | Essential Git, SQL, code review, auth, debugging, and monorepo skills | `/plugin install developer-essentials`        |

### 📚 Documentation (5 plugins)

| Plugin                       | Description                                                                                                                                     | Install                                    |
| ---------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------ |
| **documentation-standards**  | HADS semantic tagging conventions plus the grounded-vault pattern for provenance-linked, drift-checked knowledge stores                         | `/plugin install documentation-standards`  |
| **code-documentation**       | Documentation generation and code explanation                                                                                                   | `/plugin install code-documentation`       |
| **documentation-generation** | OpenAPI specs, Mermaid diagrams, tutorials                                                                                                      | `/plugin install documentation-generation` |
| **c4-architecture**          | Comprehensive C4 architecture documentation workflow with bottom-up code analysis, component synthesis, container mapping, and context diagrams | `/plugin install c4-architecture`          |
| **avoid-ai-writing**         | Audit and rewrite prose that reads as machine-generated across READMEs, changelogs, PR descriptions, and docs                                   | `/plugin install avoid-ai-writing`         |

### 🔄 Workflows (8 plugins)

| Plugin                       | Description                                                                                                                                                   | Install                                    |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------ |
| **conductor**                | Context-Driven Development with tracks, specs, and phased implementation plans                                                                                | `/plugin install conductor`                |
| **git-workflows**         | Git automation and PR enhancement                                                                                                                             | `/plugin install git-workflows`            |
| **full-stack-orchestration** | End-to-end feature orchestration                                                                                                                              | `/plugin install full-stack-orchestration` |
| **operating-kit**            | Session lifecycle, pre-ship review, deploy with live verification + state doc update, prod log health check                                                   | `/plugin install operating-kit`            |
| **tdd-workflows**            | Test-driven development methodology                                                                                                                           | `/plugin install tdd-workflows`            |
| **agent-teams**              | Parallel code review, debugging, feature, and research teams                                                                                                  | `/plugin install agent-teams`              |
| **ship-mate**                | Story-file to reviewed, tested PR workflow orchestration                                                                                                      | `/plugin install ship-mate`                |
| **superself**                | Drive the Superself `self` CLI: project state (goals, decisions, work units, reports) outside the code repo, context at session start, done gated by evidence | `/plugin install superself`                |

### ✅ Testing (1 plugin)

| Plugin           | Description                                        | Install                        |
| ---------------- | -------------------------------------------------- | ------------------------------ |
| **unit-testing** | Automated unit test generation (Python/JavaScript) | `/plugin install unit-testing` |

### 🔍 Quality (4 plugins)

| Plugin                         | Description                                                                              | Install                                      |
| ------------------------------ | ---------------------------------------------------------------------------------------- | -------------------------------------------- |
| **comprehensive-review**       | Multi-perspective code analysis                                                          | `/plugin install comprehensive-review`       |
| **performance-testing-review** | Performance analysis and test coverage review                                            | `/plugin install performance-testing-review` |
| **plugin-eval**                | Static lint for Claude Code plugins and skills, with experimental LLM scoring for skills | `/plugin install plugin-eval`                |
| **skill-forge-essentials**     | Behavioral skills for AI code debt detection and session compaction survival             | `/plugin install skill-forge-essentials`     |

### 🛠️ Utilities (3 plugins)

| Plugin                    | Description                                | Install                                 |
| ------------------------- | ------------------------------------------ | --------------------------------------- |
| **error-debugging**       | Error analysis and trace debugging         | `/plugin install error-debugging`       |
| **file-conversion**       | Local file conversion with installed tools | `/plugin install file-conversion`       |
| **team-collaboration**    | Team workflows and standup automation      | `/plugin install team-collaboration`    |

### 🤖 AI & ML (6 plugins)

| Plugin                   | Description                                                                                                                  | Install                                |
| ------------------------ | ---------------------------------------------------------------------------------------------------------------------------- | -------------------------------------- |
| **llm-application-dev**  | LLM apps and prompt engineering                                                                                              | `/plugin install llm-application-dev`  |
| **agent-orchestration**  | Multi-agent system optimization                                                                                              | `/plugin install agent-orchestration`  |
| **context-management**   | Context persistence and restoration                                                                                          | `/plugin install context-management`   |
| **machine-learning-ops** | ML training pipelines and MLOps                                                                                              | `/plugin install machine-learning-ops` |
| **llm-finetuning**       | Eval-gated LLM fine-tuning lifecycle: dataset prep, LoRA/QLoRA training, and promotion gating                                | `/plugin install llm-finetuning`       |
| **dgx-spark-ops**        | NVIDIA DGX Spark (GB10) environment ops: aarch64/CUDA-13 stack setup, training preflights, unified-memory/thermal management | `/plugin install dgx-spark-ops`        |

### 📊 Data (1 plugin)

| Plugin                    | Description                        | Install                                 |
| ------------------------- | ---------------------------------- | --------------------------------------- |
| **data-engineering**      | ETL pipelines and data warehouses  | `/plugin install data-engineering`      |

### 🗄️ Database (2 plugins)

| Plugin                  | Description                             | Install                               |
| ----------------------- | --------------------------------------- | ------------------------------------- |
| **database-design**     | Database architecture and schema design | `/plugin install database-design`     |
| **database-migrations** | Database migration automation           | `/plugin install database-migrations` |

### 🚨 Operations (3 plugins)

| Plugin                       | Description                           | Install                                    |
| ---------------------------- | ------------------------------------- | ------------------------------------------ |
| **incident-response**        | Production incident management        | `/plugin install incident-response`        |
| **distributed-debugging**    | Distributed system tracing            | `/plugin install distributed-debugging`    |
| **observability-monitoring** | Metrics, logging, tracing, and SLO    | `/plugin install observability-monitoring` |

### ⚡ Performance (2 plugins)

| Plugin                          | Description                                | Install                                       |
| ------------------------------- | ------------------------------------------ | --------------------------------------------- |
| **application-performance**     | Application profiling and optimization     | `/plugin install application-performance`     |
| **database-cloud-optimization** | Database query and cloud cost optimization | `/plugin install database-cloud-optimization` |

### ☁️ Infrastructure (6 plugins)

| Plugin                    | Description                                 | Install                                 |
| ------------------------- | ------------------------------------------- | --------------------------------------- |
| **deployment-strategies** | Deployment patterns and rollback automation | `/plugin install deployment-strategies` |
| **deployment-validation** | Pre-deployment checks and validation        | `/plugin install deployment-validation` |
| **kubernetes-operations** | K8s manifests and GitOps workflows          | `/plugin install kubernetes-operations` |
| **cloud-infrastructure**  | AWS/Azure/GCP cloud architecture            | `/plugin install cloud-infrastructure`  |
| **cicd-automation**       | CI/CD pipeline configuration                | `/plugin install cicd-automation`       |
| **email-deliverability**  | MX/SPF/DKIM/DMARC planning, audit, verify   | `/plugin install email-deliverability`  |

### 🔒 Security (6 plugins)

| Plugin                       | Description                                                            | Install                                    |
| ---------------------------- | ---------------------------------------------------------------------- | ------------------------------------------ |
| **security-scanning**        | SAST analysis and vulnerability scanning                               | `/plugin install security-scanning`        |
| **backend-api-security**     | API security and authentication                                        | `/plugin install backend-api-security`     |
| **frontend-mobile-security** | XSS/CSRF prevention and mobile security                                | `/plugin install frontend-mobile-security` |
| **reverse-engineering**      | Binary analysis, malware triage, firmware security (authorized)        | `/plugin install reverse-engineering`      |
| **block-no-verify**          | PreToolUse hook blocking `--no-verify` and hook-bypass flags           | `/plugin install block-no-verify`          |
| **hol-guard**                | Local pre-execution policy and pre-install agent supply-chain scanning | `/plugin install hol-guard`                |

### 🛡️ Governance (3 plugins)

| Plugin                      | Description                                                                                                              | Install                                   |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------- |
| **protect-mcp**             | Cedar policy enforcement + Ed25519 signed receipts for every tool call; offline-verifiable audit trail via hash chaining | `/plugin install protect-mcp`             |
| **signed-audit-trails**     | Cookbook-style signed audit trail patterns for Claude Code tool calls                                                    | `/plugin install signed-audit-trails`     |
| **review-agent-governance** | Human approval governance before AI agents post reviews, comments, merges, or CI writes                                  | `/plugin install review-agent-governance` |

### 🔄 Modernization (1 plugin)

| Plugin                  | Description                               | Install                               |
| ----------------------- | ----------------------------------------- | ------------------------------------- |
| **codebase-cleanup**    | Technical debt reduction and cleanup      | `/plugin install codebase-cleanup`    |

### 🌐 API (2 plugins)

| Plugin                        | Description                 | Install                                     |
| ----------------------------- | --------------------------- | ------------------------------------------- |
| **api-scaffolding**           | REST/GraphQL API generation | `/plugin install api-scaffolding`           |
| **api-testing-observability** | API testing and monitoring  | `/plugin install api-testing-observability` |

### 📢 Marketing (4 plugins)

| Plugin                         | Description                             | Install                                      |
| ------------------------------ | --------------------------------------- | -------------------------------------------- |
| **seo-content-creation**       | SEO content writing and planning        | `/plugin install seo-content-creation`       |
| **seo-technical-optimization** | Meta tags, keywords, and schema markup  | `/plugin install seo-technical-optimization` |
| **seo-analysis-monitoring**    | Content analysis and authority building | `/plugin install seo-analysis-monitoring`    |
| **social-publishing**          | Multi-platform social media publishing  | `/plugin install social-publishing`          |

### 💼 Business (4 plugins)

| Plugin                       | Description                                                                           | Install                                    |
| ---------------------------- | ------------------------------------------------------------------------------------- | ------------------------------------------ |
| **business-analytics**       | KPI tracking and financial reporting                                                  | `/plugin install business-analytics`       |
| **startup-business-analyst** | Market sizing, financial modeling, team planning, and strategic research for startups | `/plugin install startup-business-analyst` |
| **before-you-build**         | Pre-build product risk review for founders, product teams, and AI-assisted builders   | `/plugin install before-you-build`         |
| **hr-legal-compliance**      | HR policies and legal templates                                                       | `/plugin install hr-legal-compliance`      |

### 💻 Languages (4 plugins)

| Plugin                    | Description                                     | Install                                 |
| ------------------------- | ----------------------------------------------- | --------------------------------------- |
| **python-development**    | Python 3.12+ with Django/FastAPI                | `/plugin install python-development`    |
| **javascript-typescript** | JavaScript/TypeScript with Node.js              | `/plugin install javascript-typescript` |
| **systems-programming**   | Rust, Go, C, C++ for systems development        | `/plugin install systems-programming`   |
| **shell-scripting**       | Production-grade Bash and POSIX shell scripting | `/plugin install shell-scripting`       |

### 💳 Payments (1 plugin)

| Plugin                 | Description                           | Install                              |
| ---------------------- | ------------------------------------- | ------------------------------------ |
| **payment-processing** | Stripe/PayPal integration and billing | `/plugin install payment-processing` |

### 🎮 Gaming (1 plugin)

| Plugin               | Description                            | Install                            |
| -------------------- | -------------------------------------- | ---------------------------------- |
| **game-development** | Unity and Minecraft plugin development | `/plugin install game-development` |

### ♿ Accessibility (1 plugin)

| Plugin                       | Description                        | Install                                    |
| ---------------------------- | ---------------------------------- | ------------------------------------------ |
| **accessibility-compliance** | WCAG auditing and inclusive design | `/plugin install accessibility-compliance` |

## Plugin Structure

Each plugin contains:

- **agents/** - Specialized agents for that domain
- **commands/** - Tools and workflows specific to that plugin
- **skills/** - Optional modular knowledge packages (progressive disclosure)

Example:

```
plugins/python-development/
├── agents/
│   ├── python-pro.md
│   ├── django-pro.md
│   └── fastapi-pro.md
├── commands/
│   └── python-scaffold.md
└── skills/
    ├── async-python-patterns/
    ├── python-testing-patterns/
    ├── python-packaging/
    ├── python-performance-optimization/
    └── uv-package-manager/
```

## Installation

The marketplace commands in this section run inside Claude Code. Other tools use the [per-tool installation routes](./harnesses.md#native-install).

### Step 1: Add the Marketplace

```bash
/plugin marketplace add shotcowboystyle/ag-skills
```

This makes all 74 marketplace plugins available for installation, but **does not load any agents or tools** into your context.

### Step 2: Install Specific Plugins

Browse available plugins:

```bash
/plugin
```

Install only the plugins you need:

```bash
/plugin install python-development
/plugin install backend-development
```

Installing a Claude Code plugin makes its agents, commands, and skills available. Claude loads skill guidance when relevant to the task.

### Skills Only (Any Agent)

To take one skill without its plugin, use an Agent Skills installer. Both read `plugins/*/skills/` from GitHub directly and install into Claude Code or any other agent they support:

```bash
gh skill install shotcowboystyle/ag-skills python-testing-patterns --agent claude-code   # GitHub CLI 2.90+
npx skills add shotcowboystyle/ag-skills --skill python-testing-patterns -a claude-code  # vercel-labs/skills
```

Selectors, install paths, and gotchas: [harnesses.md](./harnesses.md#skills-only-installers).

## Plugin Design Principles

### Single Responsibility

- Each plugin does **one thing well** (Unix philosophy)
- Clear, focused purposes (describable in 5-10 words)
- Average plugin size: **5.9 components** (follows Anthropic's 2-8 pattern)

### Minimal Token Usage

- Install only what you need
- Each plugin loads only its specific agents and tools
- No unnecessary resources loaded into context
- Better context efficiency with granular plugins

### Composability

- Mix and match plugins for complex workflows
- Workflow orchestrators compose focused plugins
- Clear boundaries between plugins
- No forced feature bundling

## See Also

- [Agent Skills](./agent-skills.md) - 167 specialized skills across plugins
- [Agent Reference](./agents.md) - Complete agent catalog
- [Usage Guide](./usage.md) - Commands and workflows
- [Architecture](./architecture.md) - Design principles
