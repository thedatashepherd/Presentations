# Fabric 101 demo resources

The session's live demos were walkthroughs in a Fabric workspace. These files let you rebuild the same route, from the slide **"Follow one piece of data"**, in your own workspace:

**Ride wait times → Notebook (hourly) → Lakehouse → Warehouse views → Model and report**

A Fabric trial capacity is enough. Names below match the session; if you choose different names, update them in the SQL and the report connection.

## What's here

| Folder | Item | Slide section |
|---|---|---|
| `1_Collect` | `ThemePark_WaitTime_Collector.ipynb` — pure Python notebook that pulls Orlando park, attraction and wait-time data and writes Delta tables | The Lake · Data Engineering |
| `2_Prepare` | `RideTime_DirectLake_Prepare.ipynb` — Spark notebook that builds the date, hour and reporting tables for the Direct Lake model | Data Engineering |
| `3_Warehouse` | `theme-park-views.sql` — the five views behind the report | Data Warehouse · *Behind the report* |
| `4_Report` | `RideTime/` — the Import report as a Power BI project (`.pbip`); `RideTimeDirectLake-model-setup.tmdl` — measures and relationships for the Direct Lake version | Power BI · *Reports* |
| `data` | `dim_entity.csv` and `live_waits_snapshot.csv` — a ready-made snapshot of Orlando park data (one collection, 10 Oct 2026) for the **Your first report** exercise | The Take-Home Map |

## Your first report (slide 45)

No notebook needed. Use the files in `data`:

1. **Workspace.** Use a workspace with capacity and create a Lakehouse.
2. **Upload.** Upload `dim_entity.csv` and `live_waits_snapshot.csv` to the Lakehouse **Files** section.
3. **Table.** Load each file to a Delta table (… menu → **Load to Tables**). Check the row counts (929 entities, 477 wait readings) and that `standby_wait_min` is numeric.
4. **Model.** Create a Direct Lake semantic model from both tables and relate `live_waits_snapshot.entity_id` to `dim_entity.entity_id`.
5. **Report.** Build a visual that answers a question, such as average standby wait by park.

`live_waits_snapshot` is one collection, so it shows a moment in time, not a trend. For history, use the full route below.

## Rebuild the full demo route

1. **Workspace and Lakehouse.** In a workspace with Fabric capacity, create a Lakehouse named `lh_the_queue` (schemas enabled).
2. **Collect.** Import `1_Collect/ThemePark_WaitTime_Collector.ipynb`, attach `lh_the_queue` as the default Lakehouse, and run it. It creates `dim_entity` and appends to `fact_wait_snapshot`. Run it a few times, or schedule it hourly, to build up history.
3. **Shape.** Create a Warehouse named `wh_the_queue` in the same workspace. Once the tables show up in the Lakehouse SQL analytics endpoint, run `3_Warehouse/theme-park-views.sql` one batch at a time.
4. **Report (Import).** Open `4_Report/RideTime/RideTime.pbip` in Power BI Desktop. In the model, replace `YOUR-SQL-ENDPOINT` with your Warehouse's SQL connection string (Warehouse → Settings → SQL endpoint), then refresh.
5. **Optional: Direct Lake.** Import `2_Prepare/RideTime_DirectLake_Prepare.ipynb`, attach `lh_the_queue`, and run it after the collector. Create a Direct Lake semantic model on `dim_entity`, `fact_wait_snapshot_reporting`, `dim_date_utc` and `dim_hour_utc`, then paste `RideTimeDirectLake-model-setup.tmdl` into the model's TMDL view to add the measures and relationships. Adjust the source expression name to match your model.

## Notes

- All dates and hours are **UTC**. Averages are per observation, and "operating" counts include overnight closures — it is not uptime.
- Attach your own Lakehouse to each notebook after import.
- Park and wait-time data in `data` and from the collector comes from [ThemeParks.wiki](https://themeparks.wiki), via their public API. It is shared here for learning only; credit ThemeParks.wiki if you reuse it.
