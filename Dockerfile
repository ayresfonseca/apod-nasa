FROM python:3.12.10-slim

LABEL org.opencontainers.image.source="https://github.com/ayresfonseca/apod-nasa"
LABEL org.opencontainers.image.description="Minimal application Astronomy Picture of the Day"
LABEL org.opencontainers.image.licenses="MIT"

ENV WORKERS=2
WORKDIR /app

# Install build dependencies and clean up
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends build-essential gcc && \
    rm -rf /var/lib/apt/lists/*

# Copy only what is needed for dependency installation first (for better Docker cache)
COPY pyproject.toml ./
COPY poetry.lock ./

# Install Poetry and project dependencies
RUN pip install --no-cache-dir "poetry==2.0.1" && \
    poetry config virtualenvs.create false && \
    poetry install --without dev

# Copy application code and templates
COPY apod.py ./
COPY templates ./templates/

EXPOSE 8000

# Use exec form and explicit module for better reliability
CMD ["uwsgi", "--http", "0.0.0.0:8000", "--master", "-p", "2", "-w", "apod:app"]
