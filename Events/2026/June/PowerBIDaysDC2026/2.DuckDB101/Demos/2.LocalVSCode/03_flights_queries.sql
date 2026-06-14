-- ============================================================
-- DuckDB 101 — Flight Delays Demo
-- US Airline On-Time Performance (BTS) · 2022–2024
-- Run from: local-vscode/ directory
-- ============================================================


-- ── 1. READING FILES ────────────────────────────────────────

-- Read CSV directly — no import step
SELECT * FROM 'data/flights/flights_2023.csv' LIMIT 5;

-- Inspect the schema
DESCRIBE SELECT * FROM 'data/flights/flights_2023.csv';

-- Instant data profile
SUMMARIZE SELECT * FROM 'data/flights/flights_2023.csv';

-- Drop columns you don't want (not available in T-SQL!)
SELECT * EXCLUDE (CRSElapsedTime, ActualElapsedTime, AirTime, DepDel15, ArrDel15)
FROM 'data/flights/flights_2023.csv'
LIMIT 10;


-- ── 2. GLOB — ALL 3 YEARS IN ONE QUERY ─────────────────────

SELECT
    year(FlightDate::DATE)  AS year,
    COUNT(*)                AS total_flights,
    SUM(Cancelled)          AS cancellations
FROM 'data/flights/flights_*.csv'
GROUP BY year
ORDER BY year;


-- ── 3. LOAD TABLES ──────────────────────────────────────────

CREATE OR REPLACE TABLE airlines AS SELECT * FROM 'data/flights/airlines.csv';
CREATE OR REPLACE TABLE airports AS SELECT * FROM 'data/flights/airports.csv';
CREATE OR REPLACE TABLE flights  AS SELECT * FROM 'data/flights/flights_*.csv';

SHOW TABLES;


-- ── 4. BASIC AGGREGATIONS ───────────────────────────────────

-- On-time performance by airline
SELECT
    al.AIRLINE,
    COUNT(*)                                        AS total_flights,
    ROUND(AVG(f.ArrDelay), 1)                       AS avg_arr_delay_min,
    ROUND(SUM(f.Cancelled) * 100.0 / COUNT(*), 1)  AS cancel_pct
FROM flights f
JOIN airlines al ON f.Reporting_Airline = al.IATA_CODE
WHERE f.Cancelled = 0
GROUP BY al.AIRLINE
ORDER BY avg_arr_delay_min DESC;

-- Monthly trends across all 3 years
SELECT
    strftime(FlightDate::DATE, '%Y-%m') AS month,
    COUNT(*)                             AS flights,
    ROUND(AVG(ArrDelay), 1)              AS avg_arr_delay
FROM flights
WHERE Cancelled = 0
GROUP BY month
ORDER BY month;


-- ── 5. WHAT'S CAUSING THE DELAYS? ───────────────────────────

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


-- ── 6. THE SOUTHWEST DECEMBER 2022 STORY ────────────────────

SELECT
    al.AIRLINE,
    strftime(FlightDate::DATE, '%Y-%m')          AS month,
    COUNT(*)                                      AS flights,
    SUM(Cancelled)                                AS cancellations,
    ROUND(SUM(Cancelled) * 100.0 / COUNT(*), 1)  AS cancel_pct
FROM flights f
JOIN airlines al ON f.Reporting_Airline = al.IATA_CODE
WHERE al.AIRLINE = 'Southwest Airlines'
GROUP BY al.AIRLINE, month
ORDER BY month;


-- ── 7. WORST AIRPORTS ───────────────────────────────────────

SELECT
    ap.iata_code,
    ap.name,
    ap.municipality,
    COUNT(*)                                        AS departures,
    ROUND(AVG(f.DepDelay), 1)                       AS avg_dep_delay,
    ROUND(SUM(f.Cancelled) * 100.0 / COUNT(*), 1)  AS cancel_pct
FROM flights f
JOIN airports ap ON f.Origin = ap.iata_code
WHERE f.Cancelled = 0
GROUP BY ap.iata_code, ap.name, ap.municipality
HAVING departures > 10000
ORDER BY avg_dep_delay DESC
LIMIT 15;


-- ── 8. EXPORT TO PARQUET ────────────────────────────────────

-- Export — much smaller and faster than CSV
COPY flights TO 'data/flights/flights_all.parquet' (FORMAT PARQUET);

-- Read it back
SELECT COUNT(*) FROM 'data/flights/flights_all.parquet';
