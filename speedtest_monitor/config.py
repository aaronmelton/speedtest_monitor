"""Config file required to support Speedtest Monitor."""

# !/usr/bin/env python
# -*- coding: utf-8 -*-
#

from dataclasses import dataclass
from datetime import datetime
from os import environ as os_environ


@dataclass
class Config:
    """Class for Application variables."""

    def __init__(self):
        """Application Variables."""
        self.app_dict = {
            "author": "Aaron Melton <aaron@aaronmelton.com>",
            "date": "2024-09-19",
            "desc": "A Python script to capture speedtest JSON and insert it into a database.",
            "title": "speedtest_monitor",
            "url": "https://github.com/aaronmelton/speedtest_monitor",
            "version": "0.7.1",
        }

        # Logging Variables
        self.log_dict = {
            "filename": f"""{os_environ.get("SPEEDTEST_LOG_PATH", "log/")}{self.app_dict["title"]}_{datetime.now().strftime("%Y%m%d")}.log""",
            "level": os_environ.get("SPEEDTEST_LOG_LEVEL", "INFO"),
            "path": os_environ.get("SPEEDTEST_LOG_PATH", "./log/"),
        }

        # Database Variables
        self.db_dict = {
            "host": os_environ.get("SPEEDTEST_DB_HOSTNAME"),
            "username": os_environ.get("SPEEDTEST_DB_USERNAME"),
            "password": os_environ.get("SPEEDTEST_DB_PASSWORD"),
            "schema_name": os_environ.get("SPEEDTEST_DB_SCHEMA"),
            "table_name": os_environ.get("SPEEDTEST_DB_TABLE"),
        }
