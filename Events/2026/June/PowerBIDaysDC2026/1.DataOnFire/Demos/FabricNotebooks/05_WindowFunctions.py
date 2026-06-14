# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "a00e356e-9db3-407d-9821-84a5a281c008",
# META       "default_lakehouse_name": "lh_the_forge",
# META       "default_lakehouse_workspace_id": "0b035a83-b973-4c68-b788-96831f4aee2e",
# META       "known_lakehouses": [
# META         {
# META           "id": "a00e356e-9db3-407d-9821-84a5a281c008"
# META         }
# META       ]
# META     }
# META   }
# META }

# MARKDOWN ********************

# # Window Functions

# MARKDOWN ********************

# ## What is a Window Function?
# - Performs a calculation **across a set of rows** related to the current row
# - Unlike `groupBy`, the original rows are **not collapsed** — you keep every row
# - Think of it like: *"rank this row compared to others in the same group"*
# 
# ### The building block: `Window.partitionBy().orderBy()`
# - **`partitionBy`** — defines the group (like GROUP BY)
# - **`orderBy`** — defines the sort order within each group

# MARKDOWN ********************

# ## Setup — Create Schema and Load CSVs to Delta Tables
# This notebook uses the `window_demo` schema to keep its tables isolated from other notebooks.
# Run these cells once before the rest of the demo.

# CELL ********************

# Create an isolated schema for this demo
spark.sql("CREATE SCHEMA IF NOT EXISTS window_demo")
print("Schema ready: window_demo")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql.functions import col

# Load sets.csv and save as a managed Delta table in window_demo schema
(
    spark.read
    .format("csv")
    .option("header", "true")
    .load("Files/Legos/sets.csv")
    .withColumn("year", col("year").cast("int"))
    .withColumn("num_parts", col("num_parts").cast("int"))
    .write
    .mode("overwrite")
    .saveAsTable("window_demo.sets")
)

print(f"sets table created: {spark.table('window_demo.sets').count()} rows")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Load themes.csv and save as a managed Delta table in window_demo schema
(
    spark.read
    .format("csv")
    .option("header", "true")
    .load("Files/Legos/themes.csv")
    .withColumn("id", col("id").cast("int"))
    .withColumn("parent_id", col("parent_id").cast("int"))
    .write
    .mode("overwrite")
    .saveAsTable("window_demo.themes")
)

print(f"themes table created: {spark.table('window_demo.themes').count()} rows")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### Load Data

# CELL ********************

from pyspark.sql import Window
from pyspark.sql.functions import col, rank, dense_rank, row_number, lag, lead, sum, avg, count, ntile, first, last

# Load LEGO sets from the window_demo schema
legosets = spark.table("window_demo.sets")

display(legosets.limit(5))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 1. Ranking Functions
# | Function | Behavior with ties |
# |----------|--------------------|  
# | `rank()` | Leaves gaps after ties (1, 1, 3) |
# | `dense_rank()` | No gaps (1, 1, 2) |
# | `row_number()` | Always unique — ties broken arbitrarily |

# CELL ********************

# Rank sets within each theme by number of parts (largest first)
window_by_theme = Window.partitionBy("theme_id").orderBy(col("num_parts").desc())

ranked = (
    legosets
    .withColumn("rank",        rank().over(window_by_theme))
    .withColumn("dense_rank",  dense_rank().over(window_by_theme))
    .withColumn("row_number",  row_number().over(window_by_theme))
    .select("theme_id", "name", "num_parts", "rank", "dense_rank", "row_number")
)

display(ranked.filter(col("theme_id") == 158).orderBy("rank"))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### Top 1 per group — the classic use case
# Equivalent of SQL: `WHERE rank = 1`

# CELL ********************

# Get the largest set (by parts) in each theme
largest_per_theme = (
    legosets
    .withColumn("rank", rank().over(window_by_theme))
    .filter(col("rank") == 1)
    .select("theme_id", "set_num", "name", "num_parts")
    .orderBy(col("num_parts").desc())
)

display(largest_per_theme.limit(10))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 2. Lag and Lead
# - **`lag()`** — looks at the **previous** row's value
# - **`lead()`** — looks at the **next** row's value
# - Great for period-over-period comparisons

# CELL ********************

from pyspark.sql.functions import count as spark_count

# Count sets released per year
sets_per_year = (
    legosets
    .groupBy("year")
    .agg(spark_count("set_num").alias("set_count"))
    .orderBy("year")
)

display(sets_per_year)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql.functions import round as spark_round

# Compare each year to the previous year
window_by_year = Window.orderBy("year")

yoy = (
    sets_per_year
    .withColumn("prev_year_count", lag("set_count", 1).over(window_by_year))
    .withColumn("next_year_count", lead("set_count", 1).over(window_by_year))
    .withColumn(
        "yoy_change",
        spark_round((col("set_count") - col("prev_year_count")) / col("prev_year_count") * 100, 1)
    )
)

display(yoy.filter(col("year") >= 2010))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 3. Running / Cumulative Aggregates
# - Aggregate functions (`sum`, `avg`, `count`) can run over a window
# - **`rowsBetween`** controls the frame — which rows are included in the calculation
#   - `Window.unboundedPreceding` = from the very first row
#   - `Window.currentRow` = up to and including the current row

# CELL ********************

# Running total of sets released, ordered by year
running_window = (
    Window
    .orderBy("year")
    .rowsBetween(Window.unboundedPreceding, Window.currentRow)
)

running_total = (
    sets_per_year
    .withColumn("running_total", sum("set_count").over(running_window))
)

display(running_total.filter(col("year") >= 2010))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Rolling 3-year average
rolling_window = (
    Window
    .orderBy("year")
    .rowsBetween(-2, Window.currentRow)  # current row + 2 rows before
)

rolling_avg = (
    sets_per_year
    .withColumn("rolling_3yr_avg", spark_round(avg("set_count").over(rolling_window), 1))
)

display(rolling_avg.filter(col("year") >= 2010))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 4. ntile — Divide rows into equal buckets
# - `ntile(4)` = divide into quartiles
# - `ntile(10)` = deciles
# - Useful for segmentation (top 25%, bottom 25%, etc.)

# CELL ********************

# Assign each LEGO set to a quartile based on number of parts
# within its theme
quartile_window = Window.partitionBy("theme_id").orderBy("num_parts")

quartiles = (
    legosets
    .withColumn("parts_quartile", ntile(4).over(quartile_window))
    .select("theme_id", "name", "num_parts", "parts_quartile")
)

# Top-quartile sets (biggest builds) in theme 158
display(
    quartiles
    .filter((col("theme_id") == 158) & (col("parts_quartile") == 4))
    .orderBy(col("num_parts").desc())
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 5. Named Windows — reuse the same spec

# CELL ********************

# Define the window spec once and reuse it across multiple columns
theme_window = Window.partitionBy("theme_id").orderBy(col("num_parts").desc())

enriched = (
    legosets
    .withColumn("rank_in_theme",    rank().over(theme_window))
    .withColumn("avg_parts_theme",  spark_round(avg("num_parts").over(Window.partitionBy("theme_id")), 1))
    .withColumn("max_parts_theme",  spark_round(col("num_parts") / avg("num_parts").over(Window.partitionBy("theme_id")), 2))
    .select("theme_id", "name", "num_parts", "rank_in_theme", "avg_parts_theme", "max_parts_theme")
    .filter(col("rank_in_theme") <= 3)
    .orderBy("theme_id", "rank_in_theme")
)

display(enriched.limit(15))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 6. first() and last() — grab boundary values

# CELL ********************

# For each theme, show the first and most recent set released
theme_history_window = Window.partitionBy("theme_id").orderBy("year")
theme_history_window_desc = Window.partitionBy("theme_id").orderBy(col("year").desc())

first_last = (
    legosets
    .withColumn("first_year",   first("year").over(theme_history_window))
    .withColumn("latest_year",  first("year").over(theme_history_window_desc))
    .select("theme_id", "first_year", "latest_year")
    .dropDuplicates(["theme_id"])
    .withColumn("years_active", col("latest_year") - col("first_year"))
    .orderBy(col("years_active").desc())
)

display(first_last.limit(10))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
