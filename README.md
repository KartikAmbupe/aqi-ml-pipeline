# 🌤️ Air Quality MLOps Project

[![GitHub Actions Workflow Status](https://github.com/KartikAmbupe/aqi-ml-pipeline/actions/workflows/main.yml/badge.svg)](https://github.com/KartikAmbupe/aqi-ml-pipeline/actions)

A minimal MLOps pipeline for a college assignment demonstrating automated data ingestion, model training, and deployment for **Air Quality in Mumbai, India**.

This project fulfills the **"DevOps + AI"** requirement by creating a fully automated CI/CD pipeline using GitHub Actions, which handles the complete machine learning lifecycle.

---

## 🧩 1. Project Overview

This repository contains all the code for an **end-to-end MLOps pipeline** that:

* **Ingests** daily real-time air quality data from the **OpenWeatherMap API**.
* **Stores** this data in a historical CSV, which grows over time.
* **Trains** a machine learning model (`RandomForestRegressor`) to predict the **Air Quality Index (AQI)** based on pollutant components (CO, NO₂, PM₂.₅, etc.).
* **Evaluates** the new model and saves its performance metrics.
* **Deploys** the new model by automatically committing updated artifacts back to the repository.

---

## ⚙️ 2. The MLOps Pipeline (DevOps + AI)

The core of this project is the automated workflow defined in `.github/workflows/main.yml`.
This pipeline runs on a **daily schedule** or on any **push** to the `main` branch.

### 🔁 Automated Workflow

1. **Trigger:**
   The workflow is triggered by:

   * A schedule (`cron`)
   * A push to `main`
   * Manual trigger (`workflow_dispatch`)

2. **Setup:**
   A new Ubuntu runner (`ubuntu-latest`) is provisioned and Python dependencies are installed via `requirements.txt`.

3. **Ingest:**
   The script `src/data_ingestion.py` runs and uses the secret `OPENWEATHER_API_KEY` to fetch the latest air quality data for **Mumbai**.

4. **Append:**
   The new data row is appended to `data/raw/aqi_data.csv`, maintaining a growing historical dataset.

5. **Train:**
   The script `src/train.py` loads the dataset, performs preprocessing (imputation), and trains a **Random Forest Regressor** model.

6. **Evaluate:**
   Model performance is evaluated using **Mean Absolute Error (MAE)**, and results are written to `src/metrics.txt`.

7. **Deploy (Commit):**
   The updated files (`aqi_data.csv`, `model.pkl`, and `metrics.txt`) are automatically committed to the repository.
   This automated commit represents **deployment**, as the model is now the “live” artifact in production.

### 🔄 Workflow Summary

```
[Daily Schedule] → [GitHub Action Job] → [Run data_ingestion.py] → [Run train.py] → [Commit New Model & Data]
```

---

## 🧰 3. Technology Stack

| Layer                    | Tools Used                   |
| ------------------------ | ---------------------------- |
| **Programming Language** | Python 3.10                  |
| **Data Science**         | Pandas, Scikit-learn, Joblib |
| **Automation / CI-CD**   | GitHub Actions               |
| **Data Source**          | OpenWeatherMap API           |

---

## 🗂️ 4. Project Structure

```
.
├── .github/
│   └── workflows/
│       └── main.yml              # The automated MLOps pipeline
│
├── data/
│   └── raw/
│       └── aqi_data.csv          # Historical + appended daily data
│
├── src/
│   ├── models/
│   │   └── model.pkl             # The deployed model artifact
│   ├── data_ingestion.py         # Fetches new data for Mumbai
│   ├── train.py                  # Trains and evaluates the model
│   ├── prepare_initial_data.py   # Seeds the project with initial data
│   └── metrics.txt               # Latest model performance metrics
│
├── .gitignore
├── city_day.csv                  # Raw Kaggle dataset (ignored by git)
├── README.md
└── requirements.txt
```

---

## 🚀 5. Setup & Installation

Follow these steps to run and automate the project locally.

### Step 1: Clone the Repository

```bash
git clone https://github.com/KartikAmbupe/aqi-ml-pipeline.git
cd aqi-ml-pipeline
```

---

### Step 2: Set Up the Initial Dataset

1. Download the **city_day.csv** file from the Kaggle dataset
   **"Air Quality Data in India (2015–2020)"**.
   [https://www.kaggle.com/datasets/rohanrao/air-quality-data-in-india](https://www.kaggle.com/datasets/rohanrao/air-quality-data-in-india)

2. Place the downloaded file in the project root folder.

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the one-time setup script to create the initial dataset for **Mumbai**:

```bash
python src/prepare_initial_data.py
```

This will generate `data/raw/aqi_data.csv` containing thousands of historical records.

---

### Step 3: Run the First Training

Run the training script to build your baseline model:

```bash
python src/train.py
```

This will generate:

* `src/models/model.pkl`
* `src/metrics.txt`

---

### Step 4: Set Up GitHub Secrets

1. Get a free API key from [OpenWeatherMap](https://openweathermap.org/api).
2. In your GitHub repository:

   * Go to **Settings → Secrets and variables → Actions**
   * Click **New repository secret**
   * Add:

     * **Name:** `OPENWEATHER_API_KEY`
     * **Value:** *Your API key here*

---

### Step 5: Push to GitHub

Commit and push all files:

```bash
git add .
git commit -m "feat: initial project setup with baseline model"
git push origin main
```

Your push will trigger the **first GitHub Action**, which:

* Retrains your model
* Evaluates it
* Commits updated data and model artifacts automatically

From then on, the pipeline runs **daily** — fully automated!