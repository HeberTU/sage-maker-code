FROM --platform=linux/amd64 python:3.12-slim as builder

ENV PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    POETRY_CACHE_DIR='/var/cache/poetry' \
    ENV=PROD \
    PIP_TRUSTED_HOST="pypi.org files.pythonhosted.org" \
    PYTHONUNBUFFERED=TRUE \
    PYTHONDONTWRITEBYTECODE=TRUE \
    PATH="/opt/program:${PATH}"

RUN apt-get update \
    && apt-get install -y --no-install-recommends  \
    curl \
    libgomp1 \
    nginx \
    wget \
    ca-certificates \
    && apt-get purge -y --auto-remove curl

RUN pip install poetry

FROM builder as  runtime

COPY . /opt/program
COPY ./pyproject.toml  /opt/program
COPY ./poetry.lock* /opt/program

WORKDIR /opt/program

# Make the script executable
RUN chmod +x docker-entrypoint.sh

RUN poetry source add fpho https://files.pythonhosted.org
RUN poetry config certificates.fpho.cert false
RUN poetry source add pypi
RUN poetry config certificates.PyPI.cert false
RUN poetry config certificates.pypi.cert false


#RUN poetry lock --no-update
RUN poetry install -vvv --no-root


# Set our script as the default entrypoint
ENTRYPOINT ["./docker-entrypoint.sh"]