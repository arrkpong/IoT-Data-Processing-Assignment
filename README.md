# IoT Data Processing Assignment

## Overview

This project implements a backend service that processes IoT time-series data (temperature, humidity, and air quality) and provides API endpoints for data ingestion, cleaning, anomaly detection, and aggregation of sensor statistics.

## Tech Stack

* **Backend**: Django REST Framework (DRF)
* **Frontend**: Vite + Vue 3 + TypeScript
* **Database**: SQLite
* **Data Processing**: Pandas, NumPy, SciPy
* **Charting**: Chart.js

---

## Backend Setup (Django REST Framework)

```bash
git clone https://github.com/arrkpong/IoT-Data-Processing-Assignment.git
cd IoT-Data-Processing-Assignment
pip install -r backend/requirements.txt
python backend/manage.py migrate
python backend/manage.py runserver
```

API is available at:
`http://127.0.0.1:8000/`

---

## Frontend Setup (Vue 3 + TypeScript)

```bash
cd frontend
npm install
npm run dev
```

Frontend is available at:
`http://localhost:5173/`

---

## API Testing with Postman

To simplify testing, a Postman collection is included.

### Steps to Import:

1. Open **Postman**
2. Click **Import** > **File**
3. Select the file:
   `postman_collection/iot_data_processing_collection.json`
4. Collection includes:

   * `Ingest Sensor Data`
   * `Fetch Processed Data`
   * `Fetch Aggregated Statistics`

---

## API Endpoints

### 1. Ingest Sensor Data

**POST** `http://127.0.0.1:8000/api/sensors/data/`

Request body:

```json
{
  "timestamp": "2023-05-10T12:00:00Z",
  "temperature": 22.5,
  "humidity": 60.0,
  "air_quality": 55.0
}
```

---

### 2. Fetch Processed Data

**GET** `http://127.0.0.1:8000/api/sensors/processed/`

Response example:

```json
[
  {
    "timestamp": "2023-05-10T12:00:00Z",
    "temperature": 22.5,
    "temperature_anomaly": 0,
    "humidity": 60.0,
    "humidity_anomaly": 0,
    "air_quality": 55.0,
    "air_quality_anomaly": 0
  }
]
```

---

### 3. Fetch Aggregated Statistics

**GET** `http://127.0.0.1:8000/api/sensors/aggregated/?window=1H`

Response example:

```json
{
  "temperature_mean": [22.4],
  "temperature_median": [22.5],
  "temperature_min": [20.0],
  "temperature_max": [25.0],
  "humidity_mean": [60.1],
  "humidity_median": [60.0],
  "humidity_min": [55.0],
  "humidity_max": [65.0],
  "air_quality_mean": [54.8],
  "air_quality_median": [55.0],
  "air_quality_min": [50.0],
  "air_quality_max": [60.0]
}
```

---

## Data Processing Pipeline

* **Duplicate Removal**: Based on timestamp
* **Missing Data**: Interpolated using time-based strategy
* **Anomaly Detection**:

  * Z-score method (|Z| > 3 → anomaly)
* **Aggregation**:

  * Rolling stats by time window (mean, median, min, max)

---

## Docker Setup (Optional)

```bash
docker-compose up --build
```

This will spin up both the backend and frontend containers.

---

## License

This project is licensed under the **MIT License**.
