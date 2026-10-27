---
name: changelog-automation
description: Draft changelogs and release notes from Conventional Commits with release-please or git-cliff, in Keep a Changelog format, for a person to edit before release. Use when setting up release workflows, generating release notes, or standardizing commit conventions.
last_verified: 2026-10-27
---

# Changelog Automation

Turn commit history into a draft changelog and release notes. A tool writes the draft; a
person edits it before anything is tagged or published. Commit messages are written for
reviewers, changelogs for users, so the draft always needs a human pass.

## When to Use This Skill

- Setting up changelog or release-note generation for a repository
- Adopting Conventional Commits and enforcing them in CI
- Replacing `standard-version`, which is deprecated and no longer maintained
- Writing the release notes for one release

## Procedure

1. **Read what exists.** Check for `CHANGELOG.md`, `cliff.toml`, `release-please-config.json`,
   `.versionrc*`, `commitlint.config.*`, and how tags are named (`git tag --sort=-v:refname |
   head`). Keep the existing tag format and changelog layout unless asked to change them.
2. **Enforce the commit format.** Add commitlint with `@commitlint/config-conventional`.
   Run it in CI on the PR title (squash merges) or on every PR commit (merge commits). A
   local hook alone is skipped by `--no-verify`.
3. **Pick one generator.**
   - **release-please** when the repo is on GitHub and you want a release PR that bumps
     the version and updates `CHANGELOG.md`. The PR is the draft: edit it, then merge.
   - **git-cliff** for any host, for a Keep a Changelog layout, or when you want full
     control of the template. It writes the draft to a file you edit and commit.
   - If the project uses `standard-version`, migrate to one of these. Map each
     `.versionrc` type/section pair to `changelog-sections` (release-please) or
     `commit_parsers` (git-cliff).
4. **Generate a draft, never a release.** Configure GitHub releases as drafts
   (`"draft": true` for release-please; `gh release create --draft` with git-cliff).
5. **Edit the draft.** Rewrite entries for users: say what changed for them, merge
   duplicate entries, drop internal noise, and add an upgrade note for each breaking change.
   Read the commits the generator skipped (non-conventional ones) for anything that matters.
6. **Ask before publishing.** Show the final changelog diff, the version and the tag.
   Confirm with the user before committing the changelog, creating the tag, pushing, or
   publishing a release.
7. **Stop when** the commit check runs in CI, one draft has been generated from real
   history, and a person has reviewed it. Report the tool chosen, the files added, the CI
   job names, the next version the tool computed, and anything the user must still do
   (for example, create a token or enable squash merges).

## Commit Types and Changelog Sections

Conventional Commits: `<type>[optional scope][!]: <description>`, then an optional body
and footers. `!` or a `BREAKING CHANGE:` footer marks a breaking change.

| Type       | Keep a Changelog section | Version bump (1.0.0 and later) |
| ---------- | ------------------------ | ------------------------------ |
| `feat`     | Added                    | minor                          |
| `fix`      | Fixed                    | patch                          |
| `perf`     | Changed                  | patch                          |
| `refactor` | Changed (or hidden)      | none                           |
| `revert`   | Removed / Fixed          | depends on reverted commit     |
| `docs`, `style`, `test`, `chore`, `ci`, `build` | hidden | none            |
| any type with `!` or `BREAKING CHANGE:` | add an upgrade note | major       |

Before 1.0.0, release-please bumps minor for breaking changes only if
`bump-minor-pre-major` is set. Check the computed version rather than assuming it.

Keep a Changelog adds `Deprecated` and `Security`, which no commit type maps to. Fill
those by hand while editing the draft.

## Keep a Changelog Shape

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.2.0] - 2026-01-15

### Added

- Profile avatars.

### Changed

- **Breaking:** `GET /users/:id` returns `userId` instead of `id`. Update API clients.

### Fixed

- Login no longer times out after 30 seconds of inactivity (#123).

[Unreleased]: https://github.com/OWNER/REPO/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/OWNER/REPO/compare/v1.1.0...v1.2.0
```

release-please writes its own heading style (`## [1.2.0](compare-link) (date)`), not this
exact layout. Use git-cliff when the Keep a Changelog layout itself is required.

## Rules

- Generated text is a draft. Never publish it unedited.
- One logical change per commit, so each changelog entry maps to one commit.
- Never tag, push, or publish a release without the user's confirmation.
- Pin CI actions to a commit SHA and give the release job only the permissions it needs.

## References

Read `references/details.md` when you need:

- commitlint and husky setup, and the CI job that lints PR titles or commits
- release-please workflow, config and manifest, and how to correct release notes
- git-cliff `cliff.toml`, local commands, and a CI job that makes a draft release
- migrating from `standard-version`
- commit message and release-notes examples
