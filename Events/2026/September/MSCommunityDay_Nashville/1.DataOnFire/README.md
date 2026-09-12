# Data on Fire: A Hands-On Intro to Spark in Fabric

**Event:** Nashville Microsoft Community Day 2026
**Date:** September 11, 2026
**Location:** Nelson Andrews Leadership Center, Nashville, TN
**Speaker:** Jason Romans — The Data Shepherd

Event page: https://m365nashville.org

---

## Slides

`Nashville_MSCommunityDay2026_FabricSpark.pdf`

---

## Dataset

The flight demos use the **US Airline On-Time Performance** dataset from the [Bureau of Transportation Statistics (BTS)](https://www.transtats.bts.gov/) — 2022–2024, plus `airlines` and `airports` lookups. For this session the flights are narrowed to the two Tennessee airports, **BNA** (Nashville) and **MEM** (Memphis), so everything runs fast live.

The CSVs are large and not stored in this repo. Upload them to `Files/flights/` in your lakehouse to follow along.

The Semantic Link demos use the **Contoso10K** semantic models rather than flight data.

---

## Demos

All demos run in Microsoft Fabric notebooks using PySpark and Python. Import the `.ipynb` files into a Fabric notebook to follow along.

### Fabric Notebooks (`Demos/FabricNotebooks/`)

| File | Description |
|---|---|
| `00_Setup_Fresh.ipynb` | Setup notebook — a one-cell sentinel that `02_PySpark` calls via `%run` to confirm the Spark session is alive |
| `01_Python.ipynb` | Python basics in a Fabric notebook — data types, f-strings, functions, pandas, and a DuckDB detour |
| `02_PySpark.ipynb` | Introduction to PySpark — DataFrames, transformations, actions, Data Wrangler, and the `%%sql` magic |
| `03_WritingToLakehouse.ipynb` | Writing data to a Fabric Lakehouse — write modes, partitioning, merge, and time travel |
| `04_SemanticLink.ipynb` | Semantic Link and Semantic Link Labs — explore a model, evaluate measures and DAX, check referential integrity, analyze memory, and write back to the lakehouse |
| `05_WindowFunctions.ipynb` | PySpark window functions — ranking, lag/lead, running totals, and quartiles |

> Notebooks 03 and 05 were not demoed live but are included as bonus material.

---

## Session order

`01_Python` → `02_PySpark` → `04_SemanticLink`
