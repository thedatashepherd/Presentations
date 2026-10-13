# Summit NA demo resources

## 1. Inspect Dataverse data and metadata

Open the [attendee Excel toolkit](Connection%20Demos/Dataverse_Connection_and_Metadata_Toolkit_Attendee.xlsx). It retains the saved test rows, metadata, query tables, and Power Query examples from the session.

In Excel, choose **Data > Get Data > Launch Power Query Editor > Home > Manage Parameters**. Replace the three environment placeholders together:

| Parameter | Placeholder / default | Set to |
| --- | --- | --- |
| `pDataverseHost` | `YOURORG.crm.dynamics.com` | Your environment's Dataverse/TDS hostname, without `https://` or a path |
| `pDataverseApiHost` | `YOURORG.api.crm.dynamics.com` | The Web API hostname for the same environment |
| `pDataverseDatabaseName` | `YOUR_DATAVERSE_DATABASE_NAME` | The database name exposed by your Dataverse TDS endpoint |
| `pMetadataTables` | `account,contact` | Comma-separated logical table names to inspect |
| `pFetchXMLRowLimit` | `10` | A positive whole-number sample limit |

The values shown on **Connections and Setup** are reference examples. Edit the actual Power Query parameters, then use Organizational account authentication for your own environment. SQL and Dataverse connector queries require the TDS endpoint to be enabled and accessible. Hostnames vary by environment and region; copy yours rather than assuming the example suffix applies.

Close & Load, then refresh `account` and `FetchXML_AccountSample`. Refresh `DataverseTableMetadata` and `Selected_Table_Columns` to inspect identity and lookup targets. The optional full-environment `DataverseColumnMetadata` query makes two API calls per table and may take longer. Refresh replaces the saved test rows with your environment's results.

[Power Query source](Connection%20Demos/PowerQuery_Section1.m) is also provided for inspection and reuse. The workbook already contains these queries.

For the small retrieval example, load [Account FetchXML](FetchXML/01-Account-Three-Fields.xml) in XrmToolBox FetchXML Builder. See [FetchXML instructions](FetchXML/README.md).

## 2. Query the source and linked Fabric data

- [Dataverse SQL 4 CDS](SQL/01-Dataverse-SQL4CDS.sql): inspect Accounts and primary Contacts, change a test Account's state/status, and reset it.
- [Fabric SQL analytics endpoint](SQL/02-Fabric-SSMS.sql): inspect linked tables, resolve contact names and state/status labels, create a reporting view, and reconcile a changed record.

Use your own test environment. Replace every zero Account GUID with your chosen test Account ID and update the `Fourth Coffee` name guard if you use another record. Execute selected blocks: the Dataverse script includes both an update and a reset. Native Dataverse TDS is read-only; the update examples use SQL 4 CDS through Dataverse APIs.

For Fabric, prepare a consumer lakehouse with `account`, `contact`, `StateMetadata`, and `StatusMetadata` shortcuts to linked Dataverse tables. Connect SSMS to that consumer's SQL analytics endpoint with Microsoft Entra authentication. Run FB-1 and FB-2 to inspect schema and label uniqueness, FB-3 to inspect the join, FB-4 to create the view, and FB-6 to validate it. Use FB-5 after changing the source record. The scripts assume `dbo` and English labels (`1033`); adjust them for your environment. A view stores the query definition rather than materializing a Delta table.

Data propagation and SQL endpoint visibility are separate checks. These examples do not establish a synchronization-latency guarantee. FB-7 is optional diagnostics and depends on the endpoint's metadata-sync capability and permissions.

## 3. Optional Fabric Link migration checks

Import the [attendee migration notebook](Notebook%20Uploads/Fabric_Link_Migration_Check_Attendee.ipynb) into Fabric and follow its setup and run order. Configure your source/consumer workspaces and attach a separate writable snapshot lakehouse that survives migration. Save a `before` baseline and compare an `after` run with the same migration run name.

The notebook has no saved execution outputs or attached lakehouse identifiers. Normal runs read selected Fabric items and write diagnostic snapshots. Optional shortcut repair and SQL metadata refresh remain disabled by default. Live execution against an attendee environment has not been verified here.

## Connection examples shown in the talk

Create Power BI connection files from **Analyze in Power BI** in your own Dataverse environment. Presenter PBIX/PBIDS files, duplicate workbooks, rehearsal runbooks, and historical Fabric Git exports are outside this attendee package.
