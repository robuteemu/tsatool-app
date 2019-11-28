#!/bin/bash

# Call server-side COPY statements and populate_...() procedures
# for multiple LOTJU monthly files.
# Adjust the month set and connection parameters in the beginning according to your case.
# You must provide the PG password interactively;
# to avoid this, use PGPASSWORD environment variable
# or ~/.pgpass file.

# NOTE: not tested extensively with big data sets!
# dbhost=localhost
# dbport=7001
# dbname=tsa
# dbuser=postgres
dbhost=localhost
dbport=5432
dbname=tsa
dbuser=tsadash
months=(
  01
  02
  03
  04
  05
  06
  07
  08
  09
  10
  11
  12
)
for m in "${months[@]}"; do
  echo "Processing month $m ..."
  # FIXME: Current implementation asks the password interactively every time.
  #        Consider using ~/.pgpass file to avoid this, for example.
  psql -h "$dbhost" -p "$dbport" -d "$dbname" -U "$dbuser" \
    -c  "BEGIN; \
         COPY tiesaa_mittatieto FROM '/rawdata/tiesaa_mittatieto-2018_$m.csv' CSV HEADER DELIMITER '|'; \
         CALL populate_statobs(); \
         TRUNCATE TABLE tiesaa_mittatieto; \
         COPY anturi_arvo FROM '/rawdata/anturi_arvo-2018_$m.csv' CSV HEADER DELIMITER '|'; \
         CALL populate_seobs(); \
         TRUNCATE TABLE anturi_arvo; \
         COMMIT;"
done
