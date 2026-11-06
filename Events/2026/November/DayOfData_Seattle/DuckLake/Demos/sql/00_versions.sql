-- Read-only checkpoint; repeat after ATTACH to see loaded extensions.
SELECT version() AS duckdb_engine;
SELECT extension_name, extension_version, installed, loaded
FROM duckdb_extensions()
WHERE extension_name IN ('ducklake', 'postgres', 'quack')
ORDER BY extension_name;
-- Record DuckLake catalog/spec format separately from engine/extension versions.
