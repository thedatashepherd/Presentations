-- In a second in-memory DuckDB client, first read 01_attach.sql.
SELECT count(*) FROM orders;
-- Repeat after A commits. Use fresh autocommit statements.
SELECT count(*) FROM orders;
