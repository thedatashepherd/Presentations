-- Run in: DuckDB B. Run one labeled block at a time.

-- A and B share one lake and PostgreSQL catalog.
-- Attach both with 05_attach.sql. Run 06_flights.sql and 08_schema.sql
-- in A first. 07_history.sql is optional for this example.
-- Run A's readiness query first. Both rows should be unreviewed.
-- Keep B in autocommit mode, with no open transaction.
-- Order: readiness, A1, B1, A2, B2, B3, A3.

-- B1: after A1, read flight 1 before A commits.
-- Expected: unreviewed. B cannot see A's uncommitted change.
SELECT flight_id, origin, destination, review_status
FROM flights
WHERE flight_id = 1;

-- Switch to A2 in 09_client_a.sql to commit the change.


-- B2: after A2 commits, run a fresh query.
-- Expected: reviewed-by-a.
SELECT flight_id, origin, destination, review_status
FROM flights
WHERE flight_id = 1;


-- B3: update flight 2. Autocommit commits the update immediately.
UPDATE flights
SET review_status = 'reviewed-by-b'
WHERE flight_id = 2;

SELECT flight_id, review_status
FROM flights
WHERE flight_id IN (1, 2)
ORDER BY flight_id;

-- Switch to A3 in 09_client_a.sql to verify B's committed change.
-- Result: A and B can read each other's committed annotations.
