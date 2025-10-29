import sys
import os
from dotenv import load_dotenv
import requests

load_dotenv()
API_URL="https://api.openweathermap.org/data/2.5"
API_KEY=os.getenv("WEATHER_APP_KEY")
if not API_KEY:
    print("Error: Missing API key!")
    sys.exit(1)

def icons(desc: str) -> str:
    d=(desc or "").lower()
    if "thunder" in d: return "⛈️"
    if "drizzle" in d: return "🌦️"
    if "rain" in d: return "🌧️"
    if "snow" in d: return "❄️"
    if "cloud" in d: return "☁️"
    if "clear" in d: return "☀️"
    return "🌡️"

def main():
    city=input("Enter city name: ").strip()
    if not city:
        print("Error! The city must have a name!")
        sys.exit(1)
    url=f"{API_URL}/weather"
    params={"q":city,"appid": API_KEY,"units":"metric","lang":"en"}
    try:
        r=requests.get(url,params=params,timeout=10)
        r.raise_for_status()
        data=r.json()
    except requests.exceptions.HTTPError:
        try:
            msg = r.json().get("message","HTTP error")
        except Exception:
            msg="HTTP error"
        print(f"Error: {msg}")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
        sys.exit(1)
    name=data.get("name",city)
    country=(data.get("sys") or {}).get("country","")
    w=(data.get("weather") or [{}])[0]
    desc=w.get("description","N/A").capitalize()
    m=data.get("main") or {}
    wind=data.get("wind") or {}
    print(f"\nWeather in {name}{', ' + country if country else ''}")
    print("-" * (11 + len(name)))
    print(f"{icons(desc)}  {desc}")
    print(f"Temp:        {m.get('temp', '—')}°C (feels {m.get('feels_like', '—')}°C)")
    print(f"Humidity:    {m.get('humidity', '—')}%")
    print(f"Pressure:    {m.get('pressure', '—')} hPa")
    print(f"Wind:        {wind.get('speed', '—')} m/s")
if __name__ == "__main__":
    main()