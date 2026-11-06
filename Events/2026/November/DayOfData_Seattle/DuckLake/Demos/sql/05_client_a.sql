-- In client A, first read 01_attach.sql. Run each statement manually.
BEGIN;
INSERT INTO orders VALUES (6001, 42, DATE '2026-10-14', 75.00, 'store');
-- Switch to B before committing and compare counts.
COMMIT;
-- Switch to B again to observe the committed change.
