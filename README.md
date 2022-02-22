# Speedtest Monitor

A Python script to capture speedtest JSON and insert it into a database.

![speedtest_monitor.png](speedtest_monitor.png)

## Getting Started

### About This Code
This script was written to track internet speed using Ookla's speed test.

This repository contains the SQL schema and the Grafana dashboard JSON so you can track your own metrics.

### Prerequisites
* [speedtest binary from Ookla](https://www.speedtest.net/apps/cli); I'm using the Linux binary here.  (Installed automatically if using Dockerfile.)
* MySQL database, built with the [database/speedtest_database.sql](https://github.com/aaronmelton/speedtest_monitor/blob/master/database/speedtest_database.sql) schema,  to store results.
* Set environment variables (DB_HOST, DB_USERNAME, DB_PASSWORD, DB_SCHEMA) in `docker-compose.yml` OR in your environment if not using Docker.

#### Python Libraries
* See [pyproject.toml](pyproject.toml)

### Instructions For Use

#### Running Python Natively
* To run the Python script:
`python speedtest_monitor.py`

#### Docker Commands
_(All Docker commands must be run from the cloned directory or you must specify the path and filename to docker-compose.yml.)_

* To pull/build the necessary Docker images:

`docker-compose build`

* To run the application:

`docker-compose run --rm speedtest_monitor`

* To remove intermediate build images (no longer required after `docker-compose build`):

`docker image prune --filter "label=prune=true"`

#### Grafana
* In order to use the provided `grafana_dashboard.json` file, you'll need to use the SQL schema provided in `speedtest_database.sql` AND a Grafana MySQL Data Source named "SpeedTest".

## Acknowledgements
* Grafana dashboard layout borrowed from [speedtest_exporter](https://github.com/danopstech/speedtest_exporter).

## Authors
* **Aaron Melton** - *Author* - Aaron Melton <aaron@aaronmelton.com>
