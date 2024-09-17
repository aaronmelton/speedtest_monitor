"""Speedtest Monitor."""

# !/usr/bin/env python
# -*- coding: utf-8 -*-
#

import json
import subprocess
import sys
from datetime import datetime
from time import perf_counter

import MySQLdb
from aaron_common_libs.common_funcs import pretty_print
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

    logger.info("Running speedtest...")
    try:
        process = subprocess.run(["/usr/local/bin/speedtest", "--json"], check=True, capture_output=True)
        speedtest_results = json.loads(process.stdout.decode("utf-8"))
        logger.debug("speedtest_results==%s", pretty_print(speedtest_results))
        logger.info("Speedtest run successfully.")
    except Exception as some_exception:  # pylint: disable=broad-except
        speedtest_results = None
        logger.error("ERROR running speed test.")
        logger.exception("EXCEPTION='%s'", str(some_exception))

    if speedtest_results:
        speedtest_dict = {
            "datetime": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "timestamp": int(datetime.strptime(speedtest_results["timestamp"], "%Y-%m-%dT%H:%M:%S.%fZ").timestamp()),
            "ping_latency": speedtest_results["ping"],
            "download_throughput": int(speedtest_results["download"]),
            "upload_throughput": int(speedtest_results["upload"]),
            "server_id": speedtest_results["server"]["id"],
            "server_host": speedtest_results["server"]["host"],
        }

        query = """INSERT INTO {schema_name}.{table_name} (datetime, timestamp, ping_latency, download_throughput, upload_throughput, server_id, server_host) VALUES (%s, %s, %s, %s, %s, %s, %s)"""

        try:
            db_query(config.db_dict, query, speedtest_dict)
        except Exception as some_exception:  # pylint: disable=broad-except
            logger.error("ERROR running db_query")
            logger.exception("EXCEPTION='%s'", str(some_exception))
    else:
        logger.error("Error running speed test.")

    logger_all.info("Total Execution Time: %s seconds", round(perf_counter() - start_time, 2))
    logger_all.info("----------   STOP STOP STOP  ----------")
    logger.info("")


if __name__ == "__main__":
    sys.exit(main())
