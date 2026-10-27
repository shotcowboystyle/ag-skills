---
name: track-management
description: Use this skill when creating, sizing, updating, completing or archiving a Conductor track (the work unit for one feature, bug, chore or refactor), or when reading or writing its spec.md, plan.md, metadata.json or its row in conductor/tracks.md.
version: 1.1.0
---

# Track Management

A track is one unit of work, a feature, bug, chore or refactor, with a spec, a phased plan and
metadata. The Conductor commands read these files by format, so write them exactly as below.

## When to Use This Skill

- Creating a feature, bug, chore or refactor track
- Writing or reviewing a track's spec.md or plan.md
- Updating, finishing or archiving a track

## Procedure

### Create a track (`/conductor:new-track`)

1. **Gather the requirements**: summary, acceptance criteria, scope in and out, dependencies,
   risks. Each acceptance criterion must be testable.
2. **Generate the ID**: `{shortname}_{YYYYMMDD}`, where the shortname is 2 to 4 lowercase
   words joined by hyphens and the date is today. If the ID is already in `tracks.md`,
   append `_2`, `_3` and so on.

   ```text
   user-auth_20250115      fix-login-error_20250115      user-auth_20250115_2
   ```

3. **Size it** before writing the plan: 2 to 4 phases, 3 to 5 tasks per phase. More than 5
   phases or 25 tasks: split the track. One phase of 1 or 2 tasks: fold it into another track.
4. **Write `conductor/tracks/<id>/spec.md`** with summary, requirements, acceptance criteria,
   scope, dependencies and risks (template in `references/details.md`).
5. **Write `plan.md`**: phases, each with numbered tasks and a verification step. Every
   requirement in the spec maps to at least one task.
6. **Write `metadata.json`** and the track's `index.md`.
7. **Register it**: add a row to the table in `conductor/tracks.md` and a link in
   `conductor/index.md`.

### Work a track (`/conductor:implement`)

1. Validate the track first (the command runs `conductor-validator` in `track` mode).
2. Set the registry row to `[~]` and `metadata.json` `status` to `in_progress`.
3. Work tasks in order with the `workflow-patterns` skill. Only one task is `[~]` at a time.
4. After each task, update its marker in `plan.md` and `tasks.completed` in `metadata.json`.
5. Mark a blocked task `[!]` with the reason on the same line, and record the blocker in the
   spec's dependencies.

### Finish a track

1. Check every acceptance criterion in `spec.md` and run the full test suite.
2. Set the registry row to `[x]`, `metadata.json` `status` to `completed`, and the phase and
   task counts to their totals.
3. Sync `product.md` and `tech-stack.md` (the `context-driven-development` skill).
4. Archive with `/conductor:manage --archive <id>`. Archive, don't delete: `/conductor:revert`
   finds commits by track ID.

## Formats

**Registry row** in `conductor/tracks.md`:

```markdown
| Status | Track ID | Title | Created | Updated |
| ------ | -------- | ----- | ------- | ------- |
| [~] | user-auth_20250115 | User Authentication | 2025-01-15 | 2025-01-16 |
```

**Task line** in `plan.md`. `/conductor:implement` and `/conductor:status` match this shape:

```markdown
- [ ] Task 1.1: Create the users table
- [x] Task 1.2: Add the User model `abc1234`
```

**Markers**, for registry rows and tasks:

| Marker | Meaning |
| --- | --- |
| `[ ]` | Pending |
| `[~]` | In progress |
| `[x]` | Complete; tasks carry the commit SHA |
| `[!]` | Blocked; give the reason |

**`metadata.json`**:

```json
{
  "id": "user-auth_20250115",
  "title": "User Authentication",
  "type": "feature",
  "status": "in_progress",
  "created": "2025-01-15T10:00:00Z",
  "updated": "2025-01-16T14:30:00Z",
  "phases": { "total": 3, "completed": 1 },
  "tasks": { "total": 12, "completed": 5 }
}
```

`type` is `feature`, `bug`, `chore` or `refactor`. `status` is `pending`, `in_progress`,
`completed` or `archived`. `id` equals the directory name.

## References

`references/details.md` has the spec and plan templates, the spec and plan quality
checklists, dependency handling, and phase patterns for feature, bug and refactor tracks.
