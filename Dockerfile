FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && pip install poetry

COPY pyproject.toml poetry.lock README.md ./
COPY src ./src

RUN poetry install --no-interaction --no-ansi --no-root

COPY .env .env

# Run main.py to populate DB, then start Streamlit
CMD poetry run python src/main.py && poetry run streamlit run src/web-app.py --server.port 8501 --server.address 0.0.0.0