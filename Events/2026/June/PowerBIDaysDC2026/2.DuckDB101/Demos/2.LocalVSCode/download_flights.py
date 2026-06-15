"""
Download BTS airline on-time performance data (2022-2024).
Filters to demo-relevant columns and saves as annual CSVs.

Run with:  python download_flights.py
       or: uv run python download_flights.py
"""

import urllib.request
import zipfile
import io
import csv
import os
import time
import sys

YEARS = [2022, 2023, 2024]

KEEP_COLS = {
    "FlightDate", "Reporting_Airline", "Origin", "Dest", "Distance",
    "DepDelay", "DepDelayMinutes", "DepDel15",
    "ArrDelay", "ArrDelayMinutes", "ArrDel15",
    "Cancelled", "CancellationCode", "Diverted",
    "CarrierDelay", "WeatherDelay", "NASDelay", "SecurityDelay", "LateAircraftDelay",
    "AirTime", "CRSElapsedTime", "ActualElapsedTime",
}

BASE_URL = (
    "https://transtats.bts.gov/PREZIP/"
    "On_Time_Reporting_Carrier_On_Time_Performance_1987_present_{year}_{month}.zip"
)

OUT_DIR = os.path.join(os.path.dirname(__file__), "data", "flights")


def download_month(year: int, month: int) -> list[dict]:
    url = BASE_URL.format(year=year, month=month)
    print(f"  Downloading {year}-{month:02d}...", end=" ", flush=True)
    t0 = time.time()
    try:
        with urllib.request.urlopen(url, timeout=120) as r:
            data = r.read()
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            csv_name = next(n for n in z.namelist() if n.endswith(".csv") and not n.startswith("_"))
            with z.open(csv_name) as f:
                rows = list(csv.DictReader(io.TextIOWrapper(f, encoding="utf-8-sig")))
        print(f"{len(rows):,} rows ({time.time()-t0:.0f}s)")
        return rows
    except Exception as e:
        print(f"FAILED: {e}")
        return []


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    for year in YEARS:
        out_path = os.path.join(OUT_DIR, f"flights_{year}.csv")
        if os.path.exists(out_path):
            size_mb = os.path.getsize(out_path) / 1e6
            print(f"{year}: already exists ({size_mb:.0f} MB), skipping")
            continue

        print(f"\n--- {year} ---")
        all_rows: list[dict] = []
        fieldnames: list[str] | None = None

        for month in range(1, 13):
            rows = download_month(year, month)
            if not rows:
                continue
            if fieldnames is None:
                # Preserve original column order, filtered to KEEP_COLS
                fieldnames = [c for c in rows[0].keys() if c in KEEP_COLS]
            all_rows.extend(rows)

        if not all_rows or not fieldnames:
            print(f"  No data for {year}, skipping")
            continue

        print(f"  Writing {len(all_rows):,} rows to {out_path}...")
        with open(out_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(all_rows)

        size_mb = os.path.getsize(out_path) / 1e6
        print(f"  Saved {size_mb:.0f} MB")

    print("\nDone! Files are in data/flights/")
    print("Open 01_duckdb_local_intro.ipynb to get started.")


if __name__ == "__main__":
    main()
