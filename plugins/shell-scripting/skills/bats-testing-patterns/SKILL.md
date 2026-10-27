---
name: bats-testing-patterns
description: Test shell scripts with bats-core - installation, file layout, run/status/output, bats-assert helpers, per-test temp directories, skips, setup_file and CI. Use when writing or fixing tests for a Bash or sh script, adding shell tests to CI, or doing test-first development of a shell utility.
last_verified: 2026-10-27
---

# Bats Testing Patterns

[bats-core](https://github.com/bats-core/bats-core) runs `@test` blocks written in Bash and
reports results in TAP. Each test runs in its own subshell; a test fails when any command in
it fails.

## When to Use This Skill

- Writing tests for a shell script or function library
- Adding shell tests to CI
- Reproducing a shell bug with a failing test before fixing it

## Install

Vendor bats and its helper libraries as git submodules, so every machine and CI runner uses
the same versions:

```bash
git submodule add https://github.com/bats-core/bats-core.git test/bats
git submodule add https://github.com/bats-core/bats-support.git test/test_helper/bats-support
git submodule add https://github.com/bats-core/bats-assert.git test/test_helper/bats-assert
```

Or install system-wide: `brew install bats-core` or `npm install -g bats`. Either way, the
helper libraries are separate.

## Layout

```
project/
├── src/
│   └── greet.sh
└── test/
    ├── bats/                     # submodule
    ├── test_helper/
    │   ├── bats-support/         # submodule
    │   ├── bats-assert/          # submodule
    │   └── common-setup.bash
    └── greet.bats
```

## A Complete Test File

`src/greet.sh` under test:

```bash
#!/usr/bin/env bash
greet() {
  [[ $# -eq 1 && -n $1 ]] || { printf 'usage: greet NAME\n' >&2; return 2; }
  printf 'Hello, %s!\n' "$1"
}
if [[ ${BASH_SOURCE[0]} == "$0" ]]; then greet "$@"; fi
```

The last line runs `greet` only when the file is executed, not when a test sources it.
Make it executable (`chmod +x src/greet.sh`) for the "works as an executable" test.

`test/test_helper/common-setup.bash`:

```bash
_common_setup() {
  load 'test_helper/bats-support/load'
  load 'test_helper/bats-assert/load'
  PROJECT_ROOT="$(cd "$BATS_TEST_DIRNAME/.." && pwd)"
  PATH="$PROJECT_ROOT/src:$PATH"
}
```

`test/greet.bats`:

```bash
#!/usr/bin/env bats

bats_require_minimum_version 1.5.0

setup() {
  load 'test_helper/common-setup'
  _common_setup
  source "$PROJECT_ROOT/src/greet.sh"
}

@test "greets by name" {
  run greet "Ada"
  assert_success
  assert_output "Hello, Ada!"
}

@test "rejects a missing name with exit code 2" {
  run -2 --separate-stderr greet
  assert_output ""
  [[ $stderr == *"usage: greet NAME"* ]]
}

@test "works as an executable" {
  run greet.sh "Grace"
  assert_success
  assert_line --index 0 "Hello, Grace!"
}

@test "writes a file in the per-test temp dir" {
  greet "Linus" >"$BATS_TEST_TMPDIR/out.txt"
  run cat "$BATS_TEST_TMPDIR/out.txt"
  assert_output --partial "Linus"
}

@test "formats JSON when jq is installed" {
  command -v jq >/dev/null || skip "jq not installed"
  run jq -n --arg n "$(greet Ada)" '$n'
  assert_success
}
```

Run it with `test/bats/bin/bats test/` (or `bats test/` with a system install).

## Core Rules

- **`run` captures, it never fails the test.** After `run cmd`, check `$status`, `$output`
  and `${lines[@]}` yourself, or with `assert_success`, `assert_failure`, `assert_output`,
  `assert_line` and `refute_output` from bats-assert.
- **`run -N cmd`** asserts the exit code is `N`; `run ! cmd` asserts it is non-zero. Both
  need `bats_require_minimum_version 1.5.0` at the top of the file.
- **`--separate-stderr`** puts stderr in `$stderr` instead of mixing it into `$output`.
- **Commands outside `run`** fail the test on a non-zero exit, so plain `[ … ]` and `[[ … ]]`
  lines are assertions. On Bash older than 4.1 a failing `[[ … ]]` or `(( … ))` in the
  middle of a test does not fail it; use `[ … ]` or the `assert_*` helpers when that matters.
- **Temp files go in `$BATS_TEST_TMPDIR`**, a fresh directory per test that bats deletes
  afterwards. `$BATS_FILE_TMPDIR` is shared by the tests in one file. Do not reassign
  `TMPDIR`: the code under test and `mktemp` read it.
- **Skip with `skip "reason"`**, inside a test or `setup`. Bats has no conditional-skip helper; write the
  condition yourself: `command -v jq >/dev/null || skip "jq not installed"`.
- **`setup`/`teardown` run around every test; `setup_file`/`teardown_file` once per file.**
  Variables from `setup_file` reach tests only if exported.
- **Pipes need a wrapper**: `run bash -c "producer | consumer"`, or `run` a function that
  contains the pipe. `run producer | consumer` pipes `run`'s own (empty) output.

## Running

```bash
bats test/                         # every .bats file in the directory
bats -r test/                      # recurse into subdirectories
bats --filter 'rejects' test/      # tests whose name matches a regex
bats --formatter tap test/         # TAP for CI tools
bats --jobs 4 test/                # parallel; needs GNU parallel installed
bats --print-output-on-failure test/
```

## More Patterns

`references/details.md` covers output and file assertions, fixtures, command stubs on
`PATH`, testing error paths and multiple shells, and CI workflows.
