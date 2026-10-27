# dbt-transformation-patterns: detailed patterns

The files below form one small project: Stripe customers and payments, staged, joined and
published as `dim_customers` and an incremental `fct_payments`. The YAML uses the dbt 1.10+
forms, which parse without deprecation warnings on dbt Core 1.12 and are what dbt v2 requires.

## Sources and freshness

```yaml
# models/staging/stripe/_stripe__sources.yml
sources:
  - name: stripe
    description: Raw Stripe data loaded by Fivetran.
    schema: stripe
    config:
      loaded_at_field: _loaded_at
      freshness:
        warn_after: { count: 12, period: hour }
        error_after: { count: 24, period: hour }
    tables:
      - name: customers
        columns:
          - name: id
            data_tests: [unique, not_null]
      - name: payments
        columns:
          - name: id
            data_tests: [unique, not_null]
```

`dbt source freshness` compares `max(_loaded_at)` with the current time and fails past
`error_after`. Run it before `dbt build` in the scheduled job.

## Staging

Rename to the project's conventions, cast types and convert units. Nothing else. The payments
staging model is in the SKILL.md quick start.

```sql
-- models/staging/stripe/stg_stripe__customers.sql
with source as (
    select * from {{ source('stripe', 'customers') }}
)

select
    id as customer_id,
    lower(email) as email,
    name as customer_name,
    cast(created as timestamp) as created_at,
    _loaded_at
from source
```

```yaml
# models/staging/stripe/_stripe__models.yml
models:
  - name: stg_stripe__customers
    columns:
      - name: customer_id
        data_tests: [unique, not_null]
  - name: stg_stripe__payments
    columns:
      - name: payment_id
        data_tests: [unique, not_null]
      - name: customer_id
        data_tests:
          - not_null
          - relationships:
              arguments:
                to: ref('stg_stripe__customers')
                field: customer_id
      - name: payment_status
        data_tests:
          - accepted_values:
              arguments:
                values: ["succeeded", "failed", "refunded"]
```

## Intermediate

```sql
-- models/intermediate/int_customer_payments.sql
with payments as (
    select * from {{ ref('stg_stripe__payments') }}
),

customers as (
    select * from {{ ref('stg_stripe__customers') }}
),

per_customer as (
    select
        customer_id,
        count(*) as payment_count,
        sum(case when payment_status = 'succeeded' then amount else 0 end) as lifetime_value,
        min(created_at) as first_payment_at
    from payments
    group by customer_id
)

select
    customers.customer_id,
    customers.email,
    customers.created_at,
    coalesce(per_customer.payment_count, 0) as payment_count,
    coalesce(per_customer.lifetime_value, 0) as lifetime_value,
    per_customer.first_payment_at
from customers
left join per_customer on customers.customer_id = per_customer.customer_id
```

## Marts

```sql
-- models/marts/dim_customers.sql
select
    customer_id,
    email,
    created_at,
    payment_count,
    lifetime_value,
    first_payment_at,
    case
        when lifetime_value >= 1000 then 'high'
        when lifetime_value >= 100 then 'medium'
        else 'low'
    end as customer_tier
from {{ ref('int_customer_payments') }}
```

An incremental fact reprocesses the last three days on every run so that late-arriving and
updated rows are merged instead of skipped. `dbt.dateadd` compiles to each warehouse's own
syntax.

```sql
-- models/marts/fct_payments.sql
{{
    config(
        materialized='incremental',
        unique_key='payment_id',
        incremental_strategy='delete+insert',
        on_schema_change='append_new_columns'
    )
}}

select
    payment_id,
    customer_id,
    amount,
    payment_status,
    created_at,
    _loaded_at
from {{ ref('stg_stripe__payments') }}

{% if is_incremental() %}
where _loaded_at >= (
    select {{ dbt.dateadd('day', -3, 'max(_loaded_at)') }} from {{ this }}
)
{% endif %}
```

```yaml
# models/marts/_marts__models.yml
models:
  - name: dim_customers
    description: One row per Stripe customer.
    columns:
      - name: customer_id
        data_tests: [unique, not_null]
      - name: customer_tier
        data_tests:
          - accepted_values:
              arguments:
                values: ["high", "medium", "low"]
      - name: lifetime_value
        data_tests:
          - dbt_utils.expression_is_true:
              arguments:
                expression: ">= 0"

  - name: fct_payments
    description: One row per payment attempt.
    columns:
      - name: payment_id
        data_tests: [unique, not_null]
      - name: customer_id
        data_tests:
          - relationships:
              arguments:
                to: ref('dim_customers')
                field: customer_id
              config:
                severity: warn

unit_tests:
  - name: dim_customers_assigns_tiers
    model: dim_customers
    given:
      - input: ref('int_customer_payments')
        rows:
          - { customer_id: 1, lifetime_value: 1500 }
          - { customer_id: 2, lifetime_value: 100 }
          - { customer_id: 3, lifetime_value: 99.99 }
    expect:
      rows:
        - { customer_id: 1, customer_tier: high }
        - { customer_id: 2, customer_tier: medium }
        - { customer_id: 3, customer_tier: low }
```

`dbt_utils` comes from `packages.yml`; run `dbt deps` after adding it:

```yaml
# packages.yml
packages:
  - package: dbt-labs/dbt_utils
    version: [">=1.3.0", "<2.0.0"]
```

Unit tests run before the model is built in `dbt build`, using only the rows you give. List only
the columns the logic reads; the rest are null.

## Incremental strategies

| Strategy | What it does | Use when |
| --- | --- | --- |
| `append` | inserts new rows | rows never change and duplicates can't arrive |
| `merge` | updates matching `unique_key` rows, inserts the rest | rows are updated after they land |
| `delete+insert` | deletes matching keys, then inserts | the adapter has no `merge`, or merge is slow on large batches |
| `insert_overwrite` | replaces whole partitions | BigQuery or Spark tables partitioned by date |
| `microbatch` | runs one query per time batch on `event_time` | large event tables; dbt 1.9+ |

Support and defaults vary by adapter, so set the strategy in the config. Check the adapter's
documentation page before using `merge_update_columns`, `incremental_predicates` or
`insert_overwrite`.

Microbatch splits the work into batches by an `event_time` column and can rerun one batch
(`dbt run --event-time-start ... --event-time-end ...`). Set `event_time` on the upstream model
too, so dbt filters it to the batch:

```sql
-- models/marts/fct_payment_events.sql
{{
    config(
        materialized='incremental',
        incremental_strategy='microbatch',
        event_time='created_at',
        batch_size='day',
        begin='2026-01-01',
        lookback=3
    )
}}

select payment_id, customer_id, amount, payment_status, created_at
from {{ ref('stg_stripe__payments') }}
```

```yaml
# in models/staging/stripe/_stripe__models.yml
  - name: stg_stripe__payments
    config:
      event_time: created_at
```

## Macros

```sql
-- macros/cents_to_dollars.sql
{% macro cents_to_dollars(column_name, scale=2) %}
    cast({{ column_name }} as numeric(18, {{ scale }})) / 100
{% endmacro %}
```

```sql
-- macros/limit_in_dev.sql
{% macro limit_in_dev(column_name, days=3) %}
    {% if target.name == 'dev' %}
        where {{ column_name }} >= {{ dbt.dateadd('day', -days, dbt.current_timestamp()) }}
    {% endif %}
{% endmacro %}
```

A `generate_schema_name` override controls which schema each model lands in. dbt's default
already prefixes a custom schema with the target schema (`<target>_<custom>`); override it only
when production should use the bare custom name.

## Commands

```bash
dbt deps                                   # install packages
dbt parse                                  # parse and print deprecations
dbt source freshness                       # check source freshness
dbt build --select stg_stripe__payments+   # build and test a model and everything downstream
dbt build --select state:modified+ --defer --state prod-artifacts/   # CI: only changed models
dbt build --select fct_payments --full-refresh   # rebuild an incremental model from scratch
dbt test --select test_type:unit           # unit tests only
dbt ls --select tag:daily                  # list matching nodes
dbt docs generate
```
