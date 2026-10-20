-- Fabric 101 · Day of Data Orlando 2026
-- Warehouse views behind the RideTime report.
-- Create a Warehouse named wh_the_queue in the same workspace as lh_the_queue,
-- wait for the collector tables to appear in the Lakehouse SQL analytics endpoint,
-- then run each GO-separated batch in order.

-- v_dim_entity
-- Entity dimension: one row per entity_id, using the collector's current attributes.
-- Relate entity_id (one) to v_fact_wait_snapshot.entity_id (many).
-- Historical snapshots use current names and park attributes (Type 1 dimension).
CREATE VIEW [dbo].[v_dim_entity]
AS
SELECT
    [entity_id],
    [entity_name],
    [entity_type],
    [destination],
    [park_id],
    [park_name],
    [latitude],
    [longitude],
    [timezone]
FROM [lh_the_queue].[dbo].[dim_entity];

GO
GO

-- v_fact_wait_snapshot
-- Grain: one attraction per collection snapshot. Keep all collected history.
-- snapshot_date_utc is UTC, not the park's local calendar date.
-- Missing waits remain NULL; reported zero-minute waits remain zero.
CREATE VIEW [dbo].[v_fact_wait_snapshot]
AS
SELECT
    [snapshot_utc],
    CAST([snapshot_utc] AS date) AS [snapshot_date_utc],
    [entity_id],
    [park_id],
    [status],
    [standby_wait_min],
    [last_updated_utc]
FROM [lh_the_queue].[dbo].[fact_wait_snapshot];

GO
GO

-- v_wait_history
-- Run in wh_the_queue Warehouse, in the same Fabric workspace as lh_the_queue.
-- Wait until the collector tables appear in the lh_the_queue SQL analytics endpoint.
-- Execute each CREATE OR ALTER VIEW batch separately if the editor does not support GO.
-- This standalone script must be executed; afterward commit the Warehouse item through Fabric Source control.

CREATE   VIEW dbo.v_wait_history
AS
SELECT
    f.snapshot_utc,
    f.entity_id,
    d.entity_name,
    d.entity_type,
    d.destination,
    COALESCE(f.park_id, d.park_id) AS park_id,
    d.park_name,
    d.latitude,
    d.longitude,
    d.timezone,
    f.status,
    f.standby_wait_min,
    f.last_updated_utc
FROM [lh_the_queue].[dbo].[fact_wait_snapshot] AS f
LEFT JOIN [lh_the_queue].[dbo].[dim_entity] AS d ON d.entity_id = f.entity_id;

GO
GO

-- v_latest_waits
-- Use the latest whole collection, not each attraction's latest individual row.
-- This prevents stale attractions from being mixed into the current map.
CREATE   VIEW dbo.v_latest_waits
AS
SELECT
    h.snapshot_utc,
    h.entity_id,
    h.entity_name,
    h.entity_type,
    h.destination,
    h.park_id,
    h.park_name,
    h.latitude,
    h.longitude,
    h.timezone,
    h.status,
    h.standby_wait_min,
    h.last_updated_utc
FROM dbo.v_wait_history AS h
WHERE h.snapshot_utc = (SELECT MAX(snapshot_utc) FROM [lh_the_queue].[dbo].[fact_wait_snapshot]);

GO
GO

-- v_park_summary
-- Wait statistics include only OPERATING attractions with a reported wait.
-- A reported zero is valid; a missing wait remains NULL.
CREATE   VIEW dbo.v_park_summary
AS
SELECT
    snapshot_utc,
    destination,
    park_id,
    park_name,
    COUNT_BIG(*) AS attraction_count,
    SUM(CAST(CASE WHEN status = 'OPERATING' THEN 1 ELSE 0 END AS bigint)) AS operating_attraction_count,
    SUM(CAST(CASE WHEN status = 'OPERATING' AND standby_wait_min IS NOT NULL THEN 1 ELSE 0 END AS bigint)) AS reported_wait_attraction_count,
    AVG(CASE WHEN status = 'OPERATING' THEN CAST(standby_wait_min AS decimal(18,2)) END) AS avg_standby_wait_min,
    MAX(CASE WHEN status = 'OPERATING' THEN standby_wait_min END) AS max_standby_wait_min
FROM dbo.v_latest_waits
GROUP BY snapshot_utc, destination, park_id, park_name;

GO
GO
