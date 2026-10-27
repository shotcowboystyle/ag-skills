---
name: bash-defensive-patterns
description: Script skeleton and defensive patterns for production Bash - strict mode, version checks, getopts parsing, temp-file cleanup, error traps and the set -e traps that silently skip errors. Use when writing or hardening a Bash script, CI step or system utility that must fail loudly and clean up after itself.
last_verified: 2026-10-27
---

# Bash Defensive Patterns

A script skeleton to start from, and the rules that keep `set -e` from lying to you.

## When to Use This Skill

- Starting a new Bash script or CLI tool
- Hardening a script that fails silently, leaves temp files behind, or breaks on spaces in
  file names
- Reviewing a CI step or deploy script before it runs in production

## Script Skeleton

Copy this, then replace the body of `main`. It runs clean under `shellcheck`, refuses to
start on Bash older than 4.4, supports `-n` (dry run) and `-v`, and removes its temp
directory on any exit.

```bash
#!/usr/bin/env bash
# archive-dir: write SRC as a dated .tar.gz into DEST.
# Requires: bash >= 4.4, tar. Exit codes: 0 ok, 1 error, 2 usage.
set -Eeuo pipefail

bash_at_least() { (( BASH_VERSINFO[0] > $1 || (BASH_VERSINFO[0] == $1 && BASH_VERSINFO[1] >= $2) )); }
bash_at_least 4 4 || { printf 'error: needs bash >= 4.4, found %s\n' "$BASH_VERSION" >&2; exit 1; }
shopt -s inherit_errexit

SCRIPT_NAME=${0##*/}
readonly SCRIPT_NAME
dry_run=0
verbose=0
tmpdir=''

usage() {
  cat <<EOF
Usage: $SCRIPT_NAME [-n] [-v] SRC DEST
Write SRC as a dated .tar.gz archive into DEST.

  -n  dry run: print commands instead of running them
  -v  verbose
  -h  show this help
EOF
}

die() { printf '%s: error: %s\n' "$SCRIPT_NAME" "$*" >&2; exit 1; }

log() {
  if (( verbose )); then printf '%s: %s\n' "$SCRIPT_NAME" "$*" >&2; fi
}

run() {
  if (( dry_run )); then
    printf 'would run:'
    printf ' %q' "$@"
    printf '\n'
  else
    "$@"
  fi
}

cleanup() {
  if [[ -n $tmpdir ]]; then rm -rf -- "$tmpdir"; fi
}

on_error() {
  printf '%s: line %s: exit %s: %s\n' "$SCRIPT_NAME" "$1" "$2" "$3" >&2
}

main() {
  local opt
  while getopts ':nvh' opt; do
    case $opt in
      n) dry_run=1 ;;
      v) verbose=1 ;;
      h) usage; exit 0 ;;
      *) usage >&2; exit 2 ;;
    esac
  done
  shift $((OPTIND - 1))
  (( $# == 2 )) || { usage >&2; exit 2; }

  local -r src=$1 dest=$2
  [[ -d $src ]] || die "not a directory: $src"
  [[ -d $dest && -w $dest ]] || die "not a writable directory: $dest"
  command -v tar >/dev/null || die "tar not found"

  trap cleanup EXIT
  trap 'on_error "$LINENO" "$?" "$BASH_COMMAND"' ERR
  tmpdir=$(mktemp -d)

  local archive
  archive="$dest/$(basename -- "$src")-$(date +%Y%m%d).tar.gz"
  log "writing $archive"
  run tar -czf "$tmpdir/out.tar.gz" -C "$src" .
  run mv -- "$tmpdir/out.tar.gz" "$archive"
}

main "$@"
```

What each part is for:

- **`bash_at_least`** compares the minor version only when the major is equal. Testing
  major `>= 4` and minor `>= 4` separately rejects Bash 5.0–5.3. Run it
  before `shopt -s inherit_errexit`, which older Bash rejects.
- **`set -Eeuo pipefail`**: `-e` exits on an unchecked failure, `-u` on an unset variable,
  `-o pipefail` makes a pipeline fail if any stage fails, `-E` lets functions inherit the
  `ERR` trap. `inherit_errexit` keeps `-e` active inside `$( … )`.
- **`main "$@"` at the bottom**: the whole file is parsed before anything runs, so a
  half-downloaded script does nothing.
- **Exit codes**: 0 success, 1 runtime error (`die`), 2 usage error.
- **`run`** prints the exact command, shell-quoted with `%q`, in dry-run mode.

## Where `set -e` Does Not Stop the Script

`set -e` is ignored in some places and fires unexpectedly in others. Check each of these:

| Pattern | What happens | Fix |
|---|---|---|
| `if f; then`, `f && x`, `f \|\| x`, `! f` | `set -e` is off for everything `f` runs, including inside `f` | check each command in `f` explicitly, or call `f` on its own line |
| `local x=$(cmd)`, `export x=$(cmd)` | the exit status is `local`'s, so a failing `cmd` is ignored | `local x; x=$(cmd)` |
| `(( i++ ))` when `i` is 0 | the expression is 0, status is 1, the script exits | `i=$((i + 1))` |
| `[[ $v ]] && echo x` as a function's last line | the function returns 1 when `$v` is empty, and the caller exits | use `if … fi` |
| `cmd \| head -1` under `pipefail` | `cmd` can die of SIGPIPE (status 141) and fail the pipeline | read the full output, or accept 141 explicitly |
| `cmd1 $(cmd2)` | the failure of `cmd2` is ignored | assign `cmd2`'s output to a variable first |

## Rules

1. **Quote every expansion**: `"$var"`, `"${arr[@]}"`, `"$(cmd)"`. Unquoted, a file name
   with a space becomes two arguments and `*` expands to the directory listing.
2. **Put `--` before user-supplied paths**: `rm -rf -- "$dir"`, `mv -- "$a" "$b"`.
3. **Guard destructive paths**: `rm -rf -- "${dir:?}/"*` stops if `dir` is empty instead
   of deleting `/*`.
4. **Iterate files NUL-safely**: `find … -print0 | xargs -0 …` or
   `while IFS= read -r -d '' f; do …; done < <(find … -print0)`. Never `for f in $(ls)`.
5. **Build commands as arrays**, never as strings for `eval`:
   `args=(--verbose); [[ $dry ]] && args+=(--dry-run); tool "${args[@]}"`.
6. **Require environment variables up front**: `: "${API_URL:?API_URL must be set}"`.
7. **Check for commands with `command -v`**, not `which`.
8. **Use `printf`**, not `echo`, for any data that might start with `-` or contain `\`.
9. **Write files atomically**: write to a temp file in the target's directory, then `mv`.
10. **Lint and test**: `shellcheck -x` (see `shellcheck-configuration`) and Bats tests (see
    `bats-testing-patterns`).

## More Patterns

`references/details.md` has worked examples for long-option parsing, logging, signal
handling for background jobs, atomic writes, idempotent setup, dry-run wrappers and
dependency checks.
