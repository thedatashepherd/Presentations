# Jax Data User Group - demo resources

[Notebook demo reference (PDF)](Jax_Pure_Python_Notebook_Demo_Reference.pdf) - the five core notebooks and optional Polars exercise, with code and explanations for working through the examples.

## Run the notebooks

Import the `.ipynb` files into Microsoft Fabric as **Pure Python** notebooks. Attach your own schema-enabled Lakehouse named `lh_pond` as the default Lakehouse. These notebooks use Fabric's `notebookutils` and Lakehouse mount; they are not standalone local Python demos.

Run in order:

0. **Setup** - download the 2025 flight files and reference data; create the January Delta table and optional Excel workbook.
1. **Query a Lakehouse File** - query Parquet directly with DuckDB.
2. **Friendly SQL** - analytical SQL with less scaffolding.
3. **CSV to Parquet** - compare storage formats and equivalent results.
4. **Query Data Where It Lives** - Lakehouse Parquet, Delta and public Blob; optional shortcut, private Blob and Excel examples.
5. **Polars SQL Encore** - optional bonus; follow its upgrade and restart instructions in a fresh session.

The attendee setup uses `DATA_SCOPE = "one_year"`; the four-year validation path is optional. Setup writes demo data to your attached Lakehouse and replaces the derived `dbo.flights_202501` table and workbook. Optional publishing to `dbo.busiest_airports`, public Blob, shortcut and private-storage examples are disabled until you choose to enable them. Upload the January flight file to your own Blob storage and replace the public/private storage and Key Vault placeholders before enabling those examples.

Attach your own Lakehouse after importing each notebook. Use your workspace settings to choose the Python node size. The reference PDF contains the same six notebooks, including the optional Polars exercise.
