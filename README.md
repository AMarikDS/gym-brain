<div align="center">
  <h1>Gym Brain</h1>
  <p><b>Two-Stage Recommender System for Fitness Workouts</b></p>
  
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

  <!-- PLACEHOLDER FOR VIDEO: Once you record a video, we will replace this image with:
  <video src="docs/demo.mp4" autoplay loop muted width="800" style="border-radius: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.1);"></video> -->
  
</div>

<hr/>

## 🚀 BigTech & Highload Инференс (Triton, TensorRT, JIT)

В проекте реализован **C++ TorchScript (JIT)** движок для инференса Трансформера, симулирующий стандарты BigTech (Triton Inference Server). 

### Почему не чистый PyTorch?
Обычный PyTorch имеет большой overhead из-за GIL (Global Interpreter Lock) и динамического графа вычислений (Python overhead). Для production-ready 1000+ RPS это неприемлемо. Мы скомпилировали модель в **TorchScript (JIT)** — это позволяет запускать её полностью в среде C++ (LibTorch) без участия Python.

### Сравнение технологий (Production Stack)
1. **TorchScript JIT (Реализовано):** Компилирует модель в статичный граф, который можно использовать в C++ или Rust. Ускоряет инференс на CPU и GPU, используется как нативный бэкенд в **NVIDIA Triton Inference Server**.
2. **ONNX Runtime:** Универсальный C++ движок от Microsoft, который часто дает максимальную производительность на CPU за счет агрессивного слияния слоев (graph optimization).
3. **TensorRT:** Проприетарный движок от NVIDIA. Оптимизирует веса конкретно под архитектуру вашего чипа (например, T4, A100), квантизует в FP16/INT8. Дает максимальный FPS на GPU.
4. **Triton Inference Server & Kubernetes:** В BigTech сами модели оборачивают не в FastAPI, а в Triton, который через gRPC принимает батчи запросов от пользователей (Dynamic Batching) и загружает GPU на 100%. Затем всё это скейлится в K8s.

### 📊 Benchmark (1000 запросов)
Проведенный нагрузочный тест показал значительный **Бизнес-эффект** от компиляции модели:
* **PyTorch (Python):** p99 Latency = `4.023 ms` | Mean = `2.556 ms`
* **C++ JIT (LibTorch):** p99 Latency = `2.546 ms` | Mean = `2.183 ms`

✅ **Бизнес-эффект:** C++ движок оказался в **1.6 раз быстрее** на 99-м перцентиле (p99). Это радикально снижает потребление ресурсов железа и гарантирует стабильное время ответа при спайках нагрузки (highload).

<br />

## Key Features

- **Interactive Wizard UI**: Step-by-step workout initialization gathering biological stats, available equipment, and 1RM metrics.
- **Dynamic Contextual Predictions**: Generates target metrics formatted based on exercise type.
- **Data Validation**: Real-time client-side and backend validation to prevent dirty inputs.
- **Workout Trajectory Engine**: Auto-scrollable session workspace with Undo and Restart features.

<br />

## Pipeline Architecture

This project follows a microservices architecture powered by a 3-stage Machine Learning pipeline.

### 1. Candidate Generation
- **Model**: TransformerRec (BERT architecture).
- **Input**: Sequence of past exercise IDs.
- **Output**: Top-N potential next exercises scored by contextual relevance.

### 2. Reranking
- **Model**: CatBoost Ranker.
- **Input**: User profile and candidate exercises.
- **Output**: Re-ranked list of exercises sorted by personalized relevance score.

### 3. Target Regression
- **Model**: CatBoost Regressor.
- **Input**: Selected exercise and user profile.
- **Output**: Predicted optimal dynamic target (weight, reps, or time).

<br />

## Tech Stack

- **Machine Learning**: PyTorch, CatBoost, Scikit-learn, Pandas, NumPy
- **Backend**: FastAPI, Uvicorn, Pydantic, Poetry
- **Frontend**: React, Vite, Vanilla CSS
- **Infrastructure**: Docker, Nginx

<br />

## How to Run Locally

1. Clone the repository:
```bash
git clone https://github.com/AMarikDS/gym-brain.git
cd gym-brain
```

2. Start the services using Docker Compose:
```bash
# Optional: If you are behind a corporate proxy, you must pass it to the build process:
# docker compose build --build-arg HTTP_PROXY=$HTTP_PROXY --build-arg HTTPS_PROXY=$HTTPS_PROXY backend

docker compose up --build -d
```

3. Access the web interface:
Open [http://localhost:3001](http://localhost:3001) in your browser.

4. Access the API documentation:
Open [http://localhost:8001/docs](http://localhost:8001/docs) in your browser.

<br />

## Project Structure

- `models/` - Machine learning weights and mappings.
- `backend/` - FastAPI application and ML inference service.
- `frontend/` - React SPA with Nginx reverse proxy.
- `notebooks/` - Jupyter notebooks for model training and data exploration.
