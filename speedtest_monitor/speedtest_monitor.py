"""Speedtest Monitor."""

# !/usr/bin/env python
# -*- coding: utf-8 -*-
#

import json
import shutil
import subprocess
import sys
from datetime import datetime
from time import perf_counter

import MySQLdb
from aaron_common_libs.common_funcs import argument, cli, pretty_print, subcommand
from aaron_common_libs.logger.custom_logger import CustomLogger
from config import Config

config = Config()
logging_handler = CustomLogger(log_dict=config.log_dict)
logger = logging_handler.default
logger_all = logging_handler.all


def db_query(db_details, query, some_dict):
    """Query database and return results.

    Args:
        db_details (dict)
        query (str)
        some_dict (dict)

    Returns:
        output_json (str)
    """
    output_json = {}
    database_connection = MySQLdb.connect(
        db_details["host"], db_details["username"], db_details["password"], db_details["schema_name"]
    )
    cursor = database_connection.cursor()
    try:  # Execute database query
        logger.info("Writing changes to database...")
        output_json = cursor.execute(
            query.format(schema_name=db_details["schema_name"], table_name=db_details["table_name"]),
            some_dict.values(),
        )
    except Exception as some_exception:  # pylint: disable=broad-exception-caught
        logger.error("ERROR running query.")
        logger.exception("ERROR=='%s'", some_exception)
    try:  # Python MySQL connector does not autocommit
        database_connection.commit()
    except Exception as some_exception:  # pylint: disable=broad-exception-caught
        logger.exception("ERROR=='%s'", some_exception)
        logger.error("ERROR committing changes.")

    database_connection.close()
    return output_json


def run_speedtest():
    """Run speedtest binary and capture results.

    Args:
        None

    Returns:
        test_results (dict)
    """
    test_results = {}
    speedtest_path = shutil.which("speedtest")
    if speedtest_path is None:
        raise FileNotFoundError("The 'speedtest' executable was not found on your system.")
    try:
        process = subprocess.run([speedtest_path, "--json"], check=True, capture_output=True)
        speedtest_results = json.loads(process.stdout.decode("utf-8"))
        test_results = {
            "datetime": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "timestamp": int(datetime.strptime(speedtest_results["timestamp"], "%Y-%m-%dT%H:%M:%S.%fZ").timestamp()),
            "ping_latency": speedtest_results["ping"],
            "download_throughput": int(speedtest_results["download"]),
            "upload_throughput": int(speedtest_results["upload"]),
            "server_id": speedtest_results["server"]["id"],
            "server_host": speedtest_results["server"]["host"],
        }
        logger.debug("test_results==%s", pretty_print(speedtest_results))
        logger.info("Speedtest run successfully.")
    except Exception as some_exception:  # pylint: disable=broad-except
        logger.error("ERROR running speed test.")
        logger.exception("EXCEPTION='%s'", str(some_exception))
    return test_results


# Sub-Commands for TEST operations
@subcommand(
    [
        argument("--pull", help="Collect Speedtest results and print to console.", action="store_true", required=False),
        argument(
            "--pullpush",
            help="Collect Speedtest results and store them in a database.",
            action="store_true",
            required=False,
        ),
    ]
)
def speedtest(args):
    """Subcommand options for test operations."""
    logger.debug("args==%s", vars(args))
    test_results = {}
    if args.pull:
        test_results = run_speedtest()
    if args.pullpush:
        test_results = run_speedtest()
        if test_results:
            query = """INSERT INTO {schema_name}.{table_name} (datetime, timestamp, ping_latency, download_throughput, upload_throughput, server_id, server_host) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            try:
                db_query(config.db_dict, query, test_results)
            except Exception as some_exception:  # pylint: disable=broad-except
                logger.error("ERROR running db_query")
                logger.exception("EXCEPTION='%s'", str(some_exception))
        else:
            logger.error("Error running speed test.")
    return test_results


def main():
    """Do Something."""
    start_time = perf_counter()

    logger.info("")
    logger_all.info("---------- START START START ----------")
    logger_all.info(
        "%s v%s (%s)",
        config.app_dict["title"],
        config.app_dict["version"],
        config.app_dict["date"],
    )

    required_vars = {}
    find_null_vars = [value for value in required_vars.items() if None is value[1]]
    if find_null_vars:
        logger.error("Missing Environment Variable(s): %s", find_null_vars)
        print(f"\nERROR: Missing Environment Variable(s): {find_null_vars}")
    else:
        args = cli.parse_args()
        if args.subcommand is None:
            cli.print_help()
        else:
            arg_results = args.func(args)
            if arg_results:
                print(pretty_print(arg_results))
            else:
                cli.print_help()

    logger_all.info("Total Execution Time: %s seconds", round(perf_counter() - start_time, 2))
    logger_all.info("----------   STOP STOP STOP  ----------")
    logger.info("")


if __name__ == "__main__":
    sys.exit(main())
