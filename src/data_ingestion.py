import os
import requests
import pandas as pd
from pathlib import Path
from datetime import datetime

# --- Configuration ---
# Mumbai, India
LAT = 19.0760
LON = 72.8777

API_KEY = os.environ.get("OPENWEATHER_API_KEY")
API_URL = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={LAT}&lon={LON}&appid={API_KEY}"

DATA_DIR = Path("data/raw")
DATA_FILE = DATA_DIR / "aqi_data.csv"

def fetch_aqi_data():
    """Fetches the current air quality data from OpenWeatherMap."""
    if not API_KEY:
        print("Error: OPENWEATHER_API_KEY environment variable not set.")
        print("Please set this as a GitHub Secret.")
        return None
        
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()

        if "list" in data and len(data["list"]) > 0:
            return data["list"][0]
        else:
            print("Error: Unexpected API response format.")
            print(data)
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def process_and_save_data(api_data):
    """Processes the API response and appends it to the CSV file."""
    if api_data is None:
        return

    flat_data = {}
    flat_data["timestamp"] = datetime.utcfromtimestamp(api_data["dt"]).isoformat()
    flat_data["aqi"] = api_data["main"]["aqi"]

    for component, value in api_data["components"].items():
        flat_data[component] = value

    df = pd.DataFrame([flat_data])

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if not DATA_FILE.exists():
        df.to_csv(DATA_FILE, index=False, mode='w', header=True)
        print(f"Created new data file and saved first entry to {DATA_FILE}")
    else:
        df.to_csv(DATA_FILE, index=False, mode='a', header=False)
        print(f"Appended new data to {DATA_FILE}")

def main():
    print(f"Starting data ingestion job for Mumbai (Lat: {LAT}, Lon: {LON})...")
    api_data = fetch_aqi_data()
    if api_data:
        process_and_save_data(api_data)
    print("Data ingestion job finished.")

if __name__ == "__main__":
    main()