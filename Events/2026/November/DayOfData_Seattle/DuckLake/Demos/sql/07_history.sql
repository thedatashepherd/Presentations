-- Run in: DuckDB A, in the same session used to load flights.

-- Compare rollback, commit, and an earlier snapshot using another day
-- of Seattle flights.
-- Run once in DuckDB after 06_flights.sql and before 08_schema.sql.

-- 1. Stage the next day's flights (February 1).
-- This temporary staging table is local to A, not stored in DuckLake.
-- Run once after loading January; rerunning would append duplicates.
-- Stage February 1 flights in this session before changing the
-- lakehouse.
CREATE TEMP TABLE incoming_flights AS
SELECT
    1000000 + row_number() OVER (
        ORDER BY FlightDate, Reporting_Airline, Origin, Dest,
                 DepDelay, ArrDelay, Distance
    ) AS flight_id,
    FlightDate AS flight_date,
    Reporting_Airline AS airline,
    Origin AS origin,
    Dest AS destination,
    DepDelay AS departure_delay_minutes,
    ArrDelay AS arrival_delay_minutes,
    CAST(Cancelled AS BOOLEAN) AS cancelled,
    Distance AS distance_miles
FROM read_parquet('./source-data/flights/flights_all.parquet')
WHERE FlightDate = DATE '2024-02-01'
  AND (Origin = 'SEA' OR Dest = 'SEA');

-- 2. Save our starting point.
-- Remember the committed snapshot and row count before any changes.
SET VARIABLE before_version = (SELECT max(snapshot_id) FROM lake.snapshots());
SET VARIABLE before_count = (SELECT count(*) FROM flights);
SELECT count(*) AS incoming_flights FROM incoming_flights;

-- 3. Try an insert, then roll it back.
-- BY NAME matches columns by name rather than position.
-- Inside the transaction: 24,295 flights. After rollback: 23,508.
BEGIN;
INSERT INTO flights BY NAME SELECT * FROM incoming_flights;
SELECT count(*) AS inside_transaction FROM flights;
ROLLBACK;
SELECT getvariable('before_count') AS before_insert,
       count(*) AS after_rollback,
       count(*) = getvariable('before_count') AS rollback_preserved_count
FROM flights;

-- 4. Insert the same batch again and commit it.
BEGIN;
INSERT INTO flights BY NAME SELECT * FROM incoming_flights;
COMMIT;

-- 5. Query before and after the commit.
-- AT (VERSION ...) reads the earlier version; it does not restore it.
-- Before: 23,508 flights through January 31.
-- After: 24,295 flights through February 1.
SELECT
    'Before commit' AS table_state,
    count(*) AS flights,
    max(flight_date) AS latest_flight_date
FROM flights AT (VERSION => getvariable('before_version'))

UNION ALL

SELECT
    'After commit' AS table_state,
    count(*) AS flights,
    max(flight_date) AS latest_flight_date
FROM flights
ORDER BY latest_flight_date, table_state DESC;

-- Show the committed versions in chronological snapshot order.
SELECT snapshot_id, snapshot_time
FROM lake.snapshots()
ORDER BY snapshot_id;

-- Result: Rollback keeps 23,508 flights. Committing 787 more gives
-- 24,295; the earlier snapshot still has 23,508.

-- NEXT: stay in DuckDB A and continue with 08_schema.sql.

