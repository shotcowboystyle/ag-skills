# changelog-automation — setup and worked examples

Versions checked on 2026-10-27: commitlint 21.2, husky 9.1, release-please 17.11 with
release-please-action 5.0, git-cliff 2.14 with git-cliff-action 4.9. Actions are pinned to
commit SHAs; bump them with Dependabot or Renovate.

## Contents

- [Commit linting](#commit-linting): commitlint config, local hook, CI job
- [release-please](#release-please): workflow, config, manifest, correcting notes
- [git-cliff](#git-cliff): `cliff.toml`, local commands, draft release in CI
- [Migrating from standard-version](#migrating-from-standard-version)
- [Commit message examples](#commit-message-examples)
- [Editing the draft](#editing-the-draft): before and after, release notes template

## Commit linting

```bash
npm install -D @commitlint/cli @commitlint/config-conventional
```

```javascript
// commitlint.config.mjs
export default {
  extends: ["@commitlint/config-conventional"],
};
```

The conventional preset already limits types to `build`, `chore`, `ci`, `docs`, `feat`,
`fix`, `perf`, `refactor`, `revert`, `style` and `test`, and caps the header at 100
characters. Override a rule only when the team has agreed to it.

Optional local hook with husky 9. `husky init` adds a `prepare` script and a
`.husky/pre-commit` that runs `npm test`; edit or delete that file if you don't want it.

```bash
npm install -D husky
npx husky init
echo 'npx --no -- commitlint --edit "$1"' > .husky/commit-msg
```

The hook is a convenience. CI is the check that counts:

```yaml
# .github/workflows/commitlint.yml
name: Commit lint

on:
  pull_request:
    types: [opened, edited, synchronize, reopened]

permissions:
  contents: read

jobs:
  commitlint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
        with:
          fetch-depth: 0
      - uses: actions/setup-node@949feb2413d6458794dcd2491c4babbbce0c15c1 # v7.1.0
        with:
          node-version: 24
      - run: npm ci

      # Keep the step that matches how PRs are merged and delete the other.
      # Squash merge: the PR title becomes the commit message.
      - name: Lint PR title
        env:
          TITLE: ${{ github.event.pull_request.title }}
        run: printf '%s\n' "$TITLE" | npx commitlint --verbose

      # Merge commit or rebase: every PR commit lands on main.
      - name: Lint PR commits
        env:
          BASE: ${{ github.event.pull_request.base.sha }}
          HEAD: ${{ github.event.pull_request.head.sha }}
        run: npx commitlint --from "$BASE" --to "$HEAD" --verbose
```

The title goes through an environment variable, not straight into the script, so a
crafted PR title can't inject shell commands.

## release-please

release-please keeps a release PR open on the default branch. Each merge to main updates
the PR with the next version and changelog entries. Merging the PR tags the release and
creates the GitHub release, as a draft with the config below.

```yaml
# .github/workflows/release-please.yml
name: release-please

on:
  push:
    branches: [main]

permissions:
  contents: write
  issues: write
  pull-requests: write

jobs:
  release-please:
    runs-on: ubuntu-latest
    steps:
      - uses: googleapis/release-please-action@45996ed1f6d02564a971a2fa1b5860e934307cf7 # v5.0.0
        id: release
        with:
          config-file: release-please-config.json
          manifest-file: .release-please-manifest.json
```

`release-please-config.json`:

```json
{
  "$schema": "https://raw.githubusercontent.com/googleapis/release-please/main/schemas/config.json",
  "release-type": "node",
  "draft": true,
  "force-tag-creation": true,
  "changelog-sections": [
    { "type": "feat", "section": "Added" },
    { "type": "fix", "section": "Fixed" },
    { "type": "perf", "section": "Changed" },
    { "type": "refactor", "section": "Changed" },
    { "type": "revert", "section": "Removed" },
    { "type": "docs", "section": "Documentation", "hidden": true },
    { "type": "chore", "section": "Miscellaneous", "hidden": true }
  ],
  "packages": {
    ".": {}
  }
}
```

`.release-please-manifest.json`, holding the version currently released:

```json
{
  ".": "1.1.0"
}
```

Notes:

- `release-type` sets which files get bumped: `node` (package.json), `python`
  (pyproject.toml), `rust`, `go`, `simple` (a `version.txt`), and others.
- `draft: true` makes the GitHub release a draft. GitHub doesn't tag a draft until it is
  published, which makes release-please lose track of the previous release.
  `force-tag-creation: true` creates the tag at once to prevent that.
- An existing repo with a long history: set `bootstrap-sha` to the last released commit
  so the first release PR doesn't list every commit ever made.
- PRs opened with the default `GITHUB_TOKEN` don't trigger other workflows, so CI won't run
  on the release PR. Pass a fine-grained token or GitHub App token as `token:` if CI must
  run there.
- Force a version with a `Release-As: 2.0.0` line in a commit body.

**Correcting the notes.** release-please rewrites its PR branch whenever main changes,
so edits made directly in that branch can be lost. To fix one entry, edit the body of the
merged PR that produced it (squash merges only) and add:

```text
BEGIN_COMMIT_OVERRIDE
fix(auth): stop logging users out after 30 seconds of inactivity
END_COMMIT_OVERRIDE
```

The next run uses that text. For wording beyond single entries, edit `CHANGELOG.md` in the
release PR right before merging it, and edit the draft GitHub release before publishing.

## git-cliff

Install with `cargo install git-cliff`, `npx git-cliff`, `uvx git-cliff` or a package
manager. This config writes Keep a Changelog sections. The HTML comments in group names
control section order and are stripped from the output.

```toml
# cliff.toml
[changelog]
header = """
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
"""
body = """
{% if version -%}
## [{{ version | trim_start_matches(pat="v") }}] - {{ timestamp | date(format="%Y-%m-%d") }}
{% else -%}
## [Unreleased]
{% endif -%}
{% for group, commits in commits | group_by(attribute="group") %}
### {{ group | striptags | trim }}
{% for commit in commits %}
- {% if commit.scope %}**{{ commit.scope }}:** {% endif %}\
{% if commit.breaking %}**BREAKING:** {% endif %}\
{{ commit.message | upper_first }}\
{% endfor %}
{% endfor %}
"""
trim = false

[git]
conventional_commits = true
# Non-conventional commits stay out of the draft; the reviewer reads them by hand.
filter_unconventional = true
protect_breaking_commits = true
commit_parsers = [
  { body = "(?i)security", group = "<!-- 4 -->Security" },
  { message = "^feat", group = "<!-- 0 -->Added" },
  { message = "^fix", group = "<!-- 1 -->Fixed" },
  { message = "^perf", group = "<!-- 2 -->Changed" },
  { message = "^refactor", group = "<!-- 2 -->Changed" },
  { message = "^revert", group = "<!-- 3 -->Removed" },
  { message = "^chore\\(release\\)", skip = true },
  { message = "^(docs|style|test|chore|ci|build)", skip = true },
]
tag_pattern = "v[0-9].*"
sort_commits = "oldest"
```

Local release, with the person editing between steps:

```bash
# 1. Next version from commits since the last tag.
git cliff --bumped-version

# 2. Draft the new section only, with no header.
git cliff --unreleased --bump --strip header -o NEXT.md

# 3. List the commits git-cliff skipped as non-conventional, and read them.
git log --oneline "$(git describe --tags --abbrev=0)"..HEAD

# 4. Edit NEXT.md, paste it under the header of CHANGELOG.md, and delete NEXT.md.
# 5. Show the diff and the version, and get the user's confirmation before
#    committing CHANGELOG.md and creating the tag.
```

`git cliff -o CHANGELOG.md` regenerates the whole file from history and throws away hand
edits to earlier releases. Use it only to create the first changelog. `--prepend` keeps
old entries, but it also repeats the header, so remove the duplicate if you use it.

Draft GitHub release when a person pushes a tag:

```yaml
# .github/workflows/release-notes.yml
name: Release notes

on:
  push:
    tags: ["v*"]

permissions:
  contents: write

jobs:
  draft-release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
        with:
          fetch-depth: 0
      - uses: orhun/git-cliff-action@a9a95522b26fe6403f7bb24031f21fb573d0f5ff # v4.9.1
        id: git-cliff
        with:
          config: cliff.toml
          args: --latest --strip header
        env:
          OUTPUT: RELEASE_NOTES.md
      # A draft is visible only to maintainers until someone edits and publishes it.
      - name: Create draft release
        env:
          GH_TOKEN: ${{ github.token }}
        run: gh release create "$GITHUB_REF_NAME" --draft --notes-file RELEASE_NOTES.md
```

## Migrating from standard-version

`standard-version` is deprecated. Its README recommends release-please; outside GitHub
Actions, use git-cliff, or the `commit-and-tag-version` fork if you must keep the same
CLI.

1. Note the current version and the latest tag. For release-please, write that version
   to `.release-please-manifest.json`. git-cliff reads tags directly.
2. Translate each `.versionrc` entry. `{ type: "feat", section: "Features" }` becomes
   `{ "type": "feat", "section": "Features" }` in `changelog-sections`, or a
   `{ message = "^feat", group = "Features" }` commit parser. Entries with
   `hidden: true` become `"hidden": true` or `skip = true`.
3. Keep the existing `CHANGELOG.md`. Both tools add new releases above old ones.
4. Remove `standard-version`, `.versionrc*` and its `release` scripts from
   `package.json` in the same PR.
5. Do a dry run before the first real release: let release-please open its PR, or run
   `git cliff --unreleased --bump`, and compare the result with the commits.

## Commit message examples

```text
feat(auth): add Google sign-in

fix(checkout): retry payment capture once on a network timeout

Closes #123

feat(api)!: return userId instead of id from GET /users/:id

BREAKING CHANGE: API clients must read `userId`. `id` is no longer returned.

fix(db): retry dropped connections with exponential backoff

Timeouts used to fail the whole request. Retries now back off up to three
times before failing, and the timeout is 10 s instead of 5 s.

Fixes #456
```

## Editing the draft

Generated entries repeat commit subjects. Rewrite them for the people reading the
changelog.

| Generated | Edited |
| --- | --- |
| `**api:** **BREAKING:** Return userId instead of id` | **Breaking:** `GET /users/:id` returns `userId` instead of `id`. Update API clients before upgrading. |
| `**deps:** Bump lib` | Updated `lib` to 4.17.21, which fixes CVE-XXXX-NNNN (moved to Security). |
| `**checkout:** Retry payment capture once on a network timeout` | Payments no longer fail on a brief network drop. |
| `Fix typo` in Fixed | Deleted: not user-visible. |

GitHub release body, filled in by hand from the edited changelog:

```markdown
## Highlights

- One or two sentences on what this release means for users.

## Breaking changes

- What changed, who is affected, and the exact upgrade step.

## Added / Changed / Fixed / Security

- Copied from the edited CHANGELOG.md section.

## Upgrade notes

- Migrations, config changes or flags, in order. Write "None" if there are none.

**Full changelog:** https://github.com/OWNER/REPO/compare/vPREVIOUS...vCURRENT
```
