import os
from dotenv import load_dotenv
load_dotenv()
import requests
from flask import Flask, jsonify, render_template
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from datetime import datetime, timezone
import json

app = Flask(__name__)

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")
ZIP_CODE = os.environ.get("ZIP_CODE", "10003")


def get_calendar_service():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as f:
            f.write(creds.to_json())
    return build("calendar", "v3", credentials=creds)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/weather")
def weather():
    if not WEATHER_API_KEY:
        return jsonify({"error": "Missing WEATHER_API_KEY"}), 500

    url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {
        "zip": f"{ZIP_CODE},us",
        "appid": WEATHER_API_KEY,
        "units": "imperial",
        "cnt": 40,
    }
    r = requests.get(url, params=params)
    if r.status_code != 200:
        return jsonify({"error": "Failed to fetch weather"}), 500

    data = r.json()
    current = data["list"][0]

    hourly = []
    for entry in data["list"][:5]:
        hourly.append({
            "time": datetime.fromtimestamp(entry["dt"]).strftime("%-I %p"),
            "temp": round(entry["main"]["temp"]),
            "icon": entry["weather"][0]["icon"],
            "description": entry["weather"][0]["description"].title(),
        })

    today = datetime.now().strftime("%a, %b %d")
    days = {}
    for entry in data["list"]:
        date = datetime.fromtimestamp(entry["dt"]).strftime("%a, %b %d")
        if date == today:
            continue
        if date not in days:
            days[date] = {"temps": [], "descriptions": [], "icons": []}
        days[date]["temps"].append(entry["main"]["temp"])
        days[date]["descriptions"].append(entry["weather"][0]["description"].title())
        days[date]["icons"].append(entry["weather"][0]["icon"])

    forecast = []
    for date, info in list(days.items())[:5]:
        forecast.append({
            "date": date,
            "temp_high": round(max(info["temps"])),
            "temp_low": round(min(info["temps"])),
            "description": info["descriptions"][len(info["descriptions"]) // 2],
            "icon": info["icons"][len(info["icons"]) // 2],
        })

    return jsonify({
        "location": data["city"]["name"],
        "current": {
            "temp": round(current["main"]["temp"]),
            "feels_like": round(current["main"]["feels_like"]),
            "description": current["weather"][0]["description"].title(),
            "humidity": current["main"]["humidity"],
            "icon": current["weather"][0]["icon"],
        },
        "hourly": hourly,
        "forecast": forecast[:5],
    })


@app.route("/api/calendar")
def calendar():
    try:
        service = get_calendar_service()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    now = datetime.now(timezone.utc).isoformat()
    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=now,
            maxResults=10,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )

    events = []
    for e in events_result.get("items", []):
        start = e["start"].get("dateTime", e["start"].get("date"))
        try:
            dt = datetime.fromisoformat(start)
            formatted = dt.strftime("%a, %b %d at %I:%M %p").replace(" 0", " ")
        except Exception:
            formatted = start
        events.append({"title": e.get("summary", "(no title)"), "start": formatted})

    return jsonify({"events": events})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
