# personal-dashboard

A personal dashboard web app built with Flask that displays real-time weather data and upcoming Google Calendar events in one place. It pulls current conditions, hourly forecasts, and a 5-day outlook from OpenWeatherMap, and shows your next 10 calendar events using the Google Calendar API.

---

## Setup

### 1. Clone the repo

```bash
git clone git@github.com:Rephase/playground1.git
cd playground1
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your API keys

Copy the example env file and fill in your values:

```bash
cp .env.example .env
```

Open `.env` and set:

- `WEATHER_API_KEY` - your [OpenWeatherMap](https://openweathermap.org) API key (free tier)
- `ZIP_CODE` - your zip code (default is 10003)

### 5. Add Google Calendar credentials

Follow the [Google Calendar API quickstart](https://developers.google.com/calendar/api/quickstart/python) to create OAuth credentials. Download the credentials JSON and save it as `credentials.json` in the project root.

On first run, a browser window will open asking you to authorize access to your calendar. After that, a `token.json` file is saved and you won't be prompted again.

---

## Running

Make sure the virtual environment is active by going to your local repository:

```bash
source venv/bin/activate
```

Then:

```bash
python3 app.py
```

Open `http://localhost:5000` in your browser.

You can deactivate your virtual environent with:

```bash
deactivate
```

> Note: each time you open a new terminal session, run `source venv/bin/activate` before starting the app.
