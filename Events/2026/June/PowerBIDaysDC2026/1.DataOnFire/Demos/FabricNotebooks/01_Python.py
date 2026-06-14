# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "jupyter",
# META     "jupyter_kernel_name": "python3.12"
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
# META     },
# META     "warehouse": {
# META       "known_warehouses": []
# META     }
# META   }
# META }

# MARKDOWN ********************

# # Intro to Python

# MARKDOWN ********************

# ### Start a small Python session
# 
# Fabric pure Python notebooks run on VM-backed compute.
# 
# For this demo, I’m requesting a small 2 vCore session so the notebook starts quickly and we can focus on the workflow instead of waiting on compute.
# 
# For larger datasets or heavier Python workloads, you can choose more vCores.
# 
# > Python notebooks scale up by choosing a VM size.  
# > PySpark notebooks scale out by using Spark compute.

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

# MARKDOWN ********************

# ## Let's start with the mandatory 'Hello World' – because tradition matters!

# CELL ********************

print('Hello World!')

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# MARKDOWN ********************

# ## Libraries

# MARKDOWN ********************

# ### Install library
# - ### Example Pandas, Polars, DuckDB 

# CELL ********************

%pip install matplotlib

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# MARKDOWN ********************

# ### Install if not installed, Upgrade if installed and Upgrade dependencies

# CELL ********************

%pip install -U matplotlib

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# MARKDOWN ********************

# ### Is Library installed?

# MARKDOWN ********************

# #### Specific library with detail

# CELL ********************

%pip show duckdb

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# MARKDOWN ********************

# #### List installed libraries

# CELL ********************

%pip list

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# MARKDOWN ********************

# #### List and filter using grep

# CELL ********************

%pip list | grep duck

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# MARKDOWN ********************

# #### List that we can display and filter

# CELL ********************

# Method that gives us more options like displaying and filtering
# uses newer method and not ones that are deprecated

from importlib.metadata import distributions
import pandas as pd

packages = [(dist.metadata['Name'], dist.version) for dist in distributions()]
# Give human readable column names
df = pd.DataFrame(packages, columns=['Package', 'Version'])
display(df.sort_values('Package'))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# MARKDOWN ********************

# ### Import library - alias friendly shorter names (preference)

# CELL ********************

import matplotlib.pyplot as plt
import numpy as np

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

x = np.linspace(0, 2 * np.pi, 200)
y = np.sin(x)

fig, ax = plt.subplots()
ax.plot(x, y)
plt.show()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# MARKDOWN ********************

# ## Python is Object Orientated

# MARKDOWN ********************

# ### Variables

# CELL ********************

# Code for Variables

my_variable = 100
print(my_variable)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

hello = "Hello World!"
print(hello)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# MARKDOWN ********************

# ### f-strings — the clean way to build strings
# Use `f"..."` and put variable names inside `{}` — Python fills them in at runtime.
# You'll see this pattern constantly in notebook code.

# CELL ********************

airline = "American Airlines"
origin = "DCA"
distance = 2288

# Old way
print("Airline: " + airline + ", From: " + origin + ", Distance: " + format(distance, ",") + " miles")

# f-string way
print(f"Airline: {airline}, From: {origin}, Distance: {distance:,} miles")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# MARKDOWN ********************

# ### Functions

# CELL ********************

# Code for Functions
# We have already seen one: print()
# We apply this over the object
# Here is another

fruit = 'apple'
fruit_length = len(fruit)
print(fruit_length)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

# We can create our own

def double(x):
    return x * 2

print(double(10))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# MARKDOWN ********************

# ### Methods - part of the object

# CELL ********************

# Code for Methods

name = "DAX Shepherd"
lowername = name.lower()    # Method to convert to lowercase
lowername.startswith("d")        


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# MARKDOWN ********************

# ### Method Chaining

# CELL ********************

# Chaining

name = "DAX Shepherd"

#First convert to lowercase and then check if it start with lowercase "d"

name.lower().startswith("d")


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# MARKDOWN ********************

# ### Chaining across lines

# MARKDOWN ********************

# ### **Method 1: Parenthesis '()'**

# CELL ********************

# Chaining across lines

# Very common in PySpark code
# Allows you to think about each transformtion you are doing

# Use the parenthesis '()'

name = "DAX Shepherd"

result = (
    name
    .lower()
    .startswith("d")
)

result

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# MARKDOWN ********************

# ### **Method 2: Backslash '\\'**

# CELL ********************

# Chaining across lines

# Very common in PySpark code
# Allows you to think about each transformation you are doing

# Use the backslash '\'

name = "DAX Shepherd"

name \
    .lower() \
    .startswith("d")


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# MARKDOWN ********************

# ### Accessing data from Pure Python notebook


# MARKDOWN ********************

# - #### Drag File over — DuckDB reads the 650 MB CSV directly

# CELL ********************

import duckdb

flights_path = "/lakehouse/default/Files/flights/flights_2022.csv"
display(duckdb.sql(f"SELECT * FROM read_csv('{flights_path}') LIMIT 1000").df())

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# MARKDOWN ********************

# - #### Small lookup files — pandas is perfect here

# CELL ********************

import pandas as pd
airlines = pd.read_csv("/lakehouse/default/Files/flights/airlines.csv")
display(airlines)


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# MARKDOWN ********************

# ### Using DuckDB Example - adding our own SQL Code

# CELL ********************

import duckdb

duckdb.sql(
    """
    SELECT
        Origin,
        Reporting_Airline,
        COUNT(*) AS Cancelled_Flights
    FROM read_csv('/lakehouse/default/Files/flights/flights_2022.csv')
    WHERE Cancelled = 1
        AND Origin IN ('DCA', 'IAD', 'BWI')
    GROUP BY Origin, Reporting_Airline
    ORDER BY Origin, Cancelled_Flights DESC
    LIMIT 15
    """
).df()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# MARKDOWN ********************

# ## Pandas - Working with Data
# Pandas is the go-to library for data work in Python.
# Everything here has a direct equivalent in PySpark — same ideas, different syntax.

# MARKDOWN ********************

# ### Inspect the data

# CELL ********************

import pandas as pd

airports = pd.read_csv("/lakehouse/default/Files/flights/airports.csv")

print(airports.shape)      # rows, columns
print(airports.dtypes)     # column types
airports.head(5)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# MARKDOWN ********************

# ### Filter rows
# We're presenting at Power BI Days DC — let's look at the DC metro airports

# CELL ********************

dc_airports = airports[airports["iata_code"].isin(["DCA", "IAD", "BWI"])]
display(dc_airports)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# MARKDOWN ********************

# ### Select columns
# Only the columns we care about

# CELL ********************

slim = airports[["iata_code", "name", "municipality", "iso_region", "type"]]
display(slim.head(10))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# MARKDOWN ********************

# ### GroupBy + Aggregation
# Count airports by type — same concept as PySpark's `.groupBy().agg()`

# CELL ********************

airports_by_type = (
    airports
    .groupby("type")
    .agg(airport_count=("iata_code", "count"))
    .reset_index()
    .sort_values("airport_count", ascending=False)
)

display(airports_by_type)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# MARKDOWN ********************

# ### Merge (Join)
# Add the departure airport name to a sample of flights — same concept as PySpark's `.join()`

# CELL ********************

flights_sample = pd.read_csv("/lakehouse/default/Files/flights/flights_2022.csv", nrows=50000)

dc_flights = flights_sample[flights_sample["Origin"].isin(["DCA", "IAD", "BWI"])]

dc_with_airport = (
    dc_flights
    .merge(airports[["iata_code", "name", "municipality"]], left_on="Origin", right_on="iata_code", how="left")
    .rename(columns={"name": "Origin Airport", "municipality": "Origin City"})
    .drop(columns=["iata_code"])
)

display(dc_with_airport[["FlightDate", "Reporting_Airline", "Origin", "Origin Airport", "Origin City", "Dest"]].head(10))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# MARKDOWN ********************

# # What happens when your data is too big??

# CELL ********************

from IPython.display import Image, display
display(Image(filename="/lakehouse/default/Files/demo_assets/Out_Of_Memory.jpg", width=1000))
display(Image(filename="/lakehouse/default/Files/demo_assets/this_is_fine.jpg", width=800))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }
