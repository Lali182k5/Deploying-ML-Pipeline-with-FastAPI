# 🚀 Deploying ML Pipeline with FastAPI

## 📌 Overview
This project demonstrates an end-to-end **machine learning inference pipeline** exposed through a **FastAPI-based REST API**. The primary focus is on **backend design, request validation, and deployment structure**, with machine learning used as a supporting component rather than a black box.

The project uses the Census Income dataset to predict whether an individual earns `<=50K` or `>50K`. It now also contains **DataWise AI**, a production-ready natural-language-to-SQL layer with schema grounding, SQL safety, caching, and data quality checks.

---

## 🎯 Problem Statement
Machine learning models are often trained but not deployed in a structured, production-ready way. This project shows how a trained model can be:
- validated,
- served through an API,
- and packaged for deployment using Docker.

---

## 🏗 Project Structure
    Deploying-ML-Pipeline-with-FastAPI/
    ├── data/ # Dataset files
    ├── ml/ # Data processing and model logic
    ├── model/ # Saved model artifacts (encoder, model.pkl)
    ├── Experimentation/ # Jupyter notebooks for EDA
    ├── main.py # FastAPI application
    ├── train_model.py # Script to train the model
    ├── evaluation.py # Model evaluation script
    ├── Dockerfile # Docker configuration
    ├── requirements.txt # Python dependencies
    └── README.md


The codebase is organized to clearly separate **data processing**, **model logic**, and **API serving**.


## 🧠 How the System Works
- Raw census data is processed and cleaned.
- A machine learning model is trained and evaluated offline.
- The trained model and encoders are saved for inference.
- FastAPI loads the model at startup.
- Incoming API requests are validated and passed to the prediction pipeline.
- Predictions are returned as structured JSON responses.


## 🛠️ Tech Stack
- **Python**
- **FastAPI**
- **scikit-learn / XGBoost**
- **Pydantic**
- **Uvicorn**
- **Docker**

---

## 📥 Installation

### Clone the repository
```
git clone https://github.com/Lali182k5/Deploying-ML-Pipeline-with-FastAPI.git
cd Deploying-ML-Pipeline-with-FastAPI
```

### Create a virtual environment
```
python -m venv venv
# Windows
.\venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### Install dependencies
```
pip install -r requirements.txt
```

---

## ▶️ Usage

### 1. Train the Model
```
python train_model.py
```
This saves trained model artifacts to the model/ directory.

### 2. Run the API Locally
```
uvicorn main:app --reload
```
The API will be available at:
```
http://127.0.0.1:8000
```
### 3. Docker Deployment
Build the image
```
docker build -t fastapi-ml-app .
```
Run the container
```
docker run -p 8000:8000 fastapi-ml-app
```

## 🔌 API Endpoints

### DataWise AI endpoints
- `GET /` health message
- `GET /schema` returns schema snapshot (live Postgres if configured, otherwise sample schema)
- `POST /query` converts NL → SQL, validates, executes safely, runs data-quality checks, and returns results, SQL, confidence, and insights
- `GET /history` returns recent queries

Run locally:
```
uvicorn main:app --reload
```

Sample request:
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "Show revenue by customer", "filters": {}, "limit": 10}'
```
The response includes the SQL used, parameter values, data quality warnings, insights, and a table-ready payload.

## 📘 Documentation

Interactive API documentation is available via Swagger UI:
```
http://localhost:8000/docs
```

For the full production blueprint (architecture, deployment, extension ideas) see [ARCHITECTURE.md](ARCHITECTURE.md).

## 📌 Key Learnings

- Deploying ML inference using FastAPI
- Structuring backend APIs with validation
- Separating training and serving logic
- Packaging applications using Docker

## 📄 License

This project is licensed under the MIT License.




