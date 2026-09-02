# Gym Brain AI 🏋️‍♂️🧠

A Two-Stage AI Recommender System (Transformer + CatBoost) for dynamic fitness workouts, providing personalized exercise sequencing and target weight predictions.

## Architecture 🏛

This project follows a Microservices architecture using modern Python tooling:

1. **Candidate Generation (TransformerRec / BERT)**: Encodes the user's workout history and generates candidate exercises.
2. **Reranking (CatBoost Classifier)**: Takes the top candidates and reranks them based on user context (Level, Goal, Equipment) and muscle group continuity.
3. **Target Regression (CatBoost Regressor - Pro/Light)**: Predicts the optimal working weight and reps for the next chosen exercise. The "Pro" version leverages known 1RM stats (Squat, Bench, Deadlift) for extreme accuracy, while the "Light" version solves the cold-start problem using standard demographics.
4. **Backend (FastAPI)**: Serves the Machine Learning models via a high-performance REST API.
5. **Frontend (Reflex)**: A reactive and modern web application UI that communicates with the Backend.

## Tech Stack ⚙️
- **Machine Learning**: PyTorch, CatBoost, Pandas
- **Backend**: FastAPI, Uvicorn, Pydantic, Poetry
- **Frontend**: Reflex
- **Infrastructure**: Docker, Docker Compose

## How to Run Locally 🐳

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

## Project Structure 📁

- `backend/` - FastAPI application, REST endpoints, ML service, and model assets (`vocab.json`, `*.cbm`, `*.pth`).
- `frontend/` - Reflex UI application.
- `notebooks/` - Original Jupyter notebooks used for training the models and exploring data.
