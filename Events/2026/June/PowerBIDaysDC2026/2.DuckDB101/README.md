# DuckDB 101: From Desktop to Notebook

**Event:** Power BI Days DC 2026  
**Date:** June 12, 2026 — 1:30 PM ET  
**Location:** Washington, DC

## Slides

`DCDays2026_DuckDB101.pptx`

## Dataset

All demos use the **US Airline On-Time Performance** dataset from the [Bureau of Transportation Statistics (BTS)](https://www.transtats.bts.gov/). It covers ~21 million flights across 2022–2024 with three tables: `flights`, `airlines`, and `airports`.

## Demos

### CLI Demo (`Demos/1.CLI/`)

| File | Description |
|---|---|
| `DuckDB 101 — Notes.md` | Full CLI walkthrough — install, dot commands, SQL queries, joins, and exports using the US flights dataset |

### Local / VS Code (`Demos/2.LocalVSCode/`)

| File | Description |
|---|---|
| `01_intro.ipynb` | DuckDB intro notebook — connecting, querying CSVs, basic SQL |
| `02_flights_demo.ipynb` | Flights dataset demo — aggregations, joins, and exports |
| `03_flights_queries.sql` | Standalone SQL queries from the demo |

### Fabric Notebooks (`Demos/3.FabricNotebooks/`)

| File | Description |
|---|---|
| `nb_01_meet_the_duck.ipynb` | Intro to DuckDB in a Fabric notebook |
| `nb_02_flights_demo.ipynb` | Flights dataset queries running in Fabric |

> Import the `.ipynb` files into a Fabric notebook to follow along.
