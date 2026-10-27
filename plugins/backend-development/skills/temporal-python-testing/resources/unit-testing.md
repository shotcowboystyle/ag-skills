# Unit Testing Temporal Workflows and Activities

Focused guide for testing individual workflows and activities in isolation using WorkflowEnvironment and ActivityEnvironment.

Define workflow classes at module level (in production code or at the top of the
test module). The SDK rejects a `@workflow.defn` class defined inside a test
function (`ValueError: Local classes unsupported`).

## WorkflowEnvironment with Time-Skipping

**Purpose**: Test workflows in isolation with instant time progression (month-long workflows → seconds)

### Basic Setup Pattern

```python
import pytest
import pytest_asyncio
from temporalio.testing import WorkflowEnvironment
from temporalio.worker import Worker

# Async fixtures need @pytest_asyncio.fixture unless asyncio_mode = auto
@pytest_asyncio.fixture
async def workflow_env():
    """Reusable time-skipping test environment"""
    env = await WorkflowEnvironment.start_time_skipping()
    yield env
    await env.shutdown()

@pytest.mark.asyncio
async def test_workflow_execution(workflow_env):
    """Test workflow with time-skipping"""
    async with Worker(
        workflow_env.client,
        task_queue="test-queue",
        workflows=[YourWorkflow],
        activities=[your_activity],
    ):
        result = await workflow_env.client.execute_workflow(
            YourWorkflow.run,
            "test-input",
            id="test-wf-id",
            task_queue="test-queue",
        )
        assert result == "expected-output"
```

**Key Benefits**:

- `workflow.sleep(timedelta(days=30))` completes instantly
- Fast feedback loop (milliseconds vs hours)
- Deterministic test execution

### Time-Skipping Examples

**Sleep Advancement**:

```python
from datetime import timedelta
from temporalio import workflow

@workflow.defn
class DelayedWorkflow:
    @workflow.run
    async def run(self) -> str:
        await workflow.sleep(timedelta(hours=24))  # Instant in tests
        return "completed"

@pytest.mark.asyncio
async def test_workflow_with_delays(workflow_env):
    """Workflow sleeps are instant in time-skipping mode"""
    async with Worker(
        workflow_env.client,
        task_queue="test",
        workflows=[DelayedWorkflow],
    ):
        result = await workflow_env.client.execute_workflow(
            DelayedWorkflow.run,
            id="delayed-wf",
            task_queue="test",
        )
        assert result == "completed"
```

**Manual Time Control**:

```python
@workflow.defn
class TimeBasedWorkflow:
    def __init__(self) -> None:
        self._state = "started"

    @workflow.run
    async def run(self) -> str:
        await workflow.sleep(timedelta(minutes=30))
        self._state = "processing"
        await workflow.sleep(timedelta(hours=12))
        self._state = "completed"
        return self._state

    @workflow.query
    def get_state(self) -> str:
        return self._state

@pytest.mark.asyncio
async def test_workflow_manual_time(workflow_env):
    """Manually advance time for precise control"""
    async with Worker(
        workflow_env.client,
        task_queue="test",
        workflows=[TimeBasedWorkflow],
    ):
        handle = await workflow_env.client.start_workflow(
            TimeBasedWorkflow.run,
            id="time-wf",
            task_queue="test",
        )

        # Advance time by specific amount
        await workflow_env.sleep(timedelta(hours=1))

        # Verify intermediate state via query
        assert await handle.query(TimeBasedWorkflow.get_state) == "processing"

        # Waiting on the result skips the remaining time
        assert await handle.result() == "completed"
```

### Testing Workflow Logic

**Decision Testing**:

```python
@workflow.defn
class ConditionalWorkflow:
    @workflow.run
    async def run(self, condition: bool) -> str:
        if condition:
            return "path-a"
        return "path-b"

@pytest.mark.asyncio
async def test_workflow_branching(workflow_env):
    """Test different execution paths"""
    async with Worker(
        workflow_env.client,
        task_queue="test",
        workflows=[ConditionalWorkflow],
    ):
        # Test true path
        result_a = await workflow_env.client.execute_workflow(
            ConditionalWorkflow.run,
            True,
            id="cond-wf-true",
            task_queue="test",
        )
        assert result_a == "path-a"

        # Test false path
        result_b = await workflow_env.client.execute_workflow(
            ConditionalWorkflow.run,
            False,
            id="cond-wf-false",
            task_queue="test",
        )
        assert result_b == "path-b"
```

## ActivityEnvironment Testing

**Purpose**: Test activities in isolation without workflows or Temporal server

### Basic Activity Test

```python
from temporalio import activity
from temporalio.testing import ActivityEnvironment

@activity.defn
async def process_data(input: str) -> str:
    return input.upper()

@pytest.mark.asyncio
async def test_activity_basic():
    """Test activity without workflow context"""
    env = ActivityEnvironment()
    result = await env.run(process_data, "test")
    assert result == "TEST"
```

### Testing Activity Context

**Heartbeat Testing**:

```python
import asyncio

@activity.defn
async def long_running_activity(total_items: int) -> int:
    for i in range(total_items):
        activity.heartbeat(i)  # Report progress
        await asyncio.sleep(0.1)
    return total_items

@pytest.mark.asyncio
async def test_activity_heartbeat():
    """Verify heartbeat calls"""
    heartbeats = []
    env = ActivityEnvironment()
    env.on_heartbeat = lambda *details: heartbeats.append(details[0])

    result = await env.run(long_running_activity, 10)
    assert result == 10
    assert heartbeats == list(range(10))
```

**Cancellation Testing**:

```python
@activity.defn
async def cancellable_activity() -> str:
    try:
        while True:
            activity.heartbeat()
            await asyncio.sleep(0.1)
    except asyncio.CancelledError:
        return "cancelled"

@pytest.mark.asyncio
async def test_activity_cancellation():
    """Test activity cancellation handling"""
    env = ActivityEnvironment()
    task = asyncio.create_task(env.run(cancellable_activity))
    await asyncio.sleep(0.2)

    env.cancel()  # Delivers cancellation to the running activity
    assert await task == "cancelled"
```

### Testing Error Handling

**Exception Propagation**:

```python
from temporalio.exceptions import ApplicationError

@activity.defn
async def failing_activity(should_fail: bool) -> str:
    if should_fail:
        raise ApplicationError("Validation failed", non_retryable=True)
    return "success"

@pytest.mark.asyncio
async def test_activity_error():
    """Test activity error handling"""
    env = ActivityEnvironment()

    # Test success path
    result = await env.run(failing_activity, False)
    assert result == "success"

    # Test error path
    with pytest.raises(ApplicationError, match="Validation failed"):
        await env.run(failing_activity, True)
```

## Pytest Integration Patterns

### Shared Fixtures

```python
# conftest.py
import pytest
import pytest_asyncio
from temporalio.testing import ActivityEnvironment, WorkflowEnvironment

# A module-scoped async fixture needs a module-scoped event loop, and the
# tests that use it must run on that loop: @pytest.mark.asyncio(loop_scope="module")
@pytest_asyncio.fixture(scope="module", loop_scope="module")
async def workflow_env():
    """Module-scoped environment (reused across tests)"""
    env = await WorkflowEnvironment.start_time_skipping()
    yield env
    await env.shutdown()

@pytest.fixture
def activity_env():
    """Function-scoped environment (fresh per test)"""
    return ActivityEnvironment()
```

### Parameterized Tests

```python
@pytest.mark.parametrize("input,expected", [
    ("test", "TEST"),
    ("hello", "HELLO"),
    ("123", "123"),
])
@pytest.mark.asyncio
async def test_activity_parameterized(activity_env, input, expected):
    """Test multiple input scenarios"""
    result = await activity_env.run(process_data, input)
    assert result == expected
```

## Best Practices

1. **Fast Execution**: Use time-skipping for all workflow tests
2. **Isolation**: Test workflows and activities separately
3. **Shared Fixtures**: Reuse WorkflowEnvironment across related tests
4. **Branch Coverage**: Test every decision path in workflow logic
5. **Mock Activities**: Use ActivityEnvironment for activity-specific logic
6. **Determinism**: Ensure test results are consistent across runs
7. **Error Cases**: Test both success and failure scenarios

## Common Patterns

**Testing Retry Logic**:

```python
from temporalio.common import RetryPolicy

call_count = 0

@activity.defn
async def flaky_activity() -> str:
    global call_count
    call_count += 1
    if call_count < 3:
        raise RuntimeError("Transient error")
    return "success"

@workflow.defn
class RetryWorkflow:
    @workflow.run
    async def run(self) -> str:
        return await workflow.execute_activity(
            flaky_activity,
            start_to_close_timeout=timedelta(seconds=10),
            retry_policy=RetryPolicy(
                initial_interval=timedelta(milliseconds=1),
                maximum_attempts=5,
            ),
        )

@pytest.mark.asyncio
async def test_workflow_with_retries(workflow_env):
    """Test activity retry behavior"""
    async with Worker(
        workflow_env.client,
        task_queue="test",
        workflows=[RetryWorkflow],
        activities=[flaky_activity],
    ):
        result = await workflow_env.client.execute_workflow(
            RetryWorkflow.run,
            id="retry-wf",
            task_queue="test",
        )
        assert result == "success"
        assert call_count == 3  # Verify retry attempts
```

## Additional Resources

- Python SDK Testing: docs.temporal.io/develop/python/testing-suite
- pytest Documentation: docs.pytest.org
- Temporal Samples: github.com/temporalio/samples-python
