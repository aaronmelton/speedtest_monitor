# CHANGELOG

## [0.7.1] - 2024-09-19
### Fixed
- entrypoint.sh: Corrected the wrong flag.  /facepalm


## [0.7.0] - 2024-09-19
### Changed
- Moved code that calls Speedtest binary into its own function to improve code
  reuse.
- Added an argument/flag to show test results (pull) and insert them into a
  database (pull-push).
- Improved code to remove static path to the speedtest bin and have the script
  dynamically-determine where the binary is.


## [0.6.2] - 2024-09-17
### Changed
- Bumping all Python packages to most recent version.
- Changed environment variables so they will be unique.
- Cleaning up Dockerfiles to be more in line with my other projects.


## [0.6.1] - 2024-07-18
### Changed
- Bumping all Python packages to most recent version.


## [0.6.0] - 2024-05-17
### Changed
- Bumping Python to 3.12 and updating all library versions.
- Dockerfile: Updating file to be more in line with the format I use for all
  my projects.
- docker-compose.yml: Pointing environment values to the system's environment
  instead of a blank string.
- Renamed some_list -> some_dict because its a dict and not a list.
- Updating Speedtest to the newest versions introduced new changes:
- Added --secure option to the command line
- Speedtest JSON output changed so the speedtest_dict{} had to be updated to
  match.  This also required a change to the SQL INSERT query.
- grafana_dashboard.json: Renamed bandwidth -> throughput (since that is what
  we're actually measuring); Adjusted any math from 0.000008 to 0.000001 to
  correct the values the tool reports (bits instead of bytes); Removed the
  Duration panel as the newest version of Speedtest doesnt track it.
- speedtest_database.sql: Removed columns no longer tracked by the newest
  version of Speedtest.


## [0.5.0] - 2024-03-20
### Changed
- Converted speedtest data type from list to dict.
- Removing gitdb (4.0.11)
- Removing gitpython (3.1.40)
- Removing smmap (5.0.1)
- Updating certifi (2023.11.17 -> 2024.2.2)
- Updating urllib3 (2.1.0 -> 2.2.1)
- Updating typing-extensions (4.8.0 -> 4.10.0)
- Updating azure-core (1.29.5 -> 1.30.1)
- Updating cryptography (41.0.5 -> 42.0.5)
- Updating packaging (23.2 -> 24.0)
- Updating pluggy (1.3.0 -> 1.4.0)
- Updating astroid (3.0.1 -> 3.1.0)
- Updating azure-storage-blob (12.19.0 -> 12.19.1)
- Updating dill (0.3.7 -> 0.3.8)
- Updating isort (5.12.0 -> 5.13.2)
- Updating pathspec (0.11.2 -> 0.12.1)
- Updating platformdirs (4.0.0 -> 4.2.0)
- Updating pytest (7.4.3 -> 7.4.4)
- Updating rich (13.7.0 -> 13.7.1)
- Updating slack-sdk (3.26.0 -> 3.27.1)
- Updating stevedore (5.1.0 -> 5.2.0)
- Updating tomlkit (0.12.3 -> 0.12.4)
- Updating aaron-common-libs (0.1.1 4688216 -> 0.1.2 4162593)
- Updating bandit (1.7.5 -> 1.7.8)
- Updating black (23.11.0 -> 23.12.1)
- Updating coverage (7.3.2 -> 7.4.4)
- Updating mysqlclient (2.2.0 -> 2.2.4)
- Updating pylint (3.0.2 -> 3.1.0)
- Updating pytest-env (1.1.1 -> 1.1.3)


## [0.4.0] - 2023-11-26
### Added
- tests/test_class_Config.py: Poor excuse for a unit test file.
### Changed
- .gitignore: Updating project-specific files.
- README.md: Minor clarification to the instructions.
- pyproject.toml: Bumped Python to v3.12; Python functions consolidated into
  a new code repository, aaron-common-libs, which is now imported into this
  script; speedtest-cli is now installed via Poetry; Bumped all development
  test packages to latest versions.
- speedtest_monitor/config.py, speedtest_monitor/speedtest_monitor.py: 
  Refactored most functions: Config, logging setup, SQL calls.
### Removed
- docker-compose.yml, Dockerfile: Is anyone using Docker to run a basic
  Python script?
- flake8: No longer required with changes to pyproject.toml


## [0.3.2] - 2022-02-22
### Added
- docker-compose.yml: Adding docker-compose file for ease of use.
### Changed
- README.md: Improving instructions for Docker.
- Dockerfile: Adding pruning labels.
- Updating click (8.0.3 -> 8.0.4)
- Updating gitpython (3.1.26 -> 3.1.27)
- Updating platformdirs (2.4.1 -> 2.5.1)
- Updating typing-extensions (4.0.1 -> 4.1.1)


## [0.3.1] - 2022-02-07
### Changed
- Dockerfile: Improved Dockerfile.
- pyproject.toml: Reduced Docker image size by moving packages required for
  dev only into [tool.poetry.dev-dependencies]
- Bumped pbr (5.8.0 -> 5.8.1)

## [0.3.0] - 2022-02-04
### Added
- Added Dockerfile.
### Changed
- Changed path to the speedtest binary.  If you're not using Docker, you'll need
  to install the speedtest binary on your computer and/or change the path.
- Added the `--accept-license` argument to speedtest, otherwise it wouldn't work
  if you haven't run speedtest and accepted the license prior to running the
  Python script.
- Renamed instances of bandwidth to throughput (what we're actually measuring).
- Bumped bandit v1.7.1 -> v1.7.2

## [0.2.0] - 2022-01-24
### Added
- Added schema structure to the project.
- Added Grafana dashboard export to the project.
- pyproject.toml[bandit]: Ignoring info-warnings about subprocess.
### Changed
- Switched from using Silva's speedtest-cli to Ookla's speedtest CLI binary.
  Both produce JSON format output that can be collected.  Decided to switch to
  Ookla's binary since the vendor provides JSON output too.
- README.md: Updated to reflect changes in the project; Included screenshot of
  dashboard.
- speedtest_list{} and SQL table also had to change to capture additional
  information Ookla's JSON output provided that I wanted to capture.

## [0.1.0] - 2022-01-16
### Added
- Creating a new project to collect speedtest.net results and store them in a
  database.
