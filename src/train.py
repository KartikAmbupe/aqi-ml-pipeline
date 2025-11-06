import pandas as pd
import joblib
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.impute import SimpleImputer

# --- Configuration ---
DATA_FILE = Path("data/raw/aqi_data.csv")
MODEL_DIR = Path("src/models")
MODEL_FILE = MODEL_DIR / "model.pkl"
METRICS_FILE = Path("src/metrics.txt") 

TARGET = "aqi"
FEATURES = ["co", "no", "no2", "o3", "so2", "pm2_5", "pm10", "nh3"]

def train_model():
    """Loads data, trains, evaluates, and saves the model."""
    
    print("Starting model training job...")
    
    if not DATA_FILE.exists():
        print(f"Error: Data file not found at {DATA_FILE}")
        print("Please run the ingestion script first.")
        return

    try:
        df = pd.read_csv(DATA_FILE)
    except pd.errors.EmptyDataError:
        print(f"Error: Data file {DATA_FILE} is empty.")
        return

    df = df.dropna(subset=[TARGET])
    
    if df.empty:
        print("Error: No valid data to train on after dropping NaN in target.")
        return

    for col in FEATURES:
        if col not in df.columns:
            df[col] = pd.NA

    imputer = SimpleImputer(strategy='mean')
    df[FEATURES] = imputer.fit_transform(df[FEATURES])

    X = df[FEATURES]
    y = df[TARGET]

    if len(df) < 10:
        print(f"Warning: Very few data samples ({len(df)}). Model will be weak.")
        X_train, X_test, y_train, y_test = X, X, y, y
    else:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("Training RandomForestRegressor...")
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    print(f"Model evaluation complete. Mean Absolute Error (MAE): {mae:.4f}")

    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    joblib.dump(model, MODEL_FILE)
    print(f"Model saved to {MODEL_FILE}")

    with open(METRICS_FILE, 'w') as f:
        f.write(f"Mean Absolute Error (MAE): {mae:.4f}\n")
    print(f"Metrics saved to {METRICS_FILE}")
    
    print("Model training job finished.")

if __name__ == "__main__":
    train_model()