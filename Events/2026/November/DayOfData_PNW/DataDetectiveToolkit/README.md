# The Data Detective’s Toolkit: Diagnose, Monitor, and Fix with Semantic Link Labs

Jason Romans · Day of Data PNW · November 7, 2026 · Vancouver, Washington

## Session resources

- [Slides (PDF)](PNW2026_DataDetectiveToolkit.pdf)
- [Session notebooks](Demos)
- [More presentations](https://slides.datashepherd.dev/)

## Notebook running order

| Notebook | Investigation |
|---|---|
| [1. Model investigation](Demos/1.InitialSFCaseFiles.ipynb) | Cases 1–6: model inventory, relationships, DAX, referential integrity, SQL endpoint visibility, and table recovery |
| [2. Best Practice Analyzer](Demos/2.SFCaseFiles_BPA.ipynb) | Model rules, bulk scans, and BPA reporting |
| [3. Lineage repair](Demos/3.SFCaseFiles_LineageRepair.ipynb) | Inspect broken references, repair through the lineage UI, and verify the saved report |
| [4. Refresh Manager](Demos/4.RefreshManager.ipynb) | Refresh history, execution details, refresh controls, and schedules |
| [5. VertiPaq Analyzer](Demos/5.SFCaseFiles_VertipaqAnalyzer.ipynb) | Compare model memory and the cost of hidden auto-date tables |
| [6. Report analysis](Demos/6.SFCaseFiles_ReportAnalysis.ipynb) | Inspect filters, visuals, bookmarks, interactions, report measures, and report BPA findings |

## Use the notebooks

Import the six `.ipynb` files into Microsoft Fabric. Each notebook contains its own configuration and imports; no shared setup notebook is required. Use the package version demonstrated in the session, **`semantic-link-labs==0.18.1`**, through an attached Fabric Environment or the optional installation cell. Restart the session if requested, then run configuration and imports.

Set the model/report names and `WORKSPACE` in each configuration cell. `WORKSPACE = None` targets the notebook’s current workspace. The sample investigations reference specific tables and measures, so using a different schema also requires adapting those cells.

| Notebook | Sample prerequisites |
|---|---|
| 1 | `SFCaseFiles`, `SFCaseFiles_RelationshipDiscover`, `Trudoso10K`, `Trudoso10K_WithAutoDate`, and `Trudoso10K_RI`. Cases 5–6 use PySpark and an attached Lakehouse; the session used `EvidenceLocker`. |
| 2 | `SFCaseFiles` and `Trudoso10K_WithAutoDate`. Attach a Lakehouse for exports, bulk-scan results, and BPA reporting. |
| 3 | `SFCaseFiles` and a PBIR report named `SFCaseFiles_PNW_Lineage`. The demo report contains an invalid `Incident Count` reference; the intended measure is `Total Incidents`. The notebook inspects references, opens the lineage UI for the repair, then checks the saved report again. |
| 4 | A published `Trudoso10K` model with configured data-source credentials and permissions for the refresh or schedule actions you choose. |
| 5 | Published and processed `Trudoso10K` and `Trudoso10K_WithAutoDateXL` models. A Lakehouse is needed only for optional CSV/Delta exports. |
| 6 | `SFCaseFiles_ReportLab` and its PBIR report `SFCaseFiles_ReportLab_Thin`. The later report-BPA export section uses PySpark and an attached Lakehouse. |

Model/report fixtures and datasets are not bundled here. Prepare equivalent sample items in your workspace or adapt the notebook targets. Run one investigation at a time: table writes/recovery, report repairs, refresh or schedule changes, and BPA exports modify workspace items. The report-BPA export example drops and recreates its sample results table.

These are the session notebook sources exported without saved outputs or presenter workspace bindings. JSON structure and Python syntax have been checked; the exports have not been run in a fresh attendee workspace.

[Semantic Link Labs](https://github.com/microsoft/semantic-link-labs) · [The Data Shepherd](https://datashepherd.dev/)
