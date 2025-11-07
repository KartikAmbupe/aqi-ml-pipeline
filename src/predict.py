import joblib
import pandas as pd
from pathlib import Path

# --- CONFIGURATION ---
MODEL_PATH = Path("src/models/model.pkl")

FEATURES = ["co", "no", "no2", "o3", "so2", "pm2_5", "pm10", "nh3"]

sample_data = {
    "co": 500.68,
    "no": 1.58,
    "no2": 10.33,
    "o3": 35.77,
    "so2": 3.65,
    "pm2_5": 14.23,
    "pm10": 20.72,
    "nh3": 5.86
}

def get_aqi_category(aqi):
    """Converts a numerical AQI value (0-500) into a human-readable category."""
    if aqi <= 50:
        return f"Good (AQI: {aqi})"
    elif aqi <= 100:
        return f"Satisfactory (AQI: {aqi})"
    elif aqi <= 200:
        return f"Moderate (AQI: {aqi})"
    elif aqi <= 300:
        return f"Poor (AQI: {aqi})"
    elif aqi <= 400:
        return f"Very Poor (AQI: {aqi})"
    else:
        return f"Severe (AQI: {aqi})"

def predict(data):
    """Loads the model and makes a prediction."""
    
    print("Loading model...")
    try:
        model = joblib.load(MODEL_PATH)
    except FileNotFoundError:
        print(f"Error: Model file not found at {MODEL_PATH}")
        print("Please run 'python src/train.py' first.")
        return

    print("Model loaded successfully.")

    data_df = pd.DataFrame([data])
    data_df = data_df[FEATURES]
    
    print("\nMaking prediction for the following data:")
    print(data_df.to_markdown(index=False))

    prediction = model.predict(data_df)
    predicted_aqi = round(prediction[0], 2)

    category = get_aqi_category(predicted_aqi)
    
    print("\n" + "="*30)
    print(f"  Prediction Result: {category}")
    print("="*30)


if __name__ == "__main__":
    predict(sample_data)