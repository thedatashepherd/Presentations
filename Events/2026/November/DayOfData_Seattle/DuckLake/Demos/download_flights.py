"""Download a Seattle flight sample and build the Parquet for this walkthrough.

Adapted from the downloader distributed with Jason Romans's DuckDB 101 demos.
Uses Python's standard library and the DuckDB CLI installed by sql/00_setup-duckdb.ps1.
Annual CSVs are published only after all twelve monthly downloads succeed.
"""
import argparse
import csv
import io
from pathlib import Path
import shutil
import subprocess
import tempfile
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parent
DATA = ROOT / 'source-data' / 'flights'
YEARS = (2022, 2023, 2024)
KEEP_COLS = {
    'FlightDate', 'Reporting_Airline', 'Origin', 'Dest', 'Distance',
    'DepDelay', 'DepDelayMinutes', 'DepDel15', 'ArrDelay', 'ArrDelayMinutes',
    'ArrDel15', 'Cancelled', 'CancellationCode', 'Diverted', 'CarrierDelay',
    'WeatherDelay', 'NASDelay', 'SecurityDelay', 'LateAircraftDelay',
    'AirTime', 'CRSElapsedTime', 'ActualElapsedTime',
}
BASE_URL = ('https://transtats.bts.gov/PREZIP/'
            'On_Time_Reporting_Carrier_On_Time_Performance_1987_present_{year}_{month}.zip')


def download_year(year, output_dir=DATA, sample=False):
    output_dir.mkdir(parents=True, exist_ok=True)
    destination = output_dir / (f'flights_seattle_{year}.csv' if sample else f'flights_{year}.csv')
    if destination.exists():
        print(f'{year}: reusing {destination.name}', flush=True)
        return destination
    partial = destination.with_suffix('.csv.partial')
    try:
        with partial.open('w', newline='', encoding='utf-8') as out:
            writer = None
            columns = None
            for month in ((1, 2) if sample else range(1, 13)):
                print(f'Downloading {year}-{month:02d}...', flush=True)
                # Use disk for the compressed month and stream rows, rather than
                # holding a full year of Python dictionaries in memory.
                with tempfile.TemporaryFile() as archive:
                    request = urllib.request.Request(
                        BASE_URL.format(year=year, month=month),
                        headers={'User-Agent': 'DuckLake-Attendee-Data-Setup/1.0'})
                    with urllib.request.urlopen(request, timeout=120) as response:
                        shutil.copyfileobj(response, archive)
                    archive.seek(0)
                    with zipfile.ZipFile(archive) as bundle:
                        members = [n for n in bundle.namelist()
                                   if n.lower().endswith('.csv') and not n.startswith('__MACOSX/')]
                        if len(members) != 1:
                            raise RuntimeError('Expected one BTS CSV in monthly archive')
                        with bundle.open(members[0]) as raw:
                            reader = csv.DictReader(io.TextIOWrapper(raw, encoding='utf-8-sig'))
                            selected = [c for c in (reader.fieldnames or []) if c in KEEP_COLS]
                            if set(selected) != KEEP_COLS:
                                raise RuntimeError(f'Missing expected BTS columns for {year}-{month:02d}')
                            if writer is None:
                                columns = selected
                                writer = csv.DictWriter(out, fieldnames=columns, extrasaction='ignore')
                                writer.writeheader()
                            elif set(selected) != set(columns):
                                raise RuntimeError('BTS schema changed between months')
                            count = 0
                            for row in reader:
                                if sample and not (
                                    (row['Origin'] == 'SEA' or row['Dest'] == 'SEA')
                                    and '2024-01-01' <= row['FlightDate'][:10] <= '2024-02-01'
                                ):
                                    continue
                                writer.writerow(row)
                                count += 1
                            if count == 0:
                                raise RuntimeError('Monthly BTS CSV contains no rows')
                            print(f'  {count:,} flights', flush=True)
        partial.replace(destination)
    except BaseException:
        partial.unlink(missing_ok=True)
        raise
    return destination


def build_parquet(executable, inputs, destination):
    partial = destination.with_suffix('.parquet.partial')
    def literal(value):
        return "'" + Path(value).as_posix().replace("'", "''") + "'"
    sources = ', '.join(literal(p) for p in inputs)
    query = (f'COPY (SELECT * FROM read_csv([{sources}], header=true, union_by_name=true)) '
             f'TO {literal(partial)} (FORMAT PARQUET);')
    try:
        subprocess.run([str(executable), '-c', query], check=True, cwd=ROOT)
        partial.replace(destination)
    except BaseException:
        partial.unlink(missing_ok=True)
        raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--full', action='store_true',
                        help='Download all 36 months of 2022-2024 instead of the Seattle sample.')
    parser.add_argument('--duckdb', type=Path,
                        default=ROOT / '.tools/duckdb-2.0.0/duckdb.exe')
    args = parser.parse_args()
    if not args.duckdb.is_file():
        parser.error('Run ./sql/00_setup-duckdb.ps1 first, or supply --duckdb PATH.')
    for lookup in ('airlines.csv', 'airports.csv'):
        if not (DATA / lookup).is_file():
            parser.error(f'Missing bundled lookup: source-data/flights/{lookup}')
    # Separate generated files so switching modes never silently reuses
    # a sample as the full dataset. SQL always reads flights_all.parquet.
    mode_destination = DATA / ('flights_full.parquet' if args.full else 'flights_seattle.parquet')
    destination = DATA / 'flights_all.parquet'
    if not mode_destination.exists():
        inputs = ([download_year(year) for year in YEARS] if args.full
                  else [download_year(2024, sample=True)])
        build_parquet(args.duckdb.resolve(), inputs, mode_destination)
    else:
        print(f'Reusing {mode_destination.name}')
    shutil.copyfile(mode_destination, destination)
    print(f'Ready: {destination}')


if __name__ == '__main__':
    main()
