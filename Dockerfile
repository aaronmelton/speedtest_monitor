##################
### BASE IMAGE ###
##################

ARG PYTHON_VER=3.10

FROM python:${PYTHON_VER} AS base

WORKDIR /usr/src/speedtest_monitor

RUN pip install poetry
RUN poetry config virtualenvs.create false

COPY pyproject.toml .

RUN poetry install --no-dev

##################
### TEST IMAGE ###
##################

FROM base AS test

RUN poetry install

COPY . .

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

###################
### FINAL IMAGE ###
###################

FROM python:${PYTHON_VER}-slim

ARG PYTHON_VER

WORKDIR /usr/src/speedtest_monitor

RUN apt-get update && apt-get install --no-install-recommends -y cron curl default-libmysqlclient-dev && \
    apt-get clean

# Install Speedtest CLI
RUN curl -s https://install.speedtest.net/app/cli/install.deb.sh | bash
RUN apt-get update && apt-get install --no-install-recommends -y speedtest && \
    apt-get clean

COPY --from=base /usr/local/lib/python${PYTHON_VER}/site-packages /usr/local/lib/python${PYTHON_VER}/site-packages

COPY speedtest_monitor/*.py /usr/src/speedtest_monitor/

ENTRYPOINT ["python", "speedtest_monitor.py"]
