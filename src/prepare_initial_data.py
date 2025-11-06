import pandas as pd
from pathlib import Path

# --- Configuration ---
RAW_DATA_FILE = "../city_day.csv"
TARGET_CITY = "Mumbai"
DATA_DIR = Path("data/raw")
FINAL_DATA_FILE = DATA_DIR / "aqi_data.csv"

FINAL_COLUMNS = [
    "timestamp",
    "aqi",
    "co",
    "no",
    "no2",
    "o3",
    "so2",
    "pm2_5",
    "pm10",
    "nh3"
]

print(f"Starting initial data preparation for {TARGET_CITY}...")

try:
    df = pd.read_csv(RAW_DATA_FILE)
except FileNotFoundError:
    print(f"Error: '{RAW_DATA_FILE}' not found.")
    print("Please download it from Kaggle and place it in the project root.")
    exit()

df_city = df[df["City"] == TARGET_CITY].copy()
if df_city.empty:
    print(f"Error: No data found for city '{TARGET_CITY}'.")
    exit()

column_map = {
    "Date": "timestamp",
    "AQI": "aqi",
    "PM2.5": "pm2_5",
    "PM10": "pm10",
    "NO": "no",
    "NO2": "no2",
    "NH3": "nh3",
"CO": "co",
    "SO2": "so2",
    "O3": "o3"
}
df_city.rename(columns=column_map, inplace=True)

df_final = df_city[FINAL_COLUMNS].copy()

DATA_DIR.mkdir(parents=True, exist_ok=True)

df_final.to_csv(FINAL_DATA_FILE, index=False)

print(f"Successfully prepared initial data for '{TARGET_CITY}'.")
print(f"Saved {len(df_final)} rows to {FINAL_DATA_FILE}")