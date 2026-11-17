-- Run in: DuckDB A, attached to lake, after 06_flights.sql.

-- Add a review-status column and compare the current schema with an
-- earlier snapshot.
-- In the full walkthrough, run after 07_history.sql.
-- History is optional for the schema example.
-- Run once: review_status must not exist yet.
-- review_status is an example annotation, not BTS data.

-- Save the snapshot before changing the schema.
SET VARIABLE before_schema_version = (SELECT max(snapshot_id) FROM lake.snapshots());

-- Existing rows read the default without rewriting their Parquet data.
ALTER TABLE flights ADD COLUMN review_status VARCHAR DEFAULT 'unreviewed';

SELECT flight_id, flight_date, origin, destination, review_status
FROM flights ORDER BY flight_id LIMIT 5;

-- Compare the earlier column set with the current one.
DESCRIBE SELECT * FROM flights AT (VERSION => getvariable('before_schema_version'));
DESCRIBE flights;
SELECT * FROM lake.snapshots();

-- Result: flights now includes review_status, with unreviewed as the
-- default. The earlier snapshot keeps its original schema.
