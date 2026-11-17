-- Run in: DuckDB A, at the DuckDB prompt.

-- Inspect and query Parquet, join airline names from CSV, and
-- export a summary. The queries create no tables or views until the
-- final section, which persists the summary into a local .duckdb file
-- to set up the comparison with DuckLake.
-- Run after 03_versions.sql. No DuckLake catalog is needed.

-- Inspect column names and types directly from the Parquet file.
DESCRIBE
SELECT *
FROM read_parquet(
    './source-data/flights/flights_all.parquet'
);

-- Read a few rows directly from the Parquet file.
SELECT FlightDate, Reporting_Airline, Origin, Dest, ArrDelay, Cancelled
FROM read_parquet(
    './source-data/flights/flights_all.parquet'
)
LIMIT 10;

-- Profile delays and distance with DuckDB's SUMMARIZE statement.
-- See ranges, averages, and null percentages.
SUMMARIZE
SELECT ArrDelay, DepDelay, Distance
FROM read_parquet(
    './source-data/flights/flights_all.parquet'
);

-- Summarize January 2024 flights arriving at or departing Seattle.
SELECT Reporting_Airline AS airline,
       count(*) AS flights,
       round(avg(ArrDelay), 1) AS avg_arrival_delay_minutes,
       count(*) FILTER (WHERE Cancelled = 1) AS cancellations
FROM read_parquet(
    './source-data/flights/flights_all.parquet'
)
WHERE FlightDate >= DATE '2024-01-01'
  AND FlightDate < DATE '2024-02-01'
  AND (Origin = 'SEA' OR Dest = 'SEA')
GROUP BY Reporting_Airline
ORDER BY flights DESC;

-- Read the airline lookup from a separate CSV file.
SELECT *
FROM read_csv(
    './source-data/flights/airlines.csv',
    header = true
)
LIMIT 5;

-- A CTE gives this query a named summary. It exists only within this
-- statement. Join it to the CSV and keep codes with no lookup match.
WITH sea_airline_delays AS (
    SELECT Reporting_Airline AS airline,
           count(*) AS flights,
           round(avg(ArrDelay), 1) AS avg_arrival_delay_minutes,
           count(*) FILTER (WHERE Cancelled = 1) AS cancellations
    FROM read_parquet(
        './source-data/flights/flights_all.parquet'
    )
    WHERE FlightDate >= DATE '2024-01-01'
      AND FlightDate < DATE '2024-02-01'
      AND (Origin = 'SEA' OR Dest = 'SEA')
    GROUP BY Reporting_Airline
)
SELECT s.airline AS airline_code,
       coalesce(a.AIRLINE, s.airline) AS airline_name,
       s.flights,
       s.avg_arrival_delay_minutes,
       s.cancellations
FROM sea_airline_delays AS s
LEFT JOIN read_csv(
    './source-data/flights/airlines.csv',
    header = true
) AS a ON s.airline = a.IATA_CODE
ORDER BY s.flights DESC;

-- COPY exports the query results directly to a CSV file.
-- Repeat the CTE because the previous statement did not save it.
COPY (
    WITH sea_airline_delays AS (
        SELECT Reporting_Airline AS airline,
               count(*) AS flights,
               round(avg(ArrDelay), 1) AS avg_arrival_delay_minutes,
               count(*) FILTER (WHERE Cancelled = 1) AS cancellations
        FROM read_parquet(
            './source-data/flights/flights_all.parquet'
        )
        WHERE FlightDate >= DATE '2024-01-01'
          AND FlightDate < DATE '2024-02-01'
          AND (Origin = 'SEA' OR Dest = 'SEA')
        GROUP BY Reporting_Airline
    )
    SELECT s.airline AS airline_code,
           coalesce(a.AIRLINE, s.airline) AS airline_name,
           s.flights,
           s.avg_arrival_delay_minutes,
           s.cancellations
    FROM sea_airline_delays AS s
    LEFT JOIN read_csv(
        './source-data/flights/airlines.csv',
        header = true
    ) AS a ON s.airline = a.IATA_CODE
    ORDER BY s.flights DESC
)
TO './exports/sea_airline_delays.csv'
(FORMAT CSV, HEADER true);

-- Read the exported CSV back into DuckDB.
SELECT *
FROM read_csv(
    './exports/sea_airline_delays.csv',
    header = true
)
ORDER BY flights DESC;

-- The CSV export is a file, but we have not saved a DuckDB table yet.
-- Now persist the summary in DuckDB's own database format.

-- 1. Open a local database file. ATTACH creates it if needed.
-- ATTACH alone does not change the active database.
ATTACH './exports/flights_local.duckdb' AS localdb;

-- 2. Switch to that database before creating the table.
USE localdb;

-- This should show localdb and main. The prompt also shows localdb.
SELECT current_database() AS active_database,
       current_schema() AS active_schema;

-- 3. Save the CSV summary as a table in the active database.
-- CREATE OR REPLACE replaces this table if it already exists.
CREATE OR REPLACE TABLE sea_airline_delays AS
SELECT *
FROM read_csv(
    './exports/sea_airline_delays.csv',
    header = true
);

-- The table now lives in localdb and survives a restart.
SHOW TABLES;

SELECT *
FROM sea_airline_delays
ORDER BY flights DESC;

-- 4. Switch back to memory. Run this BEFORE DETACH.
USE memory;

-- Confirm memory is active. The prompt should now show memory.
SELECT current_database() AS active_database;

-- 5. Close the attachment. The database file remains on disk.
-- DETACH fails if localdb is still the active database.
DETACH localdb;

-- A .duckdb file stores tables in DuckDB's own binary format.
-- One process can open it for writing, or several can open read-only.
-- It does not provide DuckLake-style snapshots and time travel.
-- Next, 05_attach.sql uses ATTACH and USE for a DuckLake instead.

-- Result: The CSV and local DuckDB file both contain the summary.
-- This session is back in memory, ready for the DuckLake attachment.
