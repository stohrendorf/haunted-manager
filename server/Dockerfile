FROM python:3.10

COPY pyproject.toml .
COPY poetry.lock .

ENV POETRY_VERSION=1.8.5
ENV POETRY_HOME=/etc/poetry
ENV PATH="$POETRY_HOME/bin:$PATH"
ARG TEAMCITY_VERSION=""

RUN apt-get update -y \
    && apt-get install -y --no-install-recommends libmariadb-dev python-is-python3 \
    && rm -rf /var/lib/apt/lists/* \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && mkdir -p /usr/local/haunted-manager

WORKDIR /usr/local/haunted-manager
COPY . .
RUN chmod a+x manage.py \
    && poetry install --no-interaction --no-ansi \
    && poetry run coverage run -m pytest \
    && poetry run coverage report

EXPOSE 8000

CMD ["/bin/bash", "entrypoint.sh"]
