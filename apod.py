"""
Minimal application Astronomy Picture of the Day
Based on Nasa APOD API
"""
from datetime import datetime
import requests
from flask import Flask
from flask import render_template

URL_ENDPOINT = "https://api.nasa.gov/planetary/apod"
API_KEY = "DEMO_KEY"

app = Flask(__name__)


@app.route("/")
def index():
    """
    Index function
    """

    params = {"api_key": API_KEY}

    result = requests.get(URL_ENDPOINT, params=params, timeout=10)
    content = result.json()
    date = datetime.strptime(content.get("date"), "%Y-%m-%d")
    print(
        f'X-Ratelimit-Limit: {result.headers.get("X-Ratelimit-Limit")}, X-Ratelimit-Remaining: {result.headers.get("X-Ratelimit-Remaining")}'
    )

    return render_template(
        "index.html",
        date=date.strftime("%Y %B %d"),
        image_url=content.get("url"),
        image_title=content.get("title"),
        image_copyright=content.get("copyright", "Public domain"),
        explanation=content.get("explanation"),
    )
