#!env/bin/python

"""
Script for running TSA analyses as batch job.
Meant for background use: all input and output parameters
are assumed clean and valid, and there are no interactive
wait / confirmation steps!
"""
import os
import re
import sys
import json
import argparse
import psycopg2
import logging
from tsa.analysis_collection import AnalysisCollection
from tsa.utils import list_local_statids
from tsa.utils import list_local_sensors
from tsa.utils import list_db_sensors

def main():
    # ---- COMMAND LINE ARGUMENTS ----
    parser = argparse.ArgumentParser(description='Run TSA analyses as batch job.')
    parser.add_argument('-i', '--input',
                        type=str,
                        help='Input Excel path relative to script directory',
                        metavar='INPUT_XLSX_PATH',
                        required=True)
    parser.add_argument('-n', '--name',
                        type=str,
                        help='Base name for output files saved under results/',
                        metavar='OUTPUT_BASENAME',
                        required=True)
    parser.add_argument('--dryvalidate',
                        action='store_true',
                        help='Only validate input Excel with hard-coded ids and names')
    args = parser.parse_args()
    if args.name is None:
        # Use input excel name but replace file ending
        args.name = re.sub("\.[^.]*$", "_OUT", args.input)

    # This directory, relative to the script dir,
    # is used for both logs and result files:
    os.makedirs('results', exist_ok=True)

    # ---- LOGGING ----
    log = logging.getLogger()
    log.setLevel(logging.DEBUG)
    # Note that old logs by same name are overwritten!
    log_dest = os.path.join('results', f'{args.name}.log')
    fh = logging.FileHandler(filename=log_dest,
                             mode='w')
    ch = logging.StreamHandler()
    fh.setFormatter(
        logging.Formatter(
            '%(asctime)s; %(levelname)-8s; %(module)-20s; line %(lineno)-3d; %(message)s',
            'Y-%m-%d %H:%M:%S'
            )
        )
    ch.setFormatter(logging.Formatter('%(levelname)-8s; %(message)s'))
    log.addHandler(fh)
    log.addHandler(ch)

    log.info((f'START OF TSABATCH with input={args.input} name={args.name} '
              f'dryvalidate={args.dryvalidate}, '
              f'logs are saved to {log_dest}'))

    # ---- APP LOGIC ----
    anls = AnalysisCollection(input_xlsx=args.input, name=args.name)
    log.info(f'Created {str(anls)}')

    # Add all sheets for analysis ("info" is omitted by default).
    # Adding collections includes syntax validation.
    anls.add_collections()

    if args.dryvalidate:
        log.debug('Starting dry validation without database')
        anls.set_sensor_ids(pairs=list_local_sensors())
        anls.validate_statids_with_set(station_ids=list_local_statids())
        haserrs, errors = anls.collect_errors()
        if haserrs:
            errs_dest = os.path.join('results', f'{args.name}_ERRORS.json')
            with open(errs_dest, 'w') as fobj:
                fobj.write(
                    json.dumps(errors, indent=4)
                )
            log.error('Dry validation exited with errors')
            raise Exception(
                ('Dry validation exited with errors. '
                 f'See {log_dest} and {errs_dest}.')
            )
        else:
            log.info('Dry validation was SUCCESSFUL')
            sys.exit()

    # ---- DB interaction begins here ----

    # Sensor ids; global for all collections
    try:
        with psycopg2.connect(**anls.db_params, connect_timeout=5) as pg_conn:
            db_sensors = list_db_sensors(pg_conn)
        anls.set_sensor_ids(pairs=db_sensors)
        log.info('Sensor ids from database set successfully')
    except:
        log.exception('Could not set sensor ids from database for Blocks, quitting')
        raise

    # Collection specific stuff:
    # requesting station ids is bound to the same database connection
    # in which the time-limited observation view is created
    # and analyses are run.
    # Thus we proceed by analyzing one collection at a time.
    # IDEA: If the database instance can use enough resources,
    #       this step could be parallelized, using multiple db connections,
    #       since CondCollections depend on their own db sessions
    #       and do not affect each other.
    # Prepare and validate collections
    for collname in anls.collections.keys():
        log.info(f'Analyzing {str(anls.collections[collname])} ...')
        with psycopg2.connect(**anls.db_params, connect_timeout=5) as pg_conn:
            # TODO: fetch and validate station ids
            # TODO: validate conditions
            # TODO: run analyses, skipping invalid conditions
            # TODO: ensure results are saved
            pass

    # TODO: save error tree as JSON

    log.info('END OF TSABATCH')

if __name__ == '__main__':
    main()
