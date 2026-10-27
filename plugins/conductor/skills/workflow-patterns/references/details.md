# workflow-patterns: gates, formats and variations

The task and phase procedures are in `SKILL.md`. This file has the detail behind them.

## Quality Assurance Gates

Before marking any task complete, verify these gates:

### Passing Tests

- All existing tests pass
- New tests pass
- No test regressions

### Coverage >= 80%

- New code has 80%+ coverage
- Overall project coverage maintained
- Critical paths fully covered

### Style Compliance

- Code follows style guides
- Linting passes
- Formatting correct

### Documentation

- Public APIs documented
- Complex logic explained
- README updated if needed

### Type Safety

- Type hints present (if applicable)
- Type checker passes
- No type: ignore without reason

### No Linting Errors

- Zero linter errors
- Warnings addressed or justified
- Static analysis clean

### Mobile Compatibility

If applicable:

- Responsive design verified
- Touch interactions work
- Performance acceptable

### Security Audit

- No secrets in code
- Input validation present
- Authentication/authorization correct
- Dependencies vulnerability-free

## Git Integration

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types:

- `feat`: New feature
- `fix`: Bug fix
- `refactor`: Code change without feature/fix
- `test`: Adding tests
- `docs`: Documentation
- `chore`: Maintenance

### Git Notes for Rich Summaries

Attach detailed notes to commits:

```bash
git notes add -m "<detailed summary>"
```

View notes:

```bash
git log --show-notes
```

Benefits:

- Preserves context without cluttering commit message
- Enables semantic queries across commits
- Supports track-based operations

### SHA Recording in plan.md

Always record the commit SHA when completing tasks:

```markdown
- [x] Task 1.1: Setup schema `abc1234`
- [x] Task 1.2: Add model `def5678`
```

This enables:

- Traceability from plan to code
- Semantic revert operations
- Progress auditing

## Verification Checkpoints

### Why Checkpoints Matter

Checkpoints create restore points for semantic reversion:

- Revert to end of any phase
- Maintain logical code state
- Enable safe experimentation

### When to Create Checkpoints

Create checkpoint after:

- All phase tasks complete
- All phase verifications pass
- User approval received

### Checkpoint Commit Content

Include in checkpoint commit:

- All uncommitted changes
- Updated plan.md
- Updated metadata.json
- Any documentation updates

### How to Use Checkpoints

For reverting:

```bash
# Revert to end of Phase 1
git revert --no-commit <phase-2-commits>...
git commit -m "revert: rollback to phase 1 checkpoint"
```

For review:

```bash
# See what changed in Phase 2
git diff <phase-1-sha>..<phase-2-sha>
```

## Handling Deviations

During implementation, deviations from the plan may occur. Handle them systematically:

### Types of Deviations

**Scope Addition**
Discovered requirement not in original spec.

- Document in spec.md as new requirement
- Add tasks to plan.md
- Note addition in task comments

**Scope Reduction**
Feature deemed unnecessary during implementation.

- Mark tasks as `[-]` (skipped) with reason
- Update spec.md scope section
- Document decision rationale

**Technical Deviation**
Different implementation approach than planned.

- Note deviation in task completion comment
- Update tech-stack.md if dependencies changed
- Document why original approach was unsuitable

**Requirement Change**
Understanding of requirement changes during work.

- Update spec.md with corrected requirement
- Adjust plan.md tasks if needed
- Re-verify acceptance criteria

### Deviation Documentation Format

When completing a task with deviation:

```markdown
- [x] Task 2.1: Implement validation `abc1234`
  - DEVIATION: Used library instead of custom code
  - Reason: Better edge case handling
  - Impact: Added email-validator to dependencies
```

## Error Recovery

### Failed Tests After GREEN

If tests fail after reaching GREEN:

1. Do NOT proceed to REFACTOR
2. Identify which test started failing
3. Check if refactoring broke something
4. Revert to last known GREEN state
5. Re-approach the implementation

### Checkpoint Rejection

If user rejects a checkpoint:

1. Note rejection reason in plan.md
2. Create tasks to address issues
3. Complete remediation tasks
4. Request checkpoint approval again

### Blocked by Dependency

If task cannot proceed:

1. Mark task as `[!]` with blocker description
2. Check if other tasks can proceed
3. Document expected resolution timeline
4. Consider creating dependency resolution track

## TDD Variations by Task Type

### Data Model Tasks

```
RED: Write test for model creation and validation
GREEN: Implement model class with fields
REFACTOR: Add computed properties, improve types
```

### API Endpoint Tasks

```
RED: Write test for request/response contract
GREEN: Implement endpoint handler
REFACTOR: Extract validation, improve error handling
```

### Integration Tasks

```
RED: Write test for component interaction
GREEN: Wire components together
REFACTOR: Improve error propagation, add logging
```

### Refactoring Tasks

```
RED: Add characterization tests for current behavior
GREEN: Apply refactoring (tests should stay green)
REFACTOR: Clean up any introduced complexity
```

## Working with Existing Tests

When modifying code with existing tests:

### Extend, Don't Replace

- Keep existing tests passing
- Add new tests for new behavior
- Update tests only when requirements change

### Test Migration

When refactoring changes test structure:

1. Run existing tests (should pass)
2. Add new tests for refactored code
3. Migrate test cases to new structure
4. Remove old tests only after new tests pass

### Regression Prevention

After any change:

1. Run full test suite
2. Check for unexpected failures
3. Investigate any new failures
4. Fix regressions before proceeding

## Checkpoint Verification Details

### Automated Verification

Run before requesting approval:

```bash
# Test suite
pytest -v --tb=short

# Coverage
pytest --cov=src --cov-report=term-missing

# Linting
ruff check src/ tests/

# Type checking (if applicable)
mypy src/
```

### Manual Verification Guidance

For manual items, provide specific instructions:

```markdown
## Manual Verification Steps

### User Registration

1. Navigate to /register
2. Enter valid email: test@example.com
3. Enter password meeting requirements
4. Click Submit
5. Verify success message appears
6. Verify user appears in database

### Error Handling

1. Enter invalid email: "notanemail"
2. Verify error message shows
3. Verify form retains other entered data
```

## Performance Considerations

### Test Suite Performance

Keep test suite fast:

- Use fixtures to avoid redundant setup
- Mock slow external calls
- Run subset during development, full suite at checkpoints

### Commit Performance

Keep commits atomic:

- One logical change per commit
- Complete thought, not work-in-progress
- Tests should pass after every commit
