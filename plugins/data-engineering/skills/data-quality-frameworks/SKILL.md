---
name: data-quality-frameworks
description: Implement data quality validation with Great Expectations 1.x, dbt data tests and model contracts, and ODCS data contracts. Use when building data quality pipelines, implementing validation rules, or establishing data contracts.
last_verified: 2026-10-20
---

# Data Quality Frameworks

Add data quality checks with Great Expectations (GX), dbt data tests and model contracts, and
data contracts between teams.

## When to Use This Skill

- Adding quality checks to a pipeline or a dbt project
- Setting up or upgrading Great Expectations
- Enforcing a model's schema at build time
- Agreeing a data contract with a producing or consuming team
- Blocking a load in CI/CD when data is bad

## Procedure

1. **Find what matters.** List the tables that consumers, dashboards or SLAs depend on, and
   the columns in them that carry keys, money, status or time. Check those first, not every
   column.
2. **Pick the tool by where the data lives.**
   - Models built by dbt: dbt data tests, plus `contract: enforced` on models other teams
     read.
   - Python pipelines, dataframes, files, or sources outside dbt: GX 1.x.
   - An interface between teams: an Open Data Contract Standard (ODCS) contract, checked with
     `datacontract test`.
3. **Check the GX version before you write any code.** Run
   `python -c "import great_expectations as gx; print(gx.__version__)"`. This skill targets
   1.x. In 0.x, `great_expectations init`, `context.run_checkpoint`, YAML checkpoints and
   `ExpectationConfiguration` all work differently, so don't mix the two. If the project is
   on 0.x, upgrade it using GX's migration guide first.
4. **Cover each dimension** that applies (table below). Every key column needs not-null and
   unique checks. Every table needs a freshness check and a volume check.
5. **Set thresholds from history.** Profile recent loads and set bounds just outside the
   range you observe. Don't invent row counts or means. For checks that may fail on some rows,
   use `mostly` in GX or `severity: warn` in dbt.
6. **Gate the pipeline.** A failed blocking check exits non-zero and stops the load. Warnings
   go to alerting. Never let a failed check pass silently.
7. **Stop when** every critical table has key, validity, freshness and volume checks that
   run on each load, and you have seen one failure end to end: break a row on purpose and
   confirm that the gate fails and the alert fires.

Report back with the checks added for each table, where each one runs, which ones block and
which ones warn, and the commands that run them.

## Data Quality Dimensions

| Dimension        | Description              | GX 1.x expectation                       | dbt                         |
| ---------------- | ------------------------ | ---------------------------------------- | --------------------------- |
| **Completeness** | No missing values        | `ExpectColumnValuesToNotBeNull`          | `not_null`                  |
| **Uniqueness**   | No duplicates            | `ExpectColumnValuesToBeUnique`           | `unique`                    |
| **Validity**     | Values in expected range | `ExpectColumnValuesToBeInSet`, `...ToBeBetween` | `accepted_values`    |
| **Integrity**    | Foreign keys resolve     | cross-table query                        | `relationships`             |
| **Consistency**  | No contradictions        | `ExpectColumnPairValuesAToBeGreaterThanB` | `dbt_utils.expression_is_true` |
| **Timeliness**   | Data is recent           | `ExpectColumnMaxToBeBetween`             | `dbt_utils.recency`         |
| **Volume**       | Expected row count       | `ExpectTableRowCountToBeBetween`         | custom generic test         |

## Quick start: Great Expectations 1.x

```bash
pip install "great_expectations>=1,<2"
```

```python
import great_expectations as gx
import pandas as pd

df = pd.DataFrame({"order_id": [1, 2, 3], "amount": [10.0, 25.5, 99.0]})

context = gx.get_context()  # file-backed if a gx/ directory exists, otherwise in memory
batch_definition = (
    context.data_sources.add_pandas("local")
    .add_dataframe_asset(name="orders")
    .add_batch_definition_whole_dataframe("all_rows")
)

suite = context.suites.add(gx.ExpectationSuite(name="orders_suite"))
suite.add_expectation(gx.expectations.ExpectColumnValuesToNotBeNull(column="order_id"))
suite.add_expectation(gx.expectations.ExpectColumnValuesToBeUnique(column="order_id"))
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(column="amount", min_value=0, strict_min=True)
)

result = batch_definition.get_batch(batch_parameters={"dataframe": df}).validate(suite)
print(result.success)
```

For a warehouse table, use a SQL data source with a `ValidationDefinition` and a `Checkpoint`
that runs on every load with actions such as Slack alerts and Data Docs. See
`references/details.md`.

## Quick start: dbt model contract

An enforced contract makes `dbt run` fail when the model's columns or types differ from the
YAML, before any data is written. List every column the model returns, each with a
`data_type`. Constraints need a table or incremental materialization, because views can't
carry them.

```yaml
# models/marts/_marts__models.yml
models:
  - name: fct_orders
    config:
      materialized: table
      contract:
        enforced: true
    columns:
      - name: order_id
        data_type: bigint
        constraints:
          - type: not_null
          - type: primary_key
        data_tests:
          - unique
      - name: total_amount
        data_type: numeric(12,2)
      - name: created_at
        data_type: timestamp
```

A contract checks the schema's shape. Data tests check the values. Most warehouses don't
enforce `primary_key`, so keep the `unique` test.

## Best Practices

- **Validate sources before transforming them.** A bad row caught at ingestion costs less to
  fix than one found in a mart.
- **Add a test for every incident.** Each data bug you fix should leave a check behind.
- **Describe each check.** Say what the failure means and who owns the fix.
- **Version your contracts.** Bump the major version when a change can break consumers.
- **Test relationships, not just columns.** Orphaned foreign keys and broken totals between
  tables are common failures.
- **Don't ignore warnings.** A warning that keeps firing often comes before a hard failure.

## References

- `references/details.md`: full GX 1.x warehouse setup with a checkpoint and a CI gate, a
  complete dbt test suite, custom generic and singular tests, and an ODCS data contract with
  `datacontract-cli`.
