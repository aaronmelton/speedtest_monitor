"""Speedtest Monitor."""
# !/usr/bin/env python
# -*- coding: utf-8 -*-
#

import json
import subprocess
import sys
from datetime import datetime
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
    # If some_list is provided, this query will be writing changes to
    # the database.
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

    # If some_list is NOT provided, this query will be retrieving data
    # from the database.
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
        speedtest_list = {}
        speedtest_list["datetime"] = speedtest_results["timestamp"]

        # Need to convert datetime/timestamp to epoch int; Works better with Grafana
        utc_time = datetime.strptime(speedtest_list["datetime"], "%Y-%m-%dT%H:%M:%SZ")
        epoch_time = (utc_time - datetime(1970, 1, 1)).total_seconds()

        speedtest_list["timestamp"] = int(epoch_time)
        speedtest_list["ping_jitter"] = speedtest_results["ping"]["jitter"]
        speedtest_list["ping_latency"] = speedtest_results["ping"]["latency"]
        speedtest_list["download_bandwidth"] = speedtest_results["download"]["bandwidth"]
        speedtest_list["download_bytes"] = speedtest_results["download"]["bytes"]
        speedtest_list["download_elapsed"] = speedtest_results["download"]["elapsed"]
        speedtest_list["upload_bandwidth"] = speedtest_results["upload"]["bandwidth"]
        speedtest_list["upload_bytes"] = speedtest_results["upload"]["bytes"]
        speedtest_list["upload_elapsed"] = speedtest_results["upload"]["elapsed"]
        speedtest_list["packetloss"] = speedtest_results["packetLoss"]
        speedtest_list["server_id"] = speedtest_results["server"]["id"]
        speedtest_list["server_host"] = speedtest_results["server"]["host"]
        speedtest_list["server_port"] = speedtest_results["server"]["port"]
        speedtest_list["server_name"] = speedtest_results["server"]["name"]
        speedtest_list["server_location"] = speedtest_results["server"]["location"]
        speedtest_list["server_country"] = speedtest_results["server"]["country"]
        speedtest_list["server_ip"] = speedtest_results["server"]["ip"]

        query = """INSERT INTO speedtest.speedtest (datetime, timestamp, ping_jitter, ping_latency, download_bandwidth, download_bytes, download_elapsed, upload_bandwidth, upload_bytes, upload_elapsed, packetloss, server_id, server_host, server_port, server_name, server_location, server_country, server_ip) VALUES (:datetime, :timestamp, :ping_jitter, :ping_latency, :download_bandwidth, :download_bytes, :download_elapsed, :upload_bandwidth, :upload_bytes, :upload_elapsed, :packetloss, :server_id, :server_host, :server_port, :server_name, :server_location, :server_country, :server_ip)"""

        try:
            db_query(config.db_dict, query, speedtest_list)
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
