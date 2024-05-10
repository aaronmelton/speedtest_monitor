"""Speedtest Monitor."""

# !/usr/bin/env python
# -*- coding: utf-8 -*-
#

import json
import subprocess
import sys
from time import perf_counter

import MySQLdb  # pylint: disable=import-error
from aaron_common_libs.common_funcs import pretty_print
from aaron_common_libs.logger.custom_logger import CustomLogger
from config import Config

config = Config()
logging_handler = CustomLogger(log_dict=config.log_dict)
logger = logging_handler.default
logger_all = logging_handler.all


def db_query(db_deets, query, some_list):
    """Query database and return results.

    Args
    ----
    db_deets: dict
    query: str
    some_list: dict

    Returns
    -------
    output_json: str
    """
    host = db_deets["host"]
    user = db_deets["username"]
    passwd = db_deets["password"]
    database = db_deets["schema"]
    logger.debug("host=='%s'", host)
    logger.debug("database=='%s'", database)
    logger.debug("query=='%s'", query)
    logger.debug("some_list=='%s'", some_list)
    output_json = []
    database_connection = MySQLdb.connect(host, user, passwd, database)
    cursor = database_connection.cursor()
    # If some_list is provided, this query will be writing changes to the database.
    if some_list:
        try:
            try:
                logger.info("Writing changes to database...")
                cursor.execute(query, some_list.values())
            except Exception as some_exception:  # pylint: disable=broad-except
                logger.error("ERROR running query.")
                logger.exception("ERROR=='%s'", some_exception)
            try:
                database_connection.commit()
            except Exception as some_exception:  # pylint: disable=broad-except
                logger.exception("ERROR=='%s'", some_exception)
                logger.error("ERROR committing changes.")
        except Exception as some_exception:  # pylint: disable=broad-except
            logger.error("ERROR running query: %s", str(query))
            logger.exception("ERROR=='%s'", some_exception)

    # If some_list is NOT provided, this query will be retrieving data from the database.
    if not some_list:
        try:
            logger.info("Querying database...")
            cursor.execute(query)
            # Convert SQL output to JSON.  This way we can iterate
            # through key:value pairs instead of worrying about adjusting
            # list positions if we change the query
            field_names = [i[0] for i in cursor.description]
            results = cursor.fetchall()
            for row in results:
                output_json.append(dict(zip(field_names, row)))
        except Exception as some_exception:  # pylint: disable=broad-except
            logger.error("ERROR running query: %s", str(query))
            logger.exception("ERROR=='%s'", some_exception)

    database_connection.close()
    # logger.debug("output_json==%s", output_json)
    return output_json


def main():
    """Main Function.

    Args
    ----

    Returns
    -------
    None
    """
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
            "timestamp": speedtest_results["timestamp"],
            "ping_latency": speedtest_results["ping"],
            "download_bandwidth": speedtest_results["download"],
            "upload_bandwidth": speedtest_results["upload"],
            "server_id": speedtest_results["server"]["id"],
            "server_host": speedtest_results["server"]["host"],
        }

        # query = f"""INSERT INTO {config.db_dict["schema"]}.speedtest (timestamp, ping_latency, download_bandwidth, upload_bandwidth, server_id, server_host) VALUES (:timestamp, :ping_latency, :download_bandwidth, :upload_bandwidth, :server_id, :server_host)"""
        query = """INSERT INTO speedtest.speedtest (timestamp, ping_latency, download_bandwidth, upload_bandwidth, server_id, server_host) VALUES (:timestamp, :ping_latency, :download_bandwidth, :upload_bandwidth, :server_id, :server_host)"""

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
