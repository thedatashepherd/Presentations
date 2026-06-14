# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "jupyter",
# META     "jupyter_kernel_name": "python3.12"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "e4e23765-a799-4c3c-a9ef-05c053cd6611",
# META       "default_lakehouse_name": "lh_duck_pond",
# META       "default_lakehouse_workspace_id": "cdef1857-04ff-41af-bd33-a36bf6a59d9e",
# META       "known_lakehouses": [
# META         {
# META           "id": "e4e23765-a799-4c3c-a9ef-05c053cd6611"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

# MAGIC %%configure -f
# MAGIC {
# MAGIC     "vCores": 2
# MAGIC }

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

# Uncomment to install or upgrade DuckDB
# %pip install duckdb -U

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

import pandas as pd
# Load data into pandas DataFrame from "/lakehouse/default/Files/flights/flights_2023.csv"
df = pd.read_csv("/lakehouse/default/Files/flights/flights_2023.csv")
display(df)


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

import duckdb

duckdb.sql("SELECT * FROM '/lakehouse/default/Files/flights/flights_2023.csv'")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

import duckdb

df = duckdb.sql("SELECT * FROM '/lakehouse/default/Files/flights/flights_2023.csv'").df()
display(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }
