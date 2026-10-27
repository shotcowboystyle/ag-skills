---
name: spark-optimization
description: Diagnose and fix a slow or failing Apache Spark job (PySpark, Spark SQL, Spark 3.x and 4.x) from the Spark UI and query plan, covering shuffles, skew, join strategy, spills, small files, partition sizing and executor memory. Use when a Spark or Databricks job is slow, costly or dies with out-of-memory errors. For scheduling the job use airflow-dag-patterns; for SQL models in a dbt project use dbt-transformation-patterns.
last_verified: 2026-10-27
---

# Spark Optimization

Find the stage that costs the most, name the cause from evidence, change one thing, and
measure again. Examples are checked against PySpark 4.2.

## Procedure

1. **Get the facts.** Record the Spark version (`spark.version`), the platform (open-source,
   Databricks, EMR, Dataproc), the cluster size, the input size, and the current runtime of
   the job. Without a baseline runtime, write "needs measurement" rather than predicting a
   speedup.
2. **Find the slowest stage** in the Spark UI (or the History Server for a finished job). For
   that stage, read the task-duration percentiles, shuffle read and write, spill (memory and
   disk), GC time and input size.
3. **Read the plan.** Run `df.explain(mode="formatted")` and find each `Exchange` (a shuffle),
   the join type (`BroadcastHashJoin`, `SortMergeJoin`, `ShuffledHashJoin`), and whether the
   scan shows `PartitionFilters` and `PushedFilters`.
4. **Name the cause** from the table below and apply its fix. Change one thing per run.
5. **Re-run on the same input** and compare runtime and the stage metrics from step 2. Keep the
   change only if it helped.
6. **Stop when** the job meets its target, or the slowest stage is limited by input I/O with no
   spill and no skew. Report what is left.

Report back with the baseline and new runtime, each change with the metric that justified it,
and the remaining bottleneck.

## Symptom to fix

| Evidence | Cause | Fix |
| --- | --- | --- |
| Max task time far above the median in one stage | Skewed key | Let AQE split it (on by default); if one key dominates, salt it or handle it separately |
| `SortMergeJoin` where one side is small after filtering | Missed broadcast | `F.broadcast(small_df)`, or raise `spark.sql.autoBroadcastJoinThreshold` |
| Large spill to disk, long GC | Partitions too big for executor memory | Lower `spark.sql.adaptive.advisoryPartitionSizeInBytes` or raise executor memory |
| Thousands of tasks of a few MB each | Too many small partitions or files | Compact the input; `coalesce` before writing |
| Scan reads every file despite a filter | Filter not pushed down | Filter on the partition column, without wrapping it in a function or a UDF |
| Python UDF stage is slow | Row-at-a-time Python | Built-in functions first, then Arrow-based `@pandas_udf` |
| The same expensive DataFrame recomputed by several actions | No reuse | `cache()` it once, `unpersist()` when done |
| Driver out of memory | `collect()`/`toPandas()` on large data, or a large broadcast | Write the result out instead; check broadcast sizes |

## Defaults you don't need to set

These are already on in Spark 3.2 and later. Setting them again does nothing; note it in a
review rather than adding it:

- `spark.sql.adaptive.enabled=true` and `spark.sql.adaptive.coalescePartitions.enabled=true`
- `spark.sql.adaptive.skewJoin.enabled=true` (a partition is skewed when it is over 5x the
  median and over 256 MB)
- `spark.sql.adaptive.localShuffleReader.enabled=true`
- `spark.sql.files.maxPartitionBytes=128MB`, `spark.sql.shuffle.partitions=200` (AQE coalesces
  shuffle partitions down from this number)
- `spark.memory.fraction=0.6`, `spark.memory.storageFraction=0.5`, `spark.shuffle.compress=true`

`spark.serializer=KryoSerializer` doesn't speed up DataFrame or SQL jobs: they serialize rows
with Tungsten's binary format. Kryo only affects RDD code and serialized RDD caching.
`spark.sql.shuffle.partitions=auto` is a Databricks setting; open-source Spark rejects it.

## Quick Start

```python
# jobs/inspect_join.py
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder.appName("inspect-join").getOrCreate()

orders = spark.range(1_000_000).select(
    F.col("id").alias("order_id"),
    (F.col("id") % 1000).alias("customer_id"),
    (F.rand(seed=1) * 100).alias("amount"),
)
customers = spark.range(1000).select(
    F.col("id").alias("customer_id"),
    F.when(F.col("id") % 2 == 0, "eu").otherwise("us").alias("region"),
)

totals = (
    orders.join(F.broadcast(customers), "customer_id")
    .groupBy("region")
    .agg(F.sum("amount").alias("revenue"))
)
totals.explain(mode="formatted")  # expect BroadcastHashJoin and one Exchange for the groupBy
totals.show()
```

## References

- `references/details.md`: reading the plan and the UI, skew and salting, join strategies and
  hints, partition sizing and file layout, caching, memory settings, Python UDFs, and Delta or
  Iceberg table maintenance.
