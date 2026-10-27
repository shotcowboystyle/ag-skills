# Replay Testing for Determinism and Compatibility

Comprehensive guide for validating workflow determinism and ensuring safe code changes using replay testing.

## What is Replay Testing?

**Purpose**: Verify that workflow code changes are backward-compatible with existing workflow executions

**How it works**:

1. Temporal records every workflow decision as Event History
2. Replay testing re-executes workflow code against recorded history
3. If new code makes same decisions → deterministic (safe to deploy)
4. If decisions differ → non-deterministic (breaking change)

**Critical Use Cases**:

- Deploying workflow code changes to production
- Validating refactoring doesn't break running workflows
- CI/CD automated compatibility checks
- Version migration validation

## Basic Replay Testing

### Replayer Setup

```python
from temporalio.worker import Replayer
from temporalio.client import Client

async def test_workflow_replay():
    """Test workflow against production history"""

    # Connect to Temporal server
    client = await Client.connect("localhost:7233")

    # Create replayer with current workflow code
    replayer = Replayer(
        workflows=[OrderWorkflow, PaymentWorkflow]
    )

    # Fetch workflow history from production
    handle = client.get_workflow_handle("order-123")
    history = await handle.fetch_history()

    # Replay history with current code
    await replayer.replay_workflow(history)
    # Success = deterministic, Exception = breaking change
```

### Testing Against Multiple Histories

```python
import pytest
from temporalio.client import Client
from temporalio.worker import Replayer

@pytest.mark.asyncio
async def test_replay_multiple_workflows():
    """Replay against multiple production histories"""

    client = await Client.connect("localhost:7233")
    replayer = Replayer(workflows=[OrderWorkflow])

    # Test against different workflow executions
    workflow_ids = [
        "order-success-123",
        "order-cancelled-456",
        "order-retry-789",
    ]

    for workflow_id in workflow_ids:
        handle = client.get_workflow_handle(workflow_id)
        history = await handle.fetch_history()

        # Replay should succeed for all variants
        await replayer.replay_workflow(history)
```

## Determinism Validation

### Common Non-Deterministic Patterns

**Problem: Random Number Generation**

```python
# ❌ Non-deterministic (breaks replay)
@workflow.defn
class BadWorkflow:
    @workflow.run
    async def run(self) -> int:
        return random.randint(1, 100)  # Different on replay!

# ✅ Deterministic (safe for replay)
@workflow.defn
class GoodWorkflow:
    @workflow.run
    async def run(self) -> int:
        return workflow.random().randint(1, 100)  # Deterministic random
```

**Problem: Current Time**

```python
# ❌ Non-deterministic
@workflow.defn
class BadWorkflow:
    @workflow.run
    async def run(self) -> str:
        now = datetime.now()  # Different on replay!
        return now.isoformat()

# ✅ Deterministic
@workflow.defn
class GoodWorkflow:
    @workflow.run
    async def run(self) -> str:
        now = workflow.now()  # Deterministic time
        return now.isoformat()
```

**Problem: Direct External Calls**

```python
# ❌ Non-deterministic
@workflow.defn
class BadWorkflow:
    @workflow.run
    async def run(self) -> dict:
        response = requests.get("https://api.example.com/data")  # External call!
        return response.json()

# ✅ Deterministic
@workflow.defn
class GoodWorkflow:
    @workflow.run
    async def run(self) -> dict:
        # Use activity for external calls
        return await workflow.execute_activity(
            fetch_external_data,
            start_to_close_timeout=timedelta(seconds=30),
        )
```

### Testing Determinism

Running a workflow twice and comparing outputs proves nothing: `workflow.random()`
is seeded per execution. Replay the recorded history instead, which is exactly
what a worker does after a restart.

```python
from temporalio.worker import Replayer

# Module level: the SDK rejects @workflow.defn classes defined inside a function
@workflow.defn
class DeterministicWorkflow:
    @workflow.run
    async def run(self, count: int) -> list[int]:
        # Use workflow.random() for determinism
        return [workflow.random().randint(1, 100) for _ in range(count)]

@pytest.mark.asyncio
async def test_workflow_determinism(workflow_env):
    """Verify workflow replays its own history without divergence"""
    async with Worker(
        workflow_env.client,
        task_queue="test",
        workflows=[DeterministicWorkflow],
    ):
        handle = await workflow_env.client.start_workflow(
            DeterministicWorkflow.run,
            10,
            id="determinism-test",
            task_queue="test",
        )
        await handle.result()

    history = await handle.fetch_history()
    # Raises temporalio.workflow.NondeterminismError on divergence
    await Replayer(workflows=[DeterministicWorkflow]).replay_workflow(history)
```

## Production History Replay

### Exporting Workflow History

```python
from temporalio.client import Client

async def export_workflow_history(workflow_id: str, output_file: str):
    """Export workflow history for replay testing"""

    client = await Client.connect("production.temporal.io:7233")

    # Fetch workflow history
    handle = client.get_workflow_handle(workflow_id)
    history = await handle.fetch_history()

    # fetch_history() returns a WorkflowHistory; store it as JSON
    with open(output_file, "w") as f:
        f.write(history.to_json())

    print(f"Exported history to {output_file}")
```

### Replaying from File

```python
from temporalio.client import WorkflowHistory
from temporalio.worker import Replayer

async def test_replay_from_file():
    """Replay workflow from exported history file"""

    # Load history from file (JSON, as exported above or by `temporal workflow show -o json`)
    with open("workflow_histories/order-123.json") as f:
        history = WorkflowHistory.from_json("order-123", f.read())

    # Replay with current workflow code
    replayer = Replayer(workflows=[OrderWorkflow])
    await replayer.replay_workflow(history)
    # Success = safe to deploy
```

## CI/CD Integration Patterns

### GitHub Actions Example

```yaml
# .github/workflows/replay-tests.yml
name: Replay Tests

on:
  pull_request:
    branches: [main]

jobs:
  replay-tests:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-asyncio

      - name: Download production histories
        run: |
          # Fetch recent workflow histories from production
          python scripts/export_histories.py

      - name: Run replay tests
        run: |
          pytest tests/replay/ --verbose

      - name: Upload results
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: replay-failures
          path: replay-failures/
```

### Automated History Export

```python
# scripts/export_histories.py
import asyncio
from datetime import datetime, timedelta, timezone
from pathlib import Path

from temporalio.client import Client

async def export_recent_histories():
    """Export recent production workflow histories"""

    client = await Client.connect("production.temporal.io:7233")

    # Visibility queries take RFC 3339 timestamps, not relative phrases
    since = (datetime.now(timezone.utc) - timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%SZ")
    query = f"WorkflowType = 'OrderWorkflow' AND CloseTime > '{since}'"

    out_dir = Path("workflow_histories")
    out_dir.mkdir(exist_ok=True)

    count = 0
    async for execution in client.list_workflows(query, limit=100):
        handle = client.get_workflow_handle(execution.id, run_id=execution.run_id)
        history = await handle.fetch_history()
        (out_dir / f"{execution.id}.json").write_text(history.to_json())
        count += 1

    print(f"Exported {count} workflow histories")

if __name__ == "__main__":
    asyncio.run(export_recent_histories())
```

### Replay Test Suite

```python
# tests/replay/test_workflow_replay.py
from pathlib import Path

import pytest
from temporalio.client import WorkflowHistory
from temporalio.worker import Replayer
from workflows import OrderWorkflow, PaymentWorkflow

@pytest.mark.asyncio
async def test_replay_all_histories():
    """Replay all production histories"""

    replayer = Replayer(
        workflows=[OrderWorkflow, PaymentWorkflow]
    )

    # Load all history files
    history_files = sorted(Path("workflow_histories").glob("*.json"))

    failures = []
    for history_file in history_files:
        try:
            history = WorkflowHistory.from_json(history_file.stem, history_file.read_text())

            await replayer.replay_workflow(history)
            print(f"✓ {history_file}")

        except Exception as e:
            failures.append((history_file, str(e)))
            print(f"✗ {history_file}: {e}")

    # Report failures
    if failures:
        pytest.fail(
            f"Replay failed for {len(failures)} workflows:\n"
            + "\n".join(f"  {file}: {error}" for file, error in failures)
        )
```

## Version Compatibility Testing

The Python SDK versions workflow code with `workflow.patched(patch_id)`. It returns
`True` for new executions (and records a marker in history) and `False` when
replaying a history recorded before the patch existed.

### Testing Code Evolution

Record a history with the old code, then replay it with the patched code.

```python
from temporalio import workflow
from temporalio.worker import Replayer, Worker

# Both classes register the same workflow type name
@workflow.defn(name="Evolving")
class EvolvingWorkflowV1:
    @workflow.run
    async def run(self) -> str:
        return "version-1"

@workflow.defn(name="Evolving")
class EvolvingWorkflowV2:
    @workflow.run
    async def run(self) -> str:
        if workflow.patched("new-greeting"):
            return "version-2"  # New executions
        return "version-1"      # Histories recorded before the patch

@pytest.mark.asyncio
async def test_workflow_version_compatibility(workflow_env):
    client = workflow_env.client

    # Record a history with the old code
    async with Worker(client, task_queue="test", workflows=[EvolvingWorkflowV1]):
        handle = await client.start_workflow(
            EvolvingWorkflowV1.run, id="evolving-old", task_queue="test"
        )
        assert await handle.result() == "version-1"
    old_history = await handle.fetch_history()

    # Patched code replays the old history: patched() returns False there
    await Replayer(workflows=[EvolvingWorkflowV2]).replay_workflow(old_history)

    # New executions take the patched branch
    async with Worker(client, task_queue="test", workflows=[EvolvingWorkflowV2]):
        result = await client.execute_workflow(
            EvolvingWorkflowV2.run, id="evolving-new", task_queue="test"
        )
    assert result == "version-2"
```

### Migration Strategy

```python
# Phase 1: Patch. New executions take the new branch; old ones replay the old one
@workflow.defn
class MigratingWorkflow:
    @workflow.run
    async def run(self) -> dict:
        if workflow.patched("new-logic"):
            return await self._new_implementation()
        return await self._old_implementation()

# Phase 2: Once no execution started before the patch is still open, deprecate it.
# Executions with or without the marker both replay cleanly.
@workflow.defn
class MigratingWorkflow:
    @workflow.run
    async def run(self) -> dict:
        workflow.deprecate_patch("new-logic")
        return await self._new_implementation()

# Phase 3: Once no execution started before the deprecation is still open,
# remove the deprecate_patch call
@workflow.defn
class MigratingWorkflow:
    @workflow.run
    async def run(self) -> dict:
        return await self._new_implementation()
```

## Best Practices

1. **Replay Before Deploy**: Always run replay tests before deploying workflow changes
2. **Export Regularly**: Continuously export production histories for testing
3. **CI/CD Integration**: Automated replay testing in pull request checks
4. **Version Tracking**: Use `workflow.patched()` and `workflow.deprecate_patch()` for safe code evolution
5. **History Retention**: Keep representative workflow histories for regression testing
6. **Determinism**: Use `workflow.random()`, `workflow.now()` and `workflow.uuid4()`; make external calls from activities
7. **Comprehensive Testing**: Test against various workflow execution paths

## Common Replay Errors

Replay divergence raises `temporalio.workflow.NondeterminismError`. The message
names the event the new code disagreed with, for example an activity scheduled
where the history recorded a timer.

**Cause**: A code change altered the sequence of commands the workflow issues
(added, removed or reordered an activity, timer or child workflow).

**Solution**: Guard the change with `workflow.patched("<patch-id>")` so histories
recorded before the change keep taking the old branch.

## Additional Resources

- Replay Testing: docs.temporal.io/develop/python/testing-suite#replay-testing
- Workflow Versioning: docs.temporal.io/develop/python/versioning
- Determinism Guide: docs.temporal.io/workflows#deterministic-constraints
- CI/CD Integration: github.com/temporalio/samples-python/tree/main/.github/workflows
