# Deploying ML Pipeline with FastAPI

This project demonstrates a complete Machine Learning pipeline for the Census Income Prediction task. It includes data processing, model training, and deployment using FastAPI and Docker.

## Project Structure

```
Deploying-ML-Pipeline-with-FastAPI/
├── data/                   # Dataset files
├── ml/                     # Machine learning modules (data processing, model definition)
├── model/                  # Saved model artifacts (encoder, model.pkl)
├── Experimentation/        # Jupyter notebooks for EDA
├── main.py                 # FastAPI application
├── train_model.py          # Script to train the model
├── evaluation.py           # Script to evaluate model performance
├── Dockerfile              # Docker configuration
├── requirements.txt        # Python dependencies
└── ...
```

## Features

*   **Machine Learning:** XGBoost Classifier trained on Census Income data.
*   **API:** FastAPI for serving real-time predictions.
*   **Containerization:** Docker support for easy deployment.
*   **Data Versioning:** DVC integration (configured).
*   **Testing:** Unit tests for ML components (if applicable).

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Lali182k5/Deploying-ML-Pipeline-with-FastAPI.git
    cd Deploying-ML-Pipeline-with-FastAPI
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # Linux/Mac
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### 1. Train the Model
To retrain the model using the data in `data/census_cleaned_data.csv`:
```bash
python train_model.py
```
This will save the trained model and encoder to the `model/` directory.

### 2. Run the API Locally
Start the FastAPI server using Uvicorn:
```bash
uvicorn main:app --reload
```
The API will be available at `http://127.0.0.1:8000`.

### 3. Docker Deployment
Build and run the application using Docker:

**Build the image:**
```bash
docker build -t fastapi-ml-app .
```

**Run the container:**
```bash
docker run -p 8000:8000 fastapi-ml-app
```

## API Endpoints

### `GET /`
Returns a welcome message.

### `POST /data/`
Predicts whether income is `<=50K` or `>50K`.

**Example Request Body:**
```json
{
  "age": 37,
  "workclass": "Private",
  "education": "HS-grad",
  "education-num": 10,
  "marital-status": "Married-civ-spouse",
  "occupation": "Prof-specialty",
  "relationship": "Husband",
  "race": "White",
  "sex": "Male",
  "capital-gain": 0,
  "capital-loss": 0,
  "hours-per-week": 40,
  "native-country": "United-States"
}
```

**Example Response:**
```json
{
  "result": "<=50K"
}
```

## Documentation
Once the app is running, visit `http://localhost:8000/docs` for the interactive Swagger UI documentation.
