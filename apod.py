"""
Minimal application Astronomy Picture of the Day
Based on Nasa APOD API
"""

import os
import logging
from datetime import datetime
import requests
from flask import Flask, render_template
from werkzeug.middleware.proxy_fix import ProxyFix

URL_ENDPOINT = "https://api.nasa.gov/planetary/apod"
API_KEY = os.environ.get("API_KEY", "DEMO_KEY")

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
# Apply ProxyFix to support running behind a reverse proxy
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)


@app.route("/")
def index():
    """
    Main route: fetches the Astronomy Picture of the Day from NASA API and renders the template
    """
    params = {"api_key": API_KEY}
    try:
        result = requests.get(URL_ENDPOINT, params=params, timeout=10)
        result.raise_for_status()
        content = result.json()
        date = datetime.strptime(content.get("date"), "%Y-%m-%d")
        logging.info(
            "X-Ratelimit-Limit: %s, X-Ratelimit-Remaining: %s",
            result.headers.get("X-Ratelimit-Limit"),
            result.headers.get("X-Ratelimit-Remaining"),
        )
        return render_template(
            "index.html",
            date=date.strftime("%Y %B %d"),
            image_url=content.get("url"),
            image_title=content.get("title"),
            image_copyright=content.get("copyright", "Public domain"),
            explanation=content.get("explanation"),
        )
    except requests.RequestException as e:
        logging.error("Error while calling NASA API: %s", e)
        return render_template(
            "index.html",
            date="N/A",
            image_url="",
            image_title="Retrieval error",
            image_copyright="N/A",
            explanation="Unable to fetch the picture of the day. Please try again later.",
        )


@app.route("/flask-healthz")
def health_check():
    """
    Health check endpoint
    """
    return "success"


if __name__ == "__main__":
    # Run the Flask app with configurable host, port, and debug mode
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000)),
        debug=bool(os.environ.get("DEBUG", False)),
    )
