-- Run in: DuckDB A and DuckDB B, once in each session.
-- In B, the same attachment can run with .read sql/05_attach.sql

-- Connect DuckDB to a DuckLake catalog stored in PostgreSQL.
-- Run once in each fresh DuckDB session started with
-- 02_open-duckdb.ps1.
-- PostgreSQL must be running before this connection can succeed.

-- Install the extensions if needed, then load them into this session.
INSTALL ducklake;
INSTALL postgres;
LOAD ducklake;
LOAD postgres;

-- ATTACH again, as in 04_duckdb_files.sql. There it opened one local
-- .duckdb file; here it opens a DuckLake. PostgreSQL stores the
-- catalog; DATA_PATH is where DuckLake writes its data files.
-- No password appears here: 02_open-duckdb.ps1 read it from .env into
-- the PGPASSWORD environment variable.
-- Inlining is disabled so analytical rows go into Parquet files.
ATTACH 'ducklake:postgres:dbname=ducklake_catalog host=127.0.0.1 port=55432 user=ducklake_demo' AS lake
  (DATA_PATH './ducklake/', DATA_INLINING_ROW_LIMIT 0);
-- Use lake as the default database for the following SQL.
USE lake;


-- Inspect the attachment and its connection path.
SELECT database_name, type, path
FROM duckdb_databases()
WHERE database_name = 'lake';

-- Confirm the database and schema used by unqualified table names.
SELECT current_database() AS active_database,
       current_schema() AS active_schema;

-- List only persistent tables in lake. Session objects are separate.
SELECT schema_name, table_name
FROM duckdb_tables()
WHERE database_name = 'lake'
ORDER BY schema_name, table_name;

-- Result: This session now uses lake.main. The catalog is connected;
-- this script does not load flight data.


