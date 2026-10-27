---
name: airflow-dag-patterns
description: Write, test or upgrade Apache Airflow 3 DAGs with the Task SDK (`airflow.sdk`), TaskFlow tasks, timetables and asset scheduling, dynamic task mapping, deferrable sensors, retries and failure callbacks. Use when the task is an Airflow DAG, an Airflow operator or sensor, or an Airflow 2 to 3 migration. For SQL models built inside the warehouse use dbt-transformation-patterns; for slow Spark jobs use spark-optimization.
last_verified: 2026-10-27
---

# Airflow DAG Patterns

Write Airflow 3 DAGs that are idempotent, cheap to parse, and tested before deploy. Examples
are checked against Airflow 3.3.

## Procedure

1. **Check the version.** Run `airflow version`. This skill targets 3.x. On 2.x, upgrade first:
   install `apache-airflow-providers-standard`, then run `ruff check dags/ --select AIR301,AIR302`
   (ruff 0.13.1 or later) and fix what it reports. `--fix` applies the safe rewrites.
2. **Pick the trigger.** Use a cron string or timetable when the DAG runs on a clock. Use
   `schedule=[Asset(...)]` when it should run after another DAG writes data, instead of an
   `ExternalTaskSensor`. Use `schedule=None` for DAGs that are only triggered manually or by API.
3. **Decide what a run processes.** In Airflow 3 a plain cron string uses
   `CronTriggerTimetable`, so `data_interval_start == data_interval_end == logical_date` and
   `ds` is the day the run fires, not the day before. If each run processes the period that just
   closed, use `CronDataIntervalTimetable` (quick start below) and read `data_interval_start` and
   `data_interval_end`. Manual and asset-triggered runs can have no `logical_date`.
4. **Write tasks with TaskFlow** (`@task`). Keep task bodies short and import the real logic
   from a module. Pass small values between tasks (paths, IDs, row counts). XCom is stored in
   the metadata database, so write datasets to storage and pass their location.
5. **Make every task idempotent.** A retry or a backfill of the same interval must leave the
   same result: overwrite or merge the interval's partition, never append blindly.
6. **Set failure behavior.** In `default_args`, set `retries`, `retry_delay` and
   `execution_timeout`. Add an `on_failure_callback` (a provider notifier such as
   `SlackNotifier`) at the DAG level. For a sensor, set `timeout` and `deferrable=True` where
   the sensor supports it, otherwise `mode="reschedule"`.
7. **Keep top-level code cheap.** The DAG processor re-parses every file. No network calls, no
   database queries and no `Variable.get()` at module level. Use templates such as
   `{{ var.value.name }}` or read variables inside a task.
8. **Test before you deploy.** Run `python dags/<file>.py` to catch import errors, a DagBag test
   for every file in `dags/`, and `dag.test()` or `airflow dags test <dag_id> <date>` for one full
   run. See `references/details.md` for the test file.
9. **Stop when** the DagBag test has no import errors, one `dag.test()` run succeeds, and a
   second run of the same interval leaves the target unchanged.

Report back with the DAG IDs, their schedule and what each run processes, the retry and alert
settings, and the test commands with their results.

## Airflow 2 to 3 changes that break DAGs

| Airflow 2 | Airflow 3 |
| --- | --- |
| `from airflow.decorators import dag, task` | `from airflow.sdk import dag, task` |
| `from airflow import DAG`, `airflow.models.dag.DAG` | `from airflow.sdk import DAG` |
| `airflow.models.Variable`, `airflow.hooks.base.BaseHook` | `airflow.sdk.Variable`, `airflow.sdk.BaseHook` |
| `airflow.datasets.Dataset` | `airflow.sdk.Asset` |
| `airflow.operators.python.PythonOperator`, `airflow.operators.empty.EmptyOperator`, `airflow.sensors.external_task.ExternalTaskSensor` | same names under `airflow.providers.standard.operators.*` and `airflow.providers.standard.sensors.*` |
| `execution_date`, `next_ds`, `prev_ds`, `yesterday_ds`, `tomorrow_ds` in the context | `logical_date`, `data_interval_start`, `data_interval_end` |
| `schedule_interval=` | `schedule=` |
| `catchup` defaults to `True` | defaults to `False` |
| SubDAGs, `sla=` | task groups, Deadline Alerts |
| `from airflow.settings import Session` or ORM models in a task | not allowed; use the REST API (`apache-airflow-client`) |

## Quick Start

```python
# dags/orders_daily.py
from datetime import timedelta

import pendulum
from airflow.sdk import CronDataIntervalTimetable, dag, task


@dag(
    schedule=CronDataIntervalTimetable("0 6 * * *", timezone="UTC"),
    start_date=pendulum.datetime(2026, 1, 1, tz="UTC"),
    catchup=False,
    max_active_runs=1,
    default_args={
        "retries": 3,
        "retry_delay": timedelta(minutes=5),
        "retry_exponential_backoff": True,
        "execution_timeout": timedelta(hours=1),
    },
    tags=["orders"],
)
def orders_daily():
    @task
    def extract(data_interval_start=None) -> str:
        # Context values are injected by parameter name.
        day = data_interval_start.strftime("%Y-%m-%d")
        return f"s3://raw/orders/dt={day}/"

    @task
    def transform(path: str) -> str:
        return path.replace("/raw/", "/clean/")

    @task
    def load(path: str) -> None:
        print(f"merging {path} into analytics.orders")

    load(transform(extract()))


orders_daily()
```

Each run fires at 06:00 UTC and processes the previous day: `data_interval_start` is 06:00 the
day before.

## References

- `references/details.md`: asset scheduling, dynamic task mapping, branching, deferrable and
  custom sensors, failure callbacks, a classic-operator DAG, DagBag and task tests, and the
  project layout.
