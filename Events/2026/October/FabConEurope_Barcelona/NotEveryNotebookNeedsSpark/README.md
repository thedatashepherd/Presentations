# Not Every Notebook Needs Spark: SQL-First Analytics with Pure Python

Jason Romans — The Data Shepherd · FabCon Europe 2026 · October 1, 2026 · Barcelona, Spain

## Slides

[Download the presentation PDF](TH08_Not%20Every%20Notebook%20Needs%20Spark%20SQL-First%20Analytics%20with%20Pure%20Python_Jason%20Romans.pdf)

## Run the demos

Download the notebooks from [Demos](Demos), then import the `.ipynb` files into your Microsoft Fabric workspace. Select the **Pure Python** runtime and create a Lakehouse named `lh_pond`. Attach it as the default Lakehouse to each notebook. These notebooks use Fabric paths and `notebookutils`.

Run in this order:

1. **0. Setup** — downloads the OPDI European flight data and airport/airline reference files. Keep `DATA_SCOPE = "one_year"` for the 2025 demo; `"full"` downloads 2022–2025. Run all setup cells, including the Delta table step.
2. **1. Query a Lakehouse File** — query Lakehouse files with DuckDB.
3. **2. Friendly SQL** — explore DuckDB SQL features.
4. **3. CSV to Parquet** — convert an archived CSV export to Parquet.
5. **4. Query Data Where It Lives** — query Lakehouse files and Delta. The public Blob, shortcut, private Blob, and Excel examples are optional.

Setup downloads data rather than bundling it here. Allow outbound HTTPS and enough Lakehouse storage. If upgrading DuckDB does not change the loaded version, restart the Python session before continuing.

For the optional public Blob example, upload `flight_list_202501.parquet` from your setup data to your own public Blob container, replace the `PUBLIC_BLOB` URL placeholders, and set `RUN_PUBLIC_BLOB = True`. For the optional shortcut example, create a `blob_flights` shortcut in Lakehouse Files targeting your container, then set `RUN_SHORTCUT = True`. For the optional private Blob example, replace the `YOUR-*` placeholders with your resources and configure the Key Vault secret before enabling `RUN_PRIVATE_BLOB`.

Notebooks contain no saved execution output or presenter Lakehouse bindings. Attach your own default Lakehouse after import.
