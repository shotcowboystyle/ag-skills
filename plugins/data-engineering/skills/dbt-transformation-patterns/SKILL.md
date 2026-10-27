---
name: dbt-transformation-patterns
description: Write and test dbt models in SQL, with sources and freshness, staging, intermediate and mart layers, incremental and microbatch models, data tests, unit tests and macros, in YAML that is valid for dbt Core 1.10+ and dbt v2. Use when the task is a dbt project or a SQL transformation that runs inside the warehouse. For scheduling dbt runs use airflow-dag-patterns; for Great Expectations or data contracts use data-quality-frameworks.
last_verified: 2026-10-27
---

# dbt Transformation Patterns

Build dbt models that are layered, tested and cheap to rebuild. Examples are checked against
dbt Core 1.12 with dbt-duckdb.

## Procedure

1. **Check the version.** Run `dbt --version`, then `dbt parse`. Fix every deprecation warning
   it prints: dbt v2 turns them into errors. The YAML here uses the 1.10+ forms: `data_tests:`
   instead of `tests:`, generic test arguments under `arguments:`, and `freshness`, `meta` and
   `tags` under `config:`. Use `--select`; `--models` and `-m` are gone in v2.
2. **Declare every raw table as a source** with a `loaded_at_field` and `freshness`. Models
   read raw data only through `{{ source() }}`, and everything else through `{{ ref() }}`.
3. **Staging:** one `stg_<source>__<table>` model per source table. Rename, cast, convert units
   and nothing else: no joins, no filters that drop business rows. Materialize as views.
4. **Intermediate:** `int_` models hold joins and business logic shared by more than one mart.
   Skip the layer when a mart is the only consumer.
5. **Marts:** `fct_` tables hold one row per event and `dim_` tables one row per entity. State
   the grain in the model description and test it with `unique` on the key.
6. **Go incremental only when a full rebuild is too slow or costly**, measured on the real
   table. Pick a `unique_key`, reprocess a lookback window for late rows, and set
   `incremental_strategy` explicitly, since the default differs by adapter. For large event
   tables on dbt 1.9+, prefer `incremental_strategy='microbatch'`.
7. **Test every model:** `unique` and `not_null` on its key, `relationships` on foreign keys,
   `accepted_values` on status columns. Add a unit test for any CASE, window or date logic.
8. **Build and verify:** run `dbt build --select <model>+` in a dev target, then rebuild an
   incremental model with `--full-refresh` and compare row counts with the incremental result.
9. **Stop when** `dbt build` passes with no warnings, every model has a key test, and source
   freshness passes with `dbt source freshness`.

Report back with the models added or changed and their materialization, the tests on each, and
the build commands with their results.

## Layers

dbt's own convention is staging, intermediate and marts, a split by purpose. Medallion
(bronze, silver, gold) is a Databricks lakehouse convention for storage zones, and the two
don't map one to one: a raw source loaded by Fivetran is closest to bronze, and staging models
are views over it, not a cleaned copy. Name layers the way the project already does and don't
relabel one as the other.

```
sources (raw, loaded by EL tools)
  └─ staging/       stg_stripe__payments       view, 1:1 with a source table
       └─ intermediate/  int_customer_payments  joins and shared logic
            └─ marts/    fct_payments, dim_customers   tables for BI and consumers
```

## Quick Start

```yaml
# dbt_project.yml
name: analytics
version: "1.0.0"
profile: analytics

models:
  analytics:
    staging:
      +materialized: view
    intermediate:
      +materialized: view
    marts:
      +materialized: table
```

```
models/
├── staging/stripe/
│   ├── _stripe__sources.yml
│   ├── _stripe__models.yml
│   ├── stg_stripe__customers.sql
│   └── stg_stripe__payments.sql
├── intermediate/
│   └── int_customer_payments.sql
└── marts/
    ├── _marts__models.yml
    ├── dim_customers.sql
    └── fct_payments.sql
```

```sql
-- models/staging/stripe/stg_stripe__payments.sql
with source as (
    select * from {{ source('stripe', 'payments') }}
)

select
    id as payment_id,
    customer_id,
    cast(amount as numeric(18, 2)) / 100 as amount,
    status as payment_status,
    cast(created as timestamp) as created_at,
    _loaded_at
from source
```

## Best practices

- **One source of truth per concept.** If two marts compute revenue, move the logic into one
  intermediate model.
- **Keep business logic out of staging.** Staging that filters or joins hides data from every
  downstream model.
- **Use `{{ var() }}` or the run's context for dates**, never a hardcoded date in a model.
- **Limit dev builds**, for example with a `target.name == 'dev'` filter on large sources.
- **Don't test in production.** Build in a dev schema and use `--defer --state` to read
  unchanged parents from production.

## References

- `references/details.md`: sources with freshness, the staging, intermediate and mart models of
  the example project, tests and unit tests in 1.10+ YAML, macros, incremental strategies
  and microbatch, and the command reference.
