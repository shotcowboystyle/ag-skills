# airflow-dag-patterns: detailed patterns

All examples target Airflow 3.3 and import DAG-authoring names from `airflow.sdk`. Operators and
sensors that used to ship in core (`PythonOperator`, `BashOperator`, `EmptyOperator`,
`ExternalTaskSensor`, `FileSensor`) live in `apache-airflow-providers-standard`.

## Asset scheduling between DAGs

A task that lists an asset in `outlets` marks it updated when it succeeds. A DAG scheduled on
that asset runs after the update. This replaces an `ExternalTaskSensor` that polls another DAG.

```python
# dags/orders_assets.py
import pendulum
from airflow.sdk import Asset, dag, task

raw_orders = Asset("s3://lake/raw/orders/")
clean_orders = Asset("s3://lake/clean/orders/")


@dag(schedule="@hourly", start_date=pendulum.datetime(2026, 1, 1, tz="UTC"), catchup=False)
def land_orders():
    @task(outlets=[raw_orders])
    def land() -> None:
        print("landed new files")

    land()


@dag(schedule=[raw_orders], start_date=pendulum.datetime(2026, 1, 1, tz="UTC"), catchup=False)
def clean_orders_dag():
    @task(outlets=[clean_orders])
    def clean() -> None:
        print("rewrote clean partition")

    clean()


land_orders()
clean_orders_dag()
```

`schedule=[a, b]` waits for both assets. Use `a | b` to run on either, or
`AssetOrTimeSchedule(timetable=..., assets=...)` to run on a clock and on updates.

## Dynamic task mapping

Create one task instance per input at run time with `.expand()`. Constant arguments go in
`.partial()`. Cap concurrency with `max_active_tis_per_dag` when the target can't take the load.

```python
# dags/per_table_export.py
import pendulum
from airflow.sdk import dag, task


@dag(schedule=None, start_date=pendulum.datetime(2026, 1, 1, tz="UTC"), catchup=False)
def per_table_export():
    @task
    def list_tables() -> list[str]:
        return ["customers", "orders", "payments"]

    @task(max_active_tis_per_dag=2)
    def export(table: str, bucket: str) -> int:
        print(f"exporting {table} to {bucket}")
        return 0

    @task
    def summarize(row_counts: list[int]) -> None:
        print(f"exported {len(row_counts)} tables")

    counts = export.partial(bucket="s3://exports").expand(table=list_tables())
    summarize(counts)


per_table_export()
```

## Branching

`@task.branch` returns the `task_id` (or list of IDs) to run. The other branches are skipped,
so a join task after them needs a trigger rule that tolerates skips.

```python
# dags/quality_branch.py
import pendulum
from airflow.providers.standard.operators.empty import EmptyOperator
from airflow.sdk import dag, task


@dag(schedule=None, start_date=pendulum.datetime(2026, 1, 1, tz="UTC"), catchup=False)
def quality_branch():
    @task
    def score() -> float:
        return 0.95

    @task.branch
    def route(quality: float) -> str:
        return "publish" if quality >= 0.9 else "quarantine"

    publish = EmptyOperator(task_id="publish")
    quarantine = EmptyOperator(task_id="quarantine")
    done = EmptyOperator(task_id="done", trigger_rule="none_failed_min_one_success")

    route(score()) >> [publish, quarantine] >> done


quality_branch()
```

## Sensors

Prefer a deferrable sensor: it hands the wait to the triggerer and frees the worker slot. Every
sensor needs a `timeout`, or it waits for 7 days.

```python
# Needs apache-airflow-providers-amazon.
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor

wait_for_file = S3KeySensor(
    task_id="wait_for_file",
    bucket_name="lake",
    bucket_key="raw/orders/dt={{ data_interval_start | ds }}/_SUCCESS",
    deferrable=True,
    timeout=2 * 60 * 60,
)
```

For a condition no provider covers, write a `@task.sensor`. It pokes until `is_done` is true and
pushes `xcom_value` downstream. `mode="reschedule"` releases the worker slot between pokes.

```python
# dags/wait_for_export.py
import pendulum
from airflow.sdk import PokeReturnValue, dag, task


@dag(schedule=None, start_date=pendulum.datetime(2026, 1, 1, tz="UTC"), catchup=False)
def wait_for_export():
    @task.sensor(poke_interval=60, timeout=60 * 60, mode="reschedule")
    def export_ready() -> PokeReturnValue:
        status = {"state": "done", "path": "s3://exports/latest/"}  # replace with an API call
        return PokeReturnValue(is_done=status["state"] == "done", xcom_value=status["path"])

    @task
    def load(path: str) -> None:
        print(f"loading {path}")

    load(export_ready())


wait_for_export()
```

## Failure callbacks and cleanup

A DAG-level `on_failure_callback` fires once per failed run. Put a task-level callback in
`default_args` when you need an alert per task. Provider notifiers (for example
`SlackNotifier` in `apache-airflow-providers-slack`) can be passed directly as the callback.
A task with `trigger_rule="all_done"` runs whether its upstream tasks failed or succeeded.

```python
# dags/with_alerts.py
from datetime import timedelta

import pendulum
from airflow.sdk import dag, task


def alert(context) -> None:
    ti = context["ti"]
    print(f"{ti.dag_id}.{ti.task_id} failed for run {context['run_id']}: {context.get('exception')}")


@dag(
    schedule=None,
    start_date=pendulum.datetime(2026, 1, 1, tz="UTC"),
    catchup=False,
    on_failure_callback=alert,
    default_args={"retries": 2, "retry_delay": timedelta(minutes=1)},
)
def with_alerts():
    @task
    def load() -> None:
        print("loading")

    @task(trigger_rule="all_done")
    def drop_staging_table() -> None:
        print("dropping staging table")

    load() >> drop_staging_table()


with_alerts()
```

SLAs were removed in Airflow 3. Use Deadline Alerts (3.1 and later) to alert when a run takes
longer than expected.

## Classic operators

Use an operator when a provider already wraps the work (SQL, Kubernetes, cloud services). Mix
them with TaskFlow tasks freely; a TaskFlow call returns an object you can chain with `>>`.

```python
# dags/classic_operators.py
import pendulum
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.python import PythonOperator
from airflow.sdk import DAG


def count_rows(table: str) -> int:
    print(f"counting {table}")
    return 0


with DAG(
    dag_id="classic_operators",
    schedule=None,
    start_date=pendulum.datetime(2026, 1, 1, tz="UTC"),
    catchup=False,
):
    dbt_build = BashOperator(
        task_id="dbt_build",
        bash_command="echo dbt build --select tag:daily --vars '{day: {{ ds }}}'",
    )
    count = PythonOperator(
        task_id="count",
        python_callable=count_rows,
        op_kwargs={"table": "analytics.orders"},
    )
    dbt_build >> count
```

For a dbt project with many models, the `astronomer-cosmos` package renders each model as its
own task with retries and lineage, instead of one `dbt build` call.

## Generating DAGs from config

Build one DAG per entry with a factory function. The DAG processor finds any `DAG` object at
module level, so calling the decorated function is enough.

```python
# dags/dag_factory.py
import pendulum
from airflow.sdk import dag, task

SOURCES = {"customers": "@daily", "orders": "@hourly"}


def build(name: str, schedule: str):
    @dag(
        dag_id=f"ingest_{name}",
        schedule=schedule,
        start_date=pendulum.datetime(2026, 1, 1, tz="UTC"),
        catchup=False,
        tags=["ingest"],
    )
    def ingest():
        @task
        def copy() -> None:
            print(f"copying {name}")

        copy()

    return ingest()


for name, schedule in SOURCES.items():
    build(name, schedule)
```

Keep the config in the repository. Reading it from a database or API at parse time slows every
parse and can break all DAGs when the source is down.

## Testing

```python
# tests/test_dags.py
from pathlib import Path

import pytest
from airflow.dag_processing.dagbag import DagBag

DAGS = Path(__file__).parent.parent / "dags"


@pytest.fixture(scope="session")
def dagbag() -> DagBag:
    return DagBag(dag_folder=DAGS)


def test_no_import_errors(dagbag: DagBag) -> None:
    assert dagbag.import_errors == {}


def test_no_dag_backfills_by_accident(dagbag: DagBag) -> None:
    for dag_id, dag in dagbag.dags.items():
        assert not dag.catchup, dag_id


def test_orders_daily_shape(dagbag: DagBag) -> None:
    dag = dagbag.dags["orders_daily"]
    assert [t.task_id for t in dag.get_task("extract").downstream_list] == ["transform"]
```

Test task logic as plain functions: keep it in a module and call it from the test without Airflow.
For one full run against a local metadata database:

```bash
export AIRFLOW_HOME="$PWD/.airflow"
airflow db migrate
airflow dags test orders_daily 2026-01-02
```

`dag.test()` does the same from Python and is easy to run under a debugger:

```python
if __name__ == "__main__":
    orders_daily().test()
```

## Project layout

```
airflow/
├── dags/
│   ├── orders_daily.py
│   └── orders_assets.py
├── include/            # task logic imported by DAGs; unit-tested without Airflow
│   └── orders.py
├── plugins/            # custom operators, hooks, notifiers
├── tests/
│   └── test_dags.py
└── requirements.txt    # pin apache-airflow and providers to the same constraints file
```

Install Airflow with the constraints file for your Airflow and Python versions:

```bash
pip install "apache-airflow==3.3.2" \
  --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-3.3.2/constraints-3.12.txt"
```
