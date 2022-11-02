FROM python:3.10

COPY pyproject.toml .
COPY poetry.lock .

ENV POETRY_VERSION=1.2.2
ENV POETRY_HOME=/etc/poetry
ENV PATH="$POETRY_HOME/bin:$PATH"

RUN apt-get update -y \
    && apt-get install -y libmariadb-dev python-is-python3 dos2unix \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && mkdir -p /usr/local/haunted-manager

WORKDIR /usr/local/haunted-manager
COPY . .
RUN find . -type f -exec dos2unix {} \; \
    && poetry install --only main --no-interaction --no-ansi

EXPOSE 8000

CMD ["/bin/bash", "entrypoint.sh"]
