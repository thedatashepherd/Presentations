# DuckDB 101: From Desktop to Notebook

**Event:** Day of Data Albany 2026
**Date:** August 8, 2026
**Speaker:** Jason Romans — The Data Shepherd

Event page: https://dayofdata.org/2026-08-08-dayofdata1144/

---

## Slides

`Albany_DayofData2026_DuckDB101.pptx`

---

## Dataset

All demos use the **US Airline On-Time Performance** dataset from the [Bureau of Transportation Statistics (BTS)](https://www.transtats.bts.gov/) — 3 years (2022–2024), ~21 million flights, 3 tables (`flights`, `airlines`, `airports`).

The data files are large and not stored in this repo. Download them with the included script:

```bash
cd Demos/2.LocalVSCode
python download_flights.py
```

This pulls directly from BTS and writes annual CSV files to a `data/flights/` folder. It skips any year already downloaded.

---

## Demos

### `Demos/1.CLI/` — Desktop / Command Line + Built-in UI
- `DuckDB 101 — Notes.md` — full walkthrough: terminal CLI basics (install, connect, dot commands, ATTACH/DETACH, extensions), then hands off to DuckDB's built-in UI (`duckdb -ui`) for the SQL tour — basic queries, syntactic sugar, aggregations, joins, reading/exporting files.

### `Demos/2.LocalVSCode/` — VS Code Notebook
- `flights_demo.ipynb` — single notebook picking up right after the built-in UI: DuckDB ↔ pandas bridge, querying DataFrames with SQL, charts, delay-cause breakdown, local airport spotlight (Albany/LaGuardia), Parquet export, and a bonus remote-file (S3/httpfs) query.
- `download_flights.py` — dataset download script

### `Demos/3.FabricNotebooks/` — Microsoft Fabric
- `nb_01_meet_the_duck.ipynb` — Intro to DuckDB in a Fabric notebook
- `nb_02_flights_demo.ipynb` — Full flights demo running against a Lakehouse

> Import the `.ipynb` files into a Fabric Pure Python notebook to follow along.
