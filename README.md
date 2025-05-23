# apod-nasa

Minimal application Astronomy Picture of the Day based on the [NASA APOD API](https://api.nasa.gov/).

## Features

- Fetches and displays the Astronomy Picture of the Day from NASA.
- Simple Flask web interface.
- Docker support.
- Health check endpoint at `/flask-healthz`.

## Requirements

- Python 3.12+
- [Poetry](https://python-poetry.org/) for dependency management

## Installation

```bash
git clone https://github.com/ayresfonseca/apod-nasa.git
cd apod-nasa
poetry install
```

## Usage

### Local

```bash
export API_KEY=your_nasa_api_key  # Optional, defaults to DEMO_KEY
poetry run python apod.py
```

The app will be available at [http://localhost:8000](http://localhost:8000).

### Docker

```bash
docker build -t apod-nasa .
docker run -e API_KEY=<your_nasa_api_key> -p 8000:8000 apod-nasa
```

## Configuration

- `API_KEY`: NASA API key (default: `DEMO_KEY`)
- `PORT`: Port to run the app (default: `8000`)
- `DEBUG`: Set to `True` for debug mode (default: `False`)

## Health Check

A health check endpoint is available at `/flask-healthz`.

## License

MIT
