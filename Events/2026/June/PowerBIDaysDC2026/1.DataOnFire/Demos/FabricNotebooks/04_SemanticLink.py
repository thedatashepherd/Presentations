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

# # Semantic Link & Semantic Link Labs


# MARKDOWN ********************

# ## 1. Setup
# `sempy` is pre-installed in Fabric. Upgrade to get the full `semantic-link-labs` toolkit.

# CELL ********************

!pip install -U semantic-link-labs

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Import semantic link and alias
import sempy.fabric as fabric
from sempy.relationships import plot_relationship_metadata

dataset_name = "Contoso10K"

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 2. Explore the Model

# MARKDOWN ********************

# ### Explore semantic model

# CELL ********************

df_datasets = fabric.list_datasets()
df_datasets

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### List tables

# CELL ********************

df_tables = fabric.list_tables(dataset_name)
df_tables

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### Display columns (including hidden properties)

# CELL ********************

df_columns = fabric.list_tables(dataset_name, include_columns=True)
df_columns[df_columns["Name"] == "Sales"]

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 3. Visualize Relationships

# MARKDOWN ********************

# ### Plot relationship diagram

# CELL ********************

contoso_model = "Contoso10K"
relationships = fabric.list_relationships(contoso_model)

plot_relationship_metadata(relationships)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### See the invisible — AutoDate hidden relationships

# CELL ********************

__autodate_model = "Contoso10K_WithAutoDate"

relationships_date = fabric.list_relationships(__autodate_model)
plot_relationship_metadata(relationships_date)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 4. Read Data from the Model

# MARKDOWN ********************

# ### List measures

# CELL ********************

df_measures = fabric.list_measures(dataset_name)
df_measures

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### Read a table directly

# CELL ********************

df_table = fabric.read_table(dataset_name, "Product")
df_table.head(5)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### Query the model with Spark SQL

# CELL ********************

spark.conf.set("spark.sql.catalog.pbi", "com.microsoft.azure.synapse.ml.powerbi.PowerBICatalog")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df = spark.sql("SHOW TABLES FROM pbi")
display(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 5. Evaluate Measures

# CELL ********************

fabric.evaluate_measure(dataset_name, measure="Sales Amount")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### GroupBy Columns

# CELL ********************

fabric.evaluate_measure(dataset_name, measure="Sales Amount", groupby_columns=["Product[Brand]", "Product[Category]"])

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### DAX cell magic (%%dax)

# CELL ********************

# Load %%dax cell magic
%load_ext sempy

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%dax "Contoso10K"
# MAGIC 
# MAGIC EVALUATE
# MAGIC SUMMARIZECOLUMNS(
# MAGIC "Sales Amount",[Sales Amount]
# MAGIC )


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### Run DAX with evaluate_dax

# CELL ********************

__dataset = "Contoso10K"
__workspace = "session_data_on_fire_fabric_spark"

__dax = """
EVALUATE 
SUMMARIZECOLUMNS(
    'Product'[Brand],
   'Date'[Month Short],
   'Date'[Year],
   "Sales Amount",
    CALCULATE([Sales Amount])
    )
"""

fabric.evaluate_dax(
    dataset=__dataset,
    dax_string= __dax,
    workspace=__workspace,
    verbose=0,
    num_rows=10
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 6. Data Quality — Referential Integrity
# Use DAX to surface Sales dates that don't exist in the Date table — the classic blank row problem.

# CELL ********************

__dataset = "Contoso10K_RI"
__workspace = "session_data_on_fire_fabric_spark"

dax = """
EVALUATE 
    EXCEPT (
        VALUES( 'Sales'[Order Date] ),
        VALUES('Date'[Date] )
    )
"""

fabric.evaluate_dax(
    dataset=__dataset,
    dax_string= dax,
    workspace=__workspace,
    verbose=0,
    num_rows=None
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# > **Finding:** 2017 is missing from the Date table — either it was never loaded or was filtered out in Power Query.

# MARKDOWN ********************

# ## 7. Model Health — Memory Analyzer
# One of the tools in the Semantic Link Labs model health suite.

# CELL ********************

import sempy.fabric as fabric

__smallmodel = "Contoso10K"
__workspace = "session_data_on_fire_fabric_spark"

fabric.model_memory_analyzer(dataset = __smallmodel, workspace = __workspace)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### Compare: model bloated with AutoDate

# CELL ********************

import sempy.fabric as fabric

__xlmodel = "Contoso10K_WithAutoDateXL"
__workspace = "session_data_on_fire_fabric_spark"

fabric.model_memory_analyzer(dataset = __xlmodel, workspace = __workspace)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 8. Close the Loop — Write Back to the Lakehouse
# Read from the semantic model, enrich it in Python, write it back.
# Direct Lake picks up the new table immediately — no refresh needed.
# **Power BI → Python → Power BI.**

# MARKDOWN ********************

# ### Read Sales from the semantic model

# CELL ********************

# Same data Power BI is reading — now in a Spark DataFrame
df_sales_pd = fabric.read_table(dataset_name, "Sales")
df_sales = spark.createDataFrame(df_sales_pd)

display(df_sales.limit(5))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### Enrich — compute Sales Amount, add a Sales Tier

# CELL ********************

from pyspark.sql.functions import col, when, round as spark_round

df_enriched = (
    df_sales
    .withColumn(
        "Sales Amount",
        spark_round(col("Quantity") * col("Unit Price"), 2)
    )
    .withColumn(
        "Sales Tier",
        when(col("Sales Amount") >= 1000, "High")
        .when(col("Sales Amount") >= 500,  "Medium")
        .otherwise("Low")
    )
    .filter(col("Quantity") > 0)
)

display(
    df_enriched
    .select("Order Number", "Order Date", "Quantity", "Unit Price", "Sales Amount", "Sales Tier")
    .limit(10)
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### Write back — Direct Lake sees it immediately
# Delta tables don't allow spaces in column names — rename them before writing.

# CELL ********************

from pyspark.sql.functions import col

df_enriched_clean = df_enriched
for col_name in df_enriched.columns:
    df_enriched_clean = df_enriched_clean.withColumnRenamed(col_name, col_name.replace(" ", "_"))

(
    df_enriched_clean
    .write
    .mode("overwrite")
    .saveAsTable("FactSalesEnriched")
)

print(f"Done — {df_enriched_clean.count():,} rows written to FactSalesEnriched")
print("Direct Lake sees this immediately — no refresh needed.")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
