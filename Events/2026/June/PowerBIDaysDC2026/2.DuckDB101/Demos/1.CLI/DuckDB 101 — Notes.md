# DuckDB 101 — Desktop Demo

> **Obsidian tip:** `Ctrl+=` to zoom in, `Ctrl+-` to zoom out

## Install

**Windows**
```powershell
winget install duckdb.cli
```

**Mac**
```bash
brew install duckdb
```
## Connecting & Opening a Database

**In-memory database**
```powershell
duckdb
```

**Database on disk**
```powershell
duckdb flights.db
```

**My First Select**
```SQL
SELECT 'Hello world'
```

>[!danger] What Am I Doing Wrong?
### Exit Thrashing

![vim exit thrashing](vim-exit-thrashing.png)

```
.exit   or   .quit
```

---

## Dot Commands

**Control the shell — CLI meta-commands, not SQL.**

```sql
.help
.database
.table
.open 'flights.db'
```

**Attach existing database**
```sql
ATTACH 'flights.db' AS flights;
ATTACH 'airports.db' AS airports;
DETACH flights;

USE flights;
```

**Install extensions**
```sql
INSTALL httpfs;
LOAD httpfs;

ATTACH 's3://mybucket/data.db' AS remote;
```

---

## Dataset

**US Airline On-Time Performance** — Bureau of Transportation Statistics (BTS)
[BTS Transtats](https://www.transtats.bts.gov/)

- 3 years: 2022, 2023, 2024
- ~7 million flights per year (~21 million rows total)
- 3 tables: `flights`, `airlines`, `airports`
- Too large for Excel — DuckDB reads it directly 🦆✈️

---

## Basic SQL

**Read a CSV directly — no import step**
```sql
SELECT * FROM 'flights_2023.csv';
```
**Inspect the schema**
```sql
DESCRIBE SELECT * FROM 'flights_2023.csv';
```

**Instant data profile**
```sql
SUMMARIZE SELECT * FROM 'flights_2023.csv';
```

**Load into a table**
```sql
CREATE TABLE flights AS SELECT * FROM 'flights_2023.csv';
```

**Not T-SQL — use LIMIT, not TOP**
```sql
SELECT Reporting_Airline, Origin, Dest, ArrDelay
FROM 'flights_2023.csv'
LIMIT 10;
```

**Show the tables**
```sql
SHOW TABLES;
```

---

## Syntactic Sugar

```sql
-- EXCLUDE — drop columns without listing everything else
SELECT * EXCLUDE (CRSElapsedTime, ActualElapsedTime, AirTime)
FROM 'flights_2023.csv'
LIMIT 20;
```

```sql
-- Glob — read multiple files in one query, no UNION
SELECT COUNT(*) AS total_flights
FROM 'flights_*.csv';
```

---

## Aggregations

**Most delayed airlines**
```sql
SELECT
    Reporting_Airline,
    COUNT(*) AS flights,
    ROUND(AVG(ArrDelay), 1) AS avg_arr_delay_min,
    ROUND(AVG(DepDelay), 1) AS avg_dep_delay_min,
    ROUND(SUM(Cancelled) * 100.0 / COUNT(*), 2) AS cancel_pct
FROM 'flights_2023.csv'
GROUP BY Reporting_Airline
ORDER BY avg_arr_delay_min DESC;
```

**Worst months for delays**
```sql
SELECT
    strftime(FlightDate, '%Y-%m') AS month,
    COUNT(*) AS flights,
    ROUND(AVG(ArrDelay), 1) AS avg_delay
FROM 'flights_*.csv'
WHERE Cancelled = 0
GROUP BY month
ORDER BY month;
```

**The Southwest December 2022 meltdown**
```sql
SELECT
    strftime(FlightDate, '%Y-%m') AS month,
    Reporting_Airline,
    COUNT(*) AS flights,
    SUM(Cancelled) AS cancellations,
    ROUND(SUM(Cancelled) * 100.0 / COUNT(*), 1) AS cancel_pct
FROM 'flights_2022.csv'
WHERE Reporting_Airline = 'WN'
GROUP BY month, Reporting_Airline
ORDER BY month;
```

**Export a summary**
```sql
COPY (SELECT * FROM (SUMMARIZE SELECT * FROM 'flights_2023.csv')) TO 'summary.csv';
```

---

## Joins

```
flights  ──── Reporting_Airline ──▶  airlines  (IATA_CODE)
flights  ──── Origin / Dest     ──▶  airports  (IATA_CODE)
```

**Load lookup tables**
```sql
CREATE TABLE airlines AS SELECT * FROM 'airlines.csv';
CREATE TABLE airports AS SELECT * FROM 'airports.csv';
CREATE TABLE flights  AS SELECT * FROM 'flights_*.csv';
```

**Rank airlines by delay with readable names**
```sql
SELECT
    al.AIRLINE AS airline_name,
    COUNT(*) AS total_flights,
    ROUND(AVG(f.ArrDelay), 1) AS avg_delay_min
FROM flights f
JOIN airlines al ON f.Reporting_Airline = al.IATA_CODE
WHERE f.Cancelled = 0
GROUP BY al.AIRLINE
ORDER BY avg_delay_min DESC;
```

**Worst origin airports**
```sql
SELECT
    ap.AIRPORT,
    ap.CITY,
    ap.STATE,
    COUNT(*) AS departures,
    ROUND(AVG(f.DepDelay), 1) AS avg_dep_delay
FROM flights f
JOIN airports ap ON f.Origin = ap.IATA_CODE
WHERE f.Cancelled = 0
GROUP BY ap.AIRPORT, ap.CITY, ap.STATE
ORDER BY avg_dep_delay DESC
LIMIT 15;
```

**What's actually causing delays?**
```sql
SELECT
    al.AIRLINE,
    ROUND(AVG(f.CarrierDelay), 1)      AS carrier,
    ROUND(AVG(f.WeatherDelay), 1)      AS weather,
    ROUND(AVG(f.NASDelay), 1)          AS air_system,
    ROUND(AVG(f.LateAircraftDelay), 1) AS late_aircraft,
    ROUND(AVG(f.SecurityDelay), 1)     AS security
FROM flights f
JOIN airlines al ON f.Reporting_Airline = al.IATA_CODE
WHERE f.ArrDelay > 0 AND f.Cancelled = 0
GROUP BY al.AIRLINE
ORDER BY carrier DESC;
```

---

## Reading Files

**CSV**
```sql
SELECT * FROM 'flights_2023.csv';
```

```sql
SELECT * FROM 'flights_*.csv';
```

```sql
SELECT * FROM read_csv('flights_2023.csv', header=true, null_padding=true);
```

**Parquet**
```sql
SELECT * FROM 'flights_2023.parquet';
```

```sql
SELECT * FROM read_parquet('flights_*.parquet');
```

**JSON**
```sql
SELECT * FROM read_json('data.json');
```

---

## Exporting Data

**Export to Parquet**
```sql
COPY (SELECT * FROM 'flights_*.csv') TO 'flights_all.parquet' (FORMAT PARQUET);
```

**Export a query result to CSV**
```sql
COPY (
    SELECT Reporting_Airline, COUNT(*) AS flights, AVG(ArrDelay) AS avg_delay
    FROM 'flights_*.csv'
    GROUP BY Reporting_Airline
) TO 'delay_by_airline.csv';
```

---

## Tips & Gotchas

- Tab complete works in the CLI
- `LIMIT` not `TOP` — this is not T-SQL
- Semicolons required in CLI; not needed in the Python API
- `.quit` or `.exit` to exit — not `exit`, not `quit`, not Ctrl+C
- DuckDB reads CSV / Parquet / JSON directly — no import step needed
- Column names are case-sensitive in some contexts — quote them if needed
- `information_schema` works: `SELECT * FROM information_schema.tables;`

---



