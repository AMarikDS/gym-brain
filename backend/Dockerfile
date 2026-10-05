FROM python:3.10-slim

ARG HTTP_PROXY
ARG HTTPS_PROXY
ENV HTTP_PROXY=$HTTP_PROXY
ENV HTTPS_PROXY=$HTTPS_PROXY
WORKDIR /app

RUN if [ -n "$HTTP_PROXY" ]; then \
      export HTTP_PROXY=$(echo $HTTP_PROXY | sed -e 's/127.0.0.1/host.docker.internal/g' -e 's/localhost/host.docker.internal/g'); \
    fi; \
    if [ -n "$HTTPS_PROXY" ]; then \
      export HTTPS_PROXY=$(echo $HTTPS_PROXY | sed -e 's/127.0.0.1/host.docker.internal/g' -e 's/localhost/host.docker.internal/g'); \
    fi

ENV POETRY_HTTP_TIMEOUT=1200 \
    PIP_DEFAULT_TIMEOUT=1200

RUN unset HTTP_PROXY HTTPS_PROXY http_proxy https_proxy && pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock* ./

RUN unset HTTP_PROXY HTTPS_PROXY http_proxy https_proxy && poetry config virtualenvs.create false \
    && rm -f poetry.lock \
    && pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu \
    && poetry install --no-interaction --no-ansi --no-root

COPY ./app ./app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
