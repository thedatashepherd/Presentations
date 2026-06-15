# DuckDB 101: From Desktop to Notebook

**Event:** Power BI Days DC 2026  
**Date:** June 12, 2026 — 1:30 PM ET  
**Speaker:** Jason Romans — The DAX Shepherd

---

## Slides

`DCDays2026_DuckDB101.pptx`

---

## Dataset

All demos use the **US Airline On-Time Performance** dataset from the [Bureau of Transportation Statistics (BTS)](https://www.transtats.bts.gov/) — ~21 million flights across 2022–2024.

The data files are large and not stored in this repo. Download them with the included script:

```bash
cd Demos/2.LocalVSCode
python download_flights.py
```

This pulls directly from BTS and writes annual CSV files to a `data/flights/` folder. It skips any year already downloaded.

---

## Demos

### `Demos/1.CLI/` — Desktop / Command Line
- `DuckDB 101 — Notes.md` — CLI walkthrough with commands to follow along

### `Demos/2.LocalVSCode/` — VS Code Notebooks
- `01_intro.ipynb` — DuckDB basics, file reading, schema inspection
- `02_flights_demo.ipynb` — Aggregations, joins, charts, and S3 demo
- `03_flights_queries.sql` — Standalone SQL queries (run with the DuckDB VS Code extension)
- `download_flights.py` — Dataset download script

### `Demos/3.FabricNotebooks/` — Microsoft Fabric
- `nb_01_meet_the_duck.ipynb` — Intro to DuckDB in a Fabric notebook
- `nb_02_flights_demo.ipynb` — Full flights demo running against a Lakehouse

> Import the `.ipynb` files into a Fabric Pure Python notebook to follow along.
