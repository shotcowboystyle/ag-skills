# shellcheck-configuration — detailed patterns and worked examples

## Installation

```bash
brew install shellcheck            # macOS
sudo apt-get install -y shellcheck # Debian/Ubuntu
sudo dnf install ShellCheck        # Fedora
pipx install shellcheck-py         # any platform with Python; bundles the binary

shellcheck --version
```

Distribution packages can lag several releases behind. Newer checks need a newer binary;
the release binaries on GitHub are static and run anywhere.

## How Codes Are Numbered

- **SC1xxx**: parser errors and syntax problems (unbalanced quotes, unrecognized shebang,
  sourced file not found).
- **SC2xxx**: the main body of checks: quoting, exit-status handling, likely bugs.
- **SC3xxx**: features undefined in the shell named by the shebang or `shell=`, mostly
  Bash or ksh syntax in a POSIX `sh` script.

Codes within each range are not grouped by topic. Look each one up on
`https://www.shellcheck.net/wiki/SCxxxx`.

## Configuration Examples

### Strict profile for new code

```ini
# .shellcheckrc
enable=all
external-sources=true
source-path=SCRIPTDIR

# require-variable-braces: ${var} everywhere is noise for this codebase.
disable=SC2250
```

Check which optional checks exist in your installed version with `shellcheck --list-optional`.

### One-off runs without a config file

```bash
# POSIX target, follow sources
shellcheck --shell=sh --external-sources script.sh

# Bash, every optional check, two codes excluded
shellcheck --shell=bash --enable=all --exclude=SC1091,SC2250 script.sh

# Ignore any .shellcheckrc
shellcheck --norc script.sh
```

### Environment variable

`SHELLCHECK_OPTS` is the only environment variable ShellCheck reads for options. Its value
is prepended to the command-line flags:

```bash
export SHELLCHECK_OPTS='--severity=warning --external-sources'
```

## Integration Patterns

### Git pre-commit hook without the pre-commit framework

```bash
#!/usr/bin/env bash
# .git/hooks/pre-commit
set -euo pipefail

mapfile -d '' files < <(git diff --cached --name-only -z --diff-filter=ACMR -- '*.sh')
(( ${#files[@]} == 0 )) && exit 0
shellcheck -x -- "${files[@]}"
```

### GitHub Actions workflow

```yaml
name: ShellCheck

on: [push, pull_request]

permissions:
  contents: read

jobs:
  shellcheck:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - name: Run ShellCheck
        run: git ls-files -z '*.sh' | xargs -0 --no-run-if-empty shellcheck -x
```

### GitLab CI

```yaml
shellcheck:
  stage: lint
  image: koalaman/shellcheck-alpine:stable
  script:
    - find . -type f -name '*.sh' -exec shellcheck -x {} +
```

`-exec … {} +` passes many files to one ShellCheck run and returns its exit status.
`-exec … {} \;` does not: `find` exits 0 even when every file fails.

## Handling Violations

### Suppressing with a reason

```bash
#!/usr/bin/env bash
# A directive right after the shebang applies to the whole file.
# shellcheck disable=SC2154 # set by the CI environment

# A directive on its own line applies to the next command only.
# shellcheck disable=SC2086 # $FLAGS is a deliberately split list of options
gcc $FLAGS -o app main.c

# Tell ShellCheck where a dynamically built path points.
# shellcheck source=lib/common.sh
. "$LIB_DIR/common.sh"
```

Prefer fixing over suppressing. Suppress when the code is right and ShellCheck cannot know
it, and say why in the same comment.

### Common fixes

```bash
# SC2086 / SC2046: quote expansions
cp $src $dest          # bad
cp -- "$src" "$dest"   # good

# SC2206: split a string into an array on purpose
arr=( $line )                    # bad: also globs
read -ra arr <<<"$line"          # good

# SC2155: keep the exit status
local out=$(build)               # bad: failure of build is ignored
local out; out=$(build)          # good

# SC2181: test the command, not $?
some_command
if [ $? -eq 0 ]; then echo ok; fi   # bad
if some_command; then echo ok; fi   # good

# SC2015: A && B || C is not if/else; C runs when B fails
[ -f "$f" ] && process "$f" || echo "missing"           # bad
if [ -f "$f" ]; then process "$f"; else echo "missing"; fi  # good

# SC2009: use pgrep
ps aux | grep -v grep | grep myprocess   # bad
pgrep -f myprocess                       # good
```

## Checking Many Files

```bash
# One process per batch of files; non-zero if any file has findings
git ls-files -z '*.sh' | xargs -0 shellcheck -x

# Parallel: four ShellCheck processes
git ls-files -z '*.sh' | xargs -0 -P 4 -n 20 shellcheck -x
```

Whether parallel runs are faster for a given repository needs measurement.

## Output Formats

```bash
shellcheck script.sh                  # tty: annotated source, the default
shellcheck -f gcc script.sh           # script.sh:3:6: warning: ... [SC2154]
shellcheck -f checkstyle script.sh    # XML for Jenkins and similar
shellcheck -f json1 script.sh         # {"comments": [{"file", "line", "column", "level", "code", "message", "fix"}]}
shellcheck -f diff script.sh          # unified diff of automatic fixes
shellcheck -f quiet script.sh         # no output; exit status only
```

Prefer `json1` over the older `json` format; `json1` wraps the list in a `comments` object.
