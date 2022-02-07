"""Config file required to support Speedtest Monitor."""
# !/usr/bin/env python
# -*- coding: utf-8 -*-
#

import os

# Application Variables
app_dict = {
    "author": "Aaron Melton <aaron@aaronmelton.com>",
    "date": "2022-02-07",
    "desc": "A Python script to capture speedtest JSON and insert it into a database.",
    "name": "speedtest_monitor.py",
    "title": "Speedtest Monitor",
    "url": "https://github.com/aaronmelton/speedtest_monitor",
    "version": "v0.3.1",
}

# Logging Variables
log_dict = {
    "level": os.environ.get("LOG_LEVEL"),
    "path": os.environ.get("LOG_PATH"),
    "prefix": os.environ.get("LOG_PREFIX"),
}

# Database Variables
db_dict = {
    "host": os.environ.get("DB_HOST"),
    "username": os.environ.get("DB_USERNAME"),
    "password": os.environ.get("DB_PASSWORD"),
    "schema": os.environ.get("DB_SCHEMA"),
}
