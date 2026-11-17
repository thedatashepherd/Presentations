-- Run in: DuckDB A. Run one labeled block at a time.

-- A and B share one lake and PostgreSQL catalog.
-- Attach both with 05_attach.sql. Run 06_flights.sql and 08_schema.sql
-- in A first. 07_history.sql is optional for this example.
-- Keep B in autocommit mode, with no open transaction.
-- Order: readiness, A1, B1, A2, B2, B3, A3.

-- Readiness: both rows should exist and show unreviewed.
-- Otherwise, stop and check the earlier setup before continuing.
SELECT flight_id, review_status
FROM flights
WHERE flight_id IN (1, 2)
ORDER BY flight_id;


-- A1: begin and update flight 1. Leave the transaction open.
BEGIN;
UPDATE flights
SET review_status = 'reviewed-by-a'
WHERE flight_id = 1;

SELECT flight_id, origin, destination, review_status
FROM flights
WHERE flight_id = 1;

-- Switch to B1 in 10_client_b.sql before running A2.


-- A2: after B1 reads unreviewed, commit A's change.
COMMIT;

-- Switch to B2, then B3 in 10_client_b.sql.


-- A3: after B3, read both committed changes from A.
SELECT flight_id, review_status
FROM flights
WHERE flight_id IN (1, 2)
ORDER BY flight_id;

-- Result: flight 1 is reviewed-by-a; flight 2 is reviewed-by-b.
-- Both sessions use the same lake without restarting or reattaching.
