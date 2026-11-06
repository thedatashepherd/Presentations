-- Capture the current snapshot before changing data; avoid hard-coded version IDs.
SET VARIABLE before_version = (SELECT max(snapshot_id) FROM lake.snapshots());
BEGIN;
INSERT INTO orders VALUES (5001, 42, DATE '2026-10-14', 125.00);
ROLLBACK;
SELECT count(*) AS after_rollback FROM orders; -- 5000
BEGIN;
INSERT INTO orders VALUES (5001, 42, DATE '2026-10-14', 125.00);
COMMIT;
SELECT count(*) AS current_orders FROM orders; -- 5001
SELECT count(*) AS earlier_orders FROM orders AT (VERSION => getvariable('before_version')); -- 5000
SELECT * FROM lake.snapshots();
