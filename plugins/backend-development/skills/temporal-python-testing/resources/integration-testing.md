# Integration Testing with Mocked Activities

Comprehensive patterns for testing workflows with mocked external dependencies, error injection, and complex scenarios.

Workflow classes must be defined at module level. The SDK rejects a `@workflow.defn`
class defined inside a test function (`ValueError: Local classes unsupported`).
Activities may be defined anywhere, which is what makes mocking work: register a
test activity under the production activity's name and the workflow calls it
instead.

The examples assume this fixture (see `local-setup.md` for a shared `conftest.py`):

```python
import pytest_asyncio
from temporalio.testing import WorkflowEnvironment

@pytest_asyncio.fixture
async def workflow_env():
    env = await WorkflowEnvironment.start_time_skipping()
    yield env
    await env.shutdown()
```

## Activity Mocking Strategy

**Purpose**: Test workflow orchestration logic without calling real external services

### Basic Mock Pattern

```python
# workflows.py (production code)
from datetime import timedelta
from temporalio import activity, workflow
from temporalio.exceptions import ActivityError

@activity.defn
async def process_external_data(input: str) -> str:
    ...  # calls a real service

@workflow.defn
class WorkflowWithActivity:
    @workflow.run
    async def run(self, input: str) -> str:
        try:
            result = await workflow.execute_activity(
                process_external_data,
                input,
                start_to_close_timeout=timedelta(seconds=10),
            )
        except ActivityError as e:
            # Activity failures reach the workflow as ActivityError;
            # the original ApplicationError is e.cause
            return f"error: {e.cause.message}"
        return f"processed: {result}"
```

```python
# test_workflows.py
from unittest.mock import AsyncMock

import pytest
from temporalio import activity
from temporalio.worker import Worker

from workflows import WorkflowWithActivity

@pytest.mark.asyncio
async def test_workflow_with_mocked_activity(workflow_env):
    """Mock activity to test workflow logic"""
    mock = AsyncMock(return_value="mocked-result")

    # Same name as the production activity, so the workflow calls this one
    @activity.defn(name="process_external_data")
    async def process_external_data_mocked(input: str) -> str:
        return await mock(input)

    async with Worker(
        workflow_env.client,
        task_queue="test",
        workflows=[WorkflowWithActivity],
        activities=[process_external_data_mocked],
    ):
        result = await workflow_env.client.execute_workflow(
            WorkflowWithActivity.run,
            "test-input",
            id="wf-mock",
            task_queue="test",
        )
    assert result == "processed: mocked-result"
    mock.assert_awaited_once_with("test-input")
```

### Dynamic Mock Responses

**Scenario-Based Mocking**:

```python
from temporalio.exceptions import ApplicationError

@pytest.mark.asyncio
async def test_workflow_multiple_mock_scenarios(workflow_env):
    """Test different workflow paths with dynamic mocks"""

    # Mock returns different values based on input
    @activity.defn(name="process_external_data")
    async def process_external_data_mocked(input: str) -> str:
        if input == "error-case":
            raise ApplicationError("Validation failed", non_retryable=True)
        return f"processed-{input}"

    async with Worker(
        workflow_env.client,
        task_queue="test",
        workflows=[WorkflowWithActivity],
        activities=[process_external_data_mocked],
    ):
        # Test success path
        result_success = await workflow_env.client.execute_workflow(
            WorkflowWithActivity.run,
            "valid-input",
            id="wf-success",
            task_queue="test",
        )
        assert result_success == "processed: processed-valid-input"

        # Test error path
        result_error = await workflow_env.client.execute_workflow(
            WorkflowWithActivity.run,
            "error-case",
            id="wf-error",
            task_queue="test",
        )
        assert result_error == "error: Validation failed"
```

## Error Injection Patterns

### Testing Transient Failures

**Retry Behavior**:

```python
# workflows.py
from temporalio.common import RetryPolicy

@activity.defn
async def charge_card(order_id: str) -> str:
    ...  # calls the payment provider

@workflow.defn
class RetryWorkflow:
    @workflow.run
    async def run(self, order_id: str) -> str:
        return await workflow.execute_activity(
            charge_card,
            order_id,
            start_to_close_timeout=timedelta(seconds=10),
            retry_policy=RetryPolicy(
                initial_interval=timedelta(milliseconds=10),
                backoff_coefficient=1.0,
                maximum_attempts=5,
            ),
        )
```

```python
@pytest.mark.asyncio
async def test_workflow_transient_errors(workflow_env):
    """Test retry logic with controlled failures"""
    attempts = 0

    @activity.defn(name="charge_card")
    async def charge_card_flaky(order_id: str) -> str:
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            raise RuntimeError(f"Transient error {attempts}")
        return f"charged-{order_id}"

    async with Worker(
        workflow_env.client,
        task_queue="test",
        workflows=[RetryWorkflow],
        activities=[charge_card_flaky],
    ):
        result = await workflow_env.client.execute_workflow(
            RetryWorkflow.run,
            "order-1",
            id="retry-wf",
            task_queue="test",
        )
    assert result == "charged-order-1"
    assert attempts == 3
```

### Testing Non-Retryable Errors

**Business Validation Failures**:

```python
from temporalio.client import WorkflowFailureError
from temporalio.exceptions import ActivityError

@pytest.mark.asyncio
async def test_workflow_non_retryable_error(workflow_env):
    """Test handling of permanent failures"""
    attempts = 0

    @activity.defn(name="charge_card")
    async def charge_card_declined(order_id: str) -> str:
        nonlocal attempts
        attempts += 1
        raise ApplicationError("Card declined", non_retryable=True)

    async with Worker(
        workflow_env.client,
        task_queue="test",
        workflows=[RetryWorkflow],
        activities=[charge_card_declined],
    ):
        with pytest.raises(WorkflowFailureError) as exc_info:
            await workflow_env.client.execute_workflow(
                RetryWorkflow.run,
                "order-2",
                id="declined-wf",
                task_queue="test",
            )

    # WorkflowFailureError -> ActivityError -> ApplicationError
    assert isinstance(exc_info.value.cause, ActivityError)
    assert exc_info.value.cause.cause.message == "Card declined"
    assert attempts == 1  # non_retryable skips the retry policy
```

## Multi-Activity Workflow Testing

### Sequential Activity Pattern

```python
# workflows.py
@activity.defn
async def step_1(input: str) -> str:
    return f"{input}-step1"

@activity.defn
async def step_2(input: str) -> str:
    return f"{input}-step2"

@activity.defn
async def step_3(input: str) -> str:
    return f"{input}-step3"

@workflow.defn
class SequentialWorkflow:
    @workflow.run
    async def run(self, input: str) -> str:
        result = input
        for step in (step_1, step_2, step_3):
            result = await workflow.execute_activity(
                step,
                result,
                start_to_close_timeout=timedelta(seconds=10),
            )
        return result
```

```python
@pytest.mark.asyncio
async def test_workflow_sequential_activities(workflow_env):
    """Test workflow orchestrating multiple activities"""
    async with Worker(
        workflow_env.client,
        task_queue="test",
        workflows=[SequentialWorkflow],
        activities=[step_1, step_2, step_3],
    ):
        result = await workflow_env.client.execute_workflow(
            SequentialWorkflow.run,
            "start",
            id="seq-wf",
            task_queue="test",
        )
    assert result == "start-step1-step2-step3"
```

### Parallel Activity Pattern

Workflows run on a deterministic event loop, so `asyncio.gather` over activity
calls is safe inside workflow code.

```python
# workflows.py
import asyncio

@activity.defn
async def parallel_task(task_id: int) -> str:
    return f"task-{task_id}"

@workflow.defn
class ParallelWorkflow:
    @workflow.run
    async def run(self, task_count: int) -> list[str]:
        # Execute activities in parallel
        return await asyncio.gather(
            *(
                workflow.execute_activity(
                    parallel_task,
                    i,
                    start_to_close_timeout=timedelta(seconds=10),
                )
                for i in range(task_count)
            )
        )
```

```python
@pytest.mark.asyncio
async def test_workflow_parallel_activities(workflow_env):
    """Test concurrent activity execution"""
    async with Worker(
        workflow_env.client,
        task_queue="test",
        workflows=[ParallelWorkflow],
        activities=[parallel_task],
    ):
        result = await workflow_env.client.execute_workflow(
            ParallelWorkflow.run,
            3,
            id="parallel-wf",
            task_queue="test",
        )
    assert result == ["task-0", "task-1", "task-2"]
```

## Signal and Query Testing

### Signal Handlers

```python
# workflows.py
@workflow.defn
class SignalWorkflow:
    def __init__(self) -> None:
        self._status = "initialized"

    @workflow.run
    async def run(self) -> str:
        # Wait for completion signal
        await workflow.wait_condition(lambda: self._status == "completed")
        return self._status

    @workflow.signal
    def update_status(self, new_status: str) -> None:
        self._status = new_status

    @workflow.query
    def get_status(self) -> str:
        return self._status
```

```python
@pytest.mark.asyncio
async def test_workflow_signals(workflow_env):
    """Test workflow signal handling"""
    async with Worker(
        workflow_env.client,
        task_queue="test",
        workflows=[SignalWorkflow],
    ):
        # Start workflow
        handle = await workflow_env.client.start_workflow(
            SignalWorkflow.run,
            id="signal-wf",
            task_queue="test",
        )

        # Verify initial state via query
        assert await handle.query(SignalWorkflow.get_status) == "initialized"

        # Send signal and verify updated state
        await handle.signal(SignalWorkflow.update_status, "processing")
        assert await handle.query(SignalWorkflow.get_status) == "processing"

        # Complete workflow
        await handle.signal(SignalWorkflow.update_status, "completed")
        assert await handle.result() == "completed"
```

## Coverage Strategies

Temporal does not prescribe a coverage percentage. Measure coverage of workflow
decision logic and activity logic separately, and set a threshold that suits your
team. Aim for every branch a workflow can take, not a number.

### Workflow Logic Coverage

```python
# Test all branches (ConditionalWorkflow is defined in unit-testing.md)
@pytest.mark.parametrize("condition,expected", [
    (True, "path-a"),
    (False, "path-b"),
])
@pytest.mark.asyncio
async def test_workflow_branches(workflow_env, condition, expected):
    """Ensure all code paths are tested"""
    async with Worker(
        workflow_env.client,
        task_queue="test",
        workflows=[ConditionalWorkflow],
    ):
        result = await workflow_env.client.execute_workflow(
            ConditionalWorkflow.run,
            condition,
            id=f"branch-{condition}",
            task_queue="test",
        )
    assert result == expected
```

### Activity Coverage

```python
from temporalio.testing import ActivityEnvironment

# Test activity edge cases (process_data is defined in unit-testing.md)
@pytest.mark.parametrize("input,expected", [
    ("valid", "VALID"),
    ("", ""),
])
@pytest.mark.asyncio
async def test_activity_edge_cases(input, expected):
    """Test activity edge cases"""
    assert await ActivityEnvironment().run(process_data, input) == expected
```

## Integration Test Organization

### Test Structure

```
tests/
├── integration/
│   ├── conftest.py              # Shared fixtures
│   ├── test_order_workflow.py   # Order processing tests
│   ├── test_payment_workflow.py # Payment tests
│   └── test_fulfillment_workflow.py
├── unit/
│   ├── test_order_activities.py
│   └── test_payment_activities.py
└── fixtures/
    └── test_data.py             # Test data builders
```

### Shared Fixtures

```python
# conftest.py
from unittest.mock import Mock

import pytest
import pytest_asyncio
from temporalio.testing import WorkflowEnvironment

# A session-scoped async fixture needs a session-scoped event loop
@pytest_asyncio.fixture(scope="session", loop_scope="session")
async def workflow_env():
    """Session-scoped environment for integration tests"""
    env = await WorkflowEnvironment.start_time_skipping()
    yield env
    await env.shutdown()

@pytest.fixture
def mock_payment_service():
    """Mock external payment service"""
    return Mock()

@pytest.fixture
def mock_inventory_service():
    """Mock external inventory service"""
    return Mock()
```

Tests that use the session-scoped `workflow_env` must run on the same loop:
mark them `@pytest.mark.asyncio(loop_scope="session")`, or set
`asyncio_default_test_loop_scope = session` as in `local-setup.md`.

## Best Practices

1. **Mock External Dependencies**: Never call real APIs in tests
2. **Test Error Scenarios**: Verify compensation and retry logic
3. **Parallel Testing**: Use pytest-xdist for faster test runs
4. **Isolated Tests**: Each test should be independent
5. **Clear Assertions**: Verify both results and side effects
6. **Branch Coverage**: Exercise every path a critical workflow can take
7. **Fast Execution**: Use time-skipping, avoid real delays

## Additional Resources

- Mocking Strategies: docs.temporal.io/develop/python/testing-suite
- pytest Best Practices: docs.pytest.org/en/stable/goodpractices.html
- Python SDK Samples: github.com/temporalio/samples-python
