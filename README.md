# Speedtest Monitor

A Python script to capture speedtest JSON and insert it into a database.

![speedtest_monitor.png](speedtest_monitor.png)

## Getting Started

### About This Code
This script was written to track internet speed using Ookla's speed test.

This repository contains the SQL schema and the Grafana dashboard JSON so you can track your own metrics.

### Prerequisites
* [speedtest binary from Ookla](https://www.speedtest.net/apps/cli); I'm using the Linux binary here.  (Installed automatically if using Dockerfile.)
* MySQL database to store results.
* Set environment variables (see config.py).

#### Python Libraries
* See [pyproject.toml](pyproject.toml)

### Instructions For Use

#### Running Python Natively
* To run the Python script:
`python speedtest_monitor.py`

#### Docker Commands
* To build the Docker image:
`docker build -t speedtest_monitor .`

* To run inside Docker:
`docker run --rm -e <env vars> speedtest_monitor:latest`

#### Grafana
* In order to use the provided `grafana_dashboard.json` file, you'll need to use the SQL schema provided in `speedtest_database.sql` AND a Grafana MySQL Data Source named "SpeedTest".

## Acknowledgements
* Grafana dashboard layout borrowed from [speedtest_exporter](https://github.com/danopstech/speedtest_exporter).

## Authors
* **Aaron Melton** - *Author* - Aaron Melton <aaron@aaronmelton.com>
