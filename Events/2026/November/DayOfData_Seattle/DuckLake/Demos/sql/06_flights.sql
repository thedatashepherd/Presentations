-- Run in: DuckDB A, after attaching to lake.

-- Load January 2024 Seattle flights and an airport lookup into DuckLake.
-- Run in DuckDB after 05_attach.sql, in a catalog without an existing
-- flights or airports table.
-- flight_id is a generated row identifier, not an airline flight
-- number.

-- Read existing Parquet and write new files managed by DuckLake.
-- The qualified name makes the destination explicit.
CREATE TABLE lake.main.flights AS
SELECT
    row_number() OVER (
        ORDER BY FlightDate, Reporting_Airline, Origin, Dest,
                 DepDelay, ArrDelay, Distance
    ) AS flight_id,
    FlightDate AS flight_date,
    Reporting_Airline AS airline,
    Origin AS origin,
    Dest AS destination,
    DepDelay AS departure_delay_minutes,
    ArrDelay AS arrival_delay_minutes,
    CAST(Cancelled AS BOOLEAN) AS cancelled,
    Distance AS distance_miles
FROM read_parquet('./source-data/flights/flights_all.parquet')
WHERE FlightDate >= DATE '2024-01-01'
  AND FlightDate < DATE '2024-02-01'
  AND (Origin = 'SEA' OR Dest = 'SEA');

-- Check the number of flights and their date range.
SELECT count(*) AS flights, min(flight_date) AS first_date,
       max(flight_date) AS last_date
FROM flights; -- 23,508 flights

-- Compare arrival delays and cancellations by airline.
SELECT airline, count(*) AS flights,
       round(avg(arrival_delay_minutes), 1) AS avg_arrival_delay_minutes,
       count(*) FILTER (WHERE cancelled) AS cancellations
FROM flights
GROUP BY airline
ORDER BY flights DESC;

-- Load airport names and locations from CSV into the same lake.
CREATE TABLE lake.main.airports AS
SELECT
    iata_code AS airport_code,
    name AS airport_name,
    municipality AS city,
    iso_region AS region,
    latitude_deg,
    longitude_deg
FROM read_csv(
    './source-data/flights/airports.csv',
    header = true
);

-- Join the lookup twice to name both ends of each route.
-- LEFT JOIN keeps flights even when an airport code has no match.
SELECT
    f.origin,
    origin_airport.airport_name AS origin_airport,
    f.destination,
    destination_airport.airport_name AS destination_airport,
    count(*) AS flights
FROM lake.main.flights AS f
LEFT JOIN lake.main.airports AS origin_airport
    ON f.origin = origin_airport.airport_code
LEFT JOIN lake.main.airports AS destination_airport
    ON f.destination = destination_airport.airport_code
GROUP BY
    f.origin,
    origin_airport.airport_name,
    f.destination,
    destination_airport.airport_name
ORDER BY flights DESC, f.origin, f.destination
LIMIT 10;

-- List committed snapshots. Catalog queries are in
-- 11_catalog_inspection.sql.
SELECT * FROM lake.snapshots();

-- Result: The lake contains flights and airports. Flights has 23,508
-- rows. DuckLake tracks both tables and their Parquet files.
