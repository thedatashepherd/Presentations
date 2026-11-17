-- Run in: DuckDB A or DuckDB B, at the DuckDB prompt.

-- Check the DuckDB engine version and the installed DuckLake and
-- PostgreSQL extensions. Also show how the CLI ends a SQL statement.
-- Run again after attaching to see which extensions are loaded.

-- Without a semicolon, Enter continues the SQL statement.
-- Enter just the SELECT line to see the continuation prompt.
-- Ctrl+C cancels an unfinished statement.
-- The semicolon on the next line completes and runs that statement.

SELECT version() AS duckdb_engine
;

-- With a semicolon, the complete statement runs when you press Enter.
SELECT version() AS duckdb_engine;

-- The engine and its extensions have separate versions.
-- postgres_scanner is the PostgreSQL extension's full name. postgres
-- is its alias, used by INSTALL and LOAD in 05_attach.sql.
SELECT extension_name, extension_version, installed, loaded
FROM duckdb_extensions()
WHERE extension_name IN ('ducklake', 'postgres', 'postgres_scanner')
ORDER BY extension_name;

-- Result: The results identify the engine and extension versions used
-- by this session.
