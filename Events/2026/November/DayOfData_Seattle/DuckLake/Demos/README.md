# DuckLake with PostgreSQL: attendee walkthrough

Day of Data Seattle, November 12, 2026 · Jason Romans

Start with DuckDB querying flight files, then use PostgreSQL as a DuckLake catalog for transactions, history, schema evolution and shared clients. These are the current flights examples from the session. Older orders examples and presenter tools are omitted.

## Prepare

Requirements: Windows, PowerShell, Docker Desktop using Linux containers, Python 3.10 or later, and `tar` on PATH. Initial setup needs internet access. The default downloads two monthly BTS archives and keeps only Seattle flights from January 2024 and February 1. Allow several minutes for the downloads.

Open PowerShell in this **Demos** folder. All SQL paths are relative to this folder. Keep that working directory when running DuckDB yourself; the supplied launcher sets it automatically.

```powershell
Copy-Item .env.example .env
# Edit .env and replace the placeholder password before continuing.
./sql/00_setup-duckdb.ps1
python ./download_flights.py
./sql/01_start-postgres.ps1
./sql/02_open-duckdb.ps1
```

The setup pins DuckDB 2.0.0 and installs its DuckLake/PostgreSQL extensions. The downloader uses Python's standard library and that CLI, downloads January and February 2024 BTS archives, keeps SEA arrivals/departures through February 1, and builds `source-data/flights/flights_all.parquet`. No pip packages are required. The small Seattle CSV and Parquet are reused on subsequent runs. A failed month stops preparation rather than silently publishing an incomplete sample. The default sample contains the 24,295 flights needed for the lakehouse and history examples.

For the original three-year file-profiling example, run `python ./download_flights.py --full`. This downloads 36 months from 2022–2024 and needs several GB of free disk space. Completed annual CSVs are reused. Each mode caches its own Parquet; rerunning the command selects that mode for `flights_all.parquet`. Switch modes before creating the lakehouse, or use a fresh lakehouse for a new walkthrough.

`airlines.csv` and `airports.csv` are bundled lookup snapshots used in the session. They provide names and locations; flight records come from [BTS On-Time Performance](https://www.transtats.bts.gov/). Lookup upstream provenance is not recorded in the working demo, so these snapshots should not be treated as current authoritative reference lists.

The PostgreSQL service listens at `127.0.0.1:55432`, database `ducklake_catalog`, user `ducklake_demo`. Passwords stay in ignored `.env`; the launcher supplies `PGPASSWORD` to DuckDB. Changing `.env` does not change an existing database password. This package uses the separate Compose project `ducklake-seattle-attendee`; stop any other service occupying port 55432 before starting it.

## Walkthrough

Run SQL at the DuckDB prompt unless marked PostgreSQL. `.read sql/03_versions.sql` runs one file. Table creation and schema changes expect a fresh lakehouse and should run once.

| Order | File | Purpose |
|---|---|---|
| 1 | `sql/03_versions.sql` | Check engine and extension versions. |
| 2 | `sql/04_duckdb_files.sql` | Query the sample Parquet, join the airline CSV, export a summary and save a local DuckDB table. |
| 3 | `sql/05_attach.sql` | Attach the PostgreSQL-backed DuckLake. Run once per client. |
| 4 | `sql/06_flights.sql` | Create Seattle January 2024 flights and an airport lookup in DuckLake. |
| 5 | `sql/11_catalog_inspection.sql` | Inspect metadata **in PostgreSQL**, using DBeaver or psql. |
| 6 | `sql/07_history.sql` | Roll back and commit February 1 flights; query an earlier snapshot. |
| 7 | `sql/08_schema.sql` | Add review status and compare the old/new schemas. |
| 8 | `sql/09_client_a.sql`, `sql/10_client_b.sql` | Interleave two clients as described below. |

For PostgreSQL inspection, open another PowerShell terminal in Demos:

```powershell
docker compose exec postgres psql -U ducklake_demo -d ducklake_catalog
```

Paste queries from `11_catalog_inspection.sql` there. That file is PostgreSQL SQL, not a DuckDB `.read` script. Its queries are read-only and can be repeated later.

For client B, open a second PowerShell terminal in Demos, run `./sql/02_open-duckdb.ps1`, then `.read sql/05_attach.sql`. Keep B in autocommit mode. Run the A/B files **one labeled block at a time**, in this order: readiness in A, A1, B1, A2, B2, B3, A3. Do not `.read` either A/B file wholesale: that skips the pause needed to observe an uncommitted change. This shows committed visibility and writes from each client, without demonstrating simultaneous write conflicts.

The default sample narrows file profiling in 04 to Seattle and the selected dates, rather than all US flights over three years. The SQL techniques remain the same. With the session's source data, 06 produces 23,508 flights. In 07, rollback preserves that count; committing 787 February 1 flights produces 24,295. The earlier snapshot remains queryable. `flight_id` and `review_status` are demonstration fields, not BTS fields. Source updates may affect reproduced counts.

## Storage and shutdown

- `source-data/flights/`: downloaded inputs and bundled lookups.
- `exports/`: CSV summary and local `.duckdb` output from 04.
- `ducklake/`: DuckLake-managed Parquet and retained history.
- Docker volume `ducklake-seattle-attendee_catalog`: PostgreSQL catalog.

Inlining is disabled so analytical rows go to Parquet. Both local clients share the same data path. Remote clients also need shared storage. Keep the catalog and its managed files together; deleting individual Parquet files breaks retained history.

Exit each DuckDB client with `.quit`. Then stop PostgreSQL while keeping data:

```powershell
docker compose stop postgres
```

Start again with `./sql/01_start-postgres.ps1`. Existing tables and schema changes persist. No automatic reset or Docker Desktop shutdown script is included. For another fresh walkthrough, use a separate package folder, a distinct Compose project name and an available port, updating 05's connection port to match.

The attendee files use relative paths; they do not need `C:/Demos/ducklake-postgres`. Large source downloads, credentials, binaries and generated lakehouse files are excluded by this folder's `.gitignore`.
