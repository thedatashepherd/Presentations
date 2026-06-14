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

# # Writing to the Lakehouse

# MARKDOWN ********************

# ## Overview
# - Files are stored in **OneLake** — Microsoft's unified storage layer
# - Two areas inside a Lakehouse:
#   - **Files/** — unmanaged files (CSV, Parquet, JSON, etc.)
#   - **Tables/** — managed Delta tables (queryable via SQL endpoint)
# - Writing to Tables creates Delta format automatically

# MARKDOWN ********************

# ## Setup — Create Schema and Load CSVs to Delta Tables
# This notebook uses the `writing_demo` schema to keep its tables isolated from other notebooks.
# Run these cells once before the rest of the demo.

# CELL ********************

# Create an isolated schema for this demo
spark.sql("CREATE SCHEMA IF NOT EXISTS writing_demo")
print("Schema ready: writing_demo")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql.functions import col

# Load sets.csv and save as a managed Delta table in writing_demo schema
(
    spark.read
    .format("csv")
    .option("header", "true")
    .load("Files/Legos/sets.csv")
    .withColumn("year", col("year").cast("int"))
    .withColumn("num_parts", col("num_parts").cast("int"))
    .write
    .mode("overwrite")
    .saveAsTable("writing_demo.sets")
)

print(f"sets table created: {spark.table('writing_demo.sets').count()} rows")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Load themes.csv and save as a managed Delta table in writing_demo schema
(
    spark.read
    .format("csv")
    .option("header", "true")
    .load("Files/Legos/themes.csv")
    .withColumn("id", col("id").cast("int"))
    .withColumn("parent_id", col("parent_id").cast("int"))
    .write
    .mode("overwrite")
    .saveAsTable("writing_demo.themes")
)

print(f"themes table created: {spark.table('writing_demo.themes').count()} rows")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 1. Load some data to work with

# CELL ********************

# Load the LEGO sets from the writing_demo schema
legosets = spark.table("writing_demo.sets")
display(legosets)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 2. Write to Files/ (unmanaged)

# MARKDOWN ********************

# ### Write as CSV

# CELL ********************

# Write DataFrame to CSV in the Files area
# 'overwrite' replaces the file if it already exists
(
    legosets
    .write
    .mode("overwrite")
    .option("header", "true")
    .csv("Files/Output/sets_export")
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### Write as Parquet
# - Parquet is a columnar format — more efficient for analytical queries
# - Smaller file size than CSV, faster reads

# CELL ********************

(
    legosets
    .write
    .mode("overwrite")
    .parquet("Files/Output/sets_parquet")
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 3. Write to Tables/ (managed Delta)

# MARKDOWN ********************

# ### saveAsTable — creates a managed Delta table
# - Shows up under **Tables** in the Lakehouse explorer
# - Queryable from SQL endpoint, Power BI, and other notebooks

# CELL ********************

# Write to a Delta table named 'sets_copy' in writing_demo schema
(
    legosets
    .write
    .mode("overwrite")
    .saveAsTable("writing_demo.sets_copy")
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Confirm it's there — read it back
df_check = spark.table("writing_demo.sets_copy")
df_check.count()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 4. Write Modes
# | Mode | Behavior |
# |------|----------|
# | `overwrite` | Replaces existing data |
# | `append` | Adds rows to existing data |
# | `ignore` | Does nothing if data exists |
# | `error` | Throws error if data exists (default) |

# MARKDOWN ********************

# ### Append example — add 2022+ sets to a separate table

# CELL ********************

from pyspark.sql.functions import col

# Filter to recent sets
recent_sets = legosets.filter(col("year") >= 2022)

# First write — creates the table
(
    recent_sets
    .write
    .mode("overwrite")
    .saveAsTable("writing_demo.recent_sets")
)

print(f"Initial row count: {spark.table('writing_demo.recent_sets').count()}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Append mode — adds rows without replacing
older_sets = legosets.filter(col("year") == 2021)

(
    older_sets
    .write
    .mode("append")
    .saveAsTable("writing_demo.recent_sets")
)

print(f"After append row count: {spark.table('writing_demo.recent_sets').count()}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 5. Partitioning
# - Splits the data into folders by a column value
# - Speeds up queries that filter on the partition column
# - Common to partition by date, year, or region

# CELL ********************

# Write partitioned by year
# Creates a subfolder for each year: year=1970/, year=1971/, etc.
(
    legosets
    .write
    .mode("overwrite")
    .partitionBy("year")
    .saveAsTable("writing_demo.sets_by_year")
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Spark uses partition pruning — only reads the 2022 folder
spark.table("writing_demo.sets_by_year").filter(col("year") == 2022).count()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 6. Upsert (Merge) with Delta Lake
# - **Merge** = Insert new rows + Update existing rows in one operation
# - Standard pattern for incremental loads

# CELL ********************

from delta.tables import DeltaTable

# Imagine this is your incoming batch of new/updated records
incoming = legosets.filter(col("year") >= 2020).limit(50)

# Reference the existing Delta table
target = DeltaTable.forName(spark, "writing_demo.sets_copy")

# Merge: update if set_num matches, insert if it doesn't
(
    target.alias("target")
    .merge(
        incoming.alias("source"),
        "target.set_num = source.set_num"
    )
    .whenMatchedUpdateAll()
    .whenNotMatchedInsertAll()
    .execute()
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 7. Delta Lake — Time Travel
# - Delta keeps a transaction log of every write
# - You can query any previous version

# CELL ********************

# See the history of the table
target = DeltaTable.forName(spark, "writing_demo.sets_copy")
target.history().select("version", "timestamp", "operation").show(truncate=False)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Read version 0 — the original write before the merge
df_v0 = spark.read.format("delta").option("versionAsOf", 0).table("writing_demo.sets_copy")
print(f"Version 0 row count: {df_v0.count()}")
print(f"Current row count:   {spark.table('writing_demo.sets_copy').count()}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
