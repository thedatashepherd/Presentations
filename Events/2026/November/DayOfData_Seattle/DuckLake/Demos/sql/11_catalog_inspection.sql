-- Run in: DBeaver, connected to PostgreSQL ducklake_catalog.

-- PostgreSQL tracks the lakehouse through these catalog tables.
-- Shown right after 06_flights.sql in the talk. These read-only
-- queries can run again after any later script to see what changed.

-- Which catalog tables exist?

SELECT
    table_name
FROM information_schema.tables
WHERE table_schema = 'public'
  AND table_name LIKE 'ducklake_%'
ORDER BY table_name;



-- How is the catalog configured?

SELECT *
FROM public.ducklake_metadata;



-- Which tables are tracked?

SELECT
    table_id,
    table_name,
    begin_snapshot,
    end_snapshot
FROM public.ducklake_table
ORDER BY table_id, begin_snapshot;



-- Which columns define the table?

SELECT
    table_id,
    column_id,
    column_name,
    column_type,
    begin_snapshot,
    end_snapshot
FROM public.ducklake_column
ORDER BY table_id, column_id, begin_snapshot;



-- Which Parquet files are tracked, including retained history?
-- begin_snapshot/end_snapshot describe each entry's lifetime.
-- A historical entry does not necessarily identify an active file.

SELECT
    table_id,
    data_file_id,
    path,
    record_count,
    begin_snapshot,
    end_snapshot
FROM public.ducklake_data_file
ORDER BY data_file_id;



-- What versions were committed?

SELECT
    snapshot_id,
    snapshot_time
FROM public.ducklake_snapshot
ORDER BY snapshot_id;
