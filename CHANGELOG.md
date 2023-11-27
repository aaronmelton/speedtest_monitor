# CHANGELOG

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
