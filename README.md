# GovData AI Analyst

GovData AI Analyst is a full-stack data analytics and GenAI project that lets users ask plain-English questions about an official government air quality dataset and receive computed answers, charts, and tables.

The project uses the **EPA AirData Annual AQI by County 2024** dataset. The backend performs deterministic calculations using pandas, while Gemini is used only as an explanation layer for already-computed results. This design avoids letting the LLM invent numbers.

---

## Project Overview

Users can ask questions like:

* Which state has the worst median AQI?
* Which counties had the highest Max AQI?
* Which counties had the most unhealthy days?
* Which pollutant dominated AQI days?
* Compare California and Texas.
* Which state produced the most wheat in 2024?

For supported AQI-related questions, the app returns:

* AI explanation
* Detected intent
* Computed table
* Dynamic chart

For out-of-scope questions, such as crop or agriculture questions, the app refuses clearly because the dataset does not contain that information.

---

## Dataset

**Dataset name:** EPA AirData Annual AQI by County 2024
**Source:** U.S. Environmental Protection Agency
**Dataset link:** https://aqs.epa.gov/aqsweb/airdata/annual_aqi_by_county_2024.zip

Main columns include:

* State
* County
* Year
* Good Days
* Moderate Days
* Unhealthy for Sensitive Groups Days
* Unhealthy Days
* Very Unhealthy Days
* Hazardous Days
* Max AQI
* Median AQI
* Days CO
* Days NO2
* Days Ozone
* Days PM2.5
* Days PM10

---

## Tech Stack

### Frontend

* React
* Vite
* Axios
* Recharts
* CSS

### Backend

* FastAPI
* Pandas
* Python
* Gemini API
* Uvicorn

### Data / AI Design

* pandas is used for actual calculations
* Gemini is used only to explain computed results
* The model is not allowed to directly generate or execute arbitrary code
* Out-of-scope questions are refused

---

## System Architecture

```text
React Frontend
    ↓
FastAPI Backend
    ↓
Question Intent Detection
    ↓
Pandas Analytics Functions
    ↓
EPA AQI Dataset
    ↓
Gemini Explanation Layer
    ↓
Answer + Table + Chart
```

---

## Folder Structure

```text
govdata-ai-analyst/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   │
│   │   ├── data/
│   │   │   └── annual_aqi_by_county_2024.csv
│   │   │
│   │   ├── routers/
│   │   │   ├── health_router.py
│   │   │   ├── analytics_router.py
│   │   │   └── chat_router.py
│   │   │
│   │   ├── services/
│   │   │   ├── data_service.py
│   │   │   ├── analytics_service.py
│   │   │   ├── chat_service.py
│   │   │   └── llm_service.py
│   │   │
│   │   └── schemas/
│   │       └── chat_schema.py
│   │
│   ├── requirements.txt
│   └── .env
│
└── frontend/
    ├── src/
    │   ├── App.jsx
    │   ├── App.css
    │   └── main.jsx
    │
    ├── package.json
    └── vite.config.js
```

---

## Backend Setup

Go to the backend folder:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the environment on Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file inside the `backend` folder:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Run the backend:

```bash
uvicorn app.main:app --reload
```

Backend will run at:

```text
http://127.0.0.1:8000
```

Open API docs:

```text
http://127.0.0.1:8000/docs
```

---

## Frontend Setup

Go to the frontend folder:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Install required frontend libraries:

```bash
npm install axios recharts
```

Run the frontend:

```bash
npm run dev
```

Frontend will run at:

```text
http://localhost:5173
```

---

## API Endpoints

### Health Check

```http
GET /api/health
```

Checks if the backend is running.

### Dataset Summary

```http
GET /api/analytics/summary
```

Returns dataset row count, columns, number of states, and year range.

### Top States by Median AQI

```http
GET /api/analytics/top-states
```

Returns states ranked by average Median AQI.

### Worst Counties by Max AQI

```http
GET /api/analytics/worst-counties
```

Returns counties ranked by Max AQI.

### Most Unhealthy Counties

```http
GET /api/analytics/unhealthy-counties
```

Returns counties ranked by total unhealthy days.

### Pollutant Summary

```http
GET /api/analytics/pollutants
```

Returns pollutant-day totals for CO, NO2, Ozone, PM2.5, and PM10.

### Chat Endpoint

```http
POST /api/chat/ask
```

Request body:

```json
{
  "question": "Which state has the worst median AQI?"
}
```

Example response:

```json
{
  "answer": "Based on the EPA AirData Annual AQI by County 2024 dataset, California has the highest average Median AQI...",
  "intent": "top_states_by_median_aqi",
  "data": [
    {
      "State": "California",
      "Median AQI": 47.87
    }
  ],
  "chart": {
    "type": "bar",
    "x_key": "State",
    "y_key": "Median AQI",
    "title": "Top States by Average Median AQI"
  }
}
```

---

## Supported Questions

The current version supports these question categories:

1. Top states by average Median AQI
2. Counties with highest Max AQI
3. Counties with most unhealthy days
4. Pollutant summary
5. California vs Texas comparison
6. Out-of-scope refusal

Example supported questions:

```text
Which state has the worst median AQI?
Which counties had the highest Max AQI?
Which counties had the most unhealthy days?
Which pollutant dominated AQI days?
Compare California and Texas.
```

Example out-of-scope question:

```text
Which state produced the most wheat in 2024?
```

Expected response:

```text
I cannot answer this from the selected dataset because the EPA AQI dataset does not contain agriculture or crop production data.
```

---

## Correctness and Trust

The LLM does not calculate numbers directly. The backend uses pandas to compute all metrics from the dataset.

For example, for the question:

```text
Which state has the worst median AQI?
```

The backend:

1. Loads the cleaned EPA AQI dataset
2. Groups rows by `State`
3. Calculates average `Median AQI`
4. Sorts values in descending order
5. Returns the top results
6. Sends the computed result to Gemini only for explanation

This prevents the model from fabricating numbers.

---

## Screenshots



```markdown
<img width="1920" height="1020" alt="Screenshot 2026-06-05 135821" src="https://github.com/user-attachments/assets/f7f55c88-96bd-4217-897b-4dbfeb4ed1eb" />


<img width="1920" height="1020" alt="Screenshot 2026-06-05 135807" src="https://github.com/user-attachments/assets/074202e1-0a9f-4615-969a-673078349c26" />


<img width="1920" height="1020" alt="Screenshot 2026-06-05 135751" src="https://github.com/user-attachments/assets/71754cad-2e2e-41c9-a3b1-2ef2b2139ff7" />

```

---

## Key Learning Outcomes

Through this project, I learned:

* How to build a FastAPI backend with a clean layered structure
* How to connect React frontend with backend APIs
* How to use pandas for reliable data analytics
* How to design a safer GenAI system where the LLM explains results instead of inventing numbers
* How to return chart-ready metadata from backend to frontend
* How to handle out-of-scope user questions
* How to structure a project for both assignment submission and resume use

---

## Limitations

This is a prototype and has some limitations:

* It supports only predefined question types
* Intent detection is keyword-based
* It uses one CSV file instead of a database
* Gemini may fail if API quota is exhausted
* It does not yet include user authentication or persistent audit logs
* It does not support hundreds of datasets or complex joins

---

## Future Improvements

Possible improvements:

* Replace keyword routing with a safer structured query planner
* Add DuckDB or PostgreSQL for larger datasets
* Add authentication and role-based access control
* Store audit logs for every user query
* Add downloadable reports
* Add better frontend filters and dashboard cards
* Add automated tests for each supported question
* Support more government datasets

---

## Project Status

Completed:

* FastAPI backend
* React frontend
* EPA AQI dataset integration
* Pandas analytics
* Gemini explanation layer
* Chart and table rendering
* Out-of-scope refusal
* Gradio Colab version for assignment demo

---
