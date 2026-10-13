-- ATTENDEE EDITION: replace the zero GUID with your test Account ID before running selected blocks.
-- Dataverse: inspect Account data and change one Account's status.
-- Connect SQL 4 CDS to the intended Dataverse environment.
-- Execute selected blocks. Running the whole file would change and reset the Account.
-- SQL 4 CDS uses Dataverse APIs for UPDATE; native Dataverse TDS is read-only.
-- The example uses Fourth Coffee's ID from this environment; use your own ID elsewhere.

-- [DV-1] Inspect Accounts and their primary Contacts.
-- Start with Account IDs and lookup values, then resolve the primary Contact name.
-- The primary Contact join keeps one row per Account. Sample baseline: 10 Accounts, 10 matches.
SELECT COUNT(*) AS account_count FROM account;

SELECT a.accountid, a.name, a.primarycontactid,
       a.statecode, a.statuscode, a.modifiedon
FROM account AS a;

SELECT a.accountid, a.name, a.primarycontactid,
       c.contactid, c.fullname AS primary_contact,
       a.statecode, a.statuscode, a.modifiedon
FROM account AS a
LEFT JOIN contact AS c ON c.contactid = a.primarycontactid
ORDER BY a.name;

SELECT COUNT(*) AS accounts_with_matching_primary_contact
FROM account AS a
INNER JOIN contact AS c ON c.contactid = a.primarycontactid;

-- [DV-2] Inspect Fourth Coffee's current status.
-- Verify the ID and name before running an UPDATE.
-- Active: statecode 0 / statuscode 1. Inactive: statecode 1 / statuscode 2.
SELECT accountid, name, primarycontactid, statecode, statuscode, modifiedon
FROM account
WHERE accountid = '00000000-0000-0000-0000-000000000000';

-- [DV-4] Deactivate Fourth Coffee and confirm the source result.
-- Changes only the specified Account when its name matches.
-- Expect one changed row from Active, or zero if already Inactive; inspect the SELECT result.
-- Query the Fabric reporting result later to check propagation.
UPDATE account
SET statecode = 1, statuscode = 2
WHERE accountid = '00000000-0000-0000-0000-000000000000'
  AND name = 'Fourth Coffee'
  AND (statecode <> 1 OR statuscode <> 2);

SELECT accountid, name, statecode, statuscode, modifiedon
FROM account
WHERE accountid = '00000000-0000-0000-0000-000000000000';

-- [DV-5] Reset reference.
-- DV-3 restores Active (0/1). FB-5 checks the corresponding Fabric result.

-- ============================================================
-- BEFORE-SESSION BASELINE / AFTER-SESSION RESET
-- Select DV-3 only when needed; keep it out of the live sequence.
-- ============================================================

-- [DV-3] Restore Fourth Coffee to Active.
-- Run only to establish the Active baseline before presenting or reset after the session.
-- Restores state/status only; modifiedon, audit history and automation may be affected.
UPDATE account
SET statecode = 0, statuscode = 1
WHERE accountid = '00000000-0000-0000-0000-000000000000'
  AND name = 'Fourth Coffee'
  AND (statecode <> 0 OR statuscode <> 1);

SELECT accountid, name, statecode, statuscode, modifiedon
FROM account
WHERE accountid = '00000000-0000-0000-0000-000000000000';
