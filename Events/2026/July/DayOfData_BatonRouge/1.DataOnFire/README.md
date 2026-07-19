# Data on Fire: A Hands-On Intro to Spark in Fabric

**Event:** Day of Data Baton Rouge 2026
**Date:** July 18, 2026
**Location:** Baton Rouge, LA

## Slides

`BR_DayofData2026_FabricSpark.pptx`

## Demos

All demos run in Microsoft Fabric notebooks using PySpark and Python. Import the `.ipynb` files into a Fabric notebook to follow along.

### Fabric Notebooks (`Demos/FabricNotebooks/`)

| File | Description |
|---|---|
| `00_Setup_Fresh.ipynb` | Setup notebook — creates the demo tables in the lakehouse (run first; `02_PySpark` calls it via `%run`) |
| `01_Python.ipynb` | Python basics in a Fabric notebook — data types, pandas, working with data |
| `02_PySpark.ipynb` | Introduction to PySpark — DataFrames, transformations, and actions |
| `03_WritingToLakehouse.ipynb` | Writing data to a Fabric Lakehouse using PySpark |
| `04_SemanticLink.ipynb` | Semantic Link — connecting Fabric notebooks to Power BI semantic models |
| `05_WindowFunctions.ipynb` | PySpark window functions for advanced analytics |
