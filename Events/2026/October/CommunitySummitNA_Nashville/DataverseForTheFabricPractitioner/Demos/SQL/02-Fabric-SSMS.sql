-- ATTENDEE EDITION: replace the zero GUID with your test Account ID before running selected blocks.
-- Fabric: inspect linked Dataverse data and build a reporting view.
-- Connect to the consumer lakehouse SQL analytics endpoint.
-- Required shortcuts: account, contact, StateMetadata and StatusMetadata.
-- Copy the current endpoint server and database from Fabric; use Microsoft Entra authentication.
-- Execute selected blocks. Run FB-4 to create the view before using FB-5 or FB-6.
-- Linked tables are read-only; the reporting view is a SQL object in this endpoint.
-- The example Account ID is specific to this environment; replace it for your own data.

-- [FB-1] Inspect the connected database, available columns and Account data.
-- Confirm the required tables and columns before running the joins.
-- Sample baseline: 10 Accounts and 10 matching primary Contacts.
SELECT DB_NAME() AS endpoint_database, SYSUTCDATETIME() AS observed_at_utc;
SELECT TABLE_SCHEMA, TABLE_NAME, COLUMN_NAME, DATA_TYPE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'dbo'
  AND TABLE_NAME IN ('account', 'contact', 'StateMetadata', 'StatusMetadata')
ORDER BY TABLE_NAME, ORDINAL_POSITION;

SELECT COUNT(*) AS account_count FROM dbo.account;
SELECT accountid, name, primarycontactid, statecode, statuscode, modifiedon
FROM dbo.account ORDER BY name;
SELECT COUNT(*) AS accounts_with_matching_primary_contact
FROM dbo.account AS a
INNER JOIN dbo.contact AS c ON c.contactid = a.primarycontactid;

-- [FB-3] Resolve Contact names and state/status labels.
-- LEFT JOIN preserves Accounts with missing relationships or labels.
-- Status Reason is matched on BOTH State and Status.
-- Entity, language (1033) and localization filters belong in the JOIN conditions.
SELECT a.accountid, a.name AS account_name, a.primarycontactid,
       c.contactid AS resolved_contact_id, c.fullname AS primary_contact_name,
       a.statecode, sm.LocalizedLabel AS account_state,
       a.statuscode, stm.LocalizedLabel AS status_reason, a.modifiedon
FROM dbo.account AS a
LEFT JOIN dbo.contact AS c ON c.contactid = a.primarycontactid
LEFT JOIN dbo.StateMetadata AS sm
  ON sm.EntityName = 'account' AND sm.[State] = a.statecode
 AND sm.LocalizedLabelLanguageCode = 1033 AND sm.IsUserLocalizedLabel = 0
LEFT JOIN dbo.StatusMetadata AS stm
  ON stm.EntityName = 'account' AND stm.[State] = a.statecode
 AND stm.[Status] = a.statuscode
 AND stm.LocalizedLabelLanguageCode = 1033 AND stm.IsUserLocalizedLabel = 0
ORDER BY a.name;
GO

-- [FB-5] Compare Fourth Coffee's source codes with the reporting labels.
-- After DV-4: state/status 1/2 and Inactive/Inactive.
-- After DV-3: state/status 0/1 and Active/Active.
-- The second query requires the FB-4 view in this endpoint.
-- observed_at_utc is query time; modifiedon is the source modification time.
-- A difference alone does not establish a guaranteed synchronization latency.
SELECT SYSUTCDATETIME() AS observed_at_utc,
       accountid, name, statecode, statuscode, modifiedon
FROM dbo.account
WHERE accountid = '00000000-0000-0000-0000-000000000000';
SELECT SYSUTCDATETIME() AS observed_at_utc, *
FROM dbo.vw_SummitNA_AccountReporting
WHERE accountid = '00000000-0000-0000-0000-000000000000';

-- [FB-4] Create a reusable Account reporting view.
-- Execute the complete CREATE OR ALTER VIEW batch, including GO.
-- Requires CREATE VIEW permission and ALTER permission to replace an existing view.
-- A SQL view stores the query definition; it does not materialize a Delta table.
CREATE OR ALTER VIEW dbo.vw_SummitNA_AccountReporting
AS
SELECT a.accountid, a.name AS account_name, a.primarycontactid,
       c.contactid AS resolved_contact_id, c.fullname AS primary_contact_name,
       a.statecode, sm.LocalizedLabel AS account_state,
       a.statuscode, stm.LocalizedLabel AS status_reason, a.modifiedon
FROM dbo.account AS a
LEFT JOIN dbo.contact AS c ON c.contactid = a.primarycontactid
LEFT JOIN dbo.StateMetadata AS sm
  ON sm.EntityName = 'account' AND sm.[State] = a.statecode
 AND sm.LocalizedLabelLanguageCode = 1033 AND sm.IsUserLocalizedLabel = 0
LEFT JOIN dbo.StatusMetadata AS stm
  ON stm.EntityName = 'account' AND stm.[State] = a.statecode
 AND stm.[Status] = a.statuscode
 AND stm.LocalizedLabelLanguageCode = 1033 AND stm.IsUserLocalizedLabel = 0;
GO

-- [FB-2] Inspect state/status label mappings and check their uniqueness.
-- Expected: one localized label per filtered State or State/Status key.
-- Duplicate-key queries should return no rows. Duplicates can multiply Account rows;
-- resolve the cause rather than masking it with DISTINCT.
SELECT [State], LocalizedLabel
FROM dbo.StateMetadata
WHERE EntityName = 'account' AND LocalizedLabelLanguageCode = 1033
  AND IsUserLocalizedLabel = 0
ORDER BY [State];

SELECT [State], [Status], LocalizedLabel
FROM dbo.StatusMetadata
WHERE EntityName = 'account' AND LocalizedLabelLanguageCode = 1033
  AND IsUserLocalizedLabel = 0
ORDER BY [State], [Status];

SELECT [State], COUNT(*) AS label_rows
FROM dbo.StateMetadata
WHERE EntityName = 'account' AND LocalizedLabelLanguageCode = 1033
  AND IsUserLocalizedLabel = 0
GROUP BY [State] HAVING COUNT(*) <> 1;
SELECT [State], [Status], COUNT(*) AS label_rows
FROM dbo.StatusMetadata
WHERE EntityName = 'account' AND LocalizedLabelLanguageCode = 1033
  AND IsUserLocalizedLabel = 0
GROUP BY [State], [Status] HAVING COUNT(*) <> 1;

-- [FB-6] Validate reporting grain and completeness.
-- Sample baseline: 10 reporting rows and 10 distinct Account IDs.
-- Exception queries should return no rows: duplicate IDs, missing relationships/labels,
-- or unexpected state/status combinations.
SELECT COUNT(*) AS raw_account_rows FROM dbo.account;
SELECT COUNT(*) AS reporting_rows,
       COUNT(DISTINCT accountid) AS distinct_accounts
FROM dbo.vw_SummitNA_AccountReporting;
SELECT accountid, COUNT(*) AS reporting_rows
FROM dbo.vw_SummitNA_AccountReporting
GROUP BY accountid HAVING COUNT(*) <> 1;
SELECT * FROM dbo.vw_SummitNA_AccountReporting
WHERE primarycontactid IS NULL OR resolved_contact_id IS NULL
   OR account_state IS NULL OR status_reason IS NULL
   OR NOT ((statecode = 0 AND statuscode = 1)
        OR (statecode = 1 AND statuscode = 2));

-- [FB-7] Inspect SQL endpoint metadata synchronization.
-- This DMV requires an endpoint using New metadata sync and appropriate permissions.
-- is_blocked = 1 indicates a blocked table update.
-- Endpoint refresh affects SQL metadata/data visibility, not upstream Dataverse sync.
-- Optional table refresh (New metadata sync):
-- EXEC sys.sp_dw_refresh_ext_table N'dbo.account';
SELECT * FROM sys.dm_db_external_tables_log_status;

