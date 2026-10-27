# context-driven-development: artifacts, checklist and integration

The setup, validation and sync procedures are in `SKILL.md`. This file has the detail behind them.

## Core Philosophy

Context-Driven Development treats project context as a first-class artifact managed alongside code. Instead of relying on ad-hoc prompts or scattered documentation, establish a persistent, structured foundation that informs all AI interactions.

Key principles:

1. **Context precedes code**: Define what you're building and how before implementation
2. **Living documentation**: Context artifacts evolve with the project
3. **Single source of truth**: One canonical location for each type of information
4. **AI alignment**: Consistent context produces consistent AI behavior

## The Workflow

Follow the **Context → Spec & Plan → Implement** workflow:

1. **Context Phase**: Establish or verify project context artifacts exist and are current
2. **Specification Phase**: Define requirements and acceptance criteria for work units
3. **Planning Phase**: Break specifications into phased, actionable tasks
4. **Implementation Phase**: Execute tasks following established workflow patterns

## Artifact Relationships

### product.md - Defines WHAT and WHY

Purpose: Captures product vision, goals, target users, and business context.

Contents:

- Product name and one-line description
- Problem statement and solution approach
- Target user personas
- Core features and capabilities
- Success metrics and KPIs
- Product roadmap (high-level)

Update when:

- Product vision or goals change
- New major features are planned
- Target audience shifts
- Business priorities evolve

### product-guidelines.md - Defines HOW to Communicate

Purpose: Establishes brand voice, messaging standards, and communication patterns.

Contents:

- Brand voice and tone guidelines
- Terminology and glossary
- Error message conventions
- User-facing copy standards
- Documentation style

Update when:

- Brand guidelines change
- New terminology is introduced
- Communication patterns need refinement

### tech-stack.md - Defines WITH WHAT

Purpose: Documents technology choices, dependencies, and architectural decisions.

Contents:

- Primary languages and frameworks
- Key dependencies with versions
- Infrastructure and deployment targets
- Development tools and environment
- Testing frameworks
- Code quality tools

Update when:

- Adding new dependencies
- Upgrading major versions
- Changing infrastructure
- Adopting new tools or patterns

### workflow.md - Defines HOW to Work

Purpose: Establishes development practices, quality gates, and team workflows.

Contents:

- Development methodology (TDD, etc.)
- Git workflow and commit conventions
- Code review requirements
- Testing requirements and coverage targets
- Quality assurance gates
- Deployment procedures

Update when:

- Team practices evolve
- Quality standards change
- New workflow patterns are adopted

### tracks.md - Tracks WHAT'S HAPPENING

Purpose: Registry of all work units with status and metadata.

Contents:

- Active tracks with current status
- Completed tracks with completion dates
- Track metadata (type, priority, assignee)
- Links to individual track directories

Update when:

- New tracks are created
- Track status changes
- Tracks are completed or archived

See [references/artifact-templates.md](./artifact-templates.md) for copy-paste starter templates.

## Benefits

### Team Alignment

- New team members onboard faster with explicit context
- Consistent terminology and conventions across the team
- Shared understanding of product goals and technical decisions

### AI Consistency

- AI assistants produce aligned outputs across sessions
- Reduced need to re-explain context in each interaction
- Predictable behavior based on documented standards

### Institutional Memory

- Decisions and rationale are preserved
- Context survives team changes
- Historical context informs future decisions

### Quality Assurance

- Standards are explicit and verifiable
- Deviations from context are detectable
- Quality gates are documented and enforceable

## Directory Structure

```
conductor/
├── index.md              # Navigation hub linking all artifacts
├── product.md            # Product vision and goals
├── product-guidelines.md # Communication standards
├── tech-stack.md         # Technology preferences
├── workflow.md           # Development practices
├── tracks.md             # Work unit registry
├── setup_state.json      # Resumable setup state
├── code_styleguides/     # Language-specific conventions
│   ├── python.md
│   ├── typescript.md
│   └── ...
└── tracks/
    └── <track-id>/
        ├── spec.md
        ├── plan.md
        ├── metadata.json
        └── index.md
```

## Context Lifecycle

1. **Creation**: Initial setup via `/conductor:setup`
2. **Validation**: Verify before each track
3. **Evolution**: Update as project grows
4. **Synchronization**: Keep artifacts aligned
5. **Archival**: Document historical decisions

## Context Validation Checklist

Before starting implementation on any track, validate context:

### Product Context

- [ ] product.md reflects current product vision
- [ ] Target users are accurately described
- [ ] Feature list is up to date
- [ ] Success metrics are defined

### Technical Context

- [ ] tech-stack.md lists all current dependencies
- [ ] Version numbers are accurate
- [ ] Infrastructure targets are correct
- [ ] Development tools are documented

### Workflow Context

- [ ] workflow.md describes current practices
- [ ] Quality gates are defined
- [ ] Coverage targets are specified
- [ ] Commit conventions are documented

### Track Context

- [ ] tracks.md shows all active work
- [ ] No stale or abandoned tracks
- [ ] Dependencies between tracks are noted

## Common Anti-Patterns

Avoid these context management mistakes:

### Stale Context

Problem: Context documents become outdated and misleading.
Solution: Update context as part of each track's completion process.

### Context Sprawl

Problem: Information scattered across multiple locations.
Solution: Use the defined artifact structure; resist creating new document types.

### Implicit Context

Problem: Relying on knowledge not captured in artifacts.
Solution: If you reference something repeatedly, add it to the appropriate artifact.

### Context Hoarding

Problem: One person maintains context without team input.
Solution: Review context artifacts in pull requests; make updates collaborative.

### Over-Specification

Problem: Context becomes so detailed it's impossible to maintain.
Solution: Keep artifacts focused on decisions that affect AI behavior and team alignment.

## Integration with Development Tools

### IDE Integration

Configure your IDE to display context files prominently:

- Pin conductor/product.md for quick reference
- Add tech-stack.md to project notes
- Create snippets for common patterns from style guides

### Git Hooks

Consider pre-commit hooks that:

- Warn when dependencies change without tech-stack.md update
- Remind to update product.md when feature branches merge
- Validate context artifact syntax

### CI/CD Integration

Include context validation in pipelines:

- Check tech-stack.md matches actual dependencies
- Verify links in context documents resolve
- Ensure tracks.md status matches git branch state
