# spark-optimization: detailed patterns

Examples use PySpark 4.2 and only set configuration that differs from the defaults.

## Reading the plan

```python
df.explain(mode="formatted")   # physical plan with numbered operators and their details
df.explain(mode="cost")        # adds the optimizer's size and row estimates where available
```

What to look for:

- `Exchange hashpartitioning(...)`: a shuffle. Each one is a stage boundary. Count them; two
  shuffles on the same key often mean a missing `repartition` reuse or an extra `groupBy`.
- `AdaptiveSparkPlan isFinalPlan=false`: AQE will re-plan at run time. The final plan, with the
  real join type and partition counts, is in the SQL tab of the Spark UI after the run.
- `PartitionFilters: [...]` on the scan: partition pruning worked. An empty list with a filter
  on the partition column means the filter wraps the column in a function or a cast.
- `PushedFilters: [...]`: filters the file reader applies (Parquet row-group skipping).

In the Spark UI, open the slowest stage and compare the median and max of task duration and
shuffle read size. A max several times the median is skew. Non-zero "Spill (Disk)" means the
partition did not fit in execution memory.

## Skew

AQE splits a skewed partition of a sort-merge join when it is more than
`skewedPartitionFactor` (5) times the median and over `skewedPartitionThresholdInBytes`
(256 MB). Lower those two settings if the UI still shows one long task:

```python
spark.conf.set("spark.sql.adaptive.skewJoin.skewedPartitionFactor", "3")
spark.conf.set("spark.sql.adaptive.skewJoin.skewedPartitionThresholdInBytes", "128MB")
```

AQE does not split skew in an aggregation. When one key holds most rows of a `groupBy`, or the
join is not a sort-merge join, salt the key:

```python
# jobs/salted_join.py
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder.appName("salted-join").getOrCreate()
SALTS = 16

events = spark.range(2_000_000).select(
    F.when(F.col("id") % 10 < 8, F.lit(0)).otherwise(F.col("id") % 1000).alias("customer_id"),
    F.col("id").alias("event_id"),
)
customers = spark.range(1000).select(F.col("id").alias("customer_id"), F.lit("x").alias("plan"))

salted_events = events.withColumn("salt", (F.rand(seed=7) * SALTS).cast("int"))
salted_customers = customers.crossJoin(spark.range(SALTS).withColumnRenamed("id", "salt"))

joined = salted_events.join(salted_customers, ["customer_id", "salt"]).drop("salt")
print(joined.count())  # same row count as the unsalted join
```

The small side grows by a factor of `SALTS`, so salt only the keys that are skewed when that
side is large: split the hot keys out, salt them, and union the result with a plain join of the
rest.

## Joins

| Physical join | When Spark picks it | Notes |
| --- | --- | --- |
| `BroadcastHashJoin` | one side is under `autoBroadcastJoinThreshold` (10 MB) by estimate, or AQE sees it is small at run time | no shuffle of the large side; the small side must fit in driver and executor memory |
| `SortMergeJoin` | default for two large sides | shuffles and sorts both sides |
| `ShuffledHashJoin` | with the `SHUFFLE_HASH` hint, or when AQE converts a sort-merge join after you set `spark.sql.adaptive.maxShuffledHashJoinLocalMapThreshold` (0, off, by default) | skips the sort; the build side of each partition must fit in memory |

Force a strategy with a hint when the estimate is wrong:

```python
large.join(small.hint("broadcast"), "key")
large.join(other.hint("shuffle_hash"), "key")
```

```sql
SELECT /*+ BROADCAST(c) */ * FROM orders o JOIN customers c ON o.customer_id = c.customer_id
```

Bucketed Hive tables avoid the shuffle when both sides use the same bucket column and count.
For Iceberg and other DataSource V2 tables, storage-partitioned join does the same from the
table's partitioning (`spark.sql.sources.v2.bucketing.enabled`, on by default).

## Partitions and files

- AQE starts from `spark.sql.shuffle.partitions` and coalesces toward
  `spark.sql.adaptive.advisoryPartitionSizeInBytes` (64 MB). For very large shuffles, raise
  `spark.sql.shuffle.partitions` so that AQE has room to coalesce, rather than lowering it.
- `coalesce(n)` merges partitions without a shuffle but also lowers the parallelism of the work
  before it. Use `repartition(n)` when the upstream work needs its parallelism.
- Partition tables on disk by a low-cardinality column that queries filter on, usually a date.
  Partitioning by a high-cardinality column produces many small files.
- Write fewer, larger files: `df.repartition("dt").write.partitionBy("dt")` gives one file per
  date, and `spark.sql.files.maxRecordsPerFile` caps the size.

```python
# jobs/write_partitioned.py
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder.appName("write-partitioned").getOrCreate()

events = spark.range(100_000).select(
    F.col("id").alias("event_id"),
    F.date_add(F.lit("2026-01-01"), (F.col("id") % 7).cast("int")).alias("dt"),
)

out = "/tmp/spark-optimization/events"
events.repartition("dt").write.mode("overwrite").partitionBy("dt").parquet(out)

day = spark.read.parquet(out).filter(F.col("dt") == "2026-01-03")
day.explain(mode="formatted")  # the scan lists PartitionFilters on dt
print(day.count())
```

## Caching

Cache a DataFrame only when more than one action reads it and recomputing it is expensive.
`cache()` uses `MEMORY_AND_DISK_DESER` for DataFrames. The cache is filled by the first action,
so do not add a `count()` just to fill it.

```python
active = df.filter(F.col("status") == "active").cache()
by_region = active.groupBy("region").count().collect()
by_plan = active.groupBy("plan").count().collect()
active.unpersist()
```

`checkpoint()` and `localCheckpoint()` return a new DataFrame with the lineage cut. Use the
returned value: `df = df.checkpoint()`. Use them for iterative jobs whose plan grows every loop.

## Memory

- `spark.executor.memory` is the JVM heap. Of it, 300 MB is reserved and
  `spark.memory.fraction` (0.6) of the rest is shared by execution and storage.
- `spark.executor.memoryOverhead` (default 10% of executor memory, at least 384 MB) covers
  off-heap use: Python workers, Arrow buffers and native libraries. Raise it when YARN or
  Kubernetes kills executors for exceeding the container limit while the heap looks fine.
- Spill with long GC means partitions are too large for the memory per core. Either lower the
  partition size or give each core more memory (fewer cores per executor).
- Five or fewer cores per executor is a common starting point on YARN and Kubernetes. Measure
  before and after any change.

## Python UDFs

Built-in functions run in the JVM and are optimized by Catalyst. A Python `@udf` sends every row
to a Python worker. When no built-in function fits, use an Arrow-based `@pandas_udf`, which
moves data in batches:

```python
# jobs/pandas_udf.py
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder.appName("pandas-udf").getOrCreate()


@F.pandas_udf("double")
def with_tax(amount: pd.Series) -> pd.Series:
    return amount * 1.2


df = spark.range(10).select(F.col("id").cast("double").alias("amount"))
df.select(with_tax("amount").alias("gross")).show()
```

Spark 4 also supports Arrow-optimized regular UDFs (`@udf(useArrow=True)`) and Python data
source and UDTF APIs.

## Table maintenance

Small files and stale layout slow every read of a table. Run compaction on a schedule:

- Delta Lake: `OPTIMIZE <table>`; `OPTIMIZE <table> ZORDER BY (col)` for older tables, or
  liquid clustering (`CLUSTER BY`) for new ones; `VACUUM` to delete unreferenced files after the
  retention period.
- Iceberg: the `rewrite_data_files` and `expire_snapshots` procedures
  (`CALL catalog.system.rewrite_data_files('db.table')`).

Check the Delta or Iceberg version in use before copying table properties; option names differ
between open-source releases and Databricks.

## Settings worth changing

Only set a value when a measurement shows the default is wrong for this job:

| Setting | Default | Change when |
| --- | --- | --- |
| `spark.sql.autoBroadcastJoinThreshold` | 10 MB | a dimension table just over 10 MB is joined often and fits in memory |
| `spark.sql.shuffle.partitions` | 200 | shuffles are hundreds of GB; raise so AQE can coalesce |
| `spark.sql.adaptive.advisoryPartitionSizeInBytes` | 64 MB | tasks spill (lower) or there are many tiny tasks (raise) |
| `spark.sql.files.maxPartitionBytes` | 128 MB | the scan stage spills or has too few tasks |
| `spark.executor.memoryOverhead` | 10%, min 384 MB | containers are killed for exceeding memory with PySpark or Arrow |
