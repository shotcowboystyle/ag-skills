# bazel-build-optimization — templates and worked examples

Versions below are from the Bazel Central Registry on 2026-10-27. Check
<https://registry.bazel.build> for the latest before copying.

## Templates

### Template 1: MODULE.bazel

```python
# MODULE.bazel
module(name = "myproject", version = "0.0.0")

bazel_dep(name = "platforms", version = "1.1.0")
bazel_dep(name = "bazel_skylib", version = "1.9.2")
bazel_dep(name = "aspect_rules_js", version = "3.5.2")
bazel_dep(name = "aspect_rules_ts", version = "3.10.1")
bazel_dep(name = "aspect_rules_jest", version = "0.26.0")
bazel_dep(name = "rules_nodejs", version = "6.7.7")
bazel_dep(name = "rules_python", version = "2.4.5")

# Node.js toolchain, version taken from .nvmrc
node = use_extension("@rules_nodejs//nodejs:extensions.bzl", "node")
node.toolchain(node_version_from_nvmrc = "//:.nvmrc")

# npm packages from the pnpm lockfile
npm = use_extension("@aspect_rules_js//npm:extensions.bzl", "npm")
npm.npm_translate_lock(
    name = "npm",
    pnpm_lock = "//:pnpm-lock.yaml",
    verify_node_modules_ignored = "//:.bazelignore",
)
use_repo(npm, "npm")

# TypeScript compiler, version kept in sync with package.json
typescript = use_extension("@aspect_rules_ts//ts:extensions.bzl", "typescript")
typescript.toolchain(version_from = "//:package.json")
use_repo(typescript, "npm_typescript")

# Python toolchain and pip packages
python = use_extension("@rules_python//python/extensions:python.bzl", "python")
python.toolchain(python_version = "3.12")

pip = use_extension("@rules_python//python/extensions:pip.bzl", "pip")
pip.parse(
    hub_name = "pip",
    python_version = "3.12",
    requirements_lock = "//:requirements_lock.txt",
)
use_repo(pip, "pip")
```

Run `bazel mod tidy` after editing to fix `use_repo` lists, and
`bazel mod graph` to see the resolved dependency graph.

### Template 2: .bazelrc

```bash
# .bazelrc

# Performance
build --jobs=auto
build --local_resources=cpu=HOST_CPUS*.75
build --local_resources=memory=HOST_RAM*.75

# Local caches
build --disk_cache=~/.cache/bazel-disk
build --repository_cache=~/.cache/bazel-repo

# Remote cache: everyone reads, only CI writes
build:remote-cache --remote_cache=grpcs://cache.example.com
build:remote-cache --remote_upload_local_results=false
build:remote-cache --remote_timeout=60

# Remote execution
build:remote-exec --config=remote-cache
build:remote-exec --remote_executor=grpcs://remote.example.com
build:remote-exec --remote_instance_name=projects/myproject/instances/default
build:remote-exec --extra_execution_platforms=//platforms:remote_linux
build:remote-exec --jobs=200

# CI
build:ci --config=remote-cache
build:ci --remote_upload_local_results=true
build:ci --build_metadata=ROLE=CI
build:ci --bes_backend=grpcs://bes.example.com
build:ci --bes_results_url=https://results.example.com/invocation/

# Tests
test --test_output=errors
test --test_summary=detailed

# Coverage
coverage --combined_report=lcov
coverage --instrumentation_filter="//..."

# Compilation modes
build:opt --compilation_mode=opt
build:dbg --compilation_mode=dbg

# Per-user overrides (gitignored); put credentials such as
# --remote_header=x-api-key=... here or in CI secrets, never in .bazelrc
try-import %workspace%/user.bazelrc
```

### Template 3: TypeScript Library BUILD

```python
# libs/utils/BUILD.bazel
load("@aspect_rules_jest//jest:defs.bzl", "jest_test")
load("@aspect_rules_js//js:defs.bzl", "js_library")
load("@aspect_rules_ts//ts:defs.bzl", "ts_project")
load("@npm//:defs.bzl", "npm_link_all_packages")

npm_link_all_packages(name = "node_modules")

ts_project(
    name = "utils_ts",
    srcs = glob(["src/**/*.ts"], exclude = ["src/**/*.test.ts"]),
    declaration = True,
    source_map = True,
    tsconfig = "//:tsconfig",
    deps = [":node_modules/@types/node"],
)

js_library(
    name = "utils",
    srcs = [":utils_ts"],
    visibility = ["//visibility:public"],
)

jest_test(
    name = "utils_test",
    config = "//:jest_config",
    data = [":utils"] + glob(["src/**/*.test.ts"]),
    node_modules = "//:node_modules",
)
```

`load()` statements must come before any other statement in a BUILD file.
`//:tsconfig` and `//:jest_config` are targets in the root BUILD file (for
example a `ts_config` and a `js_library` wrapping the config files).

### Template 4: Python Library BUILD

```python
# libs/ml/BUILD.bazel
load("@pip//:requirements.bzl", "requirement")
load("@rules_python//python:defs.bzl", "py_binary", "py_library", "py_test")

py_library(
    name = "ml",
    srcs = glob(["src/**/*.py"]),
    visibility = ["//visibility:public"],
    deps = [
        "//libs/utils:utils_py",
        requirement("numpy"),
        requirement("pandas"),
        requirement("scikit-learn"),
    ],
)

py_test(
    name = "ml_test",
    size = "medium",
    srcs = glob(["tests/**/*.py"]),
    deps = [
        ":ml",
        requirement("pytest"),
    ],
)

py_binary(
    name = "train",
    srcs = ["train.py"],
    data = ["//data:training_data"],
    deps = [":ml"],
)
```

### Template 5: Custom Rule

For container images, use `rules_oci` (`oci_image`, `oci_push`) instead of
writing a rule. The pattern below shows the shape of a custom rule that wraps
an in-repo tool.

```python
# tools/bazel/rules/bundle.bzl
def _bundle_impl(ctx):
    output = ctx.actions.declare_file(ctx.attr.name + ".tar")

    args = ctx.actions.args()
    args.add("--manifest", ctx.file.manifest)
    args.add("--output", output)
    args.add_all("--layer", ctx.files.layers)

    ctx.actions.run(
        inputs = [ctx.file.manifest] + ctx.files.layers,
        outputs = [output],
        executable = ctx.executable._builder,
        arguments = [args],
        mnemonic = "Bundle",
        progress_message = "Bundling %{label}",
    )

    return [DefaultInfo(files = depset([output]))]

bundle = rule(
    implementation = _bundle_impl,
    attrs = {
        "manifest": attr.label(allow_single_file = [".json"], mandatory = True),
        "layers": attr.label_list(allow_files = True),
        "_builder": attr.label(
            default = "//tools/bundle:builder",
            executable = True,
            cfg = "exec",
        ),
    },
)
```

### Template 6: Query and Dependency Analysis

```bash
# Dependencies of a target
bazel query "deps(//apps/web:web)"

# What depends on this library
bazel query "rdeps(//..., //libs/utils:utils)"

# All test targets
bazel query "kind('.*_test', //...)"

# Targets with a tag
bazel query "attr(tags, 'integration', //...)"

# Configured graph (respects select() and flags)
bazel cquery "deps(//apps/web:web)" --output=label_kind

# Dependency graph as an image
bazel query "deps(//apps/web:web)" --output=graph | dot -Tsvg > deps.svg

# Why a module is in the graph
bazel mod explain rules_python
```

To find targets affected by a change in CI, use a tool built for it, such as
`bazel-diff` or `target-determinator`, rather than mapping `git diff` output to
labels by hand.

### Template 7: Remote Execution Platforms

```python
# platforms/BUILD.bazel
platform(
    name = "linux_x86_64",
    constraint_values = [
        "@platforms//os:linux",
        "@platforms//cpu:x86_64",
    ],
)

platform(
    name = "remote_linux",
    parents = [":linux_x86_64"],
    exec_properties = {
        # Pin the worker image by digest so remote actions are reproducible
        "container-image": "docker://gcr.io/myproject/bazel-worker@sha256:...",
        "OSFamily": "Linux",
        "Pool": "default",
    },
)
```

Register toolchains that match this platform from their rule modules (for
example `rules_cc` or a hermetic toolchain module) rather than hand-writing
`toolchain()` targets.

## Performance Optimization

```bash
# Profile a build (Bazel writes a profile by default; this names it)
bazel build //... --profile=profile.json.gz
bazel analyze-profile profile.json.gz
# Or open the profile in chrome://tracing or https://ui.perfetto.dev

# Compact execution log, for comparing cache keys between two builds
bazel build //... --execution_log_compact_file=exec_log.binpb.zst

# Memory profile
bazel build //... --memory_profile=memory.profile

# Lower memory use on CI by discarding incremental state
bazel build //... --notrack_incremental_state
```

To debug remote cache misses, record the compact execution log on two machines
and compare them; the differing inputs or environment variables are the cause.
