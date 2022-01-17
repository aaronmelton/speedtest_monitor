"""Speedtest Monitor."""
# !/usr/bin/env python
# -*- coding: utf-8 -*-
#

import json
import logging
import subprocess
import sys
from datetime import date, datetime
from time import time

import MySQLdb
from config import app_dict, db_dict, log_dict


def db_query(db_deets, query, some_list):
    """Query database and return results.

    Args
    ----
    db_deets["host"] : str
    db_deets["user"] : str
    db_deets["passwd"] : str
    db_deets["database"] : str
    query : str
    some_list : dict

    Returns
    -------
    output_json : str
    """
    logger.info("START")
    host = db_deets["host"]
    user = db_deets["username"]
    passwd = db_deets["password"]
    database = db_deets["schema"]
    logger.debug("host=='%s'", host)
    # logger.debug("user=='%s'", user)
    # logger.debug("passwd=='%s'", passwd)
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
            except Exception as some_exception:
                logger.error("ERROR running query.")
                logger.exception("ERROR=='%s'", some_exception)
            try:
                database_connection.commit()
            except Exception as some_exception:
                logger.exception("ERROR=='%s'", some_exception)
                logger.error("ERROR committing changes.")
        except Exception as some_exception:
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
        except Exception as some_exception:
            logger.error("ERROR running query: %s", str(query))
            logger.exception("ERROR=='%s'", some_exception)

    database_connection.close()
    # logger.debug("output_json==%s", output_json)
    logger.info("STOP")
    return output_json


def pretty_print(this_string):
    """Return a nicely-formatted JSON string.

    Args
    ----
    this_string : str

    Returns
    -------
    : str
    """
    return json.dumps(this_string, indent=4)


def main():
    """Main Function.

    Args
    ----
    None

    Returns
    -------
    None
    """
    start_time = time()

    # Setup Logging Functionality
    logging.basicConfig(
        # pylint: disable=line-too-long
        filename=f"""{log_dict["path"]}{log_dict["prefix"]}{date.today().strftime("%Y%m%d")}.log""",
        filemode="a",
        format="{asctime}  Log Level: {levelname:8}  Line: {lineno:4}  Function: {funcName:21}  Msg: {message}",
        style="{",
        datefmt="%Y-%m-%dT%H:%M:%S",
        level=log_dict["level"],
    )

    logger.info("")
    logger.info("")
    logger.info("")
    logger.info("START START START")
    logger.info(
        "%s %s (%s)",
        app_dict["name"],
        app_dict["version"],
        app_dict["date"],
    )

    logger.info("Running speedtest.py...")
    try:
        process = subprocess.run(["./speedtest.py", "--json"], check=True, capture_output=True)
        speedtest_results = json.loads(process.stdout.decode("utf-8"))
        logger.debug("speedtest_results==%s", pretty_print(speedtest_results))

    except Exception as some_exception:
        speedtest_results = None
        logger.error("ERROR running speed test.")
        logger.exception("EXCEPTION='%s'", str(some_exception))

    if speedtest_results is not None:
        speedtest_list = {}
        speedtest_list["datetime"] = datetime.now().isoformat("T")
        speedtest_list["timestamp"] = int(time())
        speedtest_list["download"] = speedtest_results["download"]
        speedtest_list["upload"] = speedtest_results["upload"]
        speedtest_list["ping"] = speedtest_results["ping"]

        db_placeholders = ", ".join(["%s"] * len(speedtest_list))
        db_columns = ", ".join(speedtest_list.keys())
        query = f"""INSERT INTO {db_dict["schema"] + ".speedtest"} ({db_columns}) VALUES ({db_placeholders})"""

        try:
            db_query(db_dict, query, speedtest_list)
        except Exception as some_exception:
            logger.error("ERROR running db_query")
            logger.exception("EXCEPTION='%s'", str(some_exception))
    else:
        logger.error("Error running speed test.")

    logger.info("Total Execution Time: %s seconds", time() - start_time)
    logger.info("STOP STOP STOP")
    return 0


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    sys.exit(main())
