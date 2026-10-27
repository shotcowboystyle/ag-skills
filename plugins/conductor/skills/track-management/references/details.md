# track-management: templates, checklists and patterns

The procedure and the file formats are in `SKILL.md`. This file has the templates and the
checklists to run against them.

## Track Concept

A track is a logical work unit that encapsulates a complete piece of work. Each track has:

- A unique identifier
- A specification defining requirements
- A phased plan breaking work into tasks
- Metadata tracking status and progress

Tracks provide semantic organization for work, enabling:

- Clear scope boundaries
- Progress tracking
- Git-aware operations (revert by track)
- Team coordination

## Track Types

### feature

New functionality or capabilities. Use for:

- New user-facing features
- New API endpoints
- New integrations
- Significant enhancements

### bug

Defect fixes. Use for:

- Incorrect behavior
- Error conditions
- Performance regressions
- Security vulnerabilities

### chore

Maintenance and housekeeping. Use for:

- Dependency updates
- Configuration changes
- Documentation updates
- Cleanup tasks

### refactor

Code improvement without behavior change. Use for:

- Code restructuring
- Pattern adoption
- Technical debt reduction
- Performance optimization (same behavior, better performance)

## Specification (spec.md) Structure

```markdown
# {Track Title}

## Overview

Brief description of what this track accomplishes and why.

## Functional Requirements

### FR-1: {Requirement Name}

Description of the functional requirement.

- Acceptance: How to verify this requirement is met

### FR-2: {Requirement Name}

...

## Non-Functional Requirements

### NFR-1: {Requirement Name}

Description of the non-functional requirement (performance, security, etc.)

- Target: Specific measurable target
- Verification: How to test

## Acceptance Criteria

- [ ] Criterion 1: Specific, testable condition
- [ ] Criterion 2: Specific, testable condition
- [ ] Criterion 3: Specific, testable condition

## Scope

### In Scope

- Explicitly included items
- Features to implement
- Components to modify

### Out of Scope

- Explicitly excluded items
- Future considerations
- Related but separate work

## Dependencies

### Internal

- Other tracks or components this depends on
- Required context artifacts

### External

- Third-party services or APIs
- External dependencies

## Risks and Mitigations

| Risk             | Impact          | Mitigation          |
| ---------------- | --------------- | ------------------- |
| Risk description | High/Medium/Low | Mitigation strategy |

## Open Questions

- [ ] Question that needs resolution
- [x] Resolved question - Answer
```

## Plan (plan.md) Structure

```markdown
# Implementation Plan: {Track Title}

Track ID: `{track-id}`
Created: YYYY-MM-DD
Status: pending | in-progress | completed

## Overview

Brief description of implementation approach.

## Phase 1: {Phase Name}

### Tasks

- [ ] Task 1.1: Task description
  - Sub-task or detail
  - Sub-task or detail
- [ ] Task 1.2: Task description
- [ ] Task 1.3: Task description

### Verification

- [ ] Verify 1.1: Verification step for phase

## Phase 2: {Phase Name}

### Tasks

- [ ] Task 2.1: Task description
- [ ] Task 2.2: Task description

### Verification

- [ ] Verify 2.1: Verification step for phase

## Phase 3: Finalization

### Tasks

- [ ] Task 3.1: Update documentation
- [ ] Task 3.2: Final integration test

### Verification

- [ ] Verify 3.1: All acceptance criteria met

## Checkpoints

| Phase   | Checkpoint SHA | Date | Status  |
| ------- | -------------- | ---- | ------- |
| Phase 1 |                |      | pending |
| Phase 2 |                |      | pending |
| Phase 3 |                |      | pending |
```

## Handling Track Dependencies

### Identifying Dependencies

During track creation, identify:

- **Hard dependencies**: Must complete before this track can start
- **Soft dependencies**: Can proceed in parallel but may affect integration
- **External dependencies**: Third-party services, APIs, or team decisions

### Documenting Dependencies

In spec.md, list dependencies with:

- Dependency type (hard/soft/external)
- Current status (available/pending/blocked)
- Resolution path (what needs to happen)

### Managing Blocked Tracks

When a track is blocked:

1. Mark blocked tasks with `[!]` and reason
2. Update tracks.md status
3. Document blocker in metadata.json
4. Consider creating dependency track if needed

## Track Sizing Guidelines

### Right-Sized Tracks

Aim for tracks that:

- Complete in 1-5 days of work
- Have 2-4 phases
- Contain 8-20 tasks total
- Deliver a coherent, testable unit

### Too Large

Signs a track is too large:

- More than 5 phases
- More than 25 tasks
- Multiple unrelated features
- Estimated duration > 1 week

Solution: Split into multiple tracks with clear boundaries.

### Too Small

Signs a track is too small:

- Single phase with 1-2 tasks
- No meaningful verification needed
- Could be a sub-task of another track
- Less than a few hours of work

Solution: Combine with related work or handle as part of existing track.

## Specification Quality Checklist

Before finalizing spec.md, verify:

### Requirements Quality

- [ ] Each requirement has clear acceptance criteria
- [ ] Requirements are testable
- [ ] Requirements are independent (can verify separately)
- [ ] No ambiguous language ("should be fast" → "response < 200ms")

### Scope Clarity

- [ ] In-scope items are specific
- [ ] Out-of-scope items prevent scope creep
- [ ] Boundaries are clear to implementer

### Dependencies Identified

- [ ] All internal dependencies listed
- [ ] External dependencies have owners/contacts
- [ ] Dependency status is current

### Risks Addressed

- [ ] Major risks identified
- [ ] Impact assessment realistic
- [ ] Mitigations are actionable

## Plan Quality Checklist

Before starting implementation, verify plan.md:

### Task Quality

- [ ] Tasks are atomic (one logical action)
- [ ] Tasks are independently verifiable
- [ ] Task descriptions are clear
- [ ] Sub-tasks provide helpful detail

### Phase Organization

- [ ] Phases group related tasks
- [ ] Each phase delivers something testable
- [ ] Verification tasks after each phase
- [ ] Phases build on each other logically

### Completeness

- [ ] All spec requirements have corresponding tasks
- [ ] Documentation tasks included
- [ ] Testing tasks included
- [ ] Integration tasks included

## Common Track Patterns

### Feature Track Pattern

```
Phase 1: Foundation
- Data models
- Database migrations
- Basic API structure

Phase 2: Core Logic
- Business logic implementation
- Input validation
- Error handling

Phase 3: Integration
- UI integration
- API documentation
- End-to-end tests
```

### Bug Fix Track Pattern

```
Phase 1: Reproduction
- Write failing test capturing bug
- Document reproduction steps

Phase 2: Fix
- Implement fix
- Verify test passes
- Check for regressions

Phase 3: Verification
- Manual verification
- Update documentation if needed
```

### Refactor Track Pattern

```
Phase 1: Preparation
- Add characterization tests
- Document current behavior

Phase 2: Refactoring
- Apply changes incrementally
- Maintain green tests throughout

Phase 3: Cleanup
- Remove dead code
- Update documentation
```
