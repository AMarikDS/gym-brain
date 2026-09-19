<div align="center">
  <h1>Gym Brain AI</h1>
  <p><b>Hyper-Personalized Fitness Intelligence</b></p>
  
  <br />

  <p>
    <img src="https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB" alt="React"/>
    <img src="https://img.shields.io/badge/Vite-B73BFE?style=for-the-badge&logo=vite&logoColor=FFD62E" alt="Vite"/>
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
    <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI"/>
    <img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white" alt="PyTorch"/>
    <img src="https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white" alt="Docker"/>
  </p>

  <br />
  
  <blockquote>
    <p><i>A Two-Stage AI Recommender System (Transformer + CatBoost) for dynamic fitness workouts, providing personalized exercise sequencing and target predictions through a premium Light Glassmorphism UI.</i></p>
  </blockquote>
</div>

<hr/>

## Key Features

- **Interactive Wizard UI**: Step-by-step workout initialization gathering biological stats, available equipment, and 1RM maxes.
- **Dynamic Contextual Predictions**: Generates target metrics automatically formatting them based on exercise type (e.g. `+10 kg x 10 reps` for Bodyweight vs `15 mins` for Cardio).
- **Strict Data Validation**: Real-time client-side and backend validation to prevent dirty inputs and absurd predictions.
- **Workout Trajectory Engine**: Auto-scrollable session workspace with Undo/Restart features for continuous planning.

<br />

## AI Pipeline & Data Flow

This project follows a Microservices architecture powered by a 3-stage Machine Learning pipeline.

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
- **Output:** Predicted optimal dynamic target (kg/reps/mins).

<br />

## Tech Stack

- **Machine Learning**: PyTorch, CatBoost, Pandas
- **Backend**: FastAPI, Uvicorn, Pydantic, Poetry
- **Frontend**: React, Vite, Vanilla CSS (Light Glassmorphism Design System)
- **Infrastructure**: Docker, Docker Compose, Nginx

<br />

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

3. Access the web interface (Wizard):
Open [http://localhost:3001](http://localhost:3001) in your browser.

4. Access the API documentation:
Open [http://localhost:8001/docs](http://localhost:8001/docs) in your browser.

<br />

## Project Structure

- `models/` - Contains all machine learning weights and mappings (`vocab.json`, `*.cbm`, `*.pth`).
- `backend/` - FastAPI application, REST endpoints, and ML inference service.
- `frontend/` - React/Vite Single Page Application with Nginx reverse proxy.
- `notebooks/` - Original Jupyter notebooks used for training the models and exploring data.
