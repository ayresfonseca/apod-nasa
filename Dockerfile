FROM python:3.11.4-slim

LABEL org.opencontainers.image.source="https://github.com/ayresfonseca/apod-nasa"
LABEL org.opencontainers.image.description="Minimal application Astronomy Picture of the Day"
LABEL org.opencontainers.image.licenses="MIT"

ENV WORKERS=2
WORKDIR /app

COPY pyproject.toml ./
COPY poetry.lock ./
COPY apod.py ./
COPY templates ./templates/

RUN  apt-get update && apt-get upgrade -y && apt-get install -y build-essential && \
        rm -rf /var/lib/apt/lists/*
RUN  pip install --no-cache-dir "poetry==1.5.1" && \
        poetry config virtualenvs.create false && \
        poetry install --no-root --without dev

EXPOSE 8000
CMD uwsgi --http 0.0.0.0:8000 --master -p ${WORKERS} -w apod:app
