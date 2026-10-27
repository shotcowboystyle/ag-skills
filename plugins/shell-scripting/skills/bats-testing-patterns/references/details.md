# bats-testing-patterns — detailed patterns and worked examples

Basics (install, layout, `run`, temp dirs, skips) are in `SKILL.md`.

## Assertion Patterns

### Exit Code Assertions

```bash
#!/usr/bin/env bats

@test "Command succeeds" {
    run true
    [ "$status" -eq 0 ]
}

@test "Command fails as expected" {
    run false
    [ "$status" -ne 0 ]
}

@test "Command returns specific exit code" {
    run my_function --invalid
    [ "$status" -eq 127 ]
}

@test "Can capture command result" {
    run echo "hello"
    [ $status -eq 0 ]
    [ "$output" = "hello" ]
}
```

### Output Assertions

```bash
#!/usr/bin/env bats

@test "Output matches string" {
    result=$(echo "hello world")
    [ "$result" = "hello world" ]
}

@test "Output contains substring" {
    result=$(echo "hello world")
    [[ "$result" == *"world"* ]]
}

@test "Output matches pattern" {
    result=$(date +%Y)
    [[ "$result" =~ ^[0-9]{4}$ ]]
}

@test "Multi-line output" {
    run printf "line1\nline2\nline3"
    [ "$output" = "line1
line2
line3" ]
}

@test "Lines variable contains output" {
    run printf "line1\nline2\nline3"
    [ "${lines[0]}" = "line1" ]
    [ "${lines[1]}" = "line2" ]
    [ "${lines[2]}" = "line3" ]
}
```

### File Assertions

```bash
#!/usr/bin/env bats

@test "File is created" {
    [ ! -f "$BATS_TEST_TMPDIR/output.txt" ]
    my_function > "$BATS_TEST_TMPDIR/output.txt"
    [ -f "$BATS_TEST_TMPDIR/output.txt" ]
}

@test "File contents match expected" {
    my_function > "$BATS_TEST_TMPDIR/output.txt"
    [ "$(cat "$BATS_TEST_TMPDIR/output.txt")" = "expected content" ]
}

@test "File is readable" {
    touch "$BATS_TEST_TMPDIR/test.txt"
    [ -r "$BATS_TEST_TMPDIR/test.txt" ]
}

@test "File has correct permissions" {
    touch "$BATS_TEST_TMPDIR/test.txt"
    chmod 644 "$BATS_TEST_TMPDIR/test.txt"
    # stat -f is BSD/macOS; GNU stat uses -c '%a'
    [ "$(stat -f %OLp "$BATS_TEST_TMPDIR/test.txt" 2>/dev/null || stat -c %a "$BATS_TEST_TMPDIR/test.txt")" = "644" ]
}

@test "File size is correct" {
    printf '12345' > "$BATS_TEST_TMPDIR/test.txt"
    [ "$(wc -c < "$BATS_TEST_TMPDIR/test.txt")" -eq 5 ]
}
```

## Setup and Teardown Patterns

### Basic Setup and Teardown

```bash
#!/usr/bin/env bats

setup() {
    # Source script under test
    source "${BATS_TEST_DIRNAME}/../bin/script.sh"
}

teardown() {
    # Runs even when the test fails: stop anything the test started
    if [[ -n ${SERVER_PID:-} ]]; then kill "$SERVER_PID" 2>/dev/null || true; fi
}

@test "Test using the per-test temp dir" {
    touch "$BATS_TEST_TMPDIR/file.txt"
    [ -f "$BATS_TEST_TMPDIR/file.txt" ]
}
```

### Setup with Resources

```bash
#!/usr/bin/env bats

setup() {
    # Create directory structure in the per-test temp dir (bats removes it)
    mkdir -p "$BATS_TEST_TMPDIR/data/input"
    mkdir -p "$BATS_TEST_TMPDIR/data/output"

    # Create test fixtures
    echo "line1" > "$BATS_TEST_TMPDIR/data/input/file1.txt"
    echo "line2" > "$BATS_TEST_TMPDIR/data/input/file2.txt"

    # Initialize environment
    export DATA_DIR="$BATS_TEST_TMPDIR/data"
    export INPUT_DIR="$DATA_DIR/input"
    export OUTPUT_DIR="$DATA_DIR/output"
}

@test "Processes input files" {
    run my_process_script "$INPUT_DIR" "$OUTPUT_DIR"
    [ "$status" -eq 0 ]
    [ -f "$OUTPUT_DIR/file1.txt" ]
}
```

### Global Setup/Teardown

```bash
#!/usr/bin/env bats

# Load shared setup from test_helper.sh
load test_helper

# setup_file runs once before all tests
setup_file() {
    # $BATS_FILE_TMPDIR is shared by every test in this file; export to reach tests
    export SHARED_RESOURCE="$BATS_FILE_TMPDIR/shared"
    mkdir -p "$SHARED_RESOURCE"
    echo "Expensive setup" > "$SHARED_RESOURCE/data.txt"
}

@test "First test uses shared resource" {
    [ -f "$SHARED_RESOURCE/data.txt" ]
}

@test "Second test uses shared resource" {
    [ -d "$SHARED_RESOURCE" ]
}
```

## Mocking and Stubbing Patterns

### Function Mocking

```bash
#!/usr/bin/env bats

# Mock external command
my_external_tool() {
    echo "mocked output"
    return 0
}

@test "Function uses mocked tool" {
    export -f my_external_tool
    run my_function
    [[ "$output" == *"mocked output"* ]]
}
```

### Command Stubbing

```bash
#!/usr/bin/env bats

setup() {
    # Create stub directory
    STUBS_DIR="$BATS_TEST_TMPDIR/stubs"
    mkdir -p "$STUBS_DIR"

    # Add to PATH
    export PATH="$STUBS_DIR:$PATH"
}

create_stub() {
    local cmd="$1"
    local output="$2"
    local code="${3:-0}"

    cat > "$STUBS_DIR/$cmd" <<EOF
#!/bin/bash
echo "$output"
exit $code
EOF
    chmod +x "$STUBS_DIR/$cmd"
}

@test "Function works with stubbed curl" {
    create_stub curl "{ \"status\": \"ok\" }" 0
    run my_api_function
    [ "$status" -eq 0 ]
}
```

### Variable Stubbing

```bash
#!/usr/bin/env bats

@test "Function handles environment override" {
    export MY_SETTING="override_value"
    run my_function
    [ "$status" -eq 0 ]
    [[ "$output" == *"override_value"* ]]
}

@test "Function uses default when var unset" {
    unset MY_SETTING
    run my_function
    [ "$status" -eq 0 ]
    [[ "$output" == *"default"* ]]
}
```

## Fixture Management

### Using Fixture Files

```bash
#!/usr/bin/env bats

# Fixture directory: tests/fixtures/

setup() {
    FIXTURES_DIR="${BATS_TEST_DIRNAME}/fixtures"
    WORK_DIR="$BATS_TEST_TMPDIR"
}

@test "Process fixture file" {
    # Copy fixture to work directory
    cp "$FIXTURES_DIR/input.txt" "$WORK_DIR/input.txt"

    # Run function
    run my_process_function "$WORK_DIR/input.txt"

    # Compare output
    diff "$WORK_DIR/output.txt" "$FIXTURES_DIR/expected_output.txt"
}
```

### Dynamic Fixture Generation

```bash
#!/usr/bin/env bats

generate_fixture() {
    local lines="$1"
    local file="$2"

    local i
    for (( i = 1; i <= lines; i++ )); do
        printf 'Line %d content\n' "$i"
    done > "$file"
}

@test "Handle large input file" {
    generate_fixture 1000 "$BATS_TEST_TMPDIR/large.txt"
    run my_function "$BATS_TEST_TMPDIR/large.txt"
    [ "$status" -eq 0 ]
    [ "$(wc -l < "$BATS_TEST_TMPDIR/large.txt")" -eq 1000 ]
}
```


## Testing Error Conditions

```bash
#!/usr/bin/env bats

bats_require_minimum_version 1.5.0

setup() {
    load 'test_helper/bats-support/load'
    load 'test_helper/bats-assert/load'
}

@test "fails with a missing file" {
    run my_function "/nonexistent/file.txt"
    assert_failure
    assert_output --partial "not found"
}

@test "fails with empty input" {
    run ! my_function ""
}

@test "fails when the file is unreadable" {
    # root reads files regardless of mode bits
    [ "$(id -u)" -ne 0 ] || skip "running as root"
    touch "$BATS_TEST_TMPDIR/locked.txt"
    chmod 000 "$BATS_TEST_TMPDIR/locked.txt"
    run my_function "$BATS_TEST_TMPDIR/locked.txt"
    assert_failure
}

@test "prints usage for an unknown option" {
    run -2 my_function --invalid-option
    assert_output --partial "Usage:"
}
```

No cleanup is needed: bats deletes `$BATS_TEST_TMPDIR` after each test.

## Testing Under Several Shells

```bash
#!/usr/bin/env bats

SCRIPT="${BATS_TEST_DIRNAME}/../bin/script.sh"

@test "runs under bash" {
    run bash "$SCRIPT" arg1
    [ "$status" -eq 0 ]
}

@test "runs under dash" {
    command -v dash >/dev/null || skip "dash not installed"
    run dash "$SCRIPT" arg1
    [ "$status" -eq 0 ]
}

@test "runs under busybox sh" {
    command -v busybox >/dev/null || skip "busybox not installed"
    run busybox sh "$SCRIPT" arg1
    [ "$status" -eq 0 ]
}
```

Bats itself always runs in Bash; these tests run the script under test in another shell.

## CI

### GitHub Actions

```yaml
name: Tests

on: [push, pull_request]

permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
        with:
          submodules: true
      - name: Run Bats
        run: test/bats/bin/bats --formatter tap -r test/
```

With bats vendored as submodules (see `SKILL.md`), nothing else needs installing.

### Makefile

```makefile
BATS := test/bats/bin/bats

.PHONY: test test-tap
test:
	$(BATS) -r test/

test-tap:
	$(BATS) --formatter tap -r test/
```
