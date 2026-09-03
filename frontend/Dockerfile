FROM python:3.10-slim

WORKDIR /app

# Reflex uses nodejs underneath and requires unzip for bun installation
RUN apt-get update && apt-get install -y curl unzip gcc python3-dev && \
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir poetry

COPY pyproject.toml ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

COPY . .

RUN reflex init

EXPOSE 3000

CMD ["reflex", "run", "--env", "prod"]
