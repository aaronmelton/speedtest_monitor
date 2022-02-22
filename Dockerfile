########################
# START WITH BASE IMAGE
########################

ARG PYTHON_VER=3.10
ARG APP_NAME=speedtest_monitor

FROM python:${PYTHON_VER} AS base
LABEL prune=true

WORKDIR /usr/src/app

RUN pip install poetry
RUN poetry config virtualenvs.create false

COPY pyproject.toml .
RUN poetry install --no-dev

###################
# BUILD TEST IMAGE
###################

FROM base AS test
LABEL prune=true

RUN poetry install

COPY . .

######################
# PERFORM CODE CHECKS
######################

RUN echo '-->Running Flake8' && \
    flake8 . && \
    echo '-->Running Black' && \
    black --check --diff . && \
    echo '-->Running isort' && \
    find . -name '*.py' | xargs isort && \
    echo '-->Running Pylint' && \
    find . -name '*.py' | xargs pylint --rcfile=pyproject.toml && \
    echo '-->Running pydocstyle' && \
    pydocstyle . --config=pyproject.toml && \
    echo '-->Running Bandit' && \
    bandit --recursive ./ --configfile pyproject.toml

ENTRYPOINT ["pytest"]

CMD ["--color=yes", "-vvv"]

####################
# BUILD FINAL IMAGE
####################

FROM python:${PYTHON_VER}-slim

ARG PYTHON_VER
ARG APP_NAME

WORKDIR /usr/src/app

# Install cron to schedule jobs; curl to pull speedtest binary; libmysqlclient for SQL connectivity
RUN apt-get update && apt-get install --no-install-recommends -y cron curl default-libmysqlclient-dev && \
    apt-get clean

# Install Speedtest CLI
RUN curl -s https://install.speedtest.net/app/cli/install.deb.sh | bash
RUN apt-get update && apt-get install --no-install-recommends -y speedtest && \
    apt-get clean

COPY --from=base /usr/local/lib/python${PYTHON_VER}/site-packages /usr/local/lib/python${PYTHON_VER}/site-packages
COPY $APP_NAME /usr/src/app

ENTRYPOINT ["python", "speedtest_monitor.py"]
