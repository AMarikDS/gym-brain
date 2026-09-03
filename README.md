# Gym Brain AI

A Two-Stage AI Recommender System (Transformer + CatBoost) for dynamic fitness workouts, providing personalized exercise sequencing and target weight predictions.

## 🧠 AI Pipeline & Data Flow

This project follows a Microservices architecture powered by a 3-stage Machine Learning pipeline:

### 1. Candidate Generation (TransformerRec / BERT)
- **What it does:** Acts as the brain for sequencing, understanding the context of your workout.
- **Input:** A sequence of past exercise IDs (your current workout history).
- **Output:** A list of Top-N potential next exercises, scored by their contextual relevance (`bert_score`).

### 2. Reranking (CatBoost Ranker)
- **What it does:** Filters and personalizes the raw AI suggestions.
- **Input:** User profile (Sex, Age, Bodyweight, Goal, Level, Equipment constraints) + Candidate exercises from the Transformer.
- **Output:** A re-ranked list of exercises sorted by a personalized relevance score (`final_score`).

### 3. Target Regression (CatBoost Regressor Pro / Light)
- **What it does:** Accurately predicts the optimal working weight and reps for your next exercise.
- **Input:** The selected exercise + User profile (+ SBD 1RM stats for the Pro model).
- **Output:** Predicted optimal weight (kg) and target repetitions.

## 🛠 Tech Stack
- **Machine Learning**: PyTorch, CatBoost, Pandas
- **Backend**: FastAPI, Uvicorn, Pydantic, Poetry
- **Frontend**: Reflex (Reactive Python UI framework)
- **Infrastructure**: Docker, Docker Compose

## How to Run Locally

1. Clone the repository:
```bash
git clone https://github.com/AMarikDS/gym-brain.git
cd gym-brain
```

2. Start the services using Docker Compose:
```bash
docker compose up --build
```

3. Access the web interface:
Open [http://localhost:3001](http://localhost:3001) in your browser.

4. Access the API documentation:
Open [http://localhost:8001/docs](http://localhost:8001/docs) in your browser.

## Project Structure

- `models/` - Contains all machine learning weights and mappings (`vocab.json`, `*.cbm`, `*.pth`).
- `backend/` - FastAPI application, REST endpoints, and ML inference service.
- `frontend/` - Reflex UI application.
- `notebooks/` - Original Jupyter notebooks used for training the models and exploring data (Excluded from Git).
