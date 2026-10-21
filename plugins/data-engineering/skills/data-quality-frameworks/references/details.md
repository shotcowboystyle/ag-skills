# data-quality-frameworks: detailed patterns and worked examples

The examples below were run against Great Expectations 1.24, dbt Core 1.12 with dbt-duckdb
and dbt_utils 1.4, and datacontract-cli 1.2 (ODCS v3.2.0).

## Pattern 1: Great Expectations 1.x on a warehouse table

GX 1.x keeps its configuration in Python and saves it under `gx/`. A YAML checkpoint file or
`great_expectations init` belongs to 0.x and does nothing in 1.x. The building blocks are:

- **Data source and asset**: where the data lives (`add_postgres`, `add_snowflake`,
  `add_databricks_sql`, `add_pandas`, ...).
- **Batch definition**: which rows to validate (the whole table, or a daily or monthly
  partition).
- **Expectation suite**: the checks.
- **Validation definition**: one batch definition paired with one suite.
- **Checkpoint**: one or more validation definitions, plus the actions that run afterwards.

Run the setup once and commit `gx/`, except `gx/uncommitted/`.

```bash
pip install "great_expectations[postgresql]>=1,<2"   # or [snowflake], [databricks], ...
```

```python
# setup_gx.py: run once; stores the configuration under ./gx/
import great_expectations as gx
import great_expectations.expectations as gxe

context = gx.get_context(mode="file")

# "${VAR}" is read from the environment when the data source connects
orders = context.data_sources.add_postgres(
    "warehouse", connection_string="${WAREHOUSE_URL}"
).add_table_asset(name="orders", table_name="orders", schema_name="core")
batch_definition = orders.add_batch_definition_whole_table("full_table")

suite = context.suites.add(gx.ExpectationSuite(name="orders_suite"))
for expectation in [
    # Schema
    gxe.ExpectTableColumnsToMatchSet(
        column_set=["order_id", "customer_id", "amount", "status", "created_at"],
        exact_match=False,  # allow extra columns
    ),
    # Primary and foreign keys
    gxe.ExpectColumnValuesToNotBeNull(column="order_id"),
    gxe.ExpectColumnValuesToBeUnique(column="order_id"),
    gxe.ExpectColumnValuesToNotBeNull(column="customer_id"),
    # Validity
    gxe.ExpectColumnValuesToBeInSet(
        column="status",
        value_set=["pending", "processing", "shipped", "delivered", "cancelled"],
    ),
    gxe.ExpectColumnValuesToBeBetween(
        column="amount", min_value=0, max_value=100_000, strict_min=True
    ),
    # Freshness: the caller passes the floor at run time
    gxe.ExpectColumnMaxToBeBetween(
        column="created_at", min_value={"$PARAMETER": "freshness_floor"}
    ),
    # Volume and distribution: take the bounds from history, not guesses
    gxe.ExpectTableRowCountToBeBetween(min_value=1_000),
    gxe.ExpectColumnMeanToBeBetween(column="amount", min_value=50, max_value=500),
]:
    suite.add_expectation(expectation)

validation_definition = context.validation_definitions.add(
    gx.ValidationDefinition(name="orders_full", data=batch_definition, suite=suite)
)

context.checkpoints.add(
    gx.Checkpoint(
        name="orders_checkpoint",
        validation_definitions=[validation_definition],
        actions=[
            gx.checkpoint.UpdateDataDocsAction(name="update_data_docs"),
            gx.checkpoint.SlackNotificationAction(
                name="slack_on_failure",
                slack_webhook="${SLACK_WEBHOOK}",
                notify_on="failure",
                show_failed_expectations=True,
            ),
        ],
        result_format={"result_format": "SUMMARY"},
    )
)
```

To validate more tables in the same run, add one validation definition per table to the
checkpoint's `validation_definitions`. To change a check later, edit the suite and save it
with `suite.save()`. Calling `context.suites.add` again with the same name raises an error.

## Pattern 2: Run the checkpoint as a pipeline gate

```python
# run_gx.py: run on every load; exits non-zero when a check fails
import sys
from datetime import datetime, timedelta

import great_expectations as gx

context = gx.get_context(mode="file")
result = context.checkpoints.get("orders_checkpoint").run(
    expectation_parameters={"freshness_floor": datetime.now() - timedelta(days=1)}
)

for validation in result.run_results.values():
    for r in validation.results:
        if not r.success:
            observed = r.result.get("observed_value", r.result.get("unexpected_count"))
            print(f"FAILED {validation.suite_name} {r.expectation_config.type}: {observed}")

sys.exit(0 if result.success else 1)
```

Call it from the orchestrator or CI step that runs after the load, and stop downstream tasks
when it exits non-zero. `validation.statistics` gives counts of evaluated and failed
expectations for a summary line. Use the same timezone for `freshness_floor` as the column
stores.

For a dataframe batch, pass the frame at run time with
`checkpoint.run(batch_parameters={"dataframe": df})`.

## Pattern 3: dbt data tests

The syntax is for dbt Core 1.10 or later: tests go under `data_tests:`, and test inputs go
under `arguments:`. Before 1.10, drop the `arguments:` level and put its keys directly under
the test name. Install dbt_utils through `packages.yml` and `dbt deps`.

```yaml
# models/marts/_marts__models.yml
models:
  - name: fct_orders
    description: Order fact table
    config:
      materialized: table
      contract:
        enforced: true
    data_tests:
      # Table-level tests
      - row_count_in_range: # custom generic test, Pattern 4
          arguments:
            min_count: 1000
            max_count: 10000000
      - dbt_utils.recency:
          arguments:
            datepart: day
            field: created_at
            interval: 1
      - dbt_utils.expression_is_true:
          arguments:
            expression: "total_amount >= 0"

    columns:
      - name: order_id
        description: Primary key
        data_type: bigint
        constraints:
          - type: not_null
          - type: primary_key
        data_tests:
          - unique
          - not_null

      - name: customer_id
        description: Foreign key to dim_customers
        data_type: bigint
        constraints:
          - type: not_null
        data_tests:
          - relationships:
              arguments:
                to: ref('dim_customers')
                field: customer_id

      - name: order_status
        data_type: varchar
        data_tests:
          - accepted_values:
              arguments:
                values: ["pending", "processing", "shipped", "delivered", "cancelled"]

      - name: total_amount
        data_type: numeric(12,2)
        data_tests:
          - not_null

      - name: created_at
        data_type: timestamp
        data_tests:
          - not_null
          # On a column, the column name is put in front of the expression
          - dbt_utils.expression_is_true:
              arguments:
                expression: "<= current_timestamp"

  - name: dim_customers
    columns:
      - name: customer_id
        data_tests:
          - unique
          - not_null

      - name: email
        data_tests:
          - unique
          - not_null
          # A rough shape check that runs on every warehouse; regex syntax differs
          - dbt_utils.expression_is_true:
              arguments:
                expression: "like '%_@_%._%'"
              config:
                severity: warn
```

Run `dbt build` so each model's tests run right after it builds and failures skip the
models downstream.

## Pattern 4: Custom dbt tests

A generic test is a query that returns the failing rows. It passes when it returns none.

```sql
-- tests/generic/test_row_count_in_range.sql
{% test row_count_in_range(model, min_count, max_count) %}

with row_count as (
    select count(*) as cnt from {{ model }}
)

select cnt
from row_count
where cnt < {{ min_count }} or cnt > {{ max_count }}

{% endtest %}
```

A singular test is a one-off business rule saved as a file under `tests/`:

```sql
-- tests/singular/assert_orders_customers_match.sql
-- Passes when it returns 0 rows
select o.customer_id
from {{ ref('fct_orders') }} o
left join {{ ref('dim_customers') }} c using (customer_id)
where c.customer_id is null
```

Check dbt_utils before writing your own test. It already ships `sequential_values`,
`unique_combination_of_columns`, `not_null_proportion`, `accepted_range` and
`equal_rowcount`.

## Pattern 5: Data contracts (ODCS)

The Open Data Contract Standard (ODCS, Linux Foundation / Bitol) is the contract format that
`datacontract-cli` reads and writes. The producer owns the contract. Consumers review changes
to it, the way they would review changes to an API.

```yaml
# contracts/orders.odcs.yaml
apiVersion: v3.2.0
kind: DataContract
id: orders
name: Orders
version: 1.0.0
status: active

description:
  purpose: Analytics, reporting and ML features
  usage: Internal analytics only
  limitations: customer_id is PII and must not reach downstream marts

team:
  name: data-platform-team

servers:
  - server: production
    type: snowflake
    account: company-us-east-1
    database: ANALYTICS
    schema: CORE

schema:
  - name: orders
    physicalType: table
    properties:
      - name: order_id
        logicalType: string
        required: true
        unique: true
        primaryKey: true
      - name: customer_id
        logicalType: string
        required: true
        classification: restricted
      - name: total_amount
        logicalType: number
        logicalTypeOptions:
          minimum: 0
          maximum: 100000
        description: Order total in USD
      - name: status
        logicalType: string
        quality:
          - metric: invalidValues
            arguments:
              validValues: [pending, processing, shipped, delivered, cancelled]
            mustBe: 0
      - name: created_at
        logicalType: timestamp
        required: true
    quality:
      - metric: rowCount
        mustBeGreaterThan: 0

slaProperties:
  - property: freshness
    value: 1
    unit: h
    element: orders.created_at
  - property: availability
    value: 99.9%
```

```bash
pip install "datacontract-cli[snowflake]"   # extras per server type: [postgres], [databricks], [duckdb], ...
datacontract lint contracts/orders.odcs.yaml                          # schema validity
datacontract test contracts/orders.odcs.yaml --server production      # run the checks against live data
datacontract breaking contracts/orders.v1.yaml contracts/orders.odcs.yaml    # flag changes that break consumers
```

`datacontract test` builds checks from `required`, `unique`, the `logicalTypeOptions` bounds,
the `quality` rules and the freshness SLA, and exits non-zero on failure, so it can gate CI.
It reads warehouse credentials from environment variables such as
`DATACONTRACT_SNOWFLAKE_USERNAME`. Never write them into the contract.
