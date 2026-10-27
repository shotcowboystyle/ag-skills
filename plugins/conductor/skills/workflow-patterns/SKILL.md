---
name: workflow-patterns
description: Use this skill when implementing a task from a Conductor track's plan.md, running its red-green-refactor cycle, committing it with the track ID, closing a phase with the verification checkpoint, or recovering from a failed test or a rejected checkpoint.
version: 1.1.0
---

# Workflow Patterns

How to work one task, and close one phase, in a Conductor track. `conductor/workflow.md`
sets the project's TDD policy, coverage target and commit convention; where it differs from
the defaults here, `workflow.md` wins.

## When to Use This Skill

- Implementing the next task in a track's plan.md
- Closing a phase at its verification checkpoint
- Recovering from failing tests, a rejected checkpoint or a blocked task

## Procedure: one task

1. **Pick the next task**: the first `[ ]` task in the current phase of `plan.md`. Don't
   start a later phase while this one has open tasks.
2. **Mark it `[~]`** in `plan.md`. Only one task is `[~]` at a time.
3. **Red.** Write tests for the task's behavior: the happy path, the edge cases and the
   errors. Run them and confirm they fail for the expected reason. A test that passes before
   the code exists tests nothing; stop and fix the test.
4. **Green.** Write the least code that makes the tests pass. Run them.
5. **Refactor.** Clean up names and duplication with the tests green, running them after
   each change.
6. **Check coverage** for the files you changed against the target in `workflow.md`
   (80% when it sets none), for example `pytest --cov=<module> --cov-report=term-missing`
   or `npx vitest run --coverage`. Add tests for uncovered branches.
7. **Record deviations.** A new dependency goes in `tech-stack.md`; a changed requirement
   goes in `spec.md`; a changed approach is noted under the task in `plan.md`.
8. **Commit the task** with the track ID in the message. `/conductor:revert` finds a track's
   commits by grepping for its ID:

   ```bash
   git commit -m "feat(auth): add password validation (user-auth_20250115)"
   ```

9. **Mark it `[x]`** with the short SHA, and commit the plan change:

   ```markdown
   - [x] Task 2.1: Add password validation `abc1234`
   ```

   ```bash
   git add conductor/tracks/user-auth_20250115/plan.md
   git commit -m "chore: mark task 2.1 complete (user-auth_20250115)"
   ```

10. **Update `metadata.json`**: `tasks.completed` and `updated`.

When `workflow.md` turns TDD off for a task type, skip steps 3 to 5, implement, then run the
existing tests before step 6.

## Procedure: closing a phase

Run this when every task in the phase is `[x]`.

1. **List the changed files** since the last checkpoint:
   `git diff --name-only <last-checkpoint-sha>..HEAD`. Each one has tests.
2. **Run the full test suite**, the linter and the type checker. All must pass.
3. **Run the phase's verification steps** from `plan.md`, and write the manual checks a
   person has to do.
4. **Stop and ask for approval.** Show the results and the manual checklist. Don't start
   the next phase until the user says to continue.
5. **After approval, commit the checkpoint** and record its SHA in the plan's checkpoint
   table and in `metadata.json` (`phases.completed`):

   ```bash
   git commit --allow-empty -m "checkpoint: phase 2 complete (user-auth_20250115)"
   ```

## When something fails

| Situation | Do |
| --- | --- |
| Tests fail after green | Fix before anything else; don't commit red. If the fix is outside the task, mark the task `[!]` and ask. |
| Checkpoint rejected | Add the user's issues as new tasks in the same phase, work them, and close the phase again. |
| Task blocked by another track or a decision | Mark it `[!]` with the reason and ask whether to skip ahead within the phase. |
| Plan is wrong | Stop and propose the plan change; edit `plan.md` only after the user agrees. |

## References

`references/details.md` has the quality gates, commit and git-note formats, deviation
records, TDD variations by task type (data models, endpoints, integrations, refactors), and
checkpoint verification examples.
