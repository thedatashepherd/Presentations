# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "jupyter",
# META     "jupyter_kernel_name": "python3.12"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "e4e23765-a799-4c3c-a9ef-05c053cd6611",
# META       "default_lakehouse_name": "lh_duck_pond",
# META       "default_lakehouse_workspace_id": "cdef1857-04ff-41af-bd33-a36bf6a59d9e",
# META       "known_lakehouses": [
# META         {
# META           "id": "e4e23765-a799-4c3c-a9ef-05c053cd6611"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

# MAGIC %%configure -f
# MAGIC {
# MAGIC     "vCores": 2
# MAGIC }

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

# Uncomment to install or upgrade DuckDB
# %pip install duckdb -U

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

# DuckDB 101 — Flight Delays Demo
# Dataset : US Airline On-Time Performance (BTS) · 2022–2024 · ~21M flights
# Lakehouse: lh_duck_pond
# Tables  : flights · airlines · airports

import duckdb
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import time

DATA = "/lakehouse/default/Files/flights"

con = duckdb.connect()
print("DuckDB", duckdb.__version__)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

# ── 1. READING FILES ─────────────────────────────────────────
# DuckDB reads directly from the Lakehouse — no import step.

df = con.sql(f"SELECT * FROM read_csv_auto('{DATA}/flights_2023.csv') LIMIT 5").df()
display(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

# Inspect the schema
df = con.sql(f"DESCRIBE SELECT * FROM read_csv_auto('{DATA}/flights_2023.csv')").df()
display(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

# Instant data profile
df = con.sql(f"SUMMARIZE SELECT * FROM read_csv_auto('{DATA}/flights_2023.csv')").df()
display(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

# ── 2. LOAD THE THREE TABLES ─────────────────────────────────
#
#  flights ──── Reporting_Airline ──▶ airlines (IATA_CODE)
#  flights ──── Origin / Dest     ──▶ airports (IATA_CODE)
#
# Note: Fabric doesn't support glob patterns in DuckDB,
# so we UNION ALL the three years explicitly.

t0 = time.time()
con.sql(f"""
    CREATE OR REPLACE TABLE flights AS
        SELECT * FROM read_csv_auto('{DATA}/flights_2022.csv')
        UNION ALL
        SELECT * FROM read_csv_auto('{DATA}/flights_2023.csv')
        UNION ALL
        SELECT * FROM read_csv_auto('{DATA}/flights_2024.csv')
""")
con.sql(f"CREATE OR REPLACE TABLE airlines AS SELECT * FROM read_csv_auto('{DATA}/airlines.csv')")
con.sql(f"CREATE OR REPLACE TABLE airports AS SELECT * FROM read_csv_auto('{DATA}/airports.csv')")
print(f"Loaded in {time.time()-t0:.1f}s")

df = con.sql("""
    SELECT
        year(FlightDate::DATE) AS year,
        COUNT(*)               AS total_flights,
        SUM(Cancelled)         AS cancellations
    FROM flights
    GROUP BY year
    ORDER BY year
""").df()
display(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

# EXCLUDE — drop columns you don't want (not in T-SQL!)
df = con.sql("""
    SELECT * EXCLUDE (CRSElapsedTime, ActualElapsedTime, AirTime, DepDel15, ArrDel15)
    FROM flights
    LIMIT 5
""").df()
display(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

# ── 3. ON-TIME PERFORMANCE BY AIRLINE ───────────────────────

df = con.sql("""
    SELECT
        al.AIRLINE,
        COUNT(*)                                        AS total_flights,
        ROUND(AVG(f.ArrDelay), 1)                       AS avg_arr_delay_min,
        ROUND(SUM(f.Cancelled) * 100.0 / COUNT(*), 1)  AS cancel_pct
    FROM flights f
    JOIN airlines al ON f.Reporting_Airline = al.IATA_CODE
    WHERE f.Cancelled = 0
    GROUP BY al.AIRLINE
    ORDER BY avg_arr_delay_min DESC
""").df()
display(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

# Monthly average delay — 2022 through 2024
monthly = con.sql("""
    SELECT
        strftime(FlightDate::DATE, '%Y-%m') AS month,
        COUNT(*)                             AS flights,
        ROUND(AVG(ArrDelay), 1)              AS avg_arr_delay
    FROM flights
    WHERE Cancelled = 0
    GROUP BY month
    ORDER BY month
""").df()

fig, ax = plt.subplots(figsize=(14, 4))
ax.bar(monthly['month'], monthly['avg_arr_delay'], color='steelblue', width=0.7)
ax.axhline(0, color='black', linewidth=0.8)
ax.set_title('Average Arrival Delay by Month (2022–2024)', fontsize=13)
ax.set_ylabel('Minutes')
plt.xticks(rotation=45, ha='right', fontsize=7)
plt.tight_layout()
plt.show()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

# ── 4. WHAT'S CAUSING THE DELAYS? ───────────────────────────

df = con.sql("""
    SELECT
        al.AIRLINE,
        ROUND(AVG(f.CarrierDelay), 1)      AS carrier,
        ROUND(AVG(f.WeatherDelay), 1)      AS weather,
        ROUND(AVG(f.NASDelay), 1)          AS air_system,
        ROUND(AVG(f.LateAircraftDelay), 1) AS late_aircraft,
        ROUND(AVG(f.SecurityDelay), 1)     AS security
    FROM flights f
    JOIN airlines al ON f.Reporting_Airline = al.IATA_CODE
    WHERE f.ArrDelay > 0 AND f.Cancelled = 0
    GROUP BY al.AIRLINE
    ORDER BY carrier DESC
""").df()
display(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

# ── 5. THE SOUTHWEST DECEMBER 2022 STORY ────────────────────
# ~16,700 cancellations in one week. Let's find it in the data.

wn = con.sql("""
    SELECT
        strftime(FlightDate::DATE, '%Y-%m')          AS month,
        COUNT(*)                                      AS flights,
        SUM(Cancelled)                                AS cancellations,
        ROUND(SUM(Cancelled) * 100.0 / COUNT(*), 1)  AS cancel_pct
    FROM flights
    WHERE Reporting_Airline = 'WN'
    GROUP BY month
    ORDER BY month
""").df()

fig, ax = plt.subplots(figsize=(14, 4))
bars = ax.bar(wn['month'], wn['cancel_pct'], color='steelblue', width=0.7)

for i, m in enumerate(wn['month']):
    if m == '2022-12':
        bars[i].set_color('firebrick')
        ax.annotate('Dec 2022\nSouthwest meltdown',
                    xy=(i, wn['cancel_pct'].iloc[i]),
                    xytext=(i + 2, wn['cancel_pct'].iloc[i]),
                    fontsize=9, color='firebrick',
                    arrowprops=dict(arrowstyle='->', color='firebrick'))

ax.set_title('Southwest Airlines — Cancellation Rate by Month', fontsize=13)
ax.set_ylabel('Cancellation %')
ax.yaxis.set_major_formatter(mticker.PercentFormatter())
plt.xticks(rotation=45, ha='right', fontsize=7)
plt.tight_layout()
plt.show()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

# ── 6. WORST AIRPORTS TO DEPART FROM ────────────────────────

df = con.sql("""
    SELECT
        ap.iata_code,
        ap.name,
        ap.municipality || ', ' || ap.iso_region       AS location,
        COUNT(*)                                        AS departures,
        ROUND(AVG(f.DepDelay), 1)                       AS avg_dep_delay,
        ROUND(SUM(f.Cancelled) * 100.0 / COUNT(*), 1)  AS cancel_pct
    FROM flights f
    JOIN airports ap ON f.Origin = ap.iata_code
    WHERE f.Cancelled = 0
    GROUP BY ap.iata_code, ap.name, location
    HAVING departures > 10000
    ORDER BY avg_dep_delay DESC
    LIMIT 15
""").df()
display(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

# ── 7. EXPORT TO PARQUET ─────────────────────────────────────
# Parquet is columnar — smaller files, faster queries.

parquet_path = f"{DATA}/flights_all.parquet"

t0 = time.time()
con.sql(f"COPY flights TO '{parquet_path}' (FORMAT PARQUET)")
print(f"Written in {time.time()-t0:.1f}s")
print(f"Find it in: lh_duck_pond → Files → flights → flights_all.parquet")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

# ── 8. SPEED COMPARISON — CSV vs PARQUET ────────────────────

query = """
    SELECT Reporting_Airline, COUNT(*), ROUND(AVG(ArrDelay), 1) AS avg_delay
    FROM {source}
    WHERE Cancelled = 0
    GROUP BY Reporting_Airline
    ORDER BY avg_delay DESC
"""

t0 = time.time()
con.sql(query.format(source="flights")).df()
csv_time = time.time() - t0

con.sql(f"CREATE OR REPLACE TABLE flights_parquet AS SELECT * FROM read_parquet('{parquet_path}')")
t0 = time.time()
con.sql(query.format(source="flights_parquet")).df()
parq_time = time.time() - t0

print(f"CSV (in-memory): {csv_time:.2f}s")
print(f"Parquet:         {parq_time:.2f}s  ({csv_time/parq_time:.1f}x faster)")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }
