# FetchXML — first inspection demo

Load 01-Account-Three-Fields.xml in XrmToolBox > FetchXML Builder using Open > File. Connect to the same Dataverse environment as Metadata Browser and SQL 4 CDS.

1. Expand the account entity in the visual tree.
2. Show three selected attributes: accountid, name, createdon.
3. Execute the query. It requests up to 10 Accounts, sorted by name and then ID.
4. Compare the logical column names with the returned records.
5. Optional visual edit: add a filter on name equal to Fourth Coffee, then execute again. Remove the filter or reload the file to reset.

This is a retrieval query; it does not update data. Actual rows depend on the connected environment and user's access. Prepared sample expectation: 10 Accounts if all ten remain readable. XML syntax checked locally; execute in the tenant during rehearsal.

Sources:
https://fetchxmlbuilder.com/origdocs/
https://learn.microsoft.com/en-us/power-apps/developer/data-platform/fetchxml/order-rows
