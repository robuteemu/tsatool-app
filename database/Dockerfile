# Build an image containing an empty tsa database schema.
# Example usage:
# docker build -t tsadb .
# docker run --rm -d -e POSTGRES_PASSWORD=postgres -p 7001:5432 tsadb
# Should then be able to connect to db from the host:
# psql -p 7001 -U postgres -d tsa
#
FROM timescale/timescaledb:latest-pg11
# Scripts in /docker-entrypoint-initdb.d/ will be run
# when Postgres server is started for the first time
COPY 01_init_db.sql /docker-entrypoint-initdb.d/
COPY 02_rawdata_schema.sql /docker-entrypoint-initdb.d/
COPY 03_insert_stations_sensors.sql /docker-entrypoint-initdb.d/
COPY tiesaa_asema_filtered.csv /tiesaa_asema_filtered.csv
COPY laskennallinen_anturi_filtered.csv /laskennallinen_anturi_filtered.csv
RUN chmod 644 /tiesaa_asema_filtered.csv /laskennallinen_anturi_filtered.csv
EXPOSE 5432
