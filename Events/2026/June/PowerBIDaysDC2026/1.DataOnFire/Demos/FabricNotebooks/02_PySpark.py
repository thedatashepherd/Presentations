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

# # PySpark


# MARKDOWN ********************

# ## 0. Calling another notebook with `%run`
# Fabric lets you run one notebook from inside another using `%run`.
# This is great for **setup notebooks** — connection info, shared imports, helper functions.
# Instead of copying the same setup code into every notebook, put it in one place and call it.
# > Real-world use: during demo prep I kept losing my Spark session.
# > I moved all setup into `00_Setup_Fresh` so I could re-run it in one cell and pick up where I left off.

# CELL ********************

%run 00_Setup_Fresh

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 1. Different environment — different packages
# We're on Spark compute now — a completely separate environment from the pure Python notebook.
# Let's see what's installed here.

# CELL ********************

%pip list

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

%pip show duckdb

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### Where'd my DuckDB go?
# 
# Pure Python notebooks ship with DuckDB and Polars **preinstalled by default** — no `%pip install` needed.
# 
# PySpark notebooks run on different compute with a different set of defaults. DuckDB isn't here.
# 
# The two environments are completely separate — different machines, different packages.
# 
# With pandas we can display the full package list as a DataFrame — and easily filter or limit it.

# CELL ********************

from importlib.metadata import distributions
import pandas as pd

packages = [(dist.metadata['Name'], dist.version) for dist in distributions()]
df = pd.DataFrame(packages, columns=['Package', 'Version'])
display(df.sort_values('Package').head(10))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 2. How to get data
# - ### Spark read from Files (CSV, Parquet, Delta)
# - ### Pandas read from Files (great for small lookups)
# - ### Wildcard — load multiple files at once
# - ### Drag and drop (Files, Tables)
# # 

# CELL ********************

# Option 1 — Spark reads big CSVs natively (this file is 500 MB+)

flights = spark.read.format("csv").option("header", "true").option("inferSchema", "true").load("Files/flights/flights_2022.csv")
display(flights.limit(10))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Option 2 — pandas for small lookup files

import pandas as pd
airlines_pd = pd.read_csv("/lakehouse/default/Files/flights/airlines.csv")
display(airlines_pd)


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Option 3 — wildcard loads all years at once
all_flights = spark.read.format("csv").option("header", "true").option("inferSchema", "true").load("Files/flights/flights_*.csv")
display(all_flights.limit(10))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### Magic Commands
# ### Set language at the cell level

# CELL ********************

# MAGIC %%sql
# MAGIC 
# MAGIC SELECT Reporting_Airline, COUNT(*) AS FlightCount
# MAGIC FROM lh_the_forge.flights.flights_2022
# MAGIC GROUP BY Reporting_Airline
# MAGIC ORDER BY FlightCount DESC
# MAGIC LIMIT 10

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 3. DataFrames — what type are you working with?
# In a PySpark notebook there are three DataFrame flavors.
# They look similar but behave differently — `type()` is your quick way to check which one you have.

# CELL ********************

# 1. Regular pandas — single node, everything from the Python Basics section
import pandas as pd

pandas_df = pd.read_csv("/lakehouse/default/Files/flights/airlines.csv")
type(pandas_df)  # pandas.core.frame.DataFrame

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# 2. PySpark pandas — pandas API, distributed under the hood
import warnings
import os

os.environ["PYARROW_IGNORE_TIMEZONE"] = "1"
warnings.filterwarnings("ignore", category=UserWarning, module="pyspark.pandas")
warnings.filterwarnings("ignore", "If `index_col` is not specified")
import pyspark.pandas as ps

spark_pandas_df = ps.read_csv("Files/flights/airlines.csv")
type(spark_pandas_df)  # pyspark.pandas.frame.DataFrame

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# 3. Native Spark DataFrame — fully distributed, the main focus from here on
spark_df = spark.read.format("csv").option("header", "true").option("inferSchema", "true").load("Files/flights/flights_2022.csv")
type(spark_df)  # pyspark.sql.dataframe.DataFrame

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Native Spark is our focus from here on
flights = spark.read.format("csv").option("header", "true").option("inferSchema", "true").load("Files/flights/flights_2022.csv")
display(flights.limit(5))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 4. Data Wrangler
# 
# > Launch from the cell toolbar → **Data Wrangler**

# MARKDOWN ********************

# ### Code Generated from Data Wrangler (Magic of TV)

# CELL ********************

# Code generated by Data Wrangler for pandas DataFrame

def clean_data(wrangler_sample_df):
    # Drop columns: 'Age', 'SibSp' and 5 other columns
    wrangler_sample_df = wrangler_sample_df.drop(columns=['Age', 'SibSp', 'Parch', 'Ticket', 'Fare', 'Cabin', 'Embarked'])
    # Performed 1 aggregation grouped on columns: 'Pclass', 'Survived'
    wrangler_sample_df = wrangler_sample_df.groupby(['Pclass', 'Survived']).agg(PassengerId_count=('PassengerId', 'count')).reset_index()
    # Derive column 'IsSurvived' from column: 'Survived'
    def IsSurvived(Survived):
        """
        Transform based on the following examples:
           Survived    Output
        1: "0"      => "Did Not Survived"
        2: "1"      => "Survived"
        3: "1"      => "Survived"
        4: "1"      => "Survived"
        """
        if Survived == "1":
            return "Survived"
        if Survived == "0":
            return "Did Not Survived"
        return None
    wrangler_sample_df.insert(2, "IsSurvived", wrangler_sample_df.apply(lambda row : IsSurvived(row["Survived"]), axis=1))
    return wrangler_sample_df

wrangler_sample_df_clean = clean_data(wrangler_sample_df.copy())
display(wrangler_sample_df_clean)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### Does the Titanic data tell us the answer?
# 
# ### Let's ask the data a question everyone already thinks they know the answer to...

# CELL ********************

from IPython.display import Image
from IPython.display import display as ipython_display

ipython_display(Image(filename="/lakehouse/default/Files/demo_assets/real_question.png", width=800))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark",
# META   "frozen": true,
# META   "editable": false
# META }

# MARKDOWN ********************

# ## 5. Joining Datasets
# `.show()` prints plain text — fast for quick checks.

# CELL ********************

flights = spark.read.format("csv").option("header", "true").option("inferSchema", "true").load("Files/flights/flights_2022.csv")
airlines = spark.read.format("csv").option("header", "true").load("Files/flights/airlines.csv")

# show() — plain text output
(
    flights
    .join(airlines, flights.Reporting_Airline == airlines.IATA_CODE, how="left")
    .show(8)
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### Join with renaming
# Same join — readable airline name added, duplicate key dropped.  
# And we switch to `display()` for a proper table. 

# CELL ********************

from pyspark.sql.functions import col

display(
    flights
    .join(airlines, flights.Reporting_Airline == airlines.IATA_CODE, how="left")
    .select(
        flights["*"],
        airlines.AIRLINE.alias("Airline Name")
    )
    .drop("IATA_CODE")
    .limit(8)
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 6. GroupBy & Aggregation

# CELL ********************

from pyspark.sql.functions import count, sum as spark_sum

display(
    flights
    .groupBy("Reporting_Airline")
    .agg(
        count("FlightDate").alias("Total Flights"),
        spark_sum("Cancelled").alias("Cancelled Flights")
    )
    .orderBy("Cancelled Flights", ascending=False)
    .limit(10)
)


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### Alias example

# CELL ********************

from pyspark.sql.functions import col

(
    airlines
    .select(col("IATA_CODE"), col("AIRLINE").alias("Airline Name"))
    .show(10)
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 7. Actions & Transforms

# CELL ********************

flights.count()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql.functions import col

cancelled_dc = (
    flights
    .filter(
        (col("Cancelled") == 1.0) &
        (col("Origin").isin("DCA", "IAD", "BWI"))
    )
)
display(cancelled_dc)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### Select — backslash chaining style
# Covered in the Python Basics notebook — works the same way in PySpark.

# CELL ********************

key_cols =\
    flights\
    .select(flights.FlightDate, flights.Reporting_Airline, flights.Origin, flights.Dest, flights.DepDelay)\
    .limit(5)

display(key_cols)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 8. Lazy Evaluation
# Spark doesn't execute transformations immediately — it waits until an **action** is called.
# Actions include: `show()`, `display()`, `count()`, `collect()`, `write`.


# MARKDOWN ********************

# ### Action will "execute" the code
# Displaying the data is one of those actions.
# **Two Ways to display**
# - `show()` method — also `show(5, truncate=25)`
# - `display()` function

# MARKDOWN ********************

# ### Lazy in action — no data yet
# 
# Just referencing the DataFrame returns schema info, not rows.  
# Spark hasn't executed anything — there's no action.

# CELL ********************

# Only return info about dataframe — notice no data, just schema info

flights

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

display(flights.limit(5))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### Select — multiple ways to refer to columns
# - `flights.select(flights.Origin)`
# - `flights.select(flights["Origin"])`
# - `flights.select("Origin")`
# - `flights.select(col("Origin"))` — requires `from pyspark.sql.functions import col`

# CELL ********************

from pyspark.sql.functions import col

# Four ways — all return the same result
flights.select(flights.Origin)
flights.select(flights["Origin"])
flights.select("Origin")
flights.select(col("Origin"))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql.functions import col

# Four ways — all return the same result
# flights.select(flights.Origin)
# flights.select(flights["Origin"])
# flights.select("Origin")
display(flights.select(col("Origin")).limit(5))  # action — this one runs

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 9. Add to a Pipeline
# 
# Notebooks are not just for interactive work.
# 
# In Fabric, you can schedule a notebook or add it to a Data Pipeline — the same logic runs as part of a repeatable workflow.
# 
# > **Fabric UI:** Pipeline → Add activity → Notebook

# MARKDOWN ********************

# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 

