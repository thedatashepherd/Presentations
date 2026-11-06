-- Run in psql, not DuckDB. Inspect read-only; do not edit catalog tables.
\dt *.*ducklake*
SELECT table_schema, table_name FROM information_schema.tables
WHERE table_name LIKE 'ducklake_%' ORDER BY table_schema, table_name;
-- Locate the metadata schema above before querying ducklake_snapshot,
-- ducklake_table, ducklake_column, and ducklake_data_file.
